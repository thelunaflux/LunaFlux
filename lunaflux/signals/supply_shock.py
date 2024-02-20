"""Signal 5: Supply Shock — exchange balance as sell/hold pressure indicator."""

from ..models import ChainSnapshot, SignalResult, SignalBias


class SupplyShockSignal:
    """
    Tracks token supply on exchanges vs self-custody.

    Tokens leaving exchanges = holders self-custodying = bullish supply shock.
    Tokens entering exchanges = preparing to sell = bearish.
    Exchange balance declining = supply shock setup.
    """

    name = "supply_shock"

    def compute(self, snap: ChainSnapshot) -> SignalResult:
        inflow_24h   = snap.exchange_inflow_24h    # tokens being sent TO exchanges
        outflow_24h  = snap.exchange_outflow_24h   # tokens leaving exchanges
        balance_now  = snap.exchange_balance_pct   # % of supply on exchanges
        balance_7d   = snap.exchange_balance_7d_ago

        score = 50.0

        # Net exchange flow (positive = outflow > inflow = bullish)
        total = inflow_24h + outflow_24h
        if total > 0:
            net_ratio = (outflow_24h - inflow_24h) / total
            score += net_ratio * 25  # ±25 points

        # Exchange balance trend (falling balance = supply leaving = bullish)
        if balance_7d > 0:
            balance_change = balance_now - balance_7d  # negative = bullish
            if balance_change < -2.0:
                score += 20
            elif balance_change < -0.5:
                score += 10
            elif balance_change < 0:
                score += 4
            elif balance_change > 2.0:
                score -= 20
            elif balance_change > 0.5:
                score -= 10
            elif balance_change > 0:
                score -= 4

        # Absolute exchange balance level (lower = better)
        if balance_now < 5.0:
            score += 10   # Very low exchange supply = strong hold signal
        elif balance_now < 10.0:
            score += 4
        elif balance_now > 30.0:
            score -= 10   # High exchange supply = lots of potential sell pressure
        elif balance_now > 20.0:
            score -= 4

        score = max(0.0, min(100.0, score))
        bias = SignalBias.BULLISH if score > 55 else SignalBias.BEARISH if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        balance_change = balance_now - balance_7d if balance_7d > 0 else 0
        net_dir = "outflow" if outflow_24h > inflow_24h else "inflow"
        detail = (
            f"Exchange balance: {balance_now:.1f}% ({balance_change:+.1f}% 7d), "
            f"24h net {net_dir}: ${abs(outflow_24h - inflow_24h)/1e6:.1f}M"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
