# 🌙 Lumina

**Your personal AI assistant. Runs on Android. No cloud required.**

Built by [Moonlight Co](https://github.com/moonlightco09)

---

## What is Lumina?

Lumina is a fully offline-capable AI assistant that runs natively on Android via Termux. No PC, no server, no subscription required. Just your phone.

It can think, remember, use tools, run commands on your device, and talk to you — all locally.

---

## Features

- 🧠 **Three brain modes** — Claude API, Ollama (local), or llama-server (gguf)
- 🎙️ **Voice Mode** — speak to Lumina, it speaks back
- 💬 **Terminal Chat** — clean text interface in Termux
- 🌐 **Web UI** — browser dashboard at `127.0.0.1:7860`
- 🤖 **Telegram Bot** — use Lumina from Telegram
- 🧩 **Multi-agent** — Lumina (main), Scout (research), Forge (coding)
- 🔧 **Tools** — run commands, read/write files, search memory
- 🔒 **Permission system** — approves dangerous commands before running
- 💾 **Long-term memory** — remembers things across sessions
- 📦 **Context compaction** — never loses conversation history
- ⏰ **Cron/heartbeats** — scheduled background tasks
- 🔐 **Security** — Telegram allowlist, Web UI password

---

## Requirements

- Android phone (Android 10+)
- Termux from F-Droid
- Python 3.x
- termux-api package + Termux:API app (for Voice Mode)

---

## Installation

```bash
# 1. Install dependencies
pkg update && pkg install python git

# 2. Clone Lumina
git clone https://github.com/moonlightco09/lumina ~/lumina

# 3. Install Python packages
pip install python-telegram-bot

# 4. Run Lumina
cd ~/lumina && python main.py
First run launches the setup wizard automatically.
Setup Wizard
On first run, Lumina asks you:
Your Telegram user ID (get from @userinfobot)
Web UI password (optional)
Claude API key (optional — leave empty for offline mode)
Your personal config is saved to config/local.py which is never committed to git.
Brain Modes
Mode
How it works
Requires
api
Claude API (smartest)
API key
ollama
Ollama running in Termux
pkg install ollama
local
llama-server + .gguf model
llama.cpp + model file
Lumina auto-detects which brain to use.
Voice Mode
pkg install termux-api
Also install Termux:API app from F-Droid. Then choose [2] Voice Mode from the menu.
Agent Commands
Command
Agent
Specialty
(normal message)
Lumina
General assistant
/research query
Scout
Research & information
/code task
Forge
Coding & scripting
Telegram Bot
Create a bot via @BotFather on Telegram
Copy the token
Choose [3] Telegram Bot from Lumina menu
Paste the token
Web UI
Choose [4] Web UI from the menu, then open http://127.0.0.1:7860
Project Structure
lumina/
├── main.py
├── config/
│   ├── settings.py
│   ├── local.py        ← your personal config (not in git)
│   └── soul.md
├── core/
│   ├── agent.py
│   ├── brain.py
│   ├── tools.py
│   ├── memory.py
│   ├── session.py
│   ├── compact.py
│   ├── locks.py
│   ├── cron.py
│   ├── agents.py
│   └── setup.py
└── interfaces/
    ├── terminal.py
    ├── voice.py
    ├── telegram.py
    └── web.py
License
MIT — free to use, modify, and distribute.
Made with 🌙 by Moonlight Co
