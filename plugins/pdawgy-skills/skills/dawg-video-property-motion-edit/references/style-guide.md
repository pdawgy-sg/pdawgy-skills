# Property Motion — style guide

The look: the agent's tour fills the frame; warm dark/amber infographics live in the empty parts
of each shot and land on his words. Most rules below came from client feedback on the Amberwood
reel. They're why it got approved.

## Canvas and timing
- 1080×1920, 30 fps, H.264 CRF 20, AAC 192k, `+faststart`. Keep files < 30 MB.
- One section per agent take; sections cut hard. Segment length = the take's common A/V length.
- Every overlay starts on a word timestamp (≈ word start, minus 0.05–0.1 s so it lands *as* he
  says it). Fade/rise in 0.3–0.45 s with cubic ease-out; clear 0.25 s before the next idea.
- Captions: 40 px Noto Sans Bold, white on a dark rounded pill (82 %), keywords (`project.KEYWORDS`)
  in amber. Default line y≈1560. Hide them while a graphic spells out the same words.
  (The ffmpeg fallback highlights the spoken word instead — karaoke.)

## Palette and type
- Background `#0D0B09`, accent amber `#E8A85C`, text white / warm grey `#B9B2A8`.
- **Stacked titles** (main title system): a tracked caps kicker (Inter SemiBold 32 px, tracking 180,
  amber) over a bold headline (Inter Bold 88 px, white, soft shadow), with an 8 px amber rule on the
  left; left-aligned at x≈72; pairs step 158 px and stack downward as he lists things
  ("3-BEDDER / 958 sq ft", "WITH A / Flexi room", "RIGHT AT THE BACK / Bomb shelter"). The kicker
  carries the connective words he says, the headline the fact.
- Panel headlines: Noto Sans Bold 64–96 px with one accent phrase in amber (character styles).
- Labels: Noto Sans Medium 36–46 px. Fine print (CEA line): 25 px `#8E867B`.

## Layout zones (find them per take with a gridded frame grab)
- **Ceiling zone** (top ≈ 0–650 px): empty in showflat shots → headlines, counters, ticks, the price
  panel, the map card. Put a dark top scrim behind text (strength 0.85–0.92; bright cove lighting
  needs the stronger end).
- **Agent zone** (centre): keep clear of his face and body. Use `avoid` rects for map labels.
- **Below-the-agent band**: in the closer, lift the take ≈320 px and fade it into the background so
  details sit under his feet.

## Client-feedback rules (apply up front)
1. **The tour is the content.** Footage plays full-screen in every section; don't shrink it into
   floating cards ("some people actually want to see the tour"). Graphics go *over* it.
2. **When he names a feature that has b-roll, cut to it full-screen** (bomb shelter) — not a small
   picture-in-picture. Keep the counter/ticks on top.
3. **Mind where he points.** If he gestures to his right, anything he refers to goes screen-left.
4. **Map must pop, not blend.** A translucent amber HUD over warm footage read as invisible. Use the
   solid cream map card (`locmap` palette `"card"`): gold roads, deep amber 1 km ring, dark pin,
   cream-on-dark label tags 32 px, soft black shadow, footage dimmed ~0.68 behind it.
5. **Floor plans go below the agent**, popping up one per spoken number ("3… 4… 5") in the band
   under his feet — not above his head. Cards replace "3-BED/4-BED/5-BED" chips (no duplication).
6. **Hide the project name** when the goal is lead generation: map pin reads "NEW LAUNCH" + road,
   no wordmark, CTA "Text me for the project name". Road/area may stay if the client agrees.
7. **Lead with the strongest hook.** Reorder takes when the client asks (value claim first).
8. **Last clip full-screen**, with details landing below him on his words; captions move to the top
   so they don't repeat the details.

## Compliance and honesty
- Singapore CEA ads: show salesperson name, CEA registration number, contact number, agency name and
  agency licence number. Get them from the user (an ID card photo works); don't invent them.
- On-screen claims = his words or the client's documents. Derived numbers ("~27% less") must be
  plain arithmetic from his figures — say so to the user.
- Footage of one unit type is never presented as another; label units when both appear.
- Map distances are straight-line from the pin; don't call them walking times.

## Section patterns (see build_reel.py)
| Pattern | Use when he says… | Graphics |
| --- | --- | --- |
| `hook` | a value/positioning claim | headline + big keyword (CCR) in the ceiling zone |
| `size_and_features` | size + features | counter on the number, tick rows on each feature, full cut to feature b-roll |
| `price_compare` | comparable vs our price | frosted-glass panel, two bars growing on the prices, "~x% less" pill |
| `location` | schools / MRT / amenities | cream map card, POIs pop on the words, headline lines below |
| `closer` | availability + "contact me" | facilities line, floor plans on the numbers, CTA + agent + CEA details, 2.2 s hold |

## From the second Amberwood reference (another agency's cut)
- Adopted: the stacked kicker + headline titles and amber keyword captions above.
- Worth adding when the right documents exist: a corner **floor-plan minimap** with a red "you are
  here" dot that moves room to room, and a full-screen plan that **zooms into the dot and dissolves
  into that room's footage**. Only do this with the floor plan of the exact unit being toured — a dot
  on a similar-but-different layout misleads buyers.
