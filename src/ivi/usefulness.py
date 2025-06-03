"""Usefulness-Based Verification utilities for IVI."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Feedback:
    user: str
    tag: str
    notes: str


@dataclass
class UsefulnessRecord:
    """Stores feedback and calculates an impact score."""

    item_id: str
    feedback: List[Feedback] = field(default_factory=list)

    def add_feedback(self, user: str, tag: str, notes: str) -> None:
        self.feedback.append(Feedback(user=user, tag=tag, notes=notes))

    def impact_score(self) -> float:
        """Simple impact score: frequency of useful tags."""
        useful = [fb for fb in self.feedback if fb.tag.lower() in {"success", "aha", "solution"}]
        return len(useful) / max(len(self.feedback), 1)
