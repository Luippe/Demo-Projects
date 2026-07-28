# Spring–Mass–Damper System

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Spring-Mass-Damper.exe"><img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS-.EXE-0078D4?style=for-the-badge&logo=windows&logoColor=white" height="68" alt="Download Spring-Mass-Damper for Windows (.exe)"></a>
</p>

<p align="center">
<em>Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Spring%20Mass%20Damper%20System">Download the source folder</a>.</em></p>

Animates the response of a classic spring–mass–damper system — a cart on a spring
with a damper — showing how it oscillates and settles over time.

## Controls

| Input | Action |
|-------|--------|
| `Space` | Start the simulation |
| `Esc` | Quit |

## Run from source

Run it **from inside this folder** — it loads `spring.png`, `damp1.png`, and
`damp2.png` by relative path.

```bash
pip install -r requirements.txt
python smd.py
```

Opens fullscreen at 1920×1080.
