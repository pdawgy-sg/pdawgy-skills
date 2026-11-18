import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from music import house_bed


def add_music(src, out, bpm=118, bed_level=0.32):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                src], capture_output=True, text=True, check=True).stdout)
    bed = os.path.splitext(out)[0] + "_bed.wav"
    house_bed(bed, dur, bpm)
    graph = (f"[1:a]volume={bed_level}[mus];[0:a]asplit[vo][key];"
             f"[mus][key]sidechaincompress=threshold=0.015:ratio=10:attack=15:release=420:makeup=1[duck];"
             f"[vo][duck]amix=inputs=2:normalize=0:duration=first,"
             f"loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[aout]")
    subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-i", bed,
                    "-filter_complex", graph, "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    os.remove(bed)
    return out


if __name__ == "__main__":
    print(add_music(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 118))
