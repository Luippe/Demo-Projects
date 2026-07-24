# Conway's Game of Life

[![Download for Windows](https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Conway-Game-of-Life.exe)

*No Python needed — download and double-click. Prefer the code? [Grab the source folder](https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Conway%20Game%20of%20Life).*

An interactive version of Conway's classic cellular automaton. Draw a starting
pattern on the grid and watch it evolve under the Game of Life rules.

## Run it

```bash
pip install -r requirements.txt
python main.py
```

Opens fullscreen at 1920×1080.

## Controls

| Input | Action |
|-------|--------|
| Left-click / drag | Draw live cells |
| Right-click / drag | Erase cells |
| `Space` | Start / advance the simulation |
| `Esc` | Quit |

## Requirements

`pygame`, `numpy` (see `requirements.txt`).
