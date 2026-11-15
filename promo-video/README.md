# Webdesign Attila – Promo-video (Remotion)

Verticale promo-video: **1080×1920 · 30 fps · exact 23 s (690 frames)** met Nederlandse voice-over.

| Scène | Tijd | Inhoud |
|---|---|---|
| 1 Hook | 0–4 s | PageSpeed-meter zakt van 92% (groen) naar 28% (rood), "Verouderde website" |
| 2 Check | 4–8 s | Badge #1, 3 rode waarschuwingen klappen één voor één in beeld |
| 3 Oplossing | 8–14 s | Badge #2, pakket wordt aangevinkt, gele prijsbadge springt in |
| 4 Contact | 14–18 s | Badge #3, cursor klikt op pulserende WhatsApp-knop, vinkje "Binnen 24 uur klaar" |
| 5 Eindkaart | 18–23 s | Logo + contactkaart (website, belofte, bereikbaarheid) |

## Eenmalig installeren
```powershell
npm install
pip install -r requirements.txt   # gTTS; ffmpeg moet in PATH staan
```

## Renderen
```powershell
powershell -ExecutionPolicy Bypass -File scripts\render.ps1
```
Dit genereert `public\voiceover.mp3`, rendert `out\webdesign_attila_promo.mp4` en speelt daarna `scripts\zeg_klaar.ps1` af.
Losse stappen: `npm run voiceover`, `npm run render`, of live bekijken met `npm run studio`.

## Aanpassen voor een klant (± 2 minuten)
Alles staat in **`klant-config.json`**:
1. `merk` – naam, logo-letters, website, belofte, openingstijden.
2. `kleuren` – merkkleuren (`accent` = blauwe accentkleur, `prijs` = prijsbadge).
3. `scenes` – badges, waarschuwingen, pakketten, prijs, knoptekst en ondertitels.
   Woorden tussen `*sterretjes*` worden in de accentkleur getoond.
4. `voiceover.teksten` – gesproken tekst per scène. Te lange teksten worden automatisch iets versneld (max. 1,6×); het script waarschuwt als je moet inkorten.
5. Daarna `scripts\render.ps1` draaien. Kopieer de map per klant (bv. `promo-telefoonwinkel`) zodat je een archief houdt.

De scènetiming staat vast in `src/config.ts` en `scripts/genereer_voiceover.py` (moeten gelijk blijven).
