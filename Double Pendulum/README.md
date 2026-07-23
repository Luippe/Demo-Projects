# Double Pendulum

Simulates the chaotic motion of a double pendulum by numerically integrating its
equations of motion. Small differences in the start lead to wildly different
paths — the classic demonstration of chaos.

## Run it

```bash
pip install -r requirements.txt
python double_pendulum.py
```

Opens fullscreen at 1920×1080.

## Controls

| Input | Action |
|-------|--------|
| `Space` | Start the simulation |
| `Esc` | Quit |

## Requirements

`pygame`, `numpy`, `scipy` (see `requirements.txt`).
