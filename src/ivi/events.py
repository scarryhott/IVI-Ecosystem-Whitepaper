from __future__ import annotations

"""Simple event bus for IVI real-time updates."""

import asyncio
from typing import Any, Callable, List

class EventBus:
    """Basic in-memory event dispatcher."""

    def __init__(self) -> None:
        self.subscribers: List[Callable[[str, Any], Any]] = []

    def subscribe(self, callback: Callable[[str, Any], Any]) -> None:
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[str, Any], Any]) -> None:
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    async def publish(self, event_type: str, payload: Any) -> None:
        for sub in list(self.subscribers):
            try:
                result = sub(event_type, payload)
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                pass
