"""Style gate for a flow-explainer video: the rules that make every video look and move like the template.

    python build/check_style.py            # from the video folder, after python build/build.py

Checks (exit 1 on any ERROR):
  scene code (build/video_scenes.py)
    - SYSTEM(G) exists and is mounted (directly or through a helper / mini) in >= 60 % of the scenes
      and in the last scene: one persistent object, not a new diagram per scene
    - VIDEO["scenes"] and ALL list the same scenes in the same order
    - no literal-second beats: time arguments come from S.p("phrase") (+/- small offsets); a bare
      number > 1.0 s in a time slot is an error (>= 90 means "until the end" and is allowed)
  generated scenes (compositions/*.html)
    - label budgets: chips / node labels / tags / bar text <= 4 words, badges <= 3, chapter-card name <= 3,
      headlines / titles <= 6 (separators like · = + do not count)
    - something changes at least every 4 s inside every scene (WARN above 3 s)
    - no text under 20 px; fonts by literal name (never var()); no var() inside GSAP colour tweens
    - deterministic: no Math.random / Date.now / setTimeout / fetch
"""
import ast, glob, html.parser, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ERR, WRN = [], []

# ------------------------------------------------------------------ scene code
src = io.open(os.path.join(HERE, "video_scenes.py"), encoding="utf8").read()
tree = ast.parse(src)
funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}


def names_in(fn):
    return {n.id for n in ast.walk(fn) if isinstance(n, ast.Name)} | {n.attr for n in ast.walk(fn) if isinstance(n, ast.Attribute)}


uses_sys = {}


def mounts_system(name, seen=()):
    if name in uses_sys:
        return uses_sys[name]
    if name not in funcs or name in seen:
        return False
    refs = names_in(funcs[name])
    r = "SYSTEM" in refs or any(mounts_system(x, seen + (name,)) for x in refs if x in funcs and x != name)
    uses_sys[name] = r
    return r


all_list = []
for n in tree.body:
    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ALL" for t in n.targets):
        all_list = [e.id for e in n.value.elts if isinstance(e, ast.Name)]
if "SYSTEM" not in funcs:
    ERR.append("video_scenes.py: no SYSTEM(G) function (the one persistent object)")
elif all_list:
    sys_scenes = [s for s in all_list if mounts_system(s)]
    if len(sys_scenes) < 0.6 * len(all_list):
        ERR.append(f"SYSTEM is mounted in {len(sys_scenes)}/{len(all_list)} scenes (need >= 60 %): "
                   f"stage the same object, zoom into it, or mount it as mini() locator. Missing: {', '.join(s for s in all_list if s not in sys_scenes)}")
    if not mounts_system(all_list[-1]):
        ERR.append(f"the last scene ({all_list[-1]}) does not bring SYSTEM back (close on the object, e.g. a mini())")

sys.path.insert(0, HERE)
try:
    import scenes  # noqa: E402
    ids = [s["id"] for s in scenes.VIDEO["scenes"]]
    if ids != all_list:
        ERR.append(f"VIDEO['scenes'] {ids} != ALL {all_list} (same scenes, same order)")
except SystemExit as e:
    ERR.append(f"video_scenes.py does not import: {e}")
    ids = all_list

TIME_KW = {"t", "t0", "t1", "t_in", "t_out", "t_frame", "t_fill", "t_cols", "t_rows"}
# time slots come from the real signatures: every parameter named t / t0 / t1 / t_* of the atoms, the
# explain helpers, the Flow methods and the Stage methods (so the gate follows the engine automatically)
import inspect  # noqa: E402
import atoms, explain, flow as flow_mod, kit as kit_mod  # noqa: E402,E401
FN_POS, METH_POS = {}, {}
for mod in (atoms, explain, flow_mod, kit_mod):
    for nm, obj in vars(mod).items():
        if inspect.isfunction(obj) and getattr(obj, "__module__", "") == mod.__name__:
            FN_POS[nm] = [i for i, p in enumerate(inspect.signature(obj).parameters) if p in TIME_KW]
for cls in (flow_mod.Flow, kit_mod.Stage):
    for nm, obj in vars(cls).items():
        if inspect.isfunction(obj):
            METH_POS[nm] = [i - 1 for i, p in enumerate(inspect.signature(obj).parameters) if p in TIME_KW]


def lit_num(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)
    return None


for fname in all_list:
    fn = funcs.get(fname)
    if not fn:
        continue
    for c in ast.walk(fn):
        if not isinstance(c, ast.Call):
            continue
        if isinstance(c.func, ast.Name):
            nm, pos = c.func.id, FN_POS.get(c.func.id, [])
        elif isinstance(c.func, ast.Attribute):
            nm, pos = c.func.attr, METH_POS.get(c.func.attr, FN_POS.get(c.func.attr, []))
        else:
            continue
        slots = [c.args[i] for i in pos if i < len(c.args)] + [k.value for k in c.keywords if k.arg in TIME_KW]
        for a in slots:
            v = lit_num(a)
            if v is not None and 1.0 < v < 90:
                ERR.append(f"{fname}() line {c.lineno}: {nm}(...) at a literal {v:g} s; anchor it on a phrase: S.p(\"...\")")

# ------------------------------------------------------------------ generated scenes
LIMITS = {"chp": 4, "flb": 4, "fsb": 4, "fzl": 4, "fwl": 4, "tag": 4, "tlb": 4, "blb": 4, "glb": 4, "gbar": 4, "gdash": 4,
          "cap": 4, "dlb": 4, "bhd": 4, "fbg": 3, "hl": 6, "ttl": 6}


def count_words(s):
    return len([w for w in s.split() if any(ch.isalnum() for ch in w)])


class Labels(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.found = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        hit = next((c for c in cls if c in LIMITS), None)
        parent = self.stack[-1] if self.stack else None
        if tag == "span" and parent and parent[0] == "dcd":
            hit = "dcd-name"
        self.stack.append([hit or ("dcd" if "dcd" in cls else None), a.get("id", ""), ""])

    def handle_endtag(self, tag):
        if not self.stack:
            return
        hit, id_, txt = self.stack.pop()
        if hit and hit != "dcd":
            self.found.append((hit, id_, txt.strip()))
        if self.stack and self.stack[-1][0]:
            self.stack[-1][2] += " " + txt

    def handle_data(self, data):
        if self.stack:
            self.stack[-1][2] += data


TIME_RE = re.compile(r",\s*(-?\d+(?:\.\d+)?)\s*(?:,\s*-?\d+(?:\.\d+)?\s*)?\);\s*$")
for f in sorted(glob.glob(os.path.join(ROOT, "compositions", "scene-*.html"))):
    sid = os.path.basename(f)[6:-5]
    if sid not in ids:
        WRN.append(f"{os.path.basename(f)}: not in VIDEO['scenes'] (a stale file; move it out of compositions/)")
        continue
    h = io.open(f, encoding="utf8").read()
    tpl = h.split("<script>", 1)
    p = Labels()
    p.feed(tpl[0])
    for kind, id_, txt in p.found:
        lim = 3 if kind == "dcd-name" else LIMITS[kind]
        if txt and count_words(txt) > lim:
            ERR.append(f"{sid}: {kind} #{id_} has {count_words(txt)} words (max {lim}): {txt!r}")
    for m in re.finditer(r"font-size:\s*(\d+(?:\.\d+)?)px", tpl[0]):
        if float(m.group(1)) < 20:
            ERR.append(f"{sid}: font-size {m.group(1)}px (floor 20 px)")
            break
    if re.search(r"font-family:\s*var\(", h):
        ERR.append(f"{sid}: font-family via var() (use the literal name: 'Inter', 'JetBrains Mono')")
    if re.search(r"(Math\.random|Date\.now|setTimeout|setInterval|fetch\()", h):
        ERR.append(f"{sid}: non-deterministic call (Math.random / Date.now / timers / fetch)")
    js = tpl[1] if len(tpl) > 1 else ""
    for m in re.finditer(r"tl\.(?:to|fromTo|set)\([^;]*?(backgroundColor|color|borderColor|stroke|fill)\s*:\s*\"var\(", js):
        ERR.append(f"{sid}: GSAP tweens {m.group(1)} to a var(); use a literal hex (kit.tok)")
        break
    dur = float(re.search(r"const DUR = ([\d.]+);", js).group(1))
    times = sorted({float(m.group(1)) for line in js.splitlines() for m in [TIME_RE.search(line.strip())] if m and 0 <= float(m.group(1)) <= dur})
    tail = 3.5 if sid == ids[-1] else 0.0
    pts = [0.0] + [t for t in times if t <= dur - tail] + [dur - tail]
    gap, at = max(((b - a), a) for a, b in zip(pts, pts[1:]))
    if gap > 4.0:
        ERR.append(f"{sid}: nothing changes for {gap:.1f} s from {at:.1f} s (scene-local); add a beat on a phrase in that stretch")
    elif gap > 3.0:
        WRN.append(f"{sid}: {gap:.1f} s without a change from {at:.1f} s (scene-local); keep it under 3 s where you can")

idx = os.path.join(ROOT, "index.html")
if os.path.exists(idx) and re.search(r"(Math\.random|Date\.now|setTimeout|setInterval|fetch\()", io.open(idx, encoding="utf8").read()):
    ERR.append("index.html: non-deterministic call")

for w in WRN:
    print("WARN ", w)
for e in ERR:
    print("ERROR", e)
print(f"check_style: {len(ERR)} error(s), {len(WRN)} warning(s) in {len(ids)} scenes")
sys.exit(1 if ERR else 0)
