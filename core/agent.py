# Lumina by Moonlight Co
# core/agent.py - the broker between user and brain

import os
import sys
sys.path.insert(0, os.path.expanduser("~/lumina"))
from core import session, brain, locks
from config.settings import NAME

# ─── Main Agent Function ───

async def respond(user_input, session_id="default", on_tool_use=None):
    with locks.get(session_id):
        messages = session.load(session_id)
        session.append(session_id, "user", user_input)
        messages.append({"role": "user", "content": user_input})

        response, tools_used = await brain.think(
            messages,
            on_tool_use=on_tool_use
        )

        if str(response).startswith("NEEDS_APPROVAL:"):
            cmd = response.split(":", 1)[1]
            session.append(session_id, "assistant", f"Needs approval for: {cmd}")
            return {
                "type": "needs_approval",
                "command": cmd,
                "message": f"⚠️ I need permission to run:\n`{cmd}`\n\nReply /approve to allow or /deny to block."
            }

        session.append(session_id, "assistant", response)
        return {
            "type": "response",
            "message": response,
            "tools_used": tools_used
        }

async def approve_command(command, session_id="default"):
    from core.tools import save_approval, execute
    save_approval(command, True)
    result = execute("run_command", {"command": command})
    session.append(session_id, "assistant", f"Executed: {command}\nResult: {result}")
    return result

async def deny_command(command, session_id="default"):
    from core.tools import save_approval
    save_approval(command, False)
    session.append(session_id, "assistant", f"Denied command: {command}")
    return "Command denied and blocked."

def clear_session(session_id="default"):
    session.clear(session_id)
    return "Session cleared."
