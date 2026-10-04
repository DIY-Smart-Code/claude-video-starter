---
description: Look at a rendered video as a contact sheet, score it, and name the three worst problems
argument-hint: videos/<slug>
---

Review the latest render of $ARGUMENTS. Do not edit any files in this step.

1. Find the MP4 in `$ARGUMENTS/out/`. If there is none, say so and stop.
2. Run `python scripts/contact-sheet.py <that mp4>`. It writes `contact.png` and prints the timestamp of every tile.
3. Open `contact.png` and look at it. Judge only what is on the sheet.
   Each tile is a quarter of full size, so text always looks smaller there than it is. Before you
   call text too small, pull that moment at full size and look again:
   `ffmpeg -v error -ss <seconds> -i <that mp4> -frames:v 1 frame.png`
4. Score each from 1 to 10, one line each, with a short reason:
   - **Hook**: would the first two seconds stop someone scrolling?
   - **Readability**: is every word large enough and high enough contrast to read on a phone?
   - **Motion**: does something change every few seconds, or do stretches sit frozen?
   - **Variety**: do layouts change, or is it the same centered block the whole time?
5. List the three worst problems, worst first. Each gets the tile timestamp where it shows, what is wrong, and one concrete fix.
6. Ask whether to apply the fixes. After the fixes, render again so the user can run `/review` on the new version.
   Confirm each fix on a frame pulled from the new MP4, not on a preview snapshot. If
   `npx hyperframes check` still fails, the problem is still there until a full-size frame
   from the render shows otherwise.
