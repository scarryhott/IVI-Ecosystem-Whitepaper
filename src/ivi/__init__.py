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
from .token import TokenLedger
from .slearn import SlearnMap, LearningNode
from .ecosystem import IVIEcosystem

try:  # optional real-time features
    from .events import EventBus
    from .database import User, Interaction, create_db
except Exception:  # pragma: no cover - optional dependency missing
    EventBus = None  # type: ignore
    User = Interaction = create_db = None  # type: ignore

try:  # optional firebase integration
    from .firebase_utils import (
        init_firebase,
        verify_token,
        save_interaction,
        save_evaluation,
    )
except Exception:  # pragma: no cover - optional dependency missing
    def init_firebase(*_args, **_kwargs):
        return None

    def verify_token(*_args, **_kwargs):
        return None

    def save_interaction(*_args, **_kwargs) -> None:
        return None

    def save_evaluation(*_args, **_kwargs) -> None:
        return None

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
    "TokenLedger",
    "SlearnMap",
    "LearningNode",
    "IVIEcosystem",
    "EventBus",
    "User",
    "Interaction",
    "create_db",
    "init_firebase",
    "verify_token",
    "save_interaction",
    "save_evaluation",
]
