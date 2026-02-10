#!/usr/bin/env bash
set -e

echo "========================================"
echo " Installer for Control-Terminal CLI"
echo "========================================"
echo

echo "Installing dependencies..."

# ----------------------------------------
# Resolve script directory
# ----------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-./}")" && pwd 2>/dev/null || true)"
CONTROL_TERMINAL_SRC="${SCRIPT_DIR}/control-terminal"
CONTROL_TERMINAL_TMP=""

# ----------------------------------------
# Install tmux
# ----------------------------------------
if ! command -v tmux >/dev/null 2>&1; then
  echo "Installing tmux..."
  if command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y tmux
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y tmux
  else
    echo "❌ Please install tmux manually"
    exit 1
  fi
else
  echo "tmux already installed"
fi

# ----------------------------------------
# Install ttyd
# ----------------------------------------
if ! command -v ttyd >/dev/null 2>&1; then
  echo "Installing ttyd..."

  mkdir -p "$HOME/.control-terminal/bin"

  OS="$(uname | tr '[:upper:]' '[:lower:]')"
  ARCH="$(uname -m)"

  if [ "$OS" != "linux" ]; then
    echo "❌ ttyd auto-install currently supports Linux only"
    exit 1
  fi

  case "$ARCH" in
    x86_64|amd64)
      TTYD_FILE="ttyd.x86_64"
      ;;
    aarch64|arm64)
      TTYD_FILE="ttyd.aarch64"
      ;;
    *)
      echo "❌ Unsupported architecture: $ARCH"
      exit 1
      ;;
  esac

  LATEST_TAG="$(curl -fsSL https://api.github.com/repos/tsl0922/ttyd/releases/latest \
    | grep '"tag_name"' | cut -d '"' -f4)"

  TTYD_URL="https://github.com/tsl0922/ttyd/releases/download/${LATEST_TAG}/${TTYD_FILE}"

  echo "Downloading $TTYD_URL"
  curl -fL "$TTYD_URL" -o "$HOME/.control-terminal/bin/ttyd"

  chmod +x "$HOME/.control-terminal/bin/ttyd"

  # Persist PATH
  if ! grep -qs 'control-terminal/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.control-terminal/bin:$PATH"' >> "$HOME/.bashrc"
  fi

  export PATH="$HOME/.control-terminal/bin:$PATH"
else
  echo "ttyd already installed"
fi

# ----------------------------------------
# Install control-terminal CLI
# ----------------------------------------
echo "Installing control-terminal CLI..."

if [ ! -f "$CONTROL_TERMINAL_SRC" ]; then
  echo "control-terminal script not found locally. Downloading..."
  CONTROL_TERMINAL_TMP="$(mktemp)"
  curl -fsSL \
    "https://raw.githubusercontent.com/kumar045/Control-PC-Terminal/main/control-terminal" \
    -o "$CONTROL_TERMINAL_TMP"
  CONTROL_TERMINAL_SRC="$CONTROL_TERMINAL_TMP"
fi

sudo cp "$CONTROL_TERMINAL_SRC" /usr/local/bin/control-terminal
sudo chmod 755 /usr/local/bin/control-terminal

if [ -n "$CONTROL_TERMINAL_TMP" ] && [ -f "$CONTROL_TERMINAL_TMP" ]; then
  rm -f "$CONTROL_TERMINAL_TMP"
fi

echo
echo "✅ Installation complete!"
echo "👉 Run: control-terminal"
