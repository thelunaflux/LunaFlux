"""Tests for HolderVelocitySignal."""

import pytest
from lunaflux.signals.holder_velocity import HolderVelocitySignal
from lunaflux.models import SignalBias
from tests.conftest import make_snap

sig = HolderVelocitySignal()


class TestHolderVelocityBasics:
    def test_name(self):
        assert sig.name == "holder_velocity"

    def test_zero_history_returns_neutral(self):
        snap = make_snap(holder_count_7d_ago=0, holder_count_30d_ago=0)
        r = sig.compute(snap)
        assert r.score == 50.0
        assert r.bias == SignalBias.NEUTRAL
        assert r.strength == 0.0

    def test_score_clamped(self):
        snap = make_snap(holder_count=200_000, holder_count_7d_ago=100_000, holder_count_30d_ago=80_000)
        r = sig.compute(snap)
        assert 0 <= r.score <= 100

    def test_detail_contains_growth_pct(self):
        r = sig.compute(make_snap())
        assert "%" in r.detail


class TestHolderVelocityGrowth:
    def test_strong_7d_growth_bullish(self):
        snap = make_snap(holder_count=115_000, holder_count_7d_ago=100_000, holder_count_30d_ago=95_000)
        r = sig.compute(snap)
        assert r.bias == SignalBias.BULLISH
        assert r.score > 55

    def test_holder_decline_bearish(self):
        snap = make_snap(holder_count=90_000, holder_count_7d_ago=100_000, holder_count_30d_ago=105_000)
        r = sig.compute(snap)
        assert r.bias == SignalBias.BEARISH
        assert r.score < 45

    def test_flat_holder_count_neutral(self):
        snap = make_snap(holder_count=100_100, holder_count_7d_ago=100_000, holder_count_30d_ago=99_600)
        r = sig.compute(snap)
        assert r.bias == SignalBias.NEUTRAL

    def test_accelerating_growth_bonus(self):
        """Current 7d growth faster than 30d avg = bonus."""
        accel = sig.compute(make_snap(
            holder_count=112_000, holder_count_7d_ago=100_000, holder_count_30d_ago=96_000,
        ))
        decel = sig.compute(make_snap(
            holder_count=101_000, holder_count_7d_ago=100_000, holder_count_30d_ago=90_000,
        ))
        assert accel.score > decel.score

    def test_decelerating_growth_penalty(self):
        snap = make_snap(
            holder_count=100_500,
            holder_count_7d_ago=100_000,
            holder_count_30d_ago=88_000,  # 30d avg was much faster
        )
        r = sig.compute(snap)
        # Decelerating = penalty
        assert r.score < 55

    def test_detail_shows_trend(self):
        r = sig.compute(make_snap(
            holder_count=115_000, holder_count_7d_ago=100_000, holder_count_30d_ago=90_000,
        ))
        assert "accelerating" in r.detail or "decelerating" in r.detail

    def test_massive_growth_high_score(self):
        snap = make_snap(holder_count=200_000, holder_count_7d_ago=100_000, holder_count_30d_ago=90_000)
        r = sig.compute(snap)
        assert r.score > 70
