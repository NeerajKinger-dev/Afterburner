<p align="center">
  <img src="assets/logo.png" alt="Afterburner Logo" width="280">
</p>

# Afterburner 
> Frictionless workspace migration patches for creative professionals running on Linux & Windows.

Afterburner instantly overhauls Inkscape to match classic industry UI layouts and keyboard hotkey profiles. It eliminates muscle-memory breakdown and formatting friction, dramatically lowering the barrier to switching or migrating your graphic production environment.

## Roadmap & Implementation

### Phase 1: Core Layout Core (Current)
*   [x] Automated path-detection installer framework (`install.sh` for Linux & `install.ps1` for Windows)
*   [x] CorelDRAW industry-standard keyboard shortcut profiles
*   [x] CorelDRAW classic palette swatch strip integration (`CorelDRAW.gpl`)
*   [x] Single-column tool hierarchies and docker panel alignment

## Key Features Deployed
*   **CorelDRAW Keymappings:** Rebinds your workflow instantly (`Spacebar` to pick objects, `F10` for node shaping, `F5` for freehand drawing, and `F6`/`F7` for primitives).
*   **Right-Side Docker Panels:** Forces properties, layers, object managers, and color modifications to lock cleanly to the right-side layout margins.
*   **The Classic Color Swatch Strip:** Drops the standard `CorelDRAW.gpl` layout palette into the bottom tray for immediate hex-validated color choices.

## Installation

### 🐧 Linux (Ubuntu / Debian / Flatpak / Snap / Native)
Open your terminal inside the `Afterburner` directory:
```bash
chmod +x install.sh
./install.sh
```

### 🪟 Windows (Inkscape 1.x+)
Open PowerShell inside the `Afterburner` directory:
```powershell
.\install.ps1
```
*(If PowerShell script execution is restricted, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before running).*



