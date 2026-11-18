---
name: dawg-video-property-motion-edit
description: Edit raw property-agent footage into a vertical 9:16 "property motion" reel — the agent's walkthrough plays full-screen while dark/amber infographics (stat counters, feature ticks, price-comparison bars, a location map card, floor-plan cards, CTA and CEA-compliant agent details) land on the exact words he says, built as an editable FilmCraft project (native text, captions, keyframes, ducked music) plus its export. Use whenever someone wants a real-estate / showflat / condo / new-launch reel, Instagram/TikTok property video, agent tour edit, or "make it like the Amberwood edit" from raw clips, floor plans and reference videos — even if they only say "edit these property videos" or "make a reel to sell this unit".
---

# Dawg Video — Property Motion Edit

Turn an agent's raw showflat takes into a 30–40 s vertical reel where **the tour stays full-screen**
and every graphic is triggered by a word he says. The edit is built headlessly in **FilmCraft**
(`filmcraft-cli`) so the deliverable is an editable `.fcproj` — cuts, headlines, labels, prices,
contact details and captions are native timeline items the user can retype, retime or move by
hand — plus its H.264 export. The style was refined through several rounds of
real client feedback; `references/style-guide.md` records those rules and why they exist. Read it
before laying out a reel.

Work in the user's project folder. Expected layout (create `edits/<name>/` if missing):

```
<project>/raw/<name>/         raw clips, floor-plan images, ID/contact info  (never modify)
<project>/reference/          example reels the client likes (optional)
<project>/edits/<name>/tools/ copy of this skill's scripts/  ← adapt here, per project
<project>/edits/<name>/work/  proxies, words.json, map data, rendered overlay assets (generated)
<project>/edits/<name>/<name>-property-motion.fcproj + .mp4   deliverables
```

Copy the scripts in first: `cp -r <skill>/scripts <project>/edits/<name>/tools`. Every script
reads `tools/project.py` (the only per-project config, pre-filled with the Amberwood example).

## Workflow

### 1. Inventory and understand
- Probe every clip (`ffprobe`): rotation, fps, duration, audio, and **HDR** (`color_transfer`
  `arib-std-b67`/`smpte2084` → must be tone-mapped). Build timestamped contact sheets
  (`fps=2,scale=200:-2,drawtext=…,tile=`) and look at them.
- If reference reels exist, study cut rhythm, card style, caption style, map/end-card treatment.
- Ask the user what you can't see: **which clips show which unit** (e.g. agent in the 3-bed,
  b-roll of the 4-bed), the project's name policy, agent name/phone/CEA no./agency + licence,
  and any comparables he mentions. Never present one unit's footage as another's.

### 2. Proxies
`python3 tools/make_proxies.py` → 1080×1920/30 fps proxies in `work/proxy/`, dead air trimmed by
silencedetect, HDR tone-mapped (zscale + mobius), loudness-normalised. Paste its printed `TAKES`
lengths (common video/audio length — the two streams differ by frames and drift over a long edit)
into `project.py`.

### 3. Transcribe — the speech drives everything
```
for f in work/proxy/*.mp4; do ffmpeg -nostdin -i $f -vn -ac 1 -ar 16000 work/audio/$(basename $f .mp4).wav; done
uv run --python 3.12 --with faster-whisper python tools/transcribe.py work/audio work/words.json
```
This installs a package and downloads a model: get the user's OK first. Set `WHISPER_PROMPT` in
`project.py` to domain vocabulary (it fixes "belly bite" → "value buy"). Then
`python3 tools/captions.py` prints the caption lines with timestamps. **Show the user the
transcript** — local names and accents get misheard ("Thompson Resort", "As a surprise" vs
"At such a price"). Fix with `CAPTION_FIXES` (display text) or `WORD_FIXES` (per token, keeps
timing); set phrase breaks in `CHUNKS`; drop silent b-roll via `SKIP_CLIPS`.

### 4. Plan the reel from what he says
Write a table: take → line → which graphic → which word triggers it. Use the section patterns in
`scripts/build_reel.py` (hook, size+features with b-roll cut, price bars, location map, closer with
floor plans + CTA). Only put claims on screen that he says or that come from the client's
documents (floor plans, ID card). Order takes for the strongest hook (the client moved "best value
buy" before "958 sqft"). Confirm the plan with the user before rendering.

### 5. Location map
`python3 tools/fetch_map_data.py` (Nominatim, polite, ~70 requests at 1 req/s) writes
`work/map/nominatim.json` and prints distance-ranked MRT/schools/parks. Check the site pin
against the floor plans' key plan, then curate real, nearby POIs into `project.POIS`. If a map
service refuses, don't hop mirrors or spoof user agents — tell the user. Keep the
"© OpenStreetMap contributors" credit on screen.

### 6. Build in FilmCraft
Adapt `tools/build_filmcraft.py`: `SECTIONS` (take order), `CUES` (word times from `words.json`)
and the copy in each section, then `python3 tools/build_filmcraft.py` (≈3–4 min; it issues a few
hundred `filmcraft-cli exec` commands, logged to `work/filmcraft-actions.jsonl`). It builds:

| Track band | Contents |
| --- | --- |
| V1 | the takes (voice linked on A1), b-roll cuts, the lifted closer and its hold frame, push-in keyframes |
| V2–V4 | scrims, footage dim, frosted panel (blurred, masked copy of the take), closer fade |
| V5–V9 | stills and alpha ProRes clips: ticks, bars (`scale_width` keyframes), plan cards, pills, map card, counter |
| V10–V15 | native text (two-colour headlines are adjacent layers) |
| C1/C2 | caption tracks (bottom / top), burned in on export |
| A2 | music bed, typed as music, ducking generated against the dialogue |

Only the bespoke animations (map card, number counter) are pre-rendered; everything else stays
editable. Section markers carry the spoken line. Export: `file.exportMedia` (H.264, CRF 20,
captions burned in, −14 LUFS). `tools/fc.py` wraps the CLI (`place`, `kf`, `animate_in`, `image`,
`text`, `push_in`, a per-band free-track allocator). Inspect with
`filmcraft-cli --project <p> inspect sequence`; preview a frame with `render --seconds S --out f.png`
(captions only show in exports). If `filmcraft-cli` isn't installed, `tools/build_reel.py` renders
the same reel with ffmpeg alone (karaoke captions, no editable project).

### 7. Verify before showing anything
- Contact sheet of the whole reel + frame grabs **at each cue time**; read them.
- Video and audio durations match (`ffprobe -show_entries stream=duration`).
- Graphics never cover the agent's face; captions don't repeat the graphic right next to them.
- File < 30 MB for phone/web sharing (segments use CRF 20; raise it if needed).
- If a render hangs at ~0 % CPU, it's an ffmpeg framesync deadlock — see `references/pitfalls.md`.

### 8. Music and delivery
The FilmCraft build lays a synthesized, royalty-free 118 BPM deep-house bed (`music.house_bed`) on
A2 with generated ducking; mute A2 and re-export for a voice-only cut (ffmpeg path:
`tools/add_music.py`). Deliver the `.fcproj` and both exports. Always offer the voice-only version: real trending tracks must be added in the Instagram/TikTok editor
(licensed in-app; baked-in copyrighted audio gets muted or removed). You can't hear the bed —
say so and offer to rebalance.

## Iterating with the client
Expect rounds of feedback. Small tweaks (wording, a few frames of timing, a position) can be made
directly in the `.fcproj` with `filmcraft-cli exec` or by the user in FilmCraft; structural changes
go into the builder and a rebuild. Re-check frames at the touched cues and resend the exports.
Feedback this style has already absorbed is in `references/style-guide.md` — apply it up front.

## Resources
- `scripts/project.py` — per-project config (agent/CEA details, takes, caption fixes, map, plans)
- `scripts/build_filmcraft.py` — the approved Amberwood reel as an editable FilmCraft project (main path)
- `scripts/fc.py` — headless FilmCraft driver: commands, keyframes, animated stills/text, track allocation
- `scripts/build_reel.py` — the same reel rendered with ffmpeg only (fallback without FilmCraft)
- `scripts/motion.py` — `Seg` builder + overlay makers (full-bleed, scrim, glass, cut_to, counter, bar, seq, captions)
- `scripts/locmap.py`, `scripts/fetch_map_data.py` — map rendering and data
- `scripts/make_proxies.py`, `scripts/transcribe.py`, `scripts/captions.py` — media prep and captions
- `scripts/music.py`, `scripts/add_music.py` — music bed and ducking
- `references/style-guide.md` — layout zones, palette, timing and the client-feedback rules
- `references/pitfalls.md` — ffmpeg 9 / ImageMagick / data gotchas and their fixes
- `references/amberwood-example.md` — the worked example: footage, transcript, section map

Requires FilmCraft ≥ 0.17 (`filmcraft-cli`), ffmpeg ≥ 9 (uses `-/filter_complex`), ImageMagick 7
with Pango, Noto fonts, Python 3; `uv` only for transcription.
