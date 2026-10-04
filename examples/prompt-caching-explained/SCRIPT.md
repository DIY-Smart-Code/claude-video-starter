# SCRIPT — prompt-caching-explained

**Voice:** Sarah (ElevenLabs, EXAVITQu4vr4xnSDxMaL)
**Voice settings:** provider defaults (scripts/tts.py)
**Voice direction:** Calm, precise, a little dry — a senior dev explaining something over coffee. No hype.
**Written for the ear:** commas and full stops only (no dashes); CLAUDE.md is spoken as "Claude M D"; numbers spelled the way they are said.
**Audio:** narration.wav (96.64s), split per frame into assets/voice/NN.wav; times below are real.

---

## Line 1 — Every enter, from the top (Frame 1)

**Time:** 0.00 – 7.00s
**Delivery:** Even, let each cue land.

    Every time you press enter in Claude Code, Claude reads your whole session again. From the very first line.

## Line 2 — What gets re-sent (Frame 2)

**Time:** 7.00 – 19.36s
**Delivery:** Even, let each cue land.

    Your system prompt. Your Claude M D. Every message, every tool result. Then your new line, tacked on the end. Most of every request is text Claude has already read.

## Line 3 — The take (Frame 3)

**Time:** 19.36 – 26.12s
**Delivery:** Even, let each cue land.

    So most of what you pay for is the re-read. Prompt caching is the kitchen where the prep is already done.

## Line 4 — The empty kitchen (no cache) (Frame 4)

**Time:** 26.12 – 36.04s
**Delivery:** Even, let each cue land.

    Without a cache, every order starts cold. Chop the onions, make the stock, read every ticket again. All that, just to plate one new dish.

## Line 5 — The prepped kitchen (cache write) (Frame 5)

**Time:** 36.04 – 42.52s
**Delivery:** Even, let each cue land.

    With caching, the first request does the prep once and leaves it on the counter. That's a cache write.

## Line 6 — The serving kitchen (cache hit) (Frame 6)

**Time:** 42.52 – 48.44s
**Delivery:** Even, let each cue land.

    Next order, the prep is waiting. Claude only cooks what's new. That's a cache hit.

## Line 7 — It matches from the top (Frame 7)

**Time:** 48.44 – 58.64s
**Delivery:** Even, let each cue land.

    But the match is exact, and it starts at the top. Change the conversation, and the prep stays. Change something above it, and everything below gets cooked again.

## Line 8 — The price (Frame 8)

**Time:** 58.64 – 69.96s
**Delivery:** Even, let each cue land.

    Here's the price. Normal input costs one times. Writing the cache, one and a quarter. Reading it, one tenth. On Opus five point five, one twentieth.

## Line 9 — Prep doesn't keep forever (Frame 9)

**Time:** 69.96 – 78.32s
**Delivery:** Even, let each cue land.

    Prep doesn't keep forever. The cache lives five minutes. On a Claude subscription, an hour. And every hit resets the clock.

## Line 10 — What spoils the prep (Frame 10)

**Time:** 78.32 – 89.18s
**Delivery:** Even, let each cue land.

    Mid-task, three things throw the prep out: switching models, turning on fast mode, and compacting. So pick your model at the start, and compact between tasks.

## Line 11 — Check your kitchen (Frame 11)

**Time:** 89.18 – 93.04s
**Delivery:** Even, let each cue land.

    Then run slash usage, and read the prompt cache line.

## Line 12 — Read once (Frame 12)

**Time:** 93.04 – 96.64s
**Delivery:** Even, let each cue land.

    Read the context once. Cook only what's new.
