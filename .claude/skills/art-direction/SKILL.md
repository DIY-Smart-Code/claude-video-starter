---
name: art-direction
description: Generate the illustrations for a HyperFrames video with the Higgsfield MCP in one locked style. Use after the storyboard is confirmed and before the build, when scenes need metaphor art (not charts, UI or logos).
---

# Art direction

Run this after the user confirmed the storyboard sheet and before the frames are built.

1. Read the video's `STORYBOARD.md`. List the scenes whose idea is a metaphor (a kitchen, a
   book, a bookmark). Scenes that show numbers, tables, prices or token rows stay HTML: never
   generate a chart, a product screen, a logo or anything that pretends to be real UI.
2. Pick the style lock. `style-lock.md` (in this skill's folder) is drawn for cream paper. If the
   video's `frame.md` uses another look, leave that file alone and write the video's own lock to
   `videos/<slug>/assets/art/style-lock.md`: the same four parts (a medium that fits the look, the
   palette as hex codes from `frame.md`, where the empty space for the headline goes, no text) and
   the same checklist, reworded for that palette. Tell the user which lock the plates use.
3. For each metaphor scene write one subject sentence, then append the style block from the lock.
   Change nothing in the style block between plates.
4. Generate the first plate with the Higgsfield MCP (`generate_image`, model `nano_banana_pro`,
   aspect ratio 16:9). Show it to the user and ask: keep or redo. When they keep it, pass that
   plate as a reference image to every later plate so the set looks like one illustrator.
5. Check every plate against the lock's checklist. If a plate fails a line, regenerate it and
   tell the user which line it failed.
6. Download each kept plate to `videos/<slug>/assets/art/<scene>-<n>.png`. Append one line per
   plate, kept or rejected, to `videos/<slug>/assets/art/ledger.jsonl`:
   `{"scene": "...", "file": "assets/art/...", "prompt": "...", "model": "...", "job_id": "...", "status": "kept|rejected", "reason": "..."}`
7. Write each kept plate's path into its scene in `STORYBOARD.md`, so the build uses the local
   file. The composition never loads an image from a URL.
