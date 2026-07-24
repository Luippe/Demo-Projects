# Fluid Flow

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Fluid-Flow.exe"><img src="https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white" height="50" alt="Download for Windows (.exe)"></a>
</p>

<p align="center"><em>No Python needed — download and double-click. Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Fluid%20Flow">Grab the source folder</a>.</em></p>

## Controls

| Input | Action |
|-------|--------|
| Move / drag the mouse | Add fluid and velocity |
| `Esc` or close the window | Quit |

A real-time 2D fluid simulation. Move the mouse across the window to inject fluid
and velocity, and watch it diffuse and advect through the grid.

## Run it

```bash
pip install -r requirements.txt
python Fluid_Flow.py
```

Opens in a 300×300 window.

## Requirements

`pygame`, `numpy` (see `requirements.txt`).
