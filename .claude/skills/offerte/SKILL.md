---
name: offerte
description: Genereert een professionele, overtuigende offerte plus een korte voorstelmail voor een klant van Webdesign Attila, op basis van de pakketten Start (€ 599,99), Groei (€ 999,99) en Premium (€ 1.799,99) en de onderhoudsabonnementen uit CLAUDE.md. Gebruik bij "offerte", "prijsvoorstel", "voorstel sturen" of als een klant status offerte krijgt.
argument-hint: "[klantmap of bedrijfsnaam] [optioneel: pakket]"
---

# /offerte — offerte + voorstelmail

## Stap 1 — Prijzen uit het brein, nooit uit je hoofd

Lees de sectie **Pakketten & prijzen** in `CLAUDE.md`. Dat is de enige bron voor bedragen.

- Staat bij de onderhoudsabonnementen of bij btw nog `VOORSTEL` of `NOG BEVESTIGEN`? Vraag Attila eerst één keer om die te bevestigen en werk `CLAUDE.md` bij. Stuur geen offerte met onbevestigde bedragen.
- Reken niets af of op zonder dat Attila het noemt (korting, meerwerk).

## Stap 2 — Klantcontext

Lees `klanten/[slug]/klantprofiel.md` (en `teksten/teksten.md` als die er is). Bestaat de map niet: draai eerst `/nieuw-klant`.

Bepaal het pakket: uit het argument, uit het profiel, of adviseer er één met één zin waarom (aantal pagina's, behoefte aan lokale SEO, extra's). Noem de andere twee als alternatief.

## Stap 3 — Schrijf de offerte

Bestand: `klanten/[slug]/offerte-JJJJ-MM-DD.md` (en, als Attila daarom vraagt, een opgemaakte `offerte-JJJJ-MM-DD.html` in de huisstijl: licht, warm, 17px+, printbaar via `@media print`).

Opbouw:

1. **Kop**: Webdesign Attila · offertenummer `WA-JJJJ-[slug]` · datum · geldig tot (datum + 30 dagen).
2. **Voor**: bedrijfsnaam, contactpersoon, plaats.
3. **Jouw situatie** (3 zinnen): wat er nu mist (bijv. geen website, niet mobiel, niet vindbaar in [plaats]) en wat dat kost aan klanten. Alleen feiten die bekend zijn.
4. **Wat je krijgt**: het gekozen pakket met alle onderdelen uit `CLAUDE.md`, als korte bullets in klanttaal (resultaat eerst, techniek daarna).
5. **Investering**: tabel met pakketprijs, eventueel onderhoudsabonnement per maand, btw-regel volgens `CLAUDE.md`, totaal. Bedragen in Nederlandse notatie: `€ 999,99`.
6. **Planning**: intake → ontwerp → feedbackronde → livegang, met indicatie in werkdagen uit `CLAUDE.md`.
7. **Voorwaarden**: betaling volgens `CLAUDE.md`, wat de klant aanlevert (logo, foto's, teksten of akkoord dat wij schrijven), domein/hosting via Mijn.host.
8. **Akkoord**: "Akkoord? Antwoord op deze mail of bel/app [telefoonnummer Attila]."

## Stap 4 — Schrijf de voorstelmail

Max. 120 woorden, je-vorm, warm en concreet, volgens `docs/tone-of-voice.md` als die bestaat. Structuur: persoonlijke opening (verwijs naar het gesprek of de demo) → het belangrijkste resultaat → pakket + prijs in één zin → duidelijke volgende stap. Geen "Eerlijk?", geen "cruciaal", geen lange streepjes.

Lever de mail als blok:

```
Onderwerp: ...
---
[mailtekst]
```

## Stap 5 — Bijwerken & melden

- Zet in `klantprofiel.md` de status op `offerte`, `pakket:` op het gekozen pakket, en een geheugenregel met datum en bedrag.
- Vink "Pakket gekozen en offerte verstuurd" pas af als Attila zegt dat hij hem verstuurd heeft.
- **Verstuur nooit zelf.** Attila controleert en verstuurt.
