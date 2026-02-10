# Control-Terminal

A simple CLI tool to run local AI agents with a web terminal using tmux + ttyd.

Control-Terminal lets you control AI agents like Claude Code, Codex, or any custom CLI agent running on your system from anywhere—especially from your mobile phone.

## 🚀 Install

```bash
curl -fsSL https://raw.githubusercontent.com/kumar045/Control-PC-Terminal/main/install.sh | bash
```

The installer downloads the `control-terminal` script and adds `~/.control-terminal/bin` to your PATH in `~/.bashrc`.

## 🧠 Usage

```bash
control-terminal
```

You will be prompted to choose an agent:

1) codex
2) claude
3) other

After selecting, Control-Terminal will:

- Start the selected agent in a tmux session
- Expose it over a web browser via ttyd
- Keep the browser terminal in read/write mode so you can type commands remotely
- Open at `http://localhost:7681`

This makes it easy to manage long-running agent tasks from another device while away from your desk.

If `ttyd` is not installed, Control-Terminal now attempts to install the latest ttyd release automatically (Linux only).

If you opt-in to public access, Control-Terminal downloads `cloudflared` automatically (Linux only), starts a Cloudflare Tunnel, and prints a `trycloudflare.com` URL that you can share.
