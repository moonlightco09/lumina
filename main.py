#!/usr/bin/env python3
# Lumina by Moonlight Co
# main.py - entry point

import os
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import NAME, VERSION, MAKER

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
    print(f"  {GOLD}[2]{R}  Telegram Bot")
    print(f"  {GOLD}[3]{R}  Settings")
    print(f"  {GOLD}[4]{R}  Quit\n")
    print(f"  {DIM}{'─' * 30}{R}\n")
    print(f"  {CYAN}Choose:{R} ", end="")

def settings_menu():
    from config import settings
    os.system("clear")
    print(f"\n  {GOLD}{BOLD}⚙️  Settings{R}\n")
    print(f"  {DIM}{'─' * 30}{R}\n")
    print(f"  Brain mode : {settings.BRAIN_MODE}")
    print(f"  API key    : {'Set ✅' if settings.API_KEY else 'Not set ❌'}")
    print(f"  Model      : {open(settings.MODEL_CONFIG).read().strip() if os.path.exists(settings.MODEL_CONFIG) else 'Not selected'}")
    print(f"\n  {DIM}{'─' * 30}{R}\n")
    print(f"  {GOLD}[1]{R}  Set Claude API key")
    print(f"  {GOLD}[2]{R}  Switch brain mode")
    print(f"  {GOLD}[3]{R}  Back\n")
    print(f"  {CYAN}Choose:{R} ", end="")

    choice = input().strip()
    if choice == "1":
        print(f"\n  Enter Claude API key: ", end="")
        key = input().strip()
        settings.API_KEY = key
        print(f"  ✅ API key set for this session.")
        input("\n  Press Enter to continue...")
    elif choice == "2":
        current = settings.BRAIN_MODE
        new_mode = "api" if current == "local" else "local"
        settings.BRAIN_MODE = new_mode
        print(f"\n  ✅ Brain mode switched to: {new_mode}")
        input("\n  Press Enter to continue...")

def main():
    while True:
        show_menu()
        choice = input().strip()

        if choice == "1":
            from interfaces.terminal import main as terminal_main
            terminal_main()

        elif choice == "2":
            print(f"\n  Enter Telegram bot token: ", end="")
            token = input().strip()
            from interfaces.telegram import run
            run(token)

        elif choice == "3":
            settings_menu()

        elif choice == "4":
            print(f"\n  {GOLD}🌙 Goodbye!{R}\n")
            break

if __name__ == "__main__":
    main()
