# Lumina by Moonlight Co
# core/memory.py - long term memory management

import os
import json
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import MEMORY_DIR

def save(key, content):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    path = os.path.join(MEMORY_DIR, f"{key}.md")
    with open(path, "w") as f:
        f.write(content)
    return f"Saved memory: {key}"

def search(query):
    query = query.lower()
    results = []
    if os.path.exists(MEMORY_DIR):
        for fname in os.listdir(MEMORY_DIR):
            if fname.endswith(".md"):
                with open(os.path.join(MEMORY_DIR, fname)) as f:
                    content = f.read()
                if any(w in content.lower() for w in query.split()):
                    results.append(f"--- {fname} ---\n{content}")
    return "\n\n".join(results) if results else "No memories found."

def get_all():
    memories = {}
    if os.path.exists(MEMORY_DIR):
        for fname in os.listdir(MEMORY_DIR):
            if fname.endswith(".md"):
                key = fname.replace(".md", "")
                with open(os.path.join(MEMORY_DIR, fname)) as f:
                    memories[key] = f.read()
    return memories

def delete(key):
    path = os.path.join(MEMORY_DIR, f"{key}.md")
    if os.path.exists(path):
        os.remove(path)
        return f"Deleted memory: {key}"
    return f"Memory not found: {key}"

def clear_all():
    if os.path.exists(MEMORY_DIR):
        for fname in os.listdir(MEMORY_DIR):
            if fname.endswith(".md"):
                os.remove(os.path.join(MEMORY_DIR, fname))
    return "All memories cleared."
