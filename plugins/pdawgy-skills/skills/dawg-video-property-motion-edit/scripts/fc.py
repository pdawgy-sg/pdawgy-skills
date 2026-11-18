import json
import os
import subprocess

TICK = 254016000000


def ticks(seconds):
    return int(round(seconds * TICK))


def png_size(path):
    out = subprocess.run(["magick", "identify", "-format", "%w %h", path], capture_output=True, text=True,
                         check=True).stdout.split()
    return int(out[0]), int(out[1])


class FC:
    def __init__(self, project, log_path, width=1080, height=1920):
        self.project, self.width, self.height = project, width, height
        self.log = open(log_path, "w")
        self.busy = {}

    def new_sequence(self, name, fps, video, audio):
        r = subprocess.run(["filmcraft-cli", "--save-as", self.project, "exec", "file.newSequence",
                            json.dumps(dict(name=name, width=self.width, height=self.height, fps=fps,
                                            video=video, audio=audio, sampleRate=48000))],
                           capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(r.stderr)

    def c(self, cmd, **params):
        r = subprocess.run(["filmcraft-cli", "--project", self.project, "--save", "exec", cmd, json.dumps(params)],
                           capture_output=True, text=True)
        self.log.write(json.dumps({"cmd": cmd, "params": params, "exit": r.returncode,
                                   "result": r.stdout.strip()[:400], "stderr": r.stderr.strip()[:400]}) + "\n")
        self.log.flush()
        if r.returncode:
            raise RuntimeError(f"{cmd}: {r.stderr.strip()}")
        return json.loads(r.stdout) if r.stdout.strip() else None

    def import_media(self, paths):
        r = self.c("file.import", paths=[os.path.abspath(p) for p in paths])
        if r["errors"]:
            raise RuntimeError(r["errors"])
        return dict(zip(paths, r["items"]))

    def free_track(self, band, t0, t1):
        for i in range(band[0], band[1] + 1):
            if all(t1 <= a or t0 >= b for a, b in self.busy.get(i, [])):
                self.busy.setdefault(i, []).append((t0, t1))
                return i
        raise RuntimeError(f"no free track in {band} for {t0:.2f}-{t1:.2f}")

    def place(self, item, t0, t1, track=None, band=None, source_in=0.0, audio=False):
        idx = track if track is not None else self.free_track(band, t0, t1)
        if track is not None:
            self.busy.setdefault(idx, []).append((t0, t1))
        r = self.c("timeline.place", item=item, track=f"V{idx + 1}", seconds=round(t0, 4),
                   duration={"seconds": round(t1 - t0, 4)}, sourceIn={"seconds": round(source_in, 4)},
                   audio=audio)
        return r["clips"][0]

    def kf(self, clip, effect, param, t, value, ease=None):
        mt = self.c("effects.addKeyframe", clip=clip, effect=effect, param=param, time=ticks(t))["mediaTime"]
        self.c("effects.setKeyframe", clip=clip, effect=effect, param=param, mediaTime=mt, value=value)
        if ease:
            self.c("effects.setInterpolation", clip=clip, effect=effect, param=param, mediaTime=mt,
                   interpolation=ease)
        return mt

    def animate_in(self, clip, center, t0, d=0.45, rise=0, dx=0, t_out=None, end=None):
        self.c("effects.setParam", clip=clip, effect="motion", param="position", value=list(center))
        self.kf(clip, "opacity", "opacity", t0, 0)
        self.kf(clip, "opacity", "opacity", t0 + d * 0.7, 100)
        if rise or dx:
            self.kf(clip, "motion", "position", t0, [center[0] + dx, center[1] + rise], ease="easeOut")
            self.kf(clip, "motion", "position", t0 + d, list(center))
        if t_out is not None:
            self.kf(clip, "opacity", "opacity", t_out, 100)
            self.kf(clip, "opacity", "opacity", t_out + 0.25, 0)

    def image(self, item, path, x, y, t0, t1, band, d=0.45, rise=40, dx=0, t_out=None, center_x=False):
        w, h = png_size(path) if path.lower().endswith(".png") else (self.width, self.height)
        cx = self.width / 2 if center_x else x + w / 2
        clip = self.place(item, t0, t1 if t_out is None else min(t1, t_out + 0.3), band=band)
        self.animate_in(clip, (cx, y + h / 2), t0, d, rise, dx, t_out)
        return clip

    def text(self, runs, x, baseline, size, t0, t1, band, style="Bold", font="Noto Sans", align="center",
             widths=None, d=0.45, rise=30, t_out=None, props=None):
        end = t1 if t_out is None else min(t1, t_out + 0.3)
        idx = self.free_track(band, t0, end)
        full = "".join(t for t, _ in runs)
        r = self.c("graphics.newText", text=full, position=[round(x, 1), round(baseline, 1)], size=size, font=font,
                   fontStyle=style, seconds=round(end - t0, 4), track=idx, time=ticks(t0), newClip=True)
        clip, layer = r["clip"], r["layer"]
        self.c("graphics.set", clip=clip, layer=layer, props=dict(align=align, fill_color=runs[0][1], **(props or {})))
        pos = 0
        for txt, color in runs:
            if color != runs[0][1] and txt:
                self.c("graphics.setCharStyle", clip=clip, layer=layer, start=pos, end=pos + len(txt),
                       style={"color": color})
            pos += len(txt)
        self.kf(clip, "opacity", "opacity", t0, 0)
        self.kf(clip, "opacity", "opacity", t0 + d * 0.7, 100)
        if rise:
            c0 = [self.width / 2, self.height / 2]
            self.kf(clip, "motion", "position", t0, [c0[0], c0[1] + rise], ease="easeOut")
            self.kf(clip, "motion", "position", t0 + d, c0)
        if t_out is not None:
            self.kf(clip, "opacity", "opacity", t_out, 100)
            self.kf(clip, "opacity", "opacity", t_out + 0.25, 0)
        return clip

    def push_in(self, clip, t0, t1, amount=5):
        self.kf(clip, "motion", "scale", t0, 100)
        self.kf(clip, "motion", "scale", t1, 100 + amount)
