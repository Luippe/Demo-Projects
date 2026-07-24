#!/usr/bin/env python3
"""
Build standalone Windows .exe files for the pygame demos with PyInstaller.

Usage:
    python build_installers.py                     # build every demo
    python build_installers.py "Fluid Flow"        # build only the named demo(s)

Each demo becomes a single self-contained .exe in ./dist/ that a user can
double-click with no Python install. Build artifacts land in ./build/ (both
folders are git-ignored). Upload the .exe files from ./dist/ to a GitHub Release.

Excluded on purpose:
  - Audio Processing  (needs a live microphone + fussy pyaudio/opencv bundling)
  - BoidProject       (Java, not Python -- use jpackage for that one)
"""
import os
import sys
import subprocess

REPO = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(REPO, "dist")
BUILD = os.path.join(REPO, "build")

# (folder, entry script, output .exe name, [data files to bundle alongside])
DEMOS = [
    ("Conway Game of Life",       "main.py",                  "Conway-Game-of-Life",       []),
    ("Double Pendulum",           "double_pendulum.py",       "Double-Pendulum",           []),
    ("Single Pendulum",           "demo_pendulum.py",         "Single-Pendulum",           []),
    ("Projectile Motion",         "demo_projectile.py",       "Projectile-Motion",         []),
    ("Projectile Method",         "projectile_method.py",     "Projectile-Method",         []),
    ("Spring Mass Damper System", "smd.py",                   "Spring-Mass-Damper",        ["spring.png", "damp1.png", "damp2.png"]),
    ("Pathfinding Visualization", "path_finding.py",          "Pathfinding-Visualization", ["editundo.ttf"]),
    ("Fluid Flow",                "Fluid_Flow.py",            "Fluid-Flow",                []),
    ("Flow Plate",                "Flow_Plate.py",            "Flow-Plate",                ["Material Properties.txt", "Water Properties.txt"]),
    ("Image Compression",         "Image_compress_filter.py", "Image-Compression",         ["pupp_gray.jpg"]),
]


def build(folder, entry, name, data):
    demo_dir = os.path.join(REPO, folder)
    entry_path = os.path.join(demo_dir, entry)
    if not os.path.isfile(entry_path):
        return False, "entry script not found: " + entry_path

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--windowed", "--noconfirm", "--clean",
        "--name", name,
        "--distpath", DIST,
        "--workpath", os.path.join(BUILD, name),
        "--specpath", BUILD,
    ]
    for d in data:
        src = os.path.join(demo_dir, d)
        if not os.path.isfile(src):
            return False, "data file not found: " + src
        cmd += ["--add-data", src + os.pathsep + "."]
    cmd.append(entry_path)

    print("\n=== Building %s ===" % name, flush=True)
    proc = subprocess.run(cmd, cwd=demo_dir)
    exe = os.path.join(DIST, name + (".exe" if os.name == "nt" else ""))
    if proc.returncode == 0 and os.path.isfile(exe):
        return True, "%s (%d MB)" % (exe, os.path.getsize(exe) // (1024 * 1024))
    return False, "PyInstaller failed (exit %s)" % proc.returncode


def main():
    wanted = sys.argv[1:]
    todo = [d for d in DEMOS if not wanted or d[0] in wanted]
    if not todo:
        print("No matching demos. Names are:")
        for d in DEMOS:
            print("  " + d[0])
        sys.exit(2)

    os.makedirs(DIST, exist_ok=True)
    results = []
    for folder, entry, name, data in todo:
        ok, msg = build(folder, entry, name, data)
        results.append((name, ok, msg))

    print("\n" + "=" * 55)
    print("BUILD SUMMARY")
    for name, ok, msg in results:
        print("  [%s] %s: %s" % ("OK  " if ok else "FAIL", name, msg))
    print("=" * 55)
    sys.exit(1 if any(not ok for _, ok, _ in results) else 0)


if __name__ == "__main__":
    main()
