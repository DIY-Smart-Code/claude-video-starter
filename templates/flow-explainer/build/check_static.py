"""Post-render freeze check: no near-static stretch longer than 5 s in the rendered MP4.

    python build/check_static.py                  # from the video folder: out/<meta id>.mp4
    python build/check_static.py path/to/video.mp4 [--noise -50dB]

The scene check (check_style.py) sees tween times; this one sees pixels. Small movers (a chip, a packet,
a thin wire) stay under ffmpeg's freezedetect threshold, so a stretch with only those counts as frozen:
add a LARGE change on a phrase there (a solid fill(), a focus dim, a card, a camera move). The last 4 s
(the closing hold) are allowed to stand still. Needs ffmpeg + ffprobe. Exit 1 on a failure.
"""
import io, json, os, re, subprocess, sys

LIMIT, END_HOLD = 5.0, 4.0
args = sys.argv[1:]
noise = "-45dB"
if "--noise" in args:
    i = args.index("--noise")
    noise = args[i + 1]
    del args[i:i + 2]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if args:
    mp4 = args[0]
else:
    vid = json.load(io.open(os.path.join(root, "meta.json"), encoding="utf8"))["id"]
    mp4 = os.path.join(root, "out", f"{vid}.mp4")
if not os.path.exists(mp4):
    sys.exit(f"no render at {mp4}")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", mp4],
                           capture_output=True, text=True, check=True).stdout.strip())
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-vf", f"freezedetect=n={noise}:d=2", "-map", "0:v:0", "-f", "null", "-"],
                   capture_output=True, text=True, encoding="utf8", errors="replace")
starts = [float(x) for x in re.findall(r"freeze_start:\s*([0-9.]+)", r.stderr)]
durs = [float(x) for x in re.findall(r"freeze_duration:\s*([0-9.]+)", r.stderr)]
if len(durs) < len(starts):                      # a freeze running into the end has no duration line
    durs.append(dur - starts[-1])
bad, total = [], 0.0
for s, d in zip(starts, durs):
    total += d
    if d > LIMIT and s < dur - END_HOLD - 0.5:
        e = min(s + d, dur - END_HOLD)
        if e - s > LIMIT:
            bad.append((s, e - s))
print(f"[check_static] {os.path.basename(mp4)}: near-static {total:.1f} s of {dur:.1f} s "
      f"({100 * total / dur:.0f} %), longest {max(durs or [0]):.1f} s (freezedetect {noise})")
for s, d in bad:
    print(f"  FROZEN {int(s // 60)}:{s % 60:04.1f}  for {d:.1f} s")
print("OK no stretch over 5 s" if not bad else f"FAIL {len(bad)} stretch(es) over {LIMIT:.0f} s")
sys.exit(1 if bad else 0)
