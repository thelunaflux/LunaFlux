"""Tests for WhaleFlowSignal."""

import pytest
from lunaflux.signals.whale_flow import WhaleFlowSignal
from lunaflux.models import SignalBias
from tests.conftest import make_snap

sig = WhaleFlowSignal()


class TestWhaleFlowBasics:
    def test_name(self):
        assert sig.name == "whale_flow"

    def test_zero_flow_returns_neutral(self):
        snap = make_snap(whale_inflow_usd=0.0, whale_outflow_usd=0.0)
        r = sig.compute(snap)
        assert r.score == 50.0
        assert r.bias == SignalBias.NEUTRAL
        assert r.strength == 0.0

    def test_score_clamped(self):
        snap = make_snap(whale_inflow_usd=0.0, whale_outflow_usd=500_000_000.0, whale_tx_count=200)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_detail_contains_amounts(self):
        r = sig.compute(make_snap())
        assert "$" in r.detail or "M" in r.detail

    def test_strength_in_range(self):
        r = sig.compute(make_snap())
        assert 0 <= r.strength <= 1


class TestWhaleFlowDirection:
    def test_dominant_outflow_bullish(self):
        """Whales withdrawing from exchanges = accumulating = bullish."""
        snap = make_snap(whale_inflow_usd=1_000_000.0, whale_outflow_usd=15_000_000.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.BULLISH
        assert r.score > 55

    def test_dominant_inflow_bearish(self):
        """Whales sending to exchanges = distributing = bearish."""
        snap = make_snap(whale_inflow_usd=15_000_000.0, whale_outflow_usd=1_000_000.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.BEARISH
        assert r.score < 45

    def test_balanced_flow_neutral(self):
        snap = make_snap(whale_inflow_usd=5_000_000.0, whale_outflow_usd=5_000_000.0)
        r = sig.compute(snap)
        assert r.bias == SignalBias.NEUTRAL

    def test_large_volume_amplifies_bullish(self):
        small = sig.compute(make_snap(whale_inflow_usd=1_000_000.0, whale_outflow_usd=5_000_000.0))
        large = sig.compute(make_snap(whale_inflow_usd=5_000_000.0, whale_outflow_usd=60_000_000.0))
        assert large.score > small.score

    def test_high_tx_count_amplifies_signal(self):
        low_tx  = sig.compute(make_snap(whale_inflow_usd=1e6, whale_outflow_usd=9e6, whale_tx_count=5))
        high_tx = sig.compute(make_snap(whale_inflow_usd=1e6, whale_outflow_usd=9e6, whale_tx_count=60))
        assert high_tx.score > low_tx.score

    def test_detail_shows_accumulating_when_outflow_dominant(self):
        snap = make_snap(whale_inflow_usd=1e6, whale_outflow_usd=15e6)
        r = sig.compute(snap)
        assert "accumulating" in r.detail

    def test_detail_shows_distributing_when_inflow_dominant(self):
        snap = make_snap(whale_inflow_usd=15e6, whale_outflow_usd=1e6)
        r = sig.compute(snap)
        assert "distributing" in r.detail
