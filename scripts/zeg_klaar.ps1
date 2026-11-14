<#
  zeg_klaar.ps1 - spraakmelding met de ingebouwde Windows-stem.

  Gebruik:
    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\zeg_klaar.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\zeg_klaar.ps1 -Tekst "Attila, de offerte staat klaar"

  Kiest automatisch een Nederlandse stem (nl-NL) als die geinstalleerd is.
  Geen Nederlandse stem? Instellingen > Tijd en taal > Spraak > Stemmen beheren > Stem toevoegen > Nederlands.
#>
param(
    [string]$Tekst = "Attila, Claude is klaar!"
)

try {
    Add-Type -AssemblyName System.Speech
    $stem = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $nederlands = $stem.GetInstalledVoices() |
        Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name -eq 'nl-NL' } |
        Select-Object -First 1
    if ($nederlands) {
        $stem.SelectVoice($nederlands.VoiceInfo.Name)
    } else {
        Write-Warning "Geen Nederlandse stem gevonden; de standaardstem wordt gebruikt."
    }
    $stem.Volume = 100
    $stem.Rate = 0
    $stem.Speak($Tekst)
    $stem.Dispose()
} catch {
    # Valt terug op een systeemgeluid als spraak niet beschikbaar is.
    [System.Media.SystemSounds]::Asterisk.Play()
    Write-Warning "Spraak niet beschikbaar: $($_.Exception.Message)"
}
