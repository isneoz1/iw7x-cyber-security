#!/usr/bin/env bash
#
# iw7x — installer (by NeoZ)
# For authorized security testing and education only.
#
# Installs the base dependencies needed to run iw7x and to install catalog
# tools (git, python3, pip, pipx, go, etc.).
#
set -euo pipefail

CYAN='\033[1;36m'; GREEN='\033[1;32m'; YELLOW='\033[1;33m'; RED='\033[1;31m'; NC='\033[0m'
say()  { echo -e "${CYAN}[iw7x]${NC} $1"; }
ok()   { echo -e "${GREEN}[ok]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[x]${NC} $1"; }

cd "$(dirname "$0")"

# ── Privileges ─────────────────────────────────────────────────────────────────
SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if command -v doas >/dev/null 2>&1; then SUDO="doas";
  elif command -v sudo >/dev/null 2>&1; then SUDO="sudo";
  else warn "Neither sudo nor doas found — run this script as root if install fails."; fi
fi

# ── Package manager detection ──────────────────────────────────────────────────
PM=""
for mgr in apt-get pacman dnf zypper apk brew pkg; do
  if command -v "$mgr" >/dev/null 2>&1; then PM="$mgr"; break; fi
done
say "System: $(uname -s) $(uname -m)  ·  package manager: ${PM:-unknown}"

install_pkgs() {
  local pkgs="$*"
  case "$PM" in
    apt-get) $SUDO apt-get update -qq && $SUDO apt-get install -y $pkgs ;;
    pacman)  $SUDO pacman -Sy --noconfirm $pkgs ;;
    dnf)     $SUDO dnf install -y $pkgs ;;
    zypper)  $SUDO zypper install -y $pkgs ;;
    apk)     $SUDO apk add $pkgs ;;
    brew)    brew install $pkgs ;;
    pkg)     $SUDO pkg install -y $pkgs ;;
    *)       warn "Install manually: $pkgs" ;;
  esac
}

# ── Base system dependencies ───────────────────────────────────────────────────
say "Installing base dependencies..."
case "$PM" in
  apt-get) install_pkgs git python3 python3-pip python3-venv pipx curl wget golang-go ruby nodejs npm ;;
  pacman)  install_pkgs git python python-pip python-pipx curl wget go ruby nodejs npm ;;
  dnf)     install_pkgs git python3 python3-pip pipx curl wget golang ruby nodejs npm ;;
  brew)    install_pkgs git python pipx curl wget go ruby node ;;
  *)       install_pkgs git python3 curl wget ;;
esac
ok "Base dependencies handled."

# ── Python: rich (UI) via pip ─────────────────────────────────────────────────
say "Installing rich (UI)..."
if command -v pip3 >/dev/null 2>&1; then
  pip3 install --user -r requirements.txt 2>/dev/null || pip3 install --user --break-system-packages -r requirements.txt || warn "Install rich manually: pip3 install rich"
else
  warn "pip3 not found — install rich manually."
fi

# ── pipx (used by many catalog tools) ─────────────────────────────────────────
if command -v pipx >/dev/null 2>&1; then
  pipx ensurepath >/dev/null 2>&1 || true
  ok "pipx ready."
else
  warn "pipx not installed — some Python tools will need manual install."
fi

# ── Go PATH ────────────────────────────────────────────────────────────────────
if command -v go >/dev/null 2>&1; then
  GB="$(go env GOBIN 2>/dev/null || true)"; [ -z "$GB" ] && GB="$(go env GOPATH)/bin"
  if ! echo "$PATH" | grep -q "$GB"; then
    warn "Add Go to PATH:  export PATH=\"\$PATH:$GB\""
  fi
fi

# ── Optional global launcher ──────────────────────────────────────────────────
chmod +x iw7x.py neoz.py 2>/dev/null || true
if [ -n "$SUDO" ] || [ "$(id -u)" -eq 0 ]; then
  DIR="$(pwd)"
  $SUDO tee /usr/local/bin/iw7x >/dev/null <<EOF || true
#!/usr/bin/env bash
exec python3 "$DIR/iw7x.py" "\$@"
EOF
  $SUDO chmod +x /usr/local/bin/iw7x 2>/dev/null && ok "Global command installed: type 'iw7x'"
fi

echo
ok "Installation complete."
say "Run:  ${GREEN}python3 iw7x.py${NC}   (or: iw7x)"
warn "Reminder: use iw7x only for authorized security testing."
