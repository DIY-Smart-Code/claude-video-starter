"""flow-explainer scene kit: the Stage (one scene file), evidence / terminal / code components and text atoms,
skinned by tokens/flow-<skin>.css plus the per-video palette (VIDEO["palette"] -> set_palette).

Diagram verbs live in build/flow.py (living system diagrams) and build/explain.py (explainer atoms).

Colours come from tokens/flow-<skin>.css (CSS vars) with the video's palette applied on top,
every beat time is a phrase anchor (Stage.p), and every product surface is a REAL
capture (Ev / Br), recorded terminal output (Term), real code (Code), a real
recording (player) or a real file (paper). Motion graphics only point at them.

Kit verbs (Python):            what they emit
  Stage(sid, desk=False)        one scene file compositions/scene-<sid>.html
    .p(phrase, k, end)          scene-local time of word k of a unique phrase
    .g(id) / .ge() / .gout()    frame group + seam-aware exit (left | zin | zout | up)
    .cam(t, scale, x, y)        camera move on the scene's #<sid>-world root
    .words(...)                 word-level reveal, each word on its spoken time, keyword colour
    .cursor / .click / .cursor_out   oversized macOS cursor (enters off-screen, click ignites)
  Ev(...)  .mark .spot .unspot .zoom .box .focus .scroll    evidence capture card
  Br(...)  .layer .go                                       browser frame + URL swap navigation
  Term(...) .cmd .out .lines .mark .focus .spot .clear      recorded terminal replay
  Code(...) .reveal .reveal_all .mark .strike               real code replay (line reveals)
  player(...)                   screen-recording slot (muted <video>, or labelled slate)
  bars(...) + grow()            thick data bars, value counts on its word
  counter(...) + count()        big-number counter (decimals / prefix / suffix)
  kick head chip stamp num lab  text atoms (kept short: visual-richness word budget)
  paper print_ tape label_tape rstamp pull   DESK exhibits (cream paper, Playfair italic)
JS verbs (inside every scene): inn off swap foc sweep pop drop slam dim strike arrive leave cnt grow click
"""
import html as _html
import io, json, os, re
import timing as T

ROOT = T.ROOT
EVD = os.path.join(ROOT, "assets", "evidence")
SKIN = "dark"
TOKENS = io.open(os.path.join(ROOT, "tokens", "flow-dark.css"), encoding="utf8").read()


def set_skin(name):
    """flow-explainer: pick the token file (tokens/flow-<name>.css: dark | paper). video_scenes.py
    calls it right after VIDEO; Stage.render and build.py read kit.TOKENS at render time."""
    global SKIN, TOKENS
    p = os.path.join(ROOT, "tokens", f"flow-{name}.css")
    if not os.path.exists(p):
        raise SystemExit(f"kit.set_skin: no tokens/flow-{name}.css (skins: dark, paper)")
    SKIN = name
    TOKENS = io.open(p, encoding="utf8").read()


def _hex_rgb(h):
    h = h.lstrip("#")
    return ", ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def _mix(a, b, f):
    """hex colour a mixed toward hex colour b by fraction f"""
    a, b = a.lstrip("#"), b.lstrip("#")
    return "#" + "".join("%02X" % round(int(a[i:i + 2], 16) * (1 - f) + int(b[i:i + 2], 16) * f) for i in (0, 2, 4))


PALETTE_KEYS = ("accent-1", "accent-2", "on-acc", "flow", "on-flow", "ifill", "bg", "ok", "on-ok", "bad", "on-bad",
                "warn", "draft", "node", "wire", "text")


def _lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def _contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def set_palette(pal):
    """Topic palette on top of the skin: VIDEO[\"palette\"] = {\"accent-1\": \"#0E4A6B\", \"flow\": \"#E2683A\", ...}.
    accent-1 = the subject / platform colour, flow = things in motion. accent-2 (darker accent), ifill (soft
    icon fill) and the -rgb companions are derived when not given. Keys: PALETTE_KEYS, 6-digit hex only."""
    global TOKENS
    pal = dict(pal or {})
    for k, v in pal.items():
        if k not in PALETTE_KEYS or not re.fullmatch(r"#[0-9A-Fa-f]{6}", v or ""):
            raise SystemExit(f"kit.set_palette: {k}={v!r} (keys {', '.join(PALETTE_KEYS)}; 6-digit hex)")
    if "accent-1" in pal:
        pal.setdefault("accent-2", _mix(pal["accent-1"], "#000000", 0.28))
        if SKIN == "paper":   # paper icons carry a soft accent fill; dark icons stay outlines (ifill = tile)
            pal.setdefault("ifill", _mix(pal["accent-1"], pal.get("bg") or tok("bg"), 0.80))
    for k, v in pal.items():
        TOKENS, n = re.subn(rf"(--{k}:\s*)#[0-9A-Fa-f]{{6}}", lambda m: m.group(1) + v.upper(), TOKENS)
        if not n:
            raise SystemExit(f"kit.set_palette: --{k} not in the {SKIN} tokens")
    for k, onk in (("accent-1", "on-acc"), ("flow", "on-flow"), ("ok", "on-ok"), ("bad", "on-bad")):
        if k in pal and onk not in pal:     # text colour on that fill: whichever of white / ink contrasts more
            ink = "#101318"
            best = "#FFFFFF" if _contrast(pal[k], "#FFFFFF") >= _contrast(pal[k], ink) else ink
            TOKENS = re.sub(rf"(--{onk}:\s*)#[0-9A-Fa-f]{{6}}", lambda m: m.group(1) + best, TOKENS)
    for k, rgbk in (("accent-1", "accent-rgb"), ("flow", "flow-rgb")):
        if k in pal:
            TOKENS = re.sub(rf"(--{rgbk}:\s*)[0-9, ]+;", lambda m: m.group(1) + _hex_rgb(pal[k]) + ";", TOKENS)


def tok(name):
    """literal hex of a token (GSAP colour tweens need literals, not var())"""
    m = re.search(rf"--{name}:\s*(#[0-9A-Fa-f]{{6}})", TOKENS)
    if not m:
        raise SystemExit(f"kit.tok: --{name} is not a 6-digit hex in the {SKIN} tokens")
    return m.group(1)


GEO = {}
_gp = os.path.join(ROOT, "research", "geometry.json")
if os.path.exists(_gp):
    GEO = json.load(io.open(_gp, encoding="utf8"))
WARN = []

MK_LIGHT = "rgba(var(--accent-rgb), 0.45)"     # marker on white captures (multiply)
MK_DARK = "rgba(var(--accent-rgb), 0.30)"      # marker on dark terminals / code
FONT_MONO = "'JetBrains Mono', ui-monospace, monospace"


def esc(s):
    return _html.escape(s, quote=False)


def fit(s, maxc):
    """crop a real line to the window width, marked with an ellipsis (never reworded)"""
    return s if len(s) <= maxc else s[:max(1, maxc - 1)].rstrip() + "…"


def rects(file, phrase):
    g = GEO.get(file) or {}
    r = g.get("phrases", {}).get(phrase)
    if not r:
        WARN.append(f"no rect: {file} :: {phrase}")
        return []
    return [list(map(float, x)) for x in r]


def dims(file):
    """pixel size of an evidence image (needs Pillow: pip install pillow; only evidence cards use it)"""
    from PIL import Image
    p = os.path.join(ROOT, file) if "/" in file else os.path.join(EVD, file)
    return Image.open(p).size


def src(file):
    return file if "/" in file else f"assets/evidence/{file}"


def _r2(x):
    return round(x, 2)


# =============================================================== evidence
class Ev:
    """Image card (capture or real still). x,y,w in scene px; clip = visible height; off = image px scrolled at t=0."""

    def __init__(self, S, id, file, x, y, w, clip=None, off=0, cls="ev h", style="", rot=0):
        self.S, self.id, self.file = S, id, file
        self.iw, self.ih = dims(file)
        self.x, self.y, self.w = x, y, w
        self.s = w / self.iw
        self.full_h = round(self.ih * self.s, 1)
        self.h = clip if clip else self.full_h
        self.off = off * self.s
        self.cls, self.style, self.rot = cls, style, rot
        self.kids = []
        self._nspot = 0

    def _r(self, r, pad=0):
        x, y, w, h = r
        return (round(x * self.s - pad, 1), round(y * self.s - pad, 1),
                round(w * self.s + 2 * pad, 1), round(h * self.s + 2 * pad, 1))

    def mark(self, phrase, t, seg=0.45, color=MK_LIGHT, spot=True):
        """marker sweep over a real sentence (rects from research/geometry.json) + auto spotlight"""
        rs = rects(os.path.basename(self.file), phrase)
        for i, r in enumerate(rs):
            x, y, w, h = self._r(r)
            mid = f"{self.id}-mk{len(self.kids)}"
            self.kids.append(f'<div id="{mid}" class="mk" style="left:{x}px; top:{round(y + h * 0.18, 1)}px; '
                             f'height:{round(h * 0.82, 1)}px; background:{color};"></div>')
            self.S.J(f'sweep("#{mid}", {_r2(t + i * seg)}, {w}, {seg});')
        if rs and spot:
            self.spot(rs, t)
        return self

    def spot(self, rs, t, pad=8):
        """dim the card except the given rects (image px); the hole moves spot to spot"""
        holes = "".join(f"M{x},{y}h{w}v{h}h{-w}Z" for x, y, w, h in (self._r(r, pad) for r in rs))
        n = self._nspot
        sid = f"{self.id}-sp{n}"
        self.kids.append(f'<svg id="{sid}" class="spot" width="{self.w}" height="{self.full_h}" viewBox="0 0 {self.w} {self.full_h}">'
                         f'<path fill-rule="evenodd" d="M0,0H{self.w}V{self.full_h}H0Z{holes}"/></svg>')
        self.S.J(f'tl.to("#{sid}", {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, {_r2(t - 0.15)});')
        if n:
            self.S.J(f'tl.to("#{self.id}-sp{n - 1}", {{ opacity: 0, duration: 0.35, ease: "power2.out" }}, {_r2(t - 0.15)});')
        self._nspot = n + 1
        return self

    def unspot(self, t):
        if self._nspot:
            self.S.J(f'tl.to("#{self.id}-sp{self._nspot - 1}", {{ opacity: 0, duration: 0.35 }}, {_r2(t)});')
        return self

    def zoom(self, t, cx, cy, k=1.5, dur=0.8):
        """Proof zoom: bring image point (cx, cy) to the window centre at scale k (k=1 resets)."""
        x = self.w / 2 - k * cx * self.s
        y = self.h / 2 + self.off - k * cy * self.s
        x = min(0, max(self.w - k * self.w, x))
        y = min(self.off, max(self.h - k * self.full_h + self.off, y))
        if k == 1:
            x, y = 0, -self.off
        self.S.J(f'tl.to("#{self.id} > .evw", {{ scale: {k}, x: {round(x, 1)}, y: {round(y, 1)}, transformOrigin: "0 0", duration: {dur}, ease: "power3.inOut" }}, {_r2(t)});')
        return self

    def zoom_to(self, phrase, t, k=1.6, dur=0.8):
        r = (rects(os.path.basename(self.file), phrase) or [None])[0]
        if r:
            self.zoom(t, r[0] + r[2] / 2, r[1] + r[3] / 2, k, dur)
        return self

    def box(self, rect, t0, t1=None, color="", pad=8, label=None, lpos="below"):
        """focus box at image-px rect; color '' accent, 'bad', 'ok', 'warn'"""
        x, y, w, h = self._r(rect, pad)
        fid = f"{self.id}-f{len(self.kids)}"
        lab = ""
        if label:
            ly = {"below": f"left:-5px; top:{round(h + 10, 1)}px;", "above": "left:-5px; top:-58px;",
                  "in": "left:10px; top:10px;"}[lpos]
            lab = f'<span class="flab {color}" style="{ly}">{esc(label)}</span>'
        self.kids.append(f'<div id="{fid}" class="foc {color}" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px;">{lab}</div>')
        self.S.J(f'foc("#{fid}", {_r2(t0)}{", " + str(_r2(t1)) if t1 else ""});')
        return self

    def focus(self, phrase, t0, t1=None, color="", pad=10, label=None, lpos="below"):
        r = (rects(os.path.basename(self.file), phrase) or [None])[0]
        if r is None:
            return self
        return self.box(r, t0, t1, color, pad, label, lpos)

    def add(self, html):
        self.kids.append(html)
        return self

    def scroll(self, t, img_px, dur=0.9):
        """tall-capture scroll: bring image row img_px to the top of the window"""
        y = max(-(img_px * self.s - self.off), self.h - self.full_h + self.off)
        self.S.J(f'tl.to("#{self.id} > .evw", {{ y: {round(min(y, 0), 1)}, duration: {dur}, ease: "power2.inOut" }}, {_r2(t)});')
        return self

    def html(self):
        rot = f" transform:rotate({self.rot}deg);" if self.rot else ""
        return (f'<div id="{self.id}" class="{self.cls}" style="left:{self.x}px; top:{self.y}px; width:{self.w}px; '
                f'height:{self.h}px;{rot} {self.style}"><div class="evw" data-layout-allow-overflow style="position:absolute; left:0; top:{-self.off}px; '
                f'width:{self.w}px; height:{self.full_h}px;"><img class="evi" src="{src(self.file)}" alt="" '
                f'style="width:{self.w}px; height:{self.full_h}px; top:0;">'
                + "".join(self.kids) + "</div></div>")


class Br:
    """Browser frame: traffic lights + URL bar; layers are Ev windows under the bar. go() navigates."""

    def __init__(self, S, id, x, y, w, h, cls="browser h", werbung=False):
        self.S, self.id, self.x, self.y, self.w, self.h, self.cls = S, id, x, y, w, h, cls
        self.layers, self.urls, self.cur = [], [], None
        self.werbung = werbung

    def layer(self, lid, file, url, off=0):
        first = not self.layers
        ev = Ev(self.S, lid, file, 0, 46, self.w, clip=self.h - 46, off=off, cls="bl" + ("" if first else " h"))
        self.layers.append(ev)
        self.urls.append((lid, url))
        if first:
            self.cur = lid
        return ev

    def go(self, t, lid):
        a = self.cur
        self.S.J(f'swap("#{a}", "#{lid}", {_r2(t)}, {{ y: 0, x: 60 }});')
        self.S.J(f'tl.to("#{a}-u", {{ opacity: 0, duration: 0.15 }}, {_r2(t)});')
        self.S.J(f'tl.to("#{lid}-u", {{ opacity: 1, duration: 0.25 }}, {_r2(t + 0.15)});')
        self.cur = lid

    def html(self):
        urls = "".join(f'<span id="{lid}-u" class="bu"{"" if i == 0 else " style=" + chr(34) + "opacity:0" + chr(34)}>{esc(u)}</span>'
                       for i, (lid, u) in enumerate(self.urls))
        wb = ('<span class="werb" style="color:#ffffff; background:#dc2626;">Werbung</span>' if self.werbung else "")
        return (f'<div id="{self.id}" class="{self.cls}" style="left:{self.x}px; top:{self.y}px; width:{self.w}px; height:{self.h}px;">'
                f'<div class="bbar"><i></i><i></i><i></i><div class="burl">{urls}</div>{wb}</div>'
                + "".join(l.html() for l in self.layers) + "</div>")


# =============================================================== terminal + code
class Term:
    """Terminal window replaying REAL recorded output. Lines appear on beats; cmd lines type on
    (clip width, steps(n), solid caret, no blink). When a page fills it scrolls; clear() starts a page."""

    def __init__(self, S, id, x, y, w, h, title="terminal", fs=28, cls="term h", werbung=False):
        self.S, self.id, self.x, self.y, self.w, self.h = S, id, x, y, w, h
        self.title, self.fs, self.cls, self.werbung = title, fs, cls, werbung
        self.lh = round(fs * 1.5, 1)
        self.maxl = int((h - 58 - 28) // self.lh)
        self.pages, self.under = [[]], [[]]
        self.k = self.n = 0
        self.where = {}
        self.tend = 0
        self.maxc = int((w - 26 - 20) // (0.6 * fs)) - 1
        self.scrolled = set()
        self._nspot = 0

    def _line(self, t, inner, cls="", pch=0):
        page = len(self.pages) - 1
        lid = f"{self.id}-l{self.n}"
        self.n += 1
        top = 14 + self.k * self.lh
        self.pages[-1].append(f'<div id="{lid}" class="tln {cls}" style="top:{top}px;">{inner}</div>')
        self.where[lid] = (page, self.k, pch)
        self.S.J(f'tl.set("#{lid}", {{ opacity: 1 }}, {_r2(t)});')
        if self.k >= self.maxl:
            self.scrolled.add(page)
            self.S.J(f'tl.to("#{self.id}-p{page}", {{ y: {-round((self.k - self.maxl + 1) * self.lh, 1)}, duration: 0.18, ease: "power2.out" }}, {_r2(t)});')
        self.k += 1
        return lid

    def cmd(self, t, text, prompt="$", dur=None):
        text = fit(text, self.maxc - len(prompt) - 1)
        n = len(text)
        w = round(n * 0.6 * self.fs + 2, 1)
        d = dur if dur else round(min(1.4, max(0.35, n * 0.028)), 2)
        tid = f"{self.id}-ty{self.n}"
        inner = f'<span class="pr">{esc(prompt)}</span><span id="{tid}" class="ty" style="width:0px;">{esc(text)}</span>'
        lid = self._line(t, inner, "cmd", len(prompt) + 1)
        self.S.J(f'tl.fromTo("#{tid}", {{ width: 0 }}, {{ width: {w}, duration: {d}, ease: "steps({max(1, n)})", immediateRender: false }}, {_r2(t)});')
        self.tend = _r2(t + d)
        return lid

    def _geo(self, lid, start=0, n=None):
        page, k, pch = self.where[lid]
        cw = 0.6 * self.fs
        return page, round(26 + (pch + start) * cw, 1), round(14 + k * self.lh, 1), round((n if n is not None else 40) * cw, 1)

    def mark(self, t, lid, start, n, color=MK_DARK, seg=0.4):
        page, x, y, w = self._geo(lid, start, n)
        mid = f"{self.id}-mk{len(self.under[page])}"
        self.under[page].append(f'<div id="{mid}" class="tmk" style="left:{x - 3}px; top:{y + 3}px; height:{round(self.lh - 6, 1)}px; background:{color};"></div>')
        self.S.J(f'sweep("#{mid}", {_r2(t)}, {round(w + 6, 1)}, {seg});')
        return mid

    def focus(self, t0, lid, t1=None, color="", label=None):
        page, k, pch = self.where[lid]
        y = round(14 + k * self.lh - 4, 1)
        fid = f"{self.id}-f{len(self.under[page])}"
        lab = f'<span class="flab {color}" style="left:-5px; top:{round(self.lh + 18, 1)}px;">{esc(label)}</span>' if label else ""
        self.under[page].append(f'<div id="{fid}" class="foc {color}" style="left:14px; top:{y}px; width:{self.w - 40}px; height:{round(self.lh + 8, 1)}px;">{lab}</div>')
        self.S.J(f'foc("#{fid}", {_r2(t0)}{", " + str(_r2(t1)) if t1 else ""});')
        return fid

    def spot(self, t, lids, pad=2):
        page = self.where[lids[0]][0]
        W, H = self.w, 2400
        holes = "".join(f"M8,{round(14 + self.where[l][1] * self.lh - pad, 1)}h{W - 16}v{round(self.lh + 2 * pad, 1)}h{-(W - 16)}Z" for l in lids)
        sid = f"{self.id}-sp{self._nspot}"
        self.under[page].append(f'<svg id="{sid}" class="spot tsp" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                                f'<path fill-rule="evenodd" d="M0,0H{W}V{H}H0Z{holes}"/></svg>')
        self.S.J(f'tl.to("#{sid}", {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, {_r2(t - 0.15)});')
        if self._nspot:
            self.S.J(f'tl.to("#{self.id}-sp{self._nspot - 1}", {{ opacity: 0, duration: 0.35 }}, {_r2(t - 0.15)});')
        self._nspot += 1
        return sid

    def out(self, t, text, cls=""):
        return self._line(t, esc(fit(text, self.maxc)) if text else "&nbsp;", cls)

    def lines(self, t0, texts, step=0.12, cls=""):
        ids, t = [], t0
        for x in texts:
            c = cls
            if isinstance(x, tuple):
                x, c = x
            ids.append(self.out(t, x, c))
            t += step
        return ids

    def clear(self, t):
        page = len(self.pages) - 1
        self.S.J(f'tl.to("#{self.id}-p{page}", {{ opacity: 0, duration: 0.2 }}, {_r2(t)});')
        self.pages.append([])
        self.under.append([])
        self.k = 0

    def html(self):
        wb = ('<span class="werb" style="color:#ffffff; background:#dc2626;">Werbung</span>' if self.werbung else "")
        def page_html(i, p):
            body = "".join(p)
            if i in self.scrolled:
                body = body.replace('" class="tln', '" data-layout-allow-occlusion class="tln')
            return f'<div id="{self.id}-p{i}" class="tpage">{"".join(self.under[i])}{body}</div>'
        pages = "".join(page_html(i, p) for i, p in enumerate(self.pages))
        return (f'<div id="{self.id}" class="{self.cls}" style="left:{self.x}px; top:{self.y}px; width:{self.w}px; height:{self.h}px; font-size:{self.fs}px; --lh:{self.lh}px;">'
                f'<div class="tbar"><i></i><i></i><i></i><span class="ttl">{esc(self.title)}</span>{wb}</div>'
                f'<div class="tbody">{pages}</div></div>')


class Code:
    """Editor panel replaying REAL code: numbered lines, revealed when named, marked, struck out."""

    def __init__(self, S, id, x, y, w, lines, name="file", fs=28, cls="code h", show=(), lang_colors=None):
        self.S, self.id, self.x, self.y, self.w = S, id, x, y, w
        self.lines, self.name, self.fs, self.cls = lines, name, fs, cls
        self.show = set(show)       # line indexes visible from the start
        self.colors = lang_colors or {}
        self.lh = round(fs * 1.55, 1)
        self.kids = []

    def ypos(self, i):
        return round(66 + i * self.lh, 1)

    def height(self):
        return round(66 + len(self.lines) * self.lh + 84, 1)   # room for a focus label under the last line

    def lid(self, i):
        return f"{self.id}-ln{i}"

    def reveal(self, t, i):
        self.S.J(f'inn("#{self.lid(i)}", {_r2(t)}, {{ y: 0, x: -18 }}, {{ duration: 0.35 }});')
        return self

    def reveal_all(self, t0, step=0.14, idx=None):
        for k, i in enumerate(idx if idx is not None else range(len(self.lines))):
            self.reveal(t0 + k * step, i)
        return self

    def mark(self, t, i, start=0, n=None, color=MK_DARK, seg=0.45):
        text = self.lines[i]
        n = min(n if n is not None else len(text) - start, self.maxc() - start)
        cw = 0.6 * self.fs
        mid = f"{self.id}-mk{len(self.kids)}"
        self.kids.append(f'<div id="{mid}" class="tmk" style="left:{round(96 + start * cw - 4, 1)}px; top:{round(self.ypos(i) + 2, 1)}px; height:{round(self.lh - 4, 1)}px; background:{color};"></div>')
        self.S.J(f'sweep("#{mid}", {_r2(t)}, {round(n * cw + 8, 1)}, {seg});')
        return self

    def focus(self, t0, i, t1=None, color="", label=None):
        """focus box around line i (+ label pill under it)"""
        fid = f"{self.id}-f{len(self.kids)}"
        y = round(self.ypos(i) - 4, 1)
        lab = f'<span class="flab {color}" style="left:-5px; top:{round(self.lh + 16, 1)}px;">{esc(label)}</span>' if label else ""
        self.kids.append(f'<div id="{fid}" class="foc {color}" style="left:10px; top:{y}px; width:{self.w - 30}px; height:{round(self.lh + 8, 1)}px;">{lab}</div>')
        self.S.J(f'foc("#{fid}", {_r2(t0)}{", " + str(_r2(t1)) if t1 else ""});')
        return self

    def strike(self, t, i, start=0, n=None):
        text = self.lines[i]
        n = min(n if n is not None else len(text) - start, self.maxc() - start)
        cw = 0.6 * self.fs
        sid = f"{self.id}-st{len(self.kids)}"
        self.kids.append(f'<div id="{sid}" class="strike" data-layout-allow-occlusion style="left:{round(96 + start * cw - 6, 1)}px; top:{round(self.ypos(i) + self.lh / 2 - 3, 1)}px; width:{round(n * cw + 12, 1)}px;"></div>')
        self.S.J(f'strike("#{sid}", {_r2(t)}); dim("#{self.lid(i)}", {_r2(t + 0.2)}, 0.45);')
        return self

    def maxc(self):
        return int((self.w - 96 - 24) // (0.6 * self.fs))

    def html(self):
        maxc = self.maxc()
        rows = "".join(
            f'<div id="{self.lid(i)}" class="cl" style="top:{self.ypos(i)}px;{"" if i in self.show else " opacity:0;"}">'
            f'<b>{i + 1}</b><span{(" style=" + chr(34) + "color:" + self.colors[i] + chr(34)) if i in self.colors else ""}>{esc(fit(l, maxc)) if l else "&nbsp;"}</span></div>'
            for i, l in enumerate(self.lines))
        return (f'<div id="{self.id}" class="{self.cls}" style="left:{self.x}px; top:{self.y}px; width:{self.w}px; height:{self.height()}px; font-size:{self.fs}px; --lh:{self.lh}px;">'
                f'<div class="tbar"><i></i><i></i><i></i><span class="ttl">{esc(self.name)}</span></div>'
                + "".join(self.kids) + rows + "</div>")


# =============================================================== stage
COMMON_CSS = """
      .h { opacity: 0; }
      .world { position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:50% 50%; }
      .fr { position:absolute; left:0; top:0; width:1920px; height:1080px; }
      .kick { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:26px; letter-spacing:4px; text-transform:uppercase; color:var(--accent-1); white-space:nowrap; }
      .kick .no { display:inline-block; margin-right:16px; padding:4px 12px; border-radius:6px; background:var(--text); color:var(--bg); letter-spacing:1px; }
      .head { position:absolute; font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:64px; letter-spacing:-1.6px; line-height:1.04; color:var(--text); white-space:nowrap; }
      .head em { font-style:normal; color:var(--accent-1); }
      .say { position:absolute; font-family:'Inter', system-ui, sans-serif; font-weight:900; letter-spacing:-2px; line-height:1.06; color:var(--text); }
      .wd { display:inline-block; margin-right:0.26em; opacity:0; }
      .wd.kw { color:var(--accent-1); }
      .wd.bad { color:var(--bad); } .wd.ok { color:var(--ok); } .wd.warn { color:var(--warn); }
      .chip { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:28px; padding:10px 22px; border-radius:12px; background:var(--panel-2); color:var(--text); border:2px solid var(--line-2); white-space:nowrap; }
      .chip.acc { background:var(--accent-1); color:var(--on-acc); border-color:transparent; }
      .chip.ok { background:var(--ok); color:#101318; border-color:transparent; } .chip.bad { background:var(--bad); color:#fff; border-color:transparent; }
      .chip.warn { background:var(--warn); color:#101318; border-color:transparent; } .chip.draft { background:var(--draft); color:#fff; border-color:transparent; }
      .ev { position:absolute; border-radius:14px; overflow:hidden; box-shadow:0 24px 60px rgba(0,0,0,0.55); border:2px solid var(--line-2); background:var(--ev-bg); }
      .ev img, .bl img { display:block; position:absolute; left:0; }
      .browser { position:absolute; border-radius:18px; overflow:hidden; border:2px solid var(--line-2); box-shadow:0 30px 80px rgba(0,0,0,0.6), 0 0 80px rgba(var(--accent-rgb),0.10); background:#FFFFFF; }
      .bbar { position:absolute; left:0; top:0; right:0; height:46px; background:#1B2130; z-index:6; display:flex; align-items:center; gap:10px; padding-left:16px; }
      .bbar i, .tbar i { width:14px; height:14px; border-radius:50%; background:#FF5F57; display:block; flex:none; }
      .bbar i:nth-child(2), .tbar i:nth-child(2) { background:#FEBC2E; } .bbar i:nth-child(3), .tbar i:nth-child(3) { background:#28C840; }
      .burl { position:relative; margin-left:18px; margin-right:16px; height:30px; flex:1; border-radius:8px; background:rgba(255,255,255,0.06); }
      .bu { position:absolute; left:14px; top:0; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:600; font-size:22px; line-height:30px; color:#C9C4BB; white-space:nowrap; }
      .bl { position:absolute; left:0; overflow:hidden; background:#FFFFFF; }
      .werb { position:absolute; right:16px; top:8px; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:22px; letter-spacing:1.5px; text-transform:uppercase; padding:3px 14px; border-radius:7px; z-index:9; }
      .mk { position:absolute; width:0; border-radius:4px; mix-blend-mode:multiply; z-index:4; }
      .spot { position:absolute; left:0; top:0; opacity:0; z-index:3; pointer-events:none; }
      .spot path { fill:var(--spot); }
      .foc { position:absolute; border:5px solid var(--accent-1); border-radius:10px; box-shadow:0 0 34px rgba(var(--accent-rgb),0.55); pointer-events:none; opacity:0; z-index:5; }
      .foc.bad { border-color:var(--bad); box-shadow:0 0 34px rgba(255,77,94,0.5); } .foc.ok { border-color:var(--ok); box-shadow:0 0 34px rgba(61,220,151,0.5); } .foc.warn { border-color:var(--warn); box-shadow:0 0 34px rgba(255,194,74,0.5); }
      .flab { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:26px; padding:6px 14px; border-radius:8px; background:var(--accent-1); color:var(--on-acc); white-space:nowrap; }
      .flab.bad { background:var(--bad); color:#fff; } .flab.ok { background:var(--ok); color:#101318; } .flab.warn { background:var(--warn); color:#101318; }
      .stamp { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:44px; letter-spacing:4px; text-transform:uppercase; padding:12px 30px; border:6px solid currentColor; border-radius:14px; white-space:nowrap; z-index:8; background:var(--stamp-bg); color:var(--accent-1); }
      .stamp.ok { color:var(--ok); } .stamp.bad { color:var(--bad); } .stamp.warn { color:var(--warn); } .stamp.draft { color:var(--draft); }
      .num { position:absolute; font-family:'Inter', system-ui, sans-serif; font-weight:900; color:var(--text); white-space:nowrap; line-height:1; letter-spacing:-4px; font-variant-numeric:tabular-nums; }
      .lab { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:26px; letter-spacing:2px; text-transform:uppercase; color:var(--text-2); white-space:nowrap; }
      .card { position:absolute; background:linear-gradient(180deg, var(--panel-2), var(--panel)); border:1.5px solid var(--line); border-radius:22px; box-shadow:0 24px 60px rgba(0,0,0,0.45); }
      .term, .code { position:absolute; border-radius:16px; overflow:hidden; background:#0E1219; border:2px solid var(--line); box-shadow:0 24px 60px rgba(0,0,0,0.55); font-family:'JetBrains Mono', ui-monospace, monospace; }
      .tbar { position:absolute; left:0; top:0; right:0; height:46px; background:#1B2130; display:flex; align-items:center; gap:10px; padding-left:16px; z-index:3; }
      .ttl { margin-left:16px; font-weight:600; font-size:22px; color:var(--text-2); white-space:nowrap; }
      .tbody { position:absolute; left:0; right:0; top:46px; bottom:0; overflow:hidden; }
      .tpage { position:absolute; left:0; right:0; top:0; }
      .tmk { position:absolute; width:0; border-radius:4px; z-index:1; }
      .tln { position:absolute; left:26px; right:20px; white-space:pre; overflow:hidden; line-height:var(--lh); color:#D8D4CC; opacity:0; font-weight:600; z-index:2; }
      .tln .pr { color:var(--accent-1); margin-right:0.6em; } .tln .ty { display:inline-block; overflow:hidden; vertical-align:top; white-space:pre; color:var(--text); }
      .tln.ok { color:var(--ok); } .tln.warn { color:var(--warn); } .tln.err { color:var(--bad); } .tln.dim { color:#7C776F; } .tln.hi { color:var(--accent-1); }
      .tsp { z-index:3; } .tsp path { fill:rgba(14,18,25,0.74); }
      .cl { position:absolute; left:0; right:20px; white-space:pre; line-height:var(--lh); font-weight:600; color:#D8D4CC; z-index:2; }
      .cl b { display:inline-block; width:70px; text-align:right; margin-right:26px; font-weight:600; color:#8E99B2; }
      .strike { position:absolute; height:6px; background:var(--bad); border-radius:3px; transform-origin:0 50%; transform:scaleX(0); z-index:4; }
      .player { position:absolute; border-radius:18px; overflow:hidden; background:#05070B; border:2px solid var(--line-2); box-shadow:0 30px 80px rgba(0,0,0,0.6); }
      .player .pbar { position:absolute; left:0; right:0; top:0; height:46px; background:#1B2130; display:flex; align-items:center; gap:10px; padding:0 16px; z-index:4; }
      .player .pbar i { width:14px; height:14px; border-radius:50%; background:#FF5F57; display:block; } .player .pbar i:nth-child(2) { background:#FEBC2E; } .player .pbar i:nth-child(3) { background:#28C840; }
      .player .plab { margin-left:16px; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:22px; letter-spacing:1.5px; color:var(--text-2); text-transform:uppercase; white-space:nowrap; }
      .player .pclock { margin-left:auto; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:22px; color:var(--text); font-variant-numeric:tabular-nums; }
      .player .pscreen { position:absolute; left:0; right:0; top:46px; bottom:12px; overflow:hidden; }
      .player .pprog { position:absolute; left:0; bottom:0; height:12px; width:0; background:var(--accent-1); z-index:4; }
      .player video { display:block; width:100%; height:100%; object-fit:cover; }
      .slate { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:22px;
        background:repeating-linear-gradient(135deg, rgba(139,123,255,0.10) 0 26px, rgba(139,123,255,0.03) 26px 52px), #0B0F18; }
      .slate .play { width:150px; height:150px; border-radius:50%; background:var(--text); display:flex; align-items:center; justify-content:center; }
      .slate .play svg { margin-left:14px; }
      .slate .big { font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:150px; letter-spacing:-4px; color:var(--text); line-height:1; font-variant-numeric:tabular-nums; }
      .slate .st { font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:30px; letter-spacing:3px; color:var(--draft); text-transform:uppercase; }
      .slate .sd { font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:600; font-size:26px; color:var(--text-2); }
      .bar-row { position:absolute; height:64px; }
      .bar-row .bl2 { position:absolute; left:0; top:-40px; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:26px; letter-spacing:2px; text-transform:uppercase; color:var(--text-2); white-space:nowrap; }
      .bar-row .trk { position:absolute; left:0; top:0; height:64px; border-radius:12px; background:var(--track); border:1.5px dashed var(--line); }
      .bar-row .fill { position:absolute; left:0; top:0; height:64px; border-radius:12px; transform-origin:0 50%; transform:scaleX(0); background:var(--accent-1); }
      .bar-row .fill.s2 { background:var(--s2); } .bar-row .fill.s3 { background:var(--s3); } .bar-row .fill.bad { background:var(--bad); } .bar-row .fill.ok { background:var(--ok); }
      .bar-row .val { position:absolute; top:6px; font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:48px; line-height:52px; color:var(--text); white-space:nowrap; opacity:0; font-variant-numeric:tabular-nums; }
      .cursor { position:absolute; left:0; top:0; width:134px; height:168px; z-index:20; filter:drop-shadow(0 6px 10px rgba(0,0,0,0.55)); pointer-events:none; }
      .ring { position:absolute; left:0; top:0; width:90px; height:90px; margin:-45px 0 0 -45px; border:6px solid var(--accent-1); border-radius:50%; opacity:0; z-index:19; }
"""

DESK_CSS = """
      .desk-mat { position:absolute; inset:0; background-color:var(--desk-mat);
        background-image: linear-gradient(rgba(244,241,234,0.045) 2px, transparent 2px), linear-gradient(90deg, rgba(244,241,234,0.045) 2px, transparent 2px),
          linear-gradient(rgba(244,241,234,0.09) 2px, transparent 2px), linear-gradient(90deg, rgba(244,241,234,0.09) 2px, transparent 2px);
        background-size: 60px 60px, 60px 60px, 300px 300px, 300px 300px; }
      .desk-wash { position:absolute; inset:0; pointer-events:none; background: radial-gradient(ellipse 60% 60% at 30% 25%, rgba(244,241,234,0.10), transparent 70%), radial-gradient(ellipse 80% 70% at 50% 50%, transparent 55%, rgba(0,0,0,0.55) 100%); }
      .paper { position:absolute; box-sizing:border-box; background:var(--paper); color:var(--ink); border-radius:4px; padding:44px 48px;
        box-shadow:0 34px 60px rgba(0,0,0,0.62), 0 5px 10px rgba(0,0,0,0.42); }
      .paper .eb { font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:24px; letter-spacing:3px; text-transform:uppercase; color:var(--ink-2); }
      .print { position:absolute; box-sizing:content-box; border:18px solid var(--paper-2); border-bottom-width:76px; border-radius:3px; overflow:visible; background:var(--paper-2);
        box-shadow:0 34px 60px rgba(0,0,0,0.62), 0 5px 10px rgba(0,0,0,0.42); }
      .print img { display:block; position:absolute; left:0; }
      .pcap { position:absolute; font-family:'Playfair Display', Georgia, serif; font-style:italic; font-size:34px; color:var(--ink); white-space:nowrap; z-index:6; }
      .tape { position:absolute; width:150px; height:42px; background:var(--tape); z-index:7; box-shadow:0 2px 4px rgba(0,0,0,0.2); }
      .ltape { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:36px; letter-spacing:5px; text-transform:uppercase; white-space:nowrap;
        color:var(--ink); background:var(--accent-1); padding:14px 24px; border-radius:5px; z-index:8;
        box-shadow: inset 0 -4px 0 rgba(0,0,0,0.18), inset 0 2px 0 rgba(255,255,255,0.35), 0 10px 18px rgba(0,0,0,0.45); }
      .ltape.bad { background:var(--bad); color:#fff; } .ltape.ok { background:var(--ok); } .ltape.warn { background:var(--warn); } .ltape.draft { background:var(--draft); color:#fff; }
      .rstamp { position:absolute; border:8px solid var(--stamp); color:var(--stamp); border-radius:14px; padding:10px 28px; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:64px; letter-spacing:5px; text-transform:uppercase; white-space:nowrap; z-index:9; mix-blend-mode:multiply; }
      .rstamp.ink { border-color:var(--ink); color:var(--ink); }
      .pull { position:absolute; font-family:'Playfair Display', Georgia, serif; font-style:italic; font-weight:400; font-size:58px; line-height:1.18; color:var(--paper); }
      .pull .wd { margin-right:0.24em; }
      .pull .wd.kw { color:var(--accent-1); }
      .paper .pull { color:var(--ink); } .paper .pull .wd.kw { color:var(--accent-2); }
"""

COMMON_JS = """
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      function inn(sel, t, from, to) {
        tl.fromTo(sel, Object.assign({ opacity: 0, y: 26 }, from || {}),
          Object.assign({ opacity: 1, y: 0, x: 0, scale: 1, duration: 0.55, ease: "power3.out", immediateRender: false }, to || {}), t);
      }
      function off(sel, t, d) { tl.to(sel, { opacity: 0, duration: d || 0.35, ease: "power2.in" }, t); }
      function swap(a, b, t, from) { off(a, t, 0.3); inn(b, t + 0.15, from || { y: 18 }); }
      function foc(sel, t0, t1) { inn(sel, t0, { y: 0, scale: 1.06 }, { duration: 0.35 }); if (t1) off(sel, t1); }
      function sweep(sel, t, w, d) { tl.fromTo(sel, { width: 0 }, { width: w, duration: d || 0.5, ease: "power2.out", immediateRender: false }, t); }
      function pop(sel, t) { tl.fromTo(sel, { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, t); }
      function drop(sel, t, rot) { tl.fromTo(sel, { opacity: 0, y: -90, rotation: (rot || 0) - 4 }, { opacity: 1, y: 0, rotation: rot || 0, duration: 0.55, ease: "power3.out", immediateRender: false }, t); }
      function slam(sel, t, rot) { tl.fromTo(sel, { opacity: 0, scale: 1.5, rotation: rot || 0 }, { opacity: 1, scale: 1, rotation: rot || 0, duration: 0.28, ease: "power4.in", immediateRender: false }, t); }
      function dim(sel, t, o) { tl.to(sel, { opacity: o === undefined ? 0.3 : o, duration: 0.4, ease: "power2.out" }, t); }
      function strike(sel, t) { tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out", immediateRender: false }, t); }
      function arrive(sel, t) { tl.fromTo(sel, { opacity: 0, scale: 1.18, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out", immediateRender: false }, t); }
      function leave(sel, t) { tl.to(sel, { opacity: 0, x: -120, duration: 0.4, ease: "power3.in" }, t); }
      function grow(sel, t, d) { tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: d || 0.9, ease: "power3.out", immediateRender: false }, t); }
      function cnt(sel, a, b, t, d, dec, pre, suf, fmt) {
        const o = { v: a };
        tl.to(o, { v: b, duration: d, ease: "power2.out", onUpdate: function () {
          const e = document.querySelector(sel); if (!e) return; const v = o.v;
          let s = fmt === "mmss" ? (Math.floor(v / 60) + ":" + String(Math.floor(v % 60)).padStart(2, "0"))
            : Number(v).toLocaleString("en-US", { minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0 });
          e.textContent = (pre || "") + s + (suf || ""); } }, t);
      }
      function click(cur, ring, p, t) {
        const x = p[0], y = p[1];
        tl.to(cur, { x: x, y: y, duration: 0.7, ease: "power3.out" }, t - 0.7);
        tl.to(cur, { scale: 0.84, duration: 0.1, ease: "power2.in", transformOrigin: "21% 14%" }, t);
        tl.to(cur, { scale: 1, duration: 0.22, ease: "power2.out", transformOrigin: "21% 14%" }, t + 0.1);
        tl.set(ring, { x: x + 20, y: y + 16 }, t - 0.01);
        tl.fromTo(ring, { opacity: 0.9, scale: 0.4 }, { opacity: 0, scale: 1.6, duration: 0.5, ease: "power2.out", immediateRender: false }, t);
      }
"""

CURSOR_SVG = ('<svg viewBox="0 0 32 40" width="134" height="168"><path d="M2 2 L2 32 L10 24.5 L15.5 37 L21 34.6 L15.6 22.4 L26 22.4 Z" '
              'fill="#FFFFFF" stroke="#0B0F18" stroke-width="2.2" stroke-linejoin="round"/></svg>')

_SPLIT = re.compile(r";\s+(?=(?:tl\.|inn|off|swap|foc|sweep|pop|drop|slam|dim|cnt|strike|arrive|leave|click|grow)\()")


class Stage:
    """One scene. Items go inside the scene's camera root #<sid>-world."""

    def __init__(self, sid, desk=False):
        self.sid, self.desk = sid, desk
        self.cut, self.dur = T.scene_cut(sid), T.scene_dur(sid)
        self.items, self.js, self.css = [], [], []
        self.tail_ok = None   # reason string when a ROOT overlay (e.g. #cta-question) carries the tail

    # ---------- time
    def p(self, phrase, k=0, end=False):
        """scene-local time of word k of a phrase that occurs once (k<0 counts from the end)"""
        return max(0.0, round(T.phrase_t(phrase, k, end) - self.cut, 2))

    # ---------- plumbing
    def J(self, line):
        for p_ in _SPLIT.split(line.strip()):
            p_ = p_.strip()
            if p_:
                self.js.append(p_ if p_.endswith(";") else p_ + ";")

    def add(self, x):
        self.items.append(x)
        return x

    # ---------- frame groups + camera
    def g(self, id, style=""):
        """open a frame group: one beat's elements entering and leaving as a unit"""
        self.add(f'<div id="{id}" class="fr" style="{style}">')
        return id

    def ge(self):
        self.add("</div>")

    def gout(self, id, t, how="left"):
        """frame exit inside a scene: 'left' cut-the-curve LEFT, 'zin' push, 'zout' pull, 'up' rise"""
        t = round(t, 2)
        if how == "left":
            self.J(f'tl.to("#{id}", {{ x: -230, opacity: 0, duration: 0.34, ease: "power4.in" }}, {_r2(t - 0.34)});')
        elif how == "zin":
            self.J(f'tl.to("#{id}", {{ scale: 1.2, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in" }}, {_r2(t - 0.3)});')
        elif how == "zout":
            self.J(f'tl.to("#{id}", {{ scale: 0.8, opacity: 0, duration: 0.3, ease: "power3.in" }}, {_r2(t - 0.3)});')
        elif how == "up":
            self.J(f'tl.to("#{id}", {{ y: -230, opacity: 0, duration: 0.34, ease: "power4.in" }}, {_r2(t - 0.34)});')

    def gin(self, id, t, how="left"):
        """matching in-scene entry for the next frame group (mid-flight, mirrored ease)"""
        t = round(t, 2)
        frm = {"left": "{ x: 230, opacity: 0.35 }", "up": "{ y: 230, opacity: 0.35 }",
               "zin": '{ scale: 0.8, opacity: 0.15, filter: "blur(10px)" }', "zout": "{ scale: 1.25, opacity: 0.15 }"}[how]
        to = '{ x: 0, y: 0, scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.45, ease: "power4.out", immediateRender: false }'
        self.J(f'tl.set("#{id}", {{ opacity: 0 }}, 0);')
        self.J(f'tl.fromTo("#{id}", {frm}, {to}, {t});')

    def cam(self, t, scale=1.0, x=0, y=0, dur=1.2, ease="power3.inOut"):
        """camera with intent: push toward (or pull back from) the subject"""
        self.J(f'tl.to("#{self.sid}-world", {{ scale: {scale}, x: {x}, y: {y}, duration: {dur}, ease: "{ease}" }}, {_r2(t)});')

    # ---------- word-level reveal
    def words(self, id, text, x, y, phrase=None, fs=96, kw=(), t0=None, step=0.14, cls="say", width=None, style="", kwcls="kw"):
        """Each word of `text` appears on its spoken time. With `phrase` (the spoken words, same
        count as text), word i lands on transcript word i of the phrase; else a 0.14 s stagger from t0.
        Keywords (case-insensitive, punctuation ignored) take the accent colour (or kwcls)."""
        toks = text.split()
        kws = {re.sub(r"[^a-z0-9]", "", k.lower()) for k in kw}
        spans = []
        times = []
        if phrase:
            i0, n = T._find(phrase)
            if n != len(toks):
                WARN.append(f"words {id}: text has {len(toks)} words, phrase has {n}; using stagger")
                phrase = None
            else:
                times = [max(0.0, round(T.wt(i0 + k) - self.cut, 2)) for k in range(n)]
        if not phrase:
            base = t0 if t0 is not None else 0.0
            times = [round(base + k * step, 2) for k in range(len(toks))]
        for k, w in enumerate(toks):
            c = kwcls if re.sub(r"[^a-z0-9]", "", w.lower()) in kws else ""
            spans.append(f'<span id="{id}-w{k}" class="wd {c}">{esc(w)}</span>')
        wd = f" width:{width}px;" if width else " white-space:nowrap;"
        self.add(f'<div id="{id}" class="{cls}" style="left:{x}px; top:{y}px; font-size:{fs}px;{wd} {style}">{"".join(spans)}</div>')
        for k, t in enumerate(times):
            self.J(f'tl.fromTo("#{id}-w{k}", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power4.out", immediateRender: false }}, {t});')
        return times

    # ---------- oversized cursor
    def cursor(self, id, x0=1500, y0=1260):
        """oversized macOS cursor, resting OFF-SCREEN (below frame) until its first click"""
        self.add(f'<div id="{id}" class="cursor" data-layout-allow-overflow>{CURSOR_SVG}</div><div id="{id}-r" class="ring"></div>')
        self.J(f'tl.set("#{id}", {{ x: {x0}, y: {y0} }}, 0);')

    def click(self, id, x, y, t):
        """tip lands on (x, y) at t, presses; the click IGNITES whatever is scheduled at t"""
        self.J(f'click("#{id}", "#{id}-r", [{x}, {y}], {_r2(t)});')

    def cursor_out(self, id, t, x=1500, y=1260):
        self.J(f'tl.to("#{id}", {{ x: {x}, y: {y}, duration: 0.6, ease: "power2.in" }}, {_r2(t)});')

    # ---------- component factories
    def ev(self, *a, **k):
        return self.add(Ev(self, *a, **k))

    def br(self, *a, **k):
        return self.add(Br(self, *a, **k))

    def term(self, *a, **k):
        return self.add(Term(self, *a, **k))

    def code(self, *a, **k):
        return self.add(Code(self, *a, **k))

    # ---------- render
    def render(self, title):
        body = "\n".join("      " + (x if isinstance(x, str) else x.html()) for x in self.items)
        css = TOKENS + COMMON_CSS + (DESK_CSS if self.desk else "") + "\n".join(self.css)
        js = "\n".join("      " + l for l in self.js)
        ground = '    <div class="desk-mat"></div><div class="desk-wash"></div>\n' if self.desk else ""
        return f"""<!--
  scene-{self.sid}.html - {title} (slot {self.dur}s, comp {self.cut}s).
  GENERATED by build/build.py from build/scenes.py. Do not hand-edit: change the scene
  function and rebuild. Beat times are transcript phrase anchors (build/timing.py).
-->
<template id="scene-{self.sid}-template">
  <div data-composition-id="scene-{self.sid}" data-start="0" data-width="1920" data-height="1080" style="position:absolute; inset:0; overflow:hidden; font-family:'Inter', system-ui, sans-serif; color:var(--text);">
    <style>{css}
    </style>
{ground}    <div id="{self.sid}-world" class="world">
{body}
    </div>
    <script src="assets/vendor/gsap.min.js"></script>
    <script>{COMMON_JS}
      const DUR = {self.dur};{(chr(10) + "      // scene-sync: blank-tail-ok (" + self.tail_ok + ")") if self.tail_ok else ""}
{js}
      tl.set({{}}, {{}}, DUR);
      window.__timelines["scene-{self.sid}"] = tl;
    </script>
  </div>
</template>
"""

    def write(self, title):
        p = os.path.join(ROOT, "compositions", f"scene-{self.sid}.html")
        io.open(p, "w", encoding="utf8", newline="\n").write(self.render(title))


# =============================================================== atoms
def _h(vis):
    return "" if vis else " h"


def kick(S, id, txt, x, y, no=None, vis=False, style=""):
    n = f'<span class="no">{esc(no)}</span>' if no else ""
    return S.add(f'<div id="{id}" class="kick{_h(vis)}" style="left:{x}px; top:{y}px; {style}">{n}{txt}</div>')


def head(S, id, txt, x, y, vis=False, fs=None, style=""):
    f = f" font-size:{fs}px;" if fs else ""
    return S.add(f'<div id="{id}" class="head{_h(vis)}" style="left:{x}px; top:{y}px;{f} {style}">{txt}</div>')


def chip(S, id, txt, x, y, c="", vis=False, style=""):
    return S.add(f'<div id="{id}" class="chip {c}{_h(vis)}" style="left:{x}px; top:{y}px; {style}">{txt}</div>')


def stamp(S, id, txt, x, y, c="", rot=-5, style=""):
    return S.add(f'<div id="{id}" class="stamp {c} h" style="left:{x}px; top:{y}px; transform:rotate({rot}deg); {style}">{esc(txt)}</div>')


def num(S, id, val, x, y, fs=200, color="var(--text)", vis=False, style=""):
    return S.add(f'<div id="{id}" class="num{_h(vis)}" style="left:{x}px; top:{y}px; font-size:{fs}px; color:{color}; {style}">{val}</div>')


def lab(S, id, txt, x, y, vis=False, style=""):
    return S.add(f'<div id="{id}" class="lab{_h(vis)}" style="left:{x}px; top:{y}px; {style}">{txt}</div>')


def div(S, id, cls, x, y, inner="", vis=False, style=""):
    return S.add(f'<div id="{id}" class="{cls}{_h(vis)}" style="left:{x}px; top:{y}px; {style}">{inner}</div>')


# =============================================================== data viz (published numbers only)
def bars(S, id, rows, x, y, w, gap=128, vmax=None):
    """rows: [(label, value, series_cls, display_suffix)] -> thick 64 px bars. Reveal each with grow()."""
    vmax = vmax or max(r[1] for r in rows)
    out = []
    for i, (label, val, cls, suf) in enumerate(rows):
        rid = f"{id}-{i}"
        fw = round(w * val / vmax, 1)
        S.add(f'<div id="{rid}" class="bar-row h" style="left:{x}px; top:{y + i * gap}px; width:{w}px;">'
              f'<div class="bl2">{esc(label)}</div><div class="trk" style="width:{w}px;"></div>'
              f'<div id="{rid}-f" class="fill {cls}" style="width:{fw}px;"></div>'
              f'<div id="{rid}-v" class="val" data-layout-allow-overflow style="left:{round(fw + 22, 1)}px;">0{esc(suf)}</div></div>')
        out.append((rid, val, suf))
    return out


def grow_bar(S, row, t, dec=0):
    rid, val, suf = row
    S.J(f'inn("#{rid}", {_r2(t - 0.25)}, {{ y: 0, x: -20 }}, {{ duration: 0.3 }});')
    S.J(f'grow("#{rid}-f", {_r2(t)}, 0.9);')
    S.J(f'tl.to("#{rid}-v", {{ opacity: 1, duration: 0.2 }}, {_r2(t + 0.1)});')
    S.J(f'cnt("#{rid}-v", 0, {val}, {_r2(t + 0.1)}, 0.8, {dec}, "", "{suf}");')


def counter(S, id, x, y, fs=220, color="var(--text)", start="0"):
    return num(S, id, start, x, y, fs, color)


def count(S, id, a, b, t, d=1.0, dec=0, pre="", suf=""):
    S.J(f'pop("#{id}", {_r2(t - 0.05)});')
    S.J(f'cnt("#{id}", {a}, {b}, {_r2(t)}, {d}, {dec}, "{pre}", "{suf}");')


# =============================================================== player (screen recordings)
PLAY_SVG = '<svg viewBox="0 0 24 24" width="64" height="64"><path d="M6 3 L21 12 L6 21 Z" fill="#0B0F18"/></svg>'


def player(S, id, x, y, w, h, t_in, file=None, dur=None, media_start=0, label="screen recording"):
    """Bezel for a muted screen recording (strip audio first: ffmpeg -an; segment-align to the
    narration windows). file=None renders a labelled PLACEHOLDER slate, never a sourceless <video>.
    Returns (play_point_xy, clock_id, progress_id) so a cursor click can ignite play."""
    if file:
        d = dur if dur else round(S.dur - t_in, 2)
        screen = (f'<video id="{id}-v" muted playsinline data-start="{_r2(t_in)}" data-duration="{_r2(d)}" '
                  f'data-media-start="{media_start}" src="assets/clips/{file}"></video>')
    else:
        screen = (f'<div id="{id}-slate" class="slate"><div id="{id}-btn" class="play">{PLAY_SVG}</div>'
                  f'<div id="{id}-big" class="big h" style="position:absolute; top:150px;">0:00</div>'
                  f'<div class="st">PLACEHOLDER: recording slot</div>'
                  f'<div class="sd">drop a muted clip into assets/clips/ and pass file=</div></div>')
    S.add(f'<div id="{id}" class="player h" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px;">'
          f'<div class="pbar"><i></i><i></i><i></i><span class="plab">{esc(label)}</span><span id="{id}-clk" class="pclock">0:00</span></div>'
          f'<div class="pscreen">{screen}</div><div id="{id}-prog" class="pprog"></div></div>')
    return (round(x + w / 2 - 6, 1), round(y + 46 + (h - 58) / 2 - 10, 1)), f"{id}-clk", f"{id}-prog"


def play(S, id, t, dur, slate=True):
    """play-state UI life: clock ticks and the progress bar fills for `dur` seconds"""
    if slate:   # placeholder slate: the play button hands over to a big running timecode
        S.J(f'tl.to("#{id}-btn", {{ scale: 0.6, opacity: 0, duration: 0.25, ease: "power2.in" }}, {_r2(t + 0.05)});')
        S.J(f'pop("#{id}-big", {_r2(t + 0.2)});')
        S.J(f'cnt("#{id}-big", 0, {round(dur)}, {_r2(t + 0.2)}, {_r2(dur)}, 0, "", "", "mmss");')
    S.J(f'cnt("#{id}-clk", 0, {round(dur)}, {_r2(t)}, {_r2(dur)}, 0, "", "", "mmss");')
    S.J(f'tl.fromTo("#{id}-prog", {{ width: 0 }}, {{ width: "100%", duration: {_r2(dur)}, ease: "none", immediateRender: false }}, {_r2(t)});')


# =============================================================== desk exhibits (accent chapters only)
def paper(S, id, x, y, w, h, inner, rot=0):
    return S.add(f'<div id="{id}" class="paper h" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px; transform:rotate({rot}deg);">{inner}</div>')


def print_(S, id, file, x, y, w, rot=0, caption=None):
    """a real screenshot printed and laid on the desk (supports Ev.mark / spot / focus)"""
    ev = Ev(S, id, file, x, y, w, cls="print h", rot=rot)
    if caption:
        ev.add(f'<div class="pcap" style="left:4px; top:{round(ev.full_h + 18, 1)}px;">{esc(caption)}</div>')
    return S.add(ev)


def tape(S, id, x, y, rot=-8):
    return S.add(f'<div id="{id}" class="tape h" style="left:{x}px; top:{y}px; transform:rotate({rot}deg);"></div>')


def label_tape(S, id, txt, x, y, kind="", rot=-2):
    return S.add(f'<div id="{id}" class="ltape {kind} h" style="left:{x}px; top:{y}px; transform:rotate({rot}deg);">{esc(txt)}</div>')


def rstamp(S, id, txt, x, y, kind="", rot=-9):
    return S.add(f'<div id="{id}" class="rstamp {kind} h" style="left:{x}px; top:{y}px; transform:rotate({rot}deg);">{esc(txt)}</div>')


def pull(S, id, text, x, y, w, phrase=None, kw=(), t0=None, fs=58):
    """Playfair italic pull-quote / aside on the desk, word by word"""
    return S.words(id, text, x, y, phrase=phrase, fs=fs, kw=kw, t0=t0, cls="pull", width=w)
