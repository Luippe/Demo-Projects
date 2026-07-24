# Flow Plate

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Flow-Plate.exe"><img src="https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white" height="50" alt="Download for Windows (.exe)"></a>
</p>

<p align="center"><em>No Python needed — download and double-click. Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Flow%20Plate">Grab the source folder</a>.</em></p>

## Controls

| Input | Action |
|-------|--------|
| `Esc` | Quit |

Mostly a visual readout — there's no interaction beyond quitting.

Computes and displays the velocity profile of laminar flow through a pipe, using
tabulated material properties (air, ammonia, engine oil, water).

## Run it

Run it **from inside this folder** — it reads `Material Properties.txt` and
`Water Properties.txt` by relative path:

```bash
pip install -r requirements.txt
python Flow_Plate.py
```

Opens fullscreen at 1920×1080.

## Files

- `Flow_Plate.py` — the simulation.
- `Properties.py` — helper that loads the material-property tables.
- `Material Properties.txt`, `Water Properties.txt` — the data tables.

## Requirements

`pygame`, `numpy`, `scipy` (see `requirements.txt`).
