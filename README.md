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
├── examples/prompt-caching-kitchen/ the explainer from the tutorial: brief, script, storyboard, art
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
paste both in. `.env` is gitignored; the key and the voice never go into a prompt. The free plan is
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
> /review videos/<slug>
```

`/review` turns the render into a grid of 18 stills, scores Hook, Readability, Motion and Variety
out of 10 and names the three worst problems with timestamps, starting with the ones that keep a
score under 8. Apply them, render again, and run `/review` once more:

```
> Yes, apply all three.
```

The target is 8 or more on every score; only then does `/review` say the video is ready to ship.
In the tutorial run, round three put readability at 9 and said the video could ship as it was, but
the hook was still a 6: a headline on empty paper. Round four stacked request bars beside the
headline (hook 7, the bars were too small); round five made them tall, and every score reached 8.
Two lessons are built in: the tiles are a quarter of full size, so Claude checks a full-size frame
before it calls text too small; and when `npx hyperframes check` fails after a fix, believe the check
until a frame from the render proves otherwise.

The finished project from the tutorial is in `examples/prompt-caching-kitchen/`.

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
