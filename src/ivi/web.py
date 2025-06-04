from __future__ import annotations

"""Web server exposing real-time IVI updates via WebSocket."""
from fastapi import Form

import asyncio
import os
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .ecosystem import IVIEcosystem
from .events import EventBus
from .database import create_db, User, Interaction
from .firebase_utils import init_firebase, verify_token, save_interaction

app = FastAPI()
bus = EventBus()
SessionLocal = create_db()

eco = IVIEcosystem()
init_firebase(os.getenv("FIREBASE_CRED"))

# Simple dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>IVI Dashboard</title>
    <!-- Add Firebase SDK -->
    <script src="https://www.gstatic.com/firebasejs/9.6.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.0/firebase-auth-compat.js"></script>
    <!-- Add Firebase UI -->
    <script src="https://www.gstatic.com/firebasejs/ui/6.0.1/firebase-ui-auth.js"></script>
    <link type="text/css" rel="stylesheet" href="https://www.gstatic.com/firebasejs/ui/6.0.1/firebase-ui-auth.css" />
</head>
<body>
    <h1>IVI Live Interactions</h1>

    <!-- Firebase UI container -->
    <div id="firebaseui-auth-container"></div>

    <!-- Your existing dashboard content -->
    <div id="dashboard" style="display: none;">
        <div>
            <label>Idea <input id="idea" /></label>
            <label>Description <input id="desc" /></label>
            <button onclick="sendInteraction()">Add Interaction</button>
        </div>
        <div style="margin-top: 1em;">
            <label>Content <input id="content" size="60" /></label>
            <button onclick="evaluate()">Evaluate</button>
        </div>
        <input type="hidden" id="token" />
        <ul id="events"></ul>
    </div>

    <script>
    // Your Firebase configuration - REPLACE with your actual config
    const firebaseConfig = {
        apiKey: "AIzaSyDapKiSdhMrnO4XzwVqOmsp97PQksU9ZKk",
        authDomain: "browse-gpt.firebaseapp.com",
        projectId: "browse-gpt",
        // Add other config values if needed
    };

    // Initialize Firebase
    const app = firebase.initializeApp(firebaseConfig);
    const auth = firebase.auth();

    // Listen for auth state changes
    auth.onAuthStateChanged((user) => {
        if (user) {
            // User is signed in
            document.getElementById('dashboard').style.display = 'block';
            document.getElementById('firebaseui-auth-container').style.display = 'none';
            console.log("User is signed in:", user.uid);
            
            // Get and log the ID token
            user.getIdToken().then(token => {
                console.log("ID Token:", token);
                // Store the token for API calls
                document.getElementById('token').value = token;
                // Set the user for the rest of the app
                window.currentUser = user;
            });
        } else {
            // User is signed out
            document.getElementById('dashboard').style.display = 'none';
            document.getElementById('firebaseui-auth-container').style.display = 'block';
        }
    });

    // Initialize FirebaseUI
    const ui = new firebaseui.auth.AuthUI(auth);
    ui.start('#firebaseui-auth-container', {
        signInOptions: [
            firebase.auth.EmailAuthProvider.PROVIDER_ID,
            // Add other providers as needed
            // firebase.auth.GoogleAuthProvider.PROVIDER_ID,
            // firebase.auth.GithubAuthProvider.PROVIDER_ID,
        ],
        signInSuccessUrl: '/dashboard',
        callbacks: {
            signInSuccessWithAuthResult: function(authResult, redirectUrl) {
                // User successfully signed in.
                // Return type determines whether we continue the redirect automatically
                return false; // We'll handle the redirect manually
            }
        }
    });

    // Global user reference
    let user = null;

    async function login() {
        const token = document.getElementById('token').value;
        const res = await fetch(`/login?token=${encodeURIComponent(token)}`, {
            method: 'POST'
        });
        const data = await res.json();
        if (data.user) {
            user = data.user;
            alert('Login successful!');
        } else {
            alert('Login failed: ' + (data.message || 'Unknown error'));
        }
        return data;
    }

    async function sendInteraction() {
        if (!window.currentUser) return alert('Please sign in first');
        const idea = document.getElementById('idea').value;
        const desc = document.getElementById('desc').value;
        const token = document.getElementById('token').value;
        
        try {
            const response = await fetch('/interactions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': `Bearer ${token}`
                },
                body: new URLSearchParams({
                    idea_id: idea,
                    user: window.currentUser.uid,
                    description: desc
                })
            });
            const result = await response.json();
            console.log('Interaction added:', result);
        } catch (error) {
            console.error('Error adding interaction:', error);
            alert('Failed to add interaction');
        }
    }

    async function evaluate() {
        if (!window.currentUser) return alert('Please sign in first');
        const idea = document.getElementById('idea').value;
        const content = document.getElementById('content').value;
        const token = document.getElementById('token').value;
        
        try {
            const res = await fetch('/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': `Bearer ${token}`
                },
                body: new URLSearchParams({
                    idea_id: idea,
                    content: content,
                    user: window.currentUser.uid
                })
            });
            const data = await res.json();
            alert('Score: ' + data.score);
        } catch (error) {
            console.error('Error evaluating:', error);
            alert('Failed to evaluate');
        }
    }

    // WebSocket connection
    const ws = new WebSocket("ws://" + location.host + "/ws");
    ws.onmessage = (ev) => {
        const data = JSON.parse(ev.data);
        const li = document.createElement('li');
        li.textContent = data.payload.user + ' -> ' + data.payload.idea_id + ' : ' + data.payload.description;
        document.getElementById('events').appendChild(li);
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
        console.log('WebSocket connection closed');
    };
    </script>
</body>
</html>
"""

@app.get("/dashboard")
async def dashboard() -> HTMLResponse:
    return HTMLResponse(DASHBOARD_HTML)


from fastapi import Request, Form

@app.post("/login")
async def login(request: Request, token: str = Form(None)) -> dict:
    # Try to get token from query params if not in form
    if token is None:
        token = request.query_params.get("token")
    
    if not token:
        return {"status": "error", "message": "No token provided"}
        
    uid = verify_token(token)
    if uid is None:
        return {"status": "error", "message": "Invalid token"}
    return {"status": "ok", "user": uid}


@app.post("/interactions")
async def add_interaction(
    idea_id: str = Form(...),
    user: str = Form(...),
    description: str = Form(...)
) -> dict:
    session: Session = SessionLocal()
    
    try:
        # Get or create user
        db_user = session.query(User).filter_by(name=user).first()
        if not db_user:
            db_user = User(name=user)
            session.add(db_user)
            session.commit()
        
        # Create interaction with user relationship
        interaction = Interaction(
            idea_id=idea_id,
            user=db_user,  # Use the User object, not the string
            description=description,
        )
        session.add(interaction)
        session.commit()
        
        # Publish event
        await bus.publish("interaction", {
            "user": user,  # Use the string for the event
            "idea_id": idea_id,
            "description": description
        })
        
        return {"status": "ok"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.post("/evaluate")
async def evaluate(idea_id: str, content: str, user: str | None = None) -> dict:
    """Evaluate content through IVI scoring agents."""
    score = eco.evaluate_content(idea_id, content, user=user)
    return {"score": score}

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