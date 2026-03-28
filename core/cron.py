# Lumina by Moonlight Co
# core/cron.py - scheduled heartbeat tasks

import os
import sys
import threading
import time
sys.path.insert(0, os.path.expanduser("~/lumina"))

_jobs = []
_running = False
_thread = None

def every(seconds, func):
    _jobs.append({"interval": seconds, "func": func, "last": 0})

def _loop():
    while _running:
        now = time.time()
        for job in _jobs:
            if now - job["last"] >= job["interval"]:
                job["last"] = now
                try:
                    job["func"]()
                except Exception as e:
                    print(f"[cron] Error: {e}")
        time.sleep(5)

def start():
    global _running, _thread
    if _running:
        return
    _running = True
    _thread = threading.Thread(target=_loop, daemon=True)
    _thread.start()

def stop():
    global _running
    _running = False
