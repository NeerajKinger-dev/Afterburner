<p align="center">
  <img src="assets/logo.png" alt="Afterburner Logo - Ultimate Free CorelDRAW Alternative with Corel Shortcuts" width="280">
</p>

<h1 align="center">Afterburner 🚀</h1>

<p align="center">
  <b>The Drop-In Bridge Turning Inkscape into the Ultimate Free CorelDRAW Alternative</b>
</p>

<p align="center">
  <a href="https://github.com/NeerajKinger-dev/Afterburner/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Version-v2.1--release-red.svg" alt="Version: v2.1">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-brightgreen.svg" alt="Platform: Linux | macOS | Windows">
  <img src="https://img.shields.io/badge/Inkscape-1.2%2B-orange.svg" alt="Inkscape 1.2+ Supported">
  <img src="https://img.shields.io/badge/CorelDRAW-Interop-purple.svg" alt="CorelDRAW Interop Suite">
</p>

---

## 📌 The Best Free Open Source CorelDRAW Alternative with Corel Shortcuts

Looking for **free vector software that feels like CorelDRAW** without breaking your workflow or muscle memory? 

**Afterburner v2.1** is an automated workspace engine and extension suite that instantly transforms **Inkscape** into the ultimate **free open source CorelDRAW alternative**. By injecting native CorelDRAW keymappings, right-hand docker panel alignment, the iconic `CorelDRAW.gpl` color swatch strip, a **Multi-Page CorelDRAW (.cdr) Import Extension**, and a **CorelDRAW Compatible Export Extension**, Afterburner provides a zero-learning-curve transition for vector designers, illustrators, and print shops migrating to open-source software on **Linux**, **macOS**, and **Windows**.

---

## 📑 Table of Contents
- [Why Inkscape + Afterburner is the Ultimate Free CorelDRAW Alternative](#-why-inkscape--afterburner-is-the-ultimate-free-coreldraw-alternative)
- [Key Features](#-key-features)
- [CorelDRAW vs Inkscape Keybinding Comparison](#-coreldraw-vs-inkscape-keybinding-comparison)
- [Multi-Page CDR Importer Extension (v2.0)](#-multi-page-cdr-importer-extension-v20)
- [CorelDRAW Compatible Export Extension (v2.1)](#-coreldraw-compatible-export-extension-v21)
- [How to Make Inkscape Work Like CorelDRAW for Free](#-how-to-make-inkscape-work-like-coreldraw-for-free)
- [Roadmap & Status](#-roadmap--implementation)
- [Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [License](#-license)

---

## 💡 Why Inkscape + Afterburner is the Ultimate Free CorelDRAW Alternative

Inkscape is the leading free, open-source vector graphics editor, but transitioning from CorelDRAW to Inkscape usually causes severe muscle-memory friction. **Afterburner acts as the drop-in bridge** to eliminate that barrier:

1. **Zero Muscle-Memory Breakage**: Keep using `Spacebar` for Pick tool, `F10` for Node editing, and `F5` for Freehand drawing.
2. **Seamless CorelDRAW Export Interop**: Export normalized PDF/EPS files with automatic text-to-path conversion (`Ctrl+Q` equivalent) and 96 DPI / mm physical unit scaling calibration.
3. **Multi-Page CDR File Support**: Import multi-page `.cdr` files into native Inkscape 1.2+ multi-page document structures (`<inkscape:page>`).
4. **Native Docker Layouts**: Lock Object Properties, Layers, and Fill/Stroke dialogs directly to the right-side margin, mirroring CorelDRAW's classic workspace layout.
5. **Hex-Validated Color Swatches**: Enjoy immediate access to the classic CorelDRAW color palette directly in Inkscape's bottom tray.
6. **Cross-Platform & 100% Free**: Deploy effortlessly across Ubuntu/Debian, macOS, and Windows 10/11.

---

## ⚡ Key Features

* 📤 **CorelDRAW Compatible Export Extension (v2.1)**: Normalizes text nodes to vector paths, calibrates viewBox physical units (mm/in), and exports multi-page PDF/EPS files optimized for opening in CorelDRAW.
* 📄 **Multi-Page CDR Import Extension (v2.0)**: Extracts multi-page `.cdr` files and injects pages into native Inkscape 1.2+ `<inkscape:page>` elements with offset coordinates and layer groups.
* 🎯 **CorelDRAW Keyboard Shortcuts**: Instantly rebinds navigation, selection, and shape tools to classic CorelDRAW hotkeys.
* 🎨 **Classic CorelDRAW Palette Integration**: Installs the native `CorelDRAW.gpl` swatch strip into Inkscape's palette bar.
* 📐 **Right-Side Docker Panels**: Aligns layers, object properties, and fill/stroke controls into clean right-side dockers.
* 🤖 **Automated Multi-Platform Installer**: Auto-detects Inkscape installations across Linux (APT, Snap, Flatpak), macOS, and Windows.

---

## 📤 CorelDRAW Compatible Export Extension (v2.1)

Afterburner v2.1 introduces `export_corel_interop`, an Inkscape Python extension located under:
`File -> Export -> CorelDRAW Compatible Export...` and `Extensions -> Afterburner -> CorelDRAW Tools -> CorelDRAW Compatible Export`.

### Features & Settings:
- **Font Mapping Strategy**: Option to convert all text to vector paths/outlines (`Ctrl+Q` equivalent) or embed system fonts.
- **DPI Viewport Calibration**: Forces 96 DPI physical units (`mm` or `in`) on SVG `width`/`height`/`viewBox` to eliminate scaling errors when CorelDRAW opens the file.
- **Export Format**: Vector PDF (CorelDRAW X3+) or EPS (Legacy CorelDRAW PostScript).
- **Multi-page Canvas Export**: Exports all Inkscape canvas pages into a single multi-page PDF document stream.

---

## 📄 Multi-Page CDR Importer Extension (v2.0)

Afterburner introduces `cdr_multipage_importer`, an Inkscape Python extension located under:
`Extensions -> Afterburner -> CorelDRAW Tools -> Multi-Page CDR Import`.

### How it Works:
1. Converts multi-page `.cdr` documents using `libcdr-tools` or `soffice` / `libreoffice` headless converters.
2. Splits pages cleanly via `pdftocairo` / `pdf2svg`.
3. Constructs native Inkscape 1.2+ multi-page SVG DOM elements (`<inkscape:page x="..." y="0" width="..." height="..." label="Page N" />`).
4. Wraps page vector graphics into individual layer groups (`<g inkscape:groupmode="layer" inkscape:label="Page N Content">`).

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

### Phase 1: Core Layout Core
* [x] Automated path-detection installer framework (`install.sh` for Linux/macOS & `install.ps1` for Windows)
* [x] CorelDRAW industry-standard keyboard shortcut profiles
* [x] CorelDRAW classic palette swatch strip integration (`CorelDRAW.gpl`)
* [x] Single-column tool hierarchies and docker panel alignment

### Phase 2: Multi-Page CorelDRAW Support (v2.0)
* [x] Multi-Page CDR Import Extension (`cdr_multipage_importer.inx` & `.py`)
* [x] Automatic SVG DOM reconstruction (`<inkscape:page>` in `<sodipodi:namedview>`)
* [x] Automated unit test suite (`tests/test_cdr_importer.py`)
* [x] Cross-platform extension installer integration

### Phase 3: CorelDRAW Export Interoperability (v2.1)
* [x] CorelDRAW Compatible Export Extension (`export_corel_interop.inx` & `.py`)
* [x] Text-to-Path vector outline normalization (`Ctrl+Q` equivalent)
* [x] Physical unit viewBox calibration (96 DPI / mm scaling normalization)
* [x] Automated unit test suite (`tests/test_export_interop.py`)

---

## ❓ Frequently Asked Questions (FAQ)

### How do I export Inkscape files cleanly to CorelDRAW without font or scaling issues?
Use Afterburner v2.1's **CorelDRAW Compatible Export** extension (`File -> Export -> CorelDRAW Compatible Export...`). It automatically converts live text to vector paths and normalizes SVG viewport physical units (`mm`) to prevent font substitution and scaling errors in CorelDRAW.

### How does Inkscape handle multi-page CorelDRAW (.cdr) files?
Inkscape standard imports often flatten secondary pages. Afterburner provides `cdr_multipage_importer`, which extracts all `.cdr` pages and builds a native Inkscape 1.2+ multi-page document automatically.

### What is the best free open source CorelDRAW alternative with Corel shortcuts?
**Inkscape combined with Afterburner v2.1** is the best free open source CorelDRAW alternative. Afterburner automatically configures Inkscape with authentic CorelDRAW keyboard shortcuts, right-side docker panels, CorelDRAW color swatches, multi-page CDR import, and CorelDRAW export interop.

### Will Afterburner delete my custom vector files or existing artwork?
No. Afterburner only updates configuration XML keymaps (`default.xml`), palette swatch files (`CorelDRAW.gpl`), and extension scripts in your Inkscape user configuration directory.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.


