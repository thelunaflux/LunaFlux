"""Tests for FeePressureSignal."""

import pytest
from lunaflux.signals.fee_pressure import FeePressureSignal
from lunaflux.models import SignalBias
from tests.conftest import make_snap

sig = FeePressureSignal()


class TestFeePressureBasics:
    def test_name(self):
        assert sig.name == "fee_pressure"

    def test_flat_market_near_neutral(self):
        r = sig.compute(make_snap())
        assert 40 <= r.score <= 60

    def test_score_clamped(self):
        snap = make_snap(avg_fee_usd=100.0, avg_fee_7d_ago=0.001, tx_count_24h=500_000, tx_count_7d_avg=10_000.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_detail_contains_fee(self):
        r = sig.compute(make_snap())
        assert "$" in r.detail or "Fee" in r.detail


class TestFeePressureSignals:
    def test_rising_fee_and_tx_bullish(self):
        snap = make_snap(
            avg_fee_usd=0.005, avg_fee_7d_ago=0.002,
            tx_count_24h=80_000, tx_count_7d_avg=50_000.0,
        )
        r = sig.compute(snap)
        assert r.bias == SignalBias.BULLISH
        assert r.score > 55

    def test_falling_fee_and_tx_bearish(self):
        snap = make_snap(
            avg_fee_usd=0.0005, avg_fee_7d_ago=0.003,
            tx_count_24h=20_000, tx_count_7d_avg=55_000.0,
        )
        r = sig.compute(snap)
        assert r.bias == SignalBias.BEARISH
        assert r.score < 45

    def test_rising_fee_falling_tx_no_demand_bonus(self):
        """Fee up + tx down = congestion, not real demand."""
        genuine = sig.compute(make_snap(
            avg_fee_usd=0.006, avg_fee_7d_ago=0.002,
            tx_count_24h=80_000, tx_count_7d_avg=50_000.0,
        ))
        congestion = sig.compute(make_snap(
            avg_fee_usd=0.006, avg_fee_7d_ago=0.002,
            tx_count_24h=30_000, tx_count_7d_avg=55_000.0,
        ))
        assert genuine.score > congestion.score

    def test_both_falling_amplifies_bearish(self):
        both_down = sig.compute(make_snap(
            avg_fee_usd=0.0005, avg_fee_7d_ago=0.003,
            tx_count_24h=20_000, tx_count_7d_avg=60_000.0,
        ))
        only_fee_down = sig.compute(make_snap(
            avg_fee_usd=0.0005, avg_fee_7d_ago=0.003,
            tx_count_24h=55_000, tx_count_7d_avg=60_000.0,
        ))
        assert both_down.score <= only_fee_down.score

    def test_tx_surge_with_flat_fee_bullish(self):
        snap = make_snap(tx_count_24h=90_000, tx_count_7d_avg=50_000.0)
        r = sig.compute(snap)
        assert r.score > 55

    def test_tx_collapse_bearish(self):
        snap = make_snap(tx_count_24h=15_000, tx_count_7d_avg=55_000.0)
        r = sig.compute(snap)
        assert r.score < 45

    def test_zero_tx_avg_no_crash(self):
        snap = make_snap(tx_count_7d_avg=0.0)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100
