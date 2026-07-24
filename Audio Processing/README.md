# Audio Processing

<p align="center">
  <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Audio%20Processing"><img src="https://img.shields.io/badge/Download%20source-.zip-6e7681?style=for-the-badge&logo=github&logoColor=white" height="50" alt="Download source (.zip)"></a>
</p>

<p align="center"><em>Runs from source — there's no prebuilt <code>.exe</code> for this one (it needs a live microphone and heavy libraries). See setup below.</em></p>

## Controls

| Input | Action |
|-------|--------|
| Click the on-screen checkboxes | Toggle effects (echo / pitch / auto-tune) |
| Arrow keys, `W` / `A` / `S` / `D` | Move / rotate the 3D visualization |
| `H` | Toggle help / view |
| `Esc` | Quit |

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

## Files & assets

- `PythonAudioProcessingProject.py` — **the demo** (run this one).
- `checkmark0.png`, `checkmark1.png`, `editundo.ttf` — UI assets, loaded from this folder.
- `wav_test2.wav`, `wobble.wav` — sample audio used by the effects.
- `temp_audio.wav` is **written at runtime** and is git-ignored.

## Requirements

`pygame`, `numpy`, `scipy`, `matplotlib`, `pyaudio`, `opencv-python`
(see `requirements.txt`).
