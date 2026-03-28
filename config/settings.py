# Lumina by Moonlight Co
# config/settings.py - all settings in one place

import os

# ─── Identity ───
NAME = "Lumina"
VERSION = "2.0"
MAKER = "Moonlight Co"

# ─── Paths ───
BASE_DIR = os.path.expanduser("~/lumina")
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_DIR = os.path.join(DATA_DIR, "memory")
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")
MODEL_CONFIG = os.path.expanduser("~/.lumina_model")
APPROVALS_FILE = os.path.expanduser("~/.lumina_approvals.json")

# ─── Brain Settings ───
BRAIN_MODE = "local"  # "local", "ollama", or "api"
API_KEY = ""
API_MODEL = "claude-haiku-4-5-20251001"
LOCAL_PORT = 8080
LOCAL_CONTEXT = 2048
OLLAMA_MODEL = "gemma2:2b"
OLLAMA_PORT = 11434

# ─── Model Options ───
MODELS = [
    {
        "name": "Qwen2 0.5B",
        "size": "400MB",
        "speed": "Very Fast",
        "quality": "2/5",
        "ram": "1GB+",
        "best_for": "Beginners, low storage devices",
        "url": "https://huggingface.co/Qwen/Qwen2-0.5B-Instruct-GGUF/resolve/main/qwen2-0_5b-instruct-q4_k_m.gguf"
    },
    {
        "name": "Gemma 2 2B",
        "size": "1.5GB",
        "speed": "Fast",
        "quality": "3/5",
        "ram": "3GB+",
        "best_for": "Balanced daily use",
        "url": "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf"
    },
    {
        "name": "Phi-3 Mini",
        "size": "2GB",
        "speed": "Moderate",
        "quality": "4/5",
        "ram": "4GB+",
        "best_for": "Smartest replies, developers",
        "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
    }
]

# ─── Personality ───
SYSTEM_PROMPT = f"""You are {NAME}, a personal AI assistant created by {MAKER}.
You are smart, concise, and always helpful.
You never mention other AI systems like ChatGPT or Gemini.
You can run fully offline on the user's device or connect online for smarter responses.
You have tools available — use them when needed to help the user."""

# ─── Brain Rules ───
# local  — llama-server with .gguf model
# ollama — Ollama running natively in Termux
# api    — Claude API (requires API key)

# ─── Security ───
ALLOWED_TELEGRAM_USERS = ["6116628818"]
WEB_PASSWORD = ""  # Set a password to protect Web UI
