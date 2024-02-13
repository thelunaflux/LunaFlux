"""
LunaFlux — On-Chain Market Cycle Engine.

Five on-chain signals → one luna_index → four market phases.
"""

from .engine import LunaEngine, WEIGHTS
from .models import (
    ChainSnapshot,
    LunaAnalysis,
    LunaPhase,
    SignalBias,
    SignalResult,
)
from .signals import (
    WhaleFlowSignal,
    HolderVelocitySignal,
    LiquidityDepthSignal,
    FeePressureSignal,
    SupplyShockSignal,
    ALL_SIGNALS,
)

__version__ = "0.1.0"
__all__ = [
    "LunaEngine",
    "WEIGHTS",
    "ChainSnapshot",
    "LunaAnalysis",
    "LunaPhase",
    "SignalBias",
    "SignalResult",
    "WhaleFlowSignal",
    "HolderVelocitySignal",
    "LiquidityDepthSignal",
    "FeePressureSignal",
    "SupplyShockSignal",
    "ALL_SIGNALS",
]
