---
name: structuur
description: Controleert of CLAUDE.md nog klopt met wat er echt op schijf staat - vindt dode verwijzingen, nieuwe mappen en scripts die niet beschreven zijn, weesbestanden en klantmappen zonder profiel, en repareert dat na akkoord. Gebruik bij "structuur", "klopt CLAUDE.md nog", "ruim op" of na een drukke sessie.
argument-hint: "[optioneel: snel | volledig]"
---

# /structuur — brein en schijf gelijk houden

## Stap 1 — Inventaris

Maak een lijst van wat er echt staat (sla `.git/`, `node_modules/`, `__pycache__/` en `.agents/` over):
- mappen op het hoogste niveau en in `docs/`, `scripts/`, `klanten/`, `.claude/skills/`;
- alle `*.py`-, `*.ps1`-, `*.bat`- en `*.html`-bestanden in de hoofdmap en `scripts/`.

## Stap 2 — Vergelijken met CLAUDE.md

1. **Dode verwijzingen**: elk pad of bestand dat `CLAUDE.md` noemt maar niet bestaat.
2. **Ontbrekende beschrijvingen**: scripts, skills of mappen die bestaan maar niet in `CLAUDE.md` staan.
3. **Verouderde beschrijvingen**: lees bij `volledig` elk Python-script in de hoofdmap kort door en controleer of de uitleg in `CLAUDE.md` (sectie Scripts) klopt met wat de code echt doet (welke bestanden het leest en schrijft, welke websites het bezoekt).
4. **Klantmappen**: mappen in `klanten/` zonder `klantprofiel.md` of zonder `status:`.
5. **Skills**: elke `.claude/skills/*/SKILL.md` heeft `name` en `description` in de frontmatter.
6. **Privacy**: staan `echte_leads.csv`, `verzonden.txt` en `leads_status.json` nog in `.gitignore`?

## Stap 3 — Rapport

```
STRUCTUURCHECK — [datum]
✗ Dode verwijzingen: ...
+ Nieuw, nog niet beschreven: ...
~ Beschrijving klopt niet: ...
! Klantmappen zonder profiel/status: ...
✓ In orde: ...
VOORSTEL: [genummerde lijst met aanpassingen]
```

## Stap 4 — Repareren

Voer de voorgestelde aanpassingen pas uit na Attila's akkoord ("ja" of de nummers). Verwijder nooit bestanden; verplaats twijfelgevallen hooguit naar `archief/`.
