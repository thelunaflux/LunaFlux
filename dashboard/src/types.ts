export type SignalBias = 'bullish' | 'bearish' | 'neutral';
export type LunaPhase = 'contraction' | 'accumulation' | 'expansion' | 'distribution';

export interface LunaAnalysis {
  symbol: string;
  whale_flow_score: number;
  holder_velocity_score: number;
  liquidity_depth_score: number;
  fee_pressure_score: number;
  supply_shock_score: number;
  luna_index: number;
  luna_phase: LunaPhase;
  cycle_momentum: number;
  phase_duration_estimate: number | null;
  dominant_signal: string;
  bullish_signals: string[];
  bearish_signals: string[];
  warning_flags: string[];
  bias: SignalBias;
  conviction: number;
  signal_alignment: number;
  reasoning: string;
}