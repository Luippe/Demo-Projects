# Spring–Mass–Damper System

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Spring-Mass-Damper.exe"><img src="https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white" height="50" alt="Download for Windows (.exe)"></a>
</p>

<p align="center"><em>No Python needed — download and double-click. Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Spring%20Mass%20Damper%20System">Grab the source folder</a>.</em></p>

## Controls

| Input | Action |
|-------|--------|
| `Space` | Start the simulation |
| `Esc` | Quit |

Animates the response of a classic spring–mass–damper system — a cart on a spring
with a damper — showing how it settles over time.

## Run it

```bash
pip install -r requirements.txt
python smd.py
```

Opens fullscreen at 1920×1080.

## Requirements

`pygame`, `numpy` (see `requirements.txt`). The demo loads its `spring.png`,
`damp1.png`, and `damp2.png` images from this folder, so run it from here.
