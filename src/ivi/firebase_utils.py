from __future__ import annotations
"""Optional Firebase helpers for the IVI dashboard."""

import os
from typing import Any

try:
    import firebase_admin
    from firebase_admin import credentials, auth, firestore
except Exception:  # pragma: no cover - optional dependency missing
    firebase_admin = None
    credentials = auth = firestore = None  # type: ignore

__all__ = [
    "init_firebase",
    "verify_token",
    "save_interaction",
    "save_evaluation",
]

__all__ = ["init_firebase", "verify_token", "save_interaction"]

_app: firebase_admin.App | None = None


def init_firebase(cred_path: str | None = None) -> None:
    """Initialize firebase app if credentials and library are available."""
    global _app
    if firebase_admin is None:
        return
    if _app is not None:
        return
    cred_file = cred_path or os.getenv("FIREBASE_CRED")
    if not cred_file:
        return
    cred = credentials.Certificate(cred_file)
    _app = firebase_admin.initialize_app(cred)


def verify_token(id_token: str) -> str | None:
    """Verify a Firebase ID token and return the user id."""
    if firebase_admin is None or _app is None:
        return None
    try:
        info = auth.verify_id_token(id_token)
        return info.get("uid")
    except Exception:
        return None


def save_interaction(
    user: str, idea_id: str, description: str, score: float | None = None, balance: float | None = None
) -> None:

def save_interaction(user: str, idea_id: str, description: str) -> None:
    """Store interaction data in Firestore if available."""
    if firebase_admin is None or _app is None:
        return
    db = firestore.client()
    data: dict[str, Any] = {
        "user": user,
        "idea_id": idea_id,
        "description": description,
    }
    if score is not None:
        data["score"] = score
    if balance is not None:
        data["balance"] = balance
    db.collection("interactions").add(data)


def save_evaluation(user: str, idea_id: str, score: float, content: str) -> None:
    """Store evaluation results in Firestore if available."""
    if firebase_admin is None or _app is None:
        return
    db = firestore.client()
    db.collection("evaluations").add(
        {
            "user": user,
            "idea_id": idea_id,
            "content": content,
            "score": score,
        }
    )
    db.collection("interactions").add({
        "user": user,
        "idea_id": idea_id,
        "description": description,
    })

