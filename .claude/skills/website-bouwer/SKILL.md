---
name: website-bouwer
description: >-
  Bouwt high-end websites en demo-sites voor klanten en leads van Webdesign Attila, standaard met
  de design-taste-frontend bibliotheek: vloeiende hero-entree, een scroll-moment per pagina, nette
  hover-interacties, moderne secties en een snelheidscheck. Gebruik bij "bouw een website voor …",
  "maak een demo voor <lead>", "/website-bouwer", of bij een map in demos/ met een brief.md.
---

# Website-bouwer (met luxe animaties)

Elke site die deze skill bouwt gebruikt **altijd** de bibliotheek
`.claude/skills/design-taste-frontend/` (hierna `<taste>`). Die bibliotheek is leidend voor design,
animatie en controle; deze skill voegt de werkwijze van Webdesign Attila eromheen toe.

## 0. Laden (verplicht, vóór de eerste regel HTML)
1. Lees `<taste>/SKILL.md` volledig (huisregels, soort bedrijf, de run, checklist).
2. Lees daarna in `<taste>/references/`: `motion.md`, `moments.md`, `sections.md`, `perf.md`, `gate.md`.
3. Kopieer `<taste>/assets` naar de `assets`-map van de site en start vanaf `assets/starter.html`.
   Daar zit de motion-laag al in (`<html data-motion>`, `assets/motion/motion.css` en
   `assets/motion/motion.js`). Verwijder of overschrijf die nooit.

## 1. Brief
- Komt de opdracht uit de wachtrij: lees `demos/<slug>/brief.md` (gemaakt door
  `scripts/nacht_worker.py`, taak `demo_voorbereiden`): bedrijfsnaam, plaats, branche, huidige site.
- Bepaal de soort volgens `<taste>/SKILL.md` sectie 1. Een garage, kapper, hovenier of
  installateur is meestal **service**, een winkel of horeca **place**.
- Gebruik geen verzonnen adressen, telefoonnummers of KvK-nummers (huisregel 9).

## 2. Animatie-standaard (wat elke site krijgt)
Volg `motion.md` exact. Kort samengevat:

| Laag | Wat | Waar geregeld |
|---|---|---|
| Hero-entree | h1 regel voor regel, daarna lead en knoppen, ±1,1 s, één keer bij laden (`data-enter`) | `motion.md` |
| Scroll-moment | 1 moment per pagina, 2 vanaf 8 secties. Bij lokale bedrijven foto- of tekstgedreven (foto's die wisselen, een foto die "ontwikkelt", een statement dat oplicht) | `moments.mjs pick`, `moments.md` |
| Hover & klik | gelinkte kaart 2px omhoog, foto 1.02–1.03 zoom in zijn kader, knoppen stappen bij hover en drukken bij klik, onderstrepingen tekenen | motion-laag |
| Reduced motion | alles valt terug op stilstaand bij `prefers-reduced-motion` | motion-laag |

**Belangrijk, bewust zo:** "vloeiende scroll-animaties" betekent hier het **gedeelde scroll-moment**,
niet dat elke kaart in beeld fadet. De bibliotheek verbiedt standaard fade-ins op elke sectie,
parallax op tekst en smooth-scroll-libraries, omdat die goedkoop ogen en de site traag maken.
Shader/WebGL-effecten alleen bij tech/software (huisregel 8), nooit bij een lokale garage of bakker.

## 3. Bouwen
Volg `<taste>/SKILL.md` sectie 4 ("The run") stap 1 t/m 5: gate armen, eerst de copy (Nederlands,
`lang="nl"`), pagina plannen als schermen, alles **dealen** met de scripts (niet op gevoel kiezen),
bouwen vanuit `starter.html`. Moderne secties komen uit `<taste>/references/sections-library.md`.

Output per site:
```
demos/<slug>/index.html
demos/<slug>/assets/…
demos/<slug>/share.jpg
```

## 4. Snelheid (mag niet vertragen)
Snelheidsregels uit `perf.md`:
- Alleen `transform` en `opacity` animeren, geen layout-eigenschappen.
- Afbeeldingen met `width`/`height`, `loading="lazy"` onder de vouw, niet groter dan 2,2× de weergave.
- Maximaal 2 lettertype-families, geen zware animatie-libraries (GSAP/Locomotive) tenzij de klant erom vraagt.
- Draai altijd: `node <taste>/scripts/perf.mjs demos/<slug>/index.html`. Een FAIL los je op vóór oplevering.

## 5. Controle en oplevering
1. `node <taste>/scripts/copy-lint.mjs index.html --kind <kind>`
2. `node <taste>/scripts/consistency.mjs …` en `node <taste>/assets/layout/check.mjs …` (zie `<taste>/SKILL.md` stap 6)
3. `node <taste>/scripts/gate.mjs index.html` tot `GATE: PASS` (max. 3 rondes)
4. Rapporteer: GATE-regel, soort, gekozen palet en moment, perf-resultaat, wat de klant nog moet
   aanleveren (foto's, logo, echte teksten).

Vereist: Node 22+ en Chrome/Edge/Chromium (zie `<taste>/SKILL.md`).
