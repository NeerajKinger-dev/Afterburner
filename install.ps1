# ==============================================================================
# Afterburner: Windows Workspace Engine
# Targets: Inkscape (CorelDRAW Profile)
# Handles: Windows %APPDATA%\inkscape Configuration Deployment
# ==============================================================================

$ErrorActionPreference = "Stop"

function Write-Host-Color ($Text, $Color) {
    Write-Host $Text -ForegroundColor $Color
}

Write-Host-Color "====================================================" "Cyan"
Write-Host-Color "      Afterburner: Windows Workspace Engine        " "Yellow"
Write-Host-Color "====================================================" "Cyan"

$PayloadDir = Join-Path -Path $PSScriptRoot -ChildPath "config-payload\inkscape"

if (-not (Test-Path -Path $PayloadDir)) {
    Write-Host-Color "[ERROR] Payload directory '$PayloadDir' not found." "Red"
    Write-Host-Color "[ERROR] Please run this script from the root of the Afterburner folder." "Red"
    exit 1
}

$InkscapeUserConfig = Join-Path -Path $env:APPDATA -ChildPath "inkscape"
$KeysTarget = Join-Path -Path $InkscapeUserConfig -ChildPath "keys"
$PalettesTarget = Join-Path -Path $InkscapeUserConfig -ChildPath "palettes"
$ExtensionsTarget = Join-Path -Path $InkscapeUserConfig -ChildPath "extensions"

Write-Host-Color "[INFO] Scanning for Inkscape user profile at: $InkscapeUserConfig" "Cyan"

if (-not (Test-Path -Path $InkscapeUserConfig)) {
    Write-Host-Color "[INFO] Inkscape profile directory not found. Creating $InkscapeUserConfig" "Yellow"
    New-Item -ItemType Directory -Path $InkscapeUserConfig -Force | Out-Null
}

New-Item -ItemType Directory -Path $KeysTarget -Force | Out-Null
New-Item -ItemType Directory -Path $PalettesTarget -Force | Out-Null
New-Item -ItemType Directory -Path $ExtensionsTarget -Force | Out-Null

$SourceKeys = Join-Path -Path $PayloadDir -ChildPath "keys\*"
$SourcePalettes = Join-Path -Path $PayloadDir -ChildPath "palettes\*"
$SourceExtensions = Join-Path -Path $PayloadDir -ChildPath "extensions\*"

if (Test-Path -Path (Join-Path -Path $PayloadDir -ChildPath "keys")) {
    Copy-Item -Path $SourceKeys -Destination $KeysTarget -Recurse -Force
}

if (Test-Path -Path (Join-Path -Path $PayloadDir -ChildPath "palettes")) {
    Copy-Item -Path $SourcePalettes -Destination $PalettesTarget -Recurse -Force
}

if (Test-Path -Path (Join-Path -Path $PayloadDir -ChildPath "extensions")) {
    Copy-Item -Path $SourceExtensions -Destination $ExtensionsTarget -Recurse -Force
}

Write-Host-Color "[SUCCESS] Successfully deployed Afterburner v2.0 profile & extensions to $InkscapeUserConfig" "Green"
Write-Host-Color "====================================================" "Cyan"
Write-Host-Color "[SUCCESS] Afterburner payload injected! Restart Inkscape to initialize." "Green"
Write-Host-Color "====================================================" "Cyan"
