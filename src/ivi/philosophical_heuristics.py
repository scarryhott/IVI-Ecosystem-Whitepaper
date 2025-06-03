"""Philosophical heuristics for IVI."""

from __future__ import annotations
from typing import Iterable


def fractal_integrity(values: Iterable[float]) -> float:
    """Check whether a pattern holds across scales by measuring variance."""
    values = list(values)
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    # Lower variance implies higher integrity
    return 1 / (1 + variance)


def predictive_coherence(predicted: Iterable[float], observed: Iterable[float]) -> float:
    """Check how well predictions align with observations."""
    predicted = list(predicted)
    observed = list(observed)
    if not predicted or not observed or len(predicted) != len(observed):
        return 0.0
    errors = [abs(p - o) for p, o in zip(predicted, observed)]
    return 1 / (1 + (sum(errors) / len(errors)))


def self_awareness_metric(acknowledged_limits: int, total_claims: int) -> float:
    """Higher score if more limitations are acknowledged."""
    if total_claims <= 0:
        return 0.0
    return acknowledged_limits / total_claims
