# Lumina by Moonlight Co
# core/session.py - conversation history management

import os
import json
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import SESSIONS_DIR

def get_session_path(session_id):
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    safe_id = session_id.replace(":", "_").replace("/", "_")
    return os.path.join(SESSIONS_DIR, f"{safe_id}.jsonl")

def load(session_id):
    path = get_session_path(session_id)
    messages = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return messages

def append(session_id, role, content):
    path = get_session_path(session_id)
    with open(path, "a") as f:
        f.write(json.dumps({"role": role, "content": content}) + "\n")

def save(session_id, messages):
    path = get_session_path(session_id)
    with open(path, "w") as f:
        for msg in messages:
            f.write(json.dumps(msg) + "\n")

def clear(session_id):
    path = get_session_path(session_id)
    if os.path.exists(path):
        os.remove(path)

def estimate_tokens(messages):
    return sum(len(json.dumps(m)) for m in messages) // 4
