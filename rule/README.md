Here’s the idea in plain terms:

* **tmux** keeps your terminal session alive on the PC/server even if you disconnect.
* **ttyd** exposes that terminal in a **web browser**, so you can open it from your phone.

So you “touch the PC one time” to start tmux + ttyd, and after that you can control everything from mobile/web.

---

## How it works (the flow)

1. You SSH into your machine (or open terminal locally) **once**.
2. You `cd` into your project folder and start **tmux**.
3. Inside tmux you run your agent/commands (Claude Code, Codex CLI, build, etc.).
4. You start **ttyd** to show a terminal in the browser.
5. From your phone: open `http://YOUR_IP:PORT` → you see the terminal → you attach to tmux and continue.

Even if you close the browser, tmux session is still running on the machine.

---

## Setup on Linux (recommended)

### 1) Install tmux + ttyd

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y tmux
```

For `ttyd`, many distros have it, otherwise install via package/release.
If apt has it:

```bash
sudo apt install -y ttyd
```

Check:

```bash
tmux -V
ttyd -v
```

### 2) Start a tmux session inside your project folder

```bash
cd /path/to/your/project
tmux new -s agent
```

Now you are “inside tmux”.

Run whatever you want:

```bash
claude
# or
codex
# or
npm run dev
```

Detach from tmux (session keeps running):

* Press: `Ctrl + b` then `d`

### 3) Start ttyd (web terminal)

Run:

```bash
ttyd -p 7681 bash
```

Now your web terminal is live at:

* `http://YOUR_SERVER_IP:7681`

### 4) From mobile browser: attach to your tmux session

In the web terminal, run:

```bash
tmux attach -t agent
```

You’re now seeing the **same** running terminal session from your phone.

---

## “Open terminal inside any folder”

Two ways:

### Option A (manual, simple)

Open ttyd, then:

```bash
cd /path/to/folder
tmux attach -t agent
```

### Option B (force default folder for ttyd)

Start ttyd with working directory:

```bash
ttyd -p 7681 -w /path/to/your/project bash
```

So it always opens in that folder.

---

## Make it “touch PC only once” (run ttyd in background)

Simple background run:

```bash
nohup ttyd -p 7681 bash >/tmp/ttyd.log 2>&1 &
```

Even after logout/reboot, you’ll want systemd (best):

Create service:

```bash
sudo tee /etc/systemd/system/ttyd.service >/dev/null <<'EOF'
[Unit]
Description=ttyd Web Terminal
After=network.target

[Service]
ExecStart=/usr/bin/ttyd -p 7681 -w /path/to/your/project bash
Restart=always
User=root
WorkingDirectory=/path/to/your/project

[Install]
WantedBy=multi-user.target
EOF
```

Enable + start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ttyd
sudo systemctl status ttyd
```

---

## Security (VERY important)

If you expose ttyd publicly, anyone can try to access your terminal.

Use at least one of these:

### Best: Put it behind a private network (Tailscale / WireGuard)

Then ttyd isn’t public internet.

### Or: Add authentication in ttyd

Example:

```bash
ttyd -p 7681 -c username:password bash
```

### Or: Put behind Nginx reverse proxy with HTTPS + basic auth

(If you already have Nginx + domain, this is clean.)

---

## Windows note

On Windows, the easiest is:

* run this on **WSL (Ubuntu)** or on a **VPS/Linux server**.
  Because tmux + ttyd are native Linux tools.

---

If you tell me your environment:

1. **VPS Linux** or **your PC**?
2. If PC: **Windows + WSL** or pure Linux?

…I’ll give you the exact commands for your case (including domain + HTTPS if you want to open it via `terminal.yourdomain.com`).
