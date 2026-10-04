---
name: art-direction
description: Generate the illustrations for a HyperFrames video with the Higgsfield MCP in one locked style. Use after the storyboard is confirmed and before the build, when scenes need metaphor art (not charts, UI or logos).
---

# Art direction

Run this after the user confirmed the storyboard sheet and before the frames are built.

1. Read the video's `STORYBOARD.md`. List the scenes whose idea is a metaphor (a kitchen, a
   book, a bookmark). Scenes that show numbers, tables, prices or token rows stay HTML: never
   generate a chart, a product screen, a logo or anything that pretends to be real UI.
2. For each metaphor scene write one subject sentence, then append the style block from
   `style-lock.md` (in this skill's folder). Change nothing in the style block between plates.
3. Generate the first plate with the Higgsfield MCP (`generate_image`, model `nano_banana_pro`,
   aspect ratio 16:9). Show it to the user and ask: keep or redo. When they keep it, pass that
   plate as a reference image to every later plate so the set looks like one illustrator.
4. Check every plate against the checklist in `style-lock.md`. If a plate fails a line,
   regenerate it and tell the user which line it failed.
5. Download each kept plate to `videos/<slug>/assets/art/<scene>-<n>.png`. Append one line per
   plate, kept or rejected, to `videos/<slug>/assets/art/ledger.jsonl`:
   `{"scene": "...", "file": "assets/art/...", "prompt": "...", "model": "...", "job_id": "...", "status": "kept|rejected", "reason": "..."}`
6. Write each kept plate's path into its scene in `STORYBOARD.md`, so the build uses the local
   file. The composition never loads an image from a URL.
