"""LunaFlux signal modules."""

from .whale_flow import WhaleFlowSignal
from .holder_velocity import HolderVelocitySignal
from .liquidity_depth import LiquidityDepthSignal
from .fee_pressure import FeePressureSignal
from .supply_shock import SupplyShockSignal

ALL_SIGNALS = [
    WhaleFlowSignal(),
    HolderVelocitySignal(),
    LiquidityDepthSignal(),
    FeePressureSignal(),
    SupplyShockSignal(),
]

__all__ = [
    "WhaleFlowSignal",
    "HolderVelocitySignal",
    "LiquidityDepthSignal",
    "FeePressureSignal",
    "SupplyShockSignal",
    "ALL_SIGNALS",
]
