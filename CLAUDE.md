# CLAUDE.md — het brein van Webdesign Attila

Dit bestand leest Claude Code aan het begin van elke sessie. Het is het permanente bedrijfsgeheugen ("Verstand"). Houd het actueel met `/einde`; houd het kort (onder ~300 regels). Dagelijkse details horen in `docs/logs/`, klantdetails in `klanten/[slug]/klantprofiel.md`.

---

## 1. Wie ik ben

- **Bedrijf:** Webdesign Attila — websites voor lokale MKB-bedrijven in Nederland.
- **Eigenaar:** Attila. Spreek hem aan met "Attila", in het Nederlands, kort en direct.
- **Website:** webdesignattila.nl
- **Telefoon / WhatsApp zakelijk:** NOG INVULLEN
- **KvK / btw-id:** NOG INVULLEN
- **Werkwijze:** leads zelf vinden (scraper), bellen/WhatsAppen/mailen, gratis demo laten zien, offerte, bouwen, opleveren, onderhoud.

## 2. Doelgroep

Lokale MKB-bedrijven zonder of met een verouderde website, die hun klanten uit de eigen regio halen: vakmensen (hoveniers, schilders, loodgieters, installateurs, bouw), kappers en schoonheidssalons, horeca, praktijken (fysio, coaching), winkels.
Wat ze willen: gevonden worden in hun plaats, gebeld of geappt worden, er professioneel uitzien. Wat ze niet willen: technisch gedoe, lange trajecten, vage prijzen.

## 3. Pakketten & prijzen

| Pakket | Prijs (eenmalig) | Inhoud |
| --- | --- | --- |
| **Start** | € 599,99 | VOORSTEL INHOUD: tot 3 pagina's, mobiel-vriendelijk, bel- en WhatsApp-knop, basis-SEO, contactformulier |
| **Groei** | € 999,99 | VOORSTEL INHOUD: tot 6 pagina's, lokale SEO (Schema.org LocalBusiness), echte Google-reviews, Google Bedrijfsprofiel gekoppeld |
| **Premium** | € 1.799,99 | VOORSTEL INHOUD: tot 10 pagina's, uitgebreide lokale SEO per dienst/plaats, teksten geschreven, extra ontwerpronde |

**Onderhoudsabonnementen** (per maand) — VOORSTEL, NOG BEVESTIGEN DOOR ATTILA:

| Abonnement | Prijs / maand | Inhoud |
| --- | --- | --- |
| Basis | € 19,99 | hosting-beheer, SSL, back-ups, updates |
| Zorgeloos | € 39,99 | Basis + kleine tekst-/foto-aanpassingen (30 min/maand) |
| Groei | € 69,99 | Zorgeloos + maandelijkse SEO-check en 1 nieuwe pagina/blog per kwartaal |

- **Btw:** NOG BEVESTIGEN (prijzen incl. of excl. 21% btw? KOR van toepassing?)
- **Betaling:** NOG BEVESTIGEN (voorstel: 50% bij akkoord, 50% bij livegang)
- **Doorlooptijd:** NOG BEVESTIGEN (voorstel: Start 5, Groei 10, Premium 15 werkdagen na aanlevering)

> Regel voor Claude: staat er bij een bedrag of voorwaarde nog `VOORSTEL` of `NOG BEVESTIGEN`, vraag Attila om bevestiging voordat het in een offerte komt. Werk deze sectie daarna bij en haal de markering weg.

## 4. Designregels (lichte, warme MKB-websites)

1. **Licht en warm:** crème/off-white achtergrond, warme donkere tekst, één accentkleur uit logo of branche. Nooit donkere tech-look, paarse gloed of neon.
2. **Editorial typografie:** serif-koppen + rustige sans-body, max. 2 fonts. Body **minimaal 17px**, regelhoogte 1.6, regels max. ~70 tekens.
3. **Meerpagina-opbouw:** Home, Diensten, Over ons, Reviews, Contact (demo = alleen Home).
4. **Ruime knoppen:** min. 48px hoog, korte labels (max. 3 woorden), **nooit tekst-overflow**; op mobiel gestapeld en 100% breed.
5. **Direct contact:** bel- (`tel:`) en WhatsApp-knop (`wa.me`) in header en hero, op mobiel een vaste balk onderin.
6. **Echte Google-reviews:** letterlijk, met naam en datum. Nooit verzinnen. Geen reviews = sectie weglaten.
7. **Lokale SEO:** dienst + plaats in title, H1 en meta description; Schema.org `LocalBusiness` JSON-LD; `aggregateRating` alleen met echte cijfers.
8. **Snel en toegankelijk:** statische HTML/CSS, WebP-foto's met alt-tekst, contrast 4.5:1, test op 390 / 768 / 1440 px.

Volledige werkwijze: skill `/website-bouwer`.

## 5. Tone of voice

- Je-vorm, warm, concreet, kort. Resultaat voor de klant eerst, techniek daarna.
- Geen AI-verraders: "Eerlijk?", "cruciaal", "essentieel", "een scala aan", "duiken in", "In een wereld waarin", "Al met al", "Kortom", het lange streepje (—).
- Volledig profiel: `docs/tone-of-voice.md` (nog niet gemaakt? draai `/tone-of-voice`).

## 6. Domeinen & hosting

- **Hosting en domeinen van klantsites:** Mijn.host (https://mijn.host).
- **WordPress-sites:** Claude kan erin werken via de Novamira MCP-koppeling (verbindingen "Novamira - Webdesign Attila" en "novamira-akloostermanriet").
- **Advertenties:** Google Ads. **Beeld/video:** Higgsfield.
- Domein per klant staat in `klanten/[slug]/klantprofiel.md` (veld `domein:`).

## 7. Mappenstructuur (de 4 pijlers)

```
Webdesign_Attila/
├── CLAUDE.md                  ← VERSTAND: dit brein
├── mainframe_app.html         ← Mainframe 2.0 web-app (4 schermen)
├── start_mainframe.py         ← lokale server, http://localhost:8080
├── start_mainframe.bat        ← dubbelklik om de Mainframe te starten (Windows)
├── mainframe_config.json      ← VERBINDINGEN: links, scripts, WhatsApp-/mailtekst
├── echte_leads.csv            ← leads van de scraper (alleen lezen)
├── verzonden.txt              ← verzonden mails (alleen lezen)
├── leads_status.json          ← belstatus + notities uit het CRM (door de app geschreven)
├── echte_scraper.py · mijnhost_jager.py · whatsapp_jager.py   ← eigen automatiseringen
├── klanten/                   ← elke klant/demo een eigen map met eigen geheugen
│   └── _sjabloon/             ← basis voor /nieuw-klant (niet aanpassen per klant)
├── docs/
│   ├── MAINFRAME_BLAUWDRUK.md ← onderzoeksrapport Het Mainframe + vertaling naar dit systeem
│   ├── logs/                  ← sessielogs JJJJ-MM-DD.md (/einde)
│   └── dagstart/              ← automatische ochtendbriefings (scripts/dagstart.py)
├── scripts/                   ← VANZELF: dagstart, spraakmelding, ochtendtaak, nieuwe klant
└── .claude/skills/            ← VAARDIGHEDEN: alle skills
```

## 8. Skills (Vaardigheden)

| Commando | Wat het doet |
| --- | --- |
| `/dagoverzicht` | Ochtendoverzicht: wie bellen, wie opvolgen, welke projecten |
| `/nieuw-klant` | Klantmap met profiel, checklist en submappen (`scripts/nieuw_klant.py`) |
| `/website-bouwer` | Meerpagina MKB-website of demo volgens de designregels |
| `/offerte` | Offerte + voorstelmail met de pakketten hierboven |
| `/einde` | Sessielog, CLAUDE.md en klantgeheugen bijwerken, optioneel git |
| `/skill-maker` | Zes stappen: terugkerende taak → nieuwe skill |
| `/structuur` | Controleert of CLAUDE.md nog klopt met de schijf |
| `/tone-of-voice` | Interview → `docs/tone-of-voice.md` |
| `/design-taste-frontend` | Externe ontwerp-skill (tasteskill); de regels in sectie 4 gaan voor |

## 9. Scripts & bestanden

| Bestand | Wat het doet | Claude mag |
| --- | --- | --- |
| `echte_scraper.py` | Verzamelt bedrijven en schrijft ze naar `echte_leads.csv` (controleer details met `/structuur volledig`) | lezen, draaien op verzoek |
| `mijnhost_jager.py` | Eigen automatisering rond Mijn.host — exacte werking nog beschrijven na `/structuur volledig` | lezen, draaien op verzoek |
| `whatsapp_jager.py` | Eigen WhatsApp-automatisering — exacte werking nog beschrijven na `/structuur volledig` | lezen, alleen draaien na expliciet akkoord |
| `generator.py` | FastAPI-app: aanvraagformulier → AI-conceptsite via Groq + Telegram-melding (sleutels via omgevingsvariabelen `GROQ_API_KEY`, `TELEGRAM_BOT_TOKEN`) | lezen, aanpassen op verzoek |
| `start_mainframe.py` | Mainframe-server op poort 8080 (alleen standaardbibliotheek) | aanpassen op verzoek |
| `scripts/dagstart.py` | Schrijft `docs/dagstart/JJJJ-MM-DD.md` (`--spreek` = hardop) | draaien |
| `scripts/nieuw_klant.py` | Maakt `klanten/[slug]/` uit het sjabloon | draaien |
| `scripts/zeg_klaar.ps1` | Spraakmelding met de Nederlandse Windows-stem | draaien |
| `scripts/installeer_ochtendtaak.ps1` | Zet de dagstart om 07:00 in Windows Taakplanner | alleen op verzoek |
| `echte_leads.csv`, `verzonden.txt` | Brondata van de scrapers/mailmachine | **alleen lezen, nooit wijzigen** |
| `leads_status.json` | `{lead-id: {status, notitie, bijgewerkt}}`; statussen: `geen_gehoor`, `terugbellen`, `afspraak`, `niet_interessant` | lezen, bijwerken op verzoek |

## 10. Werkafspraken voor Claude

1. **Sessiestart:** lees de nieuwste log in `docs/logs/` en noem in één zin waar we gebleven waren.
2. **Eerst begrijpen:** bij een vage of grote opdracht eerst maximaal 5 gerichte vragen, dan een plan van max. 5 stappen, dan bouwen.
3. **Nooit zonder akkoord:** mails of WhatsApp-berichten versturen, iets publiceren of live zetten, bestanden verwijderen, betalen, pushen naar GitHub.
4. **Niets verzinnen:** geen reviews, cijfers, adressen, KvK-nummers of prijzen die niet in de bronbestanden staan.
5. **Privacy (AVG):** leads en klantgegevens zijn persoonsgegevens. `echte_leads.csv`, `verzonden.txt` en `leads_status.json` staan in `.gitignore` en gaan nooit naar GitHub of externe diensten. Zet geen klantgegevens in dit bestand.
6. **Spraakmelding:** rond je een grote bouw- of onderzoekstaak af (of eindigt `/einde`), voer dan als allerlaatste stap uit:
   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/zeg_klaar.ps1
   ```
   Dat zegt hardop: "Attila, Claude is klaar!". Eigen tekst: voeg `-Tekst "..."` toe.
7. **Afsluiten:** eindig een werksessie met `/einde`.

## 11. Geleerde lessen

<!-- /einde voegt hier blijvende lessen toe als: - JJJJ-MM-DD: les -->
- 2026-11-14: Mainframe opgezet (4 pijlers, 8 skills, web-app op poort 8080, dagstart + spraakmelding). Bron en achtergrond: `docs/MAINFRAME_BLAUWDRUK.md`.
