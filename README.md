# MyOmnara

A simple CLI tool to run local AI agents with a web terminal using tmux + ttyd.

## 🚀 Install

```bash
curl -fsSL https://raw.githubusercontent.com/kumar045/Control-PC-Terminal
/main/install.sh | bash
```
🧠 Usage
```bash
myomnara
```
You will be prompted to choose an agent:
1) codex
2) claude
3) other

After selecting, MyOmnara will:

Start the selected agent in a tmux session

Expose it over a web browser via ttyd

Open at http://localhost:7681
