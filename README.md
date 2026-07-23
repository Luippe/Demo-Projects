# Demo Projects

A collection of small, interactive simulations and visualizations. Most are
written in **Python** using [pygame](https://www.pygame.org/); one (Boids) is
written in **Java**. Each lives in its own folder and runs on its own — pick one,
install its requirements, and go.

Every pygame demo closes when you press **`Esc`**.

---

## Prerequisites

- **Python 3.9+** and `pip` — [python.org/downloads](https://www.python.org/downloads/)
  (on Windows, tick *"Add Python to PATH"* during install).
- **Java 17+** (only for the Boids demo) — needed to compile/run that one.

---

## Quick start — grab one demo and run it

**1. Get the files.** Either:

- **Whole collection:** click the green **`Code`** button at the top of the repo →
  **Download ZIP**, then unzip it; or
  ```bash
  git clone <this-repo-url>
  ```
- **Just one demo:** paste the folder's GitHub URL into
  [download-directory.github.io](https://download-directory.github.io/) to get a
  ZIP of only that folder.

**2. Open a terminal in the demo's folder.** Folder names contain spaces, so keep
the quotes:

```bash
cd "Conway Game of Life"
```

**3. (Recommended) create a virtual environment** so these packages don't touch
your system Python:

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
```

**4. Install requirements and run.** Each Python folder has a `requirements.txt`:

```bash
pip install -r requirements.txt
python main.py          # use the script name listed in the table below
```

> **Shortcut:** every Python demo *except Audio Processing* runs on the same four
> packages. Install them once (into a shared venv) and you can run all ten:
> ```bash
> pip install pygame numpy scipy matplotlib
> ```

---

## The demos

| Demo | What it shows | Run from its folder | Controls |
|------|---------------|---------------------|----------|
| [Conway Game of Life](./Conway%20Game%20of%20Life) | Classic cellular-automaton life simulation | `python main.py` | Left-click draw, right-click erase, `Space` step/run, `Esc` quit |
| [Double Pendulum](./Double%20Pendulum) | Chaotic double-pendulum motion | `python double_pendulum.py` | `Space` start, `Esc` quit |
| [Single Pendulum](./Single%20Pendulum) | Damped single-pendulum motion over time | `python demo_pendulum.py` | Drag the slider to scrub time, `Esc` quit |
| [Projectile Motion](./Projectile%20Motion) | Projectile trajectory with drag | `python demo_projectile.py` | Drag the slider to change time, `Esc` quit |
| [Projectile Method](./Projectile%20Method) | Launch/aim a projectile with the mouse | `python projectile_method.py` | Click-drag to launch, `Esc` quit |
| [Spring Mass Damper System](./Spring%20Mass%20Damper%20System) | Spring–mass–damper response | `python smd.py` | `Space` start, `Esc` quit |
| [Pathfinding Visualization](./Pathfinding%20Visualization) | Grid path-search visualization | `python path_finding.py` | Left-click walls, right-click erase, `S` start, `G` goal, `Esc` quit |
| [Fluid Flow](./Fluid%20Flow) | Real-time 2D fluid solver | `python "Fluid Flow.py"` | Move the mouse to add fluid, `Esc` quit |
| [Flow Plate](./Flow%20Plate) | Laminar pipe-flow velocity profile | `python "Flow Plate.py"` | Visual only, `Esc` quit |
| [Image Compression](./Image%20Compression) | FFT-based image compression / low-pass filter | `python Image_compress_filter.py` | Drag the slider to change compression, `Esc` quit |
| [Audio Processing](./Audio%20Processing) | Live mic effects + real-time FFT visuals | `python PythonAudioProcessingProject.py` | Click effect toggles, arrow keys/WASD, `Esc` quit |
| [BoidProject](./BoidProject) | Boids / flocking simulation (**Java**) | see its README | Close the window to exit |

Most pygame demos open **fullscreen at 1920×1080** — press **`Esc`** to get back out.

---

## Notes before you try each one

- **Audio Processing** is the heavy one: it needs a **working microphone and
  speakers** plus `pyaudio` and `opencv-python`, which are harder to install than
  the rest (`pyaudio` needs system PortAudio libraries). See its README.
- **Flow Plate** and **Image Compression** read data/image files from their own
  folder — run them *from inside that folder* so the relative paths resolve.
- **BoidProject** is Java, not Python — it has no `requirements.txt`; see its
  README for the compile-and-run steps.

Each folder has its own `README.md` with details specific to that demo.
