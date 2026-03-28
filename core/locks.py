# Lumina by Moonlight Co
# core/locks.py - session locking to prevent race conditions

import threading
from collections import defaultdict

_locks = defaultdict(threading.Lock)

def get(session_id):
    return _locks[session_id]
