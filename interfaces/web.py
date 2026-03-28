# Lumina by Moonlight Co
# interfaces/web.py - local web dashboard

import os
import sys
import json
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
sys.path.insert(0, os.path.expanduser("~/lumina"))
from config.settings import NAME, VERSION, MAKER
from core.agent import respond, clear_session
from core.brain import detect_mode

HTML = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="UTF-8">
<title>Lumina</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a0f; color: #e0e0e0; font-family: sans-serif; height: 100vh; display: flex; flex-direction: column; }
#header { padding: 16px; background: #111118; border-bottom: 1px solid #222; display: flex; justify-content: space-between; align-items: center; }
#header h1 { color: #ffd700; font-size: 18px; }
#status { font-size: 12px; color: #888; }
#messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
.msg { max-width: 80%; padding: 10px 14px; border-radius: 12px; font-size: 14px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; }
.user { background: #1a1a2e; align-self: flex-end; color: #a0c4ff; }
.assistant { background: #16213e; align-self: flex-start; color: #e0e0e0; }
.agent-name { font-size: 11px; color: #ffd700; margin-bottom: 4px; }
#input-area { padding: 12px; background: #111118; border-top: 1px solid #222; display: flex; gap: 8px; }
#input { flex: 1; background: #1a1a2e; border: 1px solid #333; color: #e0e0e0; padding: 10px 14px; border-radius: 20px; font-size: 14px; outline: none; }
#send { background: #ffd700; color: #000; border: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; cursor: pointer; }
#clear { background: #333; color: #e0e0e0; border: none; padding: 10px 14px; border-radius: 20px; cursor: pointer; font-size: 12px; }
.thinking { color: #666; font-style: italic; font-size: 13px; }
</style>
</head>
<body>
<div id="header">
  <h1>🌙 LUMINA</h1>
  <span id="status">Loading...</span>
</div>
<div id="messages"></div>
<div id="input-area">
  <button id="clear" onclick="clearChat()">New</button>
  <input id="input" placeholder="Message Lumina... (/research /code)" onkeydown="if(event.key==='Enter')send()">
  <button id="send" onclick="send()">Send</button>
</div>
<script>
async function loadStatus() {
  const r = await fetch('/status');
  const d = await r.json();
  document.getElementById('status').textContent = d.brain + ' · v' + d.version;
}

function addMsg(role, text, agent) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  if (agent && role === 'assistant') {
    const n = document.createElement('div');
    n.className = 'agent-name';
    n.textContent = agent;
    div.appendChild(n);
  }
  const t = document.createElement('span');
  t.textContent = text;
  div.appendChild(t);
  document.getElementById('messages').appendChild(div);
  div.scrollIntoView();
  return div;
}

async function send() {
  const input = document.getElementById('input');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  addMsg('user', text);
  const thinking = addMsg('assistant', 'Thinking...', null);
  thinking.classList.add('thinking');
  try {
    const r = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    });
    const d = await r.json();
    thinking.remove();
    addMsg('assistant', d.message, d.agent);
  } catch(e) {
    thinking.textContent = 'Error: ' + e;
  }
}

async function clearChat() {
  await fetch('/clear', {method: 'POST'});
  document.getElementById('messages').innerHTML = '';
}

loadStatus();
</script>
</body>
</html>"""

loop = None

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send_json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/status":
            self.send_json({
                "brain": detect_mode(),
                "version": VERSION,
                "name": NAME
            })
        else:
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if self.path == "/chat":
            message = body.get("message", "")
            future = asyncio.run_coroutine_threadsafe(
                respond(message, "web:main"), loop
            )
            result = future.result(timeout=60)
            self.send_json({
                "message": result["message"],
                "agent": result.get("agent", NAME)
            })

        elif self.path == "/clear":
            clear_session("web:main")
            self.send_json({"ok": True})

def run(port=7860):
    global loop
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"🌙 Lumina Web UI → http://127.0.0.1:{port}")
    server.serve_forever()
