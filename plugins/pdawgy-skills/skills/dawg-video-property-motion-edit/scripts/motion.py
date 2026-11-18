import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import project as P
from cards import sh, text_width
from captions import build_track, AMBERSTYLE

FPS = P.FPS
BOLD, MED = P.FONT_BOLD, P.FONT_MED
REG = MED
BG, AMBER = P.BG, P.AMBER
A = os.path.join(P.WORK, "reel")


def set_assets(path):
    global A
    A = path
    os.makedirs(A, exist_ok=True)


def take(stem):
    return os.path.join(P.PROXY_PLAY, f"{stem}.mp4")


def ease(t0, d, var="t"):
    return f"(1-pow(1-min(max(({var}-{t0})/{d},0),1),3))"


def headline(name, parts, size=78, width=980):
    out = os.path.join(A, f"{name}.png")
    spans = "".join(
        f'<span foreground="{c}">{t.replace("&", "&amp;")}</span>' for t, c in parts)
    markup = f'<span font_desc="Noto Sans Bold {size}px" letter_spacing="-1500">{spans}</span>'
    sh(["magick", "-background", "none", "-density", "72", "-size", f"{width}x",
        "-define", "pango:align=center", f"pango:{markup}", "-trim", "+repage", "PNG32:" + out])
    return out


def small_text(name, text, size=34, color="#B9B2A8", font=MED):
    out = os.path.join(A, f"{name}.png")
    sh(["magick", "-background", "none", "-font", font, "-pointsize", str(size),
        "-kerning", "1", "-fill", color, f"label:{text}", "PNG32:" + out])
    return out


def rounded_mask(name, w, h, r):
    out = os.path.join(A, f"{name}.png")
    sh(["magick", "-size", f"{w}x{h}", "xc:black", "-fill", "white",
        "-draw", f"roundrectangle 0,0 {w - 1},{h - 1} {r},{r}", out])
    return out


def glow(name, w, h, r, angle=0, color=AMBER, opacity=0.55, blur=45):
    out = os.path.join(A, f"{name}.png")
    pad = blur * 3
    sh(["magick", "-size", f"{w + 2 * pad}x{h + 2 * pad}", "xc:none",
        "-fill", color, "-draw", f"roundrectangle {pad},{pad} {pad + w},{pad + h} {r},{r}",
        "-channel", "A", "-evaluate", "multiply", str(opacity), "+channel",
        "-blur", f"0x{blur}", "-background", "none", "-rotate", str(angle), "PNG32:" + out])
    return out


def background():
    out = os.path.join(A, "bg.png")
    sh(["magick", "-size", "1080x1920", f"xc:{BG}",
        "(", "-size", "1500x1500", "radial-gradient:rgba(150,92,38,0.55)-rgba(13,11,9,0)", ")",
        "-geometry", "-210+300", "-composite",
        "(", "-size", "900x900", "radial-gradient:rgba(120,70,30,0.35)-rgba(13,11,9,0)", ")",
        "-geometry", "+500-200", "-composite", out])
    return out


def plan_card(name, src, crop, label, sub, angle, scale=1.0):
    out = os.path.join(A, f"{name}.png")
    tmp = os.path.join(A, f"{name}_flat.png")
    sh(["magick", src, "-crop", crop, "+repage", "-resize", "400x360",
        "-background", "white", "-gravity", "center", "-extent", "420x380",
        "(", "-size", "420x110", "xc:white", "-font", BOLD, "-pointsize", "36", "-fill", "#1B1712",
        "-gravity", "northwest", "-annotate", "+24+14", label,
        "-font", MED, "-pointsize", "26", "-fill", "#9A6A2E", "-annotate", "+24+62", sub, ")",
        "-append",
        "(", "+clone", "-alpha", "extract", "-fill", "black", "-colorize", "100",
        "-fill", "white", "-draw", "roundrectangle 0,0 419,489 26,26", ")",
        "-alpha", "off", "-compose", "copy_opacity", "-composite", "PNG32:" + tmp])
    sh(["magick", tmp, "(", "+clone", "-background", "black", "-shadow", "60x18+0+14", ")",
        "+swap", "-background", "none", "-layers", "merge", "+repage",
        "-resize", f"{int(scale * 100)}%", "-rotate", str(angle), "PNG32:" + out])
    return out


def check_row(name, text, w=780):
    out = os.path.join(A, f"{name}.png")
    sh(["magick", "-size", f"{w}x104", "xc:none",
        "-fill", "rgba(28,23,18,0.88)", "-stroke", "rgba(232,168,92,0.45)", "-strokewidth", "2",
        "-draw", f"roundrectangle 1,1 {w - 2},102 24,24", "-stroke", "none",
        "-fill", AMBER, "-draw", "circle 58,52 58,26",
        "-stroke", BG, "-strokewidth", "6", "-fill", "none",
        "-draw", "polyline 45,53 55,63 72,42", "-stroke", "none",
        "-font", MED, "-pointsize", "40", "-fill", "white",
        "-gravity", "west", "-annotate", "+108+0", text, "PNG32:" + out])
    return out


def cta_pill(name, text):
    out = os.path.join(A, f"{name}.png")
    tw = text_width(text, BOLD, 38, 0)
    w, h = tw + 88, 92
    sh(["magick", "-size", f"{w}x{h}", "xc:none", "-fill", AMBER,
        "-draw", f"roundrectangle 0,0 {w - 1},{h - 1} 46,46",
        "-font", BOLD, "-pointsize", "38", "-kerning", "0", "-fill", BG,
        "-gravity", "center", "-annotate", "+0+0", text, "PNG32:" + out])
    return out


def chip(name, text):
    out = os.path.join(A, f"{name}.png")
    tw = text_width(text, BOLD, 40, 2)
    w, h = tw + 64, 84
    sh(["magick", "-size", f"{w}x{h}", "xc:none", "-fill", "rgba(30,25,20,0.92)", "-stroke", AMBER,
        "-strokewidth", "3", "-draw", f"roundrectangle 2,2 {w - 3},{h - 3} 40,40", "-stroke", "none",
        "-font", BOLD, "-pointsize", "40", "-kerning", "2", "-fill", AMBER,
        "-gravity", "center", "-annotate", "+0+0", text, "PNG32:" + out])
    return out


class Seg:
    def __init__(self, name, video, dur, audio_pad=0.0):
        self.name, self.dur = name, dur + audio_pad
        self.inputs = [["-loop", "1", "-framerate", str(FPS), "-t", f"{self.dur:.3f}", "-i", A + "/bg.png"],
                       ["-i", video]]
        self.g = [f"[0:v]format=rgba,setsar=1[base0]"]
        self.base = "base0"
        self.n = 0
        self.audio_pad = audio_pad
        self.video_dur = dur

    def img(self, path):
        self.inputs.append(["-loop", "1", "-framerate", str(FPS), "-t", f"{self.dur:.3f}", "-i", path])
        return f"{len(self.inputs) - 1}:v"

    def lab(self):
        self.n += 1
        return f"L{self.n}"

    def over(self, src, x, y, enable=None):
        out = self.lab()
        en = f":enable='{enable}'" if enable else ""
        self.g.append(f"[{self.base}][{src}]overlay=x={x}:y={y}:eval=frame:eof_action=pass{en}[{out}]")
        self.base = out

    def layer(self, path, t_in, x, y, rise=40, d=0.45, t_out=None, dx=0):
        s = self.img(path)
        lab = self.lab()
        chain = f"[{s}]format=rgba,fade=t=in:st={t_in:.3f}:d={d * 0.7:.3f}:alpha=1"
        if t_out is not None:
            chain += f",fade=t=out:st={t_out:.3f}:d=0.25:alpha=1"
        self.g.append(chain + f"[{lab}]")
        e = ease(t_in, d)
        self.over(lab, f"'{x}+{dx}*(1-{e})'", f"'{y}+{rise}*(1-{e})'",
                  enable=f"gte(t,{t_in:.3f})" + (f"*lte(t,{t_out + 0.3:.3f})" if t_out else ""))

    def card(self, w, h, r, angle, x, y, t_in=0.0, glow_png=None, src="1:v"):
        mask = rounded_mask(f"{self.name}_mask{w}x{h}", w, h, r)
        m = self.img(mask)
        v, c = self.lab(), self.lab()
        rot = f",rotate={angle}*PI/180:c=none:ow=rotw({angle}*PI/180):oh=roth({angle}*PI/180)" if angle else ""
        self.g.append(f"[{src}]scale={w}:{h},setsar=1,format=rgba[{v}];[{m}]format=gray,scale={w}:{h}[{v}m];"
                      f"[{v}][{v}m]alphamerge{rot},fade=t=in:st={t_in:.3f}:d=0.25:alpha=1[{c}]")
        if glow_png:
            gl = self.img(glow_png)
            self.over(gl, f"'{x}+({w}-overlay_w)/2'", f"'{y}+({h}-overlay_h)/2'")
        e = ease(t_in, 0.5)
        self.over(c, f"'{x}+({w}-overlay_w)/2'", f"'{y}+({h}-overlay_h)/2+60*(1-{e})'")

    def zoom_card(self, t0, d, s_end, cy_end, src="1:v"):
        mask = os.path.join(A, f"{self.name}_zmask.png")
        sh(["magick", "-size", "1080x1920", "xc:black", "-fill", "white",
            "-draw", "roundrectangle 6,6 1073,1913 70,70", mask])
        m = self.img(mask)
        e = ease(t0, d, var=f"(in/{FPS})")
        s = f"(1-(1-{s_end})*{e})"
        cy = f"(960+({cy_end}-960)*{e})"
        L, R = f"(540-540*{s})", f"(540+540*{s})"
        T, B = f"({cy}-960*{s})", f"({cy}+960*{s})"
        full, sm, v, vm, c = self.lab(), self.lab(), self.lab(), self.lab(), self.lab()
        self.g.append(f"[{src}]setsar=1,split[{full}][{sm}]")
        self.g.append(f"[{sm}]format=rgba[{v}];[{m}]format=gray[{vm}];"
                      f"[{v}][{vm}]alphamerge,format=yuva444p,"
                      f"perspective=x0='{L}':y0='{T}':x1='{R}':y1='{T}':x2='{L}':y2='{B}':x3='{R}':y3='{B}':"
                      f"sense=destination:eval=frame:interpolation=linear[{c}]")
        self.over(full, "0", "0", enable=f"lt(t,{t0:.3f})")
        self.over(c, "0", "0", enable=f"gte(t,{t0:.3f})")

    def full(self, src="1:v", push=0.05):
        lab = self.lab()
        self.g.append(f"[{src}]setsar=1,scale=w='trunc(1080*(1+{push}*t/{self.dur:.3f})/2)*2':h=-2:eval=frame,"
                      f"crop=1080:1920,format=rgba[{lab}]")
        self.over(lab, "0", "0")

    def cut_to(self, path, at, push=0.06):
        self.inputs.append(["-i", path])
        lab = self.lab()
        self.g.append(f"[{len(self.inputs) - 1}:v]setpts=PTS-STARTPTS,setsar=1,"
                      f"scale=w='trunc(1080*(1+{push}*t/{self.dur - at:.3f})/2)*2':h=-2:eval=frame,crop=1080:1920,"
                      f"tpad=start_duration={at:.3f}:start_mode=clone,format=rgba[{lab}]")
        self.over(lab, "0", "0", enable=f"gte(t,{at:.3f})")

    def scrim(self, y, h, top=True, strength=0.85, t_in=None):
        path = os.path.join(A, f"{self.name}_scrim{y}_{h}_{int(top)}.png")
        a, b = (f"rgba(13,11,9,{strength})", "rgba(13,11,9,0)") if top else ("rgba(13,11,9,0)", f"rgba(13,11,9,{strength})")
        sh(["magick", "-size", f"1080x{h}", f"gradient:{a}-{b}", "PNG32:" + path])
        if t_in is None:
            self.over(self.img(path), "0", str(y))
        else:
            self.layer(path, t_in, 0, y, rise=0, d=0.4)

    def glass(self, x, y, w, h, r, t_in=0.0):
        m = self.img(rounded_mask(f"{self.name}_glass{w}x{h}", w, h, r))
        edge = os.path.join(A, f"{self.name}_glassedge{w}x{h}.png")
        sh(["magick", "-size", f"{w}x{h}", "xc:none", "-fill", "rgba(20,16,12,0.38)",
            "-stroke", "rgba(255,240,220,0.22)", "-strokewidth", "2",
            "-draw", f"roundrectangle 1,1 {w - 2},{h - 2} {r},{r}", "PNG32:" + edge])
        a, b, c, gm, gl = self.lab(), self.lab(), self.lab(), self.lab(), self.lab()
        self.g.append(f"[{self.base}]split[{a}][{b}];[{b}]crop={w}:{h}:{x}:{y},boxblur=22:2,"
                      f"eq=brightness=-0.10:saturation=0.85,format=rgba[{c}];[{m}]format=gray[{gm}];"
                      f"[{c}][{gm}]alphamerge,fade=t=in:st={t_in:.3f}:d=0.3:alpha=1[{gl}]")
        self.base = a
        self.over(gl, str(x), str(y))
        self.layer(edge, t_in, x, y, rise=0, d=0.3)

    def video(self, path, at):
        self.inputs.append(["-i", path])
        lab = self.lab()
        self.g.append(f"[{len(self.inputs) - 1}:v]setpts=PTS-STARTPTS,tpad=start_duration={at:.3f}:start_mode=clone[{lab}]")
        return lab

    def seq(self, pattern, t_in, push=0.06, mask=None):
        self.inputs.append(["-framerate", str(FPS), "-i", pattern])
        c = self.lab()
        d = self.dur - t_in
        src = f"[{len(self.inputs) - 1}:v]format=rgba"
        if mask:
            m, mm = self.img(mask), self.lab()
            self.g.append(f"[{m}]format=gray[{mm}]")
            src = f"[{len(self.inputs) - 2}:v]format=rgba[{c}x];[{c}x][{mm}]alphamerge"
        self.g.append(f"{src},"
                      f"scale=w='trunc(1080*(1+{push}*t/{d:.3f})/2)*2':h=-2:eval=frame,crop=1080:1920,"
                      f"setpts=PTS-STARTPTS,tpad=start_duration={t_in:.3f}:start_mode=add:color=black@0.0,"
                      f"fade=t=in:st={t_in:.3f}:d=0.25:alpha=1[{c}]")
        self.over(c, "0", "0", enable=f"gte(t,{t_in:.3f})")

    def captions(self, clip_name, y, hide=()):
        pat = build_track(os.path.join(A, f"{self.name}_cap"), [(clip_name, 0.0)], self.dur,
                          AMBERSTYLE, karaoke=True, hide=hide)
        self.inputs.append(["-framerate", str(FPS), "-i", pat])
        c = self.lab()
        self.g.append(f"[{len(self.inputs) - 1}:v]format=rgba[{c}]")
        self.over(c, "0", str(y - 100))

    def bar(self, x, y, w_full, h, color, t0, d=0.7):
        e = ease(t0, d)
        out = self.lab()
        self.g.append(f"[{self.base}]drawbox=x={x}:y={y}:w='max(2,{w_full}*{e})':h={h}:"
                      f"color={color}:t=fill:enable='gte(t,{t0 + 0.02:.3f})'[{out}]")
        self.base = out

    def counter(self, target, t0, d, y, size=170):
        cnt = ease(t0, d)
        val = f"({target}*{cnt})"
        out = self.lab()
        common = (f"fontfile={BOLD}:fontsize={size}:fontcolor={AMBER}:x=(w-text_w)/2:y={y}:"
                  f"alpha='min(max((t-{t0})/0.25,0),1)'")
        self.g.append(f"[{self.base}]drawtext={common}:text='%{{eif\\:{val}\\:d}}'"
                      f":enable='gte(t,{t0:.3f})'[{out}]")
        self.base = out

    def render(self, out):
        self.g.append(f"[{self.base}]trim=0:{self.dur:.3f},format=yuv420p[vout]")
        af = f"[1:a]apad=whole_dur={self.dur:.3f},afade=t=out:st={self.dur - 0.08:.3f}:d=0.08[aout]"
        if self.audio_pad:
            af = (f"[1:a]afade=t=out:st={self.video_dur - 0.3:.3f}:d=0.3,"
                  f"apad=whole_dur={self.dur:.3f}[aout]")
        self.g.append(af)
        script = os.path.join(A, f"{self.name}.graph")
        with open(script, "w") as fh:
            fh.write(";\n".join(self.g))
        cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y"]
        for i in self.inputs:
            cmd += i
        cmd += ["-/filter_complex", script, "-map", "[vout]", "-map", "[aout]", "-r", str(FPS),
                "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{self.dur:.3f}", out]
        subprocess.run(cmd, check=True)
        return out
