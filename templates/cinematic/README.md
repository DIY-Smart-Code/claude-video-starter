# Cinematic template

Marketing films that look shot, not animated: a product lit out of darkness, a camera moving through
the world at 24 fps with real motion blur, trailer-style edit and type, a designed score, then a
colour grade, film grain and 2.39:1 letterbox over the whole picture.

Demo: **Nocturne: "Look up"**, a 30 s film for a fictional stargazing app (cold open, sky, title card,
the hit, hero orbit, macro, feature with rack focus, montage, wordmark). Every pixel is HTML/CSS, so
the template ships no third-party footage.

```bash
python scripts/film.py all templates/cinematic          # cut + mix + finish + contact sheet (~1.5 min)
npx --yes hyperframes@0.9.29 preview templates/cinematic # live preview of the cut
```

## Start a film

```bash
python scripts/new-cinematic-video.py <slug> "Title"   # copies the template into videos/<slug>/
```

Then the `/cinematic` skill (`.claude/skills/cinematic/SKILL.md`) runs the workflow: brief → treatment
and shot list → score plan → build the cut → `film.py all` → look at every shot → hand over for
`/video-review`.

## Files

| File | What it is |
|---|---|
| `index.html` | **the cut**: shots, light, camera, type, edit. Picture only. |
| `film.json` | look, audio cues and the score prompts. `build/finish.html` is generated from it. |
| `lib/cine.js`, `lib/cine.css` | the camera / lens / light / type / edit / device toolkit (`API.md`) |
| `DESIGN.md` | the design contract: what makes it cinematic and the rules that follow |
| `assets/score/` | music and hits (`film.py score` generates missing ones with ElevenLabs) |
| `assets/fonts/` | Cormorant Garamond, Anton, Inter (SIL OFL) |
| `build/` | `cut.mp4`, `mix.wav`, QA stills (generated, not committed) |
| `out/<slug>.mp4` | the finished film |

## Pipeline

```
film.json ──score──▶ assets/score/*.mp3          (ElevenLabs music + hits, once)
index.html ──cut──▶ build/cut.mp4                (24 fps, 180° motion blur, crf 10)
film.json ──mix──▶ build/mix.wav                 (envelope, sidechain duck, hits, -14 LUFS)
film.json ──finish──▶ build/finish.html ──▶ out/<slug>.mp4   (HyperFrames colour grade + grain + bars + mix)
```

Every step is `python scripts/film.py <step> <folder>`; `stills <folder> 3.5 11.2 …` pulls full-size
frames from the cut for checking a moment.

## What it uses from HyperFrames (0.9.29)

- **Capture motion blur** (`data-motion-blur="on"`, `data-motion-blur-tier="capture"`,
  `data-motion-blur-shutter="180"`): real shutter blur on moving 2D layers.
- **The colour-grading shader** (`data-color-grading` on the cut as a `<video>`): contrast and exposure,
  shadow/highlight wheels, bloom, channel separation, vignette, deterministic film grain.
- **`render -c build/finish.html`** to render the second composition of the same project (kept in `build/`: a second root composition fails lint).
- Registry pieces worth pulling in for specific shots (`npx --yes hyperframes@0.9.29 add <name>`):
  `vfx-iphone-device` (GLTF phone, WebGL: render as its own plate), `rack-focus` and `vfx-anamorphic-flare`
  (WebGL), `camera-shake`, `light-sweep-pass`, `whip-pan-cut`, `logo-sting`. WebGL blocks can't share a
  page with capture motion blur: render them separately and place the result as a `<video>`.

The rest of the repo stays on HyperFrames 0.8.121; this template pins 0.9.29 through `npx` in
`scripts/film.py` and `package.json`.
