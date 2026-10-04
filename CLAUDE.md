# Video studio rules

1. Use HyperFrames for every video. Start with the /hyperframes skill.
2. Same input, same frame: no Math.random(), no Date.now(), no timers, no network calls inside a composition.
3. Lint after every edit. A video is not finished until the user has run /review on its render.

## Where things go

- A new video starts as a copy of `templates/long-form/` (16:9) or `templates/short/` (9:16) in `videos/<slug>/`. Set `id` and `name` in its `meta.json`.
- Check: `npx hyperframes lint videos/<slug>` after every edit, `npx hyperframes check videos/<slug>` before a render. A failed check is real until a full-size frame from the render proves otherwise.
- Preview: `npx hyperframes preview videos/<slug>`
- Render: `npx hyperframes render videos/<slug> -o videos/<slug>/out/<slug>.mp4`
- Review: the user runs `/review videos/<slug>` (contact sheet + scores). Do not skip ahead and grade your own work unasked.

## Narration

- The script lives in `videos/<slug>/script.txt`.
- ElevenLabs: `python scripts/tts.py videos/<slug>` writes `narration.wav` and `transcript.json`.
- Free and local: `npx hyperframes tts videos/<slug>/script.txt -o videos/<slug>/narration.wav`, then `npx hyperframes transcribe videos/<slug>/narration.wav -d videos/<slug>`.
- Both routes write the same `transcript.json`: a list of `{ "text", "start", "end" }` words in seconds.
- When a video has a transcript, every reveal starts at the `start` time of the word that names it. Read the times from `transcript.json`; never guess them.
- Add the narration as `<audio>` with `data-start`, `data-duration` and `data-track-index`, and make the video exactly as long as the audio.

## Composition rules

- Every timed element has `class="clip"`, `data-start`, `data-duration` and `data-track-index`.
- One paused GSAP timeline per composition, registered on `window.__timelines["<composition id>"]`. End it with `tl.set({}, {}, <video length>)`.
- Hide elements with `opacity: 0` in CSS, then reveal them with `tl.to(...)`. No `tl.from()` for things that should stay hidden.
- Fonts come from `@font-face` files in `assets/fonts/`. GSAP comes from `assets/vendor/gsap.min.js`. Never load either from a CDN.
- `<video>` is always `muted`; its sound goes on a separate `<audio>`.

## How it should look

- Text is at least 40px on 16:9 and 48px on 9:16. Short lines beat paragraphs.
- Something on screen changes at least every 3 seconds. No frozen stretches.
- No blinking cursors or pulsing loops. A blink is not motion; it hides a frozen screen.
- Show one idea at a time; lists reveal one item per spoken item.
- No background music unless the user asks for it.

## Generated images (Higgsfield MCP)

- Use them for illustrations, backgrounds and textures. Never generate a product screen, a chart, a logo or anything that pretends to be real UI.
- Put the palette hex codes in the prompt and ask for no text in the image.
- Save the file into `videos/<slug>/assets/` and reference it locally.
