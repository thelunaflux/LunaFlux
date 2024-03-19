"""Tests for LunaEngine."""

import pytest
from lunaflux.engine import LunaEngine, WEIGHTS, _phase_from_index, _bias_from_index, _conviction
from lunaflux.models import LunaPhase, SignalBias
from tests.conftest import make_snap


class TestEngineWeights:
    def test_weights_sum_to_one(self):
        total = sum(WEIGHTS.values())
        assert abs(total - 1.0) < 1e-9

    def test_all_five_signals_weighted(self):
        expected = {"whale_flow", "supply_shock", "holder_velocity", "liquidity_depth", "fee_pressure"}
        assert set(WEIGHTS.keys()) == expected

    def test_whale_highest_weight(self):
        assert WEIGHTS["whale_flow"] == max(WEIGHTS.values())


class TestPhaseMappings:
    def test_distribution_at_75(self):
        assert _phase_from_index(75.0) == LunaPhase.DISTRIBUTION
        assert _phase_from_index(100.0) == LunaPhase.DISTRIBUTION

    def test_expansion_band(self):
        assert _phase_from_index(50.0) == LunaPhase.EXPANSION
        assert _phase_from_index(74.9) == LunaPhase.EXPANSION

    def test_accumulation_band(self):
        assert _phase_from_index(25.0) == LunaPhase.ACCUMULATION
        assert _phase_from_index(49.9) == LunaPhase.ACCUMULATION

    def test_contraction_band(self):
        assert _phase_from_index(0.0) == LunaPhase.CONTRACTION
        assert _phase_from_index(24.9) == LunaPhase.CONTRACTION


class TestBiasMapping:
    def test_above_55_is_bullish(self):
        assert _bias_from_index(60.0) == SignalBias.BULLISH

    def test_below_45_is_bearish(self):
        assert _bias_from_index(40.0) == SignalBias.BEARISH

    def test_between_45_55_neutral(self):
        assert _bias_from_index(50.0) == SignalBias.NEUTRAL


class TestConviction:
    def test_zero_at_neutral(self):
        assert _conviction(50.0) == 0.0

    def test_max_at_extremes(self):
        assert _conviction(100.0) == 1.0
        assert _conviction(0.0) == 1.0

    def test_mid_conviction(self):
        assert abs(_conviction(75.0) - 0.5) < 0.001


class TestLunaEngineAnalyze:
    def test_returns_analysis(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert a is not None
        assert a.symbol == "SOL"

    def test_luna_index_in_range(self):
        engine = LunaEngine()
        assert 0 <= engine.analyze(make_snap()).luna_index <= 100

    def test_five_scores_populated(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        for score in [
            a.whale_flow_score, a.holder_velocity_score, a.liquidity_depth_score,
            a.fee_pressure_score, a.supply_shock_score,
        ]:
            assert 0 <= score <= 100

    def test_bullish_snap_bullish_result(self, bullish_snap):
        engine = LunaEngine()
        a = engine.analyze(bullish_snap)
        assert a.luna_index > 50

    def test_bearish_snap_bearish_result(self, bearish_snap):
        engine = LunaEngine()
        a = engine.analyze(bearish_snap)
        assert a.luna_index < 50

    def test_neutral_snap_near_neutral(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert 30 <= a.luna_index <= 70

    def test_phase_matches_index(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert a.luna_phase == _phase_from_index(a.luna_index)

    def test_dominant_signal_is_valid(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        valid = {"whale_flow", "holder_velocity", "liquidity_depth", "fee_pressure", "supply_shock", "none"}
        assert a.dominant_signal in valid

    def test_bullish_bearish_are_lists(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert isinstance(a.bullish_signals, list)
        assert isinstance(a.bearish_signals, list)

    def test_conviction_in_range(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert 0 <= a.conviction <= 1

    def test_alignment_in_range(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert 0 <= a.signal_alignment <= 1

    def test_cycle_momentum_in_range(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert -1 <= a.cycle_momentum <= 1

    def test_reasoning_non_empty(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert isinstance(a.reasoning, str) and len(a.reasoning) > 10

    def test_warning_flags_is_list(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert isinstance(a.warning_flags, list)

    def test_custom_weights_accepted(self):
        custom = {
            "whale_flow": 0.4, "supply_shock": 0.2,
            "holder_velocity": 0.2, "liquidity_depth": 0.1, "fee_pressure": 0.1,
        }
        engine = LunaEngine(weights=custom)
        a = engine.analyze(make_snap())
        assert 0 <= a.luna_index <= 100

    def test_phase_duration_none_or_int(self):
        engine = LunaEngine()
        a = engine.analyze(make_snap())
        assert a.phase_duration_estimate is None or isinstance(a.phase_duration_estimate, int)
