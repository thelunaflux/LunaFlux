"""Tests for LiquidityDepthSignal."""

import pytest
from lunaflux.signals.liquidity_depth import LiquidityDepthSignal
from lunaflux.models import SignalBias
from tests.conftest import make_snap

sig = LiquidityDepthSignal()


class TestLiquidityDepthBasics:
    def test_name(self):
        assert sig.name == "liquidity_depth"

    def test_score_clamped(self):
        snap = make_snap(liquidity_usd=100_000_000.0, liquidity_7d_ago=1_000.0, volume_24h=80_000_000.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_no_prior_liquidity_no_crash(self):
        snap = make_snap(liquidity_7d_ago=0.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_detail_contains_liquidity(self):
        r = sig.compute(make_snap())
        assert "$" in r.detail or "M" in r.detail


class TestLiquidityDepthSignals:
    def test_growing_liquidity_bullish(self):
        snap = make_snap(liquidity_usd=30_000_000.0, liquidity_7d_ago=20_000_000.0)
        r = sig.compute(snap)
        assert r.score > 55

    def test_falling_liquidity_bearish(self):
        snap = make_snap(liquidity_usd=10_000_000.0, liquidity_7d_ago=20_000_000.0)
        r = sig.compute(snap)
        assert r.score < 45

    def test_high_volume_utilization_bonus(self):
        """vol/liq > 0.5 = active market."""
        high = sig.compute(make_snap(volume_24h=12_000_000.0, liquidity_usd=20_000_000.0))
        low  = sig.compute(make_snap(volume_24h=200_000.0, liquidity_usd=20_000_000.0))
        assert high.score > low.score

    def test_volume_surge_bonus(self):
        surge = sig.compute(make_snap(volume_24h=12_000_000.0, volume_7d_avg=4_000_000.0))
        flat  = sig.compute(make_snap(volume_24h=4_000_000.0, volume_7d_avg=4_000_000.0))
        assert surge.score > flat.score

    def test_volume_collapse_penalty(self):
        collapse = sig.compute(make_snap(volume_24h=1_000_000.0, volume_7d_avg=8_000_000.0))
        normal   = sig.compute(make_snap(volume_24h=4_000_000.0, volume_7d_avg=4_000_000.0))
        assert collapse.score < normal.score

    def test_liq_drop_with_vol_surge_vs_liq_stable(self):
        """Stable liquidity should score higher than declining liquidity."""
        declining = sig.compute(make_snap(
            liquidity_usd=14_000_000.0, liquidity_7d_ago=20_000_000.0,
            volume_24h=4_000_000.0, volume_7d_avg=4_000_000.0,
        ))
        stable = sig.compute(make_snap(
            liquidity_usd=20_000_000.0, liquidity_7d_ago=20_000_000.0,
            volume_24h=4_000_000.0, volume_7d_avg=4_000_000.0,
        ))
        assert stable.score > declining.score

    def test_strength_proportional_to_deviation(self):
        big_change = sig.compute(make_snap(liquidity_usd=40_000_000.0, liquidity_7d_ago=20_000_000.0))
        small_change = sig.compute(make_snap(liquidity_usd=21_000_000.0, liquidity_7d_ago=20_000_000.0))
        assert big_change.strength > small_change.strength
