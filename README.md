<p align="center">
  <img src="assets/logo.png" alt="Afterburner Logo - Ultimate Free CorelDRAW Alternative with Corel Shortcuts" width="280">
</p>

<h1 align="center">Afterburner 🚀</h1>

<p align="center">
  <b>The Drop-In Bridge Turning Inkscape into the Ultimate Free CorelDRAW Alternative</b>
</p>

<p align="center">
  <a href="https://github.com/NeerajKinger-dev/Afterburner/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-brightgreen.svg" alt="Platform: Linux | macOS | Windows">
  <img src="https://img.shields.io/badge/Inkscape-1.0%2B-orange.svg" alt="Inkscape 1.0+ Supported">
  <img src="https://img.shields.io/badge/CorelDRAW-Shortcuts-red.svg" alt="CorelDRAW Shortcuts">
</p>

---

## 📌 The Best Free Open Source CorelDRAW Alternative with Corel Shortcuts

Looking for **free vector software that feels like CorelDRAW** without breaking your workflow or muscle memory? 

**Afterburner** is an automated workspace engine that instantly transforms **Inkscape** into the ultimate **free open source CorelDRAW alternative**. By injecting native CorelDRAW keymappings, right-hand docker panel alignment, and the iconic `CorelDRAW.gpl` color swatch strip, Afterburner provides a zero-learning-curve transition for vector designers, illustrators, and print shops migrating to open-source software on **Linux**, **macOS**, and **Windows**.

---

## 📑 Table of Contents
- [Why Inkscape + Afterburner is the Ultimate Free CorelDRAW Alternative](#-why-inkscape--afterburner-is-the-ultimate-free-coreldraw-alternative)
- [Key Features](#-key-features)
- [CorelDRAW vs Inkscape Keybinding Comparison](#-coreldraw-vs-inkscape-keybinding-comparison)
- [How to Make Inkscape Work Like CorelDRAW for Free](#-how-to-make-inkscape-work-like-coreldraw-for-free)
- [Roadmap & Status](#-roadmap--implementation)
- [Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [License](#-license)

---

## 💡 Why Inkscape + Afterburner is the Ultimate Free CorelDRAW Alternative

Inkscape is the leading free, open-source vector graphics editor, but transitioning from CorelDRAW to Inkscape usually causes severe muscle-memory friction. **Afterburner acts as the drop-in bridge** to eliminate that barrier:

1. **Zero Muscle-Memory Breakage**: Keep using `Spacebar` for Pick tool, `F10` for Node editing, and `F5` for Freehand drawing.
2. **Native Docker Layouts**: Lock Object Properties, Layers, and Fill/Stroke dialogs directly to the right-side margin, mirroring CorelDRAW's classic workspace layout.
3. **Hex-Validated Color Swatches**: Enjoy immediate access to the classic CorelDRAW color palette directly in Inkscape's bottom tray.
4. **Cross-Platform & 100% Free**: Deploy effortlessly across Ubuntu/Debian, macOS, and Windows 10/11.

---

## ⚡ Key Features

* 🎯 **CorelDRAW Keyboard Shortcuts**: Instantly rebinds navigation, selection, and shape tools to classic CorelDRAW hotkeys.
* 🎨 **Classic CorelDRAW Palette Integration**: Installs the native `CorelDRAW.gpl` swatch strip into Inkscape's palette bar.
* 📐 **Right-Side Docker Panels**: Aligns layers, object properties, and fill/stroke controls into clean right-side dockers.
* 🤖 **Automated Multi-Platform Installer**: Auto-detects Inkscape installations across Linux (APT, Snap, Flatpak), macOS, and Windows.

---

## ⌨️ CorelDRAW vs Inkscape Keybinding Comparison

| Action / Tool | CorelDRAW Shortcut | Default Inkscape | Afterburner Remap |
| :--- | :--- | :--- | :--- |
| **Pick / Selection Tool** | `Spacebar` | `S` or `F1` | `Spacebar` |
| **Shape / Node Tool** | `F10` | `N` or `F2` | `F10` |
| **Freehand / Curve Tool** | `F5` | `P` or `F4` | `F5` |
| **Rectangle Tool** | `F6` | `R` or `F4` | `F6` |
| **Ellipse / Circle Tool** | `F7` | `E` or `F5` | `F7` |
| **Zoom In / Out** | `F2` / `F3` | `+` / `-` | `F2` / `F3` |
| **Group / Ungroup** | `Ctrl + G` / `Ctrl + U` | `Ctrl + G` / `Ctrl + Shift + G` | `Ctrl + G` / `Ctrl + U` |

---

## 💻 How to Make Inkscape Work Like CorelDRAW for Free

Follow these simple steps to transform Inkscape into a free vector software that feels like CorelDRAW:

### 🐧 Linux (Ubuntu / Debian / Flatpak / Snap / Native)
Open your terminal inside the cloned `Afterburner` directory:
```bash
chmod +x install.sh
./install.sh
```

### 🍎 macOS Installation
Open your Terminal inside the cloned repository directory and run:
```bash
chmod +x install.sh && ./install.sh
```

### 🪟 Windows (Inkscape 1.x+)
Open PowerShell inside the `Afterburner` directory:
```powershell
.\install.ps1
```
*(If PowerShell script execution is restricted, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before running).*

---

## 🚀 Roadmap & Implementation

### Phase 1: Core Layout Core (Current)
* [x] Automated path-detection installer framework (`install.sh` for Linux/macOS & `install.ps1` for Windows)
* [x] CorelDRAW industry-standard keyboard shortcut profiles
* [x] CorelDRAW classic palette swatch strip integration (`CorelDRAW.gpl`)
* [x] Single-column tool hierarchies and docker panel alignment

---

## ❓ Frequently Asked Questions (FAQ)

### What is the best free open source CorelDRAW alternative with Corel shortcuts?
**Inkscape combined with Afterburner** is the best free open source CorelDRAW alternative. Afterburner automatically configures Inkscape with authentic CorelDRAW keyboard shortcuts, right-side docker panels, and CorelDRAW color swatches.

### How do I find free vector software that feels like CorelDRAW?
Download Inkscape (free & open source) and install Afterburner. Afterburner modifies Inkscape's user profile so that tools, keybindings (such as `Spacebar` for Pick tool and `F10` for Node tool), and layouts behave exactly like CorelDRAW.

### How to make Inkscape work like CorelDRAW for free?
Run Afterburner's automated installer script (`install.sh` for Linux/macOS or `install.ps1` for Windows). The script auto-detects your Inkscape installation path and applies the CorelDRAW profile patch instantly.

### Will Afterburner delete my custom vector files or existing artwork?
No. Afterburner only updates configuration XML keymaps (`default.xml`) and palette swatch files (`CorelDRAW.gpl`) in your Inkscape user configuration directory.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
