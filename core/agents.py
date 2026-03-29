# Lumina by Moonlight Co
# core/agents.py - multi-agent routing

import os
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import SYSTEM_PROMPT, NAME, MAKER
from core.skills import list_skills, install, remove

AGENTS = {
    "main": {
        "name": NAME,
        "soul": SYSTEM_PROMPT,
        "session_prefix": "agent:main"
    },
    "researcher": {
        "name": "Scout",
        "soul": (
            f"You are Scout, a research specialist created by {MAKER}.\n"
            "Your job: find information and give thorough answers.\n"
            "Every claim needs to be well-reasoned.\n"
            "Save important findings to memory for other agents to use.\n"
            "You have tools — use them proactively."
        ),
        "session_prefix": "agent:researcher"
    },
    "coder": {
        "name": "Forge",
        "soul": (
            f"You are Forge, a coding specialist created by {MAKER}.\n"
            "You write clean, efficient code.\n"
            "Always explain what the code does after writing it.\n"
            "Use tools to read, write, and run code directly.\n"
            "You have tools — use them proactively."
        ),
        "session_prefix": "agent:coder"
    }
}

def handle_skill_command(user_input):
    """Handle /skills commands. Returns response string or None if not a skill command."""
    text = user_input.strip()

    if text == "/skills":
        skills = list_skills()
        if not skills:
            return "No skills installed. Use `/skill add name` to install one."
        return "Installed skills:\n" + "\n".join(f"• {s}" for s in skills)

    if text.startswith("/skill remove "):
        name = text[len("/skill remove "):].strip()
        return remove(name)

    if text.startswith("/skill add "):
        name = text[len("/skill add "):].strip()
        if not name:
            return "Usage: /skill add skill-name"
        return f"SKILL_ADD:{name}"

    return None

def resolve(user_input):
    if user_input.startswith("/research "):
        return "researcher", user_input[len("/research "):]
    if user_input.startswith("/code "):
        return "coder", user_input[len("/code "):]
    return "main", user_input

def get(agent_id):
    return AGENTS.get(agent_id, AGENTS["main"])

def session_key(agent_id, interface_id):
    agent = get(agent_id)
    return f"{agent['session_prefix']}:{interface_id}"
