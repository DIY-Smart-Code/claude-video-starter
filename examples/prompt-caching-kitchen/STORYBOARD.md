---
format: 1920x1080
duration: 120s
message: "Most of your Claude Code bill is Claude re-reading the same context. Prompt caching is the kitchen where the prep is already done."
arc: concept-explainer with process
audience: Developers who use Claude Code
mode: collaborative
music: none
---

# Storyboard — prompt-caching-kitchen (v1.2)

## Decisions

- **Message:** Most of your Claude Code bill is Claude re-reading the same context; caching is the kitchen where the prep is already done.
- **Arc:** hook (re-reading) → the problem (everything, again) → metaphor (cold kitchen → prepped kitchen) → mechanism (prefix → price → worked example → stack order) → what breaks it (new chef, prep goes cold) → what's safe → habits → callback close.
- **Format:** 16:9 1920×1080, ~2:00, ElevenLabs voiceover, no music, no SFX, no captions (key terms are on-screen type).
- **Spine:** one kitchen. It appears cold (03), prepped (04), disturbed by a new chef (09) and serving (13). Between the kitchen beats, one recurring diagram — **the request bar** (a horizontal stack of segments: system · tools · CLAUDE.md · messages · new turn) — grows and gets coloured: ink = re-processed, clay = new, hatched/light = read from cache. It debuts in 02 and returns in 05, 07, 08.
- **Brand:** cream paper `#F4F1EA` canvas, charcoal ink `#1A1815` type and diagrams, clay `#C15F3C` as the single accent (only the "new / cost" thing in each frame). Playfair Display headlines and numbers, Inter body, JetBrains Mono labels. (`frame.md`, preset code-editorial remixed onto these tokens.)
- **Illustrations vs diagrams:** frames 03, 04, 09, 13 are kitchen illustrations (`/art-direction`, Higgsfield, one locked style). Every number, the bar, the stack, the timers and the lists stay HTML.
- **Bans:** no glow, no gradients, no fake Claude Code UI screenshots, no blinking cursor, no pulsing loops, no dollar figures (model prices vary; we count tokens), no static end card.
- **Motion failures to avoid:** the slideshow (each beat a fresh unrelated card) — answered by the recurring request bar; the screensaver (drift that says nothing) — every move lands on a spoken word.
- **Held frame:** 13, the close — the serving kitchen holds while the last line lands.
- **Transitions:** `crossfade` into and out of kitchen frames, `push-slide LEFT` through the diagram run (05→08), `cut` for the hook and the list frames.

## Changes from v1

- v1.1: all in-frame labels and bar text raised to the 40px minimum (CLAUDE.md); frame 05 bar label shortened to "messages".
- v1.2 (user): "Frames 11 and 12 leave the right half of the frame empty. Make each list bigger and centre it so it fills the frame." → 11 is a centred headline over a large centred 2×2 check grid; 12 is a centred block of three large numbered rows.

## Locked

- Sketch sheet storyboard.html v1.2 confirmed by the user (2026-10-05). Layouts, copy and seams are locked for all 13 frames.

## Video direction

- **Palette (frame.md):** canvas cream #F4F1EA; ink #1A1815 for type, bars, diagrams; clay #C15F3C only on the single new/costly thing per frame. Cache-read state = light diagonal hatch (ink at ~12% on cream). No gradients, no glow, no heavy shadows.
- **Type (frame.md roles):** display / number-hero = Playfair Display; body = Inter; kicker / mono-label / code = JetBrains Mono. Every on-screen word is at least 40px (2.08cqw at 1920).
- **Motion grammar:** power3.out settles, 0.5-0.8s entrances, no bounce / overshoot / elastic. Each piece reveals on the start time of the word that names it; the frame-local times in each Scene line come from transcript.json, do not move them. First visible motion within 0.2s of the frame start. Something changes at least every 3s; once a frame resolves it holds still (no breathing, no pulsing, no blinking caret, no loops).
- **Illustration frames (03, 04, 09, 13):** the kept plate is an `<img>` (object-fit: cover) with ONE slow continuous push-in (scale 1.00 to 1.04) across the whole frame; the plate's empty left-third paper carries the type.
- **Request bar:** the recurring diagram (02, 05, 07, 08): a horizontal segmented bar, thin ink border, segments labelled in JetBrains Mono; ink fill = re-processed, hatch = read from cache, clay = new.
- **Held frames:** 13 (the close) holds after "warm."; 06 and 11 hold their last second still.
- **Negative list:** no slideshow (front-load then freeze), no screensaver (independent floating motion), no fake Claude Code UI, no dollar signs, no captions, no CDN fonts or scripts, no Math.random / Date.now / timers.

## Frame 1 — Re-reading

- scene: Typographic hook. "Writing code" sits small, then "re-reading" lands huge in clay.
- voiceover: "Most of your Claude Code bill isn't Claude writing code. It's Claude, re-reading."
- duration: 5.78s
- transition_in: cut
- status: animated
- src: compositions/frames/01-re-reading.html
- type: hook
- persuasion: Counterintuitive claim
- beat: Surprise + recognition

narrativeRole: Opens the gap: the bill isn't where you think it is.
keyMessage: Most of what you pay for is Claude reading things it already read.

- blueprint: kinetic-type-beats (Adapt)
- focal: the word "re-reading."
- roles: kicker "Your Claude Code bill" = supporting; "writing code" = supporting (dim, struck through); "re-reading." = foreground subject (clay italic, display-cover size)

Adapt: keep the statement-builds-across-beats signature; the payoff word lands in clay italic.
Scene 1 (0.0-2.4s): kicker "YOUR CLAUDE CODE BILL" fades up at 0.05 (left-aligned, upper third, rule-of-thirds).
Scene 2 (2.48-4.6s): "writing code" rises in on "writing" @2.48 (Playfair, ink at 55%); a strike line draws across it left to right on "code." @3.04 (svg-path-draw).
Scene 3 (4.64-5.78s): "re-reading." lands on its word @4.64, clay italic, near full width (~12cqw), rising 30px with power3; holds still to the end.

## Frame 2 — Everything, again

- scene: The request bar debuts. Segments stack left to right as each is named: "system prompt", "CLAUDE.md", "messages", "tool results", then a small clay "new". Above it, turn 2, 3, 4 bars stack, each a copy of the last plus a sliver.
- voiceover: "Every time you send a message, Claude Code sends everything again. The system prompt. Your Claude dot M D. Every message, every tool result. Then your new line."
- duration: 11.9s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-everything-again.html
- type: pain_point
- persuasion: Progressive disclosure + Concretization
- beat: Recognition + mild unease

narrativeRole: Shows the mechanism behind the hook: every turn re-sends the whole history, and the new part is a sliver.
keyMessage: Each request is mostly a copy of the previous one.

- blueprint: compose
- focal: the request-bar rows growing turn by turn
- roles: three request-bar rows = foreground subject; kicker = supporting; turn labels = supporting

Scene 1 (0.14-4.3s): kicker "EVERY MESSAGE, EVERYTHING AGAIN" fades up @0.14; the turn-1 label and empty bar outline draw @1.02 (left-aligned stack, rows fill ~60% of frame height).
Scene 2 (4.38-7.6s): segments fill the turn-1 bar one per spoken name: "system prompt" @4.38, "CLAUDE.md" @5.9, each sliding in from the left (stat-bars-and-fills).
Scene 3 (7.62-10.3s): the turn-2 row copies the row above (its ink segments slide down) and adds "messages" @7.62; the turn-3 row copies and adds "tool results" @8.94.
Scene 4 (10.3-11.9s): the small clay "new" sliver lands at the end of each row in a quick top-to-bottom stagger starting on "new" @10.86; hold.

## Frame 3 — The cold kitchen

- scene: Illustration: a kitchen at the end of an order, prep being scraped into the bin, a cook starting over with whole onions. Mono label "no cache" top-left.
- voiceover: "Picture a kitchen that throws out its prep after every order. Chop the onions again. Make the stock again. Every single time."
- duration: 8.8s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-cold-kitchen.html
- art: assets/art/03-cold-kitchen-3.png — kept Higgsfield plate (engraving, 2752×1536); subject on the right two-thirds, empty paper left third
- type: pain_point
- persuasion: Analogy / metaphor
- beat: Wry frustration

narrativeRole: Turns the abstract re-read into a felt waste.
keyMessage: Without caching, every turn re-does all the prep.

- blueprint: compose
- focal: the cold-kitchen plate
- roles: plate assets/art/03-cold-kitchen-3.png = full-bleed background (undimmed); kicker "NO CACHE" = supporting; headline = foreground type in the left third

Scene 1 (0.0-3.7s): plate visible from 0 with the slow push-in for the whole frame; kicker "NO CACHE" fades up @0.44 ("kitchen"), left third, upper area.
Scene 2 (3.72-6.9s): headline "Every order," rises in on "Chop" @3.72 (Playfair ~5cqw, left third, lower half, on the plate's empty paper; a cream chip behind it only if contrast needs it).
Scene 3 (6.96-8.8s): "from scratch." lands in clay on "Every" @6.96; hold to the end.

## Frame 4 — The prepped kitchen

- scene: Illustration: same kitchen, mise en place ready in bowls, one cook making only the new plate. Title "Prompt caching" in Playfair, mono label "cache hit".
- voiceover: "Prompt caching is the kitchen where the prep is already done. The cook keeps it, and only makes what's new."
- duration: 6.52s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-prepped-kitchen.html
- art: assets/art/04-prepped-kitchen-2.png — kept Higgsfield plate (engraving, 2752×1536); subject on the right two-thirds, empty paper left third
- type: product_intro
- persuasion: Analogy / metaphor + Before/after
- beat: Relief + clarity

narrativeRole: Names the concept and lands the message's second half.
keyMessage: Caching keeps the prep so only the new part is made.

- blueprint: titlecard-reveal (Adapt)
- focal: the title "Prompt caching"
- roles: plate assets/art/04-prepped-kitchen-2.png = full-bleed background whose empty left third carries the type; kicker = supporting; title = foreground subject; body line = supporting

Adapt: keep the title-lands-then-subline signature. The sketch had a split panel; the plate's own empty left paper now plays the left panel, with the same type placement.
Scene 1 (0.0-1.0s): plate in with slow push-in; kicker "CACHE HIT" (clay mono) fades up @0.08.
Scene 2 (0.08-3.7s): "Prompt caching" lands on "Prompt" @0.08 (Playfair ~6.4cqw, two lines, left third, vertically centred), per-word rise ("caching" @0.32).
Scene 3 (3.8-6.52s): body line "The prep is already done." fades up on "cook" @3.8; "Only the new is made." follows on "only" @4.96 with "new" in clay; hold.

## Frame 5 — The prefix

- scene: The request bar returns, two rows: previous request and this request. A bracket spans the identical start labelled "prefix". It fills with a light hatch "read from cache"; only the clay tail is "processed fresh".
- voiceover: "Here's how. The cache matches the start of each request, the prefix. If the start is identical, it's read from cache. Only the newest turn is processed fresh."
- duration: 10.6s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-prefix.html
- type: feature_showcase
- persuasion: Demonstration + Signposting
- beat: Comprehension

narrativeRole: Shows the actual mechanism: exact match on the start of the request.
keyMessage: Same start → read from cache; only the new end costs full work.

- blueprint: comparison-split (Adapt)
- focal: the "this request" bar turning to cache hatch
- roles: two request-bar rows = foreground subject; bracket and labels = supporting; kicker = supporting

Adapt: keep the two-states-compared signature as two stacked bars (previous vs this) instead of side-by-side cards.
Scene 1 (0.04-1.7s): kicker "MATCHED ON THE START" @0.04; the "previous request" row (ink segments: system, CLAUDE.md, messages) slides in @0.28.
Scene 2 (1.76-4.2s): the "this request" row (same ink segments plus a clay "new") slides in under it on "matches" @1.76.
Scene 3 (4.24-7.7s): the bracket draws under the identical start on "prefix." @4.24 (svg-path-draw) with mono label "prefix -> read from cache"; on "read" @6.52 the matched segments wipe from ink to cache hatch, left to right.
Scene 4 (7.8-10.6s): on "Only" @7.8 the clay tail's label "fresh" appears under it; hold.

## Frame 6 — The price

- scene: Two price tiles on a baseline "normal input = 1×": "cache read 0.1×" counts down from 1.0 on "one tenth"; "cache write 1.25×" counts up on "a quarter more", with mono tag "once".
- voiceover: "And reading is cheap. A cache read costs one tenth of normal input. Writing it costs a quarter more, once."
- duration: 8s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-price.html
- type: social_proof
- persuasion: Statistical proof + Comparison of two options
- beat: "Aha"

narrativeRole: Gives the mechanism its stakes in numbers.
keyMessage: Reading from cache costs a tenth; writing costs a little extra, once.

- blueprint: dataviz-countup (Reproduce)
- focal: the two multiplier numbers
- roles: two price tiles = foreground subject (split 50/50); kicker "PRICE PER TOKEN, VS NORMAL INPUT = 1x" = supporting

Scene 1 (0.03-1.9s): kicker fades up @0.03; both tile frames draw in @0.16 showing "1.0x" in ink at 30%.
Scene 2 (1.92-4.9s): read tile label "cache read" @1.92; its number counts 1.0x down to 0.1x from "one" @2.96, landing on "tenth" @3.28; caption "one tenth" appears @3.28.
Scene 3 (4.96-8.0s): write tile (clay) label "cache write" @4.96; counts 1.0x up to 1.25x landing on "quarter" @6.0; caption "a quarter more" @6.0; mono "once" stamps in @7.12; hold.

## Frame 7 — Forty turns

- scene: Worked example. Header in mono: "100,000-token context × 40 turns (illustrative)". Two horizontal bars: "without caching" counts up to "4,000,000" full-price tokens on "four million"; "with caching" counts up to "≈ 515,000" on "five hundred fifteen thousand", its bar a short clay stub.
- voiceover: "Say your context is a hundred thousand tokens, over forty turns. Without caching, that's four million full price tokens. With caching, about five hundred fifteen thousand."
- duration: 11.34s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/07-forty-turns.html
- type: social_proof
- persuasion: Worked example with real numbers
- beat: Surprise + conviction

narrativeRole: Proves "most of your bill is re-reading" with arithmetic the viewer can follow.
keyMessage: Caching turns 4,000,000 full-price tokens into about 515,000.

- blueprint: dataviz-countup (Reproduce)
- focal: the two token totals
- roles: two horizontal bars with their numbers = foreground subject; header line = supporting; row labels = supporting

Scene 1 (0.32-4.4s): mono header "100,000-token context x 40 turns" types in chunk by chunk from "context" @0.32 (no caret); "(illustrative)" appears on "forty" @3.0.
Scene 2 (4.43-8.0s): row label "without caching - full-price tokens" @4.43; the ink bar grows to ~66% width while its number counts up from 0, landing exactly on 4,000,000 at "four" @5.76.
Scene 3 (8.08-11.34s): row label "with caching - full-price equivalent" @8.08; a short clay bar grows to ~8.5% while "≈ 515,000" counts up, landing on "five" @9.36; hold.

## Frame 8 — Order matters

- scene: The request bar turned vertical as a stack of three layers, revealed top-down: "System prompt + tools", "Project context — CLAUDE.md", "Conversation". Then the top layer flips to clay and a downward wash marks everything below "re-processed".
- voiceover: "Order matters. Claude Code stacks it from the top. System prompt and tools. Then project context. Then the conversation. Change something near the top, and everything below it gets cooked again."
- duration: 12.9s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/08-order-matters.html
- type: feature_showcase
- persuasion: Frame-then-fill + Causal chain
- beat: Foresight

narrativeRole: Explains why some actions cost a full re-read and others don't.
keyMessage: A change near the top invalidates everything beneath it.

- blueprint: compose
- focal: the three-layer stack and its top layer turning clay
- roles: layer stack (left ~55%) = foreground subject; headline (right column) = foreground type; kicker = supporting

Scene 1 (0.02-3.5s): kicker "ORDER MATTERS" @0.02 (right column); the empty stack frame appears on "stacks" @2.02.
Scene 2 (3.54-8.9s): layers drop in top-down, each on its name: "System prompt + tools" @3.54, "Project context - CLAUDE.md" @5.78, "Conversation" @7.62 (all ink).
Scene 3 (9.03-12.9s): on "Change" @9.03 the top layer turns clay and the headline "Change the top," rises in; on "everything" @10.66 an ink wash runs down the layers below with mono tag "re-processed"; "re-cook everything below." lands on "cooked" @11.86 with "re-cook" in clay; hold.

## Frame 9 — The new chef

- scene: Illustration (left 55%): a new chef in the doorway, the prep tray being cleared. Right column: a list revealing one chip per spoken item: "/model", "effort*", "fast mode", "/compact", "upgrade". Footnote "* on most models". Tag "= one slow, full-price turn".
- voiceover: "That's what a new chef does. Switching models. Changing effort, on most models. Turning on fast mode. Running slash compact. Upgrading Claude Code. Each one costs a slow, full price turn."
- duration: 13.74s
- transition_in: crossfade
- status: animated
- src: compositions/frames/09-new-chef.html
- art: assets/art/09-new-chef-3.png — kept Higgsfield plate (engraving, 2752×1536); subject on the right two-thirds, empty paper left third
- type: feature_showcase
- persuasion: Callback to the metaphor + Numbered enumeration
- beat: Recognition + unease

narrativeRole: Names the everyday actions that throw the prep away.
keyMessage: Model, effort, fast mode, compact and upgrades each trigger one full re-read.

- blueprint: compose
- focal: the list of cache-breakers
- roles: plate assets/art/09-new-chef-3.png in the left 55% panel (object-fit cover, object-position ~78% center so the new chef and the tray are in view) = illustration; list column (right 45%, cream) = foreground subject; sum line = supporting

Scene 1 (0.0-1.7s): plate panel visible with the slow push-in; kicker "THROWS OUT THE PREP" fades up on "new" @0.48.
Scene 2 (1.76-10.6s): one list row per spoken item, each sliding up 20px: "/model" @1.76, "effort*" @3.39, "fast mode" @5.57, "/compact" @7.12, "upgrade" @9.12 (JetBrains Mono, at least 2.6cqw).
Scene 3 (10.64-13.74s): clay sum "= one slow, full-price turn" lands on "slow," @11.84; footnote "* on most models" fades in @12.4; hold.

## Frame 10 — Prep goes cold

- scene: Two timer bars on one time axis. "API key — 5 min" a short bar; "Subscription (main conversation) — 1 h" a long bar. Mono note "each use resets the timer". Bars draw on their spoken durations.
- voiceover: "Prep also goes cold. With an A P I key, the cache lasts five minutes without use. On a subscription, Claude Code keeps your main conversation warm for an hour."
- duration: 10.88s
- transition_in: crossfade
- status: animated
- src: compositions/frames/10-prep-goes-cold.html
- type: feature_showcase
- persuasion: Comparison of two options
- beat: Comprehension

narrativeRole: Adds the time dimension: idle long enough and the cache expires.
keyMessage: The cache expires after 5 minutes idle on an API key, 1 hour on a subscription.

- blueprint: dataviz-countup (Adapt)
- focal: the two timer bars
- roles: two bars with values = foreground subject; kicker = supporting; note = supporting

Adapt: keep the bar-fills-to-a-value signature; the values are durations, not counts.
Scene 1 (0.02-1.9s): kicker "PREP GOES COLD - TIME TO LIVE" @0.02.
Scene 2 (1.97-5.9s): "API key" label @1.97; a short ink bar draws to ~9% and "5 min" lands on "five" @4.34; the note "each use resets the timer" fades in under the rows on "use." @5.3.
Scene 3 (5.99-10.88s): "subscription - main conversation" label @5.99; the clay bar sweeps long to ~66% starting on "main" @8.38 and finishing as "1 h" lands on "hour." @10.1; hold.

## Frame 11 — What's safe

- scene: Centred headline "Keeps the cache" over a large centred 2×2 grid of ink check items, revealing one per spoken item: "Editing files", "Skills", "Permission modes", "/rewind".
- voiceover: "The good news. Editing files, using skills, switching permission modes, and slash rewind all keep the cache."
- duration: 7.68s
- transition_in: cut
- status: animated
- src: compositions/frames/11-whats-safe.html
- type: benefit_highlight
- persuasion: Counterexample + Rule of enumeration
- beat: Relief

narrativeRole: Removes the fear that everything breaks the cache.
keyMessage: Normal work (edits, skills, modes, rewind) keeps the cache warm.

- blueprint: kinetic-type-beats (Adapt)
- focal: the 2x2 check grid
- roles: headline = foreground type (centred); four check items = foreground subject (large centred 2x2 grid, as in the confirmed sketch)

Adapt: the statement builds one grid cell per spoken item; ink only, no clay.
Scene 1 (0.02-1.3s): headline "Keeps the cache" rises in centred on "The" @0.02.
Scene 2 (1.33-6.1s): grid cells slide up one per spoken item: "Editing files" @1.33, "Skills" @2.18, "Permission modes" @3.38, "/rewind" @5.06 (left to right, top to bottom).
Scene 3 (6.18-7.68s): the four check marks thicken to bold ink together on "all" @6.18; hold still.

## Frame 12 — Habits

- scene: A large centred block of three numbered habits filling the frame, one per spoken beat: "1  Pick model + effort first", "2  /compact between tasks", "3  Check hit rate: /usage" — the last in a mono command chip with "Prompt cache (main)" label.
- voiceover: "So pick your model and effort before you start. Compact between tasks, not in the middle. And check your hit rate with slash usage."
- duration: 8.24s
- transition_in: cut
- status: animated
- src: compositions/frames/12-habits.html
- type: cta
- persuasion: Rule of three + Distillation
- beat: Resolve

narrativeRole: Turns understanding into three things to do tomorrow.
keyMessage: Choose model/effort up front, compact at breaks, watch /usage.

- blueprint: kinetic-type-beats (Adapt)
- focal: the three numbered habits
- roles: centred block of three rows = foreground subject; clay numerals = supporting

Scene 1 (0.02-2.8s): row 1 "1  Pick model + effort first" rises in on "So" @0.02, numeral first, text 0.1s after.
Scene 2 (2.9-5.7s): row 2 "2  /compact between tasks" rises in on "Compact" @2.9.
Scene 3 (5.73-8.24s): row 3 numeral @5.73; the ink chip appears and types "/usage" chunk-wise on "slash" @6.98 (no caret), then "-> Prompt cache (main)" slides out of it on "usage." @7.38; hold.

## Frame 13 — Keep the kitchen warm

- scene: Illustration: the prepped kitchen serving, plates going out, warm light. Line in Playfair: "Keep the kitchen warm." Held.
- voiceover: "Keep the kitchen warm, and you only pay to cook what's new."
- duration: 3.46s
- transition_in: crossfade
- status: animated
- src: compositions/frames/13-keep-it-warm.html
- art: assets/art/13-serving-kitchen-1.png — kept Higgsfield plate (engraving, 2752×1536); subject on the right two-thirds, empty paper left third
- type: branding
- persuasion: Callback + Distillation
- beat: Satisfaction

narrativeRole: Closes on the hook's image, resolved.
keyMessage: Keep the cache warm and you pay only for what's new.

- blueprint: titlecard-reveal (Reproduce)
- focal: the line "Keep the kitchen warm."
- roles: plate assets/art/13-serving-kitchen-1.png = full-bleed background with very slow push-in; title chip (left third, lower area) = foreground subject

Scene 1 (0.0-0.7s): plate in with the slow push-in; "Keep the kitchen" rises in on "Keep" @0.02 (Playfair ~6cqw, on the empty left paper).
Scene 2 (0.74-3.46s): "warm." lands in clay italic on "warm," @0.74; subline "Pay only to cook what's new." fades up on "only" @1.7; holds to the end (the video's held close).

