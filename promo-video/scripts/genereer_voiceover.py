"""
Genereert de Nederlandse voice-over (gTTS) voor de promo-video.

- Leest de teksten uit klant-config.json  -> voiceover.teksten
- Maakt per scène een losse gTTS-clip
- Versnelt een clip automatisch (ffmpeg atempo) als hij niet in zijn scène past
- Plaatst elke clip exact op de starttijd van zijn scène
- Schrijft één bestand van precies 23,000 s naar public/voiceover.mp3

Vereist: pip install gTTS   +   ffmpeg/ffprobe in PATH
Gebruik:  python scripts/genereer_voiceover.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from gtts import gTTS

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "klant-config.json"
PUBLIC = ROOT / "public"
TMP = PUBLIC / "_voiceover_tmp"

TOTAAL_SEC = 23.0
# Moet gelijk blijven aan SCENES in src/config.ts (start, duur in seconden)
SCENES = {
    "hook": (0.0, 4.0),
    "check": (4.0, 4.0),
    "oplossing": (8.0, 6.0),
    "contact": (14.0, 4.0),
    "eind": (18.0, 5.0),
}
START_MARGE = 0.25  # stem begint iets na de scènewissel
EIND_MARGE = 0.30   # en stopt ruim voor de volgende scène
MAX_TEMPO = 1.6     # niet sneller dan dit (verstaanbaarheid)


def run(cmd: list[str]) -> str:
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"Fout bij: {' '.join(cmd)}\n{res.stderr}")
    return res.stdout


def duur(pad: Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(pad)])
    return float(out.strip())


def atempo_keten(factor: float) -> str:
    # atempo accepteert 0.5 - 2.0 per filter
    delen = []
    while factor > 2.0:
        delen.append("atempo=2.0")
        factor /= 2.0
    delen.append(f"atempo={factor:.4f}")
    return ",".join(delen)


def main() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} niet gevonden. Installeer ffmpeg en zet het in PATH.")

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    vo = cfg["voiceover"]
    teksten: dict[str, str] = vo["teksten"]
    uitvoer = PUBLIC / vo.get("bestand", "voiceover.mp3")

    PUBLIC.mkdir(exist_ok=True)
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir()

    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []

    for i, (naam, (start, lengte)) in enumerate(SCENES.items()):
        tekst = teksten.get(naam, "").strip()
        if not tekst:
            print(f"- {naam}: geen tekst, overgeslagen")
            continue

        ruw = TMP / f"{naam}_ruw.mp3"
        print(f"- {naam}: gTTS -> \"{tekst}\"")
        gTTS(text=tekst, lang=vo.get("taal", "nl"), tld=vo.get("tld", "com")).save(str(ruw))

        # Stilte aan begin/eind wegknippen voor strakke timing
        schoon = TMP / f"{naam}.wav"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(ruw), "-af",
             "silenceremove=start_periods=1:start_threshold=-45dB,"
             "areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
             "-ar", "44100", "-ac", "2", str(schoon)])

        beschikbaar = lengte - START_MARGE - EIND_MARGE
        d = duur(schoon)
        factor = 1.0
        if d > beschikbaar:
            factor = min(d / beschikbaar, MAX_TEMPO)
            if d / beschikbaar > MAX_TEMPO:
                print(f"  ! Tekst voor '{naam}' is te lang ({d:.2f}s voor {beschikbaar:.2f}s). "
                      f"Maak hem korter in klant-config.json.")
        print(f"  duur {d:.2f}s, tempo x{factor:.2f}")

        inputs += ["-i", str(schoon)]
        delay_ms = int(round((start + START_MARGE) * 1000))
        keten = (atempo_keten(factor) + ",") if factor > 1.0 else ""
        # Clip nooit over de scènegrens laten lopen
        max_len = lengte - START_MARGE
        filters.append(
            f"[{len(labels)}:a]{keten}atrim=0:{max_len:.3f},afade=t=out:st={max_len - 0.08:.3f}:d=0.08,"
            f"adelay={delay_ms}|{delay_ms}[a{i}]"
        )
        labels.append(f"[a{i}]")

    if not labels:
        sys.exit("Geen voice-overteksten gevonden in klant-config.json")

    filters.append(
        f"{''.join(labels)}amix=inputs={len(labels)}:duration=longest:normalize=0,"
        f"apad=whole_dur={TOTAAL_SEC},atrim=0:{TOTAAL_SEC},loudnorm=I=-16:TP=-1.5:LRA=11[out]"
    )

    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
         "-map", "[out]", "-ar", "44100", "-ac", "2", "-b:a", "192k", str(uitvoer)])
    shutil.rmtree(TMP)

    print(f"\nKlaar: {uitvoer.relative_to(ROOT)} ({duur(uitvoer):.3f}s)")


if __name__ == "__main__":
    main()
