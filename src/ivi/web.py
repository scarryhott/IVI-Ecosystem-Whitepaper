from __future__ import annotations

"""Web server exposing real-time IVI updates via WebSocket."""

import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .ecosystem import IVIEcosystem
from .events import EventBus
from .database import create_db, User, Interaction

app = FastAPI()
bus = EventBus()
SessionLocal = create_db()

eco = IVIEcosystem()

# Simple dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head><title>IVI Dashboard</title></head>
<body>
<h1>IVI Live Interactions</h1>
<ul id="events"></ul>
<script>
const ws = new WebSocket("ws://" + location.host + "/ws");
ws.onmessage = (ev) => {
  const data = JSON.parse(ev.data);
  const li = document.createElement('li');
  li.textContent = data.payload.user + ' -> ' + data.payload.idea_id + ' : ' + data.payload.description;
  document.getElementById('events').appendChild(li);
};
</script>
</body>
</html>
"""

@app.get("/dashboard")
async def dashboard() -> HTMLResponse:
    return HTMLResponse(DASHBOARD_HTML)

@app.post("/interactions")
async def add_interaction(idea_id: str, user: str, description: str) -> dict:
    session: Session = SessionLocal()
    db_user = session.query(User).filter_by(name=user).first()
    if not db_user:
        db_user = User(name=user)
        session.add(db_user)
        session.commit()
    interaction = Interaction(user=db_user, idea_id=idea_id, description=description)
    session.add(interaction)
    session.commit()
    session.close()

    eco.add_interaction(idea_id, user=user, tags=["note"], description=description)
    await bus.publish("interaction", {"user": user, "idea_id": idea_id, "description": description})
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue()

    def handler(event: str, payload: dict) -> None:
        queue.put_nowait({"type": event, "payload": payload})

    bus.subscribe(handler)
    try:
        while True:
            data = await queue.get()
            await websocket.send_json(data)
    except Exception:
        pass
    finally:
        bus.unsubscribe(handler)
        await websocket.close()
