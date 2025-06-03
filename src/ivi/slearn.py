"""Simple Slearn education map built on IVI tokens."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .token import TokenLedger


@dataclass
class LearningNode:
    """Represents a lesson or goal in the learning map."""

    node_id: str
    required_tokens: float = 0.0
    children: List[str] = field(default_factory=list)


@dataclass
class SlearnMap:
    """Track user progress through token-gated lessons."""

    ledger: TokenLedger
    nodes: Dict[str, LearningNode] = field(default_factory=dict)
    progress: Dict[str, List[str]] = field(default_factory=dict)

    def add_node(self, node: LearningNode) -> None:
        self.nodes[node.node_id] = node

    def available_nodes(self, user: str) -> List[str]:
        balance = self.ledger.balance_of(user)
        completed = set(self.progress.get(user, []))
        return [
            nid
            for nid, node in self.nodes.items()
            if nid not in completed and balance >= node.required_tokens
        ]

    def complete_node(self, user: str, node_id: str) -> bool:
        if node_id not in self.available_nodes(user):
            return False
        self.progress.setdefault(user, []).append(node_id)
        return True

