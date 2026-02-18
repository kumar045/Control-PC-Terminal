# Control-PC-Terminal 🚀

**Control your Desktop AI Agents from anywhere—via Telegram or Web Terminal.**

🎥 **[Watch the Demo Video](https://youtube.com/shorts/iV7oRx2TbOc?si=j56mWWIJBJ_7PC8x)**

**Control-PC-Terminal** is an open-source tool that lets you control **Claude Code**, **Codex**, or **any custom CLI agent** running on your Desktop or VPS directly from your mobile phone.

Unlike standard remote tools, this is built for **AI Agent persistence**. Your agents run inside `tmux` sessions, so they keep working even if your internet drops. You can interact with them via a **Secure Web Terminal** or a **Telegram Bot** that streams logs and sends commands in real-time.

---

## ✨ Key Features

### 1. 📱 Telegram Remote Control (New!)

Chat with your terminal! Control-PC-Terminal bridges Telegram messages directly to your running `tmux` session.

* **Send Prompts:** Message the bot to send text directly to Claude/Codex.
* **Live Streaming:** Use `/watch` to see the agent's output stream to your chat in near real-time.
* **Interrupts:** Stop runaway agents instantly with `/interrupt` (sends `Ctrl+C`).
* **Control:** Use `/up`, `/down`, `/enter`, and `/yes` to navigate menus remotely.

### 2. 💻 Persistent Web Terminal

* **`tmux` Integration:** Your work keeps running on your machine even if your phone browser disconnects or screen locks.
* **`ttyd` Access:** Turns your terminal into a web UI accessible from any browser (`http://localhost:7681`).
* **`cloudflared` Tunnel (Optional):** Generates a secure public URL (e.g., `trycloudflare.com`) so you can access your terminal from outside your home network without router configuration.

---

## 🚀 Install

```bash
curl -fsSL https://raw.githubusercontent.com/kumar045/Control-PC-Terminal/main/install.sh | bash

```

The installer downloads the script and adds `~/.control-terminal/bin` to your PATH.

## 🖥️ OS Support

* **Linux**: Supported directly.
* **Windows**: Use **WSL (Windows Subsystem for Linux)**.

---

## 🧠 Usage

Run the tool:

```bash
control-terminal

```

You will be prompted to select an agent:

1. **codex**
2. **claude**
3. **other**
4. **preconfigured custom agent**

### Telegram Setup

During startup, you can optionally configure Telegram control:

1. Enter your **Bot Token**.
2. Enter your **Chat ID** (for allowlist security).

Once running, the tool will:

* Start the agent in a `tmux` session.
* Launch the Telegram bot (if configured) to listen for commands.
* Expose the session over a web browser via `ttyd`.

### Telegram Commands

| Command | Description |
| --- | --- |
| `/help` | Show command list |
| `/status` | Check if the tmux session is running |
| `/watch [s]` | Stream terminal output to chat (default 2s interval) |
| `/unwatch` | Stop live updates |
| `/tail [n]` | Get the last `n` lines of output |
| `/interrupt` | Send `Ctrl+C` to the agent |
| `/prompt <txt>` | Send a prompt to the agent (or just type text) |
| `/yes` / `/no` | Quick confirmation helpers |
| `/up` / `/down` | Navigate command history/menus |
| `/enter` | Send Enter key |

*Note: If you send a plain text message, it is treated as a prompt and auto-enables `/watch` mode.*

---

## 🧩 Why Control-Terminal is special

Control-Terminal combines three proven tools into one smooth workflow:

1. **`tmux` (The Engine):** Keeps processes alive. If you use only a web terminal, your long-running agent dies when the tab closes. With `tmux`, it runs forever.
2. **`ttyd` (The Web View):** Provides remote browser input/output to that specific `tmux` session.
3. **`cloudflared` (The Access):** Gives you a shareable URL quickly, without manual router/NAT setup.

## ⚙️ Advanced Configuration

### Preconfigured Custom Agents

You can define reusable agents in a config file so you don't have to type commands every time.

* **File location:** `~/.control-terminal/custom-agents.conf`
* **Format:** `name|command`

**Example:**

```text
a2a-adk-mcp|adk run --enable-a2a --enable-mcp --agent terminal_orchestrator

```

### Credentials & Security

* **Web Auth:** You can set a username/password for `ttyd` access during startup.
* **Telegram Auth:** The bot only responds to the `chat_id` you provide.

### Custom Script Requirements

If you are writing your own agent script (e.g., `my_agent.py`) to use with this:

1. Read from **stdin** (terminal input).
2. Write to **stdout** (terminal output).
3. Keep running (don't exit after one output).

*Control-Terminal handles the bridging between Telegram/Web and your script automatically.*
