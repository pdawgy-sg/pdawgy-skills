import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import project as P
import locmap
from motion import (AMBER, BG, BOLD, Seg, background, check_row, cta_pill, glow, headline,
                    plan_card, set_assets, sh, small_text, take)
import motion

LOW = 1560


def hook(stem):
    s = Seg("s1", take(stem), P.TAKES[stem])
    s.full(push=0.06)
    s.scrim(0, 760, top=True, strength=0.88)
    s.layer(headline("s1_h", [("Best ", "white"), ("value buy.", AMBER)], size=86), 1.15, "(W-overlay_w)/2", 170)
    s.layer(headline("s1_ccr", [("CCR", AMBER)], size=200), 2.6, "(W-overlay_w)/2", 290, rise=50)
    s.layer(small_text("s1_ccr_sub", "Core Central Region", 40, "white"), 2.85, "(W-overlay_w)/2", 520, rise=20)
    s.captions(stem, LOW)
    return s.render(os.path.join(motion.A, "s1.mp4"))


def size_and_features(stem, broll_stem, broll_at):
    s = Seg("s2", take(stem), P.TAKES[stem])
    s.full(push=0.05)
    s.cut_to(take(broll_stem), broll_at)
    s.scrim(0, 820, top=True, strength=0.92)
    s.counter(958, 0.5, 0.7, 150, size=160)
    s.layer(small_text("s2_unit", "square feet", 42, "white"), 0.75, "(W-overlay_w)/2", 350, rise=20)
    s.layer(check_row("s2_flexi", "Flexi room", 470), 2.35, 50, 440, rise=0, dx=50, d=0.4)
    s.layer(check_row("s2_shelter", "Bomb shelter", 470), 3.15, 50, 556, rise=0, dx=50, d=0.4)
    s.captions(stem, LOW)
    return s.render(os.path.join(motion.A, "s2.mp4"))


def price_compare(stem, theirs, ours, cues):
    s = Seg("s3", take(stem), P.TAKES[stem])
    s.full(push=0.05)
    s.glass(40, 140, 1000, 490, 34, t_in=0.15)
    s.layer(headline("s3_h", [("3-bedder", AMBER), (" prices", "white")], size=68), 0.3, "(W-overlay_w)/2", 170)
    full = 760
    here = int(full * ours / theirs)
    s.layer(small_text("s3_l1", P.COMPARABLE, 36, "#D8D0C4"), cues["label1"], 100, 275, rise=12)
    s.bar(100, 325, full, 78, "0x8A8178", cues["price1"])
    s.layer(small_text("s3_v1", f"${theirs:g}M", 48, "white", BOLD), cues["price1"] + 0.5, 100 + full - 165, 335,
            rise=0)
    s.layer(small_text("s3_l2", "Here, in the CCR", 36, "#D8D0C4"), cues["label2"], 100, 435, rise=12)
    s.bar(100, 485, here, 78, AMBER.replace("#", "0x"), cues["price2"])
    s.layer(small_text("s3_v2", f"${ours:g}M", 48, BG, BOLD), cues["price2"] + 0.5, 100 + here - 190, 495, rise=0)
    saving = round((1 - ours / theirs) * 100)
    s.layer(cta_pill("s3_save", f"~{saving}% less"), cues["price2"] + 0.75, 100 + here + 24, 478, rise=0, dx=-30)
    s.captions(stem, LOW)
    return s.render(os.path.join(motion.A, "s3.mp4"))


def location(stem, map_in, schools_word, mrt_word):
    s = Seg("s4", take(stem), P.TAKES[stem])
    s.full(push=0.05)
    s.scrim(0, 1920, top=True, strength=0.68, t_in=map_in)
    s.scrim(1150, 770, top=False, strength=0.9)
    panel = (30, 70, 1050, 820, 40)
    pw, ph = panel[2] - panel[0], panel[3] - panel[1]
    shadow = glow("s4_shadow", pw, ph, panel[4], color="black", opacity=0.75, blur=30)
    s.layer(shadow, map_in, f"{panel[0]}+({pw}-overlay_w)/2", f"{panel[1] + 14}+({ph}-overlay_h)/2", rise=0, d=0.3)
    card_mask = os.path.join(motion.A, "s4_cardmask.png")
    sh(["magick", "-size", "1080x1920", "xc:black", "-fill", "white",
        "-draw", f"roundrectangle {panel[0]},{panel[1]} {panel[2]},{panel[3]} {panel[4]},{panel[4]}", card_mask])
    labels = [(n, la, lo, schools_word - map_in + 0.15 * k) for k, (_, n, la, lo) in enumerate(locmap.pois("school"))]
    labels += [(n, la, lo, mrt_word - map_in + 0.15 * k) for k, (_, n, la, lo) in enumerate(locmap.pois("mrt"))]
    frames = locmap.render(os.path.join(motion.A, "s4_card"), P.TAKES[stem] - map_in, "card", P.MAP_PIN_LABEL,
                           P.MAP_PIN_SUB, labels, ring_at=0.05, pin=(540, 430), scale=0.30,
                           avoid=[(0, 0, 1080, 96), (0, 794, 1080, 1920)])
    s.seq(frames, map_in, push=0.0, mask=card_mask)
    s.layer(small_text("s4_osm", "© OpenStreetMap contributors", 20, "#D8D0C4"), map_in, 60, 830, rise=0)
    s.layer(headline("s4_h1", [("Near ", "white"), ("top schools.", AMBER)], size=74), schools_word - 0.07,
            "(W-overlay_w)/2", 1330)
    s.layer(headline("s4_h2", [("Walk to the ", "white"), ("MRT.", AMBER)], size=74), mrt_word - 0.86,
            "(W-overlay_w)/2", 1430)
    s.captions(stem, 1680)
    return s.render(os.path.join(motion.A, "s4.mp4"))


def closer(stem, cues, hold=2.2, lift=320):
    s = Seg("s5", take(stem), P.TAKES[stem], audio_pad=hold)
    s.g.append(f"[1:v]tpad=stop_mode=clone:stop_duration={hold},crop=1080:{1920 - lift}:0:{lift},"
               f"setsar=1,format=rgba[v5]")
    s.over("v5", "0", "0")
    fade = os.path.join(motion.A, "s5_fade.png")
    sh(["magick", "-size", "1080x380", f"gradient:rgba(13,11,9,0)-{BG}",
        "(", "-size", f"1080x{lift + 20}", f"xc:{BG}", ")", "-append", "PNG32:" + fade])
    s.over(s.img(fade), "0", str(1920 - lift - 380))
    slot = 1440
    s.layer(headline("s5_fac", [("Full-fledged ", "white"), ("facilities.", AMBER)], size=64),
            cues["facilities"], "(W-overlay_w)/2", slot, rise=25, t_out=cues["three"] - 0.15)
    layout = [(-6, 22, 1395), (0, 378, 1380), (6, 730, 1395)]
    for i, ((src, crop, label, sub), (ang, x, y), t) in enumerate(
            zip(P.FLOOR_PLANS, layout, [cues["three"], cues["four"], cues["five"]])):
        pc = plan_card(f"s5_plan{i}", os.path.join(P.RAW, src), crop, label, sub, ang, scale=0.62)
        s.layer(pc, t, x, y, rise=140, d=0.45, t_out=cues["interested"] - 0.25)
    s.layer(small_text("s5_avail", "still available", 38, "white", BOLD), cues["available"], "(W-overlay_w)/2",
            1755, rise=15, t_out=cues["interested"] - 0.25)
    s.layer(cta_pill("s5_cta", P.CTA_TEXT), cues["interested"], "(W-overlay_w)/2", slot - 10, rise=25)
    s.layer(small_text("s5_agent", f"{P.AGENT_NAME}  ·  {P.AGENT_PHONE}", 46, "white", BOLD), cues["contact"],
            "(W-overlay_w)/2", slot + 108, rise=20)
    s.layer(small_text("s5_cea", f"CEA Reg No. {P.AGENT_CEA}  ·  {P.AGENCY} ({P.AGENCY_LICENCE})", 25, "#8E867B"),
            cues["contact"] + 0.25, "(W-overlay_w)/2", slot + 182, rise=10)
    s.captions(stem, 330, hide=[(cues["three"] - 0.05, cues["interested"] - 0.2)])
    return s.render(os.path.join(motion.A, "s5.mp4"))


def main():
    set_assets(os.path.join(P.WORK, "reel"))
    background()
    segs = [
        hook("20261116151818"),
        size_and_features("20261116151450", "20261116151903", 3.05),
        price_compare("20261116152344", 3.5, 2.54, {"label1": 1.1, "price1": 2.35, "label2": 5.6, "price2": 6.85}),
        location("20261116153111", map_in=1.45, schools_word=1.72, mrt_word=3.36),
        closer("20261116153824", {"facilities": 0.8, "three": 2.3, "four": 2.88, "five": 3.36,
                                  "available": 4.1, "interested": 5.45, "contact": 6.5}),
    ]
    lst = os.path.join(motion.A, "concat.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in segs)
    subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat",
                    "-safe", "0", "-i", lst, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", P.OUT], check=True)
    print("wrote", P.OUT)


if __name__ == "__main__":
    main()
