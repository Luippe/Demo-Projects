# Image Compression

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Image-Compression.exe"><img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS-.EXE-0078D4?style=for-the-badge&logo=windows&logoColor=white" height="68" alt="Download Image Compression for Windows (.exe)"></a>
</p>

<p align="center">
<em>Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/Image%20Compression">Download the source folder</a>.</em></p>

Demonstrates image compression in the frequency domain. The image is transformed
with a 2D FFT; drag the slider to throw away high-frequency components (a low-pass
filter) and watch image quality trade off against compression.

## Controls

| Input | Action |
|-------|--------|
| Drag the slider inside the rectangle | Change the compression / filter scale |
| `Esc` | Quit |

Changing the compression scale clears any active low-pass filter.

## Run from source

Run it **from inside this folder** — it reads `pupp_gray.jpg` by relative path.

```bash
pip install -r requirements.txt
python Image_compress_filter.py
```

Opens in an 800×800 window.
