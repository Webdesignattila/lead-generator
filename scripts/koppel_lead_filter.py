"""
koppel_lead_filter.py: hangt lead_filter in echte_scraper.py en mijnhost_jager.py.

Voegt bovenaan elk script een klein blok toe dat de csv-bewaker activeert. Daarna kan geen
geblokkeerde lead (keten, dealer, gemeente, stichting, "Contactinformatie") meer in een
*leads*.csv terechtkomen, ongeacht hoe het script schrijft (csv.writer, csv.DictWriter of
pandas.to_csv).

    python scripts/koppel_lead_filter.py            # zoekt de twee scripts zelf
    python scripts/koppel_lead_filter.py pad\\naar\\script.py
    python scripts/koppel_lead_filter.py --ongedaan  # blok weer verwijderen

Elke wijziging maakt eerst <script>.py.bak. Het blok is idempotent (dubbel draaien kan geen kwaad).
"""

from __future__ import annotations

import argparse
import os
import py_compile
import re
import shutil
import sys

BEGIN = "# >>> lead_filter (automatisch toegevoegd door koppel_lead_filter.py)"
EINDE = "# <<< lead_filter"
BLOK = f'''{BEGIN}
import os as _lf_os, sys as _lf_sys
_lf_hier = _lf_os.path.dirname(_lf_os.path.abspath(__file__))
for _lf_pad in (_lf_hier, _lf_os.path.join(_lf_hier, "scripts"),
                _lf_os.path.join(_lf_os.path.dirname(_lf_hier), "scripts")):
    if _lf_os.path.isfile(_lf_os.path.join(_lf_pad, "lead_filter.py")) and _lf_pad not in _lf_sys.path:
        _lf_sys.path.insert(0, _lf_pad)
try:
    import lead_filter as _lead_filter
    _lead_filter.activeer_csv_bewaker()
except Exception as _lf_fout:  # het script moet altijd blijven werken
    print(f"[lead_filter] niet actief: {{_lf_fout}}")
{EINDE}
'''
STANDAARD = ("echte_scraper.py", "mijnhost_jager.py")


def _invoegpositie(regels: list[str]) -> int:
    """Na shebang, encoding-regel, module-docstring en `from __future__`-imports."""
    i = 0
    while i < len(regels) and (regels[i].startswith("#!") or re.match(r"#.*coding[:=]", regels[i])):
        i += 1
    j = i
    while j < len(regels) and not regels[j].strip():
        j += 1
    if j < len(regels) and re.match(r'\s*[rRuUbB]*("""|\'\'\')', regels[j]):
        q = '"""' if '"""' in regels[j] else "'''"
        if regels[j].count(q) >= 2:
            i = j + 1
        else:
            k = j + 1
            while k < len(regels) and q not in regels[k]:
                k += 1
            i = k + 1
    k = i
    while k < len(regels):
        r = regels[k].strip()
        if r.startswith("from __future__"):
            i = k + 1
        elif r and not r.startswith("#"):
            break
        k += 1
    return i


def koppel(pad: str) -> str:
    tekst = open(pad, encoding="utf-8").read()
    if BEGIN in tekst:
        return "al gekoppeld"
    shutil.copy2(pad, pad + ".bak")
    regels = tekst.splitlines(keepends=True)
    pos = _invoegpositie(regels)
    nieuw = "".join(regels[:pos]) + BLOK + "".join(regels[pos:])
    open(pad, "w", encoding="utf-8").write(nieuw)
    try:
        py_compile.compile(pad, doraise=True)
    except py_compile.PyCompileError as e:
        shutil.copy2(pad + ".bak", pad)
        return f"MISLUKT, origineel teruggezet: {e}"
    return "gekoppeld (backup: " + os.path.basename(pad) + ".bak)"


def ontkoppel(pad: str) -> str:
    tekst = open(pad, encoding="utf-8").read()
    if BEGIN not in tekst:
        return "niet gekoppeld"
    nieuw = re.sub(re.escape(BEGIN) + r".*?" + re.escape(EINDE) + r"\n?", "", tekst, flags=re.S)
    open(pad, "w", encoding="utf-8").write(nieuw)
    return "ontkoppeld"


def zoek_scripts(basis: str) -> list[str]:
    gevonden = []
    for naam in STANDAARD:
        for map_ in (basis, os.path.join(basis, "scripts")):
            p = os.path.join(map_, naam)
            if os.path.isfile(p):
                gevonden.append(p)
                break
        else:
            print(f"  - {naam}: niet gevonden in {basis} of {basis}\\scripts")
    return gevonden


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("scripts", nargs="*")
    p.add_argument("--ongedaan", action="store_true")
    a = p.parse_args(argv)
    basis = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paden = a.scripts or zoek_scripts(basis)
    for pad in paden:
        print(f"  - {pad}: {(ontkoppel if a.ongedaan else koppel)(pad)}")
    return 0 if paden else 1


if __name__ == "__main__":
    sys.exit(main())
