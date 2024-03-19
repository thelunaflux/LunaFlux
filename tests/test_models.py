"""Tests for LunaFlux core models."""

import pytest
from lunaflux.models import ChainSnapshot, LunaAnalysis, LunaPhase, SignalBias, SignalResult
from tests.conftest import make_snap


class TestLunaPhase:
    def test_four_phases_exist(self):
        assert len(list(LunaPhase)) == 4

    def test_phase_values(self):
        assert LunaPhase.CONTRACTION  == "contraction"
        assert LunaPhase.ACCUMULATION == "accumulation"
        assert LunaPhase.EXPANSION    == "expansion"
        assert LunaPhase.DISTRIBUTION == "distribution"

    def test_phase_is_string_enum(self):
        assert isinstance(LunaPhase.EXPANSION, str)


class TestSignalBias:
    def test_three_biases(self):
        assert len(list(SignalBias)) == 3

    def test_bias_values(self):
        assert SignalBias.BULLISH == "bullish"
        assert SignalBias.BEARISH == "bearish"
        assert SignalBias.NEUTRAL == "neutral"


class TestChainSnapshot:
    def test_create_basic(self):
        snap = make_snap()
        assert snap.symbol == "SOL"
        assert snap.holder_count == 100_000

    def test_default_metadata_empty(self):
        snap = make_snap()
        assert snap.metadata == {}

    def test_all_fields_accessible(self):
        snap = make_snap()
        for field in [
            "whale_inflow_usd", "whale_outflow_usd", "whale_tx_count",
            "holder_count", "holder_count_7d_ago", "holder_count_30d_ago",
            "liquidity_usd", "liquidity_7d_ago", "volume_24h", "volume_7d_avg",
            "avg_fee_usd", "avg_fee_7d_ago", "tx_count_24h", "tx_count_7d_avg",
            "exchange_inflow_24h", "exchange_outflow_24h",
            "exchange_balance_pct", "exchange_balance_7d_ago",
        ]:
            assert hasattr(snap, field)

    def test_zero_whale_flow_allowed(self):
        snap = make_snap(whale_inflow_usd=0.0, whale_outflow_usd=0.0)
        assert snap.whale_inflow_usd == 0.0

    def test_metadata_is_mutable(self):
        snap = make_snap()
        snap.metadata["source"] = "dune"
        assert snap.metadata["source"] == "dune"


class TestSignalResult:
    def test_create(self):
        r = SignalResult(
            signal_name="whale_flow",
            score=72.0,
            bias=SignalBias.BULLISH,
            strength=0.44,
            detail="test",
        )
        assert r.signal_name == "whale_flow"
        assert r.score == 72.0
        assert r.bias == SignalBias.BULLISH
