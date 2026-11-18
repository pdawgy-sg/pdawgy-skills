# Pitfalls and fixes

## ffmpeg (9.x)
- `-filter_complex_script` is gone → write the graph to a file and pass `-/filter_complex <file>`.
- Inside shell `while read` loops ffmpeg eats stdin → always `-nostdin`.
- **Deadlock (render sits at ~0 % CPU forever):** an overlay input whose first frame starts late
  (`setpts=PTS+T/TB`) can stall framesync when many looped image inputs are buffered. Pad instead:
  `tpad=start_duration=T:start_mode=clone` (video) or `start_mode=add:color=black@0` (alpha
  sequences) and fade in at `st=T`. `Seg.video/cut_to/seq` already do this. Run builds under
  `timeout`. When killing a hung ffmpeg, match the process name (`pgrep -x ffmpeg`), not a pattern
  that also matches your own shell command.
- `scale=…:eval=frame` cannot change frame size mid-graph (growing frames break the chain;
  shrinking ones render garbage). Animate size with `perspective` on a fixed canvas (`zoom_card`)
  or keep sizes static.
- `geq` uses `T` (not `t`) and copies luma into chroma unless you set `cb='128':cr='128'`.
- `drawbox` treats `w=0` as full width → use `w='max(2,…)'` and `enable` after the start time.
- Proxy video and audio streams differ by a few frames; trim both to the shorter or lip-sync drifts
  across concatenated takes.
- xfade offsets must equal the incoming clip's timeline start; give the outgoing clip a tail of
  the transition length so audio stays in sync.

## ImageMagick 7
- Fully transparent first frames are written as non-RGBA PNGs and break ffmpeg's alpha → always
  write `PNG32:path`.
- Pango markup: ImageMagick unescapes `&amp;` before Pango sees it → avoid `&` in headlines.
- Line caps go inside MVG: `-draw "stroke-linecap round stroke-linejoin round polyline …"`.
- Morphology on the alpha channel leaves black RGB blobs → close gaps on a white-on-black mask,
  then use it as the alpha of a solid fill (`locmap.base_map` does this).
- Cache rendered cards by **content hash**, not list position, or reordering shows stale text.

## Media
- iPhone `.MOV` is often HDR HLG (`arib-std-b67`, BT.2020, 10-bit). Untreated it looks washed out
  next to SDR footage. Tone-map: `zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,
  tonemap=tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv`.
- Phone clips carry rotation side-data; ffmpeg auto-rotates — scale to 1080×1920 after.
- Whisper hallucinates on silent clips ("Thank you for watching") → list them in `SKIP_CLIPS`.
- PyAV version clash in faster-whisper (`metadata_errors`) → load the WAV with `wave` + numpy.

## Data and permissions
- Overpass may refuse automated requests; don't retry with spoofed user agents or mirror-hop.
  Nominatim (`fetch_map_data.py`) at 1 req/s with an honest UA is enough for a stylised map.
- Installing faster-whisper / downloading models needs the user's go-ahead.
- Trending music can't be embedded legally; deliver a voice-only cut for in-app audio.
