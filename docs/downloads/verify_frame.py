#!/usr/bin/env python3
"""Frame check: extract a frame at time T from a video via ffmpeg.
frame_rgb    -> mean RGB of the whole frame (good for flat colour clips; BLIND to small text on a dark background)
nonbg_ratio  -> share of pixels in a crop region that differ from the background colour (use this for text checks)
"""
import subprocess, sys

def _raw(video, t, vf, w, h):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1",
                          "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    assert len(raw) == w * h * 3, f"bad frame size {len(raw)}"
    return [raw[i:i + 3] for i in range(0, len(raw), 3)]

def frame_rgb(video, t, w=64, h=36):
    px = _raw(video, t, f"scale={w}:{h}", w, h)
    return [sum(p[c] for p in px) / len(px) for c in range(3)]

def nonbg_ratio(video, t, x, y, w, h, bg=(11, 16, 32), thresh=90):
    """crop=w:h at (x,y) in source pixels; bg is the background RGB you chose in the composition."""
    px = _raw(video, t, f"crop={w}:{h}:{x}:{y}", w, h)
    return sum(1 for p in px if sum(abs(p[c] - bg[c]) for c in range(3)) > thresh) / len(px)

if __name__ == "__main__":
    v = sys.argv[1]
    for t in (0.2, 1.8):
        print("mean RGB", t, [round(x) for x in frame_rgb(v, t)])
    if len(sys.argv) == 6:  # optional: x y w h
        x, y, w, h = map(int, sys.argv[2:6])
        for t in (0.0, 1.5):
            print("non-bg ratio", t, round(nonbg_ratio(v, t, x, y, w, h), 3))
