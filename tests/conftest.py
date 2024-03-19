"""Shared fixtures for LunaFlux tests."""

import pytest
from lunaflux.models import ChainSnapshot


def make_snap(
    symbol="SOL",
    timestamp=1700000000.0,
    whale_inflow_usd=5_000_000.0,
    whale_outflow_usd=5_000_000.0,
    whale_tx_count=20,
    holder_count=100_000,
    holder_count_7d_ago=98_000,
    holder_count_30d_ago=92_000,
    liquidity_usd=20_000_000.0,
    liquidity_7d_ago=20_000_000.0,
    volume_24h=4_000_000.0,
    volume_7d_avg=4_000_000.0,
    avg_fee_usd=0.002,
    avg_fee_7d_ago=0.002,
    tx_count_24h=50_000,
    tx_count_7d_avg=50_000.0,
    exchange_inflow_24h=1_000_000.0,
    exchange_outflow_24h=1_000_000.0,
    exchange_balance_pct=12.0,
    exchange_balance_7d_ago=12.0,
) -> ChainSnapshot:
    return ChainSnapshot(
        symbol=symbol,
        timestamp=timestamp,
        whale_inflow_usd=whale_inflow_usd,
        whale_outflow_usd=whale_outflow_usd,
        whale_tx_count=whale_tx_count,
        holder_count=holder_count,
        holder_count_7d_ago=holder_count_7d_ago,
        holder_count_30d_ago=holder_count_30d_ago,
        liquidity_usd=liquidity_usd,
        liquidity_7d_ago=liquidity_7d_ago,
        volume_24h=volume_24h,
        volume_7d_avg=volume_7d_avg,
        avg_fee_usd=avg_fee_usd,
        avg_fee_7d_ago=avg_fee_7d_ago,
        tx_count_24h=tx_count_24h,
        tx_count_7d_avg=tx_count_7d_avg,
        exchange_inflow_24h=exchange_inflow_24h,
        exchange_outflow_24h=exchange_outflow_24h,
        exchange_balance_pct=exchange_balance_pct,
        exchange_balance_7d_ago=exchange_balance_7d_ago,
    )


@pytest.fixture
def neutral_snap():
    return make_snap()


@pytest.fixture
def bullish_snap():
    return make_snap(
        whale_inflow_usd=2_000_000.0,
        whale_outflow_usd=18_000_000.0,
        whale_tx_count=60,
        holder_count=115_000,
        holder_count_7d_ago=100_000,
        holder_count_30d_ago=88_000,
        liquidity_usd=30_000_000.0,
        liquidity_7d_ago=22_000_000.0,
        volume_24h=9_000_000.0,
        volume_7d_avg=5_000_000.0,
        avg_fee_usd=0.004,
        avg_fee_7d_ago=0.002,
        tx_count_24h=80_000,
        tx_count_7d_avg=50_000.0,
        exchange_inflow_24h=500_000.0,
        exchange_outflow_24h=8_000_000.0,
        exchange_balance_pct=8.0,
        exchange_balance_7d_ago=11.0,
    )


@pytest.fixture
def bearish_snap():
    return make_snap(
        whale_inflow_usd=15_000_000.0,
        whale_outflow_usd=2_000_000.0,
        whale_tx_count=40,
        holder_count=92_000,
        holder_count_7d_ago=100_000,
        holder_count_30d_ago=104_000,
        liquidity_usd=12_000_000.0,
        liquidity_7d_ago=20_000_000.0,
        volume_24h=2_000_000.0,
        volume_7d_avg=6_000_000.0,
        avg_fee_usd=0.001,
        avg_fee_7d_ago=0.003,
        tx_count_24h=25_000,
        tx_count_7d_avg=55_000.0,
        exchange_inflow_24h=12_000_000.0,
        exchange_outflow_24h=1_500_000.0,
        exchange_balance_pct=22.0,
        exchange_balance_7d_ago=16.0,
    )
