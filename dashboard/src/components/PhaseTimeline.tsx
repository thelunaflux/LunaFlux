import React from 'react';
import type { LunaPhase } from '../types';

interface PhaseTimelineProps {
  currentPhase: LunaPhase;
  lunaIndex: number;
  durationEstimate: number | null;
  alignment: number;
  bullishSignals: string[];
  bearishSignals: string[];
  warnings: string[];
}

const PHASES: { key: LunaPhase; label: string; color: string; range: string }[] = [
  { key: 'contraction',  label: 'Contraction',  color: '#ef4444', range: '0–24'  },
  { key: 'accumulation', label: 'Accumulation', color: '#f59e0b', range: '25–49' },
  { key: 'expansion',    label: 'Expansion',    color: '#22c55e', range: '50–74' },
  { key: 'distribution', label: 'Distribution', color: '#a855f7', range: '75–100'},
];

export const PhaseTimeline: React.FC<PhaseTimelineProps> = ({
  currentPhase, lunaIndex, durationEstimate, alignment, bullishSignals, bearishSignals, warnings,
}) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
    {/* Phase arc */}
    <div style={{ background: '#111827', borderRadius: 10, border: '1px solid #1f2937', padding: '14px 16px' }}>
      <div style={{ fontSize: 11, color: '#6b7280', marginBottom: 10, textTransform: 'uppercase' }}>Market Cycle</div>
      <div style={{ display: 'flex', gap: 4 }}>
        {PHASES.map(p => (
          <div key={p.key} style={{
            flex: 1, height: 6, borderRadius: 99,
            background: p.key === currentPhase ? p.color : '#1f2937',
            transition: 'background 0.3s',
          }} />
        ))}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
        {PHASES.map(p => (
          <div key={p.key} style={{ fontSize: 10, color: p.key === currentPhase ? p.color : '#374151', textAlign: 'center', flex: 1 }}>
            {p.label}
          </div>
        ))}
      </div>
      {durationEstimate && (
        <div style={{ fontSize: 11, color: '#6b7280', marginTop: 10 }}>
          Est. phase duration: ~{durationEstimate}d remaining
        </div>
      )}
    </div>

    {/* Alignment */}
    <div style={{ background: '#111827', borderRadius: 10, border: '1px solid #1f2937', padding: '14px 16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
        <span style={{ fontSize: 11, color: '#6b7280', textTransform: 'uppercase' }}>Signal Alignment</span>
        <span style={{ fontSize: 12, color: alignment > 0.7 ? '#22c55e' : '#6b7280' }}>{(alignment * 100).toFixed(0)}%</span>
      </div>
      <div style={{ height: 4, background: '#1f2937', borderRadius: 99 }}>
        <div style={{ height: '100%', width: `${alignment * 100}%`, background: '#22c55e', borderRadius: 99 }} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginTop: 12 }}>
        <div>
          <div style={{ fontSize: 10, color: '#22c55e', marginBottom: 4 }}>BULLISH</div>
          {bullishSignals.map(s => <div key={s} style={{ fontSize: 11, color: '#9ca3af' }}>• {s.replace(/_/g, ' ')}</div>)}
        </div>
        <div>
          <div style={{ fontSize: 10, color: '#ef4444', marginBottom: 4 }}>BEARISH</div>
          {bearishSignals.length === 0
            ? <div style={{ fontSize: 11, color: '#374151' }}>none</div>
            : bearishSignals.map(s => <div key={s} style={{ fontSize: 11, color: '#9ca3af' }}>• {s.replace(/_/g, ' ')}</div>)
          }
        </div>
      </div>
    </div>

    {warnings.length > 0 && (
      <div style={{ background: '#111827', borderRadius: 10, border: '1px solid #1f2937', padding: '14px 16px' }}>
        <div style={{ fontSize: 11, color: '#f59e0b', marginBottom: 6, textTransform: 'uppercase' }}>Warnings</div>
        {warnings.map(w => <div key={w} style={{ fontSize: 11, color: '#9ca3af' }}>⚠ {w.replace(/_/g, ' ')}</div>)}
      </div>
    )}
  </div>
);