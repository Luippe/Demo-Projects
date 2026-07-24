# Demo Projects

A collection of small, interactive simulations and visualizations. Most are
written in **Python** with [pygame](https://www.pygame.org/); one (Boids) is
written in **Java**.

**Quickest way to try one:** download its **Windows `.exe`** from the table below
and double-click — no Python, no setup. Every demo closes with **`Esc`**.

---

## Ways to run a demo

### 1. Download the Windows `.exe` — easiest, no install

Click a demo's **⬇ Download for Windows** button in the table below. It's a single
self-contained `.exe` — double-click and it runs, nothing else to install.

> **First-launch warning is normal.** Because these `.exe`s aren't code-signed,
> Windows SmartScreen may show a blue *"Windows protected your PC"* box the first
> time. Click **More info → Run anyway**. (Expected for any small indie tool — and
> the full source is right here if you'd rather build it yourself.)

Two demos have no `.exe`: **Audio Processing** (needs a live microphone and heavy
libraries) and **Boids** (it's Java). Run those from source.

### 2. Run from source — any OS

Needs **Python 3.9+**. Grab a demo's source folder (the *source* link at the top of
its own README, or the whole-repo ZIP via the green **Code** button), then:

```bash
cd "Conway Game of Life"
python -m venv .venv                 # optional but recommended
.venv\Scripts\Activate.ps1           # Windows PowerShell  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python main.py                       # use the script name from the table
```

> **Shortcut:** every Python demo *except Audio Processing* runs on the same four
> packages — `pip install pygame numpy scipy matplotlib`.

---

## The demos

| Demo | What it shows | Windows | Run from source |
|------|---------------|---------|-----------------|
| [Conway Game of Life](./Conway%20Game%20of%20Life) | Classic cellular-automaton life simulation | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Conway-Game-of-Life.exe) | `python main.py` |
| [Double Pendulum](./Double%20Pendulum) | Chaotic double-pendulum motion | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Double-Pendulum.exe) | `python double_pendulum.py` |
| [Single Pendulum](./Single%20Pendulum) | Damped single-pendulum motion over time | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Single-Pendulum.exe) | `python demo_pendulum.py` |
| [Projectile Motion](./Projectile%20Motion) | Projectile trajectory with drag | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Projectile-Motion.exe) | `python demo_projectile.py` |
| [Projectile Method](./Projectile%20Method) | Launch/aim a projectile with the mouse | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Projectile-Method.exe) | `python projectile_method.py` |
| [Spring Mass Damper System](./Spring%20Mass%20Damper%20System) | Spring–mass–damper response | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Spring-Mass-Damper.exe) | `python smd.py` |
| [Pathfinding Visualization](./Pathfinding%20Visualization) | Grid path-search visualization | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Pathfinding-Visualization.exe) | `python path_finding.py` |
| [Fluid Flow](./Fluid%20Flow) | Real-time 2D fluid solver | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Fluid-Flow.exe) | `python Fluid_Flow.py` |
| [Flow Plate](./Flow%20Plate) | Laminar pipe-flow velocity profile | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Flow-Plate.exe) | `python Flow_Plate.py` |
| [Image Compression](./Image%20Compression) | FFT-based image compression / low-pass filter | [![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Image-Compression.exe) | `python Image_compress_filter.py` |
| [Audio Processing](./Audio%20Processing) | Live mic effects + real-time FFT visuals | [![source](https://img.shields.io/badge/source-.zip-6e7681?style=flat-square&logo=github&logoColor=white)](https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Audio%20Processing) | `python PythonAudioProcessingProject.py` |
| [BoidProject](./BoidProject) | Boids / flocking simulation (**Java**) | [![source](https://img.shields.io/badge/source-.zip-6e7681?style=flat-square&logo=github&logoColor=white)](https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/BoidProject) | see its README |

Most demos open **fullscreen at 1920×1080** — press **`Esc`** to exit. Each demo's
own README lists its controls.

> The **`.exe`** links pull from this repo's latest [GitHub Release](https://github.com/Luippe/Demo-Projects/releases/latest).
> The **source** links use [download-directory.github.io](https://download-directory.github.io/),
> a free service that zips a single GitHub folder.

---

## Notes before you try each one

- **Audio Processing** (source only) needs a **working microphone and speakers**
  plus `pyaudio` and `opencv-python`, which are harder to install than the rest.
  See its README.
- **BoidProject** is **Java** — needs a JDK to compile/run; see its README.
- **Flow Plate** and **Image Compression** read data/image files from their own
  folder; the `.exe` builds bundle those automatically, and running from source
  works as long as you launch from inside the folder.

---

## Building the `.exe` files yourself

The Windows executables are produced from the Python sources with
[PyInstaller](https://pyinstaller.org/) via [`build_installers.py`](./build_installers.py):

```bash
pip install pyinstaller
python build_installers.py            # builds every demo into ./dist/
```

The resulting `.exe` files (in `./dist/`) are published as assets on a
[GitHub Release](https://github.com/Luippe/Demo-Projects/releases) — that's what the
download buttons point at. See [`BUILD.md`](./BUILD.md) for the full build-and-release steps.
