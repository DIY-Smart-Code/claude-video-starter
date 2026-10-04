# Example: Prompt caching, explained

The explainer built in the DIY Smart Code tutorial, exactly as Claude Code left it after the run
(2026-10-04): 12 frames, 1:37, engraving plates from Higgsfield, voiced with the ElevenLabs stock
voice Sarah.

| File | What it is |
|---|---|
| `BRIEF.md` | the brief `/hyperframes` wrote from the first prompt and the three answers |
| `SCRIPT.md` | the narration, one line per frame, written for the ear |
| `fact-check.md` | one row per claim, with the sentence from the docs it rests on |
| `frame.md` | the design system: the code-editorial preset remixed onto cream, ink and clay |
| `STORYBOARD.md` | the plan per frame, plus every change made after review |
| `storyboard.html` | the sketch sheet that was reviewed before the build (shows the planned layouts; `STORYBOARD.md` logs the later changes) |
| `assets/art/` | the five Higgsfield generations (three kept, two rejected) and `ledger.jsonl` with every prompt and job ID |
| `narration.wav`, `transcript.json`, `assets/voice/` | the ElevenLabs narration, its word timings, and the per-frame clips |
| `index.html`, `compositions/frames/` | the built video, one composition per frame |

Render it yourself from the repo root:

```bash
npx hyperframes render examples/prompt-caching-explained -o examples/prompt-caching-explained/out/prompt-caching-explained.mp4
```

Sources the facts were checked against:
[Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and
[Prompt caching in Claude Code](https://code.claude.com/docs/en/prompt-caching). Prices and cache
lifetimes are as of 2026-10-04.

The plates were generated for this example; reuse them for learning, and make your own for your videos.
