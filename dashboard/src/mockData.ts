import type { LunaAnalysis } from './types';

export const mockAnalysis: LunaAnalysis = {
  symbol: 'SOL',
  whale_flow_score: 68.0,
  holder_velocity_score: 72.0,
  liquidity_depth_score: 63.0,
  fee_pressure_score: 60.0,
  supply_shock_score: 74.0,
  luna_index: 69.35,
  luna_phase: 'expansion',
  cycle_momentum: 0.38,
  phase_duration_estimate: 48,
  dominant_signal: 'supply_shock',
  bullish_signals: ['whale_flow', 'holder_velocity', 'liquidity_depth', 'fee_pressure', 'supply_shock'],
  bearish_signals: [],
  warning_flags: [],
  bias: 'bullish',
  conviction: 0.387,
  signal_alignment: 1.0,
  reasoning: 'Luna index 69.4/100 → expansion. On-chain bias bullish: 5 bullish, 0 bearish signals. Whales accumulating — institutional interest confirmed. Exchange outflows dominant — supply leaving markets. Holder growth accelerating — organic adoption expanding.',
};