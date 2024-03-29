import React, { useState } from 'react';
import type { LunaAnalysis } from './types';
import { CycleGauge } from './components/CycleGauge';
import { SignalMatrix } from './components/SignalMatrix';
import { PhaseTimeline } from './components/PhaseTimeline';
import { mockAnalysis } from './mockData';

const SIGNAL_KEYS = [
  'whale_flow_score', 'supply_shock_score', 'holder_velocity_score',
  'liquidity_depth_score', 'fee_pressure_score',
] as const;

const SIGNAL_NAMES: Record<string, string> = {
  whale_flow_score: 'whale_flow', supply_shock_score: 'supply_shock',
  holder_velocity_score: 'holder_velocity', liquidity_depth_score: 'liquidity_depth',
  fee_pressure_score: 'fee_pressure',
};

const BIAS_COLOR = { bullish: '#22c55e', bearish: '#ef4444', neutral: '#6b7280' } as const;

export default function App() {
  const [a] = useState<LunaAnalysis>(mockAnalysis);
  const scores = SIGNAL_KEYS.map(k => ({ name: SIGNAL_NAMES[k], score: a[k] }));

  return (
    <div style={{ minHeight: '100vh', background: '#030712', color: '#e5e7eb', fontFamily: 'monospace' }}>
      <div style={{ borderBottom: '1px solid #1f2937', padding: '14px 28px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <span style={{ fontSize: 17, fontWeight: 700, color: '#f9fafb', letterSpacing: '0.04em' }}>🌙 LUNAFLUX</span>
          <span style={{ fontSize: 11, color: '#4b5563', marginLeft: 10 }}>on-chain cycle engine</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: 13, color: '#4b5563' }}>{a.symbol}</span>
          <span style={{
            fontSize: 11, fontWeight: 600, padding: '3px 10px', borderRadius: 99,
            border: `1px solid ${BIAS_COLOR[a.bias]}`, color: BIAS_COLOR[a.bias], textTransform: 'uppercase',
          }}>{a.bias}</span>
        </div>
      </div>

      <div style={{ maxWidth: 1080, margin: '0 auto', padding: '28px 20px', display: 'grid', gridTemplateColumns: '200px 1fr 280px', gap: 20 }}>
        <div style={{ background: '#111827', borderRadius: 12, border: '1px solid #1f2937' }}>
          <CycleGauge index={a.luna_index} phase={a.luna_phase} conviction={a.conviction} momentum={a.cycle_momentum} />
          <div style={{ padding: '0 20px 18px', borderTop: '1px solid #1f2937' }}>
            <div style={{ fontSize: 10, color: '#6b7280', marginTop: 12, marginBottom: 4, textTransform: 'uppercase' }}>Dominant</div>
            <div style={{ fontSize: 12, color: '#e5e7eb' }}>{a.dominant_signal.replace(/_/g, ' ')}</div>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={{ background: '#111827', borderRadius: 12, border: '1px solid #1f2937', padding: '16px 18px' }}>
            <SignalMatrix scores={scores} />
          </div>
          <div style={{ background: '#111827', borderRadius: 12, border: '1px solid #1f2937', padding: '16px 18px' }}>
            <div style={{ fontSize: 11, color: '#6b7280', marginBottom: 8, textTransform: 'uppercase' }}>Analysis</div>
            <p style={{ fontSize: 12, color: '#9ca3af', lineHeight: 1.65, margin: 0 }}>{a.reasoning}</p>
          </div>
        </div>

        <PhaseTimeline
          currentPhase={a.luna_phase}
          lunaIndex={a.luna_index}
          durationEstimate={a.phase_duration_estimate}
          alignment={a.signal_alignment}
          bullishSignals={a.bullish_signals}
          bearishSignals={a.bearish_signals}
          warnings={a.warning_flags}
        />
      </div>
    </div>
  );
}