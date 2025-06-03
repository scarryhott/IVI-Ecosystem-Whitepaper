"""Decentralized and AI-Assisted scoring mechanisms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List


def cyclic_revision(score_history: List[float], new_score: float, weight: float = 0.5) -> float:
    """Update the score with weighted average to simulate change over time."""
    if not score_history:
        return new_score
    last = score_history[-1]
    updated = (1 - weight) * last + weight * new_score
    score_history.append(updated)
    return updated


@dataclass
class Agent:
    name: str
    evaluate: Callable[[str], float]


@dataclass
class ScoringSystem:
    item_id: str
    agents: List[Agent] = field(default_factory=list)
    score_history: List[float] = field(default_factory=list)

    def run_agents(self, content: str) -> float:
        if not self.agents:
            return 0.0
        scores = [agent.evaluate(content) for agent in self.agents]
        avg = sum(scores) / len(scores)
        return cyclic_revision(self.score_history, avg)
