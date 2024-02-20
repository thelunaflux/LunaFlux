"""Signal 2: Holder Velocity — measures rate of new holder adoption."""

from ..models import ChainSnapshot, SignalResult, SignalBias


class HolderVelocitySignal:
    """
    Measures holder growth rate as a proxy for organic adoption.

    Fast holder growth = expansion phase.
    Holder decline = distribution or contraction.
    Decelerating growth = distribution approaching.
    """

    name = "holder_velocity"

    def compute(self, snap: ChainSnapshot) -> SignalResult:
        current    = snap.holder_count
        ago_7d     = snap.holder_count_7d_ago
        ago_30d    = snap.holder_count_30d_ago

        if ago_7d == 0 or ago_30d == 0:
            return SignalResult(
                signal_name=self.name,
                score=50.0,
                bias=SignalBias.NEUTRAL,
                strength=0.0,
                detail="Holder Velocity: insufficient historical data",
            )

        score = 50.0

        # 7-day growth rate
        growth_7d = (current - ago_7d) / ago_7d * 100
        if growth_7d > 10:
            score += 25
        elif growth_7d > 5:
            score += 15
        elif growth_7d > 2:
            score += 8
        elif growth_7d > 0:
            score += 3
        elif growth_7d < -5:
            score -= 25
        elif growth_7d < -2:
            score -= 15
        elif growth_7d < 0:
            score -= 8

        # 30-day trend (is growth accelerating or decelerating?)
        growth_30d = (current - ago_30d) / ago_30d * 100
        weekly_avg_30d = growth_30d / 4  # weekly average over 30 days

        if growth_7d > weekly_avg_30d + 2:
            score += 10   # Accelerating growth = expansion signal
        elif growth_7d < weekly_avg_30d - 2:
            score -= 10   # Decelerating = distribution warning

        score = max(0.0, min(100.0, score))
        bias = SignalBias.BULLISH if score > 55 else SignalBias.BEARISH if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        trend = "accelerating" if growth_7d > weekly_avg_30d else "decelerating"
        detail = (
            f"Holders: {current:,}, "
            f"7d growth: {growth_7d:+.1f}%, "
            f"30d avg weekly: {weekly_avg_30d:+.1f}%, "
            f"trend {trend}"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
