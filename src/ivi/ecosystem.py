from __future__ import annotations

"""High level integration utilities for the IVI ecosystem."""

from dataclasses import dataclass, field
from typing import Dict, List

from .belief_alignment import BeliefNode, score_alignment
from .social_verification import ReputationTrail
from .traceability import IdeaTrace
from .usefulness import UsefulnessRecord
from .decentralized_scoring import Agent, ScoringSystem
from .token import TokenLedger


@dataclass
class IVIEcosystem:
    """Lightweight container coordinating core IVI modules."""

    belief_tree: BeliefNode | None = None
    traces: Dict[str, IdeaTrace] = field(default_factory=dict)
    usefulness: Dict[str, UsefulnessRecord] = field(default_factory=dict)
    reputation: Dict[str, ReputationTrail] = field(default_factory=dict)
    scoring: Dict[str, ScoringSystem] = field(default_factory=dict)
    ledger: TokenLedger = field(default_factory=TokenLedger)
    last_scores: Dict[str, float] = field(default_factory=dict)

    impact_weight: float = 0.4
    trust_weight: float = 0.4
    alignment_weight: float = 0.2
    content_weight: float = 0.0

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

        prev = self.last_scores.get(idea_id, 0.0)
        new = self.overall_score(idea_id)
        delta = new - prev
        if delta > 0:
            self.ledger.mint(user, delta)
        self.last_scores[idea_id] = new

    def add_scoring_agent(self, idea_id: str, agent: Agent) -> None:
        """Attach a scoring agent to the given idea."""
        system = self.scoring.setdefault(idea_id, ScoringSystem(item_id=idea_id))
        system.agents.append(agent)

    def evaluate_content(self, idea_id: str, content: str, user: str | None = None) -> float:
        """Evaluate content via the idea's scoring agents."""
        system = self.scoring.get(idea_id)
        if not system:
            return 0.0
        result = system.run_agents(content)

        prev = self.last_scores.get(idea_id, 0.0)
        new = self.overall_score(idea_id)
        delta = new - prev
        if user and delta > 0:
            self.ledger.mint(user, delta)
        self.last_scores[idea_id] = new
        return result

    def overall_score(self, idea_id: str) -> float:
        """Compute an aggregate score for an idea."""
        trace = self.traces.get(idea_id)
        record = self.usefulness.get(idea_id)
        rep = self.reputation.get(idea_id)
        scoring = self.scoring.get(idea_id)

        if not trace or not record or not rep:
            return 0.0

        alignment = 0.0
        if self.belief_tree:
            tags = [fb.tag for fb in record.feedback]
            alignment = score_alignment(tags, self.belief_tree)

        content_score = (
            scoring.score_history[-1] if scoring and scoring.score_history else 0.0
        )

        return (
            self.impact_weight * record.impact_score()
            + self.trust_weight * rep.trust_score()
            + self.alignment_weight * alignment
            + self.content_weight * content_score
        )