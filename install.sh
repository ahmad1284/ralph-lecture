#!/usr/bin/env bash
# One-shot installer: system deps + prompt2video CLI on PATH
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── system dependencies ────────────────────────────────────────────────────────
install_sys_deps() {
    if command -v apt-get &>/dev/null; then
        echo "→ apt: installing system deps..."
        sudo apt-get update -qq
        sudo apt-get install -y --no-install-recommends \
            ffmpeg espeak-ng libespeak-ng1 \
            nodejs npm
    elif command -v dnf &>/dev/null; then
        echo "→ dnf: installing system deps..."
        sudo dnf install -y \
            ffmpeg espeak-ng espeak-ng-devel \
            nodejs npm
    elif command -v pacman &>/dev/null; then
        echo "→ pacman: installing system deps..."
        sudo pacman -Sy --noconfirm \
            ffmpeg espeak-ng \
            nodejs npm
    else
        echo "⚠  Unknown package manager. Install manually:"
        echo "   ffmpeg, espeak-ng, nodejs, npm"
        echo "   Then re-run this script."
        exit 1
    fi
}

# ── uv ────────────────────────────────────────────────────────────────────────
install_uv() {
    if ! command -v uv &>/dev/null; then
        echo "→ installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        # add to current shell
        export PATH="$HOME/.local/bin:$PATH"
    fi
}

# ── main ──────────────────────────────────────────────────────────────────────
install_sys_deps
install_uv

echo "→ installing prompt2video..."
uv tool install "$REPO_DIR"

echo ""
echo "✓ Done. Run: prompt2video --help"
