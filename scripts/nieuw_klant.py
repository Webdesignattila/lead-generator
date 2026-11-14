#!/usr/bin/env python3
"""
Maakt een complete klantmap aan in klanten/<slug>/ op basis van klanten/_sjabloon/.

Gebruik:
    python scripts/nieuw_klant.py "Bakkerij De Korenaar" --branche bakkerij --plaats Zwolle --pakket Groei

Wordt ook gebruikt door de skill /nieuw-klant en door de knop "Nieuwe klant" in de Mainframe-app.
Overschrijft nooit een bestaande klantmap.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
GELDIGE_PAKKETTEN = {"", "Start", "Groei", "Premium", "Maatwerk"}


def maak_slug(naam: str) -> str:
    tekst = unicodedata.normalize("NFKD", naam).encode("ascii", "ignore").decode("ascii").lower()
    tekst = re.sub(r"&", " en ", tekst)
    tekst = re.sub(r"[^a-z0-9]+", "-", tekst).strip("-")
    return tekst[:60].strip("-")


def maak_klant(basis: Path, bedrijfsnaam: str, branche: str = "", plaats: str = "",
               pakket: str = "", contact: str = "") -> dict:
    bedrijfsnaam = " ".join(bedrijfsnaam.split())
    if not bedrijfsnaam or len(bedrijfsnaam) > 120:
        raise ValueError("Geef een bedrijfsnaam op (maximaal 120 tekens).")
    if pakket not in GELDIGE_PAKKETTEN:
        raise ValueError("Pakket moet Start, Groei, Premium of Maatwerk zijn.")
    slug = maak_slug(bedrijfsnaam)
    if not slug:
        raise ValueError("Bedrijfsnaam bevat geen bruikbare letters of cijfers.")

    klanten = basis / "klanten"
    sjabloon = klanten / "_sjabloon"
    doel = klanten / slug
    if doel.exists():
        raise FileExistsError(f"klanten/{slug}/ bestaat al. Er is niets overschreven.")
    if not sjabloon.is_dir():
        raise FileNotFoundError("klanten/_sjabloon/ ontbreekt.")

    shutil.copytree(sjabloon, doel)
    vervangingen = {
        "{{BEDRIJFSNAAM}}": bedrijfsnaam,
        "{{SLUG}}": slug,
        "{{BRANCHE}}": branche.strip() or "nog invullen",
        "{{PLAATS}}": plaats.strip() or "nog invullen",
        "{{PAKKET}}": pakket or "nog kiezen",
        "{{CONTACT}}": contact.strip() or "nog invullen",
        "{{DATUM}}": date.today().isoformat(),
    }
    for bestand in doel.rglob("*.md"):
        tekst = bestand.read_text(encoding="utf-8")
        for zoek, vervang in vervangingen.items():
            tekst = tekst.replace(zoek, vervang)
        bestand.write_text(tekst, encoding="utf-8")
    bestanden = sorted(str(p.relative_to(basis)).replace("\\", "/") for p in doel.rglob("*") if p.is_file())
    return {"map": f"klanten/{slug}", "slug": slug, "bestanden": bestanden}


def main() -> None:
    parser = argparse.ArgumentParser(description="Maak een nieuwe klantmap aan.")
    parser.add_argument("bedrijfsnaam")
    parser.add_argument("--branche", default="")
    parser.add_argument("--plaats", default="")
    parser.add_argument("--pakket", default="", choices=sorted(GELDIGE_PAKKETTEN))
    parser.add_argument("--contact", default="", help="Naam, telefoon en/of e-mail van de contactpersoon")
    args = parser.parse_args()
    try:
        resultaat = maak_klant(BASIS, args.bedrijfsnaam, args.branche, args.plaats, args.pakket, args.contact)
    except (ValueError, FileExistsError, FileNotFoundError) as fout:
        print(f"FOUT: {fout}")
        sys.exit(1)
    print(f"Klantmap aangemaakt: {resultaat['map']}/")
    for bestand in resultaat["bestanden"]:
        print(f"  - {bestand}")


if __name__ == "__main__":
    main()
