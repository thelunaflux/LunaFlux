import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, Cell, ResponsiveContainer } from 'recharts';

interface SignalMatrixProps {
  scores: { name: string; score: number }[];
}

const LABELS: Record<string, string> = {
  whale_flow:       'Whale Flow',
  supply_shock:     'Supply Shock',
  holder_velocity:  'Holder Velocity',
  liquidity_depth:  'Liquidity',
  fee_pressure:     'Fee Pressure',
};

const getColor = (score: number) => {
  if (score > 65) return '#22c55e';
  if (score > 55) return '#86efac';
  if (score < 35) return '#ef4444';
  if (score < 45) return '#fca5a5';
  return '#6b7280';
};

export const SignalMatrix: React.FC<SignalMatrixProps> = ({ scores }) => {
  const data = scores.map(s => ({ name: LABELS[s.name] ?? s.name, score: s.score }));

  return (
    <div style={{ padding: '16px 0' }}>
      <h3 style={{ fontSize: 12, color: '#6b7280', marginBottom: 12, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
        On-Chain Signals
      </h3>
      <ResponsiveContainer width="100%" height={210}>
        <BarChart data={data} layout="vertical" margin={{ left: 16, right: 24, top: 4, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" horizontal={false} />
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11, fill: '#6b7280' }} />
          <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: '#9ca3af' }} width={88} />
          <Tooltip
            contentStyle={{ background: '#111827', border: '1px solid #1f2937', borderRadius: 6, fontSize: 12 }}
            formatter={(val: number) => [`${val.toFixed(1)}/100`, 'Score']}
          />
          <ReferenceLine x={50} stroke="#374151" strokeDasharray="4 4" />
          <Bar dataKey="score" radius={[0, 3, 3, 0]}>
            {data.map((entry, i) => <Cell key={i} fill={getColor(entry.score)} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};