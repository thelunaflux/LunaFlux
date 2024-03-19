"""Tests for SupplyShockSignal."""

import pytest
from lunaflux.signals.supply_shock import SupplyShockSignal
from lunaflux.models import SignalBias
from tests.conftest import make_snap

sig = SupplyShockSignal()


class TestSupplyShockBasics:
    def test_name(self):
        assert sig.name == "supply_shock"

    def test_score_clamped(self):
        snap = make_snap(
            exchange_outflow_24h=500_000_000.0, exchange_inflow_24h=0.0,
            exchange_balance_pct=1.0, exchange_balance_7d_ago=30.0,
        )
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_balanced_flows_near_neutral(self):
        r = sig.compute(make_snap())
        assert 40 <= r.score <= 60

    def test_detail_contains_balance_pct(self):
        r = sig.compute(make_snap())
        assert "%" in r.detail


class TestSupplyShockDirection:
    def test_dominant_outflow_bullish(self):
        """Tokens leaving exchanges = supply shock = bullish."""
        snap = make_snap(
            exchange_inflow_24h=500_000.0, exchange_outflow_24h=15_000_000.0,
            exchange_balance_pct=9.0, exchange_balance_7d_ago=12.0,
        )
        r = sig.compute(snap)
        assert r.bias == SignalBias.BULLISH
        assert r.score > 55

    def test_dominant_inflow_bearish(self):
        """Tokens entering exchanges = sell pressure = bearish."""
        snap = make_snap(
            exchange_inflow_24h=15_000_000.0, exchange_outflow_24h=500_000.0,
            exchange_balance_pct=20.0, exchange_balance_7d_ago=14.0,
        )
        r = sig.compute(snap)
        assert r.bias == SignalBias.BEARISH
        assert r.score < 45

    def test_falling_exchange_balance_bullish(self):
        snap = make_snap(exchange_balance_pct=7.0, exchange_balance_7d_ago=12.0)
        r = sig.compute(snap)
        assert r.score > 55

    def test_rising_exchange_balance_bearish(self):
        snap = make_snap(exchange_balance_pct=22.0, exchange_balance_7d_ago=14.0)
        r = sig.compute(snap)
        assert r.score < 45

    def test_very_low_balance_bonus(self):
        """< 5% on exchanges = very bullish supply shock."""
        low  = sig.compute(make_snap(exchange_balance_pct=3.0, exchange_balance_7d_ago=3.5))
        high = sig.compute(make_snap(exchange_balance_pct=15.0, exchange_balance_7d_ago=15.5))
        assert low.score > high.score

    def test_high_balance_penalty(self):
        snap = make_snap(exchange_balance_pct=35.0, exchange_balance_7d_ago=32.0)
        r = sig.compute(snap)
        assert r.score < 45

    def test_detail_shows_net_direction(self):
        snap = make_snap(exchange_inflow_24h=500_000.0, exchange_outflow_24h=10_000_000.0)
        r = sig.compute(snap)
        assert "outflow" in r.detail

    def test_strength_grows_with_imbalance(self):
        balanced = sig.compute(make_snap(exchange_inflow_24h=5e6, exchange_outflow_24h=5e6))
        imbalanced = sig.compute(make_snap(exchange_inflow_24h=1e6, exchange_outflow_24h=20e6))
        assert imbalanced.strength > balanced.strength
