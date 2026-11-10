---
name: cinematic
description: Make a cinematic marketing film (launch, brand, product teaser, 20-90 s) with templates/cinematic - lit product in darkness, 24 fps motion-blurred camera, trailer edit, designed score, graded and letterboxed finish. Use when someone wants a film or trailer that feels shot, not a motion-graphics explainer.
argument-hint: <product or URL, the one thing to remember, length, voice or music-only, aspect>
---

# Cinematic film

The template is `templates/cinematic/`. Read `DESIGN.md` (what makes it cinematic, and the rules) and
`API.md` (every `cine.*` call, `film.json`) before the first shot. The Nocturne demo (`index.html`,
`film.json`) is the worked example: copy its patterns, not its content.

All commands run from the repo root. HyperFrames for this template is pinned to 0.9.29
(`npx --yes hyperframes@0.9.29 ...`); `scripts/film.py` does that for you.

## 1. Brief (`BRIEF.md`)

Product, audience, the one thing the viewer must remember, the call to action, length, aspect
(16:9 at 2.39, and/or 9:16), voice (ElevenLabs from `.env`) or music-only, look (`night`,
`teal-orange`, `warm-film`, `clean`, `noir`), and the mode (collaborative: storyboard review;
automation: no stops). Ask only for what is missing, in one round.

## 2. Spawn and capture

```bash
python scripts/new-cinematic-video.py <slug> "<title>"
npx --yes hyperframes@0.9.29 capture <url> -o videos/<slug>/capture   # brand colours, fonts, logo, real screens
```

Real screenshots go into the phone (`.p-screen > img`) or a macro shot; never generate UI as an
image. Write `fact-check.md`: every on-screen claim with the source sentence it rests on.

## 3. Treatment

Decide, in this order, and write it into `film.json` `shots` (one entry per shot: `id start end key
shot light camera type sound out`):

1. **The world.** Where is the product lit? One sentence ("a phone floating in a night sky"). The
   brand's colours become `--key` / `--fill` / `--accent`; the void stays near black.
2. **The acts** (DESIGN.md §5): cold open, act 1, the turn (silence → hit), act 2, montage, title +
   button. A 30 s film has 8-10 shots, a 60 s film 14-18.
3. **Each shot:** the picture, its light (key, rim, air), its camera move, at most one line of type,
   its sound, and how it leaves (cut, flash, whip, burn, dip). No two neighbours share a composition.

## 4. Voice (optional)

Sparse: 6-12 short lines for 30-60 s, written for the ear (CLAUDE.md narration rules), with room
for the music between them. `python scripts/tts.py videos/<slug>`, then take every reveal's time
from `transcript.json`. Put the voice in `film.json` `audio.voice` (it ducks the music); never as an
`<audio>` in the cut.

## 5. Score

Write `film.json` `score`: music sections that match the acts (each 3 s or longer: ElevenLabs
rejects shorter ones) and the hits (drone, riser, boom, whoosh, tick, shimmer, plus anything the film
needs). Then `python scripts/film.py score videos/<slug>`. Put every hit on its cut in `audio.sfx`
and pull the music down before the turn with `audio.music.envelope`.

## 6. Storyboard

`python scripts/film.py board videos/<slug>` writes `storyboard.html` from the shot list. Collaborative
mode: show it and wait for the confirmation (CLAUDE.md rule 2). Automation mode: go on.

## 7. The cut (`index.html`)

Replace the demo's shots, keep its skeleton: root with `data-fps="24"`, `data-aspect`, the motion-blur
attributes; one `.shot clip` per shot; the four overlays (`fx-leak`, `fx-flash`, `fx-black`, `bars`);
one `cine.film(...)` timeline ending in `cine.end(...)`. Per shot: a light layer, an air layer, a
camera move, then type. Lint after every edit:

```bash
npx --yes hyperframes@0.9.29 lint videos/<slug>
```

The 10 `nested_structure_needs_subcomposition` / Studio warnings are expected (one-file film); errors are not.

## 8. Render and look

```bash
python scripts/film.py all videos/<slug>        # cut, mix, finish, contact sheet, storyboard with stills
python scripts/film.py stills videos/<slug> <t> <t> ...   # full-size frames of the cut
```

Look at the storyboard stills and the contact sheet yourself, then at full-size frames of the
finish (`ffmpeg -ss <t> -i videos/<slug>/out/<slug>.mp4 -frames:v 1 ...`) for every shot and every
transition. Go through DESIGN.md §9. Fix, re-render, look again. Then hand over: the user runs
`/video-review videos/<slug>`.

## Pitfalls

- **Motion blur skips 3D and blend modes.** Anything inside `.stage` / `.world` or with
  `mix-blend-mode` renders sharp. Orbits stay slow; whips and crash zooms go on 2D `.cam`s.
- **The finish darkens.** Contrast, vignette and the shadow wheel pull the image down: light the cut a
  little brighter than you want the film, and judge the finish, not the cut.
- **Bloom clips big bright areas** (a moon, a white card): keep large surfaces under ~85 % brightness.
- **SVG lines:** `vector-effect: non-scaling-stroke` breaks dash-offset drawing (it turns into dashes).
  `cine.draw` grows `<line>`s from their attributes instead; use lines, or paths without non-scaling-stroke.
- **No second root HTML.** `finish.html` lives in `build/`; another `data-composition-id` file at the
  root fails lint (`multiple_root_compositions`).
- **No template literals in `querySelector`** (the bundler crashes), and only bundled font families
  (no `Impact`, no OS fonts).
- **Initial states go in the markup or in `fromTo`**: a `tl.set(..., 0)` never renders frame 0.
- **Never put a CSS `transform` in the markup of an element GSAP moves**; wrap it instead (`.rw` around
  a ridge in the demo).
- **`hyperframes check` on the cut** reports `film_silent` and `audio_file_without_element`: expected,
  the sound lives in the finish. Put `data-layout-ignore` on in-device UI that is texture (a lock
  screen), and fix every real overlap or contrast finding.
- **ElevenLabs music doesn't hit section boundaries exactly** and can resolve early. Shape it with
  `audio.music.envelope`, and add a tail hit (a soft pad swell) if it ends before the film does.
- **Check the mix by numbers:** RMS per 0.5 s of `build/mix.wav` shows the dip before the turn, the
  hits and any digital silence (-180 dB) at the end.
- **WebGL registry blocks** (`vfx-iphone-device`, `rack-focus`, shader backgrounds) can't share a page with
  capture motion blur: render them as their own project and place the MP4 as a muted `<video>`.
