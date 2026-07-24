# Spring–Mass–Damper System

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Spring-Mass-Damper.exe"><img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS-.EXE-0078D4?style=for-the-badge&logo=windows&logoColor=white" height="68" alt="Download Spring-Mass-Damper for Windows (.exe)"></a>
</p>

<p align="center"><strong>Download, double-click, and start exploring — no Python needed.</strong><br>
<em>Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Spring%20Mass%20Damper%20System">Download the source folder</a>.</em></p>

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
