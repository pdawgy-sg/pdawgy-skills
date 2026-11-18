import json
import math
import os
import subprocess

from cards import FONT_SERIF, FONT_SANS_MED, ease_out

import project as P

SITE = P.SITE
W, H = 1080, 1920
PIN = (540, 900)
PX_PER_M = 0.42
CLIP = None

PALETTES = {
    "cream": {"bg": "#F1EBDD", "park": "#E4E2C9", "water": "#CFE0E6", "major": "#D6C391",
              "minor": "#E4D8B6", "rail": "#B9A26A", "ring": "#8A784A", "pin": "#2B2620",
              "label_bg": "rgba(243,239,231,0.96)", "label_fg": "#8A784A", "attr": "#9C927E"},
    "hud": {"bg": "none", "park": "none", "water": "none", "major": "rgba(245,188,112,0.95)",
            "minor": "rgba(245,188,112,0.50)", "rail": "#F5BC70", "ring": "#F5BC70", "pin": "#F5BC70",
            "label_bg": "rgba(14,11,8,0.94)", "label_fg": "#F6EBDD", "site_fg": "#F5BC70", "attr": "#D8D0C4",
            "label_size": 32, "site_size": 44, "ring_w": 6, "pin_r": 18},
    "card": {"bg": "#F4EEE2", "park": "#E7E3CC", "water": "#D3E2E6", "major": "#D7AE5E", "minor": "#E6D3AA",
             "rail": "#B07A2E", "ring": "#B0702A", "pin": "#1E1A15", "label_bg": "rgba(30,25,20,0.94)",
             "label_fg": "#F6EBDD", "site_fg": "#F5BC70", "attr": "#9C927E",
             "label_size": 32, "site_size": 44, "ring_w": 6, "pin_r": 18},
    "dark": {"bg": "#14110D", "park": "#1E2117", "water": "#16232A", "major": "#5A4630",
             "minor": "#3A2F22", "rail": "#E8A85C", "ring": "#E8A85C", "pin": "#E8A85C",
             "label_bg": "rgba(30,25,20,0.94)", "label_fg": "#E8A85C", "attr": "#6E6656"},
}
MAJOR = {"motorway", "trunk", "primary", "secondary", "motorway_link", "trunk_link", "primary_link"}


def project(lat, lon):
    x = (lon - SITE[1]) * math.cos(math.radians(SITE[0])) * 111320
    y = (lat - SITE[0]) * 110540
    return PIN[0] + x * PX_PER_M, PIN[1] - y * PX_PER_M


def dist_m(lat, lon):
    x = (lon - SITE[1]) * math.cos(math.radians(SITE[0])) * 111320
    y = (lat - SITE[0]) * 110540
    return math.hypot(x, y)


NOMI = os.path.join(P.WORK, "map", "nominatim.json")
MAJOR_ROADS = P.MAJOR_ROADS
POIS = P.POIS


def pois(kind, limit=5, within=None):
    data = json.load(open(NOMI))
    found = {n: (la, lo) for n, la, lo, _t in data["pois"].get(kind, [])}
    out = []
    for name, la, lo in POIS[kind]:
        if la is None:
            if name not in found:
                continue
            la, lo = found[name]
        out.append((dist_m(la, lo), name, la, lo))
    return sorted(out)[:limit]


def _lines(geo):
    t = geo.get("type")
    if t == "LineString":
        return [geo["coordinates"]]
    if t == "MultiLineString":
        return geo["coordinates"]
    if t == "Polygon":
        return [geo["coordinates"][0]]
    return []


def base_map(path, pal):
    p = PALETTES[pal]
    data = json.load(open(NOMI))
    majors, minors = [], []
    for name, geoms in data["roads"].items():
        for geo in geoms:
            for line in _lines(geo):
                pts = [project(la, lo) for lo, la in line]
                if len(pts) < 2:
                    continue
                s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
                (majors if name in MAJOR_ROADS else minors).append(s)
    def layer(lines, col, width, close, out):
        mask = out + ".mask.png"
        cmd = ["-size", f"{W}x{H}", "xc:black", "-fill", "none", "-stroke", "white", "-strokewidth", str(width)]
        for s in lines:
            cmd += ["-draw", f"stroke-linecap round stroke-linejoin round polyline {s}"]
        cmd += ["-morphology", "Close", f"Disk:{close}", mask]
        subprocess.run(["magick"] + cmd, check=True)
        subprocess.run(["magick", "-size", f"{W}x{H}", f"xc:{col}", mask, "-alpha", "off",
                        "-compose", "copy_opacity", "-composite", "PNG32:" + out], check=True)
        return out
    mi = layer(minors, p["minor"], 5, 7, path + ".minor.png")
    ma = layer(majors, p["major"], 10, 22, path + ".major.png")
    subprocess.run(["magick", "-size", f"{W}x{H}", f"xc:{p['bg']}", mi, "-composite", ma, "-composite", path],
                   check=True)
    if pal == "hud" and CLIP:
        x0, cy0, x1, cy1, r = CLIP
        subprocess.run(["magick", path, "(", "-size", f"{W}x{H}", "xc:none", "-fill", "white",
                        "-draw", f"roundrectangle {x0},{cy0} {x1},{cy1} {r},{r}", ")",
                        "-compose", "DstIn", "-composite", "PNG32:" + path], check=True)
    elif pal == "hud":
        y0 = int(PIN[1] + 1000 * PX_PER_M * 0.85)
        y1 = y0 + 220
        subprocess.run(["magick", path, "(", "-size", f"{W}x{y0}", "xc:white",
                        "-size", f"{W}x{y1 - y0}", "gradient:white-black",
                        "-size", f"{W}x{H - y1}", "xc:black", "-append", "-alpha", "copy", ")",
                        "-compose", "DstIn", "-composite", "PNG32:" + path], check=True)
    return path


def label_png(path, text, pal, size=34, sub=None, fg=None):
    p = PALETTES[pal]
    cmd = ["magick", "-background", "none",
           "(", "-font", FONT_SERIF, "-pointsize", str(size), "-kerning", "3", "-fill", fg or p["label_fg"],
           f"label:{text.upper()}", ")"]
    if sub:
        cmd += ["(", "-font", FONT_SANS_MED, "-pointsize", "20", "-kerning", "2", "-fill", p["attr"],
                f"label:{sub.upper()}", ")", "-gravity", "center", "-append"]
    cmd += ["-bordercolor", "none", "-border", "16x8",
            "(", "+clone", "-alpha", "off", "-fill", p["label_bg"], "-colorize", "100", ")",
            "+swap", "-compose", "over", "-composite", "PNG32:" + path]
    subprocess.run(cmd, check=True)
    out = subprocess.run(["magick", "identify", "-format", "%w %h", path], check=True,
                         capture_output=True, text=True).stdout.split()
    return int(out[0]), int(out[1])


def render(outdir, dur, pal="cream", site_label="Amberwood", site_sub=None, labels=(), ring_at=0.15,
           fps=30, pin=None, scale=None, avoid=(), clip=None):
    global PIN, PX_PER_M, CLIP
    saved = (PIN, PX_PER_M, CLIP)
    CLIP = clip
    if pin:
        PIN = pin
    if scale:
        PX_PER_M = scale
    try:
        return _render(outdir, dur, pal, site_label, site_sub, labels, ring_at, fps, avoid)
    finally:
        PIN, PX_PER_M, CLIP = saved


def _render(outdir, dur, pal, site_label, site_sub, labels, ring_at, fps, avoid):
    os.makedirs(outdir, exist_ok=True)
    p = PALETTES[pal]
    base = base_map(os.path.join(outdir, "_base.png"), pal)
    ring_r = 1000 * PX_PER_M
    site_png = os.path.join(outdir, "_site.png")
    sw, sh_ = label_png(site_png, site_label, pal, p.get("site_size", 38), site_sub, fg=p.get("site_fg"))
    lab, boxes = [], [(PIN[0] + 26, PIN[1] - sh_ // 2, PIN[0] + 26 + sw, PIN[1] + sh_ // 2)] + list(avoid)
    for i, (text, lat, lon, t0) in enumerate(labels):
        f = os.path.join(outdir, f"_lab{i}.png")
        lw, lh = label_png(f, text, pal, p.get("label_size", 26))
        x, y = project(lat, lon)
        sides = [x + 18, x - 18 - lw] if x + 18 + lw < W - 30 else [x - 18 - lw, x + 18]
        placed = None
        for dy in (0, -1, 1, -2, 2, -3, 3):
            for cand in sides:
                ly = y - lh / 2 + dy * (lh * 0.6)
                if cand < 20 or cand + lw > W - 20:
                    continue
                if not [b for b in boxes if cand < b[2] and cand + lw > b[0] and ly < b[3] + 2 and ly + lh > b[1] - 2]:
                    placed = (cand, ly)
                    break
            if placed:
                break
        lx, ly = placed or (sides[0], y - lh / 2)
        boxes.append((lx, ly, lx + lw, ly + lh))
        lab.append((f, lw, lh, x, y, t0, lx, ly))
    km_png = os.path.join(outdir, "_km.png")
    kw, kh = label_png(km_png, "1 km", pal, 24)
    n = int(round(dur * fps))
    for fr in range(n):
        t = fr / fps
        cmd = ["magick", base]
        rp = ease_out((t - ring_at) / 1.1)
        if rp > 0:
            cmd += ["-fill", "none", "-stroke", p["ring"], "-strokewidth", str(p.get("ring_w", 3)),
                    "-draw", f"arc {PIN[0] - ring_r:.0f},{PIN[1] - ring_r:.0f} {PIN[0] + ring_r:.0f},"
                             f"{PIN[1] + ring_r:.0f} -90,{-90 + 360 * rp:.1f}", "-stroke", "none"]
        ka = ease_out((t - ring_at - 0.9) / 0.3)
        if ka > 0:
            cmd += ["(", km_png, "-channel", "A", "-evaluate", "multiply", f"{ka:.3f}", "+channel", ")",
                    "-geometry", f"+{PIN[0] - kw // 2}+{int(PIN[1] - ring_r - kh // 2)}", "-composite"]
        for f, lw, lh, x, y, t0, lx, ly in lab:
            a = ease_out((t - t0) / 0.3)
            if a <= 0:
                continue
            cmd += ["-fill", p["pin"], "-stroke", p["bg"], "-strokewidth", "3",
                    "-draw", f"circle {x:.0f},{y:.0f} {x + 9 * a:.0f},{y:.0f}", "-stroke", "none",
                    "(", f, "-channel", "A", "-evaluate", "multiply", f"{a:.3f}", "+channel", ")",
                    "-geometry", f"+{int(lx)}+{int(ly + (1 - a) * 12)}", "-composite"]
        pulse = (t * 0.8) % 1.0
        cmd += ["-fill", "none", "-stroke", f"rgba(138,120,74,{0.6 * (1 - pulse):.2f})" if pal == "cream"
                else f"rgba(232,168,92,{0.6 * (1 - pulse):.2f})", "-strokewidth", "3",
                "-draw", f"circle {PIN[0]},{PIN[1]} {PIN[0] + 14 + 40 * pulse:.0f},{PIN[1]}", "-stroke", "none",
                "-fill", p["pin"], "-stroke", p["bg"], "-strokewidth", "4",
                "-draw", f"circle {PIN[0]},{PIN[1]} {PIN[0] + p.get('pin_r', 14)},{PIN[1]}", "-stroke", "none",
                site_png, "-geometry", f"+{PIN[0] + 12 + p.get('pin_r', 14)}+{PIN[1] - sh_ // 2}", "-composite"]
        cmd += ["-font", FONT_SANS_MED, "-pointsize", "18", "-fill", p["attr"], "-gravity", "southwest",
                "-annotate", "+90+110", "© OpenStreetMap contributors", "-gravity", "northwest",
                "PNG32:" + os.path.join(outdir, f"f{fr:04d}.png")]
        subprocess.run(cmd, check=True)
    return os.path.join(outdir, "f%04d.png")
