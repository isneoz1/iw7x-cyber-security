#!/usr/bin/env bash
#
# iw7x — updater (by NeoZ)
# Updates iw7x itself (git) and its UI dependency (rich).
#
set -uo pipefail

CYAN='\033[1;36m'; GREEN='\033[1;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
say()  { echo -e "${CYAN}[iw7x]${NC} $1"; }
ok()   { echo -e "${GREEN}[ok]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }

cd "$(dirname "$0")"

# ── Update source code (if a git repo) ─────────────────────────────────────────
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  say "Updating source code (git pull)..."
  if git pull --ff-only; then ok "Code up to date."; else warn "git pull failed — check your repo."; fi
else
  warn "Not a git repo — skipping code update."
fi

# ── Update rich ────────────────────────────────────────────────────────────────
say "Updating rich..."
if command -v pip3 >/dev/null 2>&1; then
  pip3 install --user --upgrade rich 2>/dev/null \
    || pip3 install --user --break-system-packages --upgrade rich \
    || warn "Could not auto-update rich."
  ok "rich up to date."
else
  warn "pip3 not found."
fi

# ── Update pipx-installed tools ────────────────────────────────────────────────
if command -v pipx >/dev/null 2>&1; then
  say "Updating pipx-installed tools..."
  pipx upgrade-all 2>/dev/null || warn "No pipx packages to update."
fi

# ── Auto-refresh the tool catalog from online sources (BlackArch, …) ──────────
say "Refreshing the tool catalog (fetching every tool online)..."
python3 iw7x.py --update || warn "Catalog update skipped (offline?)."

echo
ok "Update complete."
say "Run:  ${GREEN}python3 iw7x.py${NC}"
