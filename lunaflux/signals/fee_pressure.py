"""Signal 4: Fee Pressure — network fee trends as demand proxy."""

from ..models import ChainSnapshot, SignalResult, SignalBias


class FeePressureSignal:
    """
    Analyzes on-chain fee and transaction count trends.

    Rising fees + rising tx count = real network demand = bullish.
    Rising fees + falling tx count = congestion, not growth = neutral/bearish.
    Falling fees + falling tx count = low demand = bearish.
    """

    name = "fee_pressure"

    def compute(self, snap: ChainSnapshot) -> SignalResult:
        fee_now    = snap.avg_fee_usd
        fee_7d     = snap.avg_fee_7d_ago
        tx_now     = snap.tx_count_24h
        tx_avg     = snap.tx_count_7d_avg

        score = 50.0

        # Fee trend
        fee_change = 0.0
        if fee_7d > 0:
            fee_change = (fee_now - fee_7d) / fee_7d * 100
            if fee_change > 50:
                score += 15
            elif fee_change > 20:
                score += 8
            elif fee_change > 5:
                score += 3
            elif fee_change < -30:
                score -= 15
            elif fee_change < -10:
                score -= 8
            elif fee_change < -2:
                score -= 3

        # Transaction count vs 7d average
        tx_ratio = 0.0
        if tx_avg > 0:
            tx_ratio = tx_now / tx_avg
            if tx_ratio > 1.5:
                score += 15
            elif tx_ratio > 1.2:
                score += 8
            elif tx_ratio > 1.0:
                score += 3
            elif tx_ratio < 0.5:
                score -= 15
            elif tx_ratio < 0.8:
                score -= 8
            elif tx_ratio < 1.0:
                score -= 3

        # Fee up + tx count up = genuine demand (amplify bullish)
        if fee_change > 10 and tx_ratio > 1.2:
            score += 10

        # Fee up + tx count down = congestion not demand (dampen)
        if fee_change > 20 and tx_ratio < 0.9:
            score -= 8

        # Fee down + tx count down = dead market (amplify bearish)
        if fee_change < -10 and tx_ratio < 0.8:
            score -= 10

        score = max(0.0, min(100.0, score))
        bias = SignalBias.BULLISH if score > 55 else SignalBias.BEARISH if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        detail = (
            f"Fee: ${fee_now:.4f} ({fee_change:+.1f}% 7d), "
            f"Tx/day: {tx_now:,} ({tx_ratio:.2f}x avg)"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
