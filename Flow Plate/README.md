# Flow Plate

Computes and displays the velocity profile of laminar flow through a pipe, using
tabulated material properties (air, ammonia, engine oil, water).

## Run it

Run it **from inside this folder** — it reads `Material Properties.txt` and
`Water Properties.txt` by relative path:

```bash
pip install -r requirements.txt
python "Flow Plate.py"
```

> The script name contains a space, so keep the quotes.

Opens fullscreen at 1920×1080.

## Controls

| Input | Action |
|-------|--------|
| `Esc` | Quit |

Mostly a visual readout — there's no interaction beyond quitting.

## Files

- `Flow Plate.py` — the simulation.
- `Properties.py` — helper that loads the material-property tables.
- `Material Properties.txt`, `Water Properties.txt` — the data tables.

## Requirements

`pygame`, `numpy`, `scipy` (see `requirements.txt`).
