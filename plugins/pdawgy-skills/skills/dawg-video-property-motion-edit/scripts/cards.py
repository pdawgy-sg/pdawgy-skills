import functools
import os
import subprocess

FONT_SERIF = "/usr/share/fonts/noto/NotoSerifDisplay-Regular.ttf"
FONT_SANS_MED = "/usr/share/fonts/noto/NotoSans-Medium.ttf"

CREAM = "#F3EFE7"
CREAM_EDGE = "#D9D0BD"
OLIVE = "#8A784A"
PILL = "rgba(40,38,34,0.62)"


def sh(args):
    subprocess.run(args, check=True)


@functools.lru_cache(maxsize=None)
def text_width(text, font, size, kerning):
    if not text:
        return 0
    out = subprocess.run(
        ["magick", "-background", "none", "-font", font, "-pointsize", str(size),
         "-kerning", str(kerning), f"label:{text}", "-format", "%w", "info:"],
        check=True, capture_output=True, text=True)
    return int(out.stdout)


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def card_dir(base, text, sub="", size=78):
    import hashlib
    key = hashlib.md5(f"{text}|{sub}|{size}".encode()).hexdigest()[:10]
    return os.path.join(base, f"card_{key}")


def make_card(text, sub, outdir, size=78, kerning=5, fps=30, frames=None):
    os.makedirs(outdir, exist_ok=True)
    pad_x, pad_y = 44, 22
    tw = text_width(text, FONT_SERIF, size, kerning)
    th = int(size * 1.35)
    box_w, box_h = tw + 2 * pad_x, th + 2 * pad_y

    sub_size, sub_kern = 27, 4
    sub_text = f"—  {sub.upper()}" if sub else ""
    sw = text_width(sub_text, FONT_SANS_MED, sub_size, sub_kern) if sub else 0
    pill_w, pill_h = sw + 36, 50
    gap = 14
    W = max(box_w, pill_w) + 8
    H = box_h + (gap + pill_h if sub else 0) + 8
    bx = (W - box_w) // 2
    by = 4

    offs = [text_width(text[:i], FONT_SERIF, size, kerning) for i in range(len(text))]

    box_in = 7
    stagger = 1.6
    char_fade = 6
    text_end = box_in + stagger * len(text) + char_fade
    sheen_start, sheen_len = text_end - 4, 14
    sub_start = text_end - 2
    sub_len = 8
    n = frames or int(sub_start + sub_len + 2)

    for f in range(n):
        p = ease_out(f / box_in)
        cur_w = max(2, int(box_w * (0.35 + 0.65 * p)))
        alpha = min(1.0, f / 3)
        cx0 = bx + (box_w - cur_w) // 2
        cmd = ["magick", "-size", f"{W}x{H}", "xc:none"]
        cmd += ["-fill", f"rgba(243,239,231,{0.95 * alpha:.3f})",
                "-stroke", f"rgba(217,208,189,{alpha:.3f})", "-strokewidth", "2",
                "-draw", f"rectangle {cx0},{by} {cx0 + cur_w - 1},{by + box_h - 1}",
                "-stroke", "none"]
        sp = (f - sheen_start) / sheen_len
        if 0 <= sp <= 1:
            sx = bx - 120 + sp * (box_w + 240)
            cmd += ["-fill", "rgba(255,255,255,0.45)", "-draw",
                    f"polygon {sx:.0f},{by + 2} {sx + 40:.0f},{by + 2} "
                    f"{sx + 10:.0f},{by + box_h - 2} {sx - 30:.0f},{by + box_h - 2}"]
        cmd += ["-font", FONT_SERIF, "-pointsize", str(size), "-kerning", str(kerning)]
        tx, ty = bx + pad_x, by + pad_y + int(size * 1.02)
        for i, ch in enumerate(text):
            a = (f - (box_in + i * stagger)) / char_fade
            if a <= 0 or ch == " ":
                continue
            a = min(1.0, a)
            cmd += ["-fill", f"rgba(138,120,74,{a:.3f})",
                    "-annotate", f"+{tx + offs[i]}+{ty}", ch]
        if sub:
            sa = ease_out((f - sub_start) / sub_len)
            if sa > 0:
                px = (W - pill_w) // 2
                py = by + box_h + gap + int((1 - sa) * 10)
                cmd += ["-fill", f"rgba(40,38,34,{0.62 * sa:.3f})",
                        "-draw", f"roundrectangle {px},{py} {px + pill_w},{py + pill_h} 6,6",
                        "-font", FONT_SANS_MED, "-pointsize", str(sub_size),
                        "-kerning", str(sub_kern),
                        "-fill", f"rgba(255,255,255,{sa:.3f})",
                        "-annotate", f"+{px + 18}+{py + 34}", sub_text]
        cmd += ["PNG32:" + os.path.join(outdir, f"f{f:04d}.png")]
        sh(cmd)
    return W, H, n


if __name__ == "__main__":
    import sys
    print(make_card(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "", sys.argv[3]))
