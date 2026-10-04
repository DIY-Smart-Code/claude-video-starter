---
format: 1920x1080
duration: 97s
message: "Most of your Claude Code bill is Claude re-reading the same context — prompt caching is the kitchen where the prep is already done."
arc: concept-explainer with process
audience: Developers who use Claude Code
mode: collaborative
music: none
style_preset: code-editorial
---

Structure: **concept-explainer with process.** Hook on the re-read → thesis by beat 3 → the kitchen
(empty → prepped → serving) names the idea → mechanism (prefix rule) → evidence (price, lifetime) →
what spoils the prep → how to check. Hook strategy: **counterintuitive claim / direct address.**

Illustration frames (04, 05, 06) share ONE kitchen, same camera, same counter, from /art-direction.
Everything with a number, a layer, or a command stays HTML.

Transitions: `cut` (type beats), `crossfade` (inside the kitchen run), `push-slide LEFT` (diagram run).

## Changes from plan v1

- User: "write the spoken lines for the ear, with commas or full stops instead of dashes, and CLAUDE.md spoken as Claude" — voiceovers rewritten; CLAUDE.md is spoken as "Claude M D"; "Opus 5.5" spoken as "Opus five point five". On-screen text keeps CLAUDE.md / 5.5.

- Sheet v2, user: "Frame 11 has too much text on screen. Cut it to the /usage card and let the voice say the two habits." Habit lines removed from screen; the card is the only element. Voiceover unchanged.

## Changes from render v1 (/review)

- User: "Yes, apply all three." (1) habits moved from frame 11 into frame 10 (cut moved to "Then" at 89.18s; 10 = 10.86s, 11 = 3.86s); rows light on the spoken habits. (2) frame 01: hook visible at t=0, read bar thicker and moved under the headline. (3) frame 10: display headline, larger rows spread through the lower two-thirds.

## Changes from render v2 (/review)

- User: "Yes, apply all three." (1) frame 03: "You pay for *the re-read.*" builds on the spoken words (0.8–1.92s) in the quote's slot, then scale-swaps out as the quote rises in on "Prompt" (3.12s) — no more 3s near-empty stretch. (2) frame 09: timeline moved to the frame's middle and enlarged (ticks 72px, 5-min window 96px tall, labels 48px; the 1 h label stays 40px to fit the pad). (3) frame 08: bars 340px wide at x 118/568/1018 so the chart spans the frame; the "Opus 5.5 read / 0.05×" footnote sits beside the 0.1× bar (two lines).

## Locked

- Sketch sheet v2 (`storyboard.html`) confirmed by the user ("Looks right. Go on."): every frame's layout, hierarchy and on-screen copy. The build dresses these layouts and never redraws them.
- Narration (SCRIPT.md, 248 words), written for the ear.

## Video direction

- **Palette (frame.md, by role):** ground cream `#F4F1EA`; all type, bars and hairlines in ink `#1A1815` (tints of ink for secondary bars and labels); clay `#C15F3C` is the ONE voltage per frame, on the thing the line is about (the new slice, "prep", the read bar, the 5-min window, the index numbers). Clay tint `#F3E0DA` only as the fill behind a clay-outlined layer (frame 07). Navy `#181615` only for the /usage card (frame 11).
- **Type (frame.md):** Playfair Display 400 for headlines and hero figures (italic for the emphasised word); Inter for short supporting copy; JetBrains Mono 500 for labels, kickers (with the clay ✱) and commands. Project floor: nothing under 40px on the 1920×1080 canvas.
- **Motion grammar:** smooth long-tail settles (`power3`), no bounce, no overshoot. Every piece enters with `fromTo` on the word that names it (cue times below are seconds from the frame's own start, read from transcript.json). Nothing front-loads; a frame shows only what the voice is saying at t=0.
- **Held frames:** 03 (the take) and 12 (the close) hold still after their reveals. The kitchen frames (04–06) hold the plate still apart from one slow, constant push-in on the plate per frame (same speed in all three so the crossfades read as one camera). No breathing, no back-half pans.
- **Captions:** skipped (not requested; every frame carries its own on-screen headline). The approved sketch layout (bottom content down to y≈1000) stands; keep everything inside the 80px pad.
- **Plates (04–06):** the kept Higgsfield plate is a full-bleed background `class="clip"` layer (`object-fit: cover`, multiply-blended over the cream ground so its paper melts into `#F4F1EA`). The headline sits in the plate's empty left third, exactly where the sketch put it. The plate replaces the sketch's hatched panel.
- **Negative list:** no slideshow (everything up front, then frozen), no screensaver (many things drifting); no blinking or pulsing loops, no caret blink; no glow, gradients or second accent; no fake Claude Code UI and no invented /usage numbers; no narration sentences as on-screen text beyond the approved sketch copy; no exits except frame 12.

## Frame 1 — Every enter, from the top

- scene: One line of type; beneath it a thin request bar that re-draws from the left edge each time "enter" is said
- voiceover: "Every time you press enter in Claude Code, Claude reads your whole session again. From the very first line."
- duration: 7s
- transition_in: cut
- status: animated
- src: compositions/frames/01-every-enter.html
- type: hook
- persuasion: Counterintuitive claim + direct address
- beat: surprise + recognition

narrativeRole: Opens the gap — the viewer assumed Claude "remembers"; it re-reads.
keyMessage: Each turn is a full re-read of the session.

- blueprint: kinetic-type-beats (Adapt)
- focal: the headline "Every time you press enter, / Claude reads it all again."
- roles: headline = foreground subject · read bar (track + ink fill) with mono "line 1" / "↵ enter" labels = supporting · ✱ kicker = supporting

Adapt: keep the statement-builds-across-beats signature; the payoff is the read bar sweeping from line 1 instead of a logo.
Review fix (render v1, /review #2): frame 0 was blank and the frame was top-heavy with an empty middle. Now the kicker and "Every" are fully visible at t=0, and the read bar is thicker and sits under the headline (no longer at the bottom edge), so the frame fills top to middle.
Scene 1 (0.0–1.7s): cream ground; kicker "✱ CLAUDE CODE · EVERY TURN" and the word "Every" are already on screen at t=0; "time you press enter," arrives by **per-word staggered reveal** (`dynamic-content-sequencing`) from 0.0s, landing "enter," at 1.12s. Layout exactly as the sketch: kicker + two-line headline upper-left, bar strip at the bottom.
Scene 2 (1.7–4.6s): at "enter" 1.12s the empty bar track + "line 1" / "↵ enter" labels fade in; line 2 "Claude reads it all again." reveals per word from 2.72s; "all" (clay italic) lands on "whole" 3.6s.
Scene 3 (4.6–7.0s): on "From" 5.2s the ink fill sweeps the bar from the left edge to ~72% (`stat-bars-and-fills`, long-tail) and reaches it on "line." 6.24s; then holds still.

## Frame 2 — What gets re-sent

- scene: A request drawn as a horizontal stack — system prompt, CLAUDE.md, messages, tool results — then a small clay slice "your new line" appended at the end; three turns stack vertically, each longer
- voiceover: "Your system prompt. Your Claude M D. Every message, every tool result. Then your new line, tacked on the end. Most of every request is text Claude has already read."
- duration: 12.36s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/02-what-gets-resent.html
- type: pain_point
- persuasion: Progressive disclosure + concretization
- beat: recognition → concern

narrativeRole: Makes the re-read concrete — the old part dwarfs the new part.
keyMessage: The new part of each request is tiny; the repeated part is huge.

- blueprint: grid-card-assemble (Adapt)
- focal: the three growing request bars
- roles: turn bars (segments: system prompt ink, CLAUDE.md ink 72%, messages ink 48%, tool results ink 28%, new line clay) = foreground subject · headline "Most of it, Claude already read." = supporting (arrives last) · mono turn labels + legend = supporting

Adapt: keep the staggered self-assembly; the cards are bar segments assembling left-to-right, one per spoken name, then whole rows.
Scene 1 (0.0–2.8s): "turn 1" label + legend chip "■ system prompt" appear; the system-prompt segment of turn 1 grows from the left on "system" 0.2s (`stat-bars-and-fills`); the CLAUDE.md segment + its legend chip on "Claude" 1.48s. Layout as sketch: three rows at mid-frame, legend wraps along the bottom, headline zone top-left empty for now.
Scene 2 (2.8–5.6s): messages segment + chip on "message," 3.16s; tool-results chip on "tool" 4.28s (turn 1 has no tool segment, matching the sketch).
Scene 3 (5.6–8.3s): the small clay "your new line" segment snaps onto the end of turn 1 on "new" 6.28s with its clay legend chip; then turns 2 and 3 assemble (`grid-card-assemble` stagger, rows 2 then 3) on "tacked" 6.96s and "end." 7.48s, each longer than the last, each ending in the same small clay slice.
Scene 4 (8.3–12.36s): headline "Most of it, Claude *already read.*" (Playfair, "already read." clay italic) reveals per word on "Most" 8.36s through "read." 11.64s (`dynamic-content-sequencing`); then hold.

## Frame 3 — The take

- scene: Pull-quote in Playfair italic, the word "prep" in clay; ✱ kicker "THE IDEA"
- voiceover: "So most of what you pay for is the re-read. Prompt caching is the kitchen where the prep is already done."
- duration: 6.76s
- transition_in: cut
- status: animated
- src: compositions/frames/03-the-take.html
- type: branding
- persuasion: Analogy / metaphor (announced) + distillation
- beat: clarity

narrativeRole: Lands the value claim and introduces the metaphor the rest of the video lives in.
keyMessage: Caching = prep done once, reused every order.

- blueprint: titlecard-reveal (Reproduce)
- focal: the pull-quote "Caching is the kitchen where the prep is already done."
- roles: pull-quote (Playfair italic, display-italic scale) = foreground subject · "prep" in clay = the one accent · ✱ kicker "THE IDEA" + hairline rule = supporting

Scene 1 (0.0–3.1s): kicker "✱ THE IDEA" fades up on "So" 0.08s; the hairline rule draws left-to-right under where the quote will sit (`svg-path-draw`), finishing by "re-read." 1.92s. Layout as sketch: left-aligned, vertically centred block.
Scene 2 (3.1–5.1s): the quote slides up + crossfades in as one block on "Prompt" 3.12s (the blueprint's single restrained move); "prep" is ink at first.
Scene 3 (5.1–6.76s): on "prep" 5.08s the word "prep" warms from ink to clay (`css-marker-patterns`, a colour change only, no highlight box); then the HELD frame, completely still.

## Frame 4 — The empty kitchen (no cache)

- scene: ILLUSTRATION — the kitchen, empty counter, cold pans, a long ticket rail; headline in the empty third "Every order starts cold."
- voiceover: "Without a cache, every order starts cold. Chop the onions, make the stock, read every ticket again. All that, just to plate one new dish."
- duration: 9.92s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-empty-kitchen.html
- art: assets/art/04-empty-kitchen-2.png — kept plate (2752×1536, full-bleed cream; place as full-frame background, multiply-blend on #F4F1EA; left third is the headline zone)
- type: product_intro
- persuasion: Analogy + before/after (the before)
- beat: tension

narrativeRole: Names the cost of no caching in the kitchen's language.
keyMessage: Uncached = all the work, every time.

- blueprint: titlecard-reveal (Adapt)
- focal: plate A (the empty kitchen) with its single clay ticket
- roles: plate A = background full-bleed (multiply on cream, not dimmed: it is the subject) · headline "Every order starts *cold.*" = foreground (left third) · kicker "✱ NO CACHE" = supporting · ticket underline marks = supporting

Adapt: keep the single restrained title move; the "card" is the plate.
Scene 1 (0.0–2.3s): plate A fades up from cream over ~1s; a slow constant push-in on the plate starts (scale 1.00 to 1.04 over the whole frame, linear: the only camera move); kicker "✱ NO CACHE" on "cache," 0.64s. Headline zone in the left third as sketch.
Scene 2 (2.3–5.2s): "Every order starts" reveals per word from "every" 1.24s; "cold." (clay italic) lands on "cold." 2.28s.
Scene 3 (5.2–9.92s): on "read every ticket again" (5.24s to 6.36s) a thin ink underline ticks beneath the ticket rail from left to right in three steps (`css-marker-patterns`, ink not clay); then hold to the crossfade.

## Frame 5 — The prepped kitchen (cache write)

- scene: ILLUSTRATION — same kitchen, same camera; mise en place bowls lined up along the counter; mono label slides in "cache write"
- voiceover: "With caching, the first request does the prep once and leaves it on the counter. That's a cache write."
- duration: 6.48s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-prepped-kitchen.html
- art: assets/art/05-prepped-kitchen-1.png — kept plate (2752×1536, full-bleed cream; place as full-frame background, multiply-blend on #F4F1EA; left third is the headline zone)
- type: feature_showcase
- persuasion: Analogy + coined term (cache write)
- beat: orientation

narrativeRole: First move of the mechanism — the write.
keyMessage: The first request pays to prep, once.

- blueprint: titlecard-reveal (Adapt)
- focal: plate B (the prepped counter on its clay tray)
- roles: plate B = background full-bleed (multiply on cream) · headline "Prep it *once.*" = foreground (left third) · clay pill "cache write" = supporting (the label)

Scene 1 (0.0–2.3s): plate B shows from t=0 (it arrives through the crossfade from plate A; same framing, so the bowls appear to fill the counter); the same slow constant push-in (1.00 to 1.04, linear). Left third empty until the cue.
Scene 2 (2.3–4.8s): "Prep it *once.*" reveals per word on "prep" 2.36s / "once" 2.68s ("once." clay italic).
Scene 3 (4.8–6.48s): the clay pill `cache write` (mono, cream on clay) pops in with a smooth settle (`spring-pop-entrance`, no overshoot) on "cache" 5.4s; hold.

## Frame 6 — The serving kitchen (cache hit)

- scene: ILLUSTRATION — same kitchen, same camera; prep bowls in use, one fresh plate going out in the warm light; mono label "cache hit"
- voiceover: "Next order, the prep is waiting. Claude only cooks what's new. That's a cache hit."
- duration: 5.92s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-serving-kitchen.html
- art: assets/art/06-serving-kitchen-2.png — kept plate (2752×1536, full-bleed cream; place as full-frame background, multiply-blend on #F4F1EA; left third is the headline zone)
- type: feature_showcase
- persuasion: Analogy + before/after (the after)
- beat: "aha"

narrativeRole: Second move — the hit; the payoff of the metaphor.
keyMessage: Every later turn re-uses the prep and cooks only the new part.

- blueprint: titlecard-reveal (Adapt)
- focal: plate C, the clay plated dish
- roles: plate C = background full-bleed (multiply on cream) · headline "The prep is *waiting.*" = foreground (left third) · ink circle around the dish = supporting · clay pill "cache hit" = supporting

Scene 1 (0.0–0.9s): plate C shows from t=0 (arrives through the crossfade); same slow constant push-in (1.00 to 1.04, linear).
Scene 2 (0.9–4.5s): "The prep is *waiting.*" reveals per word from "the" 0.96s, "waiting." (clay italic) on 1.48s. On "only cooks what's new" (2.84s to 3.8s) a single ink hand-drawn circle draws around the plated dish (`css-marker-patterns` circle, ink stroke, `svg-path-draw` mechanics). The circle must sit on the dish: measured from the plate file, the clay dish spans x 1940–2452, y 1180–1376 of 2752×1536, which under object-fit cover on 1920×1080 is an ellipse centred ≈ (1536, 899), ≈ 360×138px; draw the circle a little larger than that, INSIDE the same wrapper that carries the push-in so it stays on the dish.
Scene 3 (4.5–5.92s): the clay pill `cache hit` pops in on "cache" 5.0s (`spring-pop-entrance`, smooth); hold.

## Frame 7 — It matches from the top

- scene: Three stacked layers (System prompt · Project context · Conversation); first a change in Conversation — only that layer re-cooks (clay); then a change in System prompt — the clay floods down through all three
- voiceover: "But the match is exact, and it starts at the top. Change the conversation, and the prep stays. Change something above it, and everything below gets cooked again."
- duration: 10.2s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/07-prefix-rule.html
- type: feature_showcase
- persuasion: Demonstration + causal chain
- beat: comprehension

narrativeRole: The one rule that explains every cache miss.
keyMessage: A change invalidates everything after it — order matters.

- blueprint: grid-card-assemble (Adapt)
- focal: the three stacked layers
- roles: layer cards "System prompt / Project context / Conversation" with mono sub-labels = foreground subject · headline "It matches from the *top.*" = supporting (top) · state tags (`cached` ink / `✎ changed` / `↻ re-read` clay) = supporting

Adapt: keep the staggered stack assembly; then a state change floods down the stack, the signature move of this frame.
Scene 1 (0.0–3.5s): headline reveals per word on "match" 0.52s through "top." 2.76s ("top." clay italic); the three layer cards (hairline ink outline on cream) assemble top-down on "starts at the top" 2.2–2.76s (`grid-card-assemble` stagger). Layout as sketch: headline top-left, stack full-width below.
Scene 2 (3.5–6.4s): on "conversation," 4.04s the Conversation card turns clay (clay outline + clay-tint fill) with tag `↻ re-read`; the two upper cards get an ink `cached` tag on "prep stays." 5.16s.
Scene 3 (6.4–10.2s): on "above" 7.08s the System prompt card turns clay with `✎ changed` (replacing `cached`); on "everything below" 8.04–8.6s the clay floods down: Project context then Conversation fill clay-tint in sequence, their tags flipping to `↻ re-read` (`discrete-text-sequence` hard swap); lands on "again." 9.68s. The end state is exactly the sketch.

## Frame 8 — The price

- scene: Bar chart on one baseline, bars grow on their word: Input 1× · Cache write 1.25× · Cache read 0.1×; then a small clay footnote bar "Opus 5.5: 0.05×"
- voiceover: "Here's the price. Normal input costs one times. Writing the cache, one and a quarter. Reading it, one tenth. On Opus five point five, one twentieth."
- duration: 11.32s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/08-the-price.html
- type: social_proof
- persuasion: Statistical proof + comparison of options
- beat: conviction

narrativeRole: Grounds the take in the real multipliers.
keyMessage: A small premium once, then reads at a tenth of the price or less.

- blueprint: dataviz-countup (Adapt)
- focal: the three price bars on one baseline
- roles: bars (input ink, cache write ink 50%, cache read clay) with Playfair figures + mono "×" units = foreground subject · mono column labels = supporting · kicker "✱ PRICE PER INPUT TOKEN" = supporting · footnote "Opus 5.5 read · 0.05×" = supporting

Adapt: keep the count-up signature (figures count up with their bars); no camera push-through, the bars carry it.
Scene 1 (0.0–2.8s): kicker on "price." 0.64s; the baseline hairline draws left-to-right (`svg-path-draw`); mono labels input / cache write / cache read sit under it from 1.6s.
Scene 2 (2.8–6.3s): the input bar grows and "1×" counts 0 to 1 on "one times." 2.88s (`stat-bars-and-fills` + `counting-dynamic-scale`); the cache-write bar grows taller and "1.25×" counts on "one and a quarter" 5.2s.
Scene 3 (6.3–8.3s): the clay cache-read bar grows to its tiny height and "0.1×" (clay) counts in on "one tenth." 7.2s; the contrast IS the payoff.
Scene 4 (8.3–11.32s): the footnote "Opus 5.5 read · 0.05×" fades in on "Opus" 8.56s, its "0.05×" landing on "twentieth." 10.4s; hold.

## Frame 9 — Prep doesn't keep forever

- scene: A horizontal timeline with a 5-minute window bracket; ticks at each request push the window forward ("hit → timer resets"); a second, longer bracket "1 h · Claude subscription"
- voiceover: "Prep doesn't keep forever. The cache lives five minutes. On a Claude subscription, an hour. And every hit resets the clock."
- duration: 8.36s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/09-cache-lifetime.html
- type: feature_showcase
- persuasion: Demonstration + anchoring on a familiar referent (a kitchen timer)
- beat: foresight

narrativeRole: The time dimension — why stepping away makes the next turn slow.
keyMessage: Keep working and it stays warm; walk away and it expires.

- blueprint: compose
- focal: the timeline with the clay 5-minute window
- roles: ink timeline + "hit" ticks = foreground subject · clay 5-min window + clay mono label = the accent · longer ink bracket "1 h · Claude subscription, within plan usage" = supporting · headline "Prep doesn't keep *forever.*" = supporting (top)

Scene 1 (0.0–1.9s): headline reveals per word "Prep" 0.12s through "forever." 1.0s (clay italic); the timeline line draws left-to-right (`svg-path-draw`) under it. Layout as sketch: full-width strip at mid-frame.
Scene 2 (1.9–3.8s): first "hit" tick + label at the left on "cache" 1.96s; on "five minutes." 2.68–3.0s the clay window bracket opens to its right with the label "5 min · resets on every hit".
Scene 3 (3.8–6.0s): on "Claude subscription" 4.04–4.6s the longer ink bracket draws beneath, its label "1 h · Claude subscription, within plan usage" landing on "hour." 5.24s.
Scene 4 (6.0–8.36s): on "every hit resets the clock" two more ticks land (6.68s, 7.08s) and with each the clay window slides forward to start at the newest tick (smooth `power3`), ending in the sketch position on "clock." 7.84s; hold.

## Frame 10 — What spoils the prep

- scene: Three mono rows reveal one per spoken item, each with a clay strike: "/model — switch models" · "fast mode — turn it on" · "/compact — mid-task"
- voiceover: "Mid-task, three things throw the prep out: switching models, turning on fast mode, and compacting. So pick your model at the start, and compact between tasks."
- duration: 10.86s
- transition_in: cut
- status: animated
- src: compositions/frames/10-what-spoils.html
- type: benefit_highlight
- persuasion: Rule of three + numbered enumeration
- beat: unease → mastery

narrativeRole: Turns the rule into behaviour the viewer controls.
keyMessage: These three actions cost you a full re-read.

- blueprint: grid-card-assemble (Adapt)
- focal: the three numbered rows
- roles: rows (clay mono index · mono command · Inter description, hairline-separated) = foreground subject · headline "Three things spoil the prep." + kicker "✱ MID-TASK" = supporting

Adapt: keep the accumulating vertical list; one row per spoken item; then the two habits light the rows they answer.
Review fix (render v1, /review #3): the frame was a small headline over a ~300px empty band. Headline now display scale; rows larger (commands ≈72px) and spread evenly through the lower two-thirds so the list fills the frame. Same copy, same order, same clay index accents.
Scene 1 (0.0–3.1s): kicker "✱ MID-TASK" on "Mid-task," 0.24s; headline "Three things spoil the prep." per word from "three" 1.12s to "out:" 2.4s.
Scene 2 (3.1–4.2s): row 01 `/model · switch models` slides in from the left with its hairline on "switching" 3.16s.
Scene 3 (4.2–5.5s): row 02 `fast mode · turn it on` on "turning" 4.24s.
Scene 4 (5.5–6.9s): row 03 `/compact · mid-task` on "compacting." 5.68s.
Scene 5 (6.9–10.86s): the habits (spoken only, no new text): on "pick your model" 7.28s row 01 lights — its command turns clay and a clay hairline underlines it, rows 02/03 dim to ~45%; on "compact between tasks" 8.96s row 01 settles back to ink and row 03 lights the same way; hold to the cut.

## Frame 11 — Check your kitchen

- scene: Only the /usage card, centered and large: "> /usage" types in; beneath a divider, "Prompt cache (main)" and the labels "hit ratio · misses · warm". The two habits are spoken, not shown
- voiceover: "Then run slash usage, and read the prompt cache line."
- duration: 3.86s
- transition_in: cut
- status: animated
- src: compositions/frames/11-check-it.html
- type: cta
- persuasion: Signposting + frame-then-fill
- beat: resolve

narrativeRole: The practical ask — two habits and one command to verify.
keyMessage: Two habits, then check the hit ratio in /usage.

- blueprint: prompt-type-submit-generate (Adapt)
- focal: the /usage card (navy surface)
- roles: navy card with title-bar dots = foreground subject (≈ 64% of frame width, centred) · "> /usage" command (mono, clay ">") · divider · "Prompt cache (main)" + "hit ratio · misses · warm" labels = supporting

Adapt: keep "watch me ask": the command types into the input; NO answer values (labels only) and NO caret (project bans blinking cursors).
Review fix (render v1, /review #1): the card no longer sits empty under the habits — the habits moved to frame 10, so this frame starts on "Then".
Scene 1 (0.0–0.9s): the card rises in from slightly below with a smooth settle on "Then" 0.1s; "> " is shown in the input.
Scene 2 (0.9–2.4s): "/usage" types in character by character (`discrete-text-sequence`, no caret) on "slash usage," 0.9–1.38s; the divider draws on 1.5s (`svg-path-draw`).
Scene 3 (2.4–3.86s): "Prompt cache (main)" fades up on "prompt" 2.5s; "hit ratio · misses · warm" reveals per token on "cache line." 2.9–3.22s (`dynamic-content-sequencing`); hold.

## Frame 12 — Read once

- scene: Callback type over cream: "Read once." then "Cook only what's new." in clay italic; ✱ mark settles
- voiceover: "Read the context once. Cook only what's new."
- duration: 3.6s
- transition_in: crossfade
- status: animated
- src: compositions/frames/12-read-once.html
- type: branding
- persuasion: Callback + distillation
- beat: satisfaction

narrativeRole: Returns to the hook and the kitchen in one line.
keyMessage: The whole idea, compressed.

- blueprint: kinetic-type-beats (Reproduce)
- focal: "Read once."
- roles: "Read once." (Playfair, display) = foreground subject · "Cook only what's new." (clay italic) = supporting · ✱ = mark

Scene 1 (0.0–1.9s): "Read once." enters on "Read" 0.24s with a smooth rise + fade (`power3`), centred as sketch.
Scene 2 (1.9–3.0s): "Cook only what's new." (clay italic) reveals per word on "Cook" 2.0s through "new." 3.12s.
Scene 3 (3.0–3.6s): the ✱ fades and scales 0.92 to 1 on 3.0s (`spring-pop-entrance`, smooth). Final frame: hold to the last frame (no exit needed; the video ends here).
