---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Most of your Claude Code bill is Claude re-reading the same context. Prompt caching is the kitchen where the prep is already done."
destination: youtube
aspect: 1920x1080
language: en
audience: "Developers who use Claude Code"
length: 120s
angle: concept
voice: elevenlabs (from .env)
---

## Intent

A 2-minute concept explainer about prompt caching for developers who use Claude Code.
User's take, verbatim: "most of your Claude Code bill is Claude re-reading the same context, and
caching is the kitchen where the prep is already done. The idea scenes use that kitchen as
illustrations; the numbers stay diagrams."

Collaborative: plan, then storyboard.html sketch sheet, confirmed before any build.

## Assets

- No user material. Sources only:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
  - https://code.claude.com/docs/en/prompt-caching

## Customizations

- Look: cream paper #F4F1EA, charcoal ink #1A1815, one clay accent #C15F3C.
  Playfair Display headlines, Inter body, JetBrains Mono labels.
- Idea scenes: kitchen illustrations via /art-direction (Higgsfield). Numbers, tables, mechanics stay HTML diagrams.
- Cost figures count up, landing on the start time of the word that says them (from transcript.json).
- Every number in the script verified against the two sources in fact-check.md.

## Notes

- Voice: ElevenLabs via `python scripts/tts.py videos/prompt-caching-kitchen` (voice from .env, never --voice).
- No music, no SFX.
- Fonts from local @font-face files only; GSAP local.
- Length 2:00 kept by the user despite 12% weekly usage left (2026-10-05); stop cleanly at milestones if usage runs low.
- Fresh build; do not copy examples/prompt-caching-explained (fonts may be reused).
