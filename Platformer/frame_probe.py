"""Frame-time probe. Inert unless env PLATFORMER_PROBE=1.

Usage:
    set PLATFORMER_PROBE=1
    python platformer.py
Walk right ~40 tiles, then ESC. Report prints to stdout.
"""

import gc
import os
import time
from collections import defaultdict

ENABLED = os.environ.get('PLATFORMER_PROBE') == '1'

_frames = []          # (ms, scroll)
_sections = defaultdict(float)
_section_max = defaultdict(float)
_gc_frames = defaultdict(list)   # generation -> [frame index]
_frame_start = 0.0
_mark_start = 0.0
_current = None


def _gc_callback(phase, info):
    if phase == 'stop':
        _gc_frames[info['generation']].append(len(_frames))


if ENABLED:
    gc.callbacks.append(_gc_callback)


def begin():
    global _frame_start, _mark_start, _current
    if not ENABLED:
        return
    _frame_start = _mark_start = time.perf_counter()
    _current = None


def mark(name):
    """Close previous section, open `name`."""
    global _mark_start, _current
    if not ENABLED:
        return
    now = time.perf_counter()
    if _current is not None:
        dt = (now - _mark_start) * 1000.0
        _sections[_current] += dt
        if dt > _section_max[_current]:
            _section_max[_current] = dt
    _mark_start = now
    _current = name


def end_frame(scroll):
    if not ENABLED:
        return
    mark(None)
    _frames.append(((time.perf_counter() - _frame_start) * 1000.0, scroll))


def report(tile_size=50):
    if not ENABLED or not _frames:
        return
    times = sorted(f[0] for f in _frames)
    n = len(times)
    median = times[n // 2]
    p99 = times[int(n * 0.99)]
    spike_cut = max(median * 1.5, median + 4.0)

    print('\n===== FRAME PROBE =====')
    print(f'frames={n}  median={median:.2f}ms  p95={times[int(n*0.95)]:.2f}ms  '
          f'p99={p99:.2f}ms  max={times[-1]:.2f}ms')
    print(f'budget@60fps=16.67ms   spike threshold={spike_cut:.2f}ms')

    print('\n-- sections (total ms / share / worst single frame) --')
    total = sum(_sections.values()) or 1.0
    for name, ms in sorted(_sections.items(), key=lambda kv: -kv[1]):
        print(f'  {name:<12} {ms/n:7.2f} ms/frame  {100*ms/total:5.1f}%  '
              f'worst {_section_max[name]:7.2f} ms')

    spikes = [(i, ms, sc) for i, (ms, sc) in enumerate(_frames) if ms > spike_cut]
    print(f'\n-- spikes: {len(spikes)} frames over {spike_cut:.2f}ms --')
    prev_i = prev_sc = None
    gaps_frames, gaps_tiles = [], []
    for i, ms, sc in spikes[:40]:
        if prev_i is None:
            print(f'  frame {i:>5}  {ms:7.2f}ms  scroll={sc}')
        else:
            df = i - prev_i
            dt_tiles = (sc - prev_sc) / tile_size
            gaps_frames.append(df)
            gaps_tiles.append(dt_tiles)
            print(f'  frame {i:>5}  {ms:7.2f}ms  scroll={sc}  '
                  f'+{df} frames  +{dt_tiles:.1f} tiles since last spike')
        prev_i, prev_sc = i, sc

    if gaps_frames:
        gf = sorted(gaps_frames)
        gt = sorted(gaps_tiles)
        print(f'\n  median spike gap: {gf[len(gf)//2]} frames '
              f'/ {gt[len(gt)//2]:.1f} tiles')

    print('\n-- gc collections (frame indices) --')
    for gen in sorted(_gc_frames):
        idx = _gc_frames[gen]
        print(f'  gen{gen}: {len(idx)} collections')
        if gen == 2 and idx:
            print(f'         frames: {idx[:25]}')
    spike_set = {i for i, _, _ in spikes}
    for gen in sorted(_gc_frames):
        hit = sum(1 for i in _gc_frames[gen] if i in spike_set)
        tot = len(_gc_frames[gen]) or 1
        print(f'  gen{gen}: {hit}/{len(_gc_frames[gen])} '
              f'({100*hit/tot:.0f}%) landed on a spike frame')

    print('\nVERDICT HINT:')
    print('  gen2 collections mostly landing on spikes -> GC pause. Fix: gc.freeze().')
    print('  spikes evenly spaced but no gc correlation -> audio/IO or vsync.')
    print('  no spikes but median > 16.67ms -> not stutter, just slow. Fix draw cost.')
    print('=======================\n')
