# Lumina by Moonlight Co
# core/skills.py - skill system

import os
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))

SKILLS_DIR = os.path.join(os.path.expanduser("~/lumina"), "skills")

def load_all():
    """Load all skill markdown files and return as combined text."""
    skills = []
    if not os.path.exists(SKILLS_DIR):
        return ""
    for fname in sorted(os.listdir(SKILLS_DIR)):
        if fname.endswith(".md"):
            path = os.path.join(SKILLS_DIR, fname)
            with open(path, "r") as f:
                content = f.read().strip()
            if content:
                skills.append(f"## Skill: {fname.replace('.md','')}\n{content}")
    return "\n\n".join(skills)

def list_skills():
    """Return list of installed skill names."""
    if not os.path.exists(SKILLS_DIR):
        return []
    return [f.replace(".md","") for f in os.listdir(SKILLS_DIR) if f.endswith(".md")]

def install(name, content):
    """Install a new skill."""
    os.makedirs(SKILLS_DIR, exist_ok=True)
    path = os.path.join(SKILLS_DIR, f"{name}.md")
    with open(path, "w") as f:
        f.write(content)
    return f"Skill '{name}' installed."

def remove(name):
    """Remove a skill."""
    path = os.path.join(SKILLS_DIR, f"{name}.md")
    if os.path.exists(path):
        os.remove(path)
        return f"Skill '{name}' removed."
    return f"Skill '{name}' not found."
