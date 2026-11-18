import subprocess


def music_bed(out, dur, bpm=96, kick=True):
    b = 60.0 / bpm
    bar = 4 * b
    ph = f"mod(t,{b})"
    k = (f"sin(2*PI*(40+90*exp(-{ph}*26))*{ph})*exp(-{ph}*8)" if kick else "0")
    shaker = f"(random(0)*2-1)*exp(-mod(t+{b / 2},{b})*55)*0.10"
    idx = f"mod(floor(t/{bar}),4)"
    root = f"if(eq({idx},0),220,if(eq({idx},1),174.61,if(eq({idx},2),261.63,196)))"
    third = f"if(eq({idx},0),261.63,if(eq({idx},1),220,if(eq({idx},2),329.63,246.94)))"
    swell = f"(0.6+0.4*sin(2*PI*mod(t,{bar})/{bar}-PI/2))"
    pad = (f"({swell})*(sin(2*PI*{root}*t)+0.7*sin(2*PI*{third}*t)+0.5*sin(2*PI*1.5*{root}*t)"
           f"+0.35*sin(2*PI*{root}/2*t))*0.05")
    expr = f"0.5*{k}+{shaker}+{pad}"
    subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", f"aevalsrc=exprs='{expr}':s=48000:d={dur:.3f}",
                    "-af", f"lowpass=f=7000,aecho=0.6:0.4:{int(b * 1000 * 0.75)}:0.18,"
                           f"aformat=channel_layouts=stereo,afade=t=in:d=0.4,"
                           f"afade=t=out:st={dur - 1.5:.3f}:d=1.5,loudnorm=I=-18:TP=-2",
                    "-ar", "48000", out], check=True)
    return out


def house_bed(out, dur, bpm=118):
    b = 60.0 / bpm
    bar = 4 * b
    ph = f"mod(t,{b})"
    kick = f"sin(2*PI*(45+120*exp(-{ph}*32))*{ph})*exp(-{ph}*7)*0.9"
    hat = f"(random(0)*2-1)*exp(-mod(t+{b / 2},{b})*38)*0.07"
    clap_ph = f"mod(t+{b},{2 * b})"
    clap = f"(random(1)*2-1)*exp(-{clap_ph}*30)*0.10"
    idx = f"mod(floor(t/{bar}),4)"
    root = f"if(eq({idx},0),110,if(eq({idx},1),87.31,if(eq({idx},2),130.81,98)))"
    third = f"if(eq({idx},0),261.63,if(eq({idx},1),220,if(eq({idx},2),329.63,246.94)))"
    bass_ph = f"mod(t+{b / 2},{b})"
    bass = f"(sin(2*PI*{root}*t)+0.3*sin(4*PI*{root}*t))*exp(-{bass_ph}*6)*0.42"
    stab_ph = f"mod(t+{b / 2},{2 * b})"
    stab = (f"(sin(2*PI*2*{root}*t)+0.8*sin(2*PI*{third}*t)+0.6*sin(2*PI*3*{root}*t)"
            f"+0.4*sin(2*PI*4*{root}*t))*exp(-{stab_ph}*3.2)*0.12")
    pad = f"(sin(2*PI*2*{root}*t)+0.6*sin(2*PI*{third}*t))*0.05"
    expr = f"{kick}+{hat}+{clap}+{bass}+{stab}+{pad}"
    subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", f"aevalsrc=exprs='{expr}':s=48000:d={dur:.3f}",
                    "-af", f"highpass=f=30,lowpass=f=11000,"
                           f"aecho=0.7:0.35:{int(b * 750)}:0.12,"
                           f"aformat=channel_layouts=stereo,extrastereo=m=1.6,"
                           f"acompressor=threshold=-14dB:ratio=3:attack=5:release=120,"
                           f"afade=t=in:d=0.3,afade=t=out:st={dur - 1.8:.3f}:d=1.8,"
                           f"loudnorm=I=-16:TP=-1.5",
                    "-ar", "48000", out], check=True)
    return out
