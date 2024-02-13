"""Core data models for LunaFlux."""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class LunaPhase(str, Enum):
    CONTRACTION  = "contraction"   # 0-24:  Bear, selling pressure dominant
    ACCUMULATION = "accumulation"  # 25-49: Smart money quietly buying
    EXPANSION    = "expansion"     # 50-74: Bull phase confirmed, growth
    DISTRIBUTION = "distribution"  # 75-100: Smart money exiting, top formation


class SignalBias(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass
class ChainSnapshot:
    """Point-in-time on-chain market data for a single token/asset."""
    symbol: str
    timestamp: float

    # Whale flow
    whale_inflow_usd: float      # Large wallet inflows (>$100k txns) last 24h
    whale_outflow_usd: float     # Large wallet outflows last 24h
    whale_tx_count: int          # Number of whale transactions

    # Holder data
    holder_count: int            # Current unique holder count
    holder_count_7d_ago: int     # Holder count 7 days ago
    holder_count_30d_ago: int    # Holder count 30 days ago

    # Liquidity depth (DEX)
    liquidity_usd: float         # Total DEX liquidity in USD
    liquidity_7d_ago: float      # Liquidity 7 days ago
    volume_24h: float            # 24h DEX trading volume
    volume_7d_avg: float         # 7-day average daily volume

    # Fee / network demand
    avg_fee_usd: float           # Average tx fee in USD (24h)
    avg_fee_7d_ago: float        # Average tx fee 7 days ago
    tx_count_24h: int            # Total on-chain transactions 24h
    tx_count_7d_avg: float       # 7-day average daily tx count

    # Supply shock (exchange flows)
    exchange_inflow_24h: float   # Tokens sent TO exchanges (sell pressure)
    exchange_outflow_24h: float  # Tokens withdrawn FROM exchanges (hold signal)
    exchange_balance_pct: float  # % of supply on exchanges (0-100)
    exchange_balance_7d_ago: float  # Exchange balance % 7 days ago

    metadata: dict = field(default_factory=dict)


@dataclass
class SignalResult:
    """Result from a single LunaFlux signal."""
    signal_name: str
    score: float       # 0-100 (50 = neutral, >55 = bullish, <45 = bearish)
    bias: SignalBias
    strength: float    # 0-1
    detail: str


@dataclass
class LunaAnalysis:
    """Full LunaFlux on-chain cycle analysis output."""
    symbol: str

    # 5 signal scores
    whale_flow_score: float
    holder_velocity_score: float
    liquidity_depth_score: float
    fee_pressure_score: float
    supply_shock_score: float

    # Aggregated
    luna_index: float           # 0-100 weighted composite
    luna_phase: LunaPhase
    cycle_momentum: float       # -1 to 1, rate of phase change
    phase_duration_estimate: Optional[int]  # estimated days in current phase

    # Breakdown
    dominant_signal: str
    bullish_signals: list[str]
    bearish_signals: list[str]
    warning_flags: list[str]

    # Action
    bias: SignalBias
    conviction: float       # 0-1
    signal_alignment: float # 0-1
    reasoning: str
