#!/usr/bin/env python3
"""Turn a rendered video into one 6x3 grid of stills that Claude can look at.

The 18 stills are spread evenly across the whole video, so a 15-second clip and a
3-minute clip both fit on one sheet. The script prints the ffmpeg command it runs
and the timestamp of every tile, so a review can point at exact moments.

Usage:
    python scripts/contact-sheet.py videos/<slug>/out/<slug>.mp4
    -> writes contact.png next to the video's folder (videos/<slug>/contact.png)

Needs ffmpeg and ffprobe on your PATH. Python 3.8+, standard library only.
"""
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

COLS, ROWS = 6, 3


def duration_of(video: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/contact-sheet.py <video.mp4>")
    video = Path(sys.argv[1])
    if not video.exists():
        sys.exit(f"No video at {video}")

    tiles = COLS * ROWS
    dur = duration_of(video)
    step = dur / tiles
    # Video folder layout is videos/<slug>/out/<slug>.mp4, so the sheet lands in videos/<slug>/.
    out_dir = video.parent.parent if video.parent.name == "out" else video.parent
    sheet = out_dir / "contact.png"

    # One exact seek per tile, then tile the stills. A single-pass `fps=` filter samples
    # each tile about half a step later than i * step, so its printed times were wrong.
    times = [i * step for i in range(tiles)]
    with tempfile.TemporaryDirectory() as tmp:
        for i, t in enumerate(times):
            grab = ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video),
                    "-frames:v", "1", "-vf", "scale=480:-1", str(Path(tmp) / f"{i:02d}.png")]
            subprocess.run(grab, check=True)
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(Path(tmp) / "%02d.png"),
               "-vf", f"tile={COLS}x{ROWS}", "-frames:v", "1", str(sheet)]
        shown = ["<tile>.png" if c.startswith(tmp) else os.path.relpath(c) if c == str(sheet) else c
                 for c in cmd]
        print(f"$ ffmpeg -ss <t> -i {shlex.quote(os.path.relpath(video).replace(chr(92), '/'))}"
              f" -frames:v 1 ...   (once per tile)")
        print("$ " + " ".join(shlex.quote(c.replace("\\", "/")) for c in shown))
        subprocess.run(cmd, check=True)

    print(f"\n{os.path.relpath(sheet)}  ({COLS}x{ROWS} tiles, {dur:.1f}s video)")
    for i, t in enumerate(times):
        row, col = divmod(i, COLS)
        print(f"  tile {i + 1:2d}  row {row + 1} col {col + 1}  {t:6.2f}s")


if __name__ == "__main__":
    main()
