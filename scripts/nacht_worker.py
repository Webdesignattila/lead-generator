"""
nacht_worker.py: Autonome Doorwerk-Wachtrij voor het Mainframe van Webdesign Attila.

Voert alle taken uit wachtrij.json achter elkaar uit, zonder te stoppen, en houdt bij:
  * wachtrij.json          : de taken en hun status (wachtend / bezig / klaar / fout / overgeslagen)
  * wachtrij_status.json   : live voortgang (voor het blok op http://localhost:8080)
  * logs/nacht_worker.log  : logboek

Starten:
    python scripts/nacht_worker.py            # alle wachtende taken
    python scripts/nacht_worker.py --reset    # alle taken terug naar "wachtend" en starten
    python scripts/nacht_worker.py --stop     # lopende worker netjes laten stoppen

Taaktypes (veld "type" in wachtrij.json):
    leads_opschonen    params: csv
    mailronde          params: csv, max_mails, pauze_min_sec, pauze_max_sec, droog, venster,
                               onderwerp, template, afmeldregel
                       env:    SMTP_HOST, SMTP_PORT (587), SMTP_USER, SMTP_PASS,
                               SMTP_TLS (starttls|ssl|geen), MAIL_AFZENDER, MAIL_NAAM
    demo_voorbereiden  params: csv, max, map
    commando           params: cmd (lijst of tekst), timeout_sec, map
    wacht              params: seconden
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import smtplib
import subprocess
import sys
import time
import traceback
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr, make_msgid

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)
sys.path.insert(0, HIER)

import lead_filter  # noqa: E402

WACHTRIJ = os.path.join(BASIS, "wachtrij.json")
STATUS = os.path.join(BASIS, "wachtrij_status.json")
STOPBESTAND = os.path.join(BASIS, "wachtrij.stop")
LOCK = os.path.join(BASIS, "wachtrij.lock")
LOGMAP = os.path.join(BASIS, "logs")
LOGBOEK = os.path.join(LOGMAP, "nacht_worker.log")
VERZONDEN = os.path.join(BASIS, "mail_verzonden.csv")

_status: dict = {}


# ---------------------------------------------------------------------------
# Hulpfuncties
# ---------------------------------------------------------------------------

def nu() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pad(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(BASIS, p)


def schrijf_json(bestand: str, data) -> None:
    tmp = bestand + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    for poging in range(5):  # Windows: bestand kan heel even open zijn bij het dashboard
        try:
            os.replace(tmp, bestand)
            return
        except PermissionError:
            time.sleep(0.2 * (poging + 1))
    os.replace(tmp, bestand)


def lees_json(bestand: str, standaard=None):
    try:
        with open(bestand, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return standaard


def log(tekst: str, niveau: str = "INFO") -> None:
    os.makedirs(LOGMAP, exist_ok=True)
    regel = f"{nu()} [{niveau}] {tekst}"
    print(regel, flush=True)
    with open(LOGBOEK, "a", encoding="utf-8") as f:
        f.write(regel + "\n")
    _status.setdefault("log", []).append(regel)
    _status["log"] = _status["log"][-40:]
    bewaar_status()


def bewaar_status(**velden) -> None:
    _status.update(velden)
    _status["bijgewerkt"] = nu()
    schrijf_json(STATUS, _status)


def stop_gevraagd() -> bool:
    return os.path.exists(STOPBESTAND)


def slaap(seconden: float) -> bool:
    """Slaapt in stapjes; geeft False terug als er een stop is gevraagd."""
    eind = time.time() + seconden
    while time.time() < eind:
        if stop_gevraagd():
            return False
        time.sleep(min(1.0, eind - time.time()))
    return True


def voortgang(gedaan: int, totaal: int, tekst: str = "") -> None:
    bewaar_status(taak_voortgang={"gedaan": gedaan, "totaal": totaal, "tekst": tekst})


def lees_leads(csv_pad: str) -> list[dict]:
    _, rijen, _, _ = lead_filter._lees_csv(csv_pad)
    return rijen


def slug(tekst: str) -> str:
    t = lead_filter._normaal(tekst)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60] or "lead"


# ---------------------------------------------------------------------------
# Taken
# ---------------------------------------------------------------------------

def taak_leads_opschonen(p: dict) -> str:
    csv_pad = pad(p.get("csv", "echte_leads.csv"))
    r = lead_filter.schoon_csv(csv_pad, dedup=p.get("dedup", True),
                               voortgang=lambda i, n: voortgang(i, n, "rijen gecontroleerd"))
    redenen = ", ".join(f"{k}: {v}" for k, v in r["redenen"].items()) or "geen"
    return (f"{r['totaal']} rijen → {r['behouden']} behouden, {r['verwijderd']} verwijderd "
            f"({redenen}); backup: {os.path.basename(r['backup'])}")


STANDAARD_TEMPLATE = """Hoi {naam},

Ik kwam {bedrijf} tegen{plaats_tekst} en heb even naar {website_tekst} gekeken. Ik denk dat daar met
een snelle, moderne website meer klanten uit te halen zijn, vooral op mobiel.

Ik heb alvast een korte demo voor jullie klaargezet. Zal ik die sturen?

Groet,
{afzender}
Webdesign Attila
"""


def _al_verzonden() -> set[str]:
    if not os.path.exists(VERZONDEN):
        return set()
    with open(VERZONDEN, encoding="utf-8") as f:
        return {r["email"].strip().lower() for r in csv.DictReader(f) if r.get("email")}


def _markeer_verzonden(email: str, bedrijf: str) -> None:
    nieuw = not os.path.exists(VERZONDEN)
    with open(VERZONDEN, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nieuw:
            w.writerow(["datum", "email", "bedrijf"])
        w.writerow([nu(), email, bedrijf])


def _binnen_venster(venster) -> bool:
    if not venster:
        return True
    uur = datetime.now().hour
    van, tot = int(venster[0]), int(venster[1])
    return van <= uur < tot if van < tot else (uur >= van or uur < tot)


def taak_mailronde(p: dict) -> str:
    """Veilige mailronde: filter, nooit dubbel mailen, limiet per ronde, willekeurige pauzes,
    alleen binnen het tijdvenster, afmeldregel. Standaard DROOG (er gaat niets de deur uit)."""
    csv_pad = pad(p.get("csv", "echte_leads.csv"))
    max_mails = int(p.get("max_mails", 20))
    pmin, pmax = int(p.get("pauze_min_sec", 90)), int(p.get("pauze_max_sec", 240))
    droog = bool(p.get("droog", True))
    venster = p.get("venster", [8, 20])
    onderwerp = p.get("onderwerp", "Idee voor de website van {bedrijf}")
    template = STANDAARD_TEMPLATE
    if p.get("template"):
        template = open(pad(p["template"]), encoding="utf-8").read()
    afmeld = p.get("afmeldregel",
                   "\n\nGeen interesse? Antwoord met 'afmelden' en je hoort niets meer van mij.")

    smtp_cfg = {k: os.getenv(k) for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS",
                                          "SMTP_TLS", "MAIL_AFZENDER", "MAIL_NAAM")}
    if not droog and not smtp_cfg["SMTP_HOST"]:
        raise RuntimeError("Echte mailronde vraagt SMTP_HOST (en meestal SMTP_USER/SMTP_PASS) als "
                           "omgevingsvariabelen. Zet ze, of laat \"droog\": true staan.")

    while not droog and not _binnen_venster(venster):
        log(f"Buiten mailvenster {venster[0]}:00–{venster[1]}:00, wacht 10 minuten…")
        if not slaap(600):
            return "gestopt voor de mailronde begon"

    verzonden = _al_verzonden()
    kandidaten = []
    for rij in lees_leads(csv_pad):
        email = lead_filter._kies(rij, lead_filter.EMAIL_KOLOMMEN).strip()
        if not email or "@" not in email or email.lower() in verzonden:
            continue
        if lead_filter.rij_geblokkeerd(rij):
            continue
        kandidaten.append((email, rij))
    kandidaten = kandidaten[:max_mails]
    log(f"Mailronde: {len(kandidaten)} ontvangers (max {max_mails}, "
        f"{'DROOG, er wordt niets verstuurd' if droog else 'ECHT versturen'})")

    server = None
    afzender = smtp_cfg["MAIL_AFZENDER"] or smtp_cfg["SMTP_USER"] or ""
    if not droog and "@" not in afzender:
        raise RuntimeError("Zet MAIL_AFZENDER (of een SMTP_USER met e-mailadres) voor een echte mailronde.")
    naam_afzender = smtp_cfg["MAIL_NAAM"] or "Attila"
    verstuurd = 0
    try:
        for i, (email, rij) in enumerate(kandidaten, 1):
            if stop_gevraagd():
                break
            if not droog and not _binnen_venster(venster):
                log("Mailvenster gesloten, rest van de ronde overgeslagen.")
                break
            bedrijf = lead_filter._kies(rij, lead_filter.NAAM_KOLOMMEN) or "jullie bedrijf"
            website = lead_filter._kies(rij, lead_filter.WEBSITE_KOLOMMEN)
            plaats = rij.get("plaats") or rij.get("stad") or rij.get("city") or ""
            velden = {
                "naam": rij.get("contactpersoon") or bedrijf, "bedrijf": bedrijf,
                "website": website, "website_tekst": website or "jullie online vindbaarheid",
                "plaats": plaats, "plaats_tekst": f" in {plaats}" if plaats else "",
                "afzender": naam_afzender,
            }
            tekst = template.format_map(_Leeg(velden)) + afmeld
            sub = onderwerp.format_map(_Leeg(velden))
            if droog:
                log(f"  [droog {i}/{len(kandidaten)}] → {email} | {sub}")
            else:
                if server is None:
                    poort = int(smtp_cfg["SMTP_PORT"] or 587)
                    tls = (smtp_cfg["SMTP_TLS"] or ("ssl" if poort == 465 else "starttls")).lower()
                    if tls == "ssl":
                        server = smtplib.SMTP_SSL(smtp_cfg["SMTP_HOST"], poort, timeout=30)
                    else:
                        server = smtplib.SMTP(smtp_cfg["SMTP_HOST"], poort, timeout=30)
                        if tls == "starttls":
                            server.starttls()
                    if smtp_cfg["SMTP_USER"] and smtp_cfg["SMTP_PASS"]:
                        server.login(smtp_cfg["SMTP_USER"], smtp_cfg["SMTP_PASS"])
                msg = EmailMessage()
                msg["From"] = formataddr((naam_afzender, afzender))
                msg["To"] = email
                msg["Subject"] = sub
                msg["Message-ID"] = make_msgid()
                msg["List-Unsubscribe"] = f"<mailto:{afzender}?subject=afmelden>"
                msg.set_content(tekst)
                server.send_message(msg)
                _markeer_verzonden(email, bedrijf)
                log(f"  [verstuurd {i}/{len(kandidaten)}] → {email}")
            verstuurd += 1
            voortgang(i, len(kandidaten), "mails")
            if i < len(kandidaten):
                pauze = random.randint(pmin, pmax) if not droog else min(2, pmax)
                if not slaap(pauze):
                    break
    finally:
        if server is not None:
            try:
                server.quit()
            except Exception:
                pass
    return f"{verstuurd} {'gesimuleerd (droog)' if droog else 'verstuurd'} van {len(kandidaten)}"


class _Leeg(dict):
    def __missing__(self, k):
        return ""


def taak_demo_voorbereiden(p: dict) -> str:
    csv_pad = pad(p.get("csv", "echte_leads.csv"))
    doelmap = pad(p.get("map", "demos"))
    maximum = int(p.get("max", 10))
    os.makedirs(doelmap, exist_ok=True)
    gemaakt, overgeslagen = 0, 0
    rijen = [r for r in lees_leads(csv_pad) if not lead_filter.rij_geblokkeerd(r)]
    for i, rij in enumerate(rijen, 1):
        if gemaakt >= maximum or stop_gevraagd():
            break
        bedrijf = lead_filter._kies(rij, lead_filter.NAAM_KOLOMMEN)
        if not bedrijf:
            continue
        map_ = os.path.join(doelmap, slug(bedrijf))
        brief = os.path.join(map_, "brief.md")
        if os.path.exists(brief):
            overgeslagen += 1
            continue
        os.makedirs(map_, exist_ok=True)
        gegevens = "\n".join(f"| {k} | {v} |" for k, v in rij.items() if k and v)
        with open(brief, "w", encoding="utf-8") as f:
            f.write(f"""# Demo-brief: {bedrijf}

> Aangemaakt door nacht_worker op {nu()}. Bouw met: `/website-bouwer demos/{slug(bedrijf)}`

## Leadgegevens
| veld | waarde |
|---|---|
{gegevens}

## Opdracht
- Bouw een demo-homepage voor **{bedrijf}** volgens `.claude/skills/website-bouwer/SKILL.md`
  (design-taste-frontend: hero-entree, één scroll-moment, hover-laag, perf-check).
- Bepaal de soort (service / place) uit de branche.
- Huidige site: {lead_filter._kies(rij, lead_filter.WEBSITE_KOLOMMEN) or "geen eigen website"}. Noem in de
  oplevering 3 concrete verbeterpunten t.o.v. de huidige situatie (voor de mail).
- Geen verzonnen adres, telefoon of KvK. Foto's: stand-ins, gemarkeerd.

## Status
- [ ] demo gebouwd (`index.html`)
- [ ] gate PASS
- [ ] gemaild
""")
        gemaakt += 1
        voortgang(gemaakt, min(maximum, len(rijen)), "demo-briefs")
        log(f"  demo-brief: {os.path.relpath(brief, BASIS)}")
    return f"{gemaakt} nieuwe demo-briefs in {os.path.relpath(doelmap, BASIS)} ({overgeslagen} bestonden al)"


def taak_commando(p: dict) -> str:
    cmd = p["cmd"]
    if isinstance(cmd, str):
        cmd = cmd.split()
    cmd = [sys.executable if c in ("python", "python3", "py") else c for c in cmd]
    timeout = int(p.get("timeout_sec", 3600))
    cwd = pad(p.get("map", "."))
    log(f"  commando: {' '.join(cmd)} (timeout {timeout}s)")
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace",
                            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"})
    begin = time.time()
    regels = 0
    try:
        for regel in proc.stdout:
            regels += 1
            log(f"    | {regel.rstrip()[:300]}")
            if stop_gevraagd() or time.time() - begin > timeout:
                proc.terminate()
                break
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
    if time.time() - begin > timeout:
        raise RuntimeError(f"timeout na {timeout}s")
    if proc.returncode not in (0, None) and not stop_gevraagd():
        raise RuntimeError(f"exitcode {proc.returncode}")
    return f"klaar ({regels} regels output, {int(time.time() - begin)}s)"


def taak_wacht(p: dict) -> str:
    s = int(p.get("seconden", 60))
    return f"{s}s gewacht" if slaap(s) else "wachten onderbroken"


TAKEN = {
    "leads_opschonen": taak_leads_opschonen,
    "mailronde": taak_mailronde,
    "demo_voorbereiden": taak_demo_voorbereiden,
    "commando": taak_commando,
    "wacht": taak_wacht,
}


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

def _pid_leeft(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True,
                             text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def draait_al() -> int | None:
    try:
        pid = int(open(LOCK).read().strip())
    except (FileNotFoundError, ValueError):
        return None
    return pid if _pid_leeft(pid) and pid != os.getpid() else None


def zeg_klaar() -> None:
    ps1 = os.path.join(HIER, "zeg_klaar.ps1")
    if os.name == "nt" and os.path.exists(ps1):
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1],
                       timeout=60)
    else:
        log("zeg_klaar.ps1 overgeslagen (alleen op Windows).")


def draai(reset: bool = False) -> int:
    andere = draait_al()
    if andere:
        print(f"Er draait al een nacht_worker (PID {andere}).")
        return 2
    open(LOCK, "w").write(str(os.getpid()))
    if os.path.exists(STOPBESTAND):
        os.remove(STOPBESTAND)

    wachtrij = lees_json(WACHTRIJ)
    if not wachtrij or not isinstance(wachtrij.get("taken"), list):
        print(f"Geen geldige wachtrij gevonden in {WACHTRIJ}")
        os.remove(LOCK)
        return 1
    if reset:
        for t in wachtrij["taken"]:
            t.update(status="wachtend", resultaat=None, gestart=None, klaar=None)
        schrijf_json(WACHTRIJ, wachtrij)
    inst = wachtrij.get("instellingen", {})

    _status.clear()
    bewaar_status(draait=True, pid=os.getpid(), gestart=nu(), klaar=None, huidige_taak=None,
                  taak_voortgang=None, totaal=len(wachtrij["taken"]), log=[])
    te_doen = [t for t in wachtrij["taken"] if t.get("status", "wachtend") in ("wachtend", "bezig")]
    log(f"Nacht-worker gestart: {len(te_doen)} taken in de wachtrij.")
    fouten = 0
    try:
        for n, taak in enumerate(te_doen, 1):
            if stop_gevraagd():
                log("Stop gevraagd: worker stopt na de huidige taak.", "WAARSCHUWING")
                break
            soort = taak.get("type")
            naam = taak.get("naam") or soort
            functie = TAKEN.get(soort)
            taak.update(status="bezig", gestart=nu(), resultaat=None)
            schrijf_json(WACHTRIJ, wachtrij)
            bewaar_status(huidige_taak={"nummer": n, "van": len(te_doen), "id": taak.get("id"),
                                        "naam": naam}, taak_voortgang=None)
            log(f"▶ Taak {n}/{len(te_doen)}: {naam}")
            try:
                if functie is None:
                    raise ValueError(f"onbekend taaktype '{soort}' (kies uit {', '.join(TAKEN)})")
                resultaat = functie(taak.get("params", {}))
                taak.update(status="klaar", resultaat=resultaat)
                log(f"✔ {naam}: {resultaat}")
            except Exception as e:
                fouten += 1
                taak.update(status="fout", resultaat=str(e))
                log(f"✖ {naam}: {e}", "FOUT")
                with open(LOGBOEK, "a", encoding="utf-8") as f:
                    f.write(traceback.format_exc())
                if inst.get("stop_bij_fout", False):
                    break
            taak["klaar"] = nu()
            schrijf_json(WACHTRIJ, wachtrij)
            pauze = int(inst.get("pauze_tussen_taken_sec", 3))
            if n < len(te_doen) and pauze and not slaap(pauze):
                log("Stop gevraagd.", "WAARSCHUWING")
                break
    finally:
        klaar = sum(1 for t in wachtrij["taken"] if t.get("status") == "klaar")
        log(f"Nacht-worker klaar: {klaar}/{len(wachtrij['taken'])} taken klaar, {fouten} fouten.")
        bewaar_status(draait=False, klaar=nu(), huidige_taak=None, taak_voortgang=None)
        for f in (LOCK, STOPBESTAND):
            if os.path.exists(f):
                os.remove(f)
    if inst.get("zeg_klaar_aan_einde", True):
        try:
            zeg_klaar()
        except Exception as e:
            log(f"zeg_klaar mislukt: {e}", "WAARSCHUWING")
    return 0 if fouten == 0 else 1


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Autonome Doorwerk-Wachtrij")
    p.add_argument("--reset", action="store_true", help="alle taken terug naar 'wachtend'")
    p.add_argument("--stop", action="store_true", help="lopende worker laten stoppen")
    a = p.parse_args(argv)
    if a.stop:
        open(STOPBESTAND, "w").write(nu())
        print("Stopverzoek geplaatst.")
        return 0
    return draai(reset=a.reset)


if __name__ == "__main__":
    sys.exit(main())
