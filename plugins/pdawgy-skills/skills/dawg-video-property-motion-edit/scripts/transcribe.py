import glob
import json
import os
import sys
import wave

import numpy as np

from faster_whisper import WhisperModel

MODEL = os.environ.get("WHISPER_MODEL", "large-v3")
import project as P
PROMPT = os.environ.get("WHISPER_PROMPT", P.WHISPER_PROMPT)
model = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=16)
out = {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.wav"))):
    with wave.open(f) as wf:
        audio = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = model.transcribe(audio, word_timestamps=True, language="en", beam_size=5, initial_prompt=PROMPT,
                               vad_filter=False)
    words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)}
             for s in segs for w in s.words]
    name = os.path.basename(f)[:-4]
    out[name] = words
    print(name, " ".join(f"{x['w']}[{x['s']}]" for x in words), flush=True)
with open(sys.argv[2], "w") as fh:
    json.dump(out, fh, indent=1)
