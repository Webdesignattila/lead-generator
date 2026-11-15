# Volledige build op Windows: voice-over genereren, MP4 renderen, daarna melding afspelen.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
python scripts\genereer_voiceover.py
if ($LASTEXITCODE -ne 0) { throw "Voice-over genereren mislukt" }
npx remotion render PromoVideo out\webdesign_attila_promo.mp4
if ($LASTEXITCODE -ne 0) { throw "Renderen mislukt" }
& "$PSScriptRoot\zeg_klaar.ps1"
