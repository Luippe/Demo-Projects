# Demo Projects

A collection of small, interactive simulations and visualizations. Most are
written in **Python** with [pygame](https://www.pygame.org/); one (Boids) is
written in **Java**.

**Quickest way to try one:** download its **Windows `.exe`** from the gallery below
and double-click — no Python, no setup. Every demo closes with **`Esc`**.

---

## Ways to run a demo

### 1. Download the Windows `.exe` — easiest, no install

Click a demo's **Windows `.exe`** badge in the gallery below. It's a single
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
python main.py                       # use the script name from the gallery
```

> **Shortcut:** every Python demo *except Audio Processing* runs on the same four
> packages — `pip install pygame numpy scipy matplotlib`.

---

## The demos

Click any preview to open that demo's folder. Each card links its **Windows `.exe`**
(or **source `.zip`**) and shows the command to run it from source.

<table>
<tr>

<td width="50%" valign="top">

**[1. Boids](./BoidProject)** &nbsp;·&nbsp; Java

<a href="./BoidProject"><img src="BoidProject/boids.gif" width="100%" alt="Boids flocking simulation"></a>

Boids / flocking simulation.

[![source](https://img.shields.io/badge/source-.zip-6e7681?style=flat-square&logo=github&logoColor=white)](https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/BoidProject) &nbsp; *see its README*

</td>

<td width="50%" valign="top">

**[2. Audio Processing](./Audio%20Processing)**

<a href="./Audio%20Processing"><img src="Audio%20Processing/audio_process.gif" width="100%" alt="Audio processing with real-time FFT visuals"></a>

Live mic effects + real-time FFT visuals.

[![source](https://img.shields.io/badge/source-.zip-6e7681?style=flat-square&logo=github&logoColor=white)](https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Audio%20Processing) &nbsp; `python PythonAudioProcessingProject.py`

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[3. Pathfinding](./Pathfinding%20Visualization)**

<a href="./Pathfinding%20Visualization"><img src="Pathfinding%20Visualization/path_finding.gif" width="100%" alt="Grid path-search visualization"></a>

Grid path-search visualization.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Pathfinding-Visualization.exe) &nbsp; `python path_finding.py`

</td>

<td width="50%" valign="top">

**[4. Conway](./Conway%20Game%20of%20Life)**

<a href="./Conway%20Game%20of%20Life"><img src="Conway%20Game%20of%20Life/conway.gif" width="100%" alt="Conway's Game of Life"></a>

Classic cellular-automaton life simulation.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Conway-Game-of-Life.exe) &nbsp; `python main.py`

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[5. Image Compression](./Image%20Compression)**

<a href="./Image%20Compression"><img src="Image%20Compression/compression.gif" width="100%" alt="FFT-based image compression"></a>

FFT-based image compression / low-pass filter.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Image-Compression.exe) &nbsp; `python Image_compress_filter.py`

</td>

<td width="50%" valign="top">

**[6. Fluid Flow](./Fluid%20Flow)**

<a href="./Fluid%20Flow"><img src="Fluid%20Flow/fluid_flow.gif" width="100%" alt="Real-time 2D fluid solver"></a>

Real-time 2D fluid solver.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Fluid-Flow.exe) &nbsp; `python Fluid_Flow.py`

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[7. Projectile Method](./Projectile%20Method)**

<a href="./Projectile%20Method"><img src="Projectile%20Method/projectile_methods.gif" width="100%" alt="Launch and aim a projectile with the mouse"></a>

Launch/aim a projectile with the mouse.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Projectile-Method.exe) &nbsp; `python projectile_method.py`

</td>

<td width="50%" valign="top">

**[8. Projectile Motion](./Projectile%20Motion)**

<a href="./Projectile%20Motion"><img src="Projectile%20Motion/projectile_motion.gif" width="100%" alt="Projectile trajectory with drag"></a>

Projectile trajectory with drag.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Projectile-Motion.exe) &nbsp; `python demo_projectile.py`

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[9. Double Pendulum](./Double%20Pendulum)**

<a href="./Double%20Pendulum"><img src="Double%20Pendulum/double_pendulum.gif" width="100%" alt="Chaotic double-pendulum motion"></a>

Chaotic double-pendulum motion.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Double-Pendulum.exe) &nbsp; `python double_pendulum.py`

</td>

<td width="50%" valign="top">

**[10. Single Pendulum](./Single%20Pendulum)**

<a href="./Single%20Pendulum"><img src="Single%20Pendulum/single_pendulum.gif" width="100%" alt="Damped single-pendulum motion"></a>

Damped single-pendulum motion over time.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Single-Pendulum.exe) &nbsp; `python demo_pendulum.py`

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[11. Spring Mass Damper](./Spring%20Mass%20Damper%20System)**

<a href="./Spring%20Mass%20Damper%20System"><img src="Spring%20Mass%20Damper%20System/smd.gif" width="100%" alt="Spring–mass–damper response"></a>

Spring–mass–damper response.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Spring-Mass-Damper.exe) &nbsp; `python smd.py`

</td>

<td width="50%" valign="top">

**[12. Flow Plate](./Flow%20Plate)**

<a href="./Flow%20Plate"><img src="Flow%20Plate/0.png" width="100%" alt="Laminar pipe-flow velocity profile"></a>

Laminar pipe-flow velocity profile.

[![.exe](https://img.shields.io/badge/Windows-.exe-2ea44f?style=flat-square&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Flow-Plate.exe) &nbsp; `python Flow_Plate.py`

</td>

</tr>
</table>

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
