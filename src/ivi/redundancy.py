"""Structural Redundancy & Pattern Integrity utilities."""

from __future__ import annotations

from typing import Iterable


def redundant_discovery_score(*independent_scores: Iterable[float]) -> float:
    """Combine scores from independent discoveries."""
    if not independent_scores:
        return 0.0
    return sum(independent_scores) / len(independent_scores)


def system_coherence(pattern_occurrences: int, domain_count: int) -> float:
    """Simple measure of coherence across domains."""
    if domain_count <= 0:
        return 0.0
    return pattern_occurrences / domain_count
