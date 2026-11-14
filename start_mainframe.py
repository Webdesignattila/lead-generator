#!/usr/bin/env python3
"""
Webdesign Attila Mainframe 2.0 - lokale server
================================================

Start:   python start_mainframe.py            (opent automatisch je browser)
         python start_mainframe.py --geen-browser
         python start_mainframe.py --poort 8081

Draait op http://localhost:8080 en praat direct met je eigen bestanden:
  echte_leads.csv      -> Lead & Bel-CRM (alleen lezen, wordt nooit aangepast)
  verzonden.txt        -> teller + "al gemaild"-badge (alleen lezen)
  leads_status.json    -> jouw belstatus + notities per lead (wordt hier opgeslagen)
  klanten/             -> klantprojecten (klantprofiel.md per klant)
  .claude/skills/      -> skills-bibliotheek
  mainframe_config.json-> verbindingen, scripts en WhatsApp-bericht

Alleen Python-standaardbibliotheek. Luistert uitsluitend op 127.0.0.1
(niet bereikbaar vanaf andere computers in je netwerk).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASIS = Path(__file__).resolve().parent
sys.path.insert(0, str(BASIS / "scripts"))

from nieuw_klant import maak_klant  # noqa: E402  (scripts/nieuw_klant.py)

LEADS_CSV = BASIS / "echte_leads.csv"
VERZONDEN_TXT = BASIS / "verzonden.txt"
STATUS_JSON = BASIS / "leads_status.json"
KLANTEN_MAP = BASIS / "klanten"
SKILLS_MAP = BASIS / ".claude" / "skills"
LOGS_MAP = BASIS / "docs" / "logs"
CONFIG_JSON = BASIS / "mainframe_config.json"
APP_HTML = BASIS / "mainframe_app.html"
SCRIPT_LOGS = LOGS_MAP / "scripts"

GELDIGE_STATUSSEN = {"", "geen_gehoor", "terugbellen", "afspraak", "niet_interessant"}
MAX_BODY = 64 * 1024
SCHRIJF_SLOT = threading.Lock()

# Kolomnamen die we herkennen in echte_leads.csv (kleine letters, zonder spaties/streepjes).
KOLOMMEN = {
    "naam": ["bedrijfsnaam", "bedrijf", "naam", "name", "title", "titel", "company", "businessname"],
    "branche": ["branche", "categorie", "category", "type", "sector", "niche", "zoekterm", "query"],
    "telefoon": ["telefoon", "telefoonnummer", "tel", "phone", "phonenumber", "mobiel", "nummer"],
    "website": ["website", "site", "url", "web", "domein", "domain"],
    "email": ["email", "e-mail", "mail", "emailadres", "e-mailadres"],
    "plaats": ["plaats", "stad", "city", "woonplaats", "locatie", "location", "adres", "address"],
    "rating": ["rating", "beoordeling", "score", "sterren", "stars"],
    "reviews": ["reviews", "aantalreviews", "reviewcount", "recensies"],
}


# ----------------------------------------------------------------------------- helpers

def lees_tekst(pad: Path) -> str:
    """Leest een tekstbestand in utf-8 (met of zonder BOM) en valt terug op Windows-1252."""
    ruw = pad.read_bytes()
    for codering in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return ruw.decode(codering)
        except UnicodeDecodeError:
            continue
    return ruw.decode("utf-8", errors="replace")


def normaliseer_kolom(naam: str) -> str:
    return re.sub(r"[\s_\-.]", "", (naam or "").strip().lower())


def koppel_kolommen(kopregel: list[str]) -> dict[str, str]:
    """Bepaalt welke CSV-kolom bij welk veld hoort. Exacte match gaat voor deel-match."""
    genormaliseerd = {normaliseer_kolom(k): k for k in kopregel if k}
    koppeling: dict[str, str] = {}
    gebruikt: set[str] = set()
    for veld, kandidaten in KOLOMMEN.items():
        for kandidaat in kandidaten:
            sleutel = normaliseer_kolom(kandidaat)
            if sleutel in genormaliseerd and genormaliseerd[sleutel] not in gebruikt:
                koppeling[veld] = genormaliseerd[sleutel]
                gebruikt.add(koppeling[veld])
                break
    for veld, kandidaten in KOLOMMEN.items():
        if veld in koppeling:
            continue
        for norm, origineel in genormaliseerd.items():
            if origineel in gebruikt:
                continue
            if any(normaliseer_kolom(k) in norm for k in kandidaten):
                koppeling[veld] = origineel
                gebruikt.add(origineel)
                break
    return koppeling


def lead_id(naam: str, telefoon: str, website: str) -> str:
    sleutel = "|".join(s.strip().lower() for s in (naam, telefoon, website))
    return hashlib.sha1(sleutel.encode("utf-8")).hexdigest()[:12]


def whatsapp_nummer(telefoon: str) -> str:
    """Zet een Nederlands nummer om naar het internationale formaat voor wa.me (bijv. 31612345678)."""
    cijfers = re.sub(r"\D", "", telefoon or "")
    if not cijfers:
        return ""
    if cijfers.startswith("0031"):
        cijfers = "31" + cijfers[4:]
    elif cijfers.startswith("00"):
        cijfers = cijfers[2:]
    elif cijfers.startswith("0"):
        cijfers = "31" + cijfers[1:]
    if cijfers.startswith("310"):
        cijfers = "31" + cijfers[3:]
    return cijfers if 10 <= len(cijfers) <= 15 else ""


def schoon_website(url: str) -> str:
    url = (url or "").strip()
    if not url or url.lower() in {"nan", "none", "-", "geen"} or " " in url:
        return ""
    if re.match(r"^[a-z][a-z0-9+.\-]*:", url, re.I) and not re.match(r"^https?://", url, re.I):
        return ""  # bijv. javascript:, mailto:, tel: hoort niet in de websitekolom
    if not re.match(r"^https?://", url, re.I):
        url = "https://" + url
    host = urlparse(url).hostname or ""
    return url if "." in host else ""


def domein(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def lees_json(pad: Path, standaard):
    if not pad.exists():
        return standaard
    try:
        return json.loads(lees_tekst(pad))
    except (json.JSONDecodeError, OSError):
        return standaard


def schrijf_json_atomisch(pad: Path, data) -> None:
    tijdelijk = pad.with_suffix(pad.suffix + ".tmp")
    tijdelijk.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tijdelijk, pad)


def lees_frontmatter(tekst: str) -> dict[str, str]:
    """Eenvoudige YAML-frontmatter-lezer (sleutel: waarde, plus '>'-blokken op één niveau)."""
    if not tekst.startswith("---"):
        return {}
    einde = tekst.find("\n---", 3)
    if einde == -1:
        return {}
    data: dict[str, str] = {}
    huidige = None
    for regel in tekst[3:einde].splitlines():
        if not regel.strip():
            continue
        if regel.startswith((" ", "\t")) and huidige:
            data[huidige] = (data[huidige] + " " + regel.strip()).strip()
            continue
        if ":" in regel:
            sleutel, _, waarde = regel.partition(":")
            huidige = sleutel.strip()
            waarde = waarde.strip()
            data[huidige] = "" if waarde in {">", ">-", "|", "|-"} else waarde.strip("\"'")
    return data


# ----------------------------------------------------------------------------- data

def lees_verzonden() -> list[str]:
    if not VERZONDEN_TXT.exists():
        return []
    return [r.strip() for r in lees_tekst(VERZONDEN_TXT).splitlines() if r.strip()]


def lees_leads() -> tuple[list[dict], dict]:
    info = {"bestand_gevonden": LEADS_CSV.exists(), "kolommen": [], "koppeling": {}}
    if not LEADS_CSV.exists():
        return [], info
    tekst = lees_tekst(LEADS_CSV)
    if not tekst.strip():
        return [], info
    try:
        dialect = csv.Sniffer().sniff(tekst[:4096], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    lezer = csv.DictReader(io.StringIO(tekst), dialect=dialect)
    kop = [k for k in (lezer.fieldnames or []) if k]
    koppeling = koppel_kolommen(kop)
    info["kolommen"] = kop
    info["koppeling"] = koppeling

    verzonden = lees_verzonden()
    verzonden_laag = {v.lower() for v in verzonden}
    verzonden_domeinen = {domein(schoon_website(v)) for v in verzonden if "." in v and "@" not in v}
    verzonden_mail_domeinen = {v.split("@", 1)[1].lower() for v in verzonden if "@" in v}
    statussen = lees_json(STATUS_JSON, {})

    leads: list[dict] = []
    gezien: set[str] = set()
    for rij in lezer:
        def veld(naam: str) -> str:
            kolom = koppeling.get(naam)
            waarde = (rij.get(kolom) or "") if kolom else ""
            return str(waarde).strip()

        naam = veld("naam")
        telefoon = veld("telefoon")
        website = schoon_website(veld("website"))
        if not (naam or telefoon or website):
            continue
        lid = lead_id(naam, telefoon, website)
        if lid in gezien:
            continue
        gezien.add(lid)
        email = veld("email")
        if email.lower() in {"nan", "none", "-", "geen"}:
            email = ""
        site_domein = domein(website)
        al_gemaild = bool(
            (email and email.lower() in verzonden_laag)
            or (naam and naam.lower() in verzonden_laag)
            or (site_domein and (site_domein in verzonden_domeinen or site_domein in verzonden_mail_domeinen))
        )
        status = statussen.get(lid, {})
        leads.append({
            "id": lid,
            "naam": naam or site_domein or telefoon,
            "branche": veld("branche"),
            "telefoon": telefoon,
            "whatsapp": whatsapp_nummer(telefoon),
            "website": website,
            "email": email,
            "plaats": veld("plaats"),
            "rating": veld("rating"),
            "reviews": veld("reviews"),
            "al_gemaild": al_gemaild,
            "status": status.get("status", ""),
            "notitie": status.get("notitie", ""),
            "bijgewerkt": status.get("bijgewerkt", ""),
        })
    return leads, info


def lees_klanten() -> list[dict]:
    klanten = []
    if not KLANTEN_MAP.exists():
        return klanten
    for map_ in sorted(KLANTEN_MAP.iterdir()):
        if not map_.is_dir() or map_.name.startswith(("_", ".")):
            continue
        profiel = map_ / "klantprofiel.md"
        meta = lees_frontmatter(lees_tekst(profiel)) if profiel.exists() else {}
        checklist = map_ / "checklist.md"
        open_, klaar = 0, 0
        if checklist.exists():
            for regel in lees_tekst(checklist).splitlines():
                s = regel.strip().lower()
                if s.startswith("- [ ]"):
                    open_ += 1
                elif s.startswith("- [x]"):
                    klaar += 1
        klanten.append({
            "map": map_.name,
            "naam": meta.get("bedrijfsnaam") or map_.name,
            "status": meta.get("status", "onbekend"),
            "pakket": meta.get("pakket", ""),
            "deadline": meta.get("deadline", ""),
            "plaats": meta.get("plaats", ""),
            "taken_open": open_,
            "taken_klaar": klaar,
        })
    return klanten


def lees_skills() -> list[dict]:
    skills = []
    if not SKILLS_MAP.exists():
        return skills
    for map_ in sorted(SKILLS_MAP.iterdir()):
        bestand = map_ / "SKILL.md"
        if not bestand.exists():
            continue
        try:
            meta = lees_frontmatter(lees_tekst(bestand))
        except OSError:
            continue
        naam = meta.get("name") or map_.name
        skills.append({
            "naam": naam,
            "commando": "/" + naam,
            "beschrijving": meta.get("description", ""),
            "voorbeeld": meta.get("argument-hint", ""),
            "eigen": not map_.is_symlink(),
        })
    return skills


def lees_config() -> dict:
    return lees_json(CONFIG_JSON, {})


def verbindingen() -> list[dict]:
    config = lees_config()
    resultaat = []
    for item in config.get("verbindingen", []):
        item = dict(item)
        controle = item.get("controle")
        if controle == "python":
            item["status"] = "actief"
            item["detail"] = f"Python {platform.python_version()}"
        elif controle == "claude":
            pad = shutil.which("claude")
            item["status"] = "actief" if pad else "niet_gevonden"
            item["detail"] = "claude-commando gevonden" if pad else "claude-commando niet gevonden in PATH"
        elif controle and controle.startswith("bestand:"):
            bestand = BASIS / controle.split(":", 1)[1]
            item["status"] = "actief" if bestand.exists() else "niet_gevonden"
            item["detail"] = f"{bestand.name} {'gevonden' if bestand.exists() else 'ontbreekt'}"
        resultaat.append(item)
    return resultaat


def scripts_overzicht() -> list[dict]:
    lijst = []
    for item in lees_config().get("scripts", []):
        bestand = BASIS / item.get("bestand", "")
        lijst.append({**item, "aanwezig": bestand.is_file()})
    return lijst


def overzicht() -> dict:
    leads, info = lees_leads()
    verzonden = lees_verzonden()
    per_status: dict[str, int] = {}
    for lead in leads:
        per_status[lead["status"] or "nieuw"] = per_status.get(lead["status"] or "nieuw", 0) + 1
    terugbellen = [l for l in leads if l["status"] == "terugbellen"]
    logs = sorted(LOGS_MAP.glob("*.md"), reverse=True) if LOGS_MAP.exists() else []
    logs = [p for p in logs if re.match(r"\d{4}-\d{2}-\d{2}", p.name)]
    return {
        "datum": datetime.now().strftime("%Y-%m-%d"),
        "leads_totaal": len(leads),
        "leads_bestand": info["bestand_gevonden"],
        "verzonden_totaal": len(verzonden),
        "verzonden_bestand": VERZONDEN_TXT.exists(),
        "verzonden_laatste": verzonden[-5:][::-1],
        "per_status": per_status,
        "terugbellen": terugbellen[:8],
        "klanten": lees_klanten(),
        "scripts": scripts_overzicht(),
        "laatste_log": logs[0].name if logs else "",
        "skills_totaal": len(lees_skills()),
    }


def sla_status_op(lid: str, status: str | None, notitie: str | None) -> dict:
    if not re.fullmatch(r"[0-9a-f]{12}", lid or ""):
        raise ValueError("Ongeldig lead-id")
    if status is not None and status not in GELDIGE_STATUSSEN:
        raise ValueError("Ongeldige status")
    with SCHRIJF_SLOT:
        data = lees_json(STATUS_JSON, {})
        item = data.get(lid, {})
        if status is not None:
            item["status"] = status
        if notitie is not None:
            item["notitie"] = notitie[:5000]
        item["bijgewerkt"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not item.get("status") and not item.get("notitie"):
            data.pop(lid, None)
        else:
            data[lid] = item
        schrijf_json_atomisch(STATUS_JSON, data)
    return item


def start_script(sleutel: str) -> dict:
    """Start alleen scripts die in mainframe_config.json staan (geen willekeurige commando's)."""
    gevonden = next((s for s in lees_config().get("scripts", []) if s.get("sleutel") == sleutel), None)
    if not gevonden:
        raise ValueError("Onbekend script")
    bestand = (BASIS / gevonden["bestand"]).resolve()
    if BASIS not in bestand.parents or not bestand.is_file():
        raise FileNotFoundError(f"{gevonden['bestand']} staat niet in {BASIS}")
    commando = [sys.executable, str(bestand)]
    if os.name == "nt":
        # Eigen consolevenster, zodat je de voortgang live ziet en het script kunt stoppen.
        subprocess.Popen(commando, cwd=str(BASIS), creationflags=subprocess.CREATE_NEW_CONSOLE)
        return {"ok": True, "melding": f"{gevonden['label']} gestart in een nieuw venster."}
    SCRIPT_LOGS.mkdir(parents=True, exist_ok=True)
    logbestand = SCRIPT_LOGS / f"{datetime.now():%Y-%m-%d_%H%M%S}_{bestand.stem}.log"
    with open(logbestand, "w", encoding="utf-8") as log:
        subprocess.Popen(commando, cwd=str(BASIS), stdout=log, stderr=subprocess.STDOUT)
    return {"ok": True, "melding": f"{gevonden['label']} gestart. Uitvoer: {logbestand.relative_to(BASIS)}"}


# ----------------------------------------------------------------------------- server

class MainframeHandler(BaseHTTPRequestHandler):
    server_version = "AttilaMainframe/2.0"

    def log_message(self, formaat, *args):  # rustige console
        if "/api/" in (args[0] if args else ""):
            return
        sys.stderr.write("  %s\n" % (formaat % args))

    def _stuur(self, code: int, inhoud: bytes, type_: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", type_)
        self.send_header("Content-Length", str(len(inhoud)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(inhoud)

    def _json(self, data, code: int = 200) -> None:
        self._stuur(code, json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def _fout(self, code: int, melding: str) -> None:
        self._json({"ok": False, "fout": melding}, code)

    def _veilige_post(self) -> bool:
        """Blokkeert verzoeken van andere websites (alleen de eigen app mag schrijven)."""
        host = (self.headers.get("Host") or "").split(":")[0]
        if host not in {"localhost", "127.0.0.1"}:
            return False
        if self.headers.get("X-Mainframe") != "1":
            return False
        origin = self.headers.get("Origin")
        if origin and urlparse(origin).hostname not in {"localhost", "127.0.0.1"}:
            return False
        return True

    def _lees_body(self) -> dict:
        lengte = int(self.headers.get("Content-Length") or 0)
        if lengte > MAX_BODY:
            raise ValueError("Verzoek te groot")
        data = json.loads(self.rfile.read(lengte) or b"{}")
        if not isinstance(data, dict):
            raise ValueError("Verwacht een JSON-object")
        return data

    def do_GET(self):  # noqa: N802
        pad = urlparse(self.path).path
        try:
            if pad in {"/", "/index.html", "/mainframe_app.html"}:
                if not APP_HTML.exists():
                    return self._fout(404, "mainframe_app.html ontbreekt")
                return self._stuur(200, APP_HTML.read_bytes(), "text/html; charset=utf-8")
            if pad == "/api/overzicht":
                return self._json(overzicht())
            if pad == "/api/leads":
                leads, info = lees_leads()
                return self._json({"leads": leads, "info": info, "config": {
                    "whatsapp_bericht": lees_config().get("whatsapp_bericht", ""),
                    "mail_onderwerp": lees_config().get("mail_onderwerp", ""),
                    "mail_bericht": lees_config().get("mail_bericht", ""),
                }})
            if pad == "/api/skills":
                return self._json({"skills": lees_skills(), "prompts": lees_config().get("prompts", [])})
            if pad == "/api/verbindingen":
                return self._json({"verbindingen": verbindingen(), "scripts": scripts_overzicht()})
            if pad == "/favicon.ico":
                return self._stuur(204, b"", "image/x-icon")
            return self._fout(404, "Niet gevonden")
        except Exception as fout:  # noqa: BLE001
            return self._fout(500, f"{type(fout).__name__}: {fout}")

    def do_POST(self):  # noqa: N802
        pad = urlparse(self.path).path
        if not self._veilige_post():
            return self._fout(403, "Geweigerd: alleen de lokale Mainframe-app mag dit.")
        try:
            data = self._lees_body()
            if pad == "/api/leads/status":
                item = sla_status_op(str(data.get("id", "")),
                                     data.get("status") if "status" in data else None,
                                     data.get("notitie") if "notitie" in data else None)
                return self._json({"ok": True, "item": item})
            if pad == "/api/scripts/start":
                return self._json(start_script(str(data.get("sleutel", ""))))
            if pad == "/api/klanten":
                resultaat = maak_klant(BASIS, str(data.get("bedrijfsnaam", "")),
                                       branche=str(data.get("branche", "")),
                                       plaats=str(data.get("plaats", "")),
                                       pakket=str(data.get("pakket", "")),
                                       contact=str(data.get("contact", "")))
                return self._json({"ok": True, **resultaat})
            return self._fout(404, "Niet gevonden")
        except (ValueError, FileNotFoundError, FileExistsError, json.JSONDecodeError) as fout:
            return self._fout(400, str(fout))
        except Exception as fout:  # noqa: BLE001
            return self._fout(500, f"{type(fout).__name__}: {fout}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Start de Webdesign Attila Mainframe.")
    parser.add_argument("--poort", type=int, default=8080)
    parser.add_argument("--geen-browser", action="store_true", help="Open de browser niet automatisch")
    args = parser.parse_args()

    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.poort), MainframeHandler)
    except OSError:
        print(f"Poort {args.poort} is al in gebruik. Draait de Mainframe al? Kijk op http://localhost:{args.poort}")
        print(f"Of start op een andere poort: python start_mainframe.py --poort {args.poort + 1}")
        sys.exit(1)

    url = f"http://localhost:{args.poort}"
    print("=" * 58)
    print("  WEBDESIGN ATTILA  ·  MAINFRAME 2.0")
    print(f"  Draait op {url}   (stoppen: Ctrl+C)")
    print(f"  Map: {BASIS}")
    print(f"  Leads: {'gevonden' if LEADS_CSV.exists() else 'echte_leads.csv ontbreekt'}"
          f"  ·  Verzonden: {'gevonden' if VERZONDEN_TXT.exists() else 'verzonden.txt ontbreekt'}")
    print("=" * 58)
    if not args.geen_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMainframe gestopt.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
