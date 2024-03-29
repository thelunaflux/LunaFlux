import React from 'react';
import type { LunaPhase } from '../types';

interface CycleGaugeProps {
  index: number;
  phase: LunaPhase;
  conviction: number;
  momentum: number;
}

const PHASE_COLORS: Record<LunaPhase, string> = {
  contraction:  '#ef4444',
  accumulation: '#f59e0b',
  expansion:    '#22c55e',
  distribution: '#a855f7',
};

const PHASE_LABELS: Record<LunaPhase, string> = {
  contraction:  'CONTRACTION',
  accumulation: 'ACCUMULATION',
  expansion:    'EXPANSION',
  distribution: 'DISTRIBUTION',
};

export const CycleGauge: React.FC<CycleGaugeProps> = ({ index, phase, conviction, momentum }) => {
  const color = PHASE_COLORS[phase];
  const label = PHASE_LABELS[phase];

  return (
    <div style={{ textAlign: 'center', padding: '24px' }}>
      <div style={{
        width: 160, height: 160, borderRadius: '50%',
        border: `8px solid ${color}`,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        margin: '0 auto 16px', background: `${color}18`,
      }}>
        <span style={{ fontSize: 36, fontWeight: 700, color }}>{index.toFixed(1)}</span>
        <span style={{ fontSize: 11, color: '#6b7280', marginTop: 2 }}>LUNA INDEX</span>
      </div>
      <div style={{ fontSize: 13, fontWeight: 600, color, letterSpacing: '0.08em' }}>{label}</div>
      <div style={{ fontSize: 12, color: '#6b7280', marginTop: 6 }}>
        Conviction {(conviction * 100).toFixed(0)}% · Momentum {momentum > 0 ? '+' : ''}{momentum.toFixed(2)}
      </div>
    </div>
  );
};