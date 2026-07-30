# ==============================================================================
# Afterburner: Windows Workspace Engine & CorelDRAW Patch Deployer
# Targets: Inkscape (CorelDRAW Profile) across Windows %APPDATA%\inkscape
# ==============================================================================

$ErrorActionPreference = "Stop"

Clear-Host

Write-Host "  █████╗ ███████╗████████╗███████╗██████╗ ██████╗ ██╗   ██╗██████╗ ███╗   ██╗███████╗██████╗ " -ForegroundColor Red
Write-Host " ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝██╔══██╗" -ForegroundColor Red
Write-Host " ███████║█████╗     ██║   █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝██╔██╗ ██║█████╗  ██████╔╝" -ForegroundColor Red
Write-Host " ██╔══██║██╔══╝     ██║   ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗██║╚██╗██║██╔══╝  ██╔══██╗" -ForegroundColor Red
Write-Host " ██║  ██║██║        ██║   ███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║██║ ╚████║███████╗██║  ██║" -ForegroundColor Red
Write-Host " ╚═╝  ╚═╝╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝" -ForegroundColor Red
Write-Host ""
Write-Host "  🔥 CorelDRAW to Inkscape Workspace Engine | v2.1 Release" -ForegroundColor DarkYellow
Write-Host "  ─────────────────────────────────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host ""

$PayloadDir = Join-Path -Path $PSScriptRoot -ChildPath "config-payload\inkscape"

if (-not (Test-Path -Path $PayloadDir)) {
    Write-Host "  ✖ [ ERROR ] Payload directory '$PayloadDir' not found." -ForegroundColor Red
    Write-Host "  ✖ [ ERROR ] Please run this script from the root of the Afterburner folder." -ForegroundColor Red
    Write-Host ""
    exit 1
}

$InkscapeUserConfig = Join-Path -Path $env:APPDATA -ChildPath "inkscape"
$KeysTarget = Join-Path -Path $InkscapeUserConfig -ChildPath "keys"
$PalettesTarget = Join-Path -Path $InkscapeUserConfig -ChildPath "palettes"
$ExtensionsTarget = Join-Path -Path $InkscapeUserConfig -ChildPath "extensions"

Write-Host "  ℹ [ INFO ]  Scanning active Windows environment for Inkscape profile..." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path -Path $InkscapeUserConfig)) {
    Write-Host "  ⚠ [ WARN ]  Inkscape profile directory not found. Initializing: $InkscapeUserConfig" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $InkscapeUserConfig -Force | Out-Null
}

Write-Host "  🔥 [ PATCH ] Target Inkscape profile: $InkscapeUserConfig" -ForegroundColor DarkYellow

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

Write-Host "  ✔ [ SUCCESS ] Injected CorelDRAW shortcuts, palettes & extensions." -ForegroundColor Green
Write-Host ""
Write-Host "  ─────────────────────────────────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host "  🚀 [ COMPLETE ] Afterburner v2.1 injected successfully!" -ForegroundColor Green
Write-Host "  👉 Restart Inkscape to activate your CorelDRAW workspace & extensions." -ForegroundColor DarkYellow
Write-Host "  ─────────────────────────────────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host ""
