#!/usr/bin/env bash
set -e

# ========================================
# Installer for MyOmnara CLI
# ========================================

echo "Installing dependencies..."

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
  mkdir -p "$HOME/.myomnara/bin"
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
  curl -fsSL "$URL" -o "$HOME/.myomnara/bin/ttyd"
  chmod +x "$HOME/.myomnara/bin/ttyd"
  export PATH="$HOME/.myomnara/bin:$PATH"
else
  echo "ttyd already installed"
fi

# Install myomnara CLI
echo "Installing myomnara CLI..."
sudo cp myomnara /usr/local/bin/
sudo chmod +x /usr/local/bin/myomnara

echo ""
echo "Installation complete!"
echo "Run: myomnara"
