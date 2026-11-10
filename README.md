# claude-video-starter

Make real explainer videos with Claude Code: a storyboard you review before anything is built,
illustrations in one locked style, a voice synced to the visuals, and a review loop on the render.
This repo is the setup from the DIY Smart Code tutorial, which builds one explainer about prompt
caching from an empty folder to a finished MP4.

**Follow along as a checklist:** every command and prompt from the video, with a copy button, at
[tasklist.smartcode.diy/list/claude-code-video-starter](https://tasklist.smartcode.diy/list/claude-code-video-starter).
The same list ships in `tasklist/claude-code-video-starter.json`.

Videos here are web pages. Claude Code writes HTML with an animation timeline,
[HyperFrames](https://hyperframes.heygen.com) opens it in a headless browser, takes a
screenshot of every frame, and ffmpeg turns the frames into an MP4. You don't need a graphics card.

```
claude-video-starter/
├── CLAUDE.md                        rules Claude Code reads on every run
├── .claude/skills/art-direction/    /art-direction: Higgsfield illustrations in one locked style
├── .claude/skills/video-review/    /video-review: contact sheet + scores for a render
├── .claude/skills/flow-explainer/   /flow-explainer: explainers drawn as one living system diagram
├── .claude/skills/cinematic/        /cinematic: marketing films that look shot, not animated
├── scripts/tts.py                   ElevenLabs: script -> narration.wav + transcript.json
├── scripts/contact-sheet.py         a render -> one 6x3 grid of stills
├── scripts/new-flow-video.py        start a flow explainer from templates/flow-explainer
├── scripts/new-cinematic-video.py   start a cinematic film from templates/cinematic
├── scripts/film.py                  cinematic pipeline: score, cut, mix, finish, sheet, storyboard
├── .env.example                     your ElevenLabs settings (copy to .env)
├── examples/prompt-caching-kitchen/ the explainer from the tutorial: brief, script, storyboard, art
├── templates/                       bundled fonts and GSAP; flow-explainer/ (diagram explainers), cinematic/ (films)
├── tasklist/                        the follow-along checklist (import file + its generator)
└── videos/                          your videos go here, one folder each
```

## 1. Set up

You need [Node.js](https://nodejs.org) 22 or newer, [ffmpeg](https://ffmpeg.org/download.html),
[Claude Code](https://code.claude.com/docs/en/overview) and Python 3.8+.

| | Windows | macOS |
|---|---|---|
| Node.js | `winget install OpenJS.NodeJS.LTS` | `brew install node` |
| ffmpeg | `winget install Gyan.FFmpeg` | `brew install ffmpeg` |

```bash
npx hyperframes@latest doctor
npx hyperframes@latest skills
git clone https://github.com/DIY-Smart-Code/claude-video-starter.git
cd claude-video-starter
pnpm install
```

`skills` installs the official HyperFrames skills for Claude Code (they land in your user folder,
so every project sees them). `pnpm install` pins one HyperFrames version for this repo, so renders
stay identical.

**Voice (ElevenLabs).** Create an
[API key](https://elevenlabs.io/docs/api-reference/authentication), then `cp .env.example .env` and
paste the key in. The voice is preset to the stock voice Sarah (`EXAVITQu4vr4xnSDxMaL`), as in the
tutorial; for another voice, copy its ID from the [voice library](https://elevenlabs.io/voice-library)
into `ELEVENLABS_VOICE_ID`. `.env` is gitignored; the key and the voice never go into a prompt. Optional voice
settings (stability, style, speed, a separate speed for vertical videos) and a pronunciation
dictionary can go in `.env` too; `.env.example` lists them. The free plan is non-commercial only;
a monetized channel needs a paid plan
([ElevenLabs on publishing](https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform)).

**Illustrations (Higgsfield MCP).** Connect it once, from the terminal:

```bash
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
```

Start Claude Code, run `/mcp`, pick **higgsfield** and log in. Or add the same URL under claude.ai
Settings → Connectors; Claude Code then shows it as `claude.ai Higgsfield`
([Higgsfield MCP](https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp)).
Higgsfield needs a paid plan, and every image costs credits.

Then start Claude Code in the repo folder: `claude`.

## 2. The brief
One prompt starts everything. Give it your topic, your take, your sources and your look:

```
> /hyperframes Make a 2-minute explainer about prompt caching for developers who use Claude Code.
  Use the standard explainer pipeline. Collaborative: show me the storyboard before you build.
  My take: most of your Claude Code bill is Claude re-reading the same context, and caching is the
  kitchen where the prep is already done. The idea scenes use that kitchen as illustrations; the
  numbers stay diagrams.
  Sources: https://platform.claude.com/docs/en/build-with-claude/prompt-caching and
  https://code.claude.com/docs/en/prompt-caching
  Look: cream paper #F4F1EA, charcoal ink #1A1815, one clay accent #C15F3C. Playfair Display
  headlines, Inter body, JetBrains Mono labels.
  Voice: ElevenLabs. No music. YouTube, 16:9.
```

"Use the standard explainer pipeline" routes it to `/faceless-explainer`. It writes the brief, may
recommend a few additions, and asks what's missing. Answer in a line each. In the tutorial run it
also warned that the week's usage was low and offered a 90-second cut, recommended counting up the
cost figures, and asked for material of your own:

```
> a. Keep 2:00.
  Yes, count up the cost figures on the word that says them.
  No material of my own, only the two docs pages.
```

The answers land in `BRIEF.md`.

A shorter prompt works too. With only a topic and a look, Claude asks before it writes the brief:
it pitches a few concepts and asks where the video will play, whether you want the storyboard
review, and whether it should run on its own (automation) or check in with you (companion).

## 3. The script
Claude writes `SCRIPT.md` from your sources and checks every claim in `fact-check.md`: one row per
claim, with the sentence from the source it rests on. Read that file. In the tutorial run it checked
19 claims and left MCP servers off the list of things that break the cache, because they only break
it when tool search is off. If your run skips the file, ask for it:

```
> Check every number in SCRIPT.md against the sources and write fact-check.md with one row per
  claim: value, source URL, verified or wrong. Fix any wrong ones in the script.
```

The voice reads exactly what's on the page, so `CLAUDE.md` tells Claude to write the narration for
the ear: commas or full stops instead of dashes, and file names written the way they're said
(`CLAUDE.md` becomes "Claude dot M D"). On screen they keep their written form.

## 4. The design system
The workflow picks one of its frame presets and remixes it onto your colours and fonts. The result
is `frame.md`: palette, type, frame treatments and composition rules. Every frame inherits it, so
check it once before the storyboard is drawn on it. (In the tutorial run the remix set the body font
to Playfair; Claude switched it back to Inter.) If none of the presets fits the look you asked for,
Claude builds a picker page instead and opens it in your browser: a few custom directions, each
shown on frames from your video. Answer with the letter of the one you want. When it looks right,
say so:

```
> The frames look right. Draw the sketches.
```

## 5. The storyboard review
Before anything moves, Claude draws every frame as a static sketch in `storyboard.html`, in the real
fonts, colours and text, with notes on what moves first and how each frame hands off to the next.
Open it in your browser and look at it the way a viewer would. Ask for changes frame by frame. The
tutorial's one change:

```
> Frames 11 and 12 leave the right half of the frame empty. Make each list bigger and centre it so
  it fills the frame. Show me the sheet again.
```

When the sheet looks right, say so. `CLAUDE.md` tells Claude never to build before you confirm it.

```
> Looks right. Go on.
```

## 6. Art direction
After you confirm the sheet, Claude runs `/art-direction` for the metaphor scenes (if it doesn't,
type `/art-direction for videos/<slug>`). The skill writes one prompt per scene with a locked style
block (medium, palette hex codes, an empty third for the headline, no text), shows you the first
plate and asks: keep or redo. Look at the plate yourself, not only at the checklist. When a plate
breaks a rule the checklist doesn't check yet, have the rule added, so every later plate is checked
for it:

```
> Redo it. That edge breaks the no-plate-border rule in the style lock. Add the rule to the
  checklist so every plate gets checked for it.
```

```
> Keep it. Go on with the other three.
```

The kept plate becomes the reference image for the rest, so they look like one illustrator made
them. Plates that fail the checklist in the style lock get redone. The lock in
`.claude/skills/art-direction/style-lock.md` is drawn for cream paper; for another look Claude
writes that video's own lock to `videos/<slug>/assets/art/style-lock.md`, in a medium and palette
that fit it, and checks the plates against that one. Everything is saved to `videos/<slug>/assets/art/` with a ledger of every prompt and job ID. Charts
and numbers stay HTML.

## 7. The voice

The workflow runs `python scripts/tts.py videos/<slug>` with the voice from `.env`. You get
`narration.wav` and `transcript.json`: the start and end time of every word, so every reveal lands
on its word.

Free and local instead (no account): `npx hyperframes tts` with a Kokoro voice, then
`npx hyperframes transcribe` for the word timings (needs whisper.cpp:
`brew install whisper-cpp` on macOS; on Windows the `whisper-bin-x64.zip` from the
[whisper.cpp releases](https://github.com/ggml-org/whisper.cpp/releases) with
`HYPERFRAMES_WHISPER_PATH` pointing at `whisper-cli.exe`).

## 8. The build
Approve the plates and Claude builds every frame on its confirmed sketch (one sub-agent per frame),
assembles the video and runs the checks:

```
> They look right. Start the build.
```

Before the preview Claude also runs `npx hyperframes snapshot`: one still per frame on a contact
sheet in `videos/<slug>/snapshots/`. Look at that sheet too. In a test run the check passed while
the sheet showed three frames that didn't render, and Claude fixed them before the preview.

The build stops at the preview, so look at it before the render. In the tutorial run one frame had
the empty right half that the storyboard review had fixed in two others:

```
> Make frame 10 fill the frame like 11 and 12, then render.
```

```bash
npx hyperframes check videos/<slug>
npx hyperframes snapshot videos/<slug>
npx hyperframes preview videos/<slug>
npx hyperframes render videos/<slug> -o videos/<slug>/out/<slug>.mp4
```

If Claude's own render can't start Chrome from its shell, run the render command yourself.

## 9. The review loop
```
> /video-review videos/<slug>
```

`/video-review` turns the render into a grid of 18 stills, scores Hook, Readability, Motion and Variety
out of 10 and names the three worst problems with timestamps, starting with the ones that keep a
score under 8. Apply them, render again, and run `/video-review` once more:

```
> Yes, apply all three.
```

The target is 8 or more on every score; only then does `/video-review` say the video is ready to ship.
In the tutorial run, round three put readability at 9 and said the video could ship as it was, but
the hook was still a 6: a headline on empty paper. Round four stacked request bars beside the
headline (hook 7, the bars were too small); round five made them tall, and every score reached 8.
Two lessons are built in: the tiles are a quarter of full size, so Claude checks a full-size frame
before it calls text too small; and when `npx hyperframes check` fails after a fix, believe the check
until a frame from the render proves otherwise.

The finished project from the tutorial is in `examples/prompt-caching-kitchen/`.

## Flow explainers: one living diagram

For a topic with parts that talk to each other (a system, a pipeline, a process, a set of decisions),
`/flow-explainer` draws the whole video as one system map instead of illustrations. Every sentence changes
the map: a packet travels a wire, a part lights up, fails, fills or gets a badge, and each chapter is a
stop on the same map. The template (`templates/flow-explainer/`) carries the motion style in a fixed
engine; a video writes one scene file. Nothing depends on art you supply: nodes come from 39 built-in
icons, the colours from the topic, the backdrop from the system's own icons.

```
> /flow-explainer Make a 3-minute explainer about how a webhook reaches your app, for backend developers.
  Take: four decisions decide whether an event arrives once. Sources: <links>. Paper look, blue accent.
  Voice: ElevenLabs. No music.
```

It writes `BRIEF.md`, `fact-check.md`, `SYSTEM.md` (the map) and `script.txt`, builds the scenes on
synthetic timing, and shows you `storyboard.html` (real stills of every scene with its narration) before
the voice is made. After the voice it rebuilds, runs its gates (`check_style.py` for the style contract,
`check_svg_fit.mjs` for wires through labels, a QA sweep it looks at, `check_static.py` on the render)
and hands over for `/video-review`. The template's demo (webhook delivery, 1:45) shows every piece:
`npx hyperframes preview templates/flow-explainer`. Style rules: `templates/flow-explainer/DESIGN.md`.

## Cinematic films: lit, shot and graded

For launch films, brand spots and product teasers, `/cinematic` makes a 20-90 s film that looks shot
instead of animated: the product lit out of darkness with a key, rim light and haze, a camera that
pushes, orbits, racks focus and whips at 24 fps with real 180° motion blur, a trailer-shaped edit (cold
open, the turn on a hit, montage, title), a designed score (music in sections that match the acts,
booms, risers, whooshes), then a colour grade, film grain and 2.39:1 letterbox over the whole picture.

```
> /cinematic Make a 45-second launch film for https://example.app. The one thing: calm is one tap away.
  ElevenLabs voice, night look, 16:9.
```

The template (`templates/cinematic/`) is a toolkit (`lib/cine.js`, `lib/cine.css`), a design contract
(`DESIGN.md`) and a worked example (Nocturne, 30 s, all HTML/CSS). `scripts/film.py` renders in two
passes, like a film: the **cut** (`index.html`, picture only) and the **finish** (the HyperFrames colour
shader, grain, bars and the mixed score, generated from `film.json`). It pins HyperFrames 0.9.29 for
capture motion blur and the grading shader; the rest of the repo stays on 0.8.121. Choosing this
template is the request for music. Try the demo: `python scripts/film.py all templates/cinematic`.

## Going further

This is a basic setup. It makes a good explainer, and there is a lot you can add on top:

- The official [GSAP skills](https://github.com/greensock/gsap-skills) for richer motion:
  `npx skills add https://github.com/greensock/gsap-skills`
- Ready-made blocks from the HyperFrames registry: `npx hyperframes catalog --query "<the look you want>"`
- Camera moves and punch-ins with `/hyperframes-keyframes`
- Sound effects through `/media-use`

Our own videos add more layers on top of this: motion rules so every scene's exit leads into the
next one, sound effects timed to the frame, a retention review of the first minute, and real
evidence captured from product pages.

## License

MIT for the code in this repo. The fonts in `templates/*/assets/fonts/` are under the SIL Open
Font License (see the `OFL-*.txt` files next to them). GSAP is vendored under its own license
(header of `gsap.min.js`).
