# Image Compression

[![Download for Windows](https://img.shields.io/badge/Download%20for%20Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/Luippe/Demo-Projects/releases/latest/download/Image-Compression.exe)

*No Python needed — download and double-click. Prefer the code? [Grab the source folder](https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Image%20Compression).*

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

## Controls

| Input | Action |
|-------|--------|
| Drag the slider inside the rectangle | Change the compression / filter scale |
| `Esc` | Quit |

> Note: changing the compression scale removes any active low-pass filter.

## Requirements

`pygame`, `numpy`, `scipy`, `matplotlib` (see `requirements.txt`). `matplotlib`
is used here only to read the JPEG.
