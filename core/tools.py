# Lumina by Moonlight Co
# core/tools.py - all tools in one place

import os
import json
import subprocess
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import APPROVALS_FILE
from core.memory import save as save_memory, search as search_memory

# ─── Tool Schemas (for Claude API) ───

SCHEMAS = [
    {
        "name": "run_command",
        "description": "Run a shell command on the user's Android phone via Termux",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to run"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Read contents of a file from the filesystem",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Full path to the file"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file on the filesystem",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Full path to the file"},
                "content": {"type": "string", "description": "Content to write"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "save_memory",
        "description": "Save important information to long term memory that persists across conversations",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Short label like user-name or preferences"},
                "content": {"type": "string", "description": "The information to remember"}
            },
            "required": ["key", "content"]
        }
    },
    {
        "name": "search_memory",
        "description": "Search long term memory for relevant information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "What to search for"}
            },
            "required": ["query"]
        }
    }
]

# ─── Permission System ───

SAFE_COMMANDS = {
    "ls", "cat", "head", "tail", "wc", "date",
    "whoami", "echo", "pwd", "which", "git",
    "python", "python3", "pip", "pkg"
}

def load_approvals():
    if os.path.exists(APPROVALS_FILE):
        with open(APPROVALS_FILE) as f:
            return json.load(f)
    return {"allowed": [], "denied": []}

def save_approval(command, approved):
    approvals = load_approvals()
    key = "allowed" if approved else "denied"
    if command not in approvals[key]:
        approvals[key].append(command)
    with open(APPROVALS_FILE, "w") as f:
        json.dump(approvals, f, indent=2)

def check_safety(command):
    base = command.strip().split()[0] if command.strip() else ""
    if base in SAFE_COMMANDS:
        return "safe"
    approvals = load_approvals()
    if command in approvals["allowed"]:
        return "approved"
    if command in approvals["denied"]:
        return "denied"
    return "needs_approval"

# ─── Tool Execution ───

def execute(name, tool_input):
    if name == "run_command":
        cmd = tool_input["command"]
        safety = check_safety(cmd)

        if safety == "denied":
            return "Permission denied — this command was previously blocked."

        if safety == "needs_approval":
            return f"NEEDS_APPROVAL:{cmd}"

        try:
            result = subprocess.run(
                cmd, shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout + result.stderr
            return output.strip() if output.strip() else "(no output)"
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds."
        except Exception as e:
            return f"Error: {e}"

    elif name == "read_file":
        try:
            with open(tool_input["path"], "r") as f:
                content = f.read()
            return content[:5000] if len(content) > 5000 else content
        except Exception as e:
            return f"Error reading file: {e}"

    elif name == "write_file":
        try:
            path = tool_input["path"]
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w") as f:
                f.write(tool_input["content"])
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {e}"

    elif name == "save_memory":
        return save_memory(tool_input["key"], tool_input["content"])

    elif name == "search_memory":
        return search_memory(tool_input["query"])

    return f"Unknown tool: {name}"
