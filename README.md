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
├── .claude/commands/review.md       /review: contact sheet + scores for a render
├── scripts/tts.py                   ElevenLabs: script -> narration.wav + transcript.json
├── scripts/contact-sheet.py         a render -> one 6x3 grid of stills
├── .env.example                     your ElevenLabs settings (copy to .env)
├── examples/prompt-caching-explained/  the explainer from the tutorial: brief, script, storyboard, art
├── templates/                       bundled fonts and GSAP the workflow can reuse
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

**Voice (ElevenLabs).** Pick a voice in the [voice library](https://elevenlabs.io/voice-library) and
copy its voice ID (the tutorial uses the stock voice Sarah, `EXAVITQu4vr4xnSDxMaL`). Create an
[API key](https://elevenlabs.io/docs/api-reference/authentication). Then `cp .env.example .env` and
paste both in. `.env` is gitignored; never paste the key into a prompt. The free plan is
non-commercial only; a monetized channel needs a paid plan
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
One prompt starts everything. Give it your topic, your take, your sources, your look and your voice:

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
  Voice: ElevenLabs, voice id EXAVITQu4vr4xnSDxMaL. No music. YouTube, 16:9.
```

"Use the standard explainer pipeline" routes it to `/faceless-explainer`. It recommends an angle,
may offer a few additions, and asks what's missing. Answer in a line each. In the tutorial run:

```
> 1. Yes, the narrative concept.
  2. Both. Keep one kitchen across the idea scenes: empty, prepped, serving.
  3. No, only the two docs pages.
```

The answers land in `BRIEF.md`.

## 3. The script
Claude writes `SCRIPT.md` from your sources and checks every claim in `fact-check.md`: one row per
claim, with the sentence from the source it rests on. Read that file. In the tutorial run it dropped
two claims the docs didn't support and marked the take as an opinion. If your run skips the file,
ask for it:

```
> Check every number in SCRIPT.md against the sources and write fact-check.md with one row per
  claim: value, source URL, verified or wrong. Fix any wrong ones in the script.
```

The voice reads exactly what's on the page, so write the narration for the ear:

```
> The frames look right. One change to the narration first: write the spoken lines for the ear, with
  commas or full stops instead of dashes, and CLAUDE.md spoken as "Claude dot M D". Keep CLAUDE.md
  as it is on screen. Then draw the sketches.
```

## 4. The design system
The workflow picks one of its frame presets and remixes it onto your colours and fonts. The result
is `frame.md`: palette, type, frame treatments and composition rules. Every frame inherits it, so
check it once before the storyboard is drawn on it. (In the tutorial run the remix set the body font
to Playfair; Claude switched it back to Inter.)

## 5. The storyboard review
Before anything moves, Claude draws every frame as a static sketch in `storyboard.html`, in the real
fonts, colours and text, with notes on what moves first and how each frame hands off to the next.
Open it in your browser and look at it the way a viewer would. Ask for changes frame by frame. The
tutorial's one change:

```
> Frame 11 has too much text on screen. Cut it to the /usage card and let the voice say the two
  habits. Show me the sheet again.
```

When the sheet looks right, say so. `CLAUDE.md` tells Claude never to build before you confirm it.

```
> Looks right. Go on.
```

## 6. Art direction
After you confirm the sheet, Claude runs `/art-direction` for the metaphor scenes (if it doesn't,
type `/art-direction for videos/<slug>`). The skill writes one prompt per scene with a locked style
block (medium, palette hex codes, an empty third for the headline, no text), shows you the first
plate and asks: keep or redo. When a plate has a problem the style should never repeat, put the fix
into the style lock, so every later plate gets it:

```
> Redo it. Add full-bleed, no plate border to the style lock so plates B and C get it too.
```

```
> Keep it. Go on with B and C.
```

The kept plate becomes the reference image for the rest, so they look like one illustrator made
them. Plates that fail the checklist in `.claude/skills/art-direction/style-lock.md` get redone.
Everything is saved to `videos/<slug>/assets/art/` with a ledger of every prompt and job ID. Charts
and numbers stay HTML.

## 7. The voice

The workflow runs `python scripts/tts.py videos/<slug>`. You get `narration.wav` and
`transcript.json`: the start and end time of every word, so every reveal lands on its word.

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

```bash
npx hyperframes check videos/<slug>
npx hyperframes preview videos/<slug>
npx hyperframes render videos/<slug> -o videos/<slug>/out/<slug>.mp4
```

If Claude's own render can't start Chrome from its shell, run the render command yourself.

## 9. The review loop
```
> /review videos/<slug>
```

`/review` turns the render into a grid of 18 stills, scores Hook, Readability, Motion and Variety
out of 10 and names the three worst problems with timestamps. Apply them, render again, and run
`/review` once more:

```
> Yes, apply all three.
```

Stop when the list gets shorter and the problems get smaller; the score doesn't have to reach 10.
Two lessons are built in: the tiles are a quarter of full size, so Claude checks a full-size frame
before it calls text too small; and when `npx hyperframes check` fails after a fix, believe the check
until a frame from the render proves otherwise.

The finished project from the tutorial is in `examples/prompt-caching-explained/`.

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
