# Lumina by Moonlight Co
# core/setup.py - first run setup wizard

import os
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))

LOCAL_CONFIG = os.path.join(os.path.expanduser("~/lumina"), "config", "local.py")

R    = "\033[0m"
GOLD = "\033[93m"
BOLD = "\033[1m"
DIM  = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"

def is_first_run():
    return not os.path.exists(LOCAL_CONFIG)

def run_setup():
    os.system("clear")
    print(f"\n  {GOLD}{BOLD}🌙  Welcome to Lumina!{R}")
    print(f"  {DIM}First-run setup by Moonlight Co{R}\n")
    print(f"  {DIM}{'─' * 38}{R}\n")
    print(f"  This will create your personal config.")
    print(f"  Your data stays on your device only.\n")
    print(f"  {DIM}{'─' * 38}{R}\n")

    # Telegram user ID
    print(f"  {GOLD}Step 1:{R} Telegram User ID")
    print(f"  {DIM}Message @userinfobot on Telegram to get it.{R}")
    print(f"  {DIM}Leave empty to allow anyone (not recommended).{R}\n")
    print(f"  {CYAN}Your Telegram user ID:{R} ", end="")
    telegram_id = input().strip()

    print()

    # Web password
    print(f"  {GOLD}Step 2:{R} Web UI Password")
    print(f"  {DIM}Protects your dashboard at 127.0.0.1:7860{R}")
    print(f"  {DIM}Leave empty for no password.{R}\n")
    print(f"  {CYAN}Web UI password:{R} ", end="")
    web_password = input().strip()

    print()

    # API key
    print(f"  {GOLD}Step 3:{R} Claude API Key {DIM}(optional){R}")
    print(f"  {DIM}For smarter responses via Claude API.{R}")
    print(f"  {DIM}Leave empty to use local/Ollama model.{R}\n")
    print(f"  {CYAN}Claude API key:{R} ", end="")
    api_key = input().strip()

    # Write local.py
    with open(LOCAL_CONFIG, "w") as f:
        f.write("# Lumina by Moonlight Co\n")
        f.write("# config/local.py - your personal settings\n")
        f.write("# This file is NOT committed to git\n\n")
        f.write(f'TELEGRAM_USER_ID = "{telegram_id}"\n')
        f.write(f'WEB_PASSWORD = "{web_password}"\n')
        f.write(f'API_KEY = "{api_key}"\n')

    print(f"\n  {GREEN}{BOLD}✅ Setup complete!{R}")
    print(f"  {DIM}Config saved to config/local.py{R}\n")
    input(f"  Press Enter to continue...")
