# zeg_klaar.ps1 - spreekt een melding uit als het Mainframe klaar is.
# Gebruik: powershell -ExecutionPolicy Bypass -File scripts\zeg_klaar.ps1 ["eigen tekst"]
param([string]$Tekst = "Attila, je Mainframe is klaar. Alle taken zijn uitgevoerd.")

try {
    Add-Type -AssemblyName System.Speech
    $stem = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $nl = $stem.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -like "nl-*" } | Select-Object -First 1
    if ($nl) { $stem.SelectVoice($nl.VoiceInfo.Name) }
    $stem.Volume = 100
    $stem.Speak($Tekst)
    $stem.Dispose()
} catch {
    [System.Media.SystemSounds]::Asterisk.Play()
    Write-Output $Tekst
}
