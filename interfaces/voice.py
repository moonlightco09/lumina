# Lumina by Moonlight Co
# interfaces/voice.py - voice interface using Termux APIs

import os
import sys
import json
import asyncio
import subprocess
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import NAME
from core.agent import respond, clear_session

# ─── Colors ───
R     = "\033[0m"
GOLD  = "\033[93m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
RED   = "\033[91m"
MGNT  = "\033[95m"

def speak(text):
    """Speak text using Termux TTS with deep Jarvis-like voice."""
    clean = text.replace("`", "").replace("*", "").replace("#", "")
    subprocess.run([
        "termux-tts-speak",
        "-l", "en",
        "-r", "0.9",  # steady pace
        "-p", "0.5",  # deep pitch
        clean
    ])

def listen():
    """Listen for speech using Termux speech-to-text."""
    print(f"\n  {CYAN}🎙  Listening...{R}")
    try:
        result = subprocess.run(
            ["termux-speech-to-text"],
            capture_output=True,
            text=True,
            timeout=15
        )
        text = result.stdout.strip()
        if text:
            return text
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"  {RED}STT Error: {e}{R}")
        return None

def check_termux_api():
    """Check if termux-api is installed."""
    result = subprocess.run(
        ["which", "termux-tts-speak"],
        capture_output=True
    )
    return result.returncode == 0

async def voice_loop():
    session_id = "voice:main"
    print(f"\n  {GOLD}{BOLD}🌙 Lumina Voice Mode{R}")
    print(f"  {DIM}Say 'goodbye' or press Ctrl+C to exit{R}")
    print(f"  {DIM}Say 'new session' to clear history{R}\n")
    print(f"  {DIM}{'─' * 38}{R}\n")

    speak(f"Hello, I am {NAME}. How can I help you?")

    while True:
        try:
            print(f"  {DIM}Press Enter to speak...{R}", end="")
            input()

            text = listen()

            if not text:
                print(f"  {RED}Could not hear anything. Try again.{R}")
                speak("Sorry, I did not catch that.")
                continue

            print(f"  {CYAN}{BOLD}You  ›{R}  {text}")

            # Check for exit commands
            lower = text.lower()
            if any(w in lower for w in ["goodbye", "bye", "exit", "quit"]):
                speak(f"Goodbye. Have a great day.")
                print(f"\n  {GOLD}🌙 Goodbye.{R}\n")
                break

            if "new session" in lower:
                clear_session(session_id)
                speak("Session cleared. Starting fresh.")
                continue

            print(f"  {DIM}Thinking...{R}")

            async def on_tool_use(tool_name, tool_input):
                print(f"  {GOLD}🔧 Using: {tool_name}{R}")

            result = await respond(text, session_id, on_tool_use)
            response = result["message"]

            print(f"  {MGNT}{BOLD}Lumina ›{R}  {response}\n")
            print(f"  {DIM}{'─' * 38}{R}")

            speak(response)

        except KeyboardInterrupt:
            speak("Goodbye.")
            print(f"\n  {GOLD}🌙 Goodbye.{R}\n")
            break

def main():
    if not check_termux_api():
        print(f"\n  {RED}termux-api not installed.{R}")
        print(f"  Run: {GOLD}pkg install termux-api{R}")
        print(f"  Then install Termux:API app from F-Droid.\n")
        return

    asyncio.run(voice_loop())

if __name__ == "__main__":
    main()
