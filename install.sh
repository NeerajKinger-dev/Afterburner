#!/usr/bin/env bash

# ==============================================================================
# Afterburner: Workspace Engine & CorelDRAW Patch Deployer
# Targets: Inkscape (CorelDRAW Profile) across Linux & macOS
# ==============================================================================

set -euo pipefail

# --- ANSI 256-Color & Format Palette ---
RST='\033[0m'
BOLD='\033[1m'

# Flame & Energy Palette
FIRE_RED='\033[38;5;196m'
FIRE_ORANGE='\033[38;5;208m'
FIRE_GOLD='\033[38;5;220m'
NEON_CYAN='\033[38;5;51m'
EMERALD_GREEN='\033[38;5;46m'
DIM_GRAY='\033[38;5;242m'
BRIGHT_WHITE='\033[1;37m'

# --- Badge Logger Helpers ---
log_info()    { echo -e "  ${NEON_CYAN}ℹ [ INFO ]${RST}  $1"; }
log_patch()   { echo -e "  ${FIRE_ORANGE}🔥 [ PATCH ]${RST} $1"; }
log_success() { echo -e "  ${EMERALD_GREEN}✔ [ SUCCESS ]${RST} $1"; }
log_warn()    { echo -e "  ${FIRE_GOLD}⚠ [ WARN ]${RST}  $1"; }
log_error()   { echo -e "  ${FIRE_RED}✖ [ ERROR ]${RST} $1"; }

# --- Header Banner ---
draw_banner() {
    clear 2>/dev/null || true
    echo -e "${FIRE_RED}"
    echo -e "  ___  ______ _____ _____ ____  _____ _____  _   _ _____ _____ "
    echo -e " / _ \ |  ___|_   _|  ___|  _ \|  _  /  ___|| \ | |  ___|  _  \\"
    echo -e "/ /_\ \| |_    | | | |__ | |_) | |_| \ \`--. |  \| | |__ | |_) |"
    echo -e "|  _  ||  _|   | | |  __||  _ <|  _  |\`--. \| . \` |  __||  _ < "
    echo -e "| | | || |    _| |_| |___| |_) | | | /\__/ /| |\  | |___| |_) |"
    echo -e "\_| |_/\_|   |_____|_____|____/\_| |_\____/ \_| \_|_____|____/ "
    echo -e "${RST}"
    echo -e "  ${FIRE_ORANGE}🔥 CorelDRAW to Inkscape Workspace Engine${RST} ${DIM_GRAY}|${RST} ${NEON_CYAN}v2.1 Release${RST}"
    echo -e "  ${DIM_GRAY}─────────────────────────────────────────────────────────────────────────────${RST}"
    echo ""
}

# --- Payload Verification ---
PAYLOAD_DIR="./config-payload"
if [[ ! -d "$PAYLOAD_DIR" ]]; then
    draw_banner
    log_error "Payload directory '${PAYLOAD_DIR}' not found."
    log_error "Please run this script from the root of the Afterburner folder."
    echo ""
    exit 1
fi

# --- Target Paths ---
declare -a INKSCAPE_TARGETS=(
    "$HOME/.var/app/org.inkscape.Inkscape/config/inkscape" # Linux Flatpak
    "$HOME/snap/inkscape/current/.config/inkscape"         # Linux Snap
    "$HOME/.config/inkscape"                               # Linux Native APT / Standard
    "$HOME/Library/Application Support/org.inkscape.Inkscape/config/inkscape" # macOS App
    "$HOME/Library/Application Support/Inkscape"           # macOS Native / Homebrew
)

deploy_inkscape_patch() {
    log_info "Scanning active system environment for Inkscape profiles..."
    echo ""
    local patched_count=0
    local source_inkscape="$PAYLOAD_DIR/inkscape"

    if [[ ! -d "$source_inkscape" ]]; then
        log_warn "No Inkscape payload found in '$source_inkscape'. Skipping Module."
        return
    fi

    for base_path in "${INKSCAPE_TARGETS[@]}"; do
        if [[ -d "$base_path" ]]; then
            log_patch "Found target Inkscape profile at: ${BRIGHT_WHITE}${base_path}${RST}"
            
            mkdir -p "$base_path/keys" "$base_path/palettes" "$base_path/extensions"

            if [[ -d "$source_inkscape/keys" ]]; then
                cp -r "$source_inkscape/keys"/* "$base_path/keys/"
            fi
            if [[ -d "$source_inkscape/palettes" ]]; then
                cp -r "$source_inkscape/palettes"/* "$base_path/palettes/"
            fi
            if [[ -d "$source_inkscape/extensions" ]]; then
                cp -r "$source_inkscape/extensions"/* "$base_path/extensions/"
            fi

            log_success "Injected CorelDRAW shortcuts, palettes & extensions."
            echo ""
            patched_count=$((patched_count + 1))
        fi
    done

    if (( patched_count == 0 )); then
        log_warn "No active Inkscape installation paths found."
        log_info "Initializing default native Inkscape path: ${BRIGHT_WHITE}$HOME/.config/inkscape${RST}"
        local default_path="$HOME/.config/inkscape"
        mkdir -p "$default_path/keys" "$default_path/palettes" "$default_path/extensions"
        
        if [[ -d "$source_inkscape/keys" ]]; then
            cp -r "$source_inkscape/keys"/* "$default_path/keys/"
        fi
        if [[ -d "$source_inkscape/palettes" ]]; then
            cp -r "$source_inkscape/palettes"/* "$default_path/palettes/"
        fi
        if [[ -d "$source_inkscape/extensions" ]]; then
            cp -r "$source_inkscape/extensions"/* "$default_path/extensions/"
        fi

        log_success "Created profile & injected Afterburner v2.1 payload."
        echo ""
    fi
}

main() {
    draw_banner
    deploy_inkscape_patch

    echo -e "  ${DIM_GRAY}─────────────────────────────────────────────────────────────────────────────${RST}"
    echo -e "  ${EMERALD_GREEN}🚀 [ COMPLETE ] Afterburner v2.1 injected successfully!${RST}"
    echo -e "  ${FIRE_GOLD}👉 Restart Inkscape to activate your CorelDRAW workspace & extensions.${RST}"
    echo -e "  ${DIM_GRAY}─────────────────────────────────────────────────────────────────────────────${RST}"
    echo ""
}

main "$@"
