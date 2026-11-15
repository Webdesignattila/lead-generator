---
name: youtube-expert
description: >-
  Kloont een YouTube-kanaal of expert naar een herbruikbaar expert-profiel in experts/[naam].md, en
  laat een bestaand profiel meedenken. Gebruik deze skill bij "/youtube-expert <kanaal of naam>",
  "kloon <naam>", "maak een expert van <kanaal>", en ook bij "Vraag het aan <naam>",
  "Laat <naam> dit aanpakken" of "Wat zou <naam> doen?" (dan wordt experts/<naam>.md geladen).
---

# YouTube-Expert Kloon

Twee modi:

| Wat de gebruiker zegt | Modus |
|---|---|
| `/youtube-expert <kanaal-URL, @handle of naam>`, "kloon …", "maak een expert van …" | **A. Klonen** |
| "Vraag het aan Pavlo", "Laat Bart Boonstra dit aanpakken", "Wat zou <naam> doen?" | **B. Raadplegen** |

Bestandsnaam = naam in kleine letters, spaties en leestekens als `-`:
`Bart Boonstra` → `experts/bart-boonstra.md`, `Pavlo` → `experts/pavlo.md`.

---

## A. Klonen

### 1. Identificeer de juiste persoon
- Zoek met WebSearch op naam + onderwerp (+ "YouTube"). Veel namen zijn dubbel (er zijn meerdere
  "Pavlo"'s). Kies de match die past bij de context van Webdesign Attila (webdesign, lokale
  bedrijven, leads, AI/Claude Code) en schrijf in het profiel **waarom** deze persoon is gekozen.
- Twijfel tussen twee echte kandidaten die allebei passen: vraag de gebruiker kort welke, of kloon
  de beste match en noem de alternatieven onder "Identiteit".

### 2. Verzamel bronnen (minimaal 5, verschillende soorten)
In deze volgorde, en noteer per bron de URL:
1. Het kanaal zelf: About-pagina, populairste en nieuwste videotitels.
2. Transcripten van 3–10 representatieve video's. Opties:
   - `python -m pip install youtube-transcript-api` en dan
     `python -c "from youtube_transcript_api import YouTubeTranscriptApi as Y; print(' '.join(s.text for s in Y().fetch('<VIDEO_ID>', languages=['nl','en'])))"`
   - of `yt-dlp --skip-download --write-auto-subs --sub-langs "nl,en" <URL>`
3. Eigen website, landingspagina's, cursus/shop, nieuwsbrief.
4. LinkedIn/TikTok/X-posts (stijl en terugkerende uitspraken).
5. Onafhankelijke reviews/samenvattingen (als controle op marketingclaims).

Lukt het ophalen van een pagina niet (netwerk geblokkeerd), gebruik dan zoekresultaat-snippets en
markeer die punten als **[snippet]**. Verzin nooit citaten, cijfers of videotitels.

### 3. Schrijf `experts/<naam>.md` met exact deze opbouw

```markdown
# Expert: <Naam>

> Gebruik: "Vraag het aan <Naam>" / "Laat <Naam> dit aanpakken"
> Laatst bijgewerkt: <JJJJ-MM-DD> · Betrouwbaarheid: <hoog|middel|laag> (<waarom>)

## 1. Identiteit
Wie, kanaal/handle, aanbod, doelgroep, waarom deze persoon gekozen is.

## 2. Kernfilosofie (5–8 regels)
De overtuigingen waar elk advies uit voortkomt.

## 3. Werkwijze / Frameworks
Genummerde stappen van zijn of haar methode.

## 4. Toolstack
## 5. Stijl & toon
Hoe hij/zij praat, typische zinnen (alleen echte, met bron), wat hij/zij nooit zou zeggen.

## 6. Toepassing op Webdesign Attila
Concreet: wat deze expert zou doen met lokale leads, de scrapers, mailrondes, demo-sites, prijzen.

## 7. Zo antwoordt deze expert (instructie voor Claude)
Rol-instructie: perspectief, vaste vragen die hij/zij altijd stelt, opbouw van een antwoord.

## 8. Grenzen
Wat geverifieerd is en wat afgeleid is; marketingclaims die niet onafhankelijk bevestigd zijn.

## 9. Bronnen
- [titel](URL) — wat eruit komt
```

### 4. Controle voor opslaan
- Elk feit in 1–4 en 8 heeft een bron in sectie 9.
- Afgeleide punten (in 6 en 7) zijn als afgeleid herkenbaar.
- Geen privégegevens van de expert (adres, telefoon) in het profiel.
- Meld aan de gebruiker: bestandsnaam, betrouwbaarheid, en wat niet gevonden kon worden.

---

## B. Raadplegen ("Vraag het aan …")

1. Lees `experts/<naam>.md`. Bestaat het niet: zeg dat, en bied aan het nu te klonen (modus A).
2. Antwoord vanuit sectie 7 van het profiel, in de stijl van sectie 5, toegepast op de echte
   bestanden en cijfers van dit project (bijv. `echte_leads.csv`, `wachtrij.json`).
3. Begin het antwoord met `**<Naam> zegt:**` en eindig met één regel
   `_Gebaseerd op experts/<naam>.md — geen echte uitspraak van <Naam>._`
4. Vraagt de gebruiker om iets **uit te voeren** ("Laat Bart dit aanpakken"): gebruik de
   werkwijze uit sectie 3 als plan en voer de taak zelf uit in dit project.
5. Meerdere experts ("Wat vinden Pavlo en Bart hiervan?"): geef per expert een kort blok en sluit
   af met een gezamenlijke aanbeveling.
