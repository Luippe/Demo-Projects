# Double Pendulum

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Double-Pendulum.exe"><img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS-.EXE-0078D4?style=for-the-badge&logo=windows&logoColor=white" height="68" alt="Download Double Pendulum for Windows (.exe)"></a>
</p>

<p align="center"><strong>Download, double-click, and start exploring — no Python needed.</strong><br>
<em>Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Double%20Pendulum">Download the source folder</a>.</em></p>

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
