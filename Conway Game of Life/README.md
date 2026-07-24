# Conway's Game of Life

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Conway-Game-of-Life.exe"><img src="https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white" height="50" alt="Download for Windows (.exe)"></a>
</p>

<p align="center"><em>No Python needed — download and double-click. Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Conway%20Game%20of%20Life">Grab the source folder</a>.</em></p>

## Controls

| Input | Action |
|-------|--------|
| Left-click / drag | Draw live cells |
| Right-click / drag | Erase cells |
| `Space` | Start / advance the simulation |
| `Esc` | Quit |

An interactive version of Conway's classic cellular automaton. Draw a starting
pattern on the grid and watch it evolve under the Game of Life rules.

## Run it

```bash
pip install -r requirements.txt
python main.py
```

Opens fullscreen at 1920×1080.

## Requirements

`pygame`, `numpy` (see `requirements.txt`).
