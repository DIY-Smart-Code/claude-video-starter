# flow-explainer template

Explainers drawn as one living system diagram: the topic becomes a map of parts and wires, every sentence
of the narration changes that map (a packet travels, a part lights, fails, fills, gets a badge), and each
chapter is a stop on it. Nothing depends on art you have to supply: nodes come from 39 built-in icons, the
palette from the topic, the backdrop from three of the system's icons. Logos are optional.

Proven on a 4.5-minute decision briefing. The demo here is a 1:45 explainer about webhook delivery
(4 decisions, 7 scenes) that uses every recurring piece.

Use it with `/flow-explainer` (`.claude/skills/flow-explainer/SKILL.md`), which runs the whole workflow.

```
templates/flow-explainer/
├── DESIGN.md               the style contract: what every video must get right (read first)
├── API.md                  every call build/video_scenes.py may use, with the topic shapes each fits
├── script.txt              the demo narration (written for the ear)
├── build/
│   ├── video_scenes.py     THE per-video file: VIDEO table, SYSTEM(G), one function per scene (demo)
│   ├── build.py            writes compositions/, index.html, ledger.json, the backdrop shapes
│   ├── flow.py explain.py atoms.py kit.py timing.py   the engine: never edited per video
│   ├── seam_stamp.mjs      scene transitions from ledger.json (run by build.py)
│   ├── check_style.py      style gate (one system, phrase anchors, label budgets, beats every <= 4 s)
│   ├── check_svg_fit.mjs   no wire through a label, no chip on a border (needs the repo's hyperframes)
│   ├── check_static.py     post-render freeze check (no stretch over 5 s)
│   ├── storyboard.py       storyboard.html: real stills of every scene + its narration
│   └── qa.py               dense QA sheets: qa.py sweep <name> <start> <end> <step> | qa.py at <name> <t,...>
├── tokens/flow-paper.css, tokens/flow-dark.css    the two skins
└── assets/fonts (Inter, JetBrains Mono, Playfair italic; OFL), assets/vendor/gsap.min.js
```

## Start a video

All commands run from the repo root (`V=videos/my-topic`):

```bash
python scripts/new-flow-video.py my-topic "My topic, explained"
# write $V/SYSTEM.md, $V/script.txt and $V/build/video_scenes.py (see /flow-explainer), then:
python $V/build/build.py && python $V/build/check_style.py && python $V/build/storyboard.py
python scripts/tts.py $V                       # the voice from .env -> narration.wav + transcript.json
python $V/build/build.py && python $V/build/check_style.py
npx hyperframes lint $V && npx hyperframes check $V && node $V/build/check_svg_fit.mjs $V
python $V/build/qa.py sweep s1 0 <total> 3     # then look at every qa/s1/sheet-NN.png
npx hyperframes render $V -o $V/out/my-topic.mp4 && python $V/build/check_static.py
```

Without `transcript.json` the build runs on synthetic timing from `script.txt` (about 150 words per
minute), so the storyboard and every check work before the voice exists. After the voice, rebuild: every
beat moves to its spoken word because every beat is a phrase anchor.

## VIDEO keys

| Key | Example | Meaning |
|---|---|---|
| `title`, `seed` | `"seed": "my-topic"` | page title; the backdrop placement seed |
| `skin` | `"paper"` / `"dark"` | cream graph paper with ink outlines, or a graphite board |
| `palette` | `{"accent-1": "#2F5BD3", "flow": "#E2683A"}` | topic colours (`accent-1` subject, `flow` motion); the rest derives |
| `lang`, `strings` | `"de"` | marker words (RECOMMENDED / EMPFOHLEN ...); `strings` overrides single words |
| `backdrop` | `["api", "queue", "shield"]` | three icons for the ghosted topic shapes |
| `chapters` | `["Overview", "D1 Signature", ...]` | the HUD strip, one segment per chapter |
| `scenes` | `{"id", "first", "enter", "chapter", "title", "source"}` | `first` = the first words of the scene (unique) |
| `hud_prefix`, `source_label` | `""`, `"SOURCE"` | HUD numbering prefix, footer label |
| `cta` | `{"phrase": "...", "kw": [...]}` or `None` | a closing question shown word by word |
| `brand_logo` | `"assets/logos/x.svg"` | optional corner mark (official file only) |
| `narration`, `lag`, `terminal_hold` | `"narration.wav"`, `0.15`, `3.0` | audio file, word-start lag of the TTS, closing hold |
| `seam_sfx` | `"assets/sfx/whoosh.mp3"` | optional whoosh before each seam (your own file) |
