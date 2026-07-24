# Demo Projects

A collection of small, interactive simulations and visualizations. Most are
written in **Python** with [pygame](https://www.pygame.org/); one (Boids) is
written in **Java**.

**Quickest way to try one:** download its **Windows `.exe`** from the
[latest release](https://github.com/Luippe/Demo-Projects/releases/latest) and
double-click — no Python, no setup. Every demo closes with **`Esc`**.

---

## Ways to run a demo

### 1. Download the Windows `.exe` — easiest, no install

Grab a demo's self-contained **Windows `.exe`** from the repo's
[latest GitHub Release](https://github.com/Luippe/Demo-Projects/releases/latest) —
double-click and it runs, nothing else to install.

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
python main.py                       # use the script name from the demo's own README
```

> **Shortcut:** every Python demo *except Audio Processing* runs on the same four
> packages — `pip install pygame numpy scipy matplotlib`.

---

## The demos

Click any preview to open that demo's folder.

<table>
<tr>

<td width="50%" valign="top">

**[1. Boids](./BoidProject)** &nbsp;·&nbsp; Java

<a href="./BoidProject"><img src="BoidProject/boids.gif" width="100%" alt="Boids flocking simulation"></a>

Boids / flocking simulation.

</td>

<td width="50%" valign="top">

**[2. Audio Processing](./Audio%20Processing)**

<a href="./Audio%20Processing"><img src="Audio%20Processing/audio_process.gif" width="100%" alt="Audio processing with real-time FFT visuals"></a>

Live mic effects + real-time FFT visuals.

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[3. Pathfinding](./Pathfinding%20Visualization)**

<a href="./Pathfinding%20Visualization"><img src="Pathfinding%20Visualization/path_finding.gif" width="100%" alt="Grid path-search visualization"></a>

Grid path-search visualization.

</td>

<td width="50%" valign="top">

**[4. Conway](./Conway%20Game%20of%20Life)**

<a href="./Conway%20Game%20of%20Life"><img src="Conway%20Game%20of%20Life/conway.gif" width="100%" alt="Conway's Game of Life"></a>

Classic cellular-automaton life simulation.

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[5. Image Compression](./Image%20Compression)**

<a href="./Image%20Compression"><img src="Image%20Compression/compression.gif" width="100%" alt="FFT-based image compression"></a>

FFT-based image compression / low-pass filter.

</td>

<td width="50%" valign="top">

**[6. Fluid Flow](./Fluid%20Flow)**

<a href="./Fluid%20Flow"><img src="Fluid%20Flow/fluid_flow.gif" width="100%" alt="Real-time 2D fluid solver"></a>

Real-time 2D fluid solver.

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[7. Projectile Method](./Projectile%20Method)**

<a href="./Projectile%20Method"><img src="Projectile%20Method/projectile_methods.gif" width="100%" alt="Launch and aim a projectile with the mouse"></a>

Launch/aim a projectile with the mouse.

</td>

<td width="50%" valign="top">

**[8. Projectile Motion](./Projectile%20Motion)**

<a href="./Projectile%20Motion"><img src="Projectile%20Motion/projectile_motion.gif" width="100%" alt="Projectile trajectory with drag"></a>

Projectile trajectory with drag.

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[9. Double Pendulum](./Double%20Pendulum)**

<a href="./Double%20Pendulum"><img src="Double%20Pendulum/double_pendulum.gif" width="100%" alt="Chaotic double-pendulum motion"></a>

Chaotic double-pendulum motion.

</td>

<td width="50%" valign="top">

**[10. Single Pendulum](./Single%20Pendulum)**

<a href="./Single%20Pendulum"><img src="Single%20Pendulum/single_pendulum.gif" width="100%" alt="Damped single-pendulum motion"></a>

Damped single-pendulum motion over time.

</td>

</tr>
<tr>

<td width="50%" valign="top">

**[11. Spring Mass Damper](./Spring%20Mass%20Damper%20System)**

<a href="./Spring%20Mass%20Damper%20System"><img src="Spring%20Mass%20Damper%20System/smd.gif" width="100%" alt="Spring–mass–damper response"></a>

Spring–mass–damper response.

</td>

<td width="50%" valign="top">

**[12. Flow Plate](./Flow%20Plate)**

<a href="./Flow%20Plate"><img src="Flow%20Plate/0.png" width="100%" alt="Laminar pipe-flow velocity profile"></a>

Laminar pipe-flow velocity profile.

</td>

</tr>
</table>

Most demos open **fullscreen at 1920×1080** — press **`Esc`** to exit. Each demo's
own README lists its controls.

> The **`.exe`** downloads come from this repo's latest [GitHub Release](https://github.com/Luippe/Demo-Projects/releases/latest).

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
download links point at. See [`BUILD.md`](./BUILD.md) for the full build-and-release steps.
