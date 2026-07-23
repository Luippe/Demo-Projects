# Audio Processing

Real-time audio effects driven by your microphone — echo, pitch shift, and
auto-tune — with live FFT frequency visuals rendered in pygame. Toggle effects
with on-screen checkboxes and steer the 3D visualization with the keyboard.

## Heads up — this is the most involved demo to set up

It needs:

- A **working microphone and speakers/headphones** (it opens a live input and
  output audio stream on your default devices).
- Two packages that are harder to install than the rest:
  - **`pyaudio`** — depends on the system **PortAudio** library.
    - Windows: `pip install pyaudio` usually works on recent Python; otherwise
      install a prebuilt wheel via `pipwin install pyaudio`.
    - macOS: `brew install portaudio` first, then `pip install pyaudio`.
    - Debian/Ubuntu: `sudo apt install portaudio19-dev`, then `pip install pyaudio`.
  - **`opencv-python`** (imported as `cv2`).

## Run it

```bash
pip install -r requirements.txt
python PythonAudioProcessingProject.py
```

Opens a resizable 1920×1080 window.

## Controls

| Input | Action |
|-------|--------|
| Click the on-screen checkboxes | Toggle effects (echo / pitch / auto-tune) |
| Arrow keys, `W` / `A` / `S` / `D` | Move / rotate the 3D visualization |
| `H` | Toggle help / view |
| `Esc` | Quit |

## Files & assets

- `PythonAudioProcessingProject.py` — **the demo** (run this one).
- `checkmark0.png`, `checkmark1.png`, `editundo.ttf` — UI assets, loaded from this folder.
- `wav_test2.wav`, `wobble.wav` — sample audio used by the effects.
- `temp_audio.wav` is **written at runtime** and is git-ignored.

## Known compatibility note

The code calls `matplotlib.cm.get_cmap('turbo')`, which was **removed in
matplotlib 3.9**. On a current matplotlib this line raises an
`AttributeError`. Until the source is updated (to `matplotlib.colormaps['turbo']`),
pin an older matplotlib in this venv:

```bash
pip install "matplotlib<3.9"
```

## Requirements

`pygame`, `numpy`, `scipy`, `matplotlib`, `pyaudio`, `opencv-python`
(see `requirements.txt`).
