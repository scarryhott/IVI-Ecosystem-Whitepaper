"""Socially Verifiable Intangibles for IVI."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ReputationEvent:
    actor: str
    description: str


@dataclass
class ReputationTrail:
    item_id: str
    events: List[ReputationEvent] = field(default_factory=list)

    def add_event(self, actor: str, description: str) -> None:
        self.events.append(ReputationEvent(actor=actor, description=description))

    def trust_score(self) -> float:
        """Simple trust score derived from number of unique actors."""
        unique_actors = {e.actor for e in self.events}
        return len(unique_actors) / max(len(self.events), 1)
