# Pathfinding Visualization

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Pathfinding-Visualization.exe"><img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS-.EXE-0078D4?style=for-the-badge&logo=windows&logoColor=white" height="68" alt="Download Pathfinding Visualization for Windows (.exe)"></a>
</p>

<p align="center"><strong>Download, double-click, and start exploring — no Python needed.</strong><br>
<em>Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Pathfinding%20Visualization">Download the source folder</a>.</em></p>

## Controls

| Input | Action |
|-------|--------|
| Left-click / drag | Place walls |
| Right-click / drag | Erase walls |
| `S` | Set the start cell (at the mouse) |
| `G` | Set the goal cell (at the mouse) |
| `Esc` | Quit |

Draw walls on a grid, set a start and a goal, and watch a path-search algorithm
find its way through in real time.

## Run it

```bash
pip install -r requirements.txt
python path_finding.py
```

Opens fullscreen at 1920×1080.

## Requirements

`pygame`, `numpy` (see `requirements.txt`).
