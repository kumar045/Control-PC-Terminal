# Control-Terminal

A simple CLI tool to run local AI agents with a web terminal using tmux + ttyd.

Control-Terminal lets you control AI agents like Claude Code, Codex, or any custom CLI agent running on your system from anywhere—especially from your mobile phone.

Because your agent runs inside `tmux`, your work keeps running even if your mobile/browser connection drops, so you can reconnect without losing progress.

## ✨ Why Control-Terminal is special

Control-Terminal is not just a web terminal launcher. It combines three proven tools into one smooth workflow for AI-agent sessions from mobile:

- **`tmux` = session persistence**
  - Your Claude/Codex job keeps running on your machine even if your phone browser disconnects, screen locks, or network changes.
  - You can reconnect anytime and continue the same live session.
- **`ttyd` = browser access to that same terminal**
  - It turns your terminal into a web UI you can open from mobile.
  - You can interact with the exact tmux session, not a separate shell.
- **`cloudflared` (optional) = easy remote/public access**
  - It gives you a shareable URL quickly, without manual router/NAT setup.

The result: **uninterrupted agent workflows from mobile with minimal setup**.

## 🧩 Why use both `tmux` and `ttyd`?

They solve different problems and work best together:

- `tmux` keeps processes alive and recoverable.
- `ttyd` provides remote browser input/output.

If you use only `ttyd` without `tmux`, your long-running agent process is more fragile when sessions reset.
If you use only `tmux` without `ttyd`, you still need SSH client tooling on mobile and a less convenient browser experience.

So the pair gives you both:

1. **durability** (`tmux`), and
2. **accessibility** (`ttyd`).

## ☁️ Why `cloudflared` instead of ngrok or others?

Control-Terminal uses `cloudflared` because it fits this use case well:

- **Simple onboarding**: one command flow, no custom reverse-proxy setup required.
- **Good tunnel stability** for long-lived terminal sessions.
- **Quick shareable URL** generation for remote/mobile access.
- **Works well as optional mode**: local-only usage still works at `localhost:7681`.

Other options like ngrok, Tailscale, WireGuard, or self-hosted reverse proxies are valid too. 
This project chooses `cloudflared` by default for a practical balance of speed, usability, and fewer setup steps for most users. 

## 🚀 Install

```bash
curl -fsSL https://raw.githubusercontent.com/kumar045/Control-PC-Terminal/main/install.sh | bash
```

The installer downloads the `control-terminal` script and adds `~/.control-terminal/bin` to your PATH in `~/.bashrc`.

## 🖥️ OS support

- **Linux**: supported directly.
- **Windows**: use **WSL (Windows Subsystem for Linux)** and run Control-Terminal inside your WSL distro.
  
## 🧠 Usage

```bash
control-terminal
```

You will be prompted to choose an agent:

1) codex
2) claude
3) other
4) preconfigured custom agent

After selecting, Control-Terminal will:

- Start the selected agent in a tmux session
- Optionally let you set a username/password for the web terminal after agent selection
- Expose it over a web browser via ttyd
- Keep the browser terminal in read/write mode so you can type commands remotely
- Open at `http://localhost:7681`

This makes it easy to manage long-running agent tasks from another device while away from your desk.


If you enable credentials, `ttyd` will require HTTP Basic Auth before opening the terminal.

If `ttyd` is not installed, Control-Terminal now attempts to install the latest ttyd release automatically (Linux only).

If you opt-in to public access, Control-Terminal downloads `cloudflared` automatically (Linux only), starts a Cloudflare Tunnel, and prints a `trycloudflare.com` URL that you can share.

### Preconfigured custom agents

Control-Terminal now supports a separate preconfigured agent file so you can select reusable custom agents from a menu instead of typing commands each time.

- Default path: `~/.control-terminal/custom-agents.conf`
- Repo fallback: `./custom-agents.conf` (used when the home file does not exist)
- Override path with env var: `CONTROL_TERMINAL_AGENTS_FILE=/path/to/file control-terminal`

Config format:

```
name|command
```

Example:

```
a2a-adk-mcp|adk run --enable-a2a --enable-mcp --agent terminal_orchestrator
```

This repository includes a starter `custom-agents.conf` that already contains an **A2A + ADK + MCP** preset entry you can customize for your environment.

## 💡 Telegram remote control (implemented)

Control-Terminal now supports running prompts from Telegram directly into the selected local agent session (Codex / Claude / custom) through tmux.

### What is implemented

- Optional Telegram setup during startup:
  - bot token input,
  - allowed `chat_id` allowlist.
- Chat commands:
  - `/help` or `/start` — show the command list and basic usage.
  - `/status` — show whether the target tmux session is running.
  - `/tail [n]` — return the latest terminal output lines (default count if `n` is omitted).
  - `/watch [seconds]` — start near real-time output updates at the given interval.
  - `/unwatch` — stop live output updates for the chat.
  - `/interrupt` — send `Ctrl+C` to the running process in the tmux session.
  - `/clear` — clear the terminal screen in the tmux session.
  - `/up` — send the Up arrow key (useful for command history navigation).
  - `/down` — send the Down arrow key.
  - `/enter` — send the Enter key.
  - `/esc` — send the Escape key.
  - `/yes` — send `y` followed by Enter (quick confirmation helper).
  - `/no` — send `n` followed by Enter (quick rejection helper).
  - `/prompt <text>` — send a full prompt/instruction to the active agent session.
  - Plain text messages are also sent as prompts.
- Each prompt is sent to the active tmux session and recent output is sent back to Telegram.
- After `/prompt` or plain text messages, live watch now auto-starts for that chat (2s interval) so you continue getting near real-time updates automatically.
- `/watch` still lets you manually choose the update interval and `/unwatch` stops live push updates.
- You can run in Telegram-only mode (without launching the web terminal).

### Important behavior

If a `control-terminal` tmux session already exists, Control-Terminal asks whether to reuse it or restart it with the newly selected agent. Restart is the default so Telegram prompts target the agent you selected in this run.

### Requirements for custom agent scripts (for example `a2a_adk_mcp_agent.py`)

Your custom agent does **not** need to implement Telegram API handling. Control-Terminal already bridges Telegram messages to your running tmux session.

For a custom script to work reliably, it should behave like a normal interactive terminal app:

- Read prompts from stdin / terminal input.
- Write responses to stdout (plain terminal output).
- Stay running to accept the next prompt (instead of exiting after one message).

In short, the runtime flow is:

`Telegram message -> control-terminal bot loop -> tmux send-keys -> your custom agent process -> tmux output capture -> Telegram reply`
