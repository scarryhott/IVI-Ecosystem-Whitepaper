"""Structural Redundancy & Pattern Integrity utilities."""

from __future__ import annotations

from typing import Iterable


def redundant_discovery_score(scores: Iterable[float]) -> float:
    """Combine scores from independent discoveries."""
    scores = list(scores)
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def system_coherence(pattern_occurrences: int, domain_count: int) -> float:
    """Simple measure of coherence across domains."""
    if domain_count <= 0:
        return 0.0
    return pattern_occurrences / domain_count
