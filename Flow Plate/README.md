# Flow Plate

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Flow-Plate.exe"><img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS-.EXE-0078D4?style=for-the-badge&logo=windows&logoColor=white" height="68" alt="Download Flow Plate for Windows (.exe)"></a>
</p>

<p align="center"><strong>Download, double-click, and start exploring — no Python needed.</strong><br>
<em>Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Flow%20Plate">Download the source folder</a>.</em></p>

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
