# Lumina by Moonlight Co
# interfaces/terminal.py - beautiful terminal UI

import os
import sys
import asyncio
import urllib.request
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import NAME, VERSION, MAKER, MODELS, MODEL_CONFIG, BRAIN_MODE, API_KEY
from core.agent import respond, approve_command, deny_command, clear_session

# ─── Colors ───
R      = "\033[0m"
GOLD   = "\033[93m"
WHITE  = "\033[97m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
MGNT   = "\033[95m"
GREEN  = "\033[92m"
RED    = "\033[91m"

def clear(): os.system("clear")
def space(n=1): print("\n" * (n-1))

def show_banner():
    clear()
    space(2)
    print(f"  {GOLD}{BOLD}🌙  L U M I N A  v{VERSION}{R}")
    space()
    print(f"  {DIM}by {MAKER}  ·  Personal AI Assistant{R}")
    space()
    mode = f"{GREEN}Online (Claude API){R}" if API_KEY else f"{CYAN}Offline (Local Model){R}"
    print(f"  Brain: {mode}")
    space()
    print(f"  {DIM}{'─' * 38}{R}")
    space()

def show_models():
    clear()
    space(2)
    print(f"  {GOLD}{BOLD}Choose Your AI Model{R}")
    space()
    print(f"  {DIM}{'─' * 38}{R}")
    space()
    for i, m in enumerate(MODELS, 1):
        print(f"  {GOLD}{BOLD}[{i}]  {WHITE}{BOLD}{m['name']}{R}")
        space()
        print(f"      {DIM}Size     {R}  {GREEN}{m['size']}{R}")
        print(f"      {DIM}Speed    {R}  {m['speed']}")
        print(f"      {DIM}Quality  {R}  {m['quality']}")
        print(f"      {DIM}RAM      {R}  {m['ram']}")
        print(f"      {DIM}Best for {R}  {m['best_for']}")
        space()
        print(f"  {DIM}{'─' * 38}{R}")
        space()

def download_model(url, name):
    path = os.path.expanduser(f"~/lumina/data/{name}.gguf")
    print(f"\n  {GOLD}Downloading {WHITE}{BOLD}{name}{R}")
    print(f"  {DIM}Please wait. Do not close Termux.{R}\n")

    def progress(count, block_size, total_size):
        if total_size > 0:
            percent = min(int(count * block_size * 100 / total_size), 100)
            filled = percent // 5
            bar = f"{GREEN}{'█' * filled}{DIM}{'░' * (20 - filled)}{R}"
            print(f"\r  [{bar}] {GOLD}{BOLD}{percent}%{R}", end="", flush=True)

    urllib.request.urlretrieve(url, path, reporthook=progress)
    space(2)
    print(f"  {GREEN}{BOLD}✓  Download complete!{R}")
    space()
    return path

def setup_model():
    if os.path.exists(MODEL_CONFIG):
        with open(MODEL_CONFIG) as f:
            path = f.read().strip()
        if os.path.exists(path):
            return path

    show_banner()
    print(f"  {WHITE}Are you a new user? {DIM}(yes / no){R}  ", end="")
    answer = input().strip().lower()

    if answer == "yes":
        show_models()
        print(f"  {GOLD}Enter choice {DIM}(1-{len(MODELS)}){R}  ", end="")
        while True:
            try:
                choice = int(input().strip()) - 1
                if 0 <= choice < len(MODELS):
                    break
                print(f"  {RED}Invalid choice. Try again:{R}  ", end="")
            except ValueError:
                print(f"  {RED}Please enter a number:{R}  ", end="")
        model = MODELS[choice]
        path = download_model(model["url"], model["name"])
    else:
        space()
        print(f"  {WHITE}Enter full path to your .gguf model:{R}  ", end="")
        path = input().strip()

    with open(MODEL_CONFIG, "w") as f:
        f.write(path)
    return path

async def chat():
    session_id = "terminal:main"
    pending_approval = None

    show_banner()
    print(f"  {DIM}Type your message. Commands: /new /clear /quit{R}")
    space()
    print(f"  {DIM}{'─' * 38}{R}")

    while True:
        space()
        print(f"  {CYAN}{BOLD}You  ›{R}  ", end="")

        try:
            user_input = input().strip()
        except (EOFError, KeyboardInterrupt):
            space()
            print(f"  {GOLD}🌙  Goodbye.{R}")
            space()
            break

        if not user_input:
            continue

        if user_input.lower() == "/quit":
            space()
            print(f"  {GOLD}🌙  Goodbye.{R}")
            space()
            break

        if user_input.lower() == "/new":
            clear_session(session_id)
            show_banner()
            print(f"  {DIM}Session cleared. Start fresh!{R}")
            space()
            print(f"  {DIM}{'─' * 38}{R}")
            continue

        if user_input.lower() == "/clear":
            show_banner()
            continue

        if user_input.lower() == "/approve" and pending_approval:
            result = await approve_command(pending_approval, session_id)
            pending_approval = None
            space()
            print(f"  {DIM}{'─' * 38}{R}")
            space()
            print(f"  {MGNT}{BOLD}Lumina  ›{R}  {WHITE}✅ Done:\n{result}{R}")
            space()
            print(f"  {DIM}{'─' * 38}{R}")
            continue

        if user_input.lower() == "/deny" and pending_approval:
            await deny_command(pending_approval, session_id)
            pending_approval = None
            space()
            print(f"  {RED}❌ Command denied.{R}")
            continue

        space()
        print(f"  {DIM}Lumina is thinking...{R}")

        async def on_tool_use(tool_name, tool_input):
            print(f"  {GOLD}🔧 Using: {tool_name}{R}")

        result = await respond(user_input, session_id, on_tool_use)

        space()
        print(f"  {DIM}{'─' * 38}{R}")
        space()

        if result["type"] == "needs_approval":
            pending_approval = result["command"]
            print(f"  {MGNT}{BOLD}Lumina  ›{R}  {WHITE}{result['message']}{R}")
        else:
            print(f"  {MGNT}{BOLD}Lumina  ›{R}  {WHITE}{result['message']}{R}")

        space()
        print(f"  {DIM}{'─' * 38}{R}")

def main():
    setup_model()
    asyncio.run(chat())

if __name__ == "__main__":
    main()
