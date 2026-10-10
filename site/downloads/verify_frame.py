#!/usr/bin/env python3
"""Frame check: extract frame at time T from a video via ffmpeg, report mean RGB and whether a region is non-background."""
import subprocess, sys
def frame_rgb(video, t, w=64, h=36):
    raw = subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",video,"-frames:v","1",
        "-vf",f"scale={w}:{h}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True,check=True).stdout
    assert len(raw)==w*h*3, f"bad frame size {len(raw)}"
    px=[raw[i:i+3] for i in range(0,len(raw),3)]
    return [sum(p[c] for p in px)/len(px) for c in range(3)]
if __name__=="__main__":
    v=sys.argv[1]
    for t in (0.2,1.8):
        print(t,[round(x) for x in frame_rgb(v,t)])
