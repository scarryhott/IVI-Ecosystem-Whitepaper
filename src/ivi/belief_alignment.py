"""Belief-System Alignment tools for IVI."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class BeliefNode:
    label: str
    children: List['BeliefNode'] = field(default_factory=list)

    def add_child(self, node: 'BeliefNode') -> None:
        self.children.append(node)


def score_alignment(info_tags: List[str], belief_tree: BeliefNode) -> float:
    """Naive alignment score: fraction of tags present in the belief tree."""

    def collect_labels(node: BeliefNode) -> List[str]:
        labels = [node.label]
        for child in node.children:
            labels.extend(collect_labels(child))
        return labels

    belief_labels = set(collect_labels(belief_tree))
    matches = [t for t in info_tags if t in belief_labels]
    return len(matches) / max(len(info_tags), 1)
