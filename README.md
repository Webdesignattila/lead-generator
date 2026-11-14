# Webdesign Attila Mainframe 2.0

Je eigen, gratis AI-werksysteem: één map op je computer met het brein (`CLAUDE.md`), je klanten, je skills, je scripts en een lokale web-app op **http://localhost:8080**.
Achtergrond en onderzoek: [`docs/MAINFRAME_BLAUWDRUK.md`](docs/MAINFRAME_BLAUWDRUK.md).

## 1. Eenmalig installeren in `C:\Webdesign_Attila`

Je bestaande bestanden (`echte_scraper.py`, `mijnhost_jager.py`, `whatsapp_jager.py`, `echte_leads.csv`, `verzonden.txt`) blijven staan. De opdracht hieronder kopieert alleen bestanden die nog **niet** bestaan en overschrijft niets.

Open **PowerShell** en voer uit:

```powershell
git clone -b claude/wonderful-mendel-sl8wyx https://github.com/Webdesignattila/lead-generator.git C:\Temp\attila-mainframe
robocopy C:\Temp\attila-mainframe C:\Webdesign_Attila /E /XC /XN /XO /XD .git
```

Daarna in dezelfde PowerShell (eenmalig, optioneel maar aangeraden):

```powershell
cd C:\Webdesign_Attila
powershell -ExecutionPolicy Bypass -File scripts\zeg_klaar.ps1                       # test de stem
powershell -ExecutionPolicy Bypass -File scripts\installeer_ochtendtaak.ps1 -MainframeBijInloggen
```

De tweede regel zet de **dagstart om 07:00** in Windows Taakplanner en start de Mainframe-server automatisch bij inloggen.
Hoor je een Engelse stem? Instellingen → Tijd en taal → Spraak → Stem toevoegen → Nederlands.

Benodigd: Python 3.10+ (python.org, vink "Add to PATH" aan), VS Code met de extensie **Claude Code**, en een Claude-abonnement.

## 2. Elke dag

| Moment | Wat je doet |
| --- | --- |
| **07:00 (vanzelf)** | De briefing staat in `docs\dagstart\JJJJ-MM-DD.md` en Windows zegt hoeveel terugbellers, afspraken en projecten je hebt. |
| **Start werkdag** | Dubbelklik `start_mainframe.bat` (of hij draait al) → **http://localhost:8080**. |
| **Bellen** | Scherm *Lead & Bel-CRM*: filter op "Nieuw" of "Nog niet gemaild", klik **Bel** / **WhatsApp** / **E-mail**, zet de status en typ je notitie (wordt direct opgeslagen). |
| **Met Claude werken** | Open de map in VS Code → Claude Code → typ `/dagoverzicht`. |
| **Lead wil een demo** | Status "Afspraak / Demo maken" → in Claude: `/nieuw-klant Bedrijfsnaam` → `/website-bouwer` → `/offerte`. |
| **Einde werkdag** | In Claude: `/einde` (log, brein en klantgeheugen bijgewerkt, spraakmelding). |
| **Iets herhaalt zich** | `/skill-maker` → binnen een paar minuten een nieuwe skill. Hij verschijnt vanzelf in de app. |

## 3. De vier schermen

1. **Overzicht & Dagstart** — leads in `echte_leads.csv`, mails in `verzonden.txt`, terugbellers, afspraken, open projecten, startknoppen voor je scripts, nieuwe klantmap aanmaken.
2. **Lead & Bel-CRM** — al je gescrapete bedrijven met Bel, WhatsApp (`wa.me` met persoonlijk bericht), E-mail en Website; statussen *Geen gehoor*, *Terugbellen*, *Afspraak / Demo maken*, *Niet interessant*; notities in `leads_status.json`.
3. **Skills & Prompts** — alle skills uit `.claude\skills\` met een kopieerknop, plus vaste prompts.
4. **Verbindingen** — Claude Code, Python, je scraper, Mijn.host, Google Ads, Novamira, Higgsfield, VS Code met status en links.

Teksten van het WhatsApp-bericht en de mail, de scripts achter de startknoppen en de links pas je aan in `mainframe_config.json`.
Leest het CRM een kolom niet goed? Bovenaan het CRM staat welke CSV-kolommen herkend zijn; de herkenning staat in `start_mainframe.py` (`KOLOMMEN`).

## 4. Eerst nog invullen

In `CLAUDE.md`: alles met **NOG INVULLEN**, **VOORSTEL** of **NOG BEVESTIGEN** (telefoon, KvK, pakketinhoud, onderhoudsprijzen, btw, betaaltermijn). `/offerte` weigert onbevestigde bedragen te gebruiken.
Laat daarna Claude je eigen scripts beschrijven met `/structuur volledig`, en maak je schrijfstijl met `/tone-of-voice`.

## 5. Privacy

`echte_leads.csv`, `verzonden.txt`, `leads_status.json` en alle andere `.csv`-bestanden staan in `.gitignore` en gaan nooit naar GitHub. De app luistert alleen op je eigen computer (127.0.0.1) en start alleen scripts die in `mainframe_config.json` staan.
