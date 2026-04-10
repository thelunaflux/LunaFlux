<div align="center">

> `$LNFLX : 5VzzNYxeNMYjVB46skvycPyrzskDAXaK2s4Smbrcpump`

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:030712,100:7c3aed&height=200&section=header&text=LunaFlux&fontSize=58&fontColor=f9fafb&fontAlignY=38&desc=On-Chain%20Market%20Cycle%20Engine&descAlignY=58&descSize=18" width="100%"/>

[![Tests](https://github.com/lunafluxdev/LunaFlux/actions/workflows/test.yml/badge.svg)](https://github.com/lunafluxdev/LunaFlux/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-7c3aed?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178c6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-374151?style=flat-square)](LICENSE)

</div>

---

Price is a lagging indicator. By the time the chart confirms what's happening, the cycle is already halfway through. LunaFlux reads what's underneath — whale wallet movements, holder adoption rates, exchange supply dynamics, liquidity flows, and on-chain fee demand — then maps them to a four-phase market cycle.

The output is a single number, the **luna index**, and four words: Contraction, Accumulation, Expansion, Distribution.

---

## The Cycle

```
0 ─────────── 25 ─────────── 50 ─────────── 75 ─────── 100
  CONTRACTION   ACCUMULATION      EXPANSION    DISTRIBUTION
  Bears winning  Smart money in   Bull confirmed  Exits building
```

LunaFlux classifies where a token sits on this arc using five independent on-chain signals. Each signal scores 0–100. The engine weights and combines them into the luna index.

---

## Architecture

```
ChainSnapshot (raw on-chain data)
        │
        ▼
  ┌─────────────────────────────────────────┐
  │  WhaleFlowSignal     → wallet direction │
  │  SupplyShockSignal   → exchange balance │
  │  HolderVelocitySignal → adoption rate  │
  │  LiquidityDepthSignal → DEX health     │
  │  FeePressureSignal   → network demand  │
  └─────────────────────────────────────────┘
        │  weighted composite (5 signals)
        ▼
   LunaAnalysis
    • luna_index        (0–100)
    • luna_phase        (contraction → distribution)
    • cycle_momentum    (-1 to 1)
    • dominant_signal
    • conviction + alignment
    • reasoning
```

---

## Signal Weights

| Signal | Weight | What it measures |
|--------|--------|-----------------|
| Whale Flow | **30%** | Large wallet inflow vs outflow direction |
| Supply Shock | **25%** | Exchange balance changes (leaving = bullish) |
| Holder Velocity | **20%** | Rate of new holder adoption |
| Liquidity Depth | **15%** | DEX pool health and utilization |
| Fee Pressure | **10%** | On-chain demand via tx fees and count |

---

## Install

```bash
pip install lunaflux
```

Or from source:

```bash
git clone https://github.com/lunafluxdev/LunaFlux
cd LunaFlux
pip install -e ".[dev]"
```

---

## Usage

```python
from lunaflux import LunaEngine, ChainSnapshot

engine = LunaEngine()

snap = ChainSnapshot(
    symbol="SOL",
    timestamp=1700000000.0,
    whale_inflow_usd=2_100_000,
    whale_outflow_usd=18_400_000,
    whale_tx_count=62,
    holder_count=118_000,
    holder_count_7d_ago=102_000,
    holder_count_30d_ago=90_000,
    liquidity_usd=32_000_000,
    liquidity_7d_ago=24_000_000,
    volume_24h=11_000_000,
    volume_7d_avg=5_500_000,
    avg_fee_usd=0.0038,
    avg_fee_7d_ago=0.0021,
    tx_count_24h=82_000,
    tx_count_7d_avg=51_000,
    exchange_inflow_24h=420_000,
    exchange_outflow_24h=9_200_000,
    exchange_balance_pct=7.4,
    exchange_balance_7d_ago=11.8,
)

analysis = engine.analyze(snap)

print(f"Luna Index:  {analysis.luna_index:.1f}")
print(f"Phase:       {analysis.luna_phase.value}")
print(f"Momentum:    {analysis.cycle_momentum:+.2f}")
print(f"Conviction:  {analysis.conviction:.1%}")
print(f"Dominant:    {analysis.dominant_signal}")
print(f"Reasoning:   {analysis.reasoning}")
```

---

## Dashboard

```bash
cd dashboard
npm install
npm run dev
# → http://localhost:3000
```

Cycle gauge, signal bar chart, phase timeline, alignment panel.

---

## Tests

```bash
pytest tests/ -v
# 132 tests covering all 5 signals, engine, and utils
```

---

## Docker

```bash
docker compose up
```

---

<details>
<summary>日本語 README</summary>

## LunaFlux — オンチェーン市場サイクルエンジン

価格は遅行指標。LunaFlux はその下にあるオンチェーンデータを読む。

**5つのシグナル**から**ルナインデックス**（0〜100）を算出し、市場の4つのフェーズに分類する。

### 市場サイクル

```
0 ──────── 25 ──────── 50 ──────── 75 ─── 100
  収縮期      蓄積期        拡張期    分配期
```

### シグナル

| シグナル | 重み | 測定内容 |
|---------|------|---------|
| クジラフロー | 30% | 大口ウォレットの方向性 |
| 供給ショック | 25% | 取引所残高変化 |
| ホルダー速度 | 20% | 新規ホルダー獲得率 |
| 流動性深度 | 15% | DEXプール健全性 |
| 手数料圧力 | 10% | オンチェーン需要指標 |

### インストール

```bash
pip install lunaflux
```

### テスト

```bash
pytest tests/ -v
# 132テスト全てパス
```

</details>

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3aed,100:030712&height=100&section=footer" width="100%"/>
</div>