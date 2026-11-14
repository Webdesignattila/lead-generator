---
name: website-bouwer
description: Bouwt een complete, meerpagina MKB-website (of demo-homepage) in de huisstijl van Webdesign Attila - licht, warm en editorial, 17px+ leesbare tekst, ruime knoppen zonder tekst-overflow, echte Google-reviews, directe bel- en WhatsApp-knoppen en lokale SEO met Schema.org LocalBusiness. Gebruik bij "bouw een website", "maak een demo", "homepage voor [bedrijf]", of na /nieuw-klant.
argument-hint: "[klantmap of bedrijfsnaam] [optioneel: demo | volledig]"
---

# /website-bouwer — websites die lokale klanten opleveren

Bouwt in `klanten/[slug]/website/`. Statische HTML + CSS (+ minimaal vanilla JS), zonder build-stap, zodat het direct op Mijn.host kan. Voor WordPress-klanten: zelfde regels, uitvoeren via de Novamira-koppeling.

Voor extra ontwerpsmaak mag je de geïnstalleerde skill `design-taste-frontend` raadplegen, maar **de regels hieronder winnen altijd** (licht en warm, geen donkere tech-look, geen shader-effecten voor MKB).

## Stap 1 — Briefing uit het geheugen (niet vragen wat al bekend is)

Lees `klanten/[slug]/klantprofiel.md`, `teksten/teksten.md`, `teksten/reviews.md` en de map `fotos/`. Bestaat de klantmap niet: draai eerst `/nieuw-klant`.

Ontbreekt iets essentieels (diensten, plaats, telefoonnummer), stel maximaal 4 vragen in één bericht. Bij `demo` mag je redelijke aannames doen, gemarkeerd met `<!-- AANNAME: ... -->` in de HTML.

## Stap 2 — Structuur (meerpagina)

| Pagina | Bestand | Inhoud |
| --- | --- | --- |
| Home | `index.html` | Hero (dienst + plaats in H1), 3 kernvoordelen, diensten-teaser, 3 reviews, werkgebied, CTA-band |
| Diensten | `diensten.html` | Per dienst: wat, voor wie, resultaat, CTA |
| Over ons | `over-ons.html` | Verhaal, mensen, waarom kiezen |
| Reviews | `reviews.html` | Alle echte Google-reviews + link naar Google-profiel |
| Contact | `contact.html` | Bel, WhatsApp, e-mail, formulier, adres/werkgebied, openingstijden |

Bij `demo`: alleen `index.html`, maar wel compleet en mobiel perfect.
Gedeelde stijl in `css/stijl.css`, foto's in `img/` (WebP, met `width`/`height` en `loading="lazy"` behalve de hero).

## Stap 3 — Designregels Webdesign Attila (verplicht)

**Kleur & sfeer**
- Lichte, warme basis: crème/off-white achtergrond (bijv. `#FAF6EE`), donkere warme tekst (`#2B2721`), één accentkleur uit het logo of de branche (bijv. olijfgroen, terracotta, diepblauw). Geen puur zwart, geen paars/neon "AI-look", geen donkere hero's.
- Kleuren als CSS-variabelen op `:root`.

**Typografie**
- Body minimaal **17px** (`font-size: 1.0625rem`), regelhoogte 1.6, regels maximaal ~70 tekens (`max-width: 68ch`).
- Editorial koppen: serif (bijv. Fraunces, Playfair Display, Lora) gecombineerd met een rustige sans (bijv. Manrope, Inter, Source Sans 3). Maximaal 2 fonts, via Google Fonts met `display=swap`.
- H1 met `clamp()` zodat hij nooit buiten beeld loopt op 390px.

**Knoppen**
- Minimaal **48px hoog**, ruime padding (`14px 24px`), `border-radius` 999px of 12px.
- Korte labels (max. 3 woorden: "Bel direct", "WhatsApp ons", "Offerte aanvragen").
- **Nooit tekst-overflow**: `white-space: nowrap` alleen als de knop in een `flex-wrap: wrap`-rij staat; op mobiel knoppen `width: 100%` gestapeld. Controleer elke knop op 390px.

**Conversie**
- Bel-knop (`tel:+31...`) en WhatsApp-knop (`https://wa.me/31...?text=...`) in de header én in de hero.
- Op mobiel een vaste balk onderin met "Bel" en "WhatsApp" (en `padding-bottom` op `body` zodat niets wegvalt).
- Elke pagina eindigt met een CTA-band.

**Echte reviews**
- Alleen reviews uit `teksten/reviews.md` (letterlijk, met voornaam, sterren en datum). Nooit verzinnen of herschrijven. Geen reviews beschikbaar? Laat de sectie weg en zet `<!-- TODO: echte Google-reviews toevoegen -->`.
- Link naar het Google Bedrijfsprofiel van de klant.

**Lokale SEO**
- Per pagina een unieke `<title>` (dienst + plaats + bedrijfsnaam, max. 60 tekens) en `<meta name="description">` (max. 155 tekens, met plaats).
- Eén H1 per pagina, logische H2/H3.
- `lang="nl"`, canonical-URL, Open Graph-tags.
- Schema.org JSON-LD `LocalBusiness` (of het specifiekere type, bijv. `Plumber`, `HairSalon`, `Restaurant`) met `name`, `telephone`, `address` of `areaServed`, `url`, `openingHoursSpecification`. Voeg `aggregateRating` **alleen** toe met echte cijfers uit het Google-profiel.
- `sitemap.xml` en `robots.txt` bij een volledige site.

**Toegankelijkheid & snelheid**
- Contrast minimaal 4.5:1, zichtbare focus-stijl, alt-teksten op alle foto's.
- Geen zware frameworks; geen carrousels. Doel: Lighthouse 90+ op mobiel.

## Stap 4 — Controleren voor je "klaar" zegt

1. Open de pagina's in een browser op 390px, 768px en 1440px breed. Geen horizontale scroll, geen afgesneden knoppen of koppen.
2. Klik elke `tel:`- en `wa.me`-link na op het juiste nummer.
3. Valideer de JSON-LD (geldige JSON, geen verzonnen velden).
4. Zoek in alle bestanden op `AANNAME` en `TODO` en noem ze in je oplevering.

## Stap 5 — Oplevering

- Vink de afgeronde punten af in `klanten/[slug]/checklist.md` en zet de status in `klantprofiel.md` (`demo` of `bouw`).
- Meld: welke bestanden, open TODO's/aannames, en de volgende stap (feedback klant / `/offerte`).
- Rond af met de spraakmelding: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/zeg_klaar.ps1`
