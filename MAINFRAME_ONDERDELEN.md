# Mainframe: de 4 laatste onderdelen

Kopieer deze bestanden naar `C:\Webdesign_Attila` (zelfde mappenstructuur) en draai één keer:

```powershell
cd C:\Webdesign_Attila
pip install fastapi uvicorn
python scripts\koppel_lead_filter.py                 # filter in echte_scraper.py + mijnhost_jager.py
python scripts\lead_filter.py schoon echte_leads.csv  # eerst backup echte_leads_backup.csv, dan opschonen
python scripts\wachtrij_dashboard.py                  # http://localhost:8080
```

| Onderdeel | Bestanden | Gebruik |
|---|---|---|
| 1. YouTube-expert | `.claude/skills/youtube-expert/SKILL.md`, `experts/pavlo.md`, `experts/bart-boonstra.md` | `/youtube-expert <kanaal>` · "Vraag het aan Pavlo" · "Laat Bart Boonstra dit aanpakken" |
| 2. Luxe webdesign | `.claude/skills/website-bouwer/SKILL.md` → `.claude/skills/design-taste-frontend/` | `/website-bouwer demos/<lead>` |
| 3. Nacht-wachtrij | `wachtrij.json`, `scripts/nacht_worker.py`, `scripts/wachtrij_dashboard.py` | knop op localhost:8080, of `python scripts\nacht_worker.py` |
| 4. Ketens-filter | `scripts/lead_filter.py`, `scripts/koppel_lead_filter.py` | automatisch in beide scrapers; test: `python scripts\lead_filter.py test "Toyota Louwman"` |

## Wachtrij
- Taaktypes: `leads_opschonen`, `demo_voorbereiden`, `mailronde`, `commando` (elk script, bijv.
  `{"cmd": "python echte_scraper.py"}`), `wacht`.
- De mailronde staat standaard op `"droog": true` (er gaat niets de deur uit). Voor echt versturen:
  zet `"droog": false` en de omgevingsvariabelen `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`,
  `MAIL_AFZENDER`. Nooit dubbel mailen (`mail_verzonden.csv`), max per ronde, willekeurige pauzes,
  alleen tussen 08:00 en 20:00, afmeldregel en `List-Unsubscribe`-header.
- Logboek: `logs\nacht_worker.log`. Aan het einde speelt `scripts\zeg_klaar.ps1`.

## Bestaand dashboard op 8080?
Draait er al een eigen FastAPI-dashboard op 8080, start `wachtrij_dashboard.py` dan niet los,
maar voeg dit toe aan dat dashboard:
```python
from scripts.wachtrij_dashboard import router as wachtrij_router, WACHTRIJ_BLOK_HTML
app.include_router(wachtrij_router)
# en zet {WACHTRIJ_BLOK_HTML} in de HTML van de dashboardpagina
```
