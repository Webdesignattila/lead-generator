---
name: skill-maker
description: Zes-stappen skill-generator - giet elke terugkerende taak van Webdesign Attila in een nieuwe, herbruikbare skill in .claude/skills/[naam]/SKILL.md. Begint bij het probleem en de ideale situatie, test de skill op een echt voorbeeld en zet hem in CLAUDE.md. Gebruik bij "maak een skill", "dit doe ik vaker", "automatiseer deze taak" of "skill-maker".
argument-hint: "[korte omschrijving van de terugkerende taak]"
---

# /skill-maker — van terugkerende klus naar skill in zes stappen

Een skill is een vaste werkwijze die je één keer vastlegt: daarna doet Claude het elke keer precies zo. Bouw geen "agent", bouw een handleiding voor een klus die vaker terugkomt.

Werk de zes stappen in volgorde af. Stuur per stap **één** kort bericht en wacht op Attila's antwoord voordat je doorgaat (behalve waar staat dat je direct door mag).

## Stap 1 — Probleem en ideale situatie schetsen

Vraag in één bericht:
1. Welke klus doe je vaker? Hoe vaak, en hoeveel tijd kost hij nu?
2. Hoe ziet de ideale situatie eruit? ("Ik typ één commando en dan …")
3. Wat is het eindresultaat precies (bestand, mail-concept, overzicht, website)?

## Stap 2 — Het huidige stappenplan uitpluizen

Laat Attila de klus één keer stap voor stap beschrijven, of — beter — doe hem nu samen echt één keer. Noteer: welke bestanden worden gelezen, welke beslissingen worden genomen, welke tools/scripts gebruikt worden, wat er vaak misgaat.

Vat het daarna samen in maximaal 8 genummerde stappen en vraag: "Klopt dit, en wat mis ik?"

## Stap 3 — Grenzen en regels vastleggen

Vraag in één bericht (alleen wat nog onbekend is):
- Wat mag de skill **nooit** zonder akkoord doen? (versturen, verwijderen, publiceren, betalen)
- Welke bestanden mag hij lezen, welke schrijven?
- Waar komt het resultaat te staan? (bijv. `klanten/[slug]/…`, `docs/…`)
- Welke vaste kennis uit `CLAUDE.md` is nodig (prijzen, huisstijl, tone of voice)?

## Stap 4 — De skill schrijven (direct door na het antwoord)

Kies een korte naam in kleine letters met streepjes (bijv. `review-verzamelaar`). Controleer dat `.claude/skills/[naam]/` nog niet bestaat. Schrijf `.claude/skills/[naam]/SKILL.md` volgens dit sjabloon:

```markdown
---
name: [naam]
description: [Wat hij doet in één zin]. Gebruik bij "[triggerwoord 1]", "[triggerwoord 2]" of [situatie].
argument-hint: "[wat je meegeeft]"
---

# /[naam] — [korte belofte]

## Stap 1 — [Context lezen]
[Welke bestanden, wat te doen als iets ontbreekt]

## Stap 2 — [Uitvoeren]
[Concrete stappen, commando's in codeblokken]

## Stap 3 — [Controleren]
[Hoe je checkt dat het resultaat klopt]

## Stap 4 — [Opleveren]
[Exact format van het resultaat + waar het wordt opgeslagen]

## Regels
- [nooit-doen-regels uit stap 3]
```

Eisen: de `description` noemt duidelijke triggerwoorden (daarop kiest Claude de skill); verwijs naar `CLAUDE.md` voor vaste kennis in plaats van die te kopiëren; hulpscripts gaan in `scripts/` of in de skillmap zelf.

## Stap 5 — Testen op een echt voorbeeld

Voer de nieuwe skill direct uit op een echt geval uit de map (een echte klant of lead). Laat het resultaat zien en vraag: "Wat moet er anders?" Verwerk elke opmerking in `SKILL.md` en test opnieuw, tot Attila zegt dat het klopt.

## Stap 6 — Vastleggen

1. Voeg de skill toe aan de skill-tabel in `CLAUDE.md` (naam + één regel).
2. Vermeld de nieuwe skill in de sessielog van vandaag (`docs/logs/JJJJ-MM-DD.md`).
3. Meld: "Nieuwe skill: `/[naam]` — [wat hij doet]. Je ziet hem ook in de Mainframe-app onder Skills." (De app leest `.claude/skills/` automatisch.)

## Regels

- Neem geen skills van internet over zonder ze eerst volledig te lezen op verdachte commando's (externe downloads, `curl | bash`, versturen van bestanden, wachtwoorden).
- Eén skill = één klus. Wordt hij te groot, splits hem.
