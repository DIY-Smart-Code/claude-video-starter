# flow-explainer: the style contract

Every video made from this template meets every line below. The topic changes, the style never does.
`build/check_style.py`, `build/check_svg_fit.mjs`, `npx hyperframes check` and `build/check_static.py`
enforce most of it; the rest you check by looking at every QA sheet.

## 1. One system, staged. Never a slideshow

- Draw the topic as ONE system: at most 9 nodes at full size, zones for boundaries (who owns what),
  wires with a direction. `SYSTEM(G)` holds only `G.node` / `G.zone` / `G.wire` calls.
- Every chapter is a stop on that map: stage it (focus and dim, zoom with `frame`, annotate with badges
  and chips) or mount it as the `mini()` locator next to a close-up. A close-up may bring its own small
  diagram (a timeline, pages, a capacity bar), but `SYSTEM` appears in at least 60 % of the scenes and
  in the last one (gate).
- Everything comes from the topic: icons from the built-in set (`API.md`), the topic palette, the backdrop
  shapes drawn from three of the system's icons. Logos are optional: official files only, at most two
  brands in a frame, never required.

## 2. Every sentence changes the picture

- Every beat sits on its spoken words: `S.p("unique phrase")`. Never a literal second (gate).
- Something changes at least every 3 s (the gate fails at 4 s), and a LARGE change comes at least every
  4 s: a solid `fill()`, a focus dim, a new card or track, a zoom. Packets alone do not count; the
  freeze check on the render ignores small movers.
- Reveal a thing on the word that names it, not before. Frame 0 is already a picture (a title plus the
  pile of cards, or the system), good enough to be the thumbnail.

## 3. Labels, not sentences

- No sentence from the narration on screen. Chips and labels have at most 4 words, badges 3, the chapter
  card's name 3, titles and headlines 6 (separators such as `·` `=` `+` do not count). Gate.
- The chapter card (number plus name, top right) replaces the sentence headline a slide would have.
- Type: Inter for titles and labels, JetBrains Mono for chips, badges and the HUD, always by literal name.
  Nothing under 20 px (gate); chips 24 px, big chips 30 px, node labels 28 px, titles 56 px and up.

## 4. Colour means something, in every video

| Token | Means | Where |
|---|---|---|
| `accent-1` | the subject, the platform, our side | zone, nodes, chapter card, big cards |
| `flow` | things in motion: events, requests, packets | packets on wires, event docs, flow chips |
| `ok` (green) | recommended, fine, arrived | `recommend()`, check badges, fills |
| `bad` (red) | missing, broken, conflict, lost | `fail()`, strikes, overflow, red spans |
| `warn` (amber, dashed) | an open question | `open_q()` |
| `draft` (violet, dashed) | derived, example, not measured | `example_tag()`, `draft_stamp()` |
| ink chip | the verdict line | `chp(..., "ink")` |

- Set the topic colours in `VIDEO["palette"]` (`accent-1`, optionally `flow`); `accent-2`, the soft icon
  fill and the rgb companions derive from them. Never hand-edit the token files for one video.
- A made-up number carries EXAMPLE, a derived one DERIVED or NOT MEASURED, on the word that says so.

## 5. Motion grammar

- Packets (`G.flow`) travel the wires for anything in motion; `fail` / `ok` / `badge` / `paint` / `fill`
  mark state; `focus` dims the rest to about 0.2; `fband` frames what the narration is on and only
  appears when its content is there (never an empty frame).
- Scene seams are stamped by the build (cut-the-curve LEFT / UP, zoom-through); the backdrop moves only
  at seams. Entrances 0.4 to 0.8 s with `power3.out`, pops with `back.out`. No loops, no blinking, no
  idle drift.
- Animate transforms (x, y, scale, rotation), opacity and colours, never `left` / `top`. No CSS transform
  in the markup of an element GSAP moves. Initial states live in the markup (a `tl.set` at 0 does not
  render frame 0). Two tweens never touch the same property at the same time (lint).
- On the paper skin a white-on-cream change is invisible to the freeze check: make the big changes with
  `fill()`, dims, coloured cards and tracks, or a camera step. The check counts change per frame, so the
  big change must be fast (0.3 to 0.6 s), not a slow fade.
- `flow` is a fill colour (packets, event docs, bars). For coloured text use `acc`, `ok` or `bad`: orange
  text on cream misses the 3:1 contrast `hyperframes check` asks for.

## 6. Layout

- Safe area: HUD 28 to 68 px from the top, chapter card 108 to 188 px top right, footer line from 1040 px.
  The `mini()` locator sits top left at (96, 112, 520, 120).
- At least 30 px between chips; wires never cross a label; chips never straddle a zone border; diagrams
  never leave the canvas. A canvas more than half empty for over 2 s needs the ghosted system or the
  next element already in place.

## 7. Determinism

- No `Math.random`, `Date.now`, timers or network calls; fonts and GSAP are local files (gate).
- `index.html`, `compositions/` and `ledger.json` are generated: edit `build/video_scenes.py`, rebuild.

## Gates, in order

`python build/build.py` (0 WARN) → `python build/check_style.py` → `npx hyperframes lint` →
`npx hyperframes check` → `node build/check_svg_fit.mjs .` → `python build/qa.py sweep ...` (look at
every sheet) → render → `python build/check_static.py` → `/video-review` (8 or higher everywhere).
