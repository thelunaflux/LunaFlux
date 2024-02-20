"""Signal 3: Liquidity Depth — DEX liquidity changes as market health proxy."""

from ..models import ChainSnapshot, SignalResult, SignalBias


class LiquidityDepthSignal:
    """
    Tracks DEX liquidity changes relative to volume.

    Deep and growing liquidity = healthy expansion.
    Liquidity draining while volume rises = distribution warning.
    Low liquidity / volume = contraction.
    """

    name = "liquidity_depth"

    def compute(self, snap: ChainSnapshot) -> SignalResult:
        liq_now    = snap.liquidity_usd
        liq_7d     = snap.liquidity_7d_ago
        vol_24h    = snap.volume_24h
        vol_7d_avg = snap.volume_7d_avg

        score = 50.0

        # Liquidity change 7d
        if liq_7d > 0:
            liq_change = (liq_now - liq_7d) / liq_7d * 100
            if liq_change > 20:
                score += 20
            elif liq_change > 8:
                score += 12
            elif liq_change > 2:
                score += 5
            elif liq_change < -20:
                score -= 20
            elif liq_change < -8:
                score -= 12
            elif liq_change < -2:
                score -= 5
        else:
            liq_change = 0.0

        # Volume / liquidity ratio (utilization)
        if liq_now > 0:
            utilization = vol_24h / liq_now
            if utilization > 0.5:       # High utilization = active market
                score += 10
            elif utilization > 0.2:
                score += 5
            elif utilization < 0.02:    # Very low utilization = illiquid
                score -= 10

        # Volume trend (is volume growing?)
        if vol_7d_avg > 0:
            vol_ratio = vol_24h / vol_7d_avg
            if vol_ratio > 2.0:         # Volume surge
                score += 8
            elif vol_ratio > 1.3:
                score += 4
            elif vol_ratio < 0.5:       # Volume collapse
                score -= 8
            elif vol_ratio < 0.8:
                score -= 4

        # Liquidity dropping while volume rising = distribution warning
        if liq_change < -5 and vol_24h > vol_7d_avg * 1.2:
            score -= 8

        score = max(0.0, min(100.0, score))
        bias = SignalBias.BULLISH if score > 55 else SignalBias.BEARISH if score < 45 else SignalBias.NEUTRAL
        strength = round(abs(score - 50) / 50, 3)

        detail = (
            f"Liquidity: ${liq_now/1e6:.1f}M ({liq_change:+.1f}% 7d), "
            f"Vol 24h: ${vol_24h/1e6:.1f}M, "
            f"Utilization: {vol_24h/liq_now*100:.1f}%" if liq_now > 0
            else f"Liquidity: ${liq_now/1e6:.1f}M (no prior data)"
        )

        return SignalResult(
            signal_name=self.name,
            score=round(score, 2),
            bias=bias,
            strength=strength,
            detail=detail,
        )
