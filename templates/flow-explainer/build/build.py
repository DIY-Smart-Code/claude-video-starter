"""Build a flow-explainer video: scene files + root index.html + seam ledger, then stamp the seams.

    python build/build.py            # from the video folder (videos/<slug>/) or the template folder

Per-video code lives in build/video_scenes.py (VIDEO table, SYSTEM(), one function per scene).
Everything below is GENERATED, never hand-edit it:
  compositions/scene-<id>.html   one per VIDEO["scenes"] row
  index.html                     root: ground + topic shapes, chapter HUD, source line, progress bar,
                                 scene wrappers, narration, optional closing question
  ledger.json                    one row per scene seam -> build/seam_stamp.mjs writes the transitions
  assets/shapes/shape1..3.svg    the ghosted backdrop, drawn from VIDEO["backdrop"] icons (topic-adaptive)
Exit 1 when the scene code raised a WARN (a chip over 4 words, a missing phrase, ...): fix it, rebuild.
"""
import io, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timing as T  # noqa: E402
import scenes  # noqa: E402
import kit  # noqa: E402
import flow  # noqa: E402
import atoms  # noqa: E402
from kit import WARN, esc  # noqa: E402

V = scenes.VIDEO
T.configure(V)
atoms.setup(V)
ROOT = T.ROOT
if V.get("midroll"):
    sys.exit("build.py: VIDEO['midroll'] is not supported in this template (remove it)")

# ------------------------------------------------------------------ topic shapes (backdrop) from icons
BACKDROP = V.get("backdrop") or ["doc", "gear", "clock"]
os.makedirs(os.path.join(ROOT, "assets", "shapes"), exist_ok=True)
for i, name in enumerate(BACKDROP[:3], 1):
    if name not in flow.ICONS:
        sys.exit(f"build.py: VIDEO['backdrop'] icon {name!r} unknown (have: {', '.join(sorted(flow.ICONS))})")
    g = "#8A8F99"
    body = (flow.ICONS[name]
            .replace('class="f"', f'fill="{g}" stroke="{g}" stroke-width="6" stroke-linejoin="round"')
            .replace('class="s"', f'fill="none" stroke="{g}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"')
            .replace('class="k"', f'fill="{g}"'))
    io.open(os.path.join(ROOT, "assets", "shapes", f"shape{i}.svg"), "w", encoding="utf8", newline="\n").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="400" height="400">{body}</svg>\n')

# ------------------------------------------------------------------ scenes
os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
for fn in scenes.ALL:
    fn()
    print("wrote scene", fn.__name__)

ORDER = T.ORDER
CUT = {s: T.scene_cut(s) for s in ORDER}
TOTAL = T.total()
ROWS = {s["id"]: s for s in V["scenes"]}

# ------------------------------------------------------------------ seam ledger
AX = {"left": ("x", -1, "cut-the-curve LEFT"), "zin": ("z", 1, "zoom-through push"),
      "zout": ("z", -1, "inverse zoom-through"), "up": ("y", -1, "cut-the-curve UP")}
ledger = {"fps": 30, "seams": []}
for a, b in zip(ORDER, ORDER[1:]):
    ax, d, tech = AX[ROWS[b].get("enter", "left")]
    row = {"id": f"{a}→{b}", "cut": CUT[b], "technique": tech,
           "exit": {"selector": f"#scene-{a}-wrap", "axis": ax, "dir": d},
           "entry": {"selector": f"#scene-{b}-wrap", "axis": ax, "dir": d}}
    if ax == "z":
        row["entry"]["scanRoot"] = f"#scene-{b}-wrap"
    ledger["seams"].append(row)
json.dump(ledger, io.open(os.path.join(ROOT, "ledger.json"), "w", encoding="utf8"), ensure_ascii=False, indent=2)
SEAM_TIMES = sorted(r["cut"] for r in ledger["seams"])

# ------------------------------------------------------------------ chrome data
CH = V["chapters"]
segs = "".join(f'<i id="sg{i}" class="sg"></i>' for i in range(1, len(CH) + 1))
HUDP = V.get("hud_prefix", "CH")      # "" = the chapter name alone
labs = "".join(f'<span id="sl{i}" class="sl">{(HUDP + " " + format(i, "02d") + " &middot; ") if HUDP else ""}{esc(c.upper())}</span>'
               for i, c in enumerate(CH, 1))
SRC = [(CUT[s["id"]], s.get("source", "")) for s in V["scenes"]]
SRC_LABEL = esc(V.get("source_label", "SOURCE"))
src_spans = "".join(
    f'<span id="src-{i}" class="src-l"{" style=" + chr(34) + "opacity:0.7" + chr(34) if i == 0 and txt else ""}>'
    f'{"<b>" + SRC_LABEL + "</b> " + esc(txt) if txt else ""}</span>' for i, (_, txt) in enumerate(SRC))
js_src = [f"  srcGo(tl, {round(SRC[i][0], 2)}, {i - 1}, {i});" for i in range(1, len(SRC))]
js_steps, cur = [], 0
for s in V["scenes"]:
    st = s.get("chapter", 0)
    if st and st != cur:
        js_steps.append(f"  stepGo(tl, {CUT[s['id']]}, {cur}, {st});" if cur else f"  stepFirst(tl, {CUT[s['id']]}, {st});")
        cur = st

# optional closing question, word by word on its spoken words: VIDEO["cta"] = {"phrase": ..., "kw": [...]}
cta = V.get("cta")
cta_spans, js_cta = "", "  // no closing question (VIDEO['cta'] is None)"
if cta:
    ci, cn = T._find(cta["phrase"])
    cwords = cta.get("text", cta["phrase"]).split()
    cwords[0] = cwords[0][:1].upper() + cwords[0][1:]
    kwset = {re.sub(r"[\W_]", "", k.lower()) for k in cta.get("kw", [])}
    kwflags = [" kw" if re.sub(r"[\W_]", "", w.lower()) in kwset else "" for w in cwords]
    cta_spans = "".join(f'<span id="cq{k}" class="cqw{kwflags[k]}">{esc(w)}</span>'
                        for k, w in enumerate(cwords))
    js_cta = "\n".join(
        f'  tl.fromTo("#cq{k}", {{ opacity: 0, y: 26 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power4.out", immediateRender: false }}, {T.wt(ci + min(k, cn - 1))});'
        for k in range(len(cwords)))

# ------------------------------------------------------------------ audio
narr_file = V.get("narration", "narration.wav")
have_narr = (not T.SYNTHETIC) and os.path.exists(os.path.join(ROOT, narr_file))
if have_narr:
    narr = (f'  <audio id="narration" class="clip" src="{narr_file}" data-start="0" '
            f'data-duration="{round(T.WORDS[-1]["end"] + 0.6, 3)}" data-track-index="2" data-volume="1.0"></audio>')
else:
    narr = (f"  <!-- narration: none yet ({'synthetic timing from script.txt, no transcript.json' if T.SYNTHETIC else narr_file + ' missing'}). "
            "Run python scripts/tts.py videos/<slug>, then rebuild. -->")
SFX = V.get("seam_sfx")    # optional: a short whoosh file under assets/ (you supply it), played 0.4 s before each seam
sfx = "\n".join(
    f'  <audio id="sfx-seam-{i + 1}" class="clip" src="{SFX}" data-start="{round(max(0.0, t - 0.4), 2)}" '
    f'data-duration="1.0" data-track-index="5" data-volume="0.11"></audio>' for i, t in enumerate(SEAM_TIMES)) if SFX else \
    "  <!-- no seam sound effects (VIDEO['seam_sfx'] unset) -->"

wrappers = "\n".join(
    f'  <div id="scene-{s}-wrap" class="scene-wrapper" data-composition-id="scene-{s}" '
    f'data-composition-src="compositions/scene-{s}.html" data-start="{CUT[s]}" data-track-index="1"></div>' for s in ORDER)

brand = (f'  <img id="brand-mark" src="{V["brand_logo"]}" alt="topic brand" style="position:absolute; top:28px; right:48px; height:44px; width:auto; z-index:12; pointer-events:none;">'
         if V.get("brand_logo") else "  <!-- no corner brand mark (VIDEO['brand_logo'] unset) -->")

SKIN = kit.SKIN
TOKENS = kit.TOKENS
ACC, OKC, BG, TXT = kit.tok("accent-1"), kit.tok("ok"), kit.tok("bg"), kit.tok("text")
if SKIN == "paper":
    GROUND = ("background-image: linear-gradient(rgba(38,40,45,0.07) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(38,40,45,0.07) 1.5px, transparent 1.5px);\n"
              "    background-size: 48px 48px, 48px 48px; background-position: 0px 0px, 0px 0px;")
    AMBIENT = "radial-gradient(ellipse 70% 60% at 50% 40%, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0) 70%)"
    VIGNETTE = "radial-gradient(ellipse 90% 80% at 50% 50%, rgba(0,0,0,0) 62%, rgba(60,40,20,0.10) 100%)"
    BLOB_FILL, BLOB_OP, SHAPE_OP, NOISE_OP = "#26282D", 0.045, 0.028, 0.035
else:
    GROUND = ("background-image: linear-gradient(rgba(201,206,216,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(201,206,216,0.045) 1px, transparent 1px);\n"
              "    background-size: 80px 80px, 80px 80px; background-position: 0px 0px, 0px 0px;")
    AMBIENT = "radial-gradient(ellipse 70% 60% at 50% 38%, #1D2027 0%, rgba(22,24,29,0) 70%), radial-gradient(circle at 22% 18%, rgba(var(--accent-rgb), 0.06), transparent 55%)"
    VIGNETTE = "radial-gradient(ellipse 85% 75% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)"
    BLOB_FILL, BLOB_OP, SHAPE_OP, NOISE_OP = "#FFFFFF", 0.035, 0.014, 0.03

STYLE = f"""
  @font-face {{ font-family: 'Inter'; src: url('assets/fonts/inter-700.woff2') format('woff2'); font-weight: 400 799; }}
  @font-face {{ font-family: 'Inter'; src: url('assets/fonts/inter-900.woff2') format('woff2'); font-weight: 800 900; }}
  @font-face {{ font-family: 'JetBrains Mono'; src: url('assets/fonts/jetbrains-mono-600.woff2') format('woff2'); font-weight: 400 650; }}
  @font-face {{ font-family: 'JetBrains Mono'; src: url('assets/fonts/jetbrains-mono-700.woff2') format('woff2'); font-weight: 651 900; }}
  @font-face {{ font-family: 'Playfair Display'; src: url('assets/fonts/playfair-display-italic.woff2') format('woff2'); font-style: italic; font-weight: 400 900; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {BG};
    font-family: 'Inter', system-ui, sans-serif; color: {TXT}; -webkit-font-smoothing: antialiased; }}
  #root {{ background: {BG}; overflow: hidden; }}
  #ground {{ position: absolute; inset: 0; z-index: 0; pointer-events: none;
    {GROUND} }}
  #ambient {{ position: absolute; inset: 0; pointer-events: none; z-index: 0; background: {AMBIENT}; }}
  #vignette {{ position: absolute; inset: 0; pointer-events: none; z-index: 9; background: {VIGNETTE}; }}
  #blob {{ position: absolute; left: 1240px; top: 560px; width: 1000px; height: 760px; z-index: 0; pointer-events: none; opacity: {BLOB_OP}; }}
  #blob path {{ fill: {BLOB_FILL}; }}
  #shape-backdrop {{ position: absolute; inset: 0; pointer-events: none; overflow: hidden; z-index: 0; }}
  #shape-backdrop img {{ position: absolute; opacity: {SHAPE_OP}; object-fit: contain; pointer-events: none; }}
  #noise-overlay {{ position: absolute; inset: 0; width: 1920px; height: 1080px; pointer-events: none; z-index: 10; opacity: {NOISE_OP}; mix-blend-mode: overlay; }}
  #strip {{ position: absolute; top: 28px; left: 560px; width: 800px; height: 40px; z-index: 12; display: flex; align-items: center; gap: 14px; pointer-events: none; opacity: 0; }}
  #segs {{ display: flex; gap: 6px; }}
  .sg {{ display: block; width: 44px; height: 8px; border-radius: 4px; background: var(--line-2); }}
  #slab {{ position: relative; height: 30px; flex: 1; margin-left: 8px; }}
  .sl {{ position: absolute; left: 0; top: 0; font-family: 'JetBrains Mono', ui-monospace, monospace; font-weight: 700; font-size: 22px; letter-spacing: 1.5px; line-height: 30px; color: var(--accent-1); white-space: nowrap; opacity: 0; }}
  #source-url {{ position: absolute; bottom: 22px; right: 48px; width: 1400px; height: 30px; z-index: 12; pointer-events: none; }}
  .src-l {{ position: absolute; right: 0; bottom: 0; white-space: nowrap; font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-weight: 600; font-size: 22px; letter-spacing: 0.5px; color: var(--text-2); opacity: 0; }}
  .src-l b {{ color: var(--accent-1); font-weight: 800; }}
  #progress-track {{ position: absolute; bottom: 0; left: 0; width: 1920px; height: 6px; background: var(--track); z-index: 12; }}
  #progress-fill {{ width: 0; height: 100%; background: var(--accent-1); box-shadow: 0 0 12px rgba(var(--accent-rgb), 0.6); }}
  .scene-wrapper {{ position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; z-index: 2; opacity: 0; visibility: hidden; }}
  #cta-question {{ position: absolute; left: 120px; top: 600px; width: 820px; z-index: 11; font-family: 'Inter', system-ui, sans-serif;
    font-weight: 900; font-size: 68px; line-height: 1.1; letter-spacing: -1.5px; color: var(--text); }}
  .cqw {{ display: inline-block; margin-right: 0.26em; opacity: 0; }}
  .cqw.kw {{ color: var(--accent-1); }}
"""

first = ORDER[0]
COMP_ID = json.load(io.open(os.path.join(ROOT, "meta.json"), encoding="utf8")).get("id") or "main"
html = f"""<!DOCTYPE html>
<html lang="{V.get('lang', 'en')}">
<head>
<meta charset="UTF-8">
<title>{esc(V["title"])}</title>
<!-- GENERATED by build/build.py (flow-explainer, skin: {SKIN}). Edit build/video_scenes.py and rebuild; never hand-edit. -->
<script src="assets/vendor/gsap.min.js"></script>
<style>{TOKENS}
{STYLE}
  #scene-{first}-wrap {{ opacity: 1; visibility: visible; }}
</style>
</head>
<body>
<div id="root" data-composition-id="{COMP_ID}" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
  <div id="ambient"></div>
  <div id="ground"></div>
  <svg id="blob" viewBox="0 0 1000 760" width="1000" height="760"><path d="M210 120C330 10 560 -20 720 70S980 260 990 430 900 700 690 745 300 760 160 650 -20 420 40 300 120 200 210 120Z"/></svg>
  <div id="shape-backdrop"></div>
  <div id="vignette"></div>

{brand}
  <div id="strip"><div id="segs">{segs}</div><div id="slab">{labs}</div></div>
  <div id="source-url">{src_spans}</div>
  <div id="progress-track"><div id="progress-fill"></div></div>

  <!-- SCENE WRAPPERS (composition clock = narration clock) -->
{wrappers}

  <div id="cta-question">{cta_spans}</div>

  <!-- AUDIO: narration (one TTS call). No background music. -->
{narr}
{sfx}

  <svg id="noise-overlay" xmlns="http://www.w3.org/2000/svg">
    <defs><filter id="noise-filter" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="4" seed="42" stitchTiles="stitch" result="noise" />
      <feColorMatrix type="saturate" values="0" in="noise" result="monoNoise" />
    </filter></defs>
    <rect width="100%" height="100%" filter="url(#noise-filter)" fill="white" />
  </svg>
</div>

<script>
  function seedHash(seed) {{
    let h = 1779033703 ^ seed.length;
    for (let i = 0; i < seed.length; i++) {{ h = Math.imul(h ^ seed.charCodeAt(i), 3432918353); h = (h << 13) | (h >>> 19); }}
    h = Math.imul(h ^ (h >>> 16), 2246822507); h = Math.imul(h ^ (h >>> 13), 3266489909); h ^= h >>> 16;
    return (h >>> 0) / 4294967296;
  }}
  // topic shapes: 12 ghosted silhouettes, placed deterministically, moved ONLY at seams
  function spawnShapes(seedPrefix, container) {{
    const shapes = ['assets/shapes/shape1.svg', 'assets/shapes/shape2.svg', 'assets/shapes/shape3.svg'];
    const count = 12, w = 1920, h = 1080, minSize = 220, sizeRange = 220, minDist = 380, MAX_TRIES = 80;
    const placed = []; let attempt = 0;
    for (let i = 0; i < count; i++) {{
      let best = null, bestScore = -1;
      for (let t = 0; t < MAX_TRIES; t++) {{
        const seed = seedPrefix + '-' + i + '-' + attempt++;
        const size = minSize + seedHash(seed + '-size') * sizeRange;
        const cx = seedHash(seed + '-x') * (w - size * 0.4) + size * 0.2;
        const cy = seedHash(seed + '-y') * (h - size * 0.4) + size * 0.2;
        const rot = (seedHash(seed + '-rot') - 0.5) * 50;
        let nearest = Infinity;
        for (const p of placed) {{ const dx = cx - p.cx, dy = cy - p.cy; const d2 = dx * dx + dy * dy; if (d2 < nearest) nearest = d2; }}
        if (nearest >= minDist * minDist) {{ best = {{ cx, cy, size, rot }}; break; }}
        if (nearest > bestScore) {{ bestScore = nearest; best = {{ cx, cy, size, rot }}; }}
      }}
      placed.push(best);
      const img = document.createElement('img');
      img.src = shapes[i % shapes.length];
      img.alt = '';
      img.style.cssText = 'left:' + (best.cx - best.size / 2) + 'px;top:' + (best.cy - best.size / 2) + 'px;width:' + best.size + 'px;height:' + best.size + 'px;';
      container.appendChild(img);
      gsap.set(img, {{ rotation: best.rot }});
    }}
  }}
  function reorderShapes(tl, container, seedPrefix, t, gen) {{
    container.querySelectorAll('img').forEach((img, i) => {{
      const seed = seedPrefix + '-reorder-' + gen + '-' + i;
      tl.to(img, {{ x: (seedHash(seed + '-x') - 0.5) * 460, y: (seedHash(seed + '-y') - 0.5) * 320,
        rotation: (seedHash(seed + '-r') - 0.5) * 50, duration: 1.0, ease: 'power2.inOut' }}, t);
    }});
  }}
  function srcGo(tl, t, a, b) {{
    tl.to('#src-' + a, {{ opacity: 0, duration: 0.2 }}, t);
    tl.to('#src-' + b, {{ opacity: 0.7, duration: 0.3 }}, t + 0.2);
  }}
  function stepFirst(tl, t, s) {{
    tl.to('#sg' + s, {{ backgroundColor: '{ACC}', duration: 0.3 }}, t);
    tl.fromTo('#sl' + s, {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.3, immediateRender: false }}, t);
  }}
  function stepGo(tl, t, a, b) {{
    tl.to('#sg' + a, {{ backgroundColor: '{OKC}', duration: 0.3 }}, t);
    tl.to('#sl' + a, {{ opacity: 0, y: -8, duration: 0.2 }}, t);
    stepFirst(tl, t + 0.2, b);
  }}

  spawnShapes('{V["seed"]}', document.getElementById('shape-backdrop'));

  window.__timelines = window.__timelines || {{}};
  const TOTAL_DURATION = {TOTAL};
  const tl = gsap.timeline({{ paused: true }});

  tl.fromTo('#progress-fill', {{ width: 0 }}, {{ width: 1920, duration: TOTAL_DURATION, ease: 'none' }}, 0);
  tl.fromTo('#strip', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, immediateRender: false }}, 0.6);

  // background moves ONLY at seams: shapes re-scatter + the grid travels one step LEFT
  const SEAMS = {json.dumps([round(t, 3) for t in SEAM_TIMES])};
  const shapeBackdrop = document.getElementById('shape-backdrop');
  SEAMS.forEach(function (st, g) {{
    reorderShapes(tl, shapeBackdrop, '{V["seed"]}', st - 0.4, g + 1);
    const gx = -60 * (g + 1);
    tl.to('#ground', {{ backgroundPosition: gx + 'px 0px, ' + gx + 'px 0px', duration: 0.8, ease: 'power3.inOut' }}, st - 0.4);
    tl.to('#blob', {{ x: (seedHash('{V["seed"]}-blob-' + g) - 0.5) * 220, y: (seedHash('{V["seed"]}-bloy-' + g) - 0.5) * 120, rotation: (seedHash('{V["seed"]}-blor-' + g) - 0.5) * 16, duration: 1.0, ease: 'power2.inOut' }}, st - 0.4);
  }});

  // chapter HUD
{chr(10).join(js_steps)}
  // source line
{chr(10).join(js_src)}

  // closing question, word by word on the spoken words
{js_cta}

  tl.set({{}}, {{}}, TOTAL_DURATION);
  window.__timelines["{COMP_ID}"] = tl;

  // <seams:auto>
  // </seams:auto>
</script>
</body>
</html>
"""
io.open(os.path.join(ROOT, "index.html"), "w", encoding="utf8", newline="\n").write(html)
print(f"index.html: {len(ORDER)} scenes, {len(ledger['seams'])} seams, total {TOTAL}s, skin {SKIN}, "
      f"narration {'yes' if have_narr else 'no (synthetic timing)' if T.SYNTHETIC else 'missing'}")

r = subprocess.run(["node", os.path.join(HERE, "seam_stamp.mjs"), "--ledger", "ledger.json", "--write", "index.html"],
                   cwd=ROOT, capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip())
if r.returncode:
    sys.exit("seam_stamp.mjs failed")
if WARN:
    print("WARN:\n  " + "\n  ".join(WARN))
    sys.exit(1)
