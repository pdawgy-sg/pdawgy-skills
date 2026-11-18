import json
import os
import re
import subprocess

import project as P

WORDS = os.path.join(P.WORK, "words.json")
FPS = P.FPS
COMPARABLE = P.COMPARABLE
FIXES = P.CAPTION_FIXES
KEYWORDS = P.KEYWORDS
SKIP_CLIPS = P.SKIP_CLIPS
WORD_FIXES = P.WORD_FIXES
CHUNKS = P.CHUNKS


def load_words():
    data = json.load(open(WORDS))
    out = {}
    for clip, ws in data.items():
        if clip in SKIP_CLIPS:
            continue
        merged = []
        for w in ws:
            if merged and re.match(r"^[-.]", w["w"]):
                merged[-1] = {"w": merged[-1]["w"] + w["w"], "s": merged[-1]["s"], "e": w["e"]}
            else:
                merged.append(dict(w))
        for i, txt in WORD_FIXES.get(clip, {}).items():
            merged[i]["w"] = txt
        out[clip] = merged
    return out


def chunk(words, max_words=4, max_chars=24, clip=None):
    if clip in CHUNKS and sum(CHUNKS[clip]) == len(words):
        out, i = [], 0
        for n in CHUNKS[clip]:
            out.append(words[i:i + n])
            i += n
        return out
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        text = " ".join(x["w"] for x in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        brk = (len(cur) >= max_words or len(text) >= max_chars or w["w"][-1] in ",.?!"
               or (nxt and nxt["s"] - w["e"] > 0.45))
        if brk or nxt is None:
            chunks.append(cur)
            cur = []
    return chunks


def apply_fixes(text):
    for a, b in FIXES.items():
        text = text.replace(a, b)
    return text


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _render(path, words, active, style):
    line = apply_fixes(" ".join(words)).rstrip(",")
    marks = [False] * len(line)
    if style.get("keywords", True):
        for kw in KEYWORDS:
            for m in re.finditer(re.escape(apply_fixes(kw)), line, flags=re.I):
                for k in range(m.start(), m.end()):
                    marks[k] = True
    if active is not None:
        pos = 0
        for i, w in enumerate(words):
            w_fixed = apply_fixes(w)
            j = line.find(w_fixed.rstrip(","), pos)
            if j < 0:
                continue
            if i == active:
                for k in range(j, j + len(w_fixed.rstrip(","))):
                    marks[k] = True
            pos = j + len(w_fixed)
    spans, k = [], 0
    while k < len(line):
        j = k
        while j < len(line) and marks[j] == marks[k]:
            j += 1
        col = style["accent"] if marks[k] else "white"
        spans.append(f'<span foreground="{col}">{esc(line[k:j])}</span>')
        k = j
    markup = f'<span font_desc="Noto Sans Bold {style["size"]}px">{"".join(spans)}</span>'
    txt = path + ".txt.png"
    subprocess.run(["magick", "-background", "none", "-density", "72", f"pango:{markup}",
                    "-trim", "+repage", "PNG32:" + txt], check=True)
    w, h = map(int, subprocess.run(["magick", "identify", "-format", "%w %h", txt],
                                   check=True, capture_output=True, text=True).stdout.split())
    px, py = style.get("pad", (22, 14))
    bw, bh = w + 2 * px, h + 2 * py
    subprocess.run(["magick", "-size", "1080x200", "xc:none", "-fill", style["box"],
                    "-draw", f"roundrectangle {(1080 - bw) // 2},{(200 - bh) // 2} "
                             f"{(1080 + bw) // 2},{(200 + bh) // 2} {style.get('radius', 10)},"
                             f"{style.get('radius', 10)}",
                    txt, "-gravity", "center", "-composite", "PNG32:" + path], check=True)
    os.remove(txt)


def build_track(outdir, placements, total, style, karaoke=False, hide=()):
    words = load_words()
    states = []
    sdir = os.path.join(outdir, "states")
    os.makedirs(sdir, exist_ok=True)
    blank = os.path.join(sdir, "blank.png")
    subprocess.run(["magick", "-size", "1080x200", "xc:none", "PNG32:" + blank], check=True)
    n = 0
    for pl in placements:
        clip, off = pl[0], pl[1]
        t_from = pl[2] if len(pl) > 2 else -1.0
        t_to = pl[3] if len(pl) > 3 else 1e9
        ch = [c for c in chunk(words[clip], clip=clip) if t_from <= c[0]["s"] < t_to]
        for ci, c in enumerate(ch):
            t0 = c[0]["s"]
            nxt = ch[ci + 1][0]["s"] if ci + 1 < len(ch) else None
            t1 = min(nxt, c[-1]["e"] + 0.5) if nxt is not None else c[-1]["e"] + 0.5
            t1 = min(t1, t_to)
            disp = [w["w"] for w in c]
            if karaoke:
                for wi, w in enumerate(c):
                    a = w["s"]
                    b = c[wi + 1]["s"] if wi + 1 < len(c) else t1
                    png = os.path.join(sdir, f"s{n:04d}.png")
                    _render(png, disp, wi, style)
                    states.append((off + a, off + b, png))
                    n += 1
            else:
                png = os.path.join(sdir, f"s{n:04d}.png")
                _render(png, disp, None, style)
                states.append((off + t0, off + t1, png))
                n += 1
    fdir = os.path.join(outdir, "frames")
    if os.path.isdir(fdir):
        for f in os.listdir(fdir):
            os.remove(os.path.join(fdir, f))
    os.makedirs(fdir, exist_ok=True)
    for i in range(int(round(total * FPS))):
        t = (i + 0.5) / FPS
        src = blank
        if not any(a <= t < b for a, b in hide):
            for a, b, p in states:
                if a <= t < b:
                    src = p
                    break
        os.symlink(src, os.path.join(fdir, f"f{i:05d}.png"))
    return os.path.join(fdir, "f%05d.png")


SIGLAP = {"size": 44, "accent": "#F0C75E", "box": "rgba(28,28,28,0.74)", "pad": (22, 12), "radius": 10}
AMBERSTYLE = {"size": 48, "accent": "#E8A85C", "box": "rgba(18,14,10,0.82)", "pad": (26, 14),
              "radius": 18, "keywords": False}

if __name__ == "__main__":
    for clip, ws in load_words().items():
        for c in chunk(ws, clip=clip):
            print(clip, f"{c[0]['s']:.2f}", apply_fixes(" ".join(w["w"] for w in c)))
