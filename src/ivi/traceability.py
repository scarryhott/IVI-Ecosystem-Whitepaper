"""Contextual Traceability utilities for Intangibly Verified Information (IVI).

This module defines simple data structures and functions to track the origin and
context of ideas. These serve as a lightweight demonstration of how IVI might
record contextual provenance without relying on traditional, authority-based
verification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class OriginEvent:
    """Represents a single event in an idea's journey."""

    actor: str
    timestamp: datetime
    description: str
    related_idea: Optional[str] = None


@dataclass
class IdeaTrace:
    """Tracks the contextual journey of an idea."""

    idea_id: str
    events: List[OriginEvent] = field(default_factory=list)

    def add_event(self, actor: str, description: str, related_idea: Optional[str] = None) -> None:
        self.events.append(
            OriginEvent(
                actor=actor,
                timestamp=datetime.now(timezone.utc),
                description=description,
                related_idea=related_idea,
            )
        )

    def origin_map(self) -> List[str]:
        """Return a simple textual representation of the idea's path."""
        return [f"{e.timestamp.isoformat()} | {e.actor}: {e.description}" for e in self.events]

    def last_actor(self) -> Optional[str]:
        return self.events[-1].actor if self.events else None


def semantic_provenance(current_text: str, related_texts: List[str]) -> float:
    """Simple semantic similarity metric using common word overlap.

    In a full implementation this would leverage embeddings or other semantic
    models. Here we keep it lightweight to demonstrate the concept of
    semantic provenance without external dependencies.
    """
    current_words = set(current_text.lower().split())
    if not related_texts:
        return 0.0
    overlaps = [len(current_words.intersection(rt.lower().split())) / max(len(current_words), 1) for rt in related_texts]
    return sum(overlaps) / len(overlaps)


def temporal_layering(event_time: datetime, context_time: datetime) -> float:
    """Simple weighting based on temporal proximity."""
    delta = abs((context_time - event_time).total_seconds())
    # 1 hour => weight 1.0, 1 day => ~0.04
    return 1 / (1 + delta / 3600)
