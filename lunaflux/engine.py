"""LunaEngine — orchestrates 5 on-chain signals into a composite cycle analysis."""

from typing import Dict, List, Optional

from .models import ChainSnapshot, LunaAnalysis, LunaPhase, SignalBias, SignalResult
from .signals import ALL_SIGNALS
from .utils.normalizer import (
    clamp,
    weighted_average,
    signal_alignment as compute_alignment,
    cycle_momentum as compute_momentum,
    phase_from_index,
)

WEIGHTS: Dict[str, float] = {
    "whale_flow":       0.30,
    "supply_shock":     0.25,
    "holder_velocity":  0.20,
    "liquidity_depth":  0.15,
    "fee_pressure":     0.10,
}
# Total = 1.00 ✓


def _phase_from_index(idx: float) -> LunaPhase:
    phase = phase_from_index(idx)
    return LunaPhase(phase)


def _bias_from_index(idx: float) -> SignalBias:
    if idx > 55:
        return SignalBias.BULLISH
    elif idx < 45:
        return SignalBias.BEARISH
    return SignalBias.NEUTRAL


def _conviction(idx: float) -> float:
    return round(abs(idx - 50) / 50, 3)


def _dominant_signal(results: List[SignalResult]) -> str:
    if not results:
        return "none"
    return max(results, key=lambda r: abs(r.score - 50)).signal_name


def _categorize(results: List[SignalResult]):
    bullish = [r.signal_name for r in results if r.bias == SignalBias.BULLISH]
    bearish = [r.signal_name for r in results if r.bias == SignalBias.BEARISH]
    return bullish, bearish


def _warning_flags(scores: Dict[str, float], alignment: float) -> List[str]:
    flags = []
    if alignment < 0.5:
        flags.append("low_signal_alignment")
    whale = scores.get("whale_flow", 50)
    supply = scores.get("supply_shock", 50)
    holder = scores.get("holder_velocity", 50)
    liq = scores.get("liquidity_depth", 50)

    # Bullish whale but bearish supply = smart money exit while whales buy
    if whale > 65 and supply < 40:
        flags.append("whale_supply_divergence")
    # Holders growing but liquidity draining = fragile expansion
    if holder > 65 and liq < 35:
        flags.append("holder_growth_liquidity_mismatch")
    # Distribution zone
    if whale < 35 and supply < 35:
        flags.append("dual_distribution_signal")
    if liq < 30:
        flags.append("liquidity_critically_low")
    return flags


def _estimate_phase_duration(phase: LunaPhase, conviction: float) -> Optional[int]:
    """Rough heuristic for how long a phase typically lasts given conviction."""
    base = {
        LunaPhase.CONTRACTION:  30,
        LunaPhase.ACCUMULATION: 45,
        LunaPhase.EXPANSION:    60,
        LunaPhase.DISTRIBUTION: 21,
    }
    if conviction < 0.1:
        return None
    return int(base[phase] * (1 - conviction * 0.3))


def _build_reasoning(
    scores: Dict[str, float],
    luna_index: float,
    phase: LunaPhase,
    bullish: List[str],
    bearish: List[str],
    momentum: float,
) -> str:
    direction = "bullish" if luna_index > 55 else "bearish" if luna_index < 45 else "neutral"
    whale  = scores.get("whale_flow", 50)
    supply = scores.get("supply_shock", 50)
    holder = scores.get("holder_velocity", 50)

    parts = [
        f"Luna index {luna_index:.1f}/100 → {phase.value}.",
        f"On-chain bias {direction}: {len(bullish)} bullish, {len(bearish)} bearish signals.",
    ]

    if whale > 65:
        parts.append("Whales accumulating — institutional interest confirmed.")
    elif whale < 35:
        parts.append("Whale distribution detected — smart money exiting.")

    if supply > 65:
        parts.append("Exchange outflows dominant — supply leaving markets.")
    elif supply < 35:
        parts.append("Exchange inflows rising — sell pressure building.")

    if holder > 65:
        parts.append("Holder growth accelerating — organic adoption expanding.")
    elif holder < 35:
        parts.append("Holder count declining — retail capitulation visible.")

    if momentum > 0.3:
        parts.append(f"Cycle momentum strong bullish ({momentum:+.2f}).")
    elif momentum < -0.3:
        parts.append(f"Cycle momentum strong bearish ({momentum:+.2f}).")

    return " ".join(parts)


class LunaEngine:
    """
    Orchestrates all 5 LunaFlux signals into a composite LunaAnalysis.

    Usage:
        engine = LunaEngine()
        analysis = engine.analyze(snap)
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or WEIGHTS
        self.signals = ALL_SIGNALS

    def analyze(self, snap: ChainSnapshot) -> LunaAnalysis:
        results: List[SignalResult] = [sig.compute(snap) for sig in self.signals]
        scores: Dict[str, float] = {r.signal_name: r.score for r in results}

        luna_index  = weighted_average(scores, self.weights)
        phase       = _phase_from_index(luna_index)
        bias        = _bias_from_index(luna_index)
        conviction  = _conviction(luna_index)
        alignment   = compute_alignment(scores)
        momentum    = compute_momentum(scores)

        dominant          = _dominant_signal(results)
        bullish, bearish  = _categorize(results)
        flags             = _warning_flags(scores, alignment)
        duration_est      = _estimate_phase_duration(phase, conviction)
        reasoning         = _build_reasoning(scores, luna_index, phase, bullish, bearish, momentum)

        return LunaAnalysis(
            symbol                  = snap.symbol,
            whale_flow_score        = scores.get("whale_flow", 50),
            holder_velocity_score   = scores.get("holder_velocity", 50),
            liquidity_depth_score   = scores.get("liquidity_depth", 50),
            fee_pressure_score      = scores.get("fee_pressure", 50),
            supply_shock_score      = scores.get("supply_shock", 50),
            luna_index              = round(luna_index, 2),
            luna_phase              = phase,
            cycle_momentum          = momentum,
            phase_duration_estimate = duration_est,
            dominant_signal         = dominant,
            bullish_signals         = bullish,
            bearish_signals         = bearish,
            warning_flags           = flags,
            bias                    = bias,
            conviction              = conviction,
            signal_alignment        = alignment,
            reasoning               = reasoning,
        )
