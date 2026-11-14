---
name: nieuw-klant
description: Maakt met één commando een complete klantmap aan in klanten/[bedrijfsnaam]/ met klantprofiel.md (eigen geheugen van de klant), checklist voor ontwerp, SEO en oplevering, en mappen voor teksten, foto's en de website. Gebruik bij "nieuwe klant", "nieuw project", "maak een klantmap", of zodra een lead op "Afspraak / Demo" staat.
argument-hint: "[bedrijfsnaam] [optioneel: branche, plaats, pakket, contact]"
---

# /nieuw-klant — klantmap in één keer goed

## Stap 1 — Verzamel de gegevens

Haal uit het argument en het gesprek: **bedrijfsnaam** (verplicht), branche, plaats, pakket (`Start`, `Groei`, `Premium` of `Maatwerk`) en contact.

- Staat het bedrijf in `echte_leads.csv`? Neem dan telefoon, website, plaats en branche daaruit over (lees het bestand, wijzig het niet).
- Ontbreekt de bedrijfsnaam, vraag die. Vraag niet naar de rest: dat mag later.

## Stap 2 — Maak de map met het script (niet met de hand)

```bash
python scripts/nieuw_klant.py "Bedrijfsnaam" --branche "..." --plaats "..." --pakket Groei --contact "Naam, 06-..."
```

Laat lege opties weg. Het script kopieert `klanten/_sjabloon/`, vult alle velden in en **overschrijft nooit** een bestaande map. Meldt het script dat de map al bestaat: stop en vraag Attila of je de bestaande map moet bijwerken.

Resultaat:

```
klanten/[slug]/
├── klantprofiel.md      ← geheugen van deze klant (status bovenaan)
├── checklist.md         ← intake → ontwerp → bouw & SEO → oplevering
├── teksten/
│   ├── teksten.md
│   └── reviews.md       ← alleen echte Google-reviews, letterlijk
├── fotos/
└── website/             ← hier bouwt /website-bouwer
```

## Stap 3 — Vul het profiel aan met wat bekend is

Werk `klanten/[slug]/klantprofiel.md` bij met de gegevens uit stap 1 (website, telefoon, Google-profiel). Zet de status:
- `lead` als er nog geen gesprek was
- `demo` als Attila een demo gaat maken
- `offerte` als er een offerte uitgaat

Schrijf onder "Geheugen" één regel met de datum en wat er is afgesproken.

## Stap 4 — Meld kort terug

```
Klantmap klaar: klanten/[slug]/
Status: [status] · Pakket: [pakket]
Volgende stap: [bijv. /website-bouwer voor een demo-homepage, of /offerte]
```

## Regels

- Persoonsgegevens van de klant blijven in de klantmap; zet ze niet in `CLAUDE.md`.
- Verzin geen reviews, KvK-nummers, adressen of openingstijden. Onbekend = leeg laten.
