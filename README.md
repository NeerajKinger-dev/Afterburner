<p align="center">
  <img src="assets/logo.png" alt="Afterburner Logo - CorelDRAW to Inkscape Migration Patch" width="280">
</p>

<h1 align="center">Afterburner 🚀</h1>

<p align="center">
  <b>Frictionless workspace migration patch transforming Inkscape into a native CorelDRAW environment.</b>
</p>

<p align="center">
  <a href="https://github.com/NeerajKinger-dev/Afterburner/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-brightgreen.svg" alt="Platform: Linux | macOS | Windows">
  <img src="https://img.shields.io/badge/Inkscape-1.0%2B-orange.svg" alt="Inkscape 1.0+ Supported">
</p>

---

## 📌 Overview & Value Proposition

**Afterburner** is an open-source workspace configuration engine designed for graphic designers, sign makers, and vector artists migrating from **CorelDRAW** to **Inkscape** on **Ubuntu/Linux**, **macOS**, and **Windows**. 

It eliminates muscle-memory friction by automatically remapping Inkscape keyboard shortcuts, docking UI panels to industry-standard right-side margins, and installing the iconic **CorelDRAW color palette** (`CorelDRAW.gpl`).

---

## 📑 Table of Contents
- [Key Features](#-key-features)
- [CorelDRAW vs Inkscape Keybinding Comparison](#-coreldraw-vs-inkscape-keybinding-comparison)
- [Installation](#-installation)
  - [Linux (Ubuntu, Debian, Flatpak, Snap)](#-linux-ubuntu--debian--flatpak--snap--native)
  - [macOS](#-macos-installation)
  - [Windows](#-windows-inkscape-1x)
- [Roadmap & Status](#-roadmap--implementation)
- [Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [License](#-license)

---

## ⚡ Key Features

* 🎯 **CorelDRAW Keyboard Shortcuts**: Instantly rebinds navigation, selection, and drawing tools to classic CorelDRAW hotkeys.
* 🎨 **Classic CorelDRAW Palette Integration**: Adds the classic `CorelDRAW.gpl` swatch strip to Inkscape's bottom palette bar.
* 📐 **Right-Side Docker Panels**: Aligns layers, object properties, and fill/stroke dialogs into clean right-side dockers.
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

## 🚀 Roadmap & Implementation

### Phase 1: Core Layout Core (Current)
* [x] Automated path-detection installer framework (`install.sh` for Linux/macOS & `install.ps1` for Windows)
* [x] CorelDRAW industry-standard keyboard shortcut profiles
* [x] CorelDRAW classic palette swatch strip integration (`CorelDRAW.gpl`)
* [x] Single-column tool hierarchies and docker panel alignment

---

## 💻 Installation

### 🐧 Linux (Ubuntu / Debian / Flatpak / Snap / Native)
Open your terminal inside the `Afterburner` directory:
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

## ❓ Frequently Asked Questions (FAQ)

### How do I make Inkscape behave and look like CorelDRAW?
Run Afterburner's automated installer script (`install.sh` on Linux/macOS or `install.ps1` on Windows). It injects CorelDRAW shortcuts and color palettes into Inkscape's user profile directory automatically.

### Does Afterburner support Inkscape installed via Flatpak or Snap?
Yes! The Linux installer (`install.sh`) automatically scans for Flatpak (`org.inkscape.Inkscape`), Snap (`snap/inkscape`), and native APT paths (`~/.config/inkscape`).

### Will Afterburner delete my custom vector files or existing artwork?
No. Afterburner only updates configuration XML keymaps (`default.xml`) and palette swatch files (`CorelDRAW.gpl`) in your Inkscape user profile directory.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
