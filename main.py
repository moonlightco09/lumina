#!/usr/bin/env python3
# Lumina by Moonlight Co
# main.py - entry point

import os
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from core.setup import is_first_run, run_setup
from config.settings import NAME, VERSION, MAKER
from core import cron

R    = "\033[0m"
GOLD = "\033[93m"
BOLD = "\033[1m"
DIM  = "\033[2m"
CYAN = "\033[96m"

def show_menu():
    os.system("clear")
    print(f"\n  {GOLD}{BOLD}🌙  L U M I N A  v{VERSION}{R}")
    print(f"  {DIM}by {MAKER}{R}\n")
    print(f"  {GOLD}[1]{R}  Terminal Chat")
    print(f"  {GOLD}[2]{R}  Voice Mode")
    print(f"  {GOLD}[3]{R}  Telegram Bot")
    print(f"  {GOLD}[4]{R}  Web UI")
    print(f"  {GOLD}[5]{R}  Settings")
    print(f"  {GOLD}[6]{R}  Quit\n")
    print(f"  {DIM}{'─' * 30}{R}\n")
    print(f"  {CYAN}Choose:{R} ", end="")

def settings_menu():
    from config import settings
    os.system("clear")
    print(f"\n  {GOLD}{BOLD}⚙️  Settings{R}\n")
    print(f"  {DIM}{'─' * 30}{R}\n")
    print(f"  Brain mode : {settings.BRAIN_MODE}")
    print(f"  API key    : {'Set ✅' if settings.API_KEY else 'Not set ❌'}")
    print(f"  Telegram   : {'Locked ✅' if settings.ALLOWED_TELEGRAM_USERS else 'Open ⚠️'}")
    print(f"  Web UI     : {'Password set ✅' if settings.WEB_PASSWORD else 'No password ⚠️'}")
    print(f"  Model      : {open(settings.MODEL_CONFIG).read().strip() if os.path.exists(settings.MODEL_CONFIG) else 'Not selected'}")
    print(f"\n  {DIM}{'─' * 30}{R}\n")
    print(f"  {GOLD}[1]{R}  Re-run setup wizard")
    print(f"  {GOLD}[2]{R}  Back\n")
    print(f"  {CYAN}Choose:{R} ", end="")

    choice = input().strip()
    if choice == "1":
        run_setup()

def main():
    if is_first_run():
        run_setup()

    cron.start()

    while True:
        show_menu()
        choice = input().strip()

        if choice == "1":
            from interfaces.terminal import main as terminal_main
            terminal_main()

        elif choice == "2":
            from interfaces.voice import main as voice_main
            voice_main()

        elif choice == "3":
            print(f"\n  Enter Telegram bot token: ", end="")
            token = input().strip()
            from interfaces.telegram import run
            run(token)

        elif choice == "4":
            from interfaces.web import run as web_run
            web_run()

        elif choice == "5":
            settings_menu()

        elif choice == "6":
            cron.stop()
            print(f"\n  {GOLD}🌙 Goodbye!{R}\n")
            break

if __name__ == "__main__":
    main()
