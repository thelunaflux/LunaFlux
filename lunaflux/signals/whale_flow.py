"""Signal 1: Whale Flow — tracks large wallet movement direction."""

from ..models import ChainSnapshot, SignalResult, SignalBias


class WhaleFlowSignal:
    """
    Analyzes large wallet inflow/outflow to determine institutional bias.

    Bullish: more outflow from exchanges, inflows to wallets (accumulation).
    Bearish: more inflow to exchanges (sell pressure building).
    """

    name = "whale_flow"

    def compute(self, snap: ChainSnapshot) -> SignalResult:
        inflow  = snap.whale_inflow_usd
        outflow = snap.whale_outflow_usd
        tx_count = snap.whale_tx_count

        total = inflow + outflow
        if total == 0:
            return SignalResult(
                signal_name=self.name,
                score=50.0,
                bias=SignalBias.NEUTRAL,
                strength=0.0,
                detail="Whale Flow: no whale activity detected",
            )

        score = 50.0

        # Net flow ratio — outflow > inflow = whales buying (bullish)
        net_ratio = (outflow - inflow) / total  # -1 to 1
        score += net_ratio * 30  # up to ±30 points

        # Volume of activity (larger whale activity = stronger signal)
        if total > 50_000_000:       # $50M+
            score += 10 if net_ratio > 0 else -10
        elif total > 10_000_000:     # $10M+
            score += 5 if net_ratio > 0 else -5

        # Transaction count bonus (many whale txns = sustained pressure)
        if tx_count > 50:
            score += 5 if net_ratio > 0 else -5
        elif tx_count > 20:
            score += 2 if net_ratio > 0 else -2

        score = max(0.0, min(100.0, score))
        bias = SignalBias.BULLISH if score > 55 else SignalBias.BEARISH if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        net_dir = "accumulating" if outflow > inflow else "distributing"
        detail = (
            f"Whale Flow: ${total/1e6:.1f}M total, "
            f"in ${inflow/1e6:.1f}M / out ${outflow/1e6:.1f}M, "
            f"whales {net_dir} ({tx_count} txns)"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
