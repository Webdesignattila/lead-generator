---
name: einde
description: Sluit een werksessie netjes af - vat alles samen in docs/logs/JJJJ-MM-DD.md, werkt CLAUDE.md en de klantprofielen bij met nieuwe inzichten, controleert of de mappenstructuur nog klopt, maakt optioneel een git-commit en geeft de spraakmelding. Gebruik bij "einde", "afsluiten", "klaar voor vandaag", "sla alles op" of aan het eind van elke sessie.
argument-hint: "[optioneel: git]"
---

# /einde — niets vergeten tussen sessies

Zo weet de volgende sessie precies waar we waren. Werk de stappen in volgorde af.

## Stap 1 — Sessielog schrijven

Bestand: `docs/logs/JJJJ-MM-DD.md` (datum van vandaag; vraag de datum op met `date` / `Get-Date` als je twijfelt).
Bestaat het bestand al (meerdere sessies op één dag)? Voeg dan onderaan een nieuwe sectie `## Sessie [HH:MM]` toe; overschrijf nooit.

Format:

```markdown
# Log JJJJ-MM-DD

## Sessie HH:MM
**Doel:** [wat Attila wilde]

### Gedaan
- [concreet resultaat] → `pad/naar/bestand`

### Beslissingen
- [keuze + reden]

### Klanten & leads
- [klant/lead]: [wat er veranderde, nieuwe status]

### Problemen / open punten
- [wat nog niet werkt of wacht op iemand]

## Volgende stap
- [ ] [eerste concrete actie voor de volgende sessie]
```

De sectie `## Volgende stap` staat altijd onderaan: `scripts/dagstart.py` leest hem de volgende ochtend uit.

## Stap 2 — CLAUDE.md bijwerken (het brein)

Voeg alleen **blijvende** kennis toe, kort en op de juiste plek:
- nieuwe of gewijzigde prijzen, werkwijzen, designregels, tools → in de betreffende sectie;
- een les die fouten voorkomt → onder `## Geleerde lessen` als `- JJJJ-MM-DD: ...`;
- nieuwe skills → in de skill-tabel.

Geen dagelijkse details (die staan in de log). Geen persoonsgegevens van klanten of leads. Houd `CLAUDE.md` onder ~300 regels; vat oude lessen samen als het te lang wordt.

## Stap 3 — Klantgeheugen bijwerken

Voor elke klant waar vandaag aan gewerkt is: werk `status:` bij in `klanten/[slug]/klantprofiel.md`, voeg een regel toe onder `## Geheugen` en vink afgeronde punten af in `checklist.md`.

## Stap 4 — Structuurcheck (kort)

Controleer of alle paden die in `CLAUDE.md` genoemd worden bestaan, en of er nieuwe mappen of scripts zijn die er nog niet in staan. Repareer dode verwijzingen. (Uitgebreide check: `/structuur`.)

## Stap 5 — Opslaan in git (alleen als het argument `git` is, of Attila erom vraagt)

```bash
git add -A
git status
git commit -m "Sessie JJJJ-MM-DD: [korte samenvatting]"
```

Controleer vóór de commit in `git status` dat `echte_leads.csv`, `verzonden.txt` en `leads_status.json` **niet** worden meegenomen (ze staan in `.gitignore` vanwege AVG). Push alleen als Attila dat expliciet zegt.

## Stap 6 — Afronden

Meld in maximaal 5 regels: wat er gelogd is, wat er in `CLAUDE.md` veranderde, en de volgende stap. Speel daarna de spraakmelding af:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/zeg_klaar.ps1 -Tekst "Attila, de sessie is opgeslagen."
```
