"""explain.py — explainer atoms for flow-explainer (the OpenRig / ByteByteGo grammar + the
house helpers, skin-aware).

Every atom SHOWS a concept instead of printing it; text inside them stays <= 4-6 words.

  headline / heads          top-centre headline "Term = meaning" that swaps on its words (<= 6 words)
  ladder / ladder_in / ladder_go   concept ladder: chips joined by arrows, the current one filled
  gloss / gloss_ghost / gloss_in   glossary rail: term + one-line meaning, ghosted then lit entry by entry
  anatomy / anat_in / anat_part    a string (address, key, command, model id) split into coloured parts
  win_card / sprawl / sprawl_pop / sprawl_grey / sprawl_order / sprawl_out   chaos -> order
  bubble                    speech bubble (<= 5 words) with a tail
  slam_plate                full-frame tint + 2 big lines: the ONE stakes moment per video
  meter / meter_in / meter_to      threshold bar (zones + ticks) with a sliding marker
  cells / cells_in / cells_fill    grid of slots (cache, context window, shards, queue)
  table / table_in / row_hl / table_scan   data table, sequential scan, row highlight
  road / road_in / road_go  wavy roadmap with numbered stops + a traveller (chapter map / what's next)
  recap / recap_row         card with check rows (the close)
  house helpers: tag / tag_row / cnt / cnl / tick / note_card / fband /
  brand_plate / fx / inn_ / mv / setp / sel
"""
import math, random
import kit
from kit import esc, WARN, tok, div
import flow as F
from flow import r1, r2, tw_inter, tw_mono, icon_svg


def rgba(hexc, a):
    h = hexc.lstrip("#")
    return f"rgba({int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}, {a})"


EX_CSS = """
      .hl { position:absolute; font-family:'Inter', system-ui, sans-serif; font-weight:900; letter-spacing:-1.4px; line-height:1.1; color:var(--text);
        white-space:nowrap; text-align:center; opacity:0; }
      .hl .eq { color:var(--accent-1); } .hl .kw { color:var(--accent-1); }
      .lad { position:absolute; box-sizing:border-box; height:56px; padding:0 22px; border-radius:14px; font-family:'JetBrains Mono', ui-monospace, monospace;
        font-weight:800; font-size:26px; line-height:52px; letter-spacing:1px; white-space:nowrap; background:var(--panel-2); color:var(--text);
        border:2px solid var(--line-2); opacity:0; }
      .lada { position:absolute; opacity:0; overflow:visible; }
      .lada path { fill:none; stroke:var(--text-2); stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }
      .gl { position:absolute; opacity:0; }
      .gl .gt { font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:42px; line-height:48px; color:var(--text); white-space:nowrap; }
      .gl .gd { font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:24px; line-height:32px; letter-spacing:0.5px; color:var(--text-2); white-space:nowrap; }
      .gl .gb { position:absolute; left:-26px; top:6px; width:8px; height:36px; border-radius:4px; background:var(--accent-1); }
      .anp { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; color:var(--text); white-space:pre; text-align:center;
        border-radius:10px; opacity:0; }
      .anb { position:absolute; overflow:visible; }
      .anb path { fill:none; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }
      .anl { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:24px; line-height:32px; letter-spacing:2px;
        text-transform:uppercase; padding:3px 12px; border-radius:8px; white-space:nowrap; opacity:0; }
      .spw { position:absolute; left:0; top:0; width:1920px; height:1080px; }
      .spi { position:absolute; opacity:0; }
      .wc { position:absolute; left:0; top:0; width:100%; height:100%; box-sizing:border-box; border-radius:14px; border:3px solid var(--wire);
        background:var(--panel); overflow:hidden; box-shadow:var(--tile-shadow); }
      .wc .wb { position:absolute; left:0; top:0; right:0; height:30px; }
      .wc .wb i { position:absolute; top:10px; width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,0.85); }
      .wc .wf { position:absolute; left:14px; top:44px; }
      .wc .wl { position:absolute; height:9px; border-radius:5px; background:var(--line-2); }
      .bub { position:absolute; box-sizing:border-box; border-radius:18px; border:3px solid var(--wire); background:var(--panel); padding:12px 22px;
        font-family:'Inter', system-ui, sans-serif; font-weight:800; color:var(--text); white-space:nowrap; opacity:0; z-index:9; }
      .bub svg { position:absolute; overflow:visible; }
      .slam { position:absolute; left:0; top:0; width:1920px; height:1080px; opacity:0; z-index:30; display:flex; flex-direction:column; align-items:center;
        justify-content:center; gap:6px; }
      .slam .slm { font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:128px; line-height:1.02; letter-spacing:-3px; color:#FFFFFF;
        text-transform:uppercase; white-space:nowrap; opacity:0; }
      .mtr { position:absolute; opacity:0; }
      .mtr .ms { position:absolute; top:0; height:48px; transform-origin:0 50%; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800;
        font-size:24px; line-height:48px; letter-spacing:1.5px; text-transform:uppercase; color:#101318; text-align:center; white-space:nowrap; overflow:hidden; }
      .mtr .mt { position:absolute; top:66px; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:22px; color:var(--text-2); white-space:nowrap; }
      .mtr .mk2 { position:absolute; left:0; top:-74px; width:0; height:0; }
      .mtr .mkc { position:absolute; left:0; top:0; transform:translateX(-50%); font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:26px;
        line-height:40px; padding:0 14px; border-radius:10px; background:var(--text); color:var(--bg); white-space:nowrap; }
      .mtr .mkt { position:absolute; left:-12px; top:42px; width:0; height:0; border-left:12px solid transparent; border-right:12px solid transparent; border-top:16px solid var(--text); }
      .cel { position:absolute; box-sizing:border-box; border-radius:10px; background:var(--track); border:2px solid var(--line-2); opacity:0; }
      .tbl { position:absolute; opacity:0; border-radius:16px; overflow:hidden; border:2px solid var(--line-2); background:var(--panel); }
      .tbl .th { position:absolute; left:0; right:0; top:0; background:var(--panel-2); }
      .tbl .tc { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; white-space:nowrap; color:var(--text); }
      .tbl .th .tc { font-weight:800; letter-spacing:1.5px; text-transform:uppercase; color:var(--text-2); }
      .tbl .tr { position:absolute; left:0; right:0; border-top:1.5px solid var(--line); }
      .tbl .thl { position:absolute; left:0; right:0; opacity:0; }
      .rd { position:absolute; left:0; top:0; overflow:visible; }
      .rd .rp { fill:none; stroke:var(--line-2); stroke-width:6; stroke-linecap:round; }
      .rst { position:absolute; box-sizing:border-box; width:64px; height:64px; margin:-32px 0 0 -32px; border-radius:50%; border:4px solid var(--wire);
        background:var(--panel); font-family:'Inter', system-ui, sans-serif; font-weight:900; font-size:30px; line-height:56px; text-align:center; color:var(--text); opacity:0; }
      .rlb { position:absolute; font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:28px; line-height:34px; color:var(--text); white-space:nowrap; opacity:0; }
      .rtv { position:absolute; left:0; top:0; width:34px; height:34px; margin:-17px 0 0 -17px; border-radius:50%; background:var(--accent-1);
        box-shadow:0 0 0 8px rgba(var(--accent-rgb),0.25), 0 0 26px rgba(var(--accent-rgb),0.8); opacity:0; z-index:4; }
      .rcp { position:absolute; box-sizing:border-box; border-radius:24px; background:var(--panel); border:2px solid var(--line-2); box-shadow:var(--tile-shadow); opacity:0; }
      .rcr { position:absolute; left:40px; opacity:0; }
      .rcr .rct { position:absolute; left:66px; top:0; font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:36px; line-height:48px; color:var(--text); white-space:nowrap; }
      .tag { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:28px; letter-spacing:2px; text-transform:uppercase;
        padding:8px 16px; border-radius:8px; white-space:nowrap; background:var(--text); color:var(--bg); border:2px solid transparent; }
      .tag.acc { background:var(--accent-1); color:var(--on-acc); } .tag.bad { background:var(--bad); color:#fff; }
      .tag.ok { background:var(--ok); color:#101318; } .tag.warn { background:var(--warn); color:#101318; } .tag.flow { background:var(--flow); color:#101318; }
      .tag.ghost { background:transparent; color:var(--text-2); border:2px solid var(--line-2); }
      .tag.lc { text-transform:none; letter-spacing:0.5px; }
      .cnt { position:absolute; font-family:'Inter', system-ui, sans-serif; font-weight:900; color:var(--text); white-space:nowrap; line-height:1; letter-spacing:-2px; font-variant-numeric:tabular-nums; }
      .cnl { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:26px; letter-spacing:2px; text-transform:uppercase; color:var(--text-2); white-space:nowrap; }
      .nc { position:absolute; box-sizing:border-box; border-radius:16px; background:#0E1219; border:2px solid var(--line-2); box-shadow:var(--tile-shadow); overflow:hidden; }
      .nc .nh { position:absolute; left:0; right:0; top:0; height:50px; background:#1B2130; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:24px; line-height:50px; padding-left:22px; color:#A7AFBD; white-space:nowrap; }
      .ncl { position:absolute; left:24px; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:28px; color:#F2F4F7; white-space:nowrap; }
      .ncl.bad { color:#FF6B7A; } .ncl.ok { color:#3DDC97; } .ncl.dim { color:#8A93A3; } .ncl.acc { color:var(--accent-1); }
      .plate { position:absolute; display:block; }
      .glow { position:absolute; border-radius:40px; background:radial-gradient(ellipse at center, rgba(var(--accent-rgb),0.5), rgba(var(--accent-rgb),0) 70%); opacity:0; }
      .rtag { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:22px; letter-spacing:2px; text-transform:uppercase;
        padding:4px 12px; border-radius:7px; white-space:nowrap; background:var(--panel-2); color:var(--text-2); border:2px solid var(--line-2); }
      .rtag i { display:inline-block; width:12px; height:12px; border-radius:50%; background:var(--bad); margin-right:10px; vertical-align:0; }
"""

if ".hl { position:absolute;" not in kit.COMMON_CSS:
    kit.COMMON_CSS = kit.COMMON_CSS + EX_CSS


# ================================================================ house helpers (skin-aware)
def fx(S, verb, sel_, t, *a):
    """any JS verb: fx(S, "pop", "#id", t) / fx(S, "slam", "#id", t, -8)"""
    extra = "".join(f", {x}" for x in a)
    S.J(f'{verb}("{sel_}", {r2(t)}{extra});')


def inn_(S, sel_, t, frm="{ y: 0, x: -24 }"):
    S.J(f'inn("{sel_}", {r2(t)}, {frm});')


def mv(S, sel_, t, props, d=0.6, ease="power3.inOut"):
    S.J(f'tl.to("{sel_}", {{ {props}, duration: {d}, ease: "{ease}" }}, {r2(t)});')


def setp(S, sel_, t, props):
    S.J(f'tl.set("{sel_}", {{ {props} }}, {r2(t)});')


def sel(ids):
    return ", ".join("#" + i for i in ids)


def off_(S, sel_, t, d=0.3):
    S.J(f'off("{sel_}", {r2(t)}, {d});')


def tag(S, id, txt, x, y, c="", vis=False, style=""):
    """FILLED chip (c = acc | ok | bad | warn | flow | ghost | lc). Never on top of evidence text."""
    return div(S, id, f"tag {c}".strip(), x, y, esc(txt), vis=vis, style=style)


def tag_w(txt):
    """generous width estimate of a .tag (28 px mono 800, ls 2, padding 16+16, border 2+2)"""
    return round(len(txt) * 19.3 + 40)


def tag_row(S, p, items, x, y, gap=30):
    """chips in a row, >= gap px apart. items = [(text, cls)] -> [(id, x, w)]"""
    out = []
    for i, (txt, c) in enumerate(items):
        tid = f"{p}{i}"
        tag(S, tid, txt, x, y, c)
        w = tag_w(txt)
        out.append((tid, x, w))
        x += w + gap
    return out


def cnt(S, id, x, y, start, fs=120, color="var(--text)", vis=False, style=""):
    return div(S, id, "cnt", x, y, start, vis=vis, style=f"font-size:{fs}px; color:{color}; {style}")


def cnl(S, id, x, y, txt, vis=False, style=""):
    return div(S, id, "cnl", x, y, txt, vis=vis, style=style)


def tick(S, id, a, b, t, d=1.0, dec=0, pre="", suf=""):
    S.J(f'cnt("#{id}", {a}, {b}, {r2(t)}, {d}, {dec}, "{pre}", "{suf}");')


def note_card(S, id, x, y, w, h, head, lines, vis=False):
    """dark file card (config / log / note): lines = [(text, cls)], cls '' | bad | ok | dim | acc"""
    inner = f'<div class="nh">{esc(head)}</div>' + "".join(
        f'<div id="{id}-l{i}" class="ncl {c}" style="top:{76 + i * 46}px;">{esc(t)}</div>' for i, (t, c) in enumerate(lines))
    return div(S, id, "nc", x, y, inner, vis=vis, style=f"width:{w}px; height:{h}px;")


def rec_tag(S, id, x, y, txt="REAL OUTPUT", vis=False):
    """'real recording' marker for a terminal / player (OpenRig): red dot + mono caps"""
    return div(S, id, "rtag", x, y, f"<i></i>{esc(txt)}", vis=vis)


def fband(S, p, steps, over=False):
    """Attention band: frames the item the narration is on right now.
    steps = [(t, (x, y, w, h)) | (t, None)]; each step crossfades from the previous one. Behind content;
    over=True = multiply highlighter on light evidence/paper. Rects enclose whole items (never cut a label)."""
    if over:
        st = "background:rgba(var(--accent-rgb),0.28); border:3px solid rgba(var(--accent-rgb),0.8); z-index:20; mix-blend-mode:multiply;"
    else:
        st = "background:rgba(var(--accent-rgb),0.13); border:3px solid rgba(var(--accent-rgb),0.5);"
    shown = None
    for i, (t, rc) in enumerate(steps):
        t = r2(max(0.05, t))
        if shown:
            S.J(f'tl.to("{shown}", {{ opacity: 0, duration: 0.35, ease: "power2.out" }}, {t});')
            shown = None
        if rc is None:
            continue
        x, y, w, h = rc
        bid = f"{p}{i}"
        html = (f'<div id="{bid}" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; box-sizing:border-box; '
                f'border-radius:{14 if over else 22}px; {st} opacity:0;"></div>')
        if over:
            S.add(html)
            sel_ = f"#{bid}"
        else:
            S.items.insert(0, html)
            S.add(f'<div id="{bid}f" style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; box-sizing:border-box; border-radius:22px; '
                  f'border:5px solid rgba(var(--accent-rgb),0.95); box-shadow:0 0 38px rgba(var(--accent-rgb),0.45), inset 0 0 34px rgba(var(--accent-rgb),0.22); '
                  f'z-index:15; opacity:0; pointer-events:none;"></div>')
            sel_ = f"#{bid}, #{bid}f"
        S.J(f'tl.to("{sel_}", {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, {t});')
        shown = sel_


def brand_plate(S, wordmark, wm_size, product=None, pr_size=None, lit=None, retire=None, y=126):
    """Hook brand plate from frame 0 (logo budget): the topic company's wordmark centred, ONE product
    lockup centred below it with a soft accent glow. Official files only (never retype a name).
    lit = scene second the glow peaks (the product's spoken name); retire = scene second the plate is
    gone: build.py fades the corner #brand-mark in at VIDEO["brand_mark_in"], so <= 2 logos ever.
    Keep the band y 110 .. 320 free of other content until the plate retires."""
    ww, wh = wm_size
    S.add(f'<img id="bp-wm" class="plate" src="{wordmark}" alt="wordmark" style="left:{round(960 - ww / 2)}px; top:{y}px; width:{ww}px; height:{wh}px;">')
    ids = "#bp-wm"
    if product:
        pw, ph = pr_size
        gy = y + wh + 22
        div(S, "bp-glow", "glow", round(960 - (pw + 110) / 2), gy - 26, "", style=f"width:{pw + 110}px; height:{ph + 52}px;")
        S.add(f'<img id="bp-pr" class="plate" src="{product}" alt="product" style="left:{round(960 - pw / 2)}px; top:{gy}px; width:{pw}px; height:{ph}px;">')
        t0 = lit if lit is not None else 0.02
        S.J(f'tl.to("#bp-glow", {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {r2(t0)});')
        S.J(f'tl.to("#bp-glow", {{ opacity: 0.35, duration: 0.6, ease: "power2.inOut" }}, {r2(t0 + 1.4)});')
        ids += ", #bp-pr, #bp-glow"
    if retire is not None:
        S.J(f'off("{ids}", {r2(retire - 0.3)}, 0.3);')
    return retire


# ================================================================ headline (OpenRig "Term = meaning")
def _hl_html(text, kw=()):
    kws = {w.lower().strip(".,:;!?") for w in kw}
    out = []
    for w in text.split():
        if w == "=":
            out.append('<span class="eq">=</span>')
        elif w.lower().strip(".,:;!?") in kws:
            out.append(f'<span class="kw">{esc(w)}</span>')
        else:
            out.append(esc(w))
    return " ".join(out)


def headline(S, id, text, y=150, fs=56, kw=(), x=960, vis=False):
    """top-centre orientation headline (<= 6 words). "A = B" colours the '=' accent; kw words accent."""
    w = round(tw_inter(text, fs) * 1.08 + 60)
    S.add(f'<div id="{id}" class="hl" style="left:{round(x - w / 2)}px; top:{y}px; width:{w}px; font-size:{fs}px;{" opacity:1;" if vis else ""}">'
          f'{_hl_html(text, kw)}</div>')
    return id


def heads(S, p, items, y=150, fs=56, t_out=None, x=960):
    """a headline that swaps on its words: items = [(t, text, kw)] -> ids. The last one stays until t_out."""
    ids = []
    for i, it in enumerate(items):
        t, text = it[0], it[1]
        kw = it[2] if len(it) > 2 else ()
        hid = f"{p}{i}"
        headline(S, hid, text, y=y, fs=fs, kw=kw, x=x)
        S.J(f'tl.fromTo("#{hid}", {{ opacity: 0, y: 22 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }}, {r2(t)});')
        if i:
            S.J(f'tl.to("#{ids[-1]}", {{ opacity: 0, y: -22, duration: 0.3, ease: "power2.in" }}, {r2(t - 0.12)});')
        ids.append(hid)
    if t_out is not None and ids:
        S.J(f'tl.to("#{ids[-1]}", {{ opacity: 0, y: -22, duration: 0.3, ease: "power2.in" }}, {r2(t_out)});')
    return ids


# ================================================================ concept ladder (model -> harness -> rig)
def ladder(S, id, items, x, y, center=True, gap=74):
    """chips joined by arrows; reveal with ladder_in, step with ladder_go. Returns total width."""
    ws = [round(tw_mono(s, 26, 1) + 48) for s in items]
    total = sum(ws) + gap * (len(items) - 1)
    cx = x - total / 2 if center else x
    for i, (s, w) in enumerate(zip(items, ws)):
        S.add(f'<div id="{id}-{i}" class="lad" style="left:{r1(cx)}px; top:{y}px; width:{w}px;">{esc(s)}</div>')
        if i < len(items) - 1:
            ax = cx + w + 12
            S.add(f'<svg id="{id}-a{i}" class="lada" style="left:{r1(ax)}px; top:{y + 14}px;" width="{gap - 24}" height="28" viewBox="0 0 {gap - 24} 28">'
                  f'<path d="M2 14 H{gap - 28} M{gap - 38} 5 L{gap - 28} 14 L{gap - 38} 23"/></svg>')
        cx += w + gap
    S.J(f'tl.set("#{id}-0", {{ opacity: 0 }}, 0);')
    return total


def ladder_in(S, id, n, t, step=0.18, o=0.4):
    for i in range(n):
        S.J(f'tl.fromTo("#{id}-{i}", {{ opacity: 0, y: 14 }}, {{ opacity: {o}, y: 0, duration: 0.35, ease: "power3.out", immediateRender: false }}, {r2(t + i * step)});')
        if i < n - 1:
            S.J(f'tl.fromTo("#{id}-a{i}", {{ opacity: 0 }}, {{ opacity: {o}, duration: 0.3, immediateRender: false }}, {r2(t + i * step + 0.1)});')


def ladder_go(S, id, n, k, t):
    """chip k becomes the current one (accent fill); earlier chips = done (accent outline); later = ghost"""
    acc, onacc, pan, txt = tok("accent-1"), tok("on-acc"), tok("panel-2"), tok("text")
    for i in range(n):
        if i == k:
            S.J(f'tl.to("#{id}-{i}", {{ opacity: 1, backgroundColor: "{acc}", color: "{onacc}", borderColor: "{acc}", duration: 0.35, ease: "power2.out" }}, {r2(t)});')
        elif i < k:
            S.J(f'tl.to("#{id}-{i}", {{ opacity: 1, backgroundColor: "{pan}", color: "{txt}", borderColor: "{acc}", duration: 0.35 }}, {r2(t)});')
        if i < k:
            S.J(f'tl.to("#{id}-a{i}", {{ opacity: 1, duration: 0.3 }}, {r2(t)});')


# ================================================================ glossary rail
def gloss(S, id, entries, x, y, gap=108):
    """entries = [(term, meaning)] stacked from (x, y); reveal one by one with gloss_in"""
    for i, (term, meaning) in enumerate(entries):
        S.add(f'<div id="{id}-{i}" class="gl" style="left:{x}px; top:{y + i * gap}px;"><div id="{id}-{i}b" class="gb"></div>'
              f'<div class="gt">{esc(term)}</div><div class="gd">{esc(meaning)}</div></div>')


def gloss_ghost(S, id, n, t, o=0.3, step=0.15):
    """all n terms appear at once as a ghost (no empty stage while the narration introduces them)"""
    for k in range(n):
        S.J(f'tl.fromTo("#{id}-{k}", {{ opacity: 0, x: -30 }}, {{ opacity: {o}, x: 0, duration: 0.4, ease: "power3.out", immediateRender: false }}, {r2(t + k * step)});')


def gloss_in(S, id, k, t, dim_prev=True, frm=0.0):
    """term k to full (from a ghost: frm = the ghost opacity); the previous term dims"""
    S.J(f'tl.fromTo("#{id}-{k}", {{ opacity: {frm}, x: {0 if frm else -30} }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out", immediateRender: false }}, {r2(t)});')
    if dim_prev and k:
        S.J(f'tl.to("#{id}-{k - 1}", {{ opacity: 0.5, duration: 0.35 }}, {r2(t)});')
        S.J(f'tl.to("#{id}-{k - 1}b", {{ opacity: 0, duration: 0.35 }}, {r2(t)});')


# ================================================================ anatomy of a string
def anatomy(S, id, parts, x, y, fs=76, center=True):
    """parts = [(text, label or None, cls)] laid out as one monospace string (address, cache key,
    CLI command, model id). anat_in shows it neutral; anat_part colours part i, draws its bracket and
    pops its label (labels alternate to a lower row when they would touch). cls: acc ok flow s2 warn bad."""
    cw = fs * 0.6
    total = sum(len(p[0]) for p in parts) * cw
    x0 = x - total / 2 if center else x
    hgt = round(fs * 1.34, 1)
    meta, cx = [], x0
    last_r = [-1e9, -1e9]
    for i, (txt, label, cls) in enumerate(parts):
        w = len(txt) * cw
        S.add(f'<div id="{id}-p{i}" class="anp" style="left:{r1(cx)}px; top:{y}px; width:{r1(w)}px; height:{hgt}px; font-size:{fs}px; line-height:{hgt}px;">{esc(txt)}</div>')
        if label:
            colr = F.col(cls or "acc")
            by = y + hgt + 10
            S.add(f'<svg id="{id}-b{i}" class="anb" style="left:{r1(cx + 6)}px; top:{r1(by)}px;" width="{r1(w - 12)}" height="22" viewBox="0 0 {r1(w - 12)} 22">'
                  f'<path id="{id}-bp{i}" d="M2 2 V12 H{r1(w / 2 - 6)} V20 M{r1(w / 2 - 6)} 12 H{r1(w - 14)} V2" pathLength="1" '
                  f'style="stroke:{colr}; stroke-dasharray:1; stroke-dashoffset:1; opacity:0;"/></svg>')
            lw = tw_mono(label, 24, 2) + 26
            lx = cx + w / 2 - lw / 2
            row = 0 if lx > last_r[0] + 24 else 1
            last_r[row] = lx + lw
            ly = by + 34 + row * 50
            S.add(f'<div id="{id}-l{i}" class="anl" style="left:{r1(lx)}px; top:{r1(ly)}px; background:{colr}; color:{"#101318" if cls in ("ok", "flow", "warn") else "#FFFFFF" if cls in ("bad", "s2") else tok("on-acc")};">{esc(label)}</div>')
        meta.append((cx, w, cls))
        cx += w
    return meta


def anat_in(S, id, n, t, step=0.05):
    for i in range(n):
        S.J(f'tl.fromTo("#{id}-p{i}", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }}, {r2(t + i * step)});')


def anat_part(S, id, i, t, cls="acc", label=True):
    c = F.col(cls)
    # text a shade deeper than its tint on the light skin, so the part keeps >= 3:1 contrast
    tc = kit._mix(c, "#000000", 0.32) if kit.SKIN == "paper" else c
    S.J(f'tl.to("#{id}-p{i}", {{ color: "{tc}", backgroundColor: "{rgba(c, 0.16)}", duration: 0.35, ease: "power2.out" }}, {r2(t)});')
    if label:
        S.J(f'tl.set("#{id}-bp{i}", {{ opacity: 1 }}, {r2(t + 0.1)});')
        S.J(f'wDraw("#{id}-bp{i}", {r2(t + 0.1)}, 0.4);')
        S.J(f'tl.fromTo("#{id}-l{i}", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)", immediateRender: false }}, {r2(t + 0.35)});')


# ================================================================ chaos -> order
def win_card(color="acc", face="bot", w=220, h=150):
    """small window card: coloured title bar + a face (bot / user / doc icon) + grey text lines"""
    c = F.col(color)
    fs = min(h - 64, 78)
    icon = icon_svg(face, fs).replace('class="ic"', f'class="ic" style="color:{c}; --ifill:{rgba(c, 0.18)};"') if face else ""
    lines = "".join(f'<div class="wl" style="left:{r1(fs + 32)}px; top:{50 + i * 22}px; width:{r1((w - fs - 52) * (1 - 0.18 * (i % 3)))}px;"></div>'
                    for i in range(max(1, int((h - 60) // 22))))
    return (f'<div class="wc"><div class="wb" style="background:{c};"><i style="left:12px;"></i><i style="left:28px;"></i><i style="left:44px;"></i></div>'
            f'<div class="wf">{icon}</div>{lines}</div>')


def sprawl(S, id, n, seed, area, w=220, h=150, colors=("acc", "s2"), faces=("bot",), min_d=None):
    """n window cards scattered (seeded, deterministic) over area=(x, y, w, h) with tilts.
    Returns [(cx, cy, rot)]. Reveal with sprawl_pop (in waves: 1, 2, 5, 10 ...)."""
    rng = random.Random(seed)
    ax, ay, aw, ah = area
    min_d = min_d or (w * 0.62)
    pts = []
    for i in range(n):
        best, bd = None, -1
        for _ in range(60):
            cx, cy = ax + w / 2 + rng.random() * (aw - w), ay + h / 2 + rng.random() * (ah - h)
            dmin = min([math.hypot(cx - p[0], cy - p[1]) for p in pts] or [1e9])
            if dmin >= min_d:
                best = (cx, cy)
                break
            if dmin > bd:
                best, bd = (cx, cy), dmin
        rot = round(rng.uniform(-9, 9), 1)
        pts.append((r1(best[0]), r1(best[1]), rot))
    S.add(f'<div id="{id}" class="spw" data-fit-allow="stroke">' + "".join(
        f'<div id="{id}-{i}" class="spi" style="left:{r1(cx - w / 2)}px; top:{r1(cy - h / 2)}px; width:{w}px; height:{h}px;">'
        f'{win_card(colors[i % len(colors)], faces[i % len(faces)], w, h)}</div>' for i, (cx, cy, rot) in enumerate(pts)) + "</div>")
    for i, (_, _, rot) in enumerate(pts):
        S.J(f'tl.set("#{id}-{i}", {{ rotation: {rot} }}, 0);')
    return pts


def sprawl_pop(S, id, pts, t, idxs, step=0.1):
    for j, i in enumerate(idxs):
        rot = pts[i][2]
        S.J(f'tl.fromTo("#{id}-{i}", {{ opacity: 0, scale: 0.3, rotation: {rot - 14} }}, {{ opacity: 1, scale: 1, rotation: {rot}, duration: 0.45, '
            f'ease: "back.out(1.8)", immediateRender: false }}, {r2(t + j * step)});')


def sprawl_grey(S, id, t, o=0.3):
    S.J(f'tl.fromTo("#{id}", {{ filter: "grayscale(0)", opacity: 1 }}, {{ filter: "grayscale(1)", opacity: {o}, duration: 0.6, ease: "power2.out", immediateRender: false }}, {r2(t)});')


def sprawl_order(S, id, pts, t, slots, scale=0.6, stagger=0.035, d=0.8):
    """un-grey and file every card into its slot (slot = target centre, canvas px)"""
    S.J(f'tl.to("#{id}", {{ filter: "grayscale(0)", opacity: 1, duration: 0.5, ease: "power2.out" }}, {r2(t)});')
    for i, ((cx, cy, _), (sx, sy)) in enumerate(zip(pts, slots)):
        S.J(f'tl.to("#{id}-{i}", {{ x: {r1(sx - cx)}, y: {r1(sy - cy)}, rotation: 0, scale: {scale}, duration: {d}, ease: "power3.inOut" }}, {r2(t + i * stagger)});')


def sprawl_out(S, id, t, d=0.4):
    S.J(f'tl.to("#{id}", {{ opacity: 0, duration: {d}, ease: "power2.in" }}, {r2(t)});')


# ================================================================ speech bubble
def bubble(S, id, text, x, y, tail="bl", fs=30, t=None, t_out=None):
    """speech bubble (top-left at x, y), <= 5 words; tail bl | br | tl | tr. Pops at t."""
    w = round(tw_inter(text, fs) + 48)
    h = round(fs * 1.25 + 30)
    tx = 26 if tail[1] == "l" else w - 62
    if tail[0] == "b":
        tsvg = (f'<svg width="36" height="26" viewBox="0 0 36 26" style="left:{tx}px; top:{h - 4}px;"><path d="M1 0 L18 24 L35 0" '
                f'style="fill:var(--panel); stroke:var(--wire); stroke-width:3; stroke-linejoin:round;"/></svg>')
        org = f"{tx + 18}px {h + 20}px"
    else:
        tsvg = (f'<svg width="36" height="26" viewBox="0 0 36 26" style="left:{tx}px; top:-22px;"><path d="M1 26 L18 2 L35 26" '
                f'style="fill:var(--panel); stroke:var(--wire); stroke-width:3; stroke-linejoin:round;"/></svg>')
        org = f"{tx + 18}px -20px"
    S.add(f'<div id="{id}" class="bub" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px; font-size:{fs}px; line-height:{round(fs * 1.25)}px;">'
          f'{esc(text)}{tsvg}</div>')
    if t is not None:
        S.J(f'tl.fromTo("#{id}", {{ opacity: 0, scale: 0.4, transformOrigin: "{org}" }}, {{ opacity: 1, scale: 1, transformOrigin: "{org}", duration: 0.4, '
            f'ease: "back.out(2.2)", immediateRender: false }}, {r2(t)});')
    if t_out is not None:
        S.J(f'tl.to("#{id}", {{ opacity: 0, duration: 0.25 }}, {r2(t_out)});')
    return id


# ================================================================ the stakes slam
def slam_plate(S, id, lines, t, t_out, tint="bad"):
    """full-frame tint with 1-2 huge lines (ByteByteGo's 'NO SEARCHES / NO PURCHASES'). Once per video:
    the stakes moment. Keep it 1.2-2.5 s; the HUD stays on top."""
    c = F.col(tint)
    S.add(f'<div id="{id}" class="slam" data-fit-allow="text" style="background:{rgba(c, 0.93)};">' +
          "".join(f'<div id="{id}-{i}" class="slm">{esc(s)}</div>' for i, s in enumerate(lines)) + "</div>")
    S.J(f'tl.fromTo("#{id}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.14, ease: "power2.out", immediateRender: false }}, {r2(t)});')
    for i in range(len(lines)):
        S.J(f'tl.fromTo("#{id}-{i}", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.26, ease: "power4.in", immediateRender: false }}, {r2(t + 0.08 + i * 0.16)});')
    S.J(f'tl.to("#{id}", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {r2(t_out)});')


# ================================================================ threshold meter
def meter(S, id, x, y, w, zones, ticks=()):
    """zones = [(label, fraction, cls)] left->right (fractions sum to 1); ticks = [(fraction, text)].
    Marker starts hidden; meter_in grows the zones, meter_to slides the marker."""
    segs, cx = [], 0.0
    for i, (lab, fr, cls) in enumerate(zones):
        sw = w * fr
        segs.append(f'<div id="{id}-s{i}" class="ms" style="left:{r1(cx)}px; width:{r1(sw - 4)}px; background:{F.col(cls)};">{esc(lab)}</div>')
        cx += sw
    tk_ = "".join(f'<div class="mt" style="left:{r1(w * f - tw_mono(s, 22, 0) / 2)}px;">{esc(s)}</div>' for f, s in ticks)
    S.add(f'<div id="{id}" class="mtr" style="left:{x}px; top:{y}px; width:{w}px; height:100px;">{"".join(segs)}{tk_}'
          f'<div id="{id}-m" class="mk2" style="opacity:0;"><div id="{id}-mc" class="mkc">0</div><div class="mkt"></div></div></div>')
    return w


def meter_in(S, id, n, t, step=0.2):
    S.J(f'tl.to("#{id}", {{ opacity: 1, duration: 0.2 }}, {r2(t)});')
    for i in range(n):
        S.J(f'tl.fromTo("#{id}-s{i}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power3.out", immediateRender: false }}, {r2(t + i * step)});')


def meter_to(S, id, w, t, frac, text=None, d=0.9, show=True):
    if show:
        S.J(f'tl.to("#{id}-m", {{ opacity: 1, duration: 0.25 }}, {r2(t)});')
    S.J(f'tl.to("#{id}-m", {{ x: {r1(w * frac)}, duration: {d}, ease: "power3.inOut" }}, {r2(t)});')
    if text is not None:
        S.J(f'tl.call(function () {{ const e = document.querySelector("#{id}-mc"); if (e) e.textContent = {text!r}; }}, null, {r2(t + d * 0.5)});')


# ================================================================ cells (slots)
def cells(S, id, x, y, n, cols, size=56, gap=12):
    """grid of n slots, cols per row; returns [(cx, cy)] centres"""
    out = []
    for i in range(n):
        cx = x + (i % cols) * (size + gap)
        cy = y + (i // cols) * (size + gap)
        S.add(f'<div id="{id}-{i}" class="cel" style="left:{cx}px; top:{cy}px; width:{size}px; height:{size}px;"></div>')
        out.append((cx + size / 2, cy + size / 2))
    return out


def cells_in(S, id, n, t, step=0.02):
    for i in range(n):
        S.J(f'tl.fromTo("#{id}-{i}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, {r2(t + i * step)});')


def cells_fill(S, id, t, idxs, cls="acc", step=0.08, a=0.85):
    c = F.col(cls)
    for j, i in enumerate(idxs):
        tt = r2(t + j * step)
        S.J(f'tl.to("#{id}-{i}", {{ backgroundColor: "{rgba(c, a)}", borderColor: "{c}", duration: 0.25, ease: "power2.out" }}, {tt});')
        S.J(f'tl.fromTo("#{id}-{i}", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }}, {tt});')


# ================================================================ table
def table(S, id, x, y, cols, rows, widths, rh=60, fs=26):
    """cols = header texts, rows = [[cell, ...]], widths = px per column. Row highlight bands sit behind."""
    W = sum(widths)
    H = rh * (len(rows) + 1)

    def cells_html(vals, top, head=False):
        cx, out = 0, []
        for v, cw in zip(vals, widths):
            out.append(f'<div class="tc" style="left:{cx + 20}px; top:{r1(top + (rh - fs * 1.3) / 2)}px; font-size:{22 if head else fs}px; line-height:{r1(fs * 1.3)}px;">{esc(str(v))}</div>')
            cx += cw
        return "".join(out)
    body = f'<div class="th" style="height:{rh}px;">{cells_html(cols, 0, True)}</div>'
    for i, r in enumerate(rows):
        top = rh * (i + 1)
        body += (f'<div id="{id}-h{i}" class="thl" style="top:{top}px; height:{rh}px; background:rgba(var(--accent-rgb),0.22);"></div>'
                 f'<div id="{id}-r{i}" class="tr" style="top:{top}px; height:{rh}px;">{cells_html(r, 0)}</div>')
    S.add(f'<div id="{id}" class="tbl" style="left:{x}px; top:{y}px; width:{W}px; height:{H}px;">{body}</div>')
    return W, H


def table_in(S, id, n, t, step=0.08):
    S.J(f'inn("#{id}", {r2(t)}, {{ y: 24 }});')
    for i in range(n):
        S.J(f'tl.fromTo("#{id}-r{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, {r2(t + 0.2 + i * step)});')


def row_hl(S, id, i, t, t_out=None, cls="acc"):
    if cls != "acc":
        S.J(f'tl.set("#{id}-h{i}", {{ backgroundColor: "{rgba(F.col(cls), 0.26)}" }}, {r2(t)});')
    S.J(f'tl.to("#{id}-h{i}", {{ opacity: 1, duration: 0.2 }}, {r2(t)});')
    if t_out is not None:
        S.J(f'tl.to("#{id}-h{i}", {{ opacity: 0, duration: 0.2 }}, {r2(t_out)});')


def table_scan(S, id, t0, rows, step=0.28, hit=None):
    """a highlight walks the rows one by one (full scan); stops and stays green on `hit`"""
    t = t0
    for i in rows:
        if i == hit:
            row_hl(S, id, i, t, None, "ok")
            return t
        row_hl(S, id, i, t, t + step)
        t += step
    return t


# ================================================================ roadmap
def road(S, id, stops, x, y, w, amp=64):
    """wavy road through len(stops) numbered stops (labels alternate above / below). Returns the
    stop centres. road_in draws it; road_go(k_from, k_to) moves the traveller and fills the stop."""
    n = len(stops)
    dx = w / (n - 1)
    P = [(x + i * dx, y + (-amp if i % 2 == 0 else amp)) for i in range(n)]
    d = f"M{r1(P[0][0])},{r1(P[0][1])}"
    legs = []
    for i in range(n - 1):
        a, b = P[i], P[i + 1]
        c1, c2 = (a[0] + dx / 2, a[1]), (b[0] - dx / 2, b[1])
        d += f" C{r1(c1[0])},{r1(c1[1])} {r1(c2[0])},{r1(c2[1])} {r1(b[0])},{r1(b[1])}"
        leg = []
        for s in range(0, 13):
            u = s / 12
            px = (1 - u) ** 3 * a[0] + 3 * (1 - u) ** 2 * u * c1[0] + 3 * (1 - u) * u * u * c2[0] + u ** 3 * b[0]
            py = (1 - u) ** 3 * a[1] + 3 * (1 - u) ** 2 * u * c1[1] + 3 * (1 - u) * u * u * c2[1] + u ** 3 * b[1]
            leg.append((r1(px), r1(py)))
        legs.append(leg)
    S.add(f'<svg id="{id}" class="rd" width="1920" height="1080" viewBox="0 0 1920 1080"><path id="{id}-p" class="rp" data-fit-allow="stroke" d="{d}" pathLength="1" '
          f'style="stroke-dasharray:1; stroke-dashoffset:1; opacity:0;"/></svg>')
    for i, ((px, py), lab) in enumerate(zip(P, stops)):
        S.add(f'<div id="{id}-s{i}" class="rst" style="left:{r1(px)}px; top:{r1(py)}px;">{i + 1}</div>')
        lw = tw_inter(lab, 28)
        ly = py - 32 - 52 if i % 2 == 0 else py + 32 + 16
        S.add(f'<div id="{id}-l{i}" class="rlb" style="left:{r1(px - lw / 2)}px; top:{r1(ly)}px;">{esc(lab)}</div>')
    S.add(f'<div id="{id}-tv" class="rtv"></div>')
    S.J(f'tl.set("#{id}-tv", {{ x: {r1(P[0][0])}, y: {r1(P[0][1])} }}, 0);')
    S._road = getattr(S, "_road", {})
    S._road[id] = legs
    return P


def road_in(S, id, n, t, step=0.25):
    S.J(f'tl.set("#{id}-p", {{ opacity: 1 }}, {r2(t)});')
    S.J(f'wDraw("#{id}-p", {r2(t)}, {round(0.5 + 0.2 * n, 2)});')
    for i in range(n):
        S.J(f'nIn("#{id}-s{i}", {r2(t + 0.2 + i * step)});')
        S.J(f'tl.fromTo("#{id}-l{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, immediateRender: false }}, {r2(t + 0.35 + i * step)});')


def road_go(S, id, k_from, k_to, t, d=1.0):
    """traveller from stop k_from to k_to along the road; k_to fills accent, passed stops fill ok"""
    acc, onacc, ok = tok("accent-1"), tok("on-acc"), tok("ok")
    legs = S._road[id]
    if k_from == k_to:
        S.J(f'tl.to("#{id}-tv", {{ opacity: 1, duration: 0.3 }}, {r2(t)});')
    else:
        pts = []
        rng = range(k_from, k_to) if k_to > k_from else range(k_from - 1, k_to - 1, -1)
        for i in rng:
            leg = legs[i] if k_to > k_from else list(reversed(legs[i]))
            pts.extend(leg if not pts else leg[1:])
        flat = ",".join(f"{p[0]},{p[1]}" for p in pts)
        S.J(f'tl.to("#{id}-tv", {{ opacity: 1, duration: 0.2 }}, {r2(t)});')
        S.J(f'pathmv("#{id}-tv", {r2(t)}, {d}, [{flat}]);')
        for i in range(min(k_from, k_to), max(k_from, k_to)):
            if i < k_to:
                S.J(f'tl.to("#{id}-s{i}", {{ backgroundColor: "{ok}", borderColor: "{ok}", color: "#101318", duration: 0.3 }}, {r2(t + 0.1)});')
    S.J(f'tl.to("#{id}-s{k_to}", {{ backgroundColor: "{acc}", borderColor: "{acc}", color: "{onacc}", duration: 0.3 }}, {r2(t + d)});')


# ================================================================ recap card
def recap(S, id, x, y, w, items, title="RECAP"):
    """card with a mono title and check rows (<= 6 words each); rows reveal with recap_row"""
    h = 110 + 74 * len(items)
    S.add(f'<div id="{id}" class="rcp" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px;">'
          f'<div class="kick" style="left:40px; top:34px;">{esc(title)}</div>' +
          "".join(f'<div id="{id}-{i}" class="rcr" style="top:{100 + 74 * i}px;"><div style="position:absolute; left:0; top:2px;">{icon_svg("check", 46).replace(chr(34) + "ic" + chr(34), chr(34) + "ic" + chr(34) + " style=" + chr(34) + "color:#101318; --ifill:var(--ok);" + chr(34))}</div>'
                  f'<div class="rct">{esc(s)}</div></div>' for i, s in enumerate(items)) + "</div>")
    return h


def recap_row(S, id, i, t):
    S.J(f'tl.fromTo("#{id}-{i}", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out", immediateRender: false }}, {r2(t)});')
