# Pathfinding Visualization

[![Download for Windows](https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Pathfinding-Visualization.exe)

*No Python needed — download and double-click. Prefer the code? [Grab the source folder](https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Pathfinding%20Visualization).*

Draw walls on a grid, set a start and a goal, and watch a path-search algorithm
find its way through in real time.

## Run it

```bash
pip install -r requirements.txt
python path_finding.py
```

Opens fullscreen at 1920×1080.

## Controls

| Input | Action |
|-------|--------|
| Left-click / drag | Place walls |
| Right-click / drag | Erase walls |
| `S` | Set the start cell (at the mouse) |
| `G` | Set the goal cell (at the mouse) |
| `Esc` | Quit |

## Requirements

`pygame`, `numpy` (see `requirements.txt`).
