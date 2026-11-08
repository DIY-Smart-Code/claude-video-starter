---
name: flow-explainer
description: Make an explainer drawn as one living system diagram (parts, wires, packets, states) from any topic with templates/flow-explainer. Use for systems, processes, pipelines, architectures and decision briefings, where things talk to each other. Not for metaphor or illustration videos (use /faceless-explainer).
argument-hint: <topic, take, sources, length, language>
---

# Flow explainer

The template is `templates/flow-explainer/`. Its engine (flow, explain, atoms, kit) is fixed and carries
the style; a video only writes `build/video_scenes.py`. Read `templates/flow-explainer/DESIGN.md` (the
style contract) and `API.md` (every call) before the first scene. The demo in
`templates/flow-explainer/build/video_scenes.py` is the worked example: copy its patterns.

The topic drives everything: the system map, the icons, the palette, the backdrop shapes, the chapters.
Never wait on assets. Logos are optional (official files only); generated art is not used.

## 1. Brief

Write `BRIEF.md` from the request: topic, audience, the take (one sentence), sources, length, language,
voice (ElevenLabs from `.env`, or the local Kokoro route), look (skin `paper` or `dark`; the topic's brand
colour if it has one, else pick one), and the mode (collaborative: storyboard review; automation: no
stops). Ask only for what is missing, in one round, one line per answer.

## 2. Spawn

`python scripts/new-flow-video.py <slug> "<title>"` creates `videos/<slug>/` with the engine and the demo.

## 3. Research

Read the sources. Write `fact-check.md`: one row per claim with the source sentence it rests on. A number
you cannot source goes on screen as EXAMPLE (`example_tag`) or not at all.

## 4. The system map (`SYSTEM.md`)

Draw the topic as one system before writing a word of narration:
- nodes (at most 9 at full size), each with an icon from the built-in list in `API.md` and a label of at
  most 4 words; zones for ownership or boundaries; wires with direction, and what travels on each wire;
- the colour of each thing by meaning (DESIGN.md section 4) and the palette (`accent-1` = the subject);
- the chapters as stops on the map: which parts each one focuses, and which atom carries its close-up
  (the recipe table in `API.md`: timeline, pages scan, capacity, gantt, value card, board ...).

## 5. Script (`script.txt`)

Written for the ear (CLAUDE.md narration rules). Every sentence names one thing you can show ("the queue
holds it", "the worker writes it"), and every beat gets a phrase that occurs only once. One chapter per
stop; a hook that states the stake as a picture; a close that brings the map back. About 150 words per
minute.

## 6. Scenes (`build/video_scenes.py`)

Replace the demo, keep its structure: `VIDEO` (scenes with unique `first` phrases, chapters, skin, palette,
lang, backdrop icons), `atoms.setup(VIDEO)`, `SYSTEM(G)`, one function per scene, `ALL`. Every time comes
from `S.p("phrase")`. Then, from the repo root:

```bash
python videos/<slug>/build/build.py        # synthetic timing until the voice exists; 0 WARN
python videos/<slug>/build/check_style.py  # one system, phrase anchors, label budgets, beats <= 4 s
npx hyperframes lint videos/<slug>
```

Fix every finding before going on.

## 7. Storyboard

`python videos/<slug>/build/storyboard.py` writes `storyboard.html`: three real stills per scene with its
narration. Look at it yourself first (empty canvas, labels crossing wires, a scene without a big change).
Collaborative mode: show it and wait for the confirmation (CLAUDE.md rule 2). Automation mode: go on.

## 8. Voice

`python scripts/tts.py videos/<slug>` (or the local route in CLAUDE.md), then rebuild and run
`check_style.py` again: the beats move to the spoken words, and gaps can change.

## 9. Visual QA

```bash
npx hyperframes check videos/<slug>
node videos/<slug>/build/check_svg_fit.mjs videos/<slug>
python videos/<slug>/build/qa.py sweep s1 0 <total> 3
```

Look at EVERY sheet in `qa/s1/`. Typical defects: a chip on a zone border, a label crossed by a wire or
an attention frame, chips closer than 30 px, a frame (fband) that appears before its content, a canvas
more than half empty for over 2 s, a node label hidden under a box placed near it. Fix, rebuild, then
re-sweep at a 1.5 s offset (`qa.py sweep s2 1.5 <total> 3`) and spot-check with `qa.py at fix1 <t,...>`.

## 10. Render

```bash
npx hyperframes render videos/<slug> -o videos/<slug>/out/<slug>.mp4
python videos/<slug>/build/check_static.py
```

A frozen stretch over 5 s fails: add a LARGE change on a phrase there (`fill()`, a focus dim, a card,
a zoom), not more packets. Then hand over: the user runs `/video-review videos/<slug>`.

## Pitfalls

- A `tl.set(..., 0)` does not render frame 0: initial states go in the markup (the atoms do this).
- Animate x / y, never `left` / `top`; never put a CSS transform in the markup of an element GSAP moves.
- Two tweens on the same property at the same time fail lint: never `off` and `on` the same part at one
  beat, never `paint` and `fill` the same node within 0.4 s.
- A phrase must occur exactly once in the narration; `S.p` stops the build with the match count.
- After the voice, a beat can land in a different place: re-run `check_style.py` and look again.
- Keep the engine files untouched in a video; improve the template itself on purpose, then re-spawn.
- The freeze check counts per-frame change: a slow fade or a small chip pop does not break a frozen
  stretch. Use fast, large changes: `fill()` on a node (0.35 s), a `focus` that dims or lights the whole
  zone, a new card, a camera step (`S.cam(t, 1.08, x, y, dur=0.6)` and back). Undo a fill with `unfill()`
  before `G.fail` / `G.paint` on that node, or the icon disappears into its own fill.
- Text in the `flow` colour on the paper skin can miss the 3:1 contrast `hyperframes check` asks for; use
  `flow` for fills and packets, `acc` / `ok` / `bad` for coloured text.
- Windows Git Bash: if a `node` command prints "stdin is not a tty", the shell's winpty alias is in the
  way; run `node.exe` instead.
