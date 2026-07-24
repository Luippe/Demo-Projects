# Double Pendulum

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Double-Pendulum.exe"><img src="https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white" height="50" alt="Download for Windows (.exe)"></a>
</p>

<p align="center"><em>No Python needed — download and double-click. Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Double%20Pendulum">Grab the source folder</a>.</em></p>

## Controls

| Input | Action |
|-------|--------|
| `Space` | Start the simulation |
| `Esc` | Quit |

Simulates the chaotic motion of a double pendulum by numerically integrating its
equations of motion. Small differences in the start lead to wildly different
paths — the classic demonstration of chaos.

## Run it

```bash
pip install -r requirements.txt
python double_pendulum.py
```

Opens fullscreen at 1920×1080.

## Requirements

`pygame`, `numpy`, `scipy` (see `requirements.txt`).
