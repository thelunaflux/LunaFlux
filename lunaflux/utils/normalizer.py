"""Normalizer utilities for LunaFlux signal aggregation."""

from typing import Dict


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def weighted_average(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    total_weight = 0.0
    weighted_sum = 0.0
    for name, score in scores.items():
        w = weights.get(name, 0.0)
        if w > 0:
            weighted_sum += score * w
            total_weight += w
    if total_weight == 0:
        return 50.0
    return clamp(weighted_sum / total_weight)


def signal_alignment(scores: Dict[str, float], threshold: float = 5.0) -> float:
    if not scores:
        return 0.0
    bullish = sum(1 for s in scores.values() if s > 50 + threshold)
    bearish = sum(1 for s in scores.values() if s < 50 - threshold)
    dominant = max(bullish, bearish)
    return round(dominant / len(scores), 3)


def cycle_momentum(scores: Dict[str, float]) -> float:
    """
    Compute cycle momentum: weighted directional pull from neutral (-1 to 1).
    Positive = bullish momentum, negative = bearish momentum.
    """
    if not scores:
        return 0.0
    deviations = [(s - 50) / 50 for s in scores.values()]
    return round(sum(deviations) / len(deviations), 3)


def phase_from_index(index: float) -> str:
    """Return the LunaPhase string for a given luna_index."""
    if index >= 75:
        return "distribution"
    elif index >= 50:
        return "expansion"
    elif index >= 25:
        return "accumulation"
    else:
        return "contraction"
