# scripts/ — de "Vanzelf"-pijler

| Script | Wat | Starten |
| --- | --- | --- |
| `dagstart.py` | Ochtendbriefing → `docs/dagstart/JJJJ-MM-DD.md` (leads, terugbellers, afspraken, projecten, volgende stap) | `python scripts/dagstart.py` · hardop: `--spreek` |
| `nieuw_klant.py` | Klantmap uit `klanten/_sjabloon/` | `python scripts/nieuw_klant.py "Bedrijfsnaam" --plaats Zwolle --pakket Groei` |
| `zeg_klaar.ps1` | Spraakmelding "Attila, Claude is klaar!" (Nederlandse Windows-stem) | `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\zeg_klaar.ps1` |
| `installeer_ochtendtaak.ps1` | Zet `dagstart.py` elke dag om 07:00 in Windows Taakplanner (`-MainframeBijInloggen` start ook de app bij inloggen; `-Verwijder` haalt alles weg) | `powershell -ExecutionPolicy Bypass -File scripts\installeer_ochtendtaak.ps1` |

## Je eigen automatiseringen (in de hoofdmap)

Deze blijven op hun vaste plek staan, zodat bestaande paden blijven werken. De Mainframe-app start ze via
de knoppen op het Overzicht (instelbaar in `mainframe_config.json` → `scripts`).

| Script | Schrijft naar |
| --- | --- |
| `echte_scraper.py` | `echte_leads.csv` |
| `mijnhost_jager.py` | zie het script (laat `/structuur volledig` dit beschrijven) |
| `whatsapp_jager.py` | zie het script (laat `/structuur volledig` dit beschrijven) |
| `generator.py` | FastAPI-aanvraagformulier → AI-conceptsite (Groq) + Telegram-melding |

Een nieuw script toevoegen aan de startknoppen: voeg in `mainframe_config.json` onder `scripts` toe:

```json
{ "sleutel": "uniek", "label": "Naam op de knop", "bestand": "mijn_script.py", "uitleg": "Wat het doet." }
```
