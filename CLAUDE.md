# Video studio rules

1. Start every video with /hyperframes. For an explainer, ask for the standard explainer pipeline (/faceless-explainer).
2. Never build before the user confirmed the storyboard sketch sheet (`storyboard.html`).
3. Metaphor scenes get illustrations from /art-direction. Charts, numbers, tables and UI stay HTML.
4. Same input, same frame: no Math.random(), no Date.now(), no timers, no network calls inside a composition.
5. Lint after every edit. A video is not finished until the user has run /review on its render.

## Where things go

- Every video lives in its own folder under `videos/<slug>/`; /hyperframes creates it.
- Check: `npx hyperframes lint videos/<slug>` after every edit, `npx hyperframes check videos/<slug>` before a render. A failed check is real until a full-size frame from the render proves otherwise.
- Preview: `npx hyperframes preview videos/<slug>`
- Render: `npx hyperframes render videos/<slug> -o videos/<slug>/out/<slug>.mp4`
- Review: the user runs `/review videos/<slug>` (contact sheet + scores). Do not skip ahead and grade your own work unasked.

## Narration

- Write the narration for the ear: the voice reads exactly what's on the page. Use commas or full stops instead of dashes, and write file names and acronyms the way they are said (`CLAUDE.md` becomes "Claude dot M D", `API` becomes "A P I"). On screen they keep their written form.
- ElevenLabs: `python scripts/tts.py videos/<slug>` reads `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` from `.env` and writes `narration.wav` and `transcript.json` (word timings) into the video folder. Use it whenever the user picked an ElevenLabs voice. The voice is set in `.env`: never ask for a voice ID and never pass `--voice`.
- Free and local: `npx hyperframes tts videos/<slug>/script.txt -o videos/<slug>/narration.wav`, then `npx hyperframes transcribe videos/<slug>/narration.wav -d videos/<slug>`.
- Both routes write the same `transcript.json`: a list of `{ "text", "start", "end" }` words in seconds.
- Every reveal starts at the `start` time of the word that names it. Read the times from `transcript.json`; never guess them.
- Add the narration as `<audio>` with `data-start`, `data-duration` and `data-track-index`, and make the video exactly as long as the audio.

## Composition rules

- Every timed element has `class="clip"`, `data-start`, `data-duration` and `data-track-index`.
- One paused GSAP timeline per composition, registered on `window.__timelines["<composition id>"]`. End it with `tl.set({}, {}, <video length>)`.
- Hide elements with `opacity: 0` in CSS, then reveal them with `tl.to(...)`. No `tl.from()` for things that should stay hidden.
- Fonts come from `@font-face` files in `assets/fonts/`. GSAP comes from a local file. Never load either from a CDN.
- `<video>` is always `muted`; its sound goes on a separate `<audio>`.

## How it should look

- Text is at least 40px on 16:9 and 48px on 9:16. Short lines beat paragraphs.
- Something on screen changes at least every 3 seconds. No frozen stretches.
- No blinking cursors or pulsing loops. A blink is not motion; it hides a frozen screen.
- Show one idea at a time; lists reveal one item per spoken item.
- No background music unless the user asks for it.

## Generated images (Higgsfield MCP)

- Use them for illustrations, backgrounds and textures. Never generate a product screen, a chart, a logo or anything that pretends to be real UI.
- Put the palette hex codes in the prompt and ask for no text in the image. /art-direction has the full recipe.
- Save the file into `videos/<slug>/assets/` and reference it locally.
