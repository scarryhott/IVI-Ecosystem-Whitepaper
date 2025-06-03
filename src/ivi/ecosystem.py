from __future__ import annotations

"""High level integration utilities for the IVI ecosystem."""

from dataclasses import dataclass, field
from typing import Dict, List

from .belief_alignment import BeliefNode, score_alignment
from .social_verification import ReputationTrail
from .traceability import IdeaTrace
from .usefulness import UsefulnessRecord


@dataclass
class IVIEcosystem:
    """Lightweight container coordinating core IVI modules."""

    belief_tree: BeliefNode | None = None
    traces: Dict[str, IdeaTrace] = field(default_factory=dict)
    usefulness: Dict[str, UsefulnessRecord] = field(default_factory=dict)
    reputation: Dict[str, ReputationTrail] = field(default_factory=dict)

    def add_interaction(
        self, idea_id: str, user: str, tags: List[str], description: str
    ) -> None:
        """Record a user interaction across modules."""
        trace = self.traces.setdefault(idea_id, IdeaTrace(idea_id=idea_id))
        trace.add_event(actor=user, description=description)

        record = self.usefulness.setdefault(
            idea_id, UsefulnessRecord(item_id=idea_id)
        )
        for tag in tags:
            record.add_feedback(user=user, tag=tag, notes=description)

        rep = self.reputation.setdefault(idea_id, ReputationTrail(item_id=idea_id))
        rep.add_event(actor=user, description=description)

    def overall_score(self, idea_id: str) -> float:
        """Compute an aggregate score for an idea."""
        trace = self.traces.get(idea_id)
        record = self.usefulness.get(idea_id)
        rep = self.reputation.get(idea_id)

        if not trace or not record or not rep:
            return 0.0

        alignment = 0.0
        if self.belief_tree:
            tags = [fb.tag for fb in record.feedback]
            alignment = score_alignment(tags, self.belief_tree)

        return (
            0.4 * record.impact_score()
            + 0.4 * rep.trust_score()
            + 0.2 * alignment
        )
