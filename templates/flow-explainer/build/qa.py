"""Dense visual QA: snapshot the composition on a time grid (or at given times) and tile labelled 3x3 sheets.

    python build/qa.py sweep <name> <start> <end> <step>     # e.g. sweep s1 0 110 3, then sweep s2 1.5 110 3
    python build/qa.py at <name> <t1,t2,...>                 # spot checks after a fix

Run from the video folder (or pass --dir videos/<slug>). Frames land in qa/<name>/, sheets in
qa/<name>/sheet-NN.png (9 frames each, time label top-left). Look at EVERY sheet; pull suspicious frames
at full size. Sheets need Pillow (pip install pillow); without it you get the frames plus the CLI's own
contact-sheet.jpg per batch.
"""
import glob, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
proj = os.path.dirname(HERE)
if "--dir" in args:
    i = args.index("--dir")
    proj = os.path.abspath(args[i + 1])
    del args[i:i + 2]
if len(args) < 3 or args[0] not in ("sweep", "at"):
    sys.exit(__doc__)
mode, name = args[0], args[1]
if mode == "sweep":
    a, b, step = float(args[2]), float(args[3]), float(args[4])
    ts, t = [], a
    while t <= b + 1e-6:
        ts.append(round(t, 2))
        t += step
else:
    ts = [round(float(x), 2) for x in args[2].split(",") if x.strip()]
out = os.path.join(proj, "qa", name)
os.makedirs(out, exist_ok=True)
shell = os.name == "nt"
for i in range(0, len(ts), 40):                 # the snapshot CLI takes ~40 times per call comfortably
    chunk = ts[i:i + 40]
    sub = os.path.join(out, f"batch-{i // 40:02d}")
    cmd = ["npx", "hyperframes", "snapshot", proj, "--no-end", "-o", sub, "--at", ",".join("%g" % x for x in chunk)]
    r = subprocess.run(cmd, shell=shell, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)
    if r.returncode:
        sys.exit("snapshot failed:\n" + (r.stderr or "")[-1500:])


def frame_at(t):
    hits = glob.glob(os.path.join(out, "batch-*", f"*-at-{'%g' % t}s.png"))
    return hits[0] if hits else None


try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print(f"{len(ts)} frames in {out} (install Pillow for labelled sheets; each batch folder has contact-sheet.jpg)")
    sys.exit(0)
W, H, C, R = 640, 360, 3, 3
try:
    font = ImageFont.truetype("arial.ttf", 22)
except Exception:
    font = ImageFont.load_default()
sheets = []
for s in range(0, len(ts), C * R):
    grp = ts[s:s + C * R]
    rows = (len(grp) + C - 1) // C
    sheet = Image.new("RGB", (W * C, H * rows), "black")
    d = ImageDraw.Draw(sheet)
    for j, tt in enumerate(grp):
        f = frame_at(tt)
        x, y = (j % C) * W, (j // C) * H
        if f:
            sheet.paste(Image.open(f).convert("RGB").resize((W, H)), (x, y))
        d.rectangle([x, y, x + 92, y + 28], fill="red")
        d.text((x + 6, y + 3), f"{tt:.1f}s", fill="white", font=font)
    p = os.path.join(out, f"sheet-{len(sheets):02d}.png")
    sheet.save(p)
    sheets.append(p)
print(len(ts), "frames,", len(sheets), "sheets in", out)
