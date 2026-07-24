# Image Compression

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Image-Compression.exe"><img src="https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white" height="50" alt="Download for Windows (.exe)"></a>
</p>

<p align="center"><em>No Python needed — download and double-click. Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Image%20Compression">Grab the source folder</a>.</em></p>

## Controls

| Input | Action |
|-------|--------|
| Drag the slider inside the rectangle | Change the compression / filter scale |
| `Esc` | Quit |

> Note: changing the compression scale removes any active low-pass filter.

Demonstrates image compression in the frequency domain. The image is transformed
with a 2D FFT; drag the slider to discard high-frequency components (a low-pass
filter) and watch image quality trade off against compression.

## Run it

Run it **from inside this folder** — it reads `pupp_gray.jpg` by relative path:

```bash
pip install -r requirements.txt
python Image_compress_filter.py
```

Opens in an 800×800 window.

## Requirements

`pygame`, `numpy`, `scipy`, `matplotlib` (see `requirements.txt`). `matplotlib`
is used here only to read the JPEG.
