# Spring–Mass–Damper System

Animates the response of a classic spring–mass–damper system — a cart on a spring
with a damper — showing how it settles over time.

## Run it

```bash
pip install -r requirements.txt
python smd.py
```

Opens fullscreen at 1920×1080.

## Controls

| Input | Action |
|-------|--------|
| `Space` | Start the simulation |
| `Esc` | Quit |

## Requirements

`pygame`, `numpy` (see `requirements.txt`). The demo loads its `spring.png`,
`damp1.png`, and `damp2.png` images from this folder, so run it from here.
