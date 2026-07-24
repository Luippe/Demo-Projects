# Building & releasing the Windows `.exe` files

The download buttons in the READMEs point at `.exe` files hosted on this repo's
**latest GitHub Release**. This file explains how to (re)build those executables
and publish them so the buttons work.

## What gets built

[`build_installers.py`](./build_installers.py) uses **PyInstaller** to package 10
of the pygame demos into standalone, single-file `.exe`s. The Java demo has its
own build script. One demo is excluded:

- **Audio Processing** — needs a live microphone and fussy `pyaudio`/`opencv`
  bundling; shipped as source.

**BoidProject** uses Java's `jpackage`. Build its portable Windows application
with:

```powershell
cd BoidProject
powershell -NoProfile -ExecutionPolicy Bypass -File .\Build-Boids.ps1
```

After installing WiX, create `dist\Boids.exe` with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Build-Boids.ps1 -Type Installer
```

Each `.exe` is named to match its download button, e.g. `Conway-Game-of-Life.exe`.

## 1. Build

```bash
pip install pyinstaller
python build_installers.py            # build all 10 into ./dist/
```

Or build just some:

```bash
python build_installers.py "Fluid Flow" "Conway Game of Life"
```

Notes:
- Output `.exe`s land in `./dist/`; scratch files in `./build/`. Both are
  git-ignored — **do not commit them** (they're large; they belong in a Release).
- Sizes: numpy-only demos are ~28 MB; the ones that use SciPy are ~75 MB; Image
  Compression (matplotlib) is the largest.
- Builds are **Windows-only** — an `.exe` built here runs on Windows. For macOS or
  Linux binaries you'd run this same script on those systems.

## 2. Publish a GitHub Release

The buttons use the stable URL
`https://github.com/Luippe/Demo-Projects/releases/latest/download/<Name>.exe`,
which always resolves to the newest **published** release. So the asset names must
match (the build script already names them correctly), and the release must be
published (not a draft/pre-release).

### Option A — GitHub CLI (fastest)

```bash
gh release create v1.0 dist/*.exe --title "Demo Projects v1.0" --notes "Standalone Windows builds of the demos."
```

### Option B — GitHub website

1. Go to the repo → **Releases** → **Draft a new release**.
2. Choose a tag (e.g. `v1.0`) and a title.
3. Drag every `.exe` from `dist/` into the **Attach binaries** box.
4. Click **Publish release**.

That's it — the download buttons go live immediately.

## Updating later

Rebuild, then create a **new** release with a new tag (e.g. `v1.1`) and the fresh
`.exe`s. Because the buttons target `releases/latest/`, they switch to the new
build automatically — no README edits needed.

## Good to know

- The `.exe`s are **unsigned**, so Windows SmartScreen shows a *"Windows protected
  your PC"* prompt on first run → **More info → Run anyway**. Code-signing removes
  this but requires a paid certificate.
- If a built `.exe` fails to launch, rebuild that one with a console window to see
  the error: temporarily change `--windowed` to `--console` in `build_installers.py`.
