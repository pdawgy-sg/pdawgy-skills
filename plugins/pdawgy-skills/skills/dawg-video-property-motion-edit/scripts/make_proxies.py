import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import project as P

PAD = 0.15
GRADE_SDR = "eq=contrast=1.06:saturation=1.08:gamma=1.02,colortemperature=temperature=6200:mix=0.25"
TONEMAP = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=contrast=1.04:saturation=0.97")


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:stream=codec_type,color_transfer", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in d["streams"])
    hdr = v.get("color_transfer") in ("arib-std-b67", "smpte2084")
    return float(d["format"]["duration"]), has_audio, hdr


def speech_bounds(path, dur):
    err = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", path, "-af",
                          "silencedetect=n=-32dB:d=0.25", "-vn", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    ends += [dur] * (len(starts) - len(ends))
    spans = list(zip(starts, ends))
    if spans and spans[0][0] <= 0.05 and spans[0][1] >= dur - 0.05:
        return None
    first = spans[0][1] if spans and spans[0][0] <= 0.05 else 0.0
    last = spans[-1][0] if spans and spans[-1][1] >= dur - 0.05 else dur
    return max(0.0, first - PAD), min(dur, last + PAD)


def stream_len(path, kind):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", kind, "-show_entries",
                          "stream=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    try:
        return float(out.strip().splitlines()[0].split(",")[0])
    except (ValueError, IndexError):
        return 0.0


def make(src):
    os.makedirs(P.PROXY, exist_ok=True)
    stem = os.path.splitext(os.path.basename(src))[0]
    stem = stem[3:] if stem.startswith("VID") else stem
    out = os.path.join(P.PROXY, f"{stem}.mp4")
    dur, has_audio, hdr = probe(src)
    bounds = speech_bounds(src, dur) if has_audio else None
    ss, to = bounds if bounds else (0.0, dur)
    vf = (TONEMAP + ",scale=1080:1920:flags=lanczos" if hdr else
          "scale=1080:1920:flags=lanczos," + GRADE_SDR) + ",fps=30,setsar=1,format=yuv420p"
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{ss:.3f}", "-to",
           f"{to:.3f}", "-i", src]
    if has_audio:
        af = ["-af", "highpass=f=90,loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000"]
        maps = []
    else:
        cmd += ["-f", "lavfi", "-t", f"{to - ss:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        af, maps = [], ["-map", "0:v", "-map", "1:a", "-shortest"]
    cmd += maps + ["-vf", vf] + af + ["-c:v", "libx264", "-crf", "14", "-preset", "fast",
                                      "-c:a", "aac", "-b:a", "192k", out]
    subprocess.run(cmd, check=True)
    common = round(min(stream_len(out, "v"), stream_len(out, "a")), 3)
    kind = "speech" if bounds else "b-roll/silent"
    print(f'    "{stem}": {common},     # {kind}{", HDR tone-mapped" if hdr else ""}, src {ss:.2f}-{to:.2f}s')
    return stem, common


if __name__ == "__main__":
    clips = sys.argv[1:] or sorted(f for f in glob.glob(os.path.join(P.RAW, "*"))
                                   if f.lower().endswith((".mp4", ".mov", ".m4v")))
    print("TAKES = {")
    for c in clips:
        make(c)
    print("}")
