#!/usr/bin/env bash

# ==============================================================================
# Afterburner: Linux Workspace Engine
# Targets: Inkscape (CorelDRAW Profile)
# Handles: Flatpak, Snap, and Native APT installations on Ubuntu/Debian
# ==============================================================================

set -euo pipefail

# --- Color Output Helpers ---
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

# --- Verification Check ---
PAYLOAD_DIR="./config-payload"
if [[ ! -d "$PAYLOAD_DIR" ]]; then
    log_error "Payload directory '$PAYLOAD_DIR' not found."
    log_error "Please run this script from the root of the Afterburner folder."
    exit 1
fi

# --- Target Paths ---
declare -a INKSCAPE_TARGETS=(
    "$HOME/.var/app/org.inkscape.Inkscape/config/inkscape" # Flatpak
    "$HOME/snap/inkscape/current/.config/inkscape"         # Snap
    "$HOME/.config/inkscape"                               # Native APT
)

deploy_inkscape_patch() {
    log_info "Scanning for active Inkscape profile directories..."
    local patched_count=0
    local source_inkscape="$PAYLOAD_DIR/inkscape"

    if [[ ! -d "$source_inkscape" ]]; then
        log_warn "No Inkscape payload found in '$source_inkscape'. Skipping Module."
        return
    fi

    for base_path in "${INKSCAPE_TARGETS[@]}"; do
        if [[ -d "$base_path" ]]; then
            log_info "Found active Inkscape profile at: $base_path"
            mkdir -p "$base_path/keys" "$base_path/palettes"

            if [[ -d "$source_inkscape/keys" ]]; then
                cp -r "$source_inkscape/keys"/* "$base_path/keys/"
            fi
            if [[ -d "$source_inkscape/palettes" ]]; then
                cp -r "$source_inkscape/palettes"/* "$base_path/palettes/"
            fi

            log_success "Successfully deployed Afterburner CD to $base_path"
            ((patched_count++))
        fi
    done

    if (( patched_count == 0 )); then
        log_warn "No active Inkscape environment paths detected. Ensure Inkscape has been run once."
    fi
}

main() {
    echo -e "${BLUE}====================================================${NC}"
    echo -e "${YELLOW}         Afterburner: Linux Workspace Engine        ${NC}"
    echo -e "${BLUE}====================================================${NC}"
    
    deploy_inkscape_patch

    echo -e "${BLUE}====================================================${NC}"
    log_success "Afterburner payload successfully injected! Restart Inkscape to initialize."
    echo -e "${BLUE}====================================================${NC}"
}

main "$@"

