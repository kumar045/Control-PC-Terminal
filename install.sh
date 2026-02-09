#!/usr/bin/env bash
set -e

# ========================================
# Installer for Control-Terminal CLI
# ========================================

echo "Installing dependencies..."

# Resolve script directory (may be empty if piped from curl)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-./}")" && pwd 2>/dev/null || true)"
CONTROL_TERMINAL_SRC="${SCRIPT_DIR}/control-terminal"
CONTROL_TERMINAL_TMP=""

# Install tmux if not present
if ! command -v tmux >/dev/null 2>&1; then
  if command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y tmux
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y tmux
  else
    echo "Please install tmux manually"
  fi
else
  echo "tmux already installed"
fi

# Install ttyd if not present
if ! command -v ttyd >/dev/null 2>&1; then
  echo "Installing ttyd..."
  mkdir -p "$HOME/.control-terminal/bin"
  OS=$(uname | tr '[:upper:]' '[:lower:]')
  ARCH=$(uname -m)
  case "$ARCH" in
    x86_64|amd64) ARCH="amd64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *) echo "Unsupported arch $ARCH"; exit 1 ;;
  esac
  LATEST=$(curl -fsSL "https://api.github.com/repos/tsl0922/ttyd/releases/latest" \
            | grep '"tag_name"' | head -1 | cut -d '"' -f4)
  FILE="ttyd-${OS}-${ARCH}"
  URL="https://github.com/tsl0922/ttyd/releases/download/${LATEST}/${FILE}"
  curl -fsSL "$URL" -o "$HOME/.control-terminal/bin/ttyd"
  chmod +x "$HOME/.control-terminal/bin/ttyd"
  export PATH="$HOME/.control-terminal/bin:$PATH"

  # Persist PATH for future shells
  if ! grep -qs 'export PATH="$HOME/.control-terminal/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.control-terminal/bin:$PATH"' >> "$HOME/.bashrc"
  fi
else
  echo "ttyd already installed"
fi

# Install control-terminal CLI
echo "Installing control-terminal CLI..."
if [ ! -f "$CONTROL_TERMINAL_SRC" ]; then
  echo "control-terminal script not found locally. Downloading..."
  CONTROL_TERMINAL_TMP="$(mktemp)"
  curl -fsSL "https://raw.githubusercontent.com/kumar045/Control-PC-Terminal/main/control-terminal" -o "$CONTROL_TERMINAL_TMP"
  CONTROL_TERMINAL_SRC="$CONTROL_TERMINAL_TMP"
fi

sudo cp "$CONTROL_TERMINAL_SRC" /usr/local/bin/control-terminal
sudo chmod +x /usr/local/bin/control-terminal
if [ -n "$CONTROL_TERMINAL_TMP" ] && [ -f "$CONTROL_TERMINAL_TMP" ]; then
  rm -f "$CONTROL_TERMINAL_TMP"
fi

echo ""
echo "Installation complete!"
echo "Run: control-terminal"
