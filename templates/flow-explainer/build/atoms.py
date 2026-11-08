"""atoms.py — the explainer atoms of the flow-explainer style, on top of flow.py (living diagrams) and
explain.py (headlines, anatomy, fband, counters). Proven on a 4.5-minute decision briefing; every atom
takes scene-local times from S.p("phrase"), never literal seconds.

  motion       appear / out / to / grow_x / el / fill
  chips        chp (mono label <= 4 words) / strike_bar / recommend / open_q / example_tag / draft_stamp
  chapter      chapter_card (the "D1 · Entrance" card top-right) / title_xl (frame-0 title)
  deck         deck -> deck_jostle / deck_row / deck_hop       (a pile of cards that files into a row)
  board        board -> board_in / board_lit / board_rect      (grouped cards: decisions, steps, options)
  timeline     track / ticks / ticks_to / events / span / span_to / target
  scan         pages / lens / lens_sweep / scan                (read page by page until a hit)
  dials        dials / dials_turn                              (per-customer / per-item settings)
  values       value_card / row_mark                           (before/after numbers, a ledger)
  plan         gantt / gantt_bar                               (who switches what, when)
  capacity     capacity                                        (parts vs a limit, overflow stripes)
  bars         bar                                             (progress / partial / equivalence)
  list         list_card / list_fail / cross

Colour meaning (keep it in every video): accent-1 = the subject / platform, flow = things in motion,
ok = recommended / fine, bad = missing / broken / conflict, warn (dashed) = open question,
draft (dashed violet) = derived / example / not measured.
"""
import kit
from kit import esc, tok
from flow import r2, tw_inter, tw_mono
from explain import rgba

# ------------------------------------------------------------------ language
STRINGS = {
    "en": {"rec": "RECOMMENDED", "open": "OPEN", "example": "EXAMPLE", "derived": "DERIVED",
           "not_measured": "NOT MEASURED", "decision": "DECISION", "page": "Page"},
    "de": {"rec": "EMPFOHLEN", "open": "OFFEN", "example": "BEISPIEL", "derived": "ABGELEITET",
           "not_measured": "NICHT GEMESSEN", "decision": "ENTSCHEIDUNG", "page": "Seite"},
}
_LANG = {"code": "en", "over": {}}


def set_lang(code, overrides=None):
    """VIDEO["lang"] picks the marker words (en, de; others fall back to en); VIDEO["strings"] overrides."""
    _LANG["code"] = code if code in STRINGS else "en"
    _LANG["over"] = dict(overrides or {})


def L(key):
    return _LANG["over"].get(key) or STRINGS[_LANG["code"]].get(key) or STRINGS["en"][key]


def setup(video):
    """call once right after VIDEO in video_scenes.py: skin, topic palette, marker language"""
    kit.set_skin(video.get("skin", "paper"))
    kit.set_palette(video.get("palette"))
    set_lang(video.get("lang", "en"), video.get("strings"))


# ------------------------------------------------------------------ CSS (literal font names, colours via tokens)
ATOMS_CSS = """
      .ttl { position:absolute; text-align:center; font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:124px; line-height:1.05; letter-spacing:-4px; color:var(--text); white-space:nowrap; transform-origin:50% 0; }
      .ttl .kw { color:var(--accent-1); }
      .dcd { position:absolute; height:80px; box-sizing:border-box; border-radius:18px; background:var(--accent-1); color:var(--on-acc); display:flex; align-items:center; gap:18px; padding:0 28px 0 24px; box-shadow:var(--tile-shadow); z-index:12; white-space:nowrap; opacity:0; }
      .dcd b { font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:44px; letter-spacing:-1px; }
      .dcd span { font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:30px; }
      .rcd { position:absolute; box-sizing:border-box; border-radius:20px; background:var(--accent-1); color:var(--on-acc); box-shadow:var(--tile-shadow); padding:14px 18px; }
      .rcd b { display:block; font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:50px; line-height:56px; letter-spacing:-1.5px; }
      .rcd span { display:block; font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:22px; line-height:30px; white-space:nowrap; margin-top:12px; }
      .bcd { position:absolute; height:96px; box-sizing:border-box; border-radius:20px; background:var(--accent-1); color:var(--on-acc); display:flex; align-items:center; gap:24px; padding:0 30px; box-shadow:var(--tile-shadow); opacity:0; }
      .bcd b { font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:52px; letter-spacing:-1.5px; min-width:92px; }
      .bcd span { font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:32px; white-space:nowrap; }
      .bhd { position:absolute; height:50px; line-height:46px; box-sizing:border-box; padding:0 24px; border-radius:25px; background:var(--panel); border:2px solid var(--accent-1); color:var(--accent-1); font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:26px; white-space:nowrap; opacity:0; }
      .bgw { position:absolute; left:0; top:0; width:0; height:0; }
      .chp { position:absolute; box-sizing:border-box; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:24px; line-height:32px; letter-spacing:0.5px; padding:6px 14px; border-radius:10px; white-space:nowrap; background:var(--panel); color:var(--text); border:2px solid var(--line-2); opacity:0; z-index:6; }
      .chp.big { font-size:30px; line-height:38px; padding:8px 18px; font-weight:800; }
      .chp.acc { background:var(--accent-1); color:var(--on-acc); border-color:var(--accent-1); }
      .chp.ok { background:var(--ok); color:var(--on-ok); border-color:var(--ok); }
      .chp.bad { background:var(--bad); color:var(--on-bad); border-color:var(--bad); }
      .chp.flow { background:var(--flow); color:var(--on-flow); border-color:var(--flow); }
      .chp.ink { background:var(--text); color:var(--bg); border-color:var(--text); }
      .chp.warn { background:var(--panel); color:var(--warn); border:2px dashed var(--warn); }
      .chp.draft { background:var(--panel); color:var(--draft); border:2px dashed var(--draft); }
      .chp.ghost { background:var(--panel); color:var(--text-2); }
      .chp svg { display:inline-block; vertical-align:-3px; margin-right:8px; }
      .stk { position:absolute; height:5px; border-radius:3px; background:var(--bad); transform-origin:0 50%; transform:scaleX(0); z-index:9; }
      .trk { position:absolute; height:6px; border-radius:3px; background:var(--line-2); transform-origin:0 50%; transform:scaleX(0); }
      .tlb { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:24px; letter-spacing:2px; text-transform:uppercase; color:var(--text-2); white-space:nowrap; opacity:0; }
      .tmk { position:absolute; width:12px; height:46px; margin:-23px 0 0 -6px; border-radius:6px; background:var(--accent-1); opacity:0; }
      .evd { position:absolute; width:30px; height:38px; margin:-19px 0 0 -15px; border-radius:6px; background:var(--flow); box-shadow:0 0 14px rgba(var(--flow-rgb),0.6); opacity:0; }
      .evd i { position:absolute; left:7px; right:7px; height:3px; border-radius:2px; background:rgba(255,255,255,0.9); }
      .spn { position:absolute; height:12px; border-radius:6px; background:var(--bad); transform-origin:0 50%; transform:scaleX(0); }
      .tgt { position:absolute; width:0; border-left:4px dashed var(--ok); opacity:0; }
      .pg { position:absolute; width:300px; height:380px; box-sizing:border-box; border-radius:18px; background:var(--panel); border:3px solid var(--wire); box-shadow:var(--tile-shadow); opacity:0; }
      .pg .pt { position:absolute; left:0; right:0; top:16px; text-align:center; font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:26px; color:var(--text); }
      .pg .pr { position:absolute; left:24px; right:24px; height:24px; border-radius:6px; background:var(--track); border:2px solid var(--line); box-sizing:border-box; }
      .pg .pf { position:absolute; left:0; right:0; bottom:14px; text-align:center; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:22px; color:var(--text-2); }
      .dots { position:absolute; font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:64px; color:var(--text-3); opacity:0; }
      .lens { position:absolute; left:0; top:0; width:96px; height:96px; margin:-48px 0 0 -48px; opacity:0; z-index:8; color:var(--accent-1); }
      .dial { position:absolute; width:160px; height:160px; box-sizing:border-box; border-radius:50%; border:6px solid var(--wire); background:var(--panel); box-shadow:var(--tile-shadow); opacity:0; }
      .dial i { position:absolute; left:71px; top:16px; width:6px; height:58px; border-radius:3px; background:var(--accent-1); transform-origin:50% 100%; }
      .dial b { position:absolute; left:64px; top:64px; width:20px; height:20px; border-radius:50%; background:var(--accent-1); }
      .dlb { position:absolute; width:220px; text-align:center; font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:26px; color:var(--text); opacity:0; }
      .icard { position:absolute; box-sizing:border-box; border-radius:18px; background:var(--panel); border:3px solid var(--wire); box-shadow:var(--tile-shadow); padding:16px 22px 12px; opacity:0; }
      .icard .ih { font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:22px; letter-spacing:2px; color:var(--text-2); margin-bottom:8px; }
      .icard .ir { height:54px; line-height:54px; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:27px; color:var(--text); border-top:2px solid var(--line); padding:0 10px; border-radius:6px; white-space:nowrap; display:flex; justify-content:space-between; gap:24px; }
      .icard .ir.sum { font-weight:800; border-top:3px solid var(--wire); }
      .gbar { position:absolute; height:64px; box-sizing:border-box; border-radius:14px; transform-origin:0 50%; transform:scaleX(0); font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:24px; line-height:64px; color:#FFFFFF; padding-left:18px; white-space:nowrap; overflow:hidden; }
      .gdash { position:absolute; height:64px; box-sizing:border-box; border-radius:14px; border:3px dashed var(--line-2); font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:24px; line-height:58px; padding-left:18px; color:var(--text-2); opacity:0; white-space:nowrap; background:var(--panel); }
      .gdash.bad { border-color:var(--bad); color:var(--bad); }
      .glb { position:absolute; font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:30px; color:var(--text); white-space:nowrap; opacity:0; }
      .gcol { position:absolute; width:0; border-left:3px dashed var(--line); opacity:0; }
      .cap { position:absolute; height:68px; box-sizing:border-box; transform-origin:0 50%; transform:scaleX(0); font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:24px; line-height:68px; color:#FFFFFF; text-align:left; padding-left:20px; white-space:nowrap; overflow:hidden; }
      .capf { position:absolute; box-sizing:border-box; border-radius:20px; border:3px dashed var(--line-2); opacity:0; }
      .lim { position:absolute; width:6px; border-radius:3px; background:var(--bad); transform-origin:50% 0; transform:scaleY(0); z-index:5; }
      .ovr { position:absolute; height:68px; border-radius:0 14px 14px 0; transform-origin:0 50%; transform:scaleX(0); z-index:4; }
      .loop { position:absolute; opacity:0; color:var(--text-2); }
      .pbar { position:absolute; height:44px; box-sizing:border-box; border-radius:22px; border:3px solid var(--line-2); background:var(--panel); opacity:0; overflow:hidden; }
      .pbar i { position:absolute; left:0; top:0; bottom:0; border-radius:20px 0 0 20px; transform-origin:0 50%; transform:scaleX(0); }
      .blb { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:24px; letter-spacing:2px; color:var(--text-2); white-space:nowrap; opacity:0; }
      .lcard { position:absolute; box-sizing:border-box; border-radius:20px; background:var(--accent-1); border:4px solid var(--accent-1); box-shadow:var(--tile-shadow); opacity:0; }
      .lcard .lh { position:absolute; left:26px; top:20px; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:24px; letter-spacing:2px; color:var(--on-acc); white-space:nowrap; }
      .lcard i { position:absolute; left:26px; right:26px; height:24px; border-radius:6px; background:rgba(255,255,255,0.32); }
      .lx { position:absolute; width:150px; height:150px; opacity:0; z-index:7; }
"""
kit.COMMON_CSS = kit.COMMON_CSS + ATOMS_CSS


# ------------------------------------------------------------------ icons
def check_svg(px=22, color="#FFFFFF"):
    return (f'<svg viewBox="0 0 24 24" width="{px}" height="{px}"><path d="M4 12.5l5 5L20 6.5" fill="none" stroke="{color}" '
            f'stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def lens_svg():
    return ('<svg viewBox="0 0 100 100" width="96" height="96"><circle cx="42" cy="42" r="27" fill="rgba(var(--accent-rgb),0.10)" '
            'stroke="currentColor" stroke-width="8"/><path d="M62 62l26 26" stroke="currentColor" stroke-width="12" stroke-linecap="round"/></svg>')


def loop_svg(px=96):
    return (f'<svg viewBox="0 0 100 100" width="{px}" height="{px}"><path d="M78 50a28 28 0 1 1-9-20.6" fill="none" stroke="currentColor" '
            'stroke-width="8" stroke-linecap="round"/><path d="M72 14v18H54" fill="none" stroke="currentColor" stroke-width="8" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def cross_svg(px=150, color=None):
    c = color or tok("bad")
    return (f'<svg viewBox="0 0 100 100" width="{px}" height="{px}"><path d="M18 18L82 82M82 18L18 82" stroke="{c}" '
            'stroke-width="13" stroke-linecap="round"/></svg>')


ON = {"accent-1": "on-acc", "flow": "on-flow", "ok": "on-ok", "bad": "on-bad"}


def on_fill(kind):
    """readable text colour (literal hex) on a fill of token `kind`"""
    return tok(ON[kind]) if kind in ON else "#FFFFFF"


# ------------------------------------------------------------------ motion helpers
def _sel(id_):
    return id_ if id_.startswith("#") or "," in id_ else "#" + id_


def appear(S, id_, t, how="pop"):
    """reveal an element hidden in the markup: pop | l | r | up | slam | fade"""
    s = _sel(id_)
    if how == "pop":
        S.J(f'pop("{s}", {r2(t)});')
    elif how == "l":
        S.J(f'inn("{s}", {r2(t)}, {{ x: -40, y: 0 }});')
    elif how == "r":
        S.J(f'inn("{s}", {r2(t)}, {{ x: 40, y: 0 }});')
    elif how == "up":
        S.J(f'inn("{s}", {r2(t)}, {{ y: 24 }});')
    elif how == "slam":
        S.J(f'slam("{s}", {r2(t)}, 0);')
    else:
        S.J(f'tl.fromTo("{s}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, immediateRender: false }}, {r2(t)});')


def out(S, sel_, t, d=0.3):
    S.J(f'tl.to("{sel_}", {{ opacity: 0, duration: {d}, ease: "power2.in" }}, {r2(t)});')


def to(S, sel_, t, props, d=0.45, ease="power2.out"):
    """tween transforms / opacity / colours (never left/top: animate x / y instead)"""
    S.J(f'tl.to("{sel_}", {{ {props}, duration: {d}, ease: "{ease}" }}, {r2(t)});')


def grow_x(S, sel_, t, d=0.7):
    S.J(f'tl.fromTo("{sel_}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {d}, ease: "power3.out", immediateRender: false }}, {r2(t)});')


def el(S, id_, cls, x, y, inner="", style="", attrs=""):
    S.add(f'<div id="{id_}" class="{cls}"{attrs} style="left:{x}px; top:{y}px; {style}">{inner}</div>')
    return id_


def fill(S, nid, t, hexc=None):
    """solid colour fill of a Flow node tile (icon + border turn white): the big, high-contrast state change
    a light skin needs (white-on-cream changes are invisible to a freeze check). nid = G.nid(key)."""
    c = hexc or tok("accent-1")
    S.J(f'tl.to("#{nid}", {{ "--c": "#FFFFFF", duration: 0.35 }}, {r2(t)});')
    S.J(f'tl.to("#{nid}-t", {{ backgroundColor: "{c}", duration: 0.35 }}, {r2(t)});')


def unfill(S, nid, t):
    """undo fill(): the tile goes back to its plain look (do it before G.fail / G.paint on a filled node)"""
    S.J(f'tl.to("#{nid}-t", {{ backgroundColor: "{tok("tile")}", duration: 0.3 }}, {r2(t)});')


# ------------------------------------------------------------------ chips
def chip_w(txt, big=False):
    return round(len(txt) * (18.5 if big else 14.9) + (40 if big else 32))


def words_of(txt):
    """words that count toward the label budget (separators like · = + → do not)"""
    return [w for w in txt.split() if any(ch.isalnum() for ch in w)]


def chp(S, id_, txt, x, y, kind="", t=None, big=False, how="pop", occl=False, center=False, icon=""):
    """mono label chip (<= 4 words). kind: "" acc ok bad flow ink warn draft ghost. Returns (x, w).
    occl=True when a strike_bar will cross it (lets the layout check accept the strike)."""
    if len(words_of(txt)) > 4:
        kit.WARN.append(f"chip {id_}: {len(words_of(txt))} words (max 4): {txt!r}")
    w = chip_w(txt, big) + (30 if icon else 0)
    if center:
        x = round(x - w / 2)
    oc = " data-layout-allow-occlusion" if occl else ""
    S.add(f'<div id="{id_}" class="chp {kind}{" big" if big else ""}"{oc} style="left:{x}px; top:{y}px;">{icon}{esc(txt)}</div>')
    if t is not None:
        appear(S, id_, t, how)
    return x, w


def strike_bar(S, id_, x, y, w, t, big=False):
    """red strike across a chip at (x, y, w): give the chip occl=True"""
    yy = y + (27 if big else 22)
    S.add(f'<div id="{id_}" class="stk" style="left:{x + 6}px; top:{yy}px; width:{w - 12}px;"></div>')
    S.J(f'strike("#{id_}", {r2(t)});')


def recommend(S, id_, x, y, t, txt=None):
    """the recommendation marker (green, check): one per recommendation, on the word 'recommended'"""
    return chp(S, id_, txt or L("rec"), x, y, "ok", t=t, big=True, icon=check_svg())


def open_q(S, id_, txt, x, y, t):
    """an open question (amber, dashed): OPEN · <what is open>"""
    return chp(S, id_, L("open") + " \u00b7 " + txt, x, y, "warn", t=t)


def example_tag(S, id_, x, y, t, txt=None):
    """violet dashed EXAMPLE tag: every made-up number on screen carries it"""
    return chp(S, id_, txt or L("example"), x, y, "draft", t=t)


def draft_stamp(S, id_, x, y, t, txt=None, rot=-4):
    """violet slammed stamp: NOT MEASURED / DERIVED / a calculation, on the word that says so"""
    from kit import stamp
    stamp(S, id_, txt or L("not_measured"), x, y, "draft", rot=rot, style="z-index:20;")
    S.J(f'slam("#{id_}", {r2(t)}, {rot});')


# ------------------------------------------------------------------ chapter card + title
def chapter_card(S, id_, num, name, t, t_out=None):
    """the chapter's card top-right (number + <= 3 words): replaces a sentence headline"""
    S.add(f'<div id="{id_}" class="dcd" style="right:96px; top:108px;"><b>{esc(num)}</b><span>{esc(name)}</span></div>')
    S.J(f'tl.fromTo("#{id_}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out", immediateRender: false }}, {r2(t)});')
    if t_out is not None:
        S.J(f'tl.to("#{id_}", {{ opacity: 0, x: 40, duration: 0.3, ease: "power2.in" }}, {r2(t_out)});')


def title_xl(S, id_, text, kw=(), y=150, fs=124, vis=True):
    """frame-0 title (<= 6 words), keywords in the accent. Visible in the markup (thumbnail-grade frame 0)."""
    kws = {k.lower() for k in kw}
    inner = " ".join(f'<span class="kw">{esc(w)}</span>' if w.lower().strip(".,:") in kws else esc(w) for w in text.split())
    op = "" if vis else " opacity:0;"
    S.add(f'<div id="{id_}" class="ttl" style="left:0; top:{y}px; width:1920px; font-size:{fs}px;{op}">{inner}</div>')


# ------------------------------------------------------------------ deck: a pile of cards that files into a row
def deck(S, id_, items, y=430, w=204, h=132, gap=12, scatter=None):
    """items = [(big, small)] e.g. [("D1", "Entrance"), ...]. The cards sit at their scatter positions
    (pile) in the markup; deck_row files them into one centred row. Returns the per-card (dx, dy)."""
    n = len(items)
    x0 = round(960 - (n * w + (n - 1) * gap) / 2)
    pile = scatter or [(250, 470), (560, 620), (880, 450), (1180, 640), (1470, 480), (380, 770), (1010, 800), (1560, 780),
                       (700, 520), (1300, 760)][:n]
    dxy = []
    for i, (big, small) in enumerate(items):
        fx_, sx, sy = x0 + i * (w + gap), pile[i][0], pile[i][1]
        dxy.append((fx_ - sx, y - sy))
        S.add(f'<div id="{id_}{i + 1}" class="rcd" style="left:{sx}px; top:{sy}px; width:{w}px; height:{h}px;">'
              f'<b>{esc(big)}</b><span>{esc(small)}</span></div>')
    return dxy


def deck_jostle(S, id_, n, t):
    """the pile shifts once (a large change in the opening seconds)"""
    jost = [(-46, 22, -6), (38, -30, 5), (-30, -24, 4), (44, 20, -5), (-40, 26, 6), (34, -24, -4), (-36, -20, 5), (42, 26, -6),
            (-30, 18, 4), (36, -22, -5)]
    for i in range(n):
        jx, jy, jr = jost[i % len(jost)]
        S.J(f'tl.to("#{id_}{i + 1}", {{ x: {jx}, y: {jy}, rotation: {jr}, duration: 0.55, ease: "back.out(1.6)" }}, {r2(t + i * 0.03)});')


def deck_row(S, id_, dxy, t, stagger=0.045):
    for i, (dx, dy) in enumerate(dxy):
        S.J(f'tl.to("#{id_}{i + 1}", {{ x: {dx}, y: {dy}, rotation: 0, duration: 0.75, ease: "power3.inOut" }}, {r2(t + i * stagger)});')


def deck_hop(S, id_, k, dxy, t):
    """card k (1-based) hops once in the row (pair it with G.pulse on the part it changes)"""
    dy = dxy[k - 1][1]
    S.J(f'tl.fromTo("#{id_}{k}", {{ y: {dy} }}, {{ y: {dy - 16}, duration: 0.15, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }}, {r2(t)});')


# ------------------------------------------------------------------ board: grouped cards
def board(S, id_, groups, y0, xs=None, w=520):
    """groups = [(group name, [(big, small), ...]), ...] in up to 3 columns. Cards get ids <id>-c<k> (1-based,
    running across groups), group wrappers <id>-g<i>, headers <id>-h<i>."""
    xs = xs or ([150, 700, 1250][:len(groups)] if len(groups) == 3 else [round(960 - len(groups) * (w + 30) / 2 + i * (w + 30) + 15) for i in range(len(groups))])
    k = 0
    for g, (name, cards) in enumerate(groups):
        S.add(f'<div id="{id_}-g{g}" class="bgw">')
        hw = round(tw_inter(name, 26) + 52)
        S.add(f'<div id="{id_}-h{g}" class="bhd" style="left:{round(xs[g] + (w - hw) / 2)}px; top:{y0}px;">{esc(name)}</div>')
        for j, (big, small) in enumerate(cards):
            k += 1
            S.add(f'<div id="{id_}-c{k}" class="bcd" style="left:{xs[g]}px; top:{y0 + 70 + j * 116}px; width:{w}px;">'
                  f'<b>{esc(big)}</b><span>{esc(small)}</span></div>')
        S.add("</div>")
    return xs


def board_in(S, id_, groups, t, step=0.07):
    k = 0
    for g, (_, cards) in enumerate(groups):
        S.J(f'tl.fromTo("#{id_}-h{g}", {{ opacity: 0, y: -14 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out", immediateRender: false }}, {r2(t + g * 0.1)});')
        for _ in cards:
            k += 1
            S.J(f'tl.fromTo("#{id_}-c{k}", {{ opacity: 0, y: 30, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }}, {r2(t + 0.15 + (k - 1) * step)});')


def board_lit(S, id_, n_groups, g, t, o=0.28):
    """light group g, dim the others (g=None lights all)"""
    for j in range(n_groups):
        to(S, f"#{id_}-g{j}", t, f"opacity: {1 if g is None or j == g else o}", d=0.4)


def board_rect(groups, g, y0, xs, w=520):
    """fband rect around group g"""
    n = len(groups[g][1])
    return (xs[g] - 22, y0 - 16, w + 44, 70 + n * 116 + 18)


# ------------------------------------------------------------------ timeline
def track(S, id_, label, x0, x1, y, t):
    """a horizontal time track with its label above (ids <id>-t, <id>-l)"""
    el(S, f"{id_}-l", "tlb", x0, y - 62, esc(label))
    S.add(f'<div id="{id_}-t" class="trk" style="left:{x0}px; top:{y - 3}px; width:{x1 - x0}px;"></div>')
    appear(S, f"{id_}-l", t, "fade")
    grow_x(S, f"#{id_}-t", t, 0.8)


def ticks(S, id_, xs, y, t, step=0.12, show=True):
    """run / check marks on a track (ids <id>0..)"""
    for i, x in enumerate(xs):
        el(S, f"{id_}{i}", "tmk", x, y)
        if show:
            appear(S, f"{id_}{i}", t + i * step)


def ticks_to(S, id_, xs_from, xs_to, t, d=0.8):
    """re-space the marks (a cadence change): moves along x, never 'left'"""
    for i, (a, b) in enumerate(zip(xs_from, xs_to)):
        to(S, f"#{id_}{i}", t, f"x: {b - a}", d=d, ease="power3.inOut")


def events(S, id_, xs, y, t, step=0.22):
    """event documents (flow colour) landing on a track"""
    for i, x in enumerate(xs):
        el(S, f"{id_}{i}", "evd", x, y, '<i style="top:9px;"></i><i style="top:17px;"></i><i style="top:25px;"></i>')
        appear(S, f"{id_}{i}", t + i * step)


def span(S, id_, x0, x1, y, t, d=1.0):
    """a worst-case gap bar under a track (red); span_to shrinks / recolours it"""
    S.add(f'<div id="{id_}" class="spn" style="left:{x0}px; top:{y}px; width:{x1 - x0}px;"></div>')
    grow_x(S, f"#{id_}", t, d)


def span_to(S, id_, frac, t, kind="ok", d=0.8):
    to(S, f"#{id_}", t, f'scaleX: {round(frac, 3)}, backgroundColor: "{tok(kind)}"', d=d, ease="power3.inOut")


def target(S, id_, x, y, h, t):
    """dashed green target line (the deadline / the promise)"""
    S.add(f'<div id="{id_}" class="tgt" style="left:{x - 2}px; top:{y}px; height:{h}px;"></div>')
    appear(S, id_, t, "fade")


# ------------------------------------------------------------------ scan: pages read one by one
def pages(S, id_, n, x0, y, gap=340, rows=8, foot="", title=None):
    """n page cards (ids <id>-p<i>, rows <id>-p<i>r<j>). Returns their x positions; reveal with appear."""
    xs = [x0 + i * gap for i in range(n)]
    for p, x in enumerate(xs):
        rr = "".join(f'<div id="{id_}-p{p}r{j}" class="pr" style="top:{70 + j * 34}px;"></div>' for j in range(rows))
        tt = (title or L("page")) + f" {p + 1}"
        ft = f'<div id="{id_}-p{p}f" class="pf">{esc(foot)}</div>' if foot else ""
        el(S, f"{id_}-p{p}", "pg", x, y, f'<div class="pt">{esc(tt)}</div>{rr}{ft}')
    return xs


def lens(S, id_):
    S.add(f'<div id="{id_}" class="lens">{lens_svg()}</div>')


def lens_sweep(S, id_, x0, x1, y, t, d=1.6):
    """a magnifier sweeps once across a diagram ("do we miss something?")"""
    lens(S, id_)
    S.J(f'tl.set("#{id_}", {{ x: {x0}, y: {y} }}, 0);')
    S.J(f'tl.to("#{id_}", {{ opacity: 1, duration: 0.2 }}, {r2(t)});')
    S.J(f'tl.to("#{id_}", {{ x: {x1}, duration: {d}, ease: "power1.inOut" }}, {r2(t)});')
    S.J(f'tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {r2(t + d)});')


def scan(S, id_, lens_id, xs, y, rows, t0, t1, stop):
    """the lens reads the pages row by row from t0 and stops on row stop=(page, row) at about t1; read rows
    tint, finished pages dim, the hit turns green. Returns the hit time."""
    lens(S, lens_id)
    seq = [(p, i) for p in range(len(xs)) for i in range(rows)]
    seq = seq[:seq.index(tuple(stop)) + 1]
    step = max(0.06, (t1 - t0) / len(seq))
    S.J(f'tl.set("#{lens_id}", {{ x: {xs[0] + 286}, y: {y + 82} }}, 0);')
    S.J(f'tl.to("#{lens_id}", {{ opacity: 1, duration: 0.2 }}, {r2(t0 - 0.25)});')
    a1, tint = tok("accent-1"), rgba(tok("accent-1"), 0.22)
    for j, (p, i) in enumerate(seq):
        tt = t0 + j * step
        S.J(f'tl.to("#{lens_id}", {{ x: {xs[p] + 286}, y: {y + 70 + i * 34 + 12}, duration: {round(step * 0.9, 2)}, ease: "power1.inOut" }}, {r2(tt)});')
        S.J(f'tl.to("#{id_}-p{p}r{i}", {{ backgroundColor: "{tint}", borderColor: "{a1}", duration: 0.15 }}, {r2(tt + step * 0.6)});')
        if i == rows - 1:
            S.J(f'tl.to("#{id_}-p{p}", {{ opacity: 0.45, duration: 0.3 }}, {r2(tt + step)});')
    t_hit = r2(t0 + len(seq) * step + 0.15)
    okc = tok("ok")
    p, i = stop
    S.J(f'tl.to("#{id_}-p{p}r{i}", {{ backgroundColor: "{okc}", borderColor: "{okc}", duration: 0.25 }}, {t_hit});')
    return t_hit


# ------------------------------------------------------------------ dials
def dials(S, id_, xs, y, labels, t, angles=None):
    """setting dials (ids <id>-d<i>, hands <id>-h<i>) with a label under each"""
    angles = angles or [(-60 + 90 * i) % 360 for i in range(len(xs))]
    for i, x in enumerate(xs):
        el(S, f"{id_}-d{i}", "dial", x - 80, y, f'<i id="{id_}-h{i}" style="transform:rotate({angles[i]}deg);"></i><b></b>')
        el(S, f"{id_}-dl{i}", "dlb", x - 110, y + 176, esc(labels[i]))
        appear(S, f"{id_}-d{i}", t + i * 0.12)
        appear(S, f"{id_}-dl{i}", t + 0.1 + i * 0.12, "fade")


def dials_turn(S, id_, angles, t):
    for i, a in enumerate(angles):
        S.J(f'tl.to("#{id_}-h{i}", {{ rotation: {a}, duration: 0.9, ease: "back.out(1.4)" }}, {r2(t + i * 0.12)});')


# ------------------------------------------------------------------ value card (numbers, a ledger, before/after)
def value_card(S, id_, x, y, head, rows, w=400, t=None, how="up", sum_last=False):
    """rows = [(name, value)] (ids <id>-r<i>). Label made-up values with example_tag."""
    inner = f'<div class="ih">{esc(head)}</div>' + "".join(
        f'<div id="{id_}-r{i}" class="ir{" sum" if sum_last and i == len(rows) - 1 else ""}"><span>{esc(a)}</span><span>{esc(b)}</span></div>'
        for i, (a, b) in enumerate(rows))
    el(S, id_, "icard", x, y, inner, style=f"width:{w}px;")
    if t is not None:
        appear(S, id_, t, how)


def row_mark(S, id_, i, t, kind="bad"):
    """tint row i of a value card (bad = the change that matters, warn = the surprise, acc = the result)"""
    c = tok(kind if kind != "acc" else "accent-1")
    S.J(f'tl.to("#{id_}-r{i}", {{ backgroundColor: "{rgba(c, 0.16)}", color: "{c}", duration: 0.35 }}, {r2(t)});')


# ------------------------------------------------------------------ plan (gantt)
def gantt(S, id_, cols, rows, t_cols, t_rows, x0=490, colw=420, y0=380, rowh=120, label_x=200):
    """column headers (phases) + row labels (workstreams) + dashed column separators.
    Returns geo for gantt_bar. cols / rows: lists of <= 3-word strings."""
    geo = {"x0": x0, "colw": colw, "y0": y0, "rowh": rowh}
    for i, txt in enumerate(cols):
        cx = x0 + colw * i + colw / 2
        wpx = round(tw_mono(txt, 24, 2))
        el(S, f"{id_}-h{i}", "tlb", round(cx - wpx / 2), y0 - 80, esc(txt))
        appear(S, f"{id_}-h{i}", t_cols + i * 0.12, "fade")
    for i in range(1, len(cols)):
        el(S, f"{id_}-v{i}", "gcol", x0 + colw * i - 20, y0 - 30, "", style=f"height:{rowh * len(rows) + 30}px;")
        appear(S, f"{id_}-v{i}", t_cols + 0.15, "fade")
    for i, txt in enumerate(rows):
        el(S, f"{id_}-r{i}", "glb", label_x, y0 + rowh * i + 12, esc(txt))
        appear(S, f"{id_}-r{i}", t_rows + i * 0.12, "l")
    return geo


def gantt_bar(S, id_, geo, r, c, text, t, kind="accent-1", dashed=False, span_cols=1):
    """a bar in row r, column c (grows on its word); dashed=True = waiting on a decision; kind="bad" + dashed = a demand"""
    x = geo["x0"] + geo["colw"] * c
    y = geo["y0"] + geo["rowh"] * r
    w = geo["colw"] * span_cols - 60
    if dashed:
        el(S, id_, "gdash" + (" bad" if kind == "bad" else ""), x, y, esc(text), style=f"width:{w}px;")
        appear(S, id_, t, "r")
    else:
        el(S, id_, "gbar", x, y, esc(text), style=f"width:{w}px; background:{tok(kind)}; color:{on_fill(kind)};")
        grow_x(S, f"#{id_}", t, 0.8)
    return (x, y, w)


# ------------------------------------------------------------------ capacity vs a limit
def capacity(S, id_, parts, limit, x0, y, unit, t_frame, label_fmt="{}"):
    """parts = [(text, value, kind, t)] stacked left to right; limit = (value, label, t). Bars past the limit
    get red overflow stripes. unit = px per value. Returns (x of the limit line, total)."""
    total = sum(p[1] for p in parts)
    el(S, f"{id_}-fr", "capf", x0 - 16, y - 16, "", style=f"width:{round(max(total, limit[0]) * unit * 1.04) + 32}px; height:100px;")
    appear(S, f"{id_}-fr", t_frame, "fade")
    x = x0
    for i, (txt, val, kind, t) in enumerate(parts):
        rad = ("14px 0 0 14px" if i == 0 else "0") if i < len(parts) - 1 else ("0 14px 14px 0" if i else "14px")
        el(S, f"{id_}-p{i}", "cap", x, y, esc(txt), style=f"width:{round(val * unit)}px; background:{tok(kind)}; color:{on_fill(kind)}; border-radius:{rad};")
        grow_x(S, f"#{id_}-p{i}", t, 0.8)
        x += round(val * unit)
    lv, ltxt, lt = limit
    xl = x0 + round(lv * unit)
    S.add(f'<div id="{id_}-lim" class="lim" style="left:{xl - 3}px; top:{y - 28}px; height:124px;"></div>')
    S.J(f'tl.fromTo("#{id_}-lim", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, ease: "power3.out", immediateRender: false }}, {r2(lt)});')
    chp(S, f"{id_}-lt", ltxt, xl, y - 88, "bad", t=lt + 0.1, center=True)
    if total > lv:
        b = tok("bad")
        stripes = f"repeating-linear-gradient(135deg, {rgba(b, 0.85)} 0 14px, {rgba(b, 0.6)} 14px 28px)"
        S.add(f'<div id="{id_}-ov" class="ovr" style="left:{xl}px; top:{y}px; width:{round((total - lv) * unit)}px; background:{stripes};"></div>')
        grow_x(S, f"#{id_}-ov", max(lt + 0.4, max(p[3] for p in parts) + 0.8), 0.5)   # after the bars are full
    return xl, total


# ------------------------------------------------------------------ bars (progress / partial / equivalence)
def bar(S, id_, x, y, w, frac, t, kind="ok", label=None, dashed=False, t_fill=None, d=0.9):
    """a rounded bar filled to frac (ids <id>, fill <id>-f, label <id>-l above-left)"""
    if label:
        el(S, f"{id_}-l", "blb", x, y - 44, esc(label))
        appear(S, f"{id_}-l", t, "fade")
    el(S, id_, "pbar", x, y, f'<i id="{id_}-f" style="width:{round(frac * 100)}%; background:{tok(kind)};"></i>',
       style=f"width:{w}px;" + (" border-style:dashed;" if dashed else ""))
    appear(S, id_, t, "fade")
    grow_x(S, f"#{id_}-f", t_fill if t_fill is not None else t + 0.2, d)


# ------------------------------------------------------------------ list card + cross
def list_card(S, id_, title, x, y, w=440, h=330, n=5, t=None):
    """a big accent card (a list, a feed, a report) that list_fail can break"""
    rows = "".join(f'<i style="top:{76 + k * 46}px;"></i>' for k in range(n))
    el(S, id_, "lcard", x, y, f'<div class="lh">{esc(title)}</div>{rows}', style=f"width:{w}px; height:{h}px;")
    if t is not None:
        appear(S, id_, t, "r")


def list_fail(S, id_, t, x, y, w=440, h=330):
    """the card turns red and gets crossed out (it does not exist / it breaks)"""
    b = tok("bad")
    S.J(f'tl.to("#{id_}", {{ backgroundColor: "{rgba(b, 0.08)}", borderColor: "{b}", duration: 0.4 }}, {r2(t)});')
    S.J(f'tl.to("#{id_} i", {{ opacity: 0.25, duration: 0.4 }}, {r2(t)});')
    S.J(f'tl.to("#{id_} .lh", {{ color: "{b}", duration: 0.4 }}, {r2(t)});')
    cross(S, f"{id_}-x", x + w / 2 - 75, y + h / 2 - 75 + 20, t + 0.1)


def cross(S, id_, x, y, t, px=150):
    el(S, id_, "lx", round(x), round(y), cross_svg(px), style=f"width:{px}px; height:{px}px;")
    appear(S, id_, t)
