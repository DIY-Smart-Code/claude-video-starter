# Example: Prompt caching, the kitchen

The explainer built in the DIY Smart Code tutorial, exactly as Claude Code left it after the run
(2026-10-05/06): 13 frames, 1:59, engraving plates from Higgsfield, voiced with the ElevenLabs stock
voice Sarah. It went through five `/video-review` rounds; the fifth scored 8 or higher in every category.

| File | What it is |
|---|---|
| `BRIEF.md` | the brief `/hyperframes` wrote from the first prompt and the answers |
| `SCRIPT.md` | the narration, one line per frame, written for the ear |
| `fact-check.md` | one row per claim (19), with the sentence from the docs it rests on, and what was left out |
| `frame.md` | the design system: the code-editorial preset remixed onto cream, ink and clay |
| `STORYBOARD.md` | the plan per frame, plus every change made after review |
| `storyboard.html` | the sketch sheet that was reviewed before the build (shows the planned layouts; `STORYBOARD.md` logs the later changes) |
| `assets/art/` | the nine Higgsfield generations (four kept, five rejected) and `ledger.jsonl` with every prompt, job ID and rejection reason |
| `narration.wav`, `transcript.json`, `assets/voice/` | the ElevenLabs narration, its word timings, and the per-frame clips |
| `index.html`, `compositions/frames/` | the built video, one composition per frame |

Render it yourself from the repo root:

```bash
npx hyperframes render examples/prompt-caching-kitchen -o examples/prompt-caching-kitchen/out/prompt-caching-kitchen.mp4
```

Sources the facts were checked against:
[Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and
[Prompt caching in Claude Code](https://code.claude.com/docs/en/prompt-caching). Prices and cache
lifetimes are as of 2026-10-05.

The plates were generated for this example; reuse them for learning, and make your own for your videos.
