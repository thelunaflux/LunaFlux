# Contributing to LunaFlux

## Setup

```bash
git clone https://github.com/lunafluxdev/LunaFlux
cd LunaFlux
pip install -e ".[dev]"
pytest tests/ -v
```

## Adding a Signal

1. Create `lunaflux/signals/your_signal.py` — implement `compute(snap: ChainSnapshot) -> SignalResult`
2. Register in `lunaflux/signals/__init__.py` and add to `ALL_SIGNALS`
3. Add weight in `lunaflux/engine.py` — weights must sum to 1.0
4. Write tests in `tests/test_signals_your_signal.py`

## Signal Conventions

- Score: 0–100 (50 = neutral, >55 = bullish, <45 = bearish)
- Strength: `abs(score - 50) / 50`
- Bias: `BULLISH` / `BEARISH` / `NEUTRAL`
- Detail: human-readable single line with key numbers

## Pull Requests

- Branch naming: `feature/signal-name` or `fix/issue`
- Tests must pass before review
- Describe the on-chain logic and data sources used