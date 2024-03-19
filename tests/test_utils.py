"""Tests for LunaFlux utility modules."""

import time
import pytest
from lunaflux.utils.normalizer import (
    clamp, weighted_average, signal_alignment, cycle_momentum, phase_from_index,
)
from lunaflux.utils.cache import ChainSnapshotCache
from tests.conftest import make_snap


class TestClamp:
    def test_in_range(self):
        assert clamp(50.0) == 50.0

    def test_above_max(self):
        assert clamp(150.0) == 100.0

    def test_below_min(self):
        assert clamp(-10.0) == 0.0

    def test_exact_boundaries(self):
        assert clamp(0.0) == 0.0
        assert clamp(100.0) == 100.0

    def test_custom_bounds(self):
        assert clamp(5.0, 10.0, 20.0) == 10.0
        assert clamp(25.0, 10.0, 20.0) == 20.0
        assert clamp(15.0, 10.0, 20.0) == 15.0


class TestWeightedAverage:
    def test_equal_weights(self):
        result = weighted_average({"a": 60.0, "b": 40.0}, {"a": 0.5, "b": 0.5})
        assert abs(result - 50.0) < 0.001

    def test_missing_signal_renormalizes(self):
        result = weighted_average({"a": 80.0}, {"a": 0.5, "b": 0.5})
        assert abs(result - 80.0) < 0.001

    def test_empty_scores_returns_50(self):
        assert weighted_average({}, {"a": 1.0}) == 50.0

    def test_all_neutral_returns_50(self):
        from lunaflux.engine import WEIGHTS
        scores = {k: 50.0 for k in WEIGHTS}
        assert abs(weighted_average(scores, WEIGHTS) - 50.0) < 0.001

    def test_clamped_to_100(self):
        assert weighted_average({"a": 200.0}, {"a": 1.0}) <= 100.0


class TestSignalAlignment:
    def test_all_bullish_is_one(self):
        scores = {"a": 70.0, "b": 75.0, "c": 65.0}
        assert signal_alignment(scores) == 1.0

    def test_all_bearish_is_one(self):
        scores = {"a": 20.0, "b": 25.0, "c": 15.0}
        assert signal_alignment(scores) == 1.0

    def test_split_is_half(self):
        scores = {"a": 70.0, "b": 70.0, "c": 25.0, "d": 25.0}
        assert signal_alignment(scores) == 0.5

    def test_all_neutral_is_zero(self):
        scores = {"a": 50.0, "b": 50.0}
        assert signal_alignment(scores) == 0.0

    def test_empty_returns_zero(self):
        assert signal_alignment({}) == 0.0


class TestCycleMomentum:
    def test_all_neutral_zero(self):
        scores = {"a": 50.0, "b": 50.0}
        assert cycle_momentum(scores) == 0.0

    def test_all_bullish_positive(self):
        scores = {"a": 70.0, "b": 80.0}
        assert cycle_momentum(scores) > 0

    def test_all_bearish_negative(self):
        scores = {"a": 20.0, "b": 30.0}
        assert cycle_momentum(scores) < 0

    def test_empty_returns_zero(self):
        assert cycle_momentum({}) == 0.0

    def test_range_is_minus_one_to_one(self):
        scores = {"a": 100.0, "b": 100.0}
        m = cycle_momentum(scores)
        assert -1 <= m <= 1


class TestPhaseFromIndex:
    def test_distribution(self):
        assert phase_from_index(80.0) == "distribution"

    def test_expansion(self):
        assert phase_from_index(60.0) == "expansion"

    def test_accumulation(self):
        assert phase_from_index(35.0) == "accumulation"

    def test_contraction(self):
        assert phase_from_index(10.0) == "contraction"

    def test_boundary_75_is_distribution(self):
        assert phase_from_index(75.0) == "distribution"

    def test_boundary_50_is_expansion(self):
        assert phase_from_index(50.0) == "expansion"

    def test_boundary_25_is_accumulation(self):
        assert phase_from_index(25.0) == "accumulation"


class TestChainSnapshotCache:
    def test_set_and_get(self):
        cache = ChainSnapshotCache(ttl_seconds=60)
        snap = make_snap()
        cache.set(snap)
        assert cache.get("SOL") is snap

    def test_miss_returns_none(self):
        cache = ChainSnapshotCache()
        assert cache.get("MISSING") is None

    def test_expired_returns_none(self):
        cache = ChainSnapshotCache(ttl_seconds=0.01)
        cache.set(make_snap())
        time.sleep(0.05)
        assert cache.get("SOL") is None

    def test_invalidate(self):
        cache = ChainSnapshotCache()
        cache.set(make_snap())
        cache.invalidate("SOL")
        assert cache.get("SOL") is None

    def test_clear(self):
        cache = ChainSnapshotCache()
        cache.set(make_snap(symbol="A"))
        cache.set(make_snap(symbol="B"))
        cache.clear()
        assert cache.size() == 0

    def test_size(self):
        cache = ChainSnapshotCache()
        cache.set(make_snap(symbol="A"))
        cache.set(make_snap(symbol="B"))
        assert cache.size() == 2

    def test_valid_symbols(self):
        cache = ChainSnapshotCache(ttl_seconds=60)
        cache.set(make_snap(symbol="SOL"))
        cache.set(make_snap(symbol="ETH"))
        syms = cache.valid_symbols()
        assert "SOL" in syms and "ETH" in syms

    def test_overwrite_refreshes(self):
        cache = ChainSnapshotCache()
        cache.set(make_snap(holder_count=100_000))
        cache.set(make_snap(holder_count=200_000))
        assert cache.get("SOL").holder_count == 200_000
