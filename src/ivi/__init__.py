"""Core package for Intangibly Verified Information (IVI)."""

from .traceability import IdeaTrace, semantic_provenance, temporal_layering
from .usefulness import UsefulnessRecord
from .belief_alignment import BeliefNode, score_alignment
from .social_verification import ReputationTrail
from .redundancy import redundant_discovery_score, system_coherence
from .philosophical_heuristics import (
    fractal_integrity,
    predictive_coherence,
    self_awareness_metric,
)
from .decentralized_scoring import Agent, ScoringSystem

__all__ = [
    "IdeaTrace",
    "semantic_provenance",
    "temporal_layering",
    "UsefulnessRecord",
    "BeliefNode",
    "score_alignment",
    "ReputationTrail",
    "redundant_discovery_score",
    "system_coherence",
    "fractal_integrity",
    "predictive_coherence",
    "self_awareness_metric",
    "Agent",
    "ScoringSystem",
]
