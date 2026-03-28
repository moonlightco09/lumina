# Lumina by Moonlight Co
# core/compact.py - smart context compaction via summarization

import os
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from core import session
from core.memory import save as save_memory

def estimate_tokens(messages):
    import json
    return sum(len(json.dumps(m)) for m in messages) // 4

async def compact(session_id, brain_module, max_tokens=3000):
    messages = session.load(session_id)

    if estimate_tokens(messages) <= max_tokens:
        return messages

    split = len(messages) // 2
    old = messages[:split]
    recent = messages[split:]

    # Build summary using brain
    import json
    history_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}"
        for m in old
        if isinstance(m.get('content'), str)
    )

    summary_messages = [{
        "role": "user",
        "content": (
            "Summarize this conversation concisely. Preserve:\n"
            "- Key facts about the user\n"
            "- Important decisions made\n"
            "- Open tasks or TODOs\n\n"
            f"{history_text}"
        )
    }]

    summary, _ = await brain_module.think(summary_messages)

    # Save to long-term memory too
    save_memory(f"compact-{session_id}", summary)

    # Replace old messages with summary
    new_messages = [
        {"role": "user", "content": f"[Earlier conversation summary: {summary}]"}
    ] + recent

    session.save(session_id, new_messages)
    return new_messages
