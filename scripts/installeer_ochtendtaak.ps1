<#
  installeer_ochtendtaak.ps1 - pijler "Vanzelf"

  Zet in Windows Taakplanner een taak die elke ochtend om 07:00 de dagstart-briefing maakt
  (docs\dagstart\JJJJ-MM-DD.md) en hem hardop samenvat.
  Stond de laptop om 07:00 uit of dicht? Dan draait de taak zodra hij weer aan staat.

  Gebruik (in PowerShell, vanuit de Mainframe-map):
    powershell -ExecutionPolicy Bypass -File scripts\installeer_ochtendtaak.ps1
    powershell -ExecutionPolicy Bypass -File scripts\installeer_ochtendtaak.ps1 -Tijd 06:30
    powershell -ExecutionPolicy Bypass -File scripts\installeer_ochtendtaak.ps1 -MainframeBijInloggen
    powershell -ExecutionPolicy Bypass -File scripts\installeer_ochtendtaak.ps1 -Verwijder
#>
param(
    [string]$Tijd = "07:00",
    [switch]$MainframeBijInloggen,
    [switch]$Verwijder
)

$ErrorActionPreference = "Stop"
$basis = Split-Path -Parent $PSScriptRoot
$taakDagstart = "Attila Mainframe - Dagstart"
$taakServer = "Attila Mainframe - Server"

if ($Verwijder) {
    foreach ($t in @($taakDagstart, $taakServer)) {
        if (Get-ScheduledTask -TaskName $t -ErrorAction SilentlyContinue) {
            Unregister-ScheduledTask -TaskName $t -Confirm:$false
            Write-Host "Verwijderd: $t"
        }
    }
    return
}

# Python zoeken (geen Microsoft Store-snelkoppeling).
$python = $null
foreach ($naam in @("python", "py")) {
    $cmd = Get-Command $naam -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notmatch "WindowsApps") { $python = $cmd.Source; break }
}
if (-not $python) { throw "Python niet gevonden. Installeer Python via python.org en vink 'Add to PATH' aan." }
$pythonw = Join-Path (Split-Path $python) "pythonw.exe"
if (-not (Test-Path $pythonw)) { $pythonw = $python }

$instellingen = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun

$actie = New-ScheduledTaskAction -Execute $pythonw `
    -Argument "`"$basis\scripts\dagstart.py`" --spreek --stil" -WorkingDirectory $basis
$trigger = New-ScheduledTaskTrigger -Daily -At $Tijd
Register-ScheduledTask -TaskName $taakDagstart -Action $actie -Trigger $trigger -Settings $instellingen `
    -Description "Maakt elke ochtend de dagstart-briefing van de Webdesign Attila Mainframe." -Force | Out-Null
Write-Host "Ingesteld: '$taakDagstart' elke dag om $Tijd."

if ($MainframeBijInloggen) {
    $actie2 = New-ScheduledTaskAction -Execute $pythonw `
        -Argument "`"$basis\start_mainframe.py`" --geen-browser" -WorkingDirectory $basis
    $trigger2 = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
    Register-ScheduledTask -TaskName $taakServer -Action $actie2 -Trigger $trigger2 -Settings $instellingen `
        -Description "Start de Mainframe-server op http://localhost:8080 bij inloggen." -Force | Out-Null
    Write-Host "Ingesteld: '$taakServer' start bij inloggen (http://localhost:8080)."
}

Write-Host "Test nu direct: Start-ScheduledTask -TaskName '$taakDagstart'"
