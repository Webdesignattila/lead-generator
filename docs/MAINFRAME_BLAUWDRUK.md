# MAINFRAME BLAUWDRUK

**Onderzoek naar Bart Boonstra, Slim Werken AI en "Het Mainframe", vertaald naar de Webdesign Attila Mainframe**

Onderzoeksdatum: 14 november 2026 · Opgesteld voor: Webdesign Attila

---

## 0. Leeswijzer en betrouwbaarheid

Dit rapport scheidt drie soorten informatie. Zo zie je steeds waar iets vandaan komt:

| Markering | Betekenis |
| --- | --- |
| **[BRON]** | Staat letterlijk of vrijwel letterlijk op een openbare pagina (bron onderaan). |
| **[REVIEW]** | Komt van een onafhankelijke reviewer (reviewreus.nl, affiliate). |
| **[EIGEN]** | Mijn eigen invulling of implementatie voor Webdesign Attila. Niet afkomstig van Bart Boonstra. |

**Wat ik wél kon lezen:** hetmainframe.nl, hetmainframe.nl/vip, hetmainframe.nl/enterprise, bartboonstra.nl, bartboonstra.nl/linkinbio, bartboonstra.nl/shop, slimwerken.ai, slimwerken.ai/shop, de openbare skill-index (slimwerken.ai/landing/skills), de Orca-gids (slimwerken.ai/landing/orca), de tone-of-voice-gids (slimwerken.ai/landing/toneofvoice) en drie reviews op reviewreus.nl.

**Wat ik níet kon lezen (eerlijk gemeld):**
- De community-weggevers achter een login (o.a. `link.slimwerken.ai/skill` — "Stop met agents bouwen: het stappenplan" — en `link.slimwerken.ai/website`). De tool gaf `login_required`.
- De inhoud/transcripts van YouTube-video's: YouTube gaf alleen titel en beschrijving terug, geen ondertitels.
- De video "NOOIT Claude Gebruiken in de App - Zo installeer je Claude Code en VScode" en "Het Nieuwe Werken met AI": met deze exacte titels niet gevonden via zoekmachines. Wat over dat onderwerp wél openbaar is, staat in hoofdstuk 6.
- De letterlijke koppen van de vier pijlers. De paginatekst kwam zonder kopjes binnen; de vier blokken zelf zijn wel duidelijk (zie hoofdstuk 2). De namen *Verbindingen / Verstand / Vaardigheden / Vanzelf* komen uit jouw opdracht en passen exact op die vier blokken.
- Modal, Apify en WooCommerce worden op de gelezen pagina's **niet** genoemd. Moneybird wel (als skill). Zie hoofdstuk 2.1.

Het Mainframe is betaalde cursusinhoud. Dit rapport bevat alleen wat Bart Boonstra zelf openbaar deelt, plus een eigen, onafhankelijke bouw van hetzelfde principe. Er is geen betaalde inhoud gekopieerd.

---

## 1. Wie is Bart Boonstra en wat is Het Mainframe?

### 1.1 De persoon [BRON]
- Nederlandse ondernemer uit Utrecht. Eerst zeven jaar televisie (Popstars op SBS6, Secret Story op Net5, presentator bij Nickelodeon), daarna een eigen videobedrijf (Grow Media, opgebouwd en verkocht), nu **Slim Werken AI**.
- Positionering: *"Als ik slaap, doet mijn AI het werk. Ik leer ondernemers AI voor zich laten werken."*
- Geen developer; hij werkt met **Claude Code** en noemt het in een TikTok-post de basis van zijn hele bedrijf (klantwerk, landingspagina's, community, betalingen, onderzoek, trainingen). Voor afbeeldingen gebruikt hij ChatGPT, "maar gewoon binnen Claude Code".
- Cijfers op zijn sites (zelf gerapporteerd): 610+ cursisten, 4.300–5.000+ community-leden, workshops tot 1.200 mensen, "#1 NL Favikon AI Workflow Automation, juli 2026".

### 1.2 De definitie [BRON]
> "Het Mainframe is een manier van werken met AI, ontwikkeld door Bart Boonstra. Je zet je kennis, je vaste werkwijzen en je programma's op een vaste plek op je eigen computer. Daardoor kent je AI je bedrijf en doet hij het werk: je offerte, je mail, je facturen. Jij kijkt het na."

Kernidee: **"Het verschil is niet het model. Het is wat eromheen staat."** AI is getraind op bijna alles, behalve op hoe jóuw bedrijf werkt. Daarom zet je in week 1 eerst je bedrijf in je Mainframe.

### 1.3 Het aanbod en de prijzen [BRON, november 2026]

| Product | Prijs | Wat |
| --- | --- | --- |
| Het Mainframe (cursus) | € 599 (nov. 2026) / € 699 (jan. 2027), ex btw | 8 weken, 1 livesessie per week (vrijdag 9:00–12:00), app Mainframe 2.0 vanaf week 1 |
| Slim Werken community | € 69 p/m ex btw | eerste 11 weken inbegrepen, daarna maandelijks opzegbaar |
| Mainframe VIP | € 3.500 + € 69 p/m | Bart komt 2 uur langs, installeert Mainframe + Jarvis, maakt één echte taak werkend |
| Mainframe Enterprise | € 7.900 installatiedag + € 199 p/m hulplijn | gedeelde lagen voor teams (persoonlijk / team / bedrijf / directie) |
| Spreeksessie/workshop | € 2.500 per sessie | max. 3 uur |
| "Los" systeem met app | € 299 (genoemd als waarde) | zit bij de cursus in |

Prijsverloop per groep [BRON/REVIEW]: april € 300 → mei € 429 → juni € 459 → juli € 489 → aug. € 539 → sept./okt. € 569 → nov. € 599 → jan. 2027 € 699.
**Dag-Terug-Garantie** [BRON]: geld terug als je na 8 weken geen werkdag per week bespaart, mits ≥ 90% lessen, alle 8 opdrachten gemaakt en gedeeld, minstens één keer hulp gevraagd, aanvraag binnen 14 dagen.
Benodigd: een computer waarop je zelf mag installeren + een eigen betaald Claude-abonnement. Werkt het best met Google Workspace; Outlook kan ook [REVIEW].

---

## 2. De 4-pijler-architectuur

Op hetmainframe.nl staan vier blokken, elk met *"een eigen scherm in de app. Groen is goed."* [BRON]:

| Pijler | Wat Bart erover zegt [BRON] | Onze vertaling [EIGEN] |
| --- | --- | --- |
| **Verbindingen** | "Je mail, je agenda, je bestanden, je boekhouding. Je koppelt ze een keer. Daarna hoef je nooit meer iets over te typen van het ene programma naar het andere." | `mainframe_config.json` + scherm 4 van de app; MCP-koppelingen in Claude Code (Gmail, Novamira/WordPress, Higgsfield) |
| **Verstand** | "Wie je bent, wat je verkoopt, hoe je schrijft. En alles wat je ooit voor een klant maakte. Je ziet het op een scherm en vult het aan. Je oude gesprekken uit ChatGPT neem je mee. Nooit meer je bedrijf opnieuw uitleggen." | `CLAUDE.md`, `klanten/[slug]/klantprofiel.md`, `docs/logs/`, `docs/tone-of-voice.md` |
| **Vaardigheden** | "Een skill is een vaste werkwijze die je een keer vastlegt. Hoe jij een offerte maakt, hoe je een klant mailt, hoe je je btw-overzicht klaarzet. Daarna doet hij het elke keer precies zo." | `.claude/skills/` (8 eigen skills) + scherm 3 van de app |
| **Vanzelf** | "Je posts 's nachts klaarzetten. 's Ochtends een overzicht van je inbox. Elke maandag de openstaande facturen. [...] Jij keurt goed, hij doet de rest." | `scripts/dagstart.py` om 07:00 via Windows Taakplanner, `scripts/zeg_klaar.ps1`, scherm 1 van de app |

Op de Enterprise-pagina staan dezelfde vier, met als vijfde belofte "Documenten, een website, zelfs een eigen app. Zo zeg je ook nog een paar abonnementen op." [BRON]

### 2.1 Verbindingen — hoe hij koppelt

Openbaar bevestigd [BRON]:
- **Koppelen gebeurt pas later en stap voor stap**: "Je hoeft niks te koppelen om te starten. [...] koppelingen komen pas later, één voor één, alleen als jij dat wilt." Week 3 heet: "Je koppelt je programma's. Veilig, en jij bepaalt wat."
- **Moneybird**: eigen skill `/moneybird` — "Praat met je Moneybird-boekhouding in gewone taal. Vraag wie je nog moet betalen [...] of laat een factuur als concept klaarzetten. Een wizard koppelt het voor je."
- **Plug&Pay**: skills `/plugandpay` (inloggen via browser, geen sleutel op je computer) en `/plugandpayExtra` (API-sleutel, alles eerst "droog").
- **Pinecone** (langetermijngeheugen) + OpenAI-sleutel voor embeddings: skill `/pinecone`.
- **Blotato** (social uploads), **Gemini** (thumbnails), **OpenRouter** (productfoto's, storyboards), **Runway** (video), **Higgsfield** (video, "vier stappen, geen terminal"), **KIE** (productpagina-beelden).
- **Scrapling** ("Claude komt niet binnen bij Coolblue, Scrapling wel") als gratis scraper.
- **Tailscale** om computers aan elkaar te koppelen (`/verbindMijnComputers`, Orca remote servers).
- Veiligheidsprincipe: "Mailen, posten, verwijderen: dat vraagt hij eerst aan jou. Jij houdt het stuur." en "Wachtwoorden staan nooit los in bestanden." (Enterprise).

Niet gevonden op openbare pagina's: **Modal, Apify, WooCommerce**. Deze tools passen wel in het patroon (API of MCP aan Claude Code hangen), maar ik kan niet bevestigen dat Bart ze gebruikt of hoe.

Patroon dat hieruit volgt [EIGEN]: per dienst één skill met een **wizard** die (1) uitlegt welk account/sleutel nodig is, (2) de sleutel in een omgevingsvariabele of de systeemsleutelbos zet en niet in een bestand in de projectmap, (3) eerst een lees-actie test, (4) schrijfacties altijd als concept of "dry run" laat zien.

### 2.2 Verstand — het permanente bedrijfsgeheugen

[BRON]:
- Week 1: "Je downloadt Het Mainframe, zet je kennis erin via de app (een wizard), en hij werkt direct voor je."
- Week 2: "Een geheugen dat blijft, en een back-up van alles."
- Week 6: "Elke klant een eigen plek. Plus je eigen dashboard, ook op je telefoon."
- Het systeem "wordt elke week slimmer": "Verbeter je iets, dan onthoudt hij het. Volgende keer doet hij het meteen goed."
- Enterprise gebruikt **vaste lagen**: *persoonlijk* (wie je bent, hoe je schrijft, eigen projecten; nooit naar het bedrijf, wel naar je eigen kluis/back-up) → *team/afdeling* → *bedrijf* (klanten, prijzen, afspraken, manier van werken) + een *directielaag*. "Aan de laag zie je meteen van wie iets is, en wie het mag zien."
- Skills `/structuurSessie` ("Controleert aan het eind van een sessie of CLAUDE.md nog klopt") en `/structuurProject` ("vergelijkt wat er op schijf staat met wat CLAUDE.md beschrijft") bevestigen dat **CLAUDE.md** het centrale contextbestand is.
- Tone of voice als apart bestand **`tone-of-voice.md`** (volledig gratis interview-prompt, zie 4.2).

Onze implementatie [EIGEN]:
- `CLAUDE.md` = bedrijfslaag (wie, doelgroep, prijzen, designregels, hosting, scripts, werkafspraken, geleerde lessen).
- `klanten/[slug]/klantprofiel.md` = klantlaag met frontmatter (`status`, `pakket`, `deadline`…) die de app uitleest, plus een sectie "Geheugen".
- `docs/logs/JJJJ-MM-DD.md` = sessiegeheugen; de sectie "Volgende stap" wordt elke ochtend automatisch uitgelezen.
- `docs/tone-of-voice.md` = schrijfstijl (te maken met `/tone-of-voice`).

### 2.3 Vaardigheden — skills

[BRON] Definitie: "Een skill is een vaste werkwijze die je een keer vastlegt." En: "Stop met het bouwen van AI-agents. [...] Een skill is gewoon een handleiding voor een klus die je vaker doet." Cursisten bouwen eigen skills en "pakken kant-en-klare uit de bibliotheek".

**De openbare skill-index van Bart** (slimwerken.ai/landing/skills, stand 14-11-2026) [BRON]:

| Categorie | Skills (eigen) | Aanraders van anderen |
| --- | --- | --- |
| Werkwijze & geheugen | `/mainframe-faq`, `/vragen`, `/nu`, `/logs`, `/einde`, `/structuurSessie`, `/structuurProject`, `/ochtend`, `/insights`, `/pinecone`, `/verbindMijnComputers` | `/superpowers` (obra) |
| Denken & beslissen | `/consensus` (5 agents: voorzichtig, klantgericht, data-gedreven, dwarsligger, dromer), `/debate` (4 rollen, 2 rondes) | — |
| Content & social | `/transcribeer` (YouTube-kanaal → tekst → expert-skill), `/viralhook`, `/shortsUpload`, `/thumbnail`, `/productfoto` | — |
| Video | `/storyboard`, `/storyboard2video`, `/genereer-video`, `/ai-video-storyboard`, `/ondertiteling`, `/premiere` | — |
| Sales & copy | `/hormozi-sales-nl`, `/landingspaginaTekst` | `/copywriting`, `/cold-email` |
| Data & rapporten | `/excel`, `/eigen-faq` | — |
| Design & UI | `/websitecloner`, `/scrollsite`, `/websitecheck`, `/mainframe-stijl`, `/productpagina` | `/impeccable`, `/high-end-visual-design`, `/ui-ux-pro-max`, `/minimalist-ui`, `/design`, `/design-system`, `/banner-design` |
| Marketing & groei | — | `/marketing-psychology`, `/pricing-strategy`, `/launch-strategy`, `/marketing-ideas`, `/content-strategy`, `/email-marketing-bible` |
| Presentaties | — | `/frontend-slides`, `/slides`, `/excalidraw` |
| Security | `/pentest-advisor` | — |
| Privacy & AVG | `/avg-bible`, `/anonimiseer` (lokaal, zonder AI/internet) | — |
| Koppelingen | `/moneybird`, `/plugandpay`, `/plugandpayExtra` | — |

Belangrijke details uit de index [BRON]:
- **`/einde`**: "Sluit een sessie netjes af: logs schrijven, CLAUDE.md syncen, geheugen opslaan in Pinecone en alles pushen naar GitHub." Vereist `/logs`, `/structuurSessie` en `/pinecone`.
- **`/logs`**: "Documenteert wat er in de sessie is gedaan en slaat dat op als een dagelijks logbestand."
- **`/ochtend`**: "Maakt elke ochtend een persoonlijke briefing met het weer, je agenda, je to-do-lijst en mails die op antwoord wachten. Slaat die op als bestand en stuurt ze eventueel als mail."
- **`/mainframe-stijl`**: "warm creme, dikke koppen en een oranje accent. Geen paarse gloed meer die iedereen als AI herkent." (Dezelfde richting als jouw lichte, warme stijl.)
- **`/websitecheck`**: controleert prijzen, datums, links, mobiel, snelheid, vindbaarheid en veiligheid; "past niets aan zonder jouw akkoord."
- Gratis weggever "Check een skill voor je hem installeert": "1 op de 20 Claude-skills is gemaakt met kwade bedoelingen" — tool SkillSpector (NVIDIA), ±70 waarschuwingssignalen.

Niet gevonden in de openbare index: `/saveGithub`, `/loadGithub`, `/dagoverzicht`, `/nieuw-klant`, `/nieuw-project`, `/archief-klant`. Mogelijk bestaan ze in de cursus; openbaar kon ik ze niet bevestigen. De functie van save/load naar GitHub zit openbaar in `/einde` ("alles pushen naar GitHub").

**Het 6-stappen skill-stappenplan** [BRON, alleen de omschrijving]: "Laat Claude een skill voor je bouwen in zes stappen, met alle prompts erbij. Van je ideale situatie schetsen tot testen tot het af is." De stappen zelf staan achter de community-login. Onze eigen uitwerking staat in `/skill-maker` [EIGEN]: (1) probleem + ideale situatie, (2) huidig stappenplan uitpluizen, (3) grenzen en regels, (4) skill schrijven, (5) testen op een echt voorbeeld, (6) vastleggen in CLAUDE.md.

### 2.4 Vanzelf — automatisering, Jarvis en Mainframe 2.0

[BRON]:
- **Week 4**: "Elke ochtend om 7 uur een overzicht in je mail. Ook met je laptop dicht."
- **Orca** (gratis, open source, onorca.dev): "Je Claude-sessies draaien op een computer die altijd aanstaat. Jij kijkt mee vanaf je telefoon of je laptop." Bart: "Om half zeven staan mijn antwoorden al klaar" — een vaste prompt op een vaste tijd leest zijn mail, LinkedIn en Instagram en zet antwoorden klaar. Zie het stappenplan in 5.3.
- **Mainframe 2.0 (app)**: "de plek waar je je systeem ziet en bestuurt. Werk zelf slim in VS Code of Orca, met meerdere sessies tegelijk. Of praat met Jarvis en hij regelt het direct." "Het systeem doet het werk. De app laat je zien wat er gebeurt, en daar praat je ertegen." De app "werkt zichzelf bij".
- **Jarvis** (spraakassistent in de app): wakker maken met je stem; lange verhalen uitschrijven en terugpraten; op iPhone/Android "hij leest kort voor wat er openstaat en zet je klussen in gang"; "Zeg: zet een offerte klaar. Hij gaat aan de slag, jij doet iets anders. Later vraag je hoe ver hij is."; zelf naam, stem, man/vrouw en uiterlijk kiezen; 132 FAQ-vragen uit livesessies met videofragment; foutmeldingen via Jarvis direct naar Bart.
- **Week 7**: "Hoe ik op een ochtend vier projecten tegelijk afwerk" (parallelle sessies).
- **Week 8**: "Je systeem vanaf je telefoon. En alles dicht: wat je AI wel en niet mag."
- Nagebouwde abonnementen: eigen Calendly-kloon (boekingspagina die in je agenda kijkt, meetlink + bevestiging + herinnering), zeven "nagebouwde Adobe-apps" (FilmCraft, PhotoCraft …), "Software waar je elke maand voor betaalt, bouw je met je Mainframe zelf na."
- Eén opdracht → post tegelijk op Instagram, TikTok, YouTube en LinkedIn (via Blotato, `/shortsUpload`).

Over "Windows-spraakmeldingen zoals 'Claude is klaar'": niet letterlijk gevonden op de gelezen pagina's. Jarvis "praat terug"; de Windows-melding is in dit systeem een eigen bouw [EIGEN] (`scripts/zeg_klaar.ps1`).

Over **Modal / cronjobs in de cloud**: niet gevonden. Bart's openbare route voor "laptop dicht" is **Orca op een altijd-aan-computer**. Onze lokale variant [EIGEN] is Windows Taakplanner met "StartWhenAvailable" (draait zodra de laptop weer aan gaat) en optioneel "WakeToRun".

---

## 3. Het 8-weken curriculum [BRON + REVIEW]

| Week | Thema (hetmainframe.nl) | Uitwerking (reviewreus.nl) |
| --- | --- | --- |
| 0 | Setup-module (30 min) | werkomgeving klaar vóór les 1 |
| 1 | "Je downloadt Het Mainframe, zet je kennis erin via de app, en hij werkt direct voor je." | Claude Code installeren, bedrijfsinformatie inladen |
| 2 | "Een geheugen dat blijft, en een back-up van alles." | geheugen en herbruikbare skills |
| 3 | "Je koppelt je programma's. Veilig, en jij bepaalt wat." | Google Workspace (best) of Outlook koppelen |
| 4 | "Elke ochtend om 7 uur een overzicht in je mail. Ook met je laptop dicht." | eerste dagelijkse automatisering: ochtendbriefing |
| 5 | "Je zoekt de klussen die het meeste opleveren en zet ze om." | bottleneck-audit |
| 6 | "Elke klant een eigen plek. Plus je eigen dashboard, ook op je telefoon." | dashboard met klanten, deadlines, taken |
| 7 | "Hoe ik op een ochtend vier projecten tegelijk afwerk." | parallel werken |
| 8 | "Je systeem vanaf je telefoon. En alles dicht: wat je AI wel en niet mag." | beveiliging, meerdere apparaten, langetermijngeheugen |

Format: 1–3 uur per week, korte les + opdracht + livesessie; community op Circle; template-bibliotheek; Bart's eigen systeem als kopieerbaar startpunt [REVIEW].

### Hoe dit naar Webdesign Attila vertaald is [EIGEN]

| Week | Staat in jouw systeem als |
| --- | --- |
| 1 | `CLAUDE.md` ingevuld met bedrijf, doelgroep, prijzen, designregels |
| 2 | `docs/logs/` + `/einde` + git (lokale back-up; push alleen op jouw verzoek) |
| 3 | `mainframe_config.json` + scherm Verbindingen; MCP's in Claude Code |
| 4 | `scripts/dagstart.py` + `scripts/installeer_ochtendtaak.ps1` (07:00) |
| 5 | `/skill-maker` (zet een tijdvreter om in een skill) |
| 6 | `klanten/` + `/nieuw-klant` + Mainframe-app (scherm Overzicht + CRM) |
| 7 | Meerdere Claude Code-sessies in VS Code (zie 6.3) |
| 8 | Werkafspraken in `CLAUDE.md` §10 + `.gitignore` voor persoonsgegevens; app luistert alleen op 127.0.0.1 |

---

## 4. Gratis weggevers en openbare prompts

### 4.1 Overzicht van de gratis community-weggevers [BRON, bartboonstra.nl/linkinbio]

| Weggever | Kern |
| --- | --- |
| Hairline-skill | lijntekening die openklapt bij muisbeweging, bovenaan je website |
| Rekenspel | met Claude gebouwd voor zijn dochter (groep 2–4) |
| Calendly nagebouwd | eigen boekingspagina: kijkt in agenda, meetlink, bevestiging, herinnering ("kostte 120 euro per jaar") |
| Website zonder AI-look | "Laat Claude eerst afkijken bij echte ontwerpers op Dribbble" — prompts + skill |
| Skill checken | SkillSpector (NVIDIA): 70+ waarschuwingssignalen |
| Stop met agents bouwen | 6-stappen skill-bouwplan met alle prompts |
| Scrapling koppelen | gratis scraper, "wat wel en niet mag" |
| Animatiestudio | 6 stappen, Claude keurt zijn eigen animaties (met HyperFrames) |
| Skill "veilig-live" | Claude keurt je app op lekken vóór livegang |
| Gegevens van internet wissen | 4 prompts: opzoeken, AVG-verzoeken schrijven/invullen, wekelijks herhalen |
| Kortingscodes | 2 zinnen: Claude zoekt codes en test ze in je winkelmandje |
| Doorwerken met laptop dicht | Orca (zie 5.3) |
| 7 nagebouwde Adobe-apps | FilmCraft, PhotoCraft e.a. |
| Foto-commando's | 7 manieren om foto's te bewerken in ChatGPT |
| 20 power words | korte keywords met 40 Nederlandse voorbeelden |
| ASTRA-video | 4 ChatGPT-taken: boodschappen, afsprakenplanner, video editen, spullen verkopen |
| Thumbnail-skill | YouTube-thumbnails uit een map eigen foto's |
| AI-watermerk | tool die tekst laat herschrijven ("makers garanderen zelf niks") |
| 21 ChatGPT-commando's | woord + vraag = tekening i.p.v. alinea's |
| Tone of voice | interview-prompt → `tone-of-voice.md` (volledig openbaar, zie 4.2) |
| De AI Formule (live) | "vier stappen van losse chatjes naar een AI die echt voor je werkt" |
| Higgsfield koppelen | beeld en video vanuit Claude, 4 stappen |

### 4.2 Openbare prompt: tone-of-voice-interviewer [BRON, samengevat]

De volledige prompt staat op slimwerken.ai/landing/toneofvoice. Structuur: *"Je bent mijn schrijfstijl-interviewer. Aan het eind lever je een bestand op met de naam tone-of-voice.md [...] Werk zes stappen af [...] Stuur per stap EEN bericht en wacht op mijn antwoord."*
1. Vraag om materiaal (3 mails, 3 social posts, appjes/website; rommelig mag).
2. Vertel wat je ziet (max. 10 punten, met echte zinnen als bewijs, niets verzinnen).
3. Gaten-vragen (max. 6).
4. Spiegeltest (proefmail + proefpost van 5 zinnen; aanpassen tot het klopt).
5. Lever `tone-of-voice.md` op met 8 vaste onderdelen, waaronder de **nooit-lijst**.
6. Zeg hoe ik het voortaan gebruik.

De nooit-lijst ("verraders") [BRON]: "Eerlijk?" / "een scala aan" / "duiken in", "laten we hier even induiken" / "cruciaal", "essentieel" / "In een wereld waarin …" / "brengt uitdagingen met zich mee, maar biedt ook kansen" / "het is niet zomaar een X, het is een Y" / "Al met al", "Concluderend", "Kortom" / het lange streepje. Plus: *"schrijf nooit een zin op die ik zelf niet hardop zou zeggen."*

Vaste gebruiksprompts [BRON]:
```
Schrijf een mailtje aan [naam] over [onderwerp]. Volg mijn tone-of-voice.md, inclusief de nooit-lijst.
Herschrijf deze tekst in mijn stem volgens tone-of-voice.md. Laat de inhoud staan.
Leg deze tekst langs mijn nooit-lijst en zeg per zin wat eruit moet.
```
"De luie truc": Claude → Settings → Cowork → Global instructions: "gebruik altijd tone-of-voice.md".

In jouw systeem: skill `/tone-of-voice` (eigen herschrijving, toegespitst op Webdesign Attila).

### 4.3 Denkwijze en workflow-patronen [BRON]

- **"Schets je probleem en je ideale situatie, en AI doet de rest."** Niet zoeken naar de juiste tool of prompt.
- **Eén model kiezen en het echt leren kennen**: "Stop met switchen tussen Claude en ChatGPT. [...] Kies er één. Leer hem echt kennen. Train hem op jouw werk en projecten."
- **Eerst vragen, dan bouwen**: skills `/vragen` ("verduidelijkingsmodus") en de aanrader `/superpowers` ("Dwingt Claude om eerst na te denken, vragen te stellen en een plan te maken voordat hij gaat bouwen").
- **Corrigeer één keer, dan onthoudt hij het**: verbeteringen terugschrijven in het geheugen/de skill.
- **Mens keurt goed**: "Jij kijkt het na." / "Jij keurt goed, hij doet de rest." / Mailen, posten, verwijderen alleen na akkoord.
- **Alles droog laten draaien** bij koppelingen die iets veranderen (`/plugandpayExtra`).
- **Website zonder AI-look**: eerst echte voorbeelden laten bekijken (Dribbble, een site die je mooi vindt — `/websitecloner` stelt 8 merkvragen en neemt geen teksten/foto's over), elk scherm laten controleren voordat Claude "klaar" zegt (`/scrollsite`).
- **Skills controleren vóór installatie** (SkillSpector; 1 op 20 is kwaadaardig).
- **Data veilig**: `/anonimiseer` haalt persoonsgegevens lokaal uit documenten vóórdat ze naar AI gaan; `/avg-bible` voor de regels.

---

## 5. Concrete instructies en commando's

### 5.1 Benodigdheden [BRON]
"Visual Studio Code (gratis), de Claude Code extensie (ook gratis), en Claude Pro voor ongeveer €22 per maand. Dat is alles." (TikTok, "Maak een professionele website met Claude Code"). Bart zelf gebruikt een Max-abonnement.

### 5.2 Claude Code installeren op Windows [EIGEN, volgens de officiële Anthropic-documentatie]
1. Installeer **Git for Windows** (git-scm.com) — Claude Code gebruikt Git Bash op Windows.
2. Installeer Claude Code (PowerShell): `irm https://claude.ai/install.ps1 | iex` — controleer de actuele opdracht op code.claude.com/docs, want die kan wijzigen.
3. Installeer **VS Code** en daarin de extensie **Claude Code** (uitgever: Anthropic).
4. Open de map `C:\Webdesign_Attila` in VS Code (Bestand → Map openen).
5. Start Claude Code via het Claude-icoon of in de terminal met `claude`, en log in met je Claude-abonnement.
6. Typ `/` om je skills te zien (`/dagoverzicht`, `/offerte`, …).

### 5.3 Orca: doorwerken met de laptop dicht [BRON]
1. Een computer die altijd aanstaat (Mac mini of oude laptop aan de stroom); slaapstand uit; Orca open laten.
2. Claude Code (of Codex) moet daar al werken.
3. Download Orca op onorca.dev en installeer.
4. **Add Repo** → kies je werkmap → plusje → sessie met Claude Code.
5. Telefoon: Orca-app (App Store / onorca.dev) → op de computer via het accountmenu koppelen → code invullen bij **Pair**.
6. **Automations**: tijd kiezen, project kiezen, prompt erin.
7. Laptop als meekijker: Settings → Remote Orca Servers → New Link → Generate Access Link; op de laptop Add Server + link plakken. Beide computers in hetzelfde **Tailscale**-netwerk.

Voorbeeld-automation voor jou [EIGEN] (om 06:45 in Orca):
```
Voer /dagoverzicht uit en zet het resultaat in docs/dagstart/. Maak daarna voor elke lead met status "afspraak" zonder klantmap een klantmap met /nieuw-klant. Verstuur niets.
```

### 5.4 Overige openbare tips [BRON]
- `/nu` haalt de actuele datum/tijd op (Amsterdam) "als de sessiedatum niet klopt".
- `/transcribeer [kanaal-URL] --bouw-skill`: laatste 20 video's van een YouTube-kanaal als tekst + een expert-skill ("Kloon elke YouTube-expert in 5 minuten met Claude").
- Higgsfield koppelen: "vier stappen, geen terminal, geen installatie".

---

## 6. Over "NOOIT Claude gebruiken in de app" en "Het nieuwe werken met AI"

De video's met deze exacte titels kon ik niet vinden of lezen. Wat Bart over dit onderwerp wél openbaar zegt [BRON]:
- In de Claude-**app** werk je met losse chats: "Je kopieert. Je plakt. Je verbetert. Je legt alles opnieuw uit." 91% van 200+ mensen in zijn livesessie kreeg van AI deze week geen vrije middag.
- In **Claude Code** (VS Code of Orca) staat je kennis in mappen op je eigen computer, dus "nooit meer je bedrijf opnieuw uitleggen".
- Tussenvorm: **Cowork** in de Claude-desktopapp (betaald account) mag in een aangewezen map lezen en schrijven; "Kies je geen Cowork, dan praat je met de gewone chat en blijft je computer dicht." "Het verschil. In de gratis chat plak jij. In Cowork staat het in je map en pakt hij het er zelf bij."
- Zijn eigen vergelijking (hetmainframe.nl): typische AI-cursus = video's kijken, kennis, in hun tool; Het Mainframe = elke week bouwen, een werkend systeem, op je eigen computer.

Conclusie voor jou [EIGEN]: werk dagelijks in **Claude Code in VS Code, gestart in `C:\Webdesign_Attila`**, niet in de chat-app. Alleen dan leest Claude `CLAUDE.md`, je skills, klantmappen en logs automatisch.

### Meerdere sessies tegelijk (week 7) [EIGEN]
In VS Code kun je meerdere Claude Code-tabbladen openen. Werk per tabblad aan één klant (bijv. tab 1: `/website-bouwer` voor klant A; tab 2: `/offerte` voor klant B). Laat ze nooit tegelijk hetzelfde bestand bewerken.

---

## 7. Vertaling naar de Webdesign Attila Mainframe (wat er gebouwd is)

| Onderdeel | Bestand(en) | Pijler |
| --- | --- | --- |
| Centraal brein | `CLAUDE.md` | Verstand |
| Klantgeheugen per klant | `klanten/_sjabloon/` → `klanten/[slug]/` | Verstand |
| Sessiegeheugen | `docs/logs/` | Verstand |
| Skills | `.claude/skills/` — dagoverzicht, nieuw-klant, website-bouwer, offerte, einde, skill-maker, structuur, tone-of-voice | Vaardigheden |
| Mainframe 2.0 web-app | `mainframe_app.html` + `start_mainframe.py` (+ `start_mainframe.bat`) | alle vier |
| Scherm 1 Overzicht & Dagstart | KPI's uit `echte_leads.csv`/`verzonden.txt`, startknoppen scripts, klantprojecten, nieuwe klant | Vanzelf |
| Scherm 2 Lead & Bel-CRM | Bel / WhatsApp (wa.me + persoonlijk bericht) / E-mail / Website, 4 statussen, notities → `leads_status.json` | Verbindingen |
| Scherm 3 Skills & Prompts | kaarten met 1-klik kopiëren | Vaardigheden |
| Scherm 4 Verbindingen | statusbadges + links uit `mainframe_config.json` | Verbindingen |
| Ochtendbriefing 07:00 | `scripts/dagstart.py` + `scripts/installeer_ochtendtaak.ps1` | Vanzelf |
| Spraakmelding | `scripts/zeg_klaar.ps1` ("Attila, Claude is klaar!") | Vanzelf |

### 7.1 Ideeën voor later (bewezen in de openbare bronnen) [EIGEN prioritering]
1. **`/tone-of-voice` draaien** — 10 minuten, maakt alle offertes en mails direct beter.
2. **Website-check-skill** voor klanten in onderhoud (prijzen, links, mobiel, snelheid, SEO) — vergelijkbaar met `/websitecheck`; ideaal als onderdeel van het onderhoudsabonnement "Groei".
3. **Website-cloner-flow** voor demo's: site die de klant mooi vindt → 8 merkvragen → bouwprompt (nooit teksten of foto's overnemen).
4. **Moneybird-koppeling** (als je Moneybird gebruikt): facturen als concept na livegang.
5. **Orca op een altijd-aan-pc** als je wilt dat Claude zelf ('s nachts) demo's voorbereidt.
6. **Eigen Calendly-kloon** op webdesignattila.nl voor demo-afspraken.
7. **`/anonimiseer`-principe**: haal persoonsgegevens uit leadlijsten voordat je ze aan externe AI-diensten geeft.

---

## 8. Bronnen

- Het Mainframe — https://hetmainframe.nl/
- Mainframe VIP — https://hetmainframe.nl/vip/
- Mainframe Enterprise — https://hetmainframe.nl/hetmainframe/enterprise/
- Bart Boonstra — https://www.bartboonstra.nl/
- Link in bio (weggevers) — https://www.bartboonstra.nl/linkinbio
- Shop — https://www.bartboonstra.nl/shop en https://slimwerken.ai/shop
- Slim Werken AI — https://slimwerken.ai/
- Mainframe skill-index — https://slimwerken.ai/landing/skills/
- Orca-gids — https://slimwerken.ai/landing/orca/
- Tone-of-voice-gids — https://slimwerken.ai/landing/toneofvoice/
- YouTube-kanaal — https://www.youtube.com/@BartBoonstra_slimwerken
- Review Het Mainframe — https://reviewreus.nl/het-mainframe-review/
- Review Slim Werken met AI — https://reviewreus.nl/slim-werken-met-ai-review/
- Profiel Bart Boonstra — https://reviewreus.nl/bart-boonstra/
- Orca — https://onorca.dev
- Novamira (WordPress-MCP) — https://novamira.ai/docs/getting-started
