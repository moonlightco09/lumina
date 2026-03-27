# Lumina by Moonlight Co
# core/brain.py - LLM handler (local + API)

import os
import json
import time
import subprocess
import urllib.request
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import (
    SYSTEM_PROMPT, BRAIN_MODE, API_KEY,
    API_MODEL, LOCAL_PORT, LOCAL_CONTEXT
)
from core.tools import SCHEMAS, execute

server_process = None

def start_local():
    global server_process
    if server_process and server_process.poll() is None:
        return
    model_path = open(os.path.expanduser("~/.lumina_model")).read().strip()
    server_process = subprocess.Popen(
        [
            "llama-server",
            "-m", model_path,
            "--port", str(LOCAL_PORT),
            "-c", str(LOCAL_CONTEXT),
            "--log-disable"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(6)

def stop_local():
    global server_process
    if server_process:
        server_process.terminate()
        server_process = None

def ask_local(messages):
    prompt = f"{SYSTEM_PROMPT}\n\n"
    for msg in messages:
        role = "You" if msg["role"] == "user" else "Lumina"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "Lumina:"

    data = json.dumps({
        "prompt": prompt,
        "n_predict": 200,
        "temperature": 0.7,
        "stop": ["You:", "\nYou:"]
    }).encode()

    req = urllib.request.Request(
        f"http://localhost:{LOCAL_PORT}/completion",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as res:
        result = json.loads(res.read())
        return result["content"].strip()

def ask_api(messages):
    data = json.dumps({
        "model": API_MODEL,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "tools": SCHEMAS,
        "messages": messages
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read())

async def think(messages, on_tool_use=None):
    mode = "api" if API_KEY else "local"

    if mode == "local":
        start_local()
        try:
            response = ask_local(messages)
        except Exception as e:
            stop_local()
            return f"Error: {e}", []
        stop_local()
        return response, []

    tool_calls = []
    for _ in range(10):
        response = ask_api(messages)
        content = response.get("content", [])
        stop_reason = response.get("stop_reason", "")

        if stop_reason == "end_turn":
            text = ""
            for block in content:
                if block.get("type") == "text":
                    text += block["text"]
            return text, tool_calls

        if stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": content})
            tool_results = []
            for block in content:
                if block.get("type") == "tool_use":
                    tool_name = block["name"]
                    tool_input = block["input"]
                    tool_calls.append(tool_name)
                    if on_tool_use:
                        await on_tool_use(tool_name, tool_input)
                    result = execute(tool_name, tool_input)
                    if str(result).startswith("NEEDS_APPROVAL:"):
                        return result, tool_calls
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block["id"],
                        "content": str(result)
                    })
            messages.append({"role": "user", "content": tool_results})

    return "Max thinking steps reached.", []
