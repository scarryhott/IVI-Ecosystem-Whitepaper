from __future__ import annotations

"""Web server exposing real-time IVI updates via WebSocket."""

import asyncio
import os
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .ecosystem import IVIEcosystem
from .events import EventBus
from .database import create_db, User, Interaction
from .firebase_utils import (
    init_firebase,
    verify_token,
    save_interaction,
    save_evaluation,
)

app = FastAPI()
bus = EventBus()
SessionLocal = create_db()

eco = IVIEcosystem()
init_firebase(os.getenv("FIREBASE_CRED"))

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IVI Ecosystem Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .connection-status {
            @apply inline-block w-3 h-3 rounded-full mr-2;
        }
        .connection-status.connected {
            @apply bg-green-500;
        }
        .connection-status.disconnected {
            @apply bg-red-500;
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="min-h-screen">
        <!-- Header -->
        <header class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
                <h1 class="text-2xl font-bold text-gray-900">IVI Ecosystem Dashboard</h1>
                <div class="flex items-center">
                    <div id="connection-status" class="connection-status disconnected"></div>
                    <span id="connection-text" class="text-sm text-gray-500">Disconnected</span>
                    <button id="login-button" class="ml-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Login</button>
                    <div id="user-info" class="hidden ml-4">
                        <span id="user-email" class="text-sm font-medium text-gray-700"></span>
                        <button id="logout-button" class="ml-2 text-sm text-blue-600 hover:text-blue-800">Logout</button>
                    </div>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <!-- Login Form (initially hidden) -->
            <div id="login-form" class="hidden max-w-md mx-auto bg-white p-6 rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-4">Sign In</h2>
                <div id="firebaseui-auth-container"></div>
            </div>

            <!-- Dashboard Content (initially hidden) -->
            <div id="dashboard-content" class="hidden">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Add Interaction -->
                    <div class="bg-white p-6 rounded-lg shadow">
                        <h2 class="text-lg font-medium text-gray-900 mb-4">Add Interaction</h2>
                        <form id="interaction-form" class="space-y-4">
                            <div>
                                <label for="idea" class="block text-sm font-medium text-gray-700">Idea ID</label>
                                <input type="text" id="idea" name="idea" required
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                            </div>
                            <div>
                                <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
                                <textarea id="description" name="description" rows="3" required
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"></textarea>
                            </div>
                            <button type="submit"
                                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                Submit Interaction
                            </button>
                        </form>
                    </div>

                    <!-- Evaluate Content -->
                    <div class="bg-white p-6 rounded-lg shadow">
                        <h2 class="text-lg font-medium text-gray-900 mb-4">Evaluate Content</h2>
                        <form id="evaluate-form" class="space-y-4">
                            <div>
                                <label for="eval-idea" class="block text-sm font-medium text-gray-700">Idea ID</label>
                                <input type="text" id="eval-idea" name="eval-idea" required
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                            </div>
                            <div>
                                <label for="content" class="block text-sm font-medium text-gray-700">Content</label>
                                <textarea id="content" name="content" rows="3" required
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"></textarea>
                            </div>
                            <button type="submit"
                                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                                Evaluate
                            </button>
                        </form>
                        <div id="evaluation-result" class="mt-4 hidden p-4 bg-gray-50 rounded">
                            <h3 class="font-medium text-gray-900">Evaluation Result</h3>
                            <p id="score" class="text-lg font-semibold"></p>
                        </div>
                    </div>
                </div>

                <!-- Live Interactions -->
                <div class="mt-8 bg-white p-6 rounded-lg shadow">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-lg font-medium text-gray-900">Live Interactions</h2>
                        <span id="interaction-count" class="text-sm text-gray-500">0 interactions</span>
                    </div>
                    <div class="overflow-hidden">
                        <ul id="interactions-list" class="divide-y divide-gray-200">
                            <!-- Interactions will be added here -->
                        </ul>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <!-- Firebase and Firebase UI -->
    <script src="https://www.gstatic.com/firebasejs/9.6.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.0/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/ui/6.0.1/firebase-ui-auth.js"></script>
    <link type="text/css" rel="stylesheet" href="https://www.gstatic.com/firebasejs/ui/6.0.1/firebase-ui-auth.css" />

    <script>
        // Firebase configuration
        const firebaseConfig = {
            apiKey: "AIzaSyDapKiSdhMrnO4XzwVqOmsp97PQksU9ZKk",
            authDomain: "browse-gpt.firebaseapp.com",
            projectId: "browse-gpt"
        };

        // Initialize Firebase
        const app = firebase.initializeApp(firebaseConfig);
        const auth = firebase.auth();

        // DOM Elements
        const loginButton = document.getElementById('login-button');
        const logoutButton = document.getElementById('logout-button');
        const loginForm = document.getElementById('login-form');
        const dashboardContent = document.getElementById('dashboard-content');
        const userInfo = document.getElementById('user-info');
        const userEmail = document.getElementById('user-email');
        const connectionStatus = document.getElementById('connection-status');
        const connectionText = document.getElementById('connection-text');
        const interactionForm = document.getElementById('interaction-form');
        const evaluateForm = document.getElementById('evaluate-form');
        const evaluationResult = document.getElementById('evaluation-result');
        const scoreElement = document.getElementById('score');
        const interactionsList = document.getElementById('interactions-list');
        const interactionCount = document.getElementById('interaction-count');
        const firebaseUiContainer = document.getElementById('firebaseui-auth-container');

        // WebSocket connection
        let ws;
        let reconnectAttempts = 0;
        const MAX_RECONNECT_ATTEMPTS = 5;
        const RECONNECT_DELAY = 1000;

        // Track interactions for deduplication
        const seenInteractions = new Set();
        let interactions = [];

        // Initialize Firebase UI
        const ui = new firebaseui.auth.AuthUI(auth);
        const uiConfig = {
            signInOptions: [
                {
                    provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
                    requireDisplayName: false
                }
            ],
            signInSuccessUrl: '/dashboard',
            callbacks: {
                signInSuccessWithAuthResult: function(authResult, redirectUrl) {
                    console.log('Sign in successful:', authResult.user.uid);
                    return false; // Don't redirect, we'll handle it
                },
                uiShown: function() {
                    document.getElementById('loader')?.remove();
                }
            },
            signInFlow: 'popup'
        };

        // Show Firebase UI
        function showFirebaseUI() {
            ui.start('#firebaseui-auth-container', uiConfig);
        }

        // Update connection status
        function updateConnectionStatus(connected) {
            connectionStatus.classList.toggle('connected', connected);
            connectionStatus.classList.toggle('disconnected', !connected);
            connectionText.textContent = connected ? 'Connected' : 'Disconnected';
        }

        // Connect to WebSocket
        function connectWebSocket() {
            if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
                return;
            }

            const wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
            ws = new WebSocket(`${wsScheme}${window.location.host}/ws`);

            ws.onopen = () => {
                console.log('WebSocket connected');
                updateConnectionStatus(true);
                reconnectAttempts = 0;
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.type === 'interaction') {
                        addInteractionToList(data.payload);
                    }
                } catch (e) {
                    console.error('Error processing message:', e);
                }
            };

            ws.onclose = () => {
                console.log('WebSocket disconnected');
                updateConnectionStatus(false);
                
                if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                    const delay = RECONNECT_DELAY * Math.pow(2, reconnectAttempts);
                    console.log(`Reconnecting in ${delay}ms... (Attempt ${reconnectAttempts + 1}/${MAX_RECONNECT_ATTEMPTS})`);
                    setTimeout(connectWebSocket, delay);
                    reconnectAttempts++;
                } else {
                    console.error('Max reconnection attempts reached');
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                ws.close();
            };
        }

        // Add interaction to the list
        function addInteractionToList(interaction) {
            const interactionKey = `${interaction.user}-${interaction.idea_id}-${interaction.timestamp || Date.now()}`;
            
            // Skip if we've already seen this interaction
            if (seenInteractions.has(interactionKey)) {
                return;
            }
            
            seenInteractions.add(interactionKey);
            interactions.unshift(interaction);
            
            // Keep only the last 100 interactions
            if (interactions.length > 100) {
                const removed = interactions.pop();
                if (removed) {
                    const removedKey = `${removed.user}-${removed.idea_id}-${removed.timestamp || 0}`;
                    seenInteractions.delete(removedKey);
                }
            }
            
            updateInteractionsList();
        }

        // Update the interactions list in the DOM
        function updateInteractionsList() {
            // Clear the list
            interactionsList.innerHTML = '';
            
            // Add each interaction
            interactions.forEach(interaction => {
                const li = document.createElement('li');
                li.className = 'py-4';
                li.innerHTML = `
                    <div class="flex space-x-3">
                        <div class="flex-1 space-y-1">
                            <div class="flex items-center justify-between">
                                <h3 class="text-sm font-medium">${interaction.user || 'Anonymous'}</h3>
                                <p class="text-sm text-gray-500">${new Date(interaction.timestamp || Date.now()).toLocaleString()}</p>
                            </div>
                            <p class="text-sm text-gray-900">${interaction.description}</p>
                            <p class="text-xs text-blue-600">Idea: ${interaction.idea_id}</p>
                        </div>
                    </div>
                `;
                interactionsList.appendChild(li);
            });
            
            // Update the count
            interactionCount.textContent = `${interactions.length} interaction${interactions.length !== 1 ? 's' : ''}`;
        }

        // Handle form submission
        async function handleInteractionSubmit(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const idea = formData.get('idea');
            const description = formData.get('description');
            
            if (!idea || !description) {
                alert('Please fill in all fields');
                return;
            }
            
            const button = e.target.querySelector('button[type="submit"]');
            const originalText = button.textContent;
            
            try {
                button.disabled = true;
                button.textContent = 'Sending...';
                
                const token = await auth.currentUser.getIdToken();
                const response = await fetch('/interactions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': `Bearer ${token}`
                    },
                    body: new URLSearchParams({
                        idea_id: idea,
                        user: auth.currentUser.uid,
                        description: description
                    })
                });
                
                if (!response.ok) {
                    const error = await response.json().catch(() => ({}));
                    throw new Error(error.detail || 'Failed to send interaction');
                }
                
                // Clear the form
                e.target.reset();
            } catch (error) {
                console.error('Error sending interaction:', error);
                alert(`Error: ${error.message || 'Failed to send interaction'}`);
            } finally {
                button.disabled = false;
                button.textContent = originalText;
            }
        }

        // Handle evaluation form submission
        async function handleEvaluateSubmit(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const idea = formData.get('eval-idea');
            const content = formData.get('content');
            
            if (!idea || !content) {
                alert('Please fill in all fields');
                return;
            }
            
            const button = e.target.querySelector('button[type="submit"]');
            const originalText = button.textContent;
            
            try {
                button.disabled = true;
                button.textContent = 'Evaluating...';
                
                const token = await auth.currentUser.getIdToken();
                const response = await fetch('/evaluate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': `Bearer ${token}`
                    },
                    body: new URLSearchParams({
                        idea_id: idea,
                        content: content,
                        user: auth.currentUser.uid
                    })
                });
                
                if (!response.ok) {
                    const error = await response.json().catch(() => ({}));
                    throw new Error(error.detail || 'Evaluation failed');
                }
                
                const data = await response.json();
                
                // Show the result
                scoreElement.textContent = `Score: ${data.score}`;
                evaluationResult.classList.remove('hidden');
                
                // Clear the form
                e.target.reset();
            } catch (error) {
                console.error('Error evaluating content:', error);
                alert(`Error: ${error.message || 'Failed to evaluate content'}`);
            } finally {
                button.disabled = false;
                button.textContent = originalText;
            }
        }

        // Handle login/logout
        function updateUI(user) {
            if (user) {
                // User is signed in
                loginButton.classList.add('hidden');
                userInfo.classList.remove('hidden');
                userEmail.textContent = user.email;
                loginForm.classList.add('hidden');
                dashboardContent.classList.remove('hidden');
                
                // Connect to WebSocket
                connectWebSocket();
            } else {
                // User is signed out
                loginButton.classList.remove('hidden');
                userInfo.classList.add('hidden');
                loginForm.classList.remove('hidden');
                dashboardContent.classList.add('hidden');
                
                // Show Firebase UI
                showFirebaseUI();
                
                // Close WebSocket if open
                if (ws) {
                    ws.close();
                }
            }
        }

        // Event listeners
        loginButton.addEventListener('click', () => {
            loginForm.classList.remove('hidden');
            showFirebaseUI();
        });

        logoutButton.addEventListener('click', () => {
            auth.signOut();
        });

        interactionForm.addEventListener('submit', handleInteractionSubmit);
        evaluateForm.addEventListener('submit', handleEvaluateSubmit);

        // Auth state changes
        auth.onAuthStateChanged((user) => {
            updateUI(user);
            
            if (user) {
                // Try to log in to the backend
                user.getIdToken().then(token => {
                    return fetch('/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams({ token })
                    });
                }).then(response => {
                    if (!response.ok) {
                        throw new Error('Backend login failed');
                    }
                    return response.json();
                }).catch(error => {
                    console.error('Login error:', error);
                    auth.signOut();
                });
            }
        });

        // Initialize
        updateUI(auth.currentUser);
    </script>
</body>
</html>
"""

@app.get("/dashboard")
async def dashboard() -> HTMLResponse:
    return HTMLResponse(DASHBOARD_HTML)


from fastapi import Request, Form

@app.post("/login")
async def login(token: str = Form(...)):
    try:
        # Verify the Firebase ID token
        decoded_token = verify_token(token)
        if not decoded_token:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        # Get the user's Firebase UID
        uid = decoded_token.get('uid')
        if not uid:
            raise HTTPException(status_code=401, detail="Invalid user ID in token")
        
        # Get or create the user in your database
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.firebase_uid == uid).first()
            if not user:
                # Create new user if they don't exist
                user = User(firebase_uid=uid, email=decoded_token.get('email', ''))
                db.add(user)
                db.commit()
                db.refresh(user)
            
            return {"status": "success", "user_id": user.id}
        finally:
            db.close()
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    score = eco.overall_score(idea_id)
    balance = eco.ledger.balance_of(user)
    save_interaction(user, idea_id, description, score=score, balance=balance)

    eco.add_interaction(idea_id, user=user, tags=["note"], description=description)
    await bus.publish("interaction", {"user": user, "idea_id": idea_id, "description": description})
    return {"status": "ok"}


@app.post("/evaluate")
async def evaluate(idea_id: str, content: str, user: str | None = None) -> dict:
    """Evaluate content through IVI scoring agents."""
    score = eco.evaluate_content(idea_id, content, user=user)
    if user:
        save_evaluation(user, idea_id, score, content)
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
