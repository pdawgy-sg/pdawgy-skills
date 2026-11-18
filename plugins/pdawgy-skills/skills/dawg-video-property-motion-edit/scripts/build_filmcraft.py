import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import project as P
import captions as CAP
import locmap
import motion
from cards import sh, text_width
from fc import FC, ticks
from motion import AMBER, BG, glow, plan_card, set_assets, take
from music import house_bed

W, H = 1080, 1920
FC_PROJECT = os.path.join(P.ROOT, f"{P.NAME}-property-motion.fcproj")
BG_BAND, GFX_BAND, TXT_BAND, CAP_BAND = (1, 3), (4, 8), (9, 15), (16, 17)
STACK_STEP = 158
LOW = 1560
CAPTION_MARGIN_BOTTOM = 0.165
BOLD_TTF = P.FONT_BOLD

SECTIONS = [
    ("hook", "20261116151818"),
    ("size", "20261116151450"),
    ("price", "20261116152344"),
    ("location", "20261116153111"),
    ("closer", "20261116153824"),
]
CUES = {
    "hook": {"best": 1.4, "core": 2.58},
    "size": {"counter": 0.5, "unit": 0.75, "flexi": 2.35, "shelter_cut": 3.05, "shelter": 3.15,
             "broll": "20261116151903", "value": 958},
    "price": {"label1": 1.1, "price1": 2.35, "label2": 5.6, "price2": 6.85, "theirs": 3.5, "ours": 2.54},
    "location": {"map_in": 1.45, "schools": 1.72, "walking": 2.5, "mrt": 3.36},
    "closer": {"facilities": 0.8, "three": 2.3, "four": 2.88, "five": 3.36, "available": 4.1,
               "interested": 5.45, "contact": 6.5, "hold": 2.2, "lift": 320},
}
NOT_TIMES = {"broll", "value", "theirs", "ours", "hold", "lift"}


def L(stem):
    return int(P.TAKES[stem] / P.SPEED * 30) / 30


def scale_cues():
    for sec in CUES.values():
        for k, v in sec.items():
            if k not in NOT_TIMES:
                sec[k] = v / P.SPEED


def baseline(top, size, trimmed=True):
    return top + size * (0.74 if trimmed else 1.06)


def pill_png(name, w, h, fill, outline=None):
    out = os.path.join(motion.A, f"{name}.png")
    cmd = ["magick", "-size", f"{w}x{h}", "xc:none", "-fill", fill]
    if outline:
        cmd += ["-stroke", outline, "-strokewidth", "3"]
    cmd += ["-draw", f"roundrectangle 1,1 {w - 2},{h - 2} {h // 2},{h // 2}", "PNG32:" + out]
    sh(cmd)
    return out


def scrim_png(name, h, top=True, strength=0.88):
    out = os.path.join(motion.A, f"{name}.png")
    a, b = (f"rgba(13,11,9,{strength})", "rgba(13,11,9,0)")
    sh(["magick", "-size", f"{W}x{h}", f"gradient:{a if top else b}-{b if top else a}", "PNG32:" + out])
    return out


def full_png(name, h_off, fade_h, lift):
    out = os.path.join(motion.A, f"{name}.png")
    sh(["magick", "-size", f"{W}x{H - fade_h - lift - 20}", "xc:none",
        "(", "-size", f"{W}x{fade_h}", f"gradient:rgba(13,11,9,0)-{BG}", ")",
        "(", "-size", f"{W}x{lift + 20}", f"xc:{BG}", ")", "-append", "PNG32:" + out])
    return out


def map_mov(stem, map_in, schools_word, mrt_word, panel=(30, 70, 1050, 820, 40)):
    dur = L(stem) - map_in
    labels = [(n, la, lo, schools_word - map_in + 0.15 * k) for k, (_, n, la, lo) in enumerate(locmap.pois("school"))]
    labels += [(n, la, lo, mrt_word - map_in + 0.15 * k) for k, (_, n, la, lo) in enumerate(locmap.pois("mrt"))]
    frames = locmap.render(os.path.join(motion.A, "map_frames"), dur, "card", P.MAP_PIN_LABEL, P.MAP_PIN_SUB,
                           labels, ring_at=0.05, pin=(540, 430), scale=0.30,
                           avoid=[(0, 0, 1080, 96), (0, 794, 1080, 1920)])
    pw, ph = panel[2] - panel[0], panel[3] - panel[1]
    shadow = glow("map_shadow", pw, ph, panel[4], color="black", opacity=0.75, blur=30)
    sw, shh = map(int, subprocess.run(["magick", "identify", "-format", "%w %h", shadow], capture_output=True,
                                      text=True, check=True).stdout.split())
    mask = os.path.join(motion.A, "map_mask.png")
    sh(["magick", "-size", f"{W}x{H}", "xc:black", "-fill", "white",
        "-draw", f"roundrectangle {panel[0]},{panel[1]} {panel[2]},{panel[3]} {panel[4]},{panel[4]}", mask])
    out = os.path.join(motion.A, "map.mov")
    sx, sy = panel[0] + (pw - sw) // 2, panel[1] + 14 + (ph - shh) // 2
    sh(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", f"color=c=black@0.0:s={W}x{H}:r=30:d={dur:.3f},format=rgba",
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", shadow,
        "-framerate", "30", "-i", frames,
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", mask,
        "-filter_complex",
        f"[0:v][1:v]overlay={sx}:{sy}:format=auto[b];[2:v]format=rgba[m0];[3:v]format=gray[mk];"
        f"[m0][mk]alphamerge[m];[b][m]overlay=0:0:format=auto,format=yuva444p10le[v]",
        "-map", "[v]", "-t", f"{dur:.3f}", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
        out])
    return out, dur


def caption_lines(stem, t_from=-1.0, t_to=1e9):
    words = CAP.load_words()[stem]
    chunks = CAP.chunk(words, clip=stem)
    out = []
    for i, c in enumerate(chunks):
        s = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else None
        e = min(nxt, c[-1]["e"] + 0.5) if nxt is not None else c[-1]["e"] + 0.5
        if not (t_from <= s < t_to):
            continue
        out.append((s, min(e, t_to), CAP.apply_fixes(" ".join(w["w"] for w in c)).rstrip(",")))
    return out


def main():
    set_assets(os.path.join(P.WORK, "filmcraft"))
    scale_cues()
    starts, t = {}, 0.0
    for key, stem in SECTIONS:
        starts[key] = t
        t += L(stem)
    hold = CUES["closer"]["hold"]
    total = t + hold

    print("rendering overlay assets ...")
    cs = CUES["size"]
    cl = CUES["location"]
    map_clip, map_dur = map_mov(SECTIONS[3][1], cl["map_in"], cl["schools"], cl["mrt"])
    music = house_bed(os.path.join(motion.A, "music.wav"), total, 118)
    closer_stem = SECTIONS[4][1]
    hold_png = os.path.join(motion.A, "closer_hold.png")
    sh(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-sseof", "-0.05",
        "-i", take(closer_stem), "-frames:v", "1", hold_png])
    lift = CUES["closer"]["lift"]
    assets = {
        "scrim_top": scrim_png("scrim_top", 760, strength=0.88),
        "scrim_top_bright": scrim_png("scrim_top_bright", 820, strength=0.92),
        "scrim_bottom": scrim_png("scrim_bottom", 770, top=False, strength=0.9),
        "closer_fade": full_png("closer_fade", 0, 380, lift),
        "rule": pill_png("rule", 8, 140, AMBER),
        "bar_theirs": pill_png("bar_theirs", 760, 78, "#8A8178"),
        "bar_ours": pill_png("bar_ours", 760, 78, AMBER),
        "save_pill": pill_png("save_pill", 210, 92, AMBER),
        "cta_pill": pill_png("cta_pill", text_width(P.CTA_TEXT, BOLD_TTF, 38, 0) + 88, 92, AMBER),
        "glass_edge": os.path.join(motion.A, "glass_edge.png"),
        "dim": os.path.join(motion.A, "dim.png"),
    }
    sh(["magick", "-size", "1000x490", "xc:none", "-fill", "rgba(20,16,12,0.38)", "-stroke", "rgba(255,240,220,0.22)",
        "-strokewidth", "2", "-draw", "roundrectangle 1,1 998,488 34,34", "PNG32:" + assets["glass_edge"]])
    sh(["magick", "-size", f"{W}x{H}", "xc:rgba(13,11,9,0.68)", "PNG32:" + assets["dim"]])
    layout = [(-6, 22, 1395), (0, 378, 1380), (6, 730, 1395)]
    plans = []
    for i, ((src, crop, label, sub), (ang, x, y)) in enumerate(zip(P.FLOOR_PLANS, layout)):
        plans.append((plan_card(f"plan{i}", os.path.join(P.RAW, src), crop, label, sub, ang, scale=0.62), x, y))

    print("building FilmCraft project ...")
    if os.path.exists(FC_PROJECT):
        os.replace(FC_PROJECT, FC_PROJECT + ".bak")
    fc = FC(FC_PROJECT, os.path.join(P.WORK, "filmcraft-actions.jsonl"))
    fc.new_sequence(f"{P.PROJECT_NAME if not P.HIDE_PROJECT_NAME else 'New launch'} | Property motion reel",
                    30, CAP_BAND[1] + 1, 2)
    media_paths = [take(s) for _, s in SECTIONS] + [take(cs["broll"]), hold_png, map_clip, music] + \
        list(assets.values()) + [p for p, _, _ in plans]
    m = fc.import_media(media_paths)
    names = {0: "Tour (agent takes, 3-bedder)", 1: "Backgrounds: scrims, dim, glass", 4: "Graphics: map, plans, bars, rules",
             9: "Text: titles, prices, contact (editable)", 16: "Captions (editable text, amber keywords)"}
    for idx, name in names.items():
        fc.c("timeline.setTrack", track=f"V{idx + 1}", name=name)
    fc.c("timeline.setTrack", track="A2", name="Music bed (ducked)")

    voice = []
    for key, stem in SECTIONS:
        t0, dur = starts[key], L(stem)
        clip = fc.place(m[take(stem)], t0, t0 + dur, track=0, audio=True)
        voice.append(clip)
        if key == "closer":
            fc.c("effects.setParam", clip=clip, effect="motion", param="position", value=[W / 2, H / 2 - lift])
        elif key != "price":
            fc.push_in(clip, t0, t0 + dur, 6)
        fc.c("markers.add", target="program", time=ticks(t0), name=key.title(),
             comment=" ".join(l[2] for l in caption_lines(stem)))
    hold_clip = fc.place(m[hold_png], t, total, track=0)
    fc.c("effects.setParam", clip=hold_clip, effect="motion", param="position", value=[W / 2, H / 2 - lift])

    def txt(runs, top, size, t0, t1, trimmed=True, style="Bold", **kw):
        return fc.text(runs, W / 2, baseline(top, size, trimmed), size, t0, t1, TXT_BAND, style=style, **kw)

    def stack(pairs, x, y0, t1, t_out=None):
        for i, (kicker, head, t) in enumerate(pairs):
            y = y0 + i * STACK_STEP
            fc.image(m[assets["rule"]], assets["rule"], x - 24, y - 6, t, t1, GFX_BAND, d=0.35, rise=20, t_out=t_out)
            fc.text([(kicker, AMBER)], x, y + 30, 32, t, t1, TXT_BAND, style="SemiBold", font="Inter", align="left",
                    rise=20, t_out=t_out, props=dict(tracking=180, shadow=True, shadow_blur=10, shadow_distance=2,
                                                     shadow_opacity=60))
            fc.text([(head, "#FFFFFF")], x, y + 30 + 92, 88, t + 0.08, t1, TXT_BAND, font="Inter", align="left",
                    rise=20, t_out=t_out, props=dict(shadow=True, shadow_blur=12, shadow_distance=2,
                                                     shadow_opacity=55))

    def caption(line, t0, t1, y):
        runs, pos, low_line = [], 0, line.lower()
        marks = sorted({(low_line.find(k.lower()), len(k)) for k in P.KEYWORDS if k.lower() in low_line and
                        low_line.find(k.lower()) >= 0})
        for start, length in marks:
            if start < pos:
                continue
            if start > pos:
                runs.append((line[pos:start], "#FFFFFF"))
            runs.append((line[start:start + length], AMBER))
            pos = start + length
        if pos < len(line):
            runs.append((line[pos:], "#FFFFFF"))
        fc.text(runs, W / 2, y + 14, 40, t0, t1, CAP_BAND, rise=0, d=0.12,
                props=dict(background=True, background_color="#120E0A", background_opacity=82,
                           background_radius=14, background_size=14))

    s = starts["hook"]
    e = starts["size"]
    fc.image(m[assets["scrim_top"]], assets["scrim_top"], 0, 0, s, e, BG_BAND, d=0.01, rise=0)
    ch = CUES["hook"]
    stack([("THE BEST", "Value buy", s + ch["best"]), ("RIGHT NOW IN THE", "Core Central Region", s + ch["core"])],
          72, 150, e)

    s, e = starts["size"], starts["price"]
    shelter = fc.place(m[take(cs["broll"])], s + cs["shelter_cut"], e, track=0)
    fc.push_in(shelter, s + cs["shelter_cut"], e, 6)
    fc.image(m[assets["scrim_top_bright"]], assets["scrim_top_bright"], 0, 0, s, e, BG_BAND, d=0.01, rise=0)
    stack([("3-BEDDER", f"{cs['value']} sq ft", s + cs["counter"]), ("WITH A", "Flexi room", s + cs["flexi"]),
           ("RIGHT AT THE BACK", "Bomb shelter", s + cs["shelter"])], 72, 150, e)

    cp = CUES["price"]
    s, e = starts["price"], starts["location"]
    glass = fc.place(m[take(SECTIONS[2][1])], s, e, track=1)
    fc.c("effects.apply", clips=[glass], effect="gaussian_blur")
    fc.c("effects.apply", clips=[glass], effect="brightness_contrast")
    fc.c("effects.setParam", clip=glass, effect="gaussian_blur", param="blurriness", value=40)
    fc.c("effects.setParam", clip=glass, effect="brightness_contrast", param="brightness", value=-20)
    fc.c("masks.add", clip=glass, effect="opacity", shape="rectangle", center=[540, 385], size=[1000, 490],
         cornerRadius=34)
    fc.kf(glass, "opacity", "opacity", s + 0.15, 0)
    fc.kf(glass, "opacity", "opacity", s + 0.4, 100)
    fc.image(m[assets["glass_edge"]], assets["glass_edge"], 40, 140, s + 0.15, e, BG_BAND, d=0.3, rise=0)
    txt([("3-bedder", AMBER), (" prices", "#FFFFFF")], 170, 68, s + 0.3, e)
    full, here = 760, int(760 * cp["ours"] / cp["theirs"])
    fc.text([(P.COMPARABLE, "#D8D0C4")], 100, baseline(275, 36, False), 36, s + cp["label1"], e, TXT_BAND,
            style="Medium", align="left", rise=12)
    for key2, png, width, y, t_bar in [("theirs", assets["bar_theirs"], full, 325, cp["price1"]),
                                       ("ours", assets["bar_ours"], here, 485, cp["price2"])]:
        bar = fc.place(m[png], s + t_bar, e, band=GFX_BAND)
        fc.c("effects.setParam", clip=bar, effect="motion", param="uniform_scale", value=False)
        fc.c("effects.setParam", clip=bar, effect="motion", param="anchor", value=[0, 39])
        fc.c("effects.setParam", clip=bar, effect="motion", param="position", value=[100, y + 39])
        fc.kf(bar, "motion", "scale_width", s + t_bar, 0, ease="easeOut")
        fc.kf(bar, "motion", "scale_width", s + t_bar + 0.7, 100 * width / full)
    fc.text([(f"${cp['theirs']:g}M", "#FFFFFF")], 100 + full - 18, baseline(335, 48, False), 48,
            s + cp["price1"] + 0.5, e, TXT_BAND, align="right", rise=0)
    fc.text([("Here, in the CCR", "#D8D0C4")], 100, baseline(435, 36, False), 36, s + cp["label2"], e, TXT_BAND,
            style="Medium", align="left", rise=12)
    fc.text([(f"${cp['ours']:g}M", BG)], 100 + here - 18, baseline(495, 48, False), 48, s + cp["price2"] + 0.5, e,
            TXT_BAND, align="right", rise=0)
    saving = round((1 - cp["ours"] / cp["theirs"]) * 100)
    fc.image(m[assets["save_pill"]], assets["save_pill"], 100 + here + 24, 478, s + cp["price2"] + 0.75, e,
             GFX_BAND, d=0.45, rise=0, dx=-30)
    fc.text([(f"~{saving}% less", BG)], 100 + here + 24 + 105, 478 + 60, 34, s + cp["price2"] + 0.75, e, TXT_BAND,
            rise=0)

    s, e = starts["location"], starts["closer"]
    fc.image(m[assets["dim"]], assets["dim"], 0, 0, s + cl["map_in"], e, BG_BAND, d=0.4, rise=0)
    fc.image(m[assets["scrim_bottom"]], assets["scrim_bottom"], 0, 1150, s, e, BG_BAND, d=0.01, rise=0)
    fc.image(m[map_clip], map_clip, 0, 0, s + cl["map_in"], e, GFX_BAND, d=0.35, rise=0)
    fc.text([("© OpenStreetMap contributors", "#D8D0C4")], 60, 830 + 22, 20, s + cl["map_in"], e, TXT_BAND,
            style="Medium", align="left", rise=0)
    stack([("NEAR", "Top schools", s + cl["schools"] - 0.07), ("WALKING DISTANCE TO", "The MRT", s + cl["walking"])],
          72, 1250, e)

    cc = CUES["closer"]
    s = starts["closer"]
    slot = 1440
    fc.image(m[assets["closer_fade"]], assets["closer_fade"], 0, 0, s, total, BG_BAND, d=0.01, rise=0)
    stack([("COMES WITH", "Full-fledged facilities", s + cc["facilities"])], 72, 1420, total,
          t_out=s + cc["three"] - 0.15)
    for (png, x, y), key2 in zip(plans, ["three", "four", "five"]):
        fc.image(m[png], png, x, y, s + cc[key2], total, GFX_BAND, d=0.45, rise=140,
                 t_out=s + cc["interested"] - 0.25)
    txt([("still available", "#FFFFFF")], 1755, 38, s + cc["available"], total, trimmed=False,
        t_out=s + cc["interested"] - 0.25, rise=15)
    fc.image(m[assets["cta_pill"]], assets["cta_pill"], 0, slot - 10, s + cc["interested"], total, GFX_BAND,
             d=0.45, rise=25, center_x=True)
    fc.text([(P.CTA_TEXT, BG)], W / 2, slot - 10 + 60, 38, s + cc["interested"], total, TXT_BAND, rise=25)
    txt([(f"{P.AGENT_NAME}  ·  {P.AGENT_PHONE}", "#FFFFFF")], slot + 108, 46, s + cc["contact"], total,
        trimmed=False, rise=20)
    txt([(f"CEA Reg No. {P.AGENT_CEA}  ·  {P.AGENCY} ({P.AGENCY_LICENCE})", "#8E867B")], slot + 182, 25,
        s + cc["contact"] + 0.25, total, trimmed=False, style="Medium", rise=10)

    print("captions, audio ...")
    low = fc.c("captions.newTrack", format="Subtitle", name="Captions")["track"]
    top = fc.c("captions.newTrack", format="Subtitle", name="Captions (closer, top)")["track"]
    for tr, anchor, margin in [(low, "bottom", CAPTION_MARGIN_BOTTOM), (top, "top", 0.15)]:
        fc.c("captions.setStyle", track=tr, font="Noto Sans", fontStyle="Bold", size=26, color="#FFFFFF",
             background=True, backgroundColor="#120E0AD1", align="center", anchor=anchor, margin=margin)
        fc.c("captions.setTrack", track=tr, enabled=False)
    cap_y = {"hook": LOW, "size": LOW, "price": LOW, "location": 1690, "closer": 330}
    for key, stem in SECTIONS:
        s0 = starts[key]
        if key == "closer":
            hide = (cc["three"] - 0.05, cc["interested"] - 0.2)
            lines = [l for l in caption_lines(stem, t_to=L(stem)) if not hide[0] <= l[0] < hide[1]]
            lines = [(a, min(b, hide[0]) if a < hide[0] else b, txt_) for a, b, txt_ in lines]
            track = top
        else:
            lines, track = caption_lines(stem, t_to=L(stem)), low
        for a, b, line in lines:
            f0, f1 = round((s0 + a) * 30), round((s0 + b) * 30)
            if f1 > f0:
                fc.c("captions.add", track=track, text=line, seconds=f0 / 30, durationSeconds=(f1 - f0) / 30)
                caption(line, f0 / 30, f1 / 30, cap_y[key])

    mus = fc.c("timeline.place", item=m[music], track="A2", seconds=0, duration={"seconds": round(total, 4)})["clips"][0]
    fc.c("essentialSound.setType", clips=voice, type="dialogue")
    fc.c("essentialSound.setType", clips=[mus], type="music")
    fc.c("essentialSound.set", clips=[mus], key="ducking.reduceDb", value=-14)
    fc.c("essentialSound.generateDucking", clips=[mus])

    print("exporting ...")
    fc.c("file.exportMedia", path=os.path.abspath(P.OUT), format="h264", crf=20, burnCaptions=False,
         loudnessLufs=-14, wait=True)
    if not os.path.exists(P.OUT) or os.path.getmtime(P.OUT) < os.path.getmtime(FC_PROJECT) - 600:
        raise RuntimeError("export did not produce " + P.OUT)
    print("wrote", FC_PROJECT, "and", P.OUT)


if __name__ == "__main__":
    main()
