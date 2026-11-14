---
name: dagoverzicht
description: Strak ochtendoverzicht voor Webdesign Attila. Leest echte_leads.csv, leads_status.json, verzonden.txt, de klantmappen en de laatste sessielog, en zet op een rij wie Attila vandaag moet bellen, mailen of opvolgen en welke projecten openstaan. Gebruik bij "dagoverzicht", "wat moet ik vandaag doen", "ochtend", "dagstart" of aan het begin van de werkdag.
argument-hint: "[optioneel: aantal leads in de belronde, standaard 10]"
---

# /dagoverzicht — de dagstart van Webdesign Attila

Doel: binnen één minuut weet Attila wat hij vandaag doet. Geen lappen tekst: een lijst die hij afwerkt.

## Stap 1 — Ververs de cijfers (altijd eerst)

Draai in de Mainframe-map:

```bash
python scripts/dagstart.py --stil
```

Dit schrijft `docs/dagstart/JJJJ-MM-DD.md` op basis van de echte bestanden (zonder AI, dus de cijfers kloppen altijd). Lees daarna dat bestand. Werkt `python` niet, probeer `py`.

Bestaat een bestand niet (`echte_leads.csv`, `verzonden.txt`, `leads_status.json`), meld dat letterlijk en ga door met wat er wel is. Verzin nooit cijfers.

## Stap 2 — Verrijk met wat alleen jij kunt zien

1. **Laatste sessielog**: lees het nieuwste bestand in `docs/logs/` en neem de sectie "Volgende stap" over.
2. **Klantmappen**: lees per lopend project (`klanten/*/klantprofiel.md`, status niet `live`/`onderhoud`/`gearchiveerd`) de eerste 3 open punten uit `checklist.md`.
3. **Terugbellers**: noem bij elke terugbeller de notitie uit `leads_status.json`, zodat Attila weet waar het gesprek over ging.
4. **Belronde**: kies uit leads zonder status, met telefoonnummer en niet in `verzonden.txt` de beste kandidaten (argument = aantal, standaard 10). Voorkeur: **geen of zwakke website** (geen websitekolom, of een gratis/verouderd domein), en een branche uit de doelgroep in `CLAUDE.md`.

## Stap 3 — Lever op in exact dit format

```
DAGOVERZICHT — [weekdag dag maand]

CIJFERS
Leads [n] · nog niet gebeld [n] · terugbellen [n] · afspraken [n] · mails verzonden [n]

1. BELLEN (terugbellers eerst)
   [ ] Naam — 06-... — waar het over ging
2. DEMO'S / AFSPRAKEN
   [ ] Naam — wat er klaar moet (bijv. demo-homepage via /website-bouwer)
3. NIEUWE BELRONDE ([n])
   [ ] Naam — branche — plaats — 06-... — waarom deze (bijv. "geen website")
4. PROJECTEN
   Klant — status — eerstvolgende 3 checklist-punten
5. VOLGENDE STAP UIT VORIGE SESSIE
   ...

EERSTE ACTIE: [één concrete zin]
```

## Regels

- Lees `echte_leads.csv` en `verzonden.txt` alleen; pas ze nooit aan.
- Wil Attila een status aanpassen, schrijf dan in `leads_status.json` (of verwijs naar het CRM op http://localhost:8080/#leads).
- Stuur nooit zelf mails of WhatsApp-berichten. Je mag wel concepten klaarzetten.
- Houd het overzicht onder de 40 regels.
