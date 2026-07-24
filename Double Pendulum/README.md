# Double Pendulum

[![Download for Windows](https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Double-Pendulum.exe)

*No Python needed — download and double-click. Prefer the code? [Grab the source folder](https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Double%20Pendulum).*

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
