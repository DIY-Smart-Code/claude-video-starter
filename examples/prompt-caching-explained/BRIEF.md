---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Most of your Claude Code bill is Claude re-reading the same context — prompt caching is the kitchen where the prep is already done."
destination: youtube
aspect: 1920x1080
language: en
audience: "Developers who use Claude Code"
length: 97s
angle: concept
voice: elevenlabs:EXAVITQu4vr4xnSDxMaL
---

## Intent

A 2-minute narrative concept explainer about prompt caching for developers who use Claude Code.
User's take, verbatim: "most of your Claude Code bill is Claude re-reading the same context, and
caching is the kitchen where the prep is already done. The idea scenes use that kitchen as
illustrations; the numbers stay diagrams."

Arc: problem (you pay for re-reading) → metaphor (the prep kitchen) → mechanism (prefix,
breakpoints, cache lifetime) → numbers (write vs read cost) → what to do in Claude Code.

Collaborative: plan, then storyboard.html sketch sheet, confirmed before any build.

## Assets

- No user material. Sources only:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
  - https://code.claude.com/docs/en/prompt-caching

## Customizations

- Look: cream paper #F4F1EA, charcoal ink #1A1815, one clay accent #C15F3C.
  Playfair Display headlines, Inter body, JetBrains Mono labels.
- Idea scenes: kitchen illustrations via /art-direction (Higgsfield). Numbers, tables, mechanics stay HTML diagrams.
- ONE recurring kitchen across the idea scenes, evolving in three states: empty → prepped → serving.
- Cost comparison as animated data: counts/bars land on the word that names them.
- Fact-check: every number in SCRIPT.md verified against the two sources in fact-check.md.

## Notes

- Voice: ElevenLabs EXAVITQu4vr4xnSDxMaL via `python scripts/tts.py videos/prompt-caching-explained`.
- No music. No SFX unless asked.
- Fonts from local @font-face files only (Playfair Display + Inter 400 to be added to assets/fonts/).
- Length confirmed by user at ~1:37 (narration 96.6s; video = audio length).
- (Original plan:) 2:00 is above the 30–90s sweet spot, inside the ~3 min cap; plan ~10–12 frames.
