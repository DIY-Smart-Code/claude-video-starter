# claude-video-starter

Make videos with Claude Code. This repo is the setup from the DIY Smart Code tutorial
**"Your first AI video: the full process"**: an empty folder to a narrated MP4 in eight steps.

Videos here are web pages. Claude Code writes HTML with an animation timeline,
[HyperFrames](https://hyperframes.heygen.com) opens it in a headless browser, takes a
screenshot of every frame, and ffmpeg turns the frames into an MP4. You don't need a graphics card:
without one, the browser renders in software.

```
claude-video-starter/
├── CLAUDE.md                 rules Claude Code reads on every run
├── .claude/commands/review.md   /review: contact sheet + scores for a render
├── templates/long-form/      16:9 starting point (1920x1080)
├── templates/short/          9:16 starting point (1080x1920)
├── scripts/tts.py            ElevenLabs: script.txt -> narration.wav + transcript.json
├── scripts/contact-sheet.py  a render -> one 6x3 grid of stills
├── .env.example              your ElevenLabs settings (copy to .env)
├── examples/demo-app/        a tiny app to point /brag at in step 8
├── examples/git-undo-explainer/  the step-7 script and its word timings
└── videos/                   your videos go here, one folder each
```

## 1. Install the tools

You need [Node.js](https://nodejs.org) 22 or newer, [ffmpeg](https://ffmpeg.org/download.html),
[Claude Code](https://docs.claude.com/en/docs/claude-code/overview) and Python 3.8+.

| | Windows | macOS |
|---|---|---|
| Node.js | `winget install OpenJS.NodeJS.LTS` | `brew install node` |
| ffmpeg | `winget install Gyan.FFmpeg` | `brew install ffmpeg` |

Then check everything and add the HyperFrames skills for Claude Code:

```bash
npx hyperframes@latest doctor
npx hyperframes@latest skills
```

`@latest` makes sure you run the current release, not an older copy that may already sit on your machine.

`doctor` marks whisper-cpp as optional. You only need it for the free voice route in step 5.

## 2. Clone the starter

```bash
git clone https://github.com/DIY-Smart-Code/claude-video-starter.git
cd claude-video-starter
pnpm install        # or: npm install
claude
```

`pnpm install` pins the HyperFrames version for this repo, so every `npx hyperframes` command in it runs the same version and renders stay identical. Read `CLAUDE.md` once. Three lines at the top do most of the work:

1. Use HyperFrames for every video.
2. Same input, same frame: no random numbers, clocks or timers in a composition, so a render never changes.
3. Lint after every edit, and a video is not finished until you have run `/review` on it.

## 3. Your first render

In Claude Code:

```
> Using /hyperframes, make a 15-second title card for claude-video-starter, 16:9.
```

Claude copies `templates/long-form/` into `videos/<slug>/` and builds the composition. Then:

```bash
npx hyperframes preview videos/<slug>        # watch it in the studio
npx hyperframes lint videos/<slug>           # catches broken timing before you render
npx hyperframes render videos/<slug> -o videos/<slug>/out/<slug>.mp4
```

## 4. Make Claude watch its own frames

```
> /review videos/<slug>
```

`/review` runs `scripts/contact-sheet.py`, which turns the render into one grid of 18 stills
spread across the video. Claude reads the image, scores Hook, Readability, Motion and Variety
out of 10, and names the three worst problems with timestamps. Say "fix them", render again,
and run `/review` once more. That loop is what turns a first draft into something you would post.

Two things the tutorial run taught us, now written into `/review`:

- The tiles are a quarter of full size, so text always looks too small on the sheet. Claude checks a
  full-size frame before it calls text too small.
- When `npx hyperframes check` fails after a fix, believe the check. Pull a frame from the render
  and look before anyone calls it a false positive.

Don't chase the scores. They stay rough; the timestamped problems are what you fix.

## 5. A voice

**ElevenLabs** (needs an account). The free plan is for non-commercial use only and asks you to
credit ElevenLabs in the title; a monetized channel needs a paid plan
([ElevenLabs on publishing](https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform)).

1. Pick a voice in the ElevenLabs voice library and copy its voice ID.
2. Create an API key.
3. `cp .env.example .env` and paste both in. `.env` is gitignored; never paste the key into a prompt.
4. Put your script in `videos/<slug>/script.txt` and run:

```bash
python scripts/tts.py videos/<slug>
```

You get `narration.wav` and `transcript.json`: the start and end time of every word.

**Free and local** (no account, no key): HyperFrames ships a voice model (Kokoro-82M).

```bash
npx hyperframes tts videos/<slug>/script.txt --voice am_michael -o videos/<slug>/narration.wav
npx hyperframes transcribe videos/<slug>/narration.wav -d videos/<slug>
```

`npx hyperframes tts --list` shows the voices. `transcribe` needs whisper.cpp for the word timings:
on macOS `brew install whisper-cpp`; on Windows download `whisper-bin-x64.zip` from the
[whisper.cpp releases](https://github.com/ggml-org/whisper.cpp/releases) and point
`HYPERFRAMES_WHISPER_PATH` at the `whisper-cli.exe` inside it. Both routes write the same
`transcript.json`, so the next steps work either way.

## 6. Pictures with the Higgsfield MCP

Higgsfield's MCP server lets Claude Code generate images and clips for your videos.

Connect it once. Both ways below use the same server, `https://mcp.higgsfield.ai/mcp`:

- **From the terminal:**

  ```bash
  claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
  ```

  Start Claude Code, run `/mcp`, pick **higgsfield** and log in to Higgsfield in the browser window.
- **Through claude.ai:** add the URL under Settings → Connectors. Claude Code shows it as
  `claude.ai Higgsfield` whenever you are logged in with that account. This is the route used in
  the video.

Run `claude mcp list` and check that Higgsfield shows as connected. Higgsfield needs a paid plan, and every
generation costs credits.

Higgsfield's own guide for Claude Code uses its CLI instead of MCP:
`npm i -g @higgsfield/cli`, then `higgsfield auth login`, then `npx skills add higgsfield-ai/skills`
([Higgsfield: connect to an AI agent](https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent)).

Then ask for an illustration with your palette locked:

```
> Generate a dark illustration of a cassette tape rewinding for my git explainer.
  Palette #0B0F18 and #68D9FF, no text, 16:9. Save it to videos/<slug>/assets/.
```

Use generated images for illustrations, backgrounds and textures only, never to fake a
product screen. Every generation uses Higgsfield credits.

## 7. A narrated explainer, synced to the voice

1. Write a few lines into `videos/<slug>/script.txt`.
2. Make the voice (step 5). `transcript.json` now knows when every word is spoken.
3. Ask:

```
> Build a narrated explainer in videos/<slug> from script.txt and narration.wav, 16:9.
  Reveal each command card on the word where the voice says it, using transcript.json.
  Put assets/<your-image>.png behind the title. Render it when check passes.
```

The tutorial's example lives in `examples/git-undo-explainer/`: the five-line script and the
transcript the voice produced, so you can compare your timings with ours.

4. Render, then `/review` it.

## 8. /brag: a launch video in one command

[brag](https://github.com/latent-spaces/brag) is a Claude Code plugin that reads a project and
makes a short launch video for it.

Install it from your terminal:

```bash
claude plugin marketplace add latent-spaces/brag
claude plugin install brag@brag
```

That installs it for every project. To keep it to one folder, run both commands inside that folder
with `--scope project`. A project-scoped plugin only loads when you start `claude` in that same
folder. (Inside Claude Code, `/plugin marketplace add latent-spaces/brag` and
`/plugin install brag@brag` open the plugin panel, where you pick the scope.)

Open the demo app and ask for a launch clip:

```bash
cd examples/demo-app
claude
```

```
> let's /brag about this, no music
```

On Claude Opus 5.5, brag switches to `/brag-slim`: it writes the whole launch video as one HTML
file, with no HyperFrames and no bundled assets. Ask for `/brag --full` when you want the
HyperFrames workflow from steps 3 to 7. The results land in `brag-output/` (`brag.mp4`, a poster
image, the plan and `share-copy.txt`).

## Rules worth keeping

- Lint after every edit; `npx hyperframes check videos/<slug>` before a final render.
- Renders go to `videos/<slug>/out/`; they are gitignored.
- No background music unless you want it. Narration and a few sound effects carry a video fine.

## License

MIT for the code in this repo. The fonts in `templates/*/assets/fonts/` are under the SIL Open
Font License (see the `OFL-*.txt` files next to them). GSAP is vendored under its own license
(header of `gsap.min.js`).
