# Solar System Simulation

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Solar-System-Simulation.exe"><img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS-.EXE-0078D4?style=for-the-badge&logo=windows&logoColor=white" height="68" alt="Download Solar System Simulation for Windows (.exe)"></a>
</p>

<p align="center">
<em>Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Solar%20System%20Simulation">Download the source folder</a>.</em></p>

Simulates the Sun and nine planets (including Pluto) with **precomputed**
gravitational trajectories. Rotate and zoom the 3D view, change the reference
frame, scrub through time, and click a planet to inspect its orbital properties.
Originally built as the final project for my Spacecraft Dynamics & Controls class.

## Controls

| Input | Action |
|-------|--------|
| Mouse wheel | Zoom in or out |
| Left-click and drag | Rotate the view |
| Click a planet | Show its orbital details |
| Click the top-right button | Open planet visibility and display options |
| `0`–`9` | Center the reference frame on the Sun through Pluto |
| `Q` / `W` | Rotate around the x-axis |
| `A` / `S` | Rotate around the y-axis |
| `Z` / `X` | Rotate around the z-axis |
| Up / Down arrow | Increase / decrease simulation speed |
| `Space` | Pause or resume |
| `T` | Toggle planet names |
| `O` | Toggle orbital trails |
| `R` | Toggle scaled planet radii |
| `Esc` | Quit |

## Run from source

Run it **from inside this folder** so the bundled images, font, and trajectory
data can be found.

```bash
pip install -r requirements.txt
python orbit.py
```

Opens fullscreen at 1920×1080.
