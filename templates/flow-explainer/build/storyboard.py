"""Storyboard sheet for a flow-explainer video: real stills of every scene + its narration, in one HTML page.

    python build/storyboard.py          # from the video folder, after python build/build.py

Works before the voice exists: without transcript.json the build runs on synthetic timing from script.txt,
so the sheet shows the real frames the build will make. Writes storyboard.html + storyboard/*.png.
Open storyboard.html in a browser and confirm it before TTS and the final build (CLAUDE.md rule 2).
"""
import glob, html, io, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import timing as T  # noqa: E402
import scenes  # noqa: E402
import kit  # noqa: E402

V = scenes.VIDEO
T.configure(V)
FR = (0.15, 0.55, 0.93)          # where in each scene the stills are taken
rows, ts = [], []
for k, s in enumerate(V["scenes"]):
    sid = s["id"]
    cut, dur = T.scene_cut(sid), T.scene_dur(sid)
    times = [round(cut + dur * f, 2) for f in FR]
    if k == 0:
        times[0] = 0.0                   # frame 0 is the thumbnail-grade first frame
    i0 = T.FIRST[sid]
    i1 = T.FIRST[V["scenes"][k + 1]["id"]] if k + 1 < len(V["scenes"]) else len(T.WORDS)
    text = " ".join(w["word"] for w in T.WORDS[i0:i1])
    rows.append((s, cut, dur, times, text))
    ts += times

out = os.path.join(ROOT, "storyboard")
os.makedirs(out, exist_ok=True)
cmd = ["npx", "hyperframes", "snapshot", ROOT, "--no-end", "-o", out, "--at", ",".join("%g" % t for t in ts)]
r = subprocess.run(cmd, shell=os.name == "nt", stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)
if r.returncode:
    sys.exit("snapshot failed:\n" + (r.stderr or "")[-1500:])


def still(t):
    hits = glob.glob(os.path.join(out, f"*-at-{'%g' % t}s.png"))
    return "storyboard/" + os.path.basename(hits[0]) if hits else ""


sw = "".join(f'<span class="sw" style="background:{kit.tok(k)}"></span><code>{k} {kit.tok(k)}</code>'
             for k in ("accent-1", "flow", "ok", "bad", "warn", "draft"))
body = []
for s, cut, dur, times, text in rows:
    imgs = "".join(f'<figure><img src="{still(t)}" alt=""><figcaption>{t:.1f} s</figcaption></figure>' for t in times)
    body.append(f'<section><h2>{html.escape(s["id"])} <small>{html.escape(s.get("title", ""))} · {cut:.1f}–{cut + dur:.1f} s'
                f' · chapter {s.get("chapter", "")}</small></h2><p class="vo">{html.escape(text)}</p><div class="row">{imgs}</div></section>')
mode = "synthetic timing (no voice yet)" if T.SYNTHETIC else "voice timing (transcript.json)"
page = f"""<!doctype html><html lang="{V.get('lang', 'en')}"><head><meta charset="utf-8"><title>Storyboard: {html.escape(V['title'])}</title>
<style>
 body {{ font-family: system-ui, sans-serif; margin: 32px; background: #f4f2ee; color: #1d1f24; }}
 h1 {{ margin: 0 0 6px; }} .meta {{ color: #5d636e; margin-bottom: 18px; }}
 .sw {{ display: inline-block; width: 18px; height: 18px; border-radius: 4px; vertical-align: -4px; margin: 0 6px 0 14px; }}
 section {{ background: #fff; border-radius: 14px; padding: 16px 20px; margin: 18px 0; box-shadow: 0 2px 0 rgba(0,0,0,.06); }}
 h2 {{ margin: 0 0 6px; font-size: 20px; }} h2 small {{ color: #5d636e; font-weight: 500; }}
 .vo {{ margin: 0 0 12px; font-size: 16px; line-height: 1.5; max-width: 1400px; }}
 .row {{ display: flex; gap: 12px; }} figure {{ margin: 0; flex: 1; }}
 img {{ width: 100%; border-radius: 8px; border: 1px solid #ddd; display: block; }}
 figcaption {{ font: 12px monospace; color: #5d636e; margin-top: 4px; }}
</style></head><body>
<h1>{html.escape(V['title'])}</h1>
<div class="meta">skin {kit.SKIN} · {len(rows)} scenes · {T.total():.1f} s · {mode}<br>{sw}</div>
{''.join(body)}
</body></html>
"""
io.open(os.path.join(ROOT, "storyboard.html"), "w", encoding="utf8", newline="\n").write(page)
print(f"storyboard.html: {len(rows)} scenes, {len(ts)} stills ({mode})")
