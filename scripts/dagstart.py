#!/usr/bin/env python3
"""
Dagstart-briefing (pijler "Vanzelf").

Schrijft docs/dagstart/JJJJ-MM-DD.md met:
  - aantal leads, nog niet gebeld, terugbellers en afspraken (uit echte_leads.csv + leads_status.json)
  - aantal verzonden mails (verzonden.txt)
  - lopende klantprojecten met open checklist-punten (klanten/)
  - de "volgende stap" uit de laatste sessielog (docs/logs/)

Gebruik:
    python scripts/dagstart.py            -> schrijft het bestand en toont het
    python scripts/dagstart.py --spreek   -> zegt daarna ook hardop "Goedemorgen Attila..." (Windows)

Draait automatisch elke ochtend om 07:00 als je scripts/installeer_ochtendtaak.ps1 hebt uitgevoerd.
Gebruikt geen AI en geen internet: het werkt dus ook zonder Claude.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS))

import start_mainframe as mf  # noqa: E402

DAGNAMEN = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus",
           "september", "oktober", "november", "december"]


def volgende_stap_uit_log() -> tuple[str, str]:
    logs = sorted(p for p in mf.LOGS_MAP.glob("*.md") if re.match(r"\d{4}-\d{2}-\d{2}", p.name)) \
        if mf.LOGS_MAP.exists() else []
    if not logs:
        return "", ""
    tekst = mf.lees_tekst(logs[-1])
    blok = re.search(r"##\s*Volgende stap[^\n]*\n(.*?)(?:\n##\s|\Z)", tekst, re.S | re.I)
    return logs[-1].stem, (blok.group(1).strip() if blok else "")


def maak_briefing() -> tuple[str, str]:
    nu = datetime.now()
    leads, info = mf.lees_leads()
    verzonden = mf.lees_verzonden()
    klanten = mf.lees_klanten()
    per_status: dict[str, int] = {}
    for lead in leads:
        per_status[lead["status"] or "nieuw"] = per_status.get(lead["status"] or "nieuw", 0) + 1
    terugbellen = [l for l in leads if l["status"] == "terugbellen"]
    afspraken = [l for l in leads if l["status"] == "afspraak"]
    nieuw_met_tel = [l for l in leads if not l["status"] and l["telefoon"] and not l["al_gemaild"]]
    lopend = [k for k in klanten if k["status"] not in {"live", "onderhoud", "gearchiveerd"}]
    log_datum, volgende = volgende_stap_uit_log()

    datum_tekst = f"{DAGNAMEN[nu.weekday()]} {nu.day} {MAANDEN[nu.month - 1]} {nu.year}"
    r = [f"# Dagstart — {datum_tekst}", ""]
    r.append(f"_Automatisch gemaakt om {nu:%H:%M} door scripts/dagstart.py._")
    r.append("")
    r.append("## Cijfers")
    if info["bestand_gevonden"]:
        r.append(f"- Leads in `echte_leads.csv`: **{len(leads)}**")
        r.append(f"- Nog niet gebeld: **{per_status.get('nieuw', 0)}**")
        r.append(f"- Terugbellen: **{len(terugbellen)}** · Afspraak/demo: **{len(afspraken)}**"
                 f" · Geen gehoor: **{per_status.get('geen_gehoor', 0)}**"
                 f" · Niet interessant: **{per_status.get('niet_interessant', 0)}**")
    else:
        r.append("- `echte_leads.csv` niet gevonden in de Mainframe-map.")
    r.append(f"- Mails verzonden (`verzonden.txt`): **{len(verzonden)}**")
    r.append("")

    r.append("## 1. Eerst bellen (terugbellers)")
    if terugbellen:
        for l in terugbellen[:15]:
            extra = f" — {l['notitie'][:100]}" if l["notitie"] else ""
            r.append(f"- [ ] **{l['naam']}** · {l['telefoon'] or 'geen nummer'} · {l['plaats'] or l['branche']}{extra}")
    else:
        r.append("- Geen terugbellers.")
    r.append("")

    r.append("## 2. Afspraken / demo's voorbereiden")
    if afspraken:
        for l in afspraken[:15]:
            r.append(f"- [ ] **{l['naam']}** · {l['plaats'] or l['branche']} → `/nieuw-klant` + `/website-bouwer` (demo)")
    else:
        r.append("- Geen openstaande afspraken.")
    r.append("")

    r.append("## 3. Nieuwe belronde (top 10, met telefoon, nog niet gemaild)")
    if nieuw_met_tel:
        for l in nieuw_met_tel[:10]:
            r.append(f"- [ ] **{l['naam']}** · {l['telefoon']} · {l['branche'] or '-'} · {l['plaats'] or '-'}")
    else:
        r.append("- Geen nieuwe leads met telefoonnummer. Start de scraper.")
    r.append("")

    r.append("## 4. Lopende klantprojecten")
    if lopend:
        for k in lopend:
            r.append(f"- **{k['naam']}** — status `{k['status']}`"
                     f"{' · deadline ' + k['deadline'] if k['deadline'] else ''}"
                     f" · checklist {k['taken_klaar']}/{k['taken_open'] + k['taken_klaar']}")
    else:
        r.append("- Geen lopende projecten.")
    r.append("")

    r.append("## 5. Volgende stap uit de laatste sessie")
    r.append(f"_Log: docs/logs/{log_datum}.md_" if log_datum else "_Nog geen sessielogs._")
    if volgende:
        r.append("")
        r.append(volgende)
    r.append("")

    gesproken = (f"Goedemorgen Attila. Je hebt {len(terugbellen)} terugbellers, "
                 f"{len(afspraken)} afspraken en {len(lopend)} lopende projecten.")
    return "\n".join(r), gesproken


def main() -> None:
    parser = argparse.ArgumentParser(description="Maak de dagstart-briefing.")
    parser.add_argument("--spreek", action="store_true", help="Lees de samenvatting hardop voor (Windows)")
    parser.add_argument("--stil", action="store_true", help="Toon de briefing niet in de console")
    args = parser.parse_args()

    tekst, gesproken = maak_briefing()
    map_ = BASIS / "docs" / "dagstart"
    map_.mkdir(parents=True, exist_ok=True)
    bestand = map_ / f"{datetime.now():%Y-%m-%d}.md"
    bestand.write_text(tekst, encoding="utf-8")
    if not args.stil:
        print(tekst)
        print(f"\nOpgeslagen: {bestand.relative_to(BASIS)}")
    if args.spreek:
        ps1 = BASIS / "scripts" / "zeg_klaar.ps1"
        if sys.platform == "win32" and ps1.exists():
            subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1),
                            "-Tekst", gesproken], check=False)
        else:
            print("(Hardop voorlezen werkt alleen op Windows.)")


if __name__ == "__main__":
    main()
