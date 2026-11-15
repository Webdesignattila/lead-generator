# Speelt een gesproken melding af zodra de render klaar is (Windows, ingebouwde spraak).
param([string]$Tekst = "De promo video van Webdesign Attila is klaar.")
try {
    Add-Type -AssemblyName System.Speech
    $stem = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $nl = $stem.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -like "nl*" } | Select-Object -First 1
    if ($nl) { $stem.SelectVoice($nl.VoiceInfo.Name) }
    $stem.Speak($Tekst)
} catch {
    [System.Media.SystemSounds]::Asterisk.Play()
    Write-Host $Tekst
}
