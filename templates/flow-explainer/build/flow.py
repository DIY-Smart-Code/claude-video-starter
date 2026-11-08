"""flow.py — LIVING SYSTEM DIAGRAMS for flow-explainer (the ByteByteGo board, built natively).

A Flow is one system diagram inside a scene: icon nodes, translucent zones, routed wires that
draw on their word, tokens (requests / messages / packets) that travel the wires, state changes
(fail, promote, dim) and a camera that frames any part of it. The same builder function can be
mounted again at a small scale as the chapter locator (mini()), which is how the video's ONE
persistent object returns in every chapter.

    G = Flow(S, "sys")                                   # full-canvas diagram, hidden parts
    G.node("db", 1500, 520, "db", "Database")           # (x, y) = tile centre, canvas px
    G.zone("data", 1180, 380, 560, 300, "Data tier", "s2")
    G.wire("w1", "cache", "db", label="miss only", dash=True)
    G.show(t, "db"); G.show(t + .4, "w1")                # pop / draw on the spoken word
    G.flow("w1", t0, t1, every=0.8)                      # tokens travel the wire t0..t1
    G.fail("db", t); G.badge("rep", "PRIMARY", t, "ok"); G.focus(t, ["cache", "db"])
    G.frame(t, ["cache", "db"])                          # camera: fit these nodes; frame(t) resets
    mini(S, "loc", system, (96, 120, 420, 210), lit=["cache"])   # the locator, same builder

Node looks: "tile" (rounded tile + icon, default), "bare" (icon only, ByteByteGo line art),
"box" (rounded rect with text inside: a service / a concept), any of them with logo=<file>.
Every colour comes from tokens/flow-<skin>.css; one meaning per colour (DESIGN.md).

JS verbs added to every scene: nIn nOut wDraw tk pathmv march ring shake
"""
import math
import kit
from kit import esc, WARN, tok


def r1(x):
    return round(x, 1)


def r2(x):
    return round(x, 2)


# ------------------------------------------------------------------ icon set (100-unit box)
# classes: s = stroke only, f = filled part (var(--ifill)) + stroke, k = solid currentColor
ICONS = {
    "server": '<rect class="f" x="16" y="10" width="68" height="36" rx="8"/><rect class="f" x="16" y="54" width="68" height="36" rx="8"/>'
              '<circle class="k" cx="30" cy="28" r="5"/><circle class="k" cx="30" cy="72" r="5"/><path class="s" d="M46 28h24M46 72h24"/>',
    "db": '<path class="f" d="M18 24v52c0 8 14 14 32 14s32-6 32-14V24"/><ellipse class="f" cx="50" cy="24" rx="32" ry="12"/>'
          '<path class="s" d="M18 43c0 8 14 14 32 14s32-6 32-14M18 61c0 8 14 14 32 14s32-6 32-14"/>',
    "cache": '<rect class="f" x="12" y="12" width="76" height="76" rx="16"/><path class="k" d="M57 18 L30 55 H47 L41 82 L70 43 H52 Z"/>',
    "queue": '<rect class="f" x="6" y="28" width="88" height="44" rx="10"/>'
             '<path class="s" d="M15 39h20v22H15zM15 39l10 9 10-9M40 39h20v22H40zM40 39l10 9 10-9M65 39h20v22H65zM65 39l10 9 10-9"/>',
    "cloud": '<path class="f" d="M28 76h46a18 18 0 0 0 3-36 24 24 0 0 0-46-5 20 20 0 0 0-3 41z"/>',
    "cpu": '<rect class="f" x="24" y="24" width="52" height="52" rx="7"/><rect class="s" x="38" y="38" width="24" height="24" rx="3"/>'
           '<path class="s" d="M36 10v12M50 10v12M64 10v12M36 78v12M50 78v12M64 78v12M10 36h12M10 50h12M10 64h12M78 36h12M78 50h12M78 64h12"/>',
    "user": '<circle class="f" cx="50" cy="31" r="17"/><path class="f" d="M17 90c0-21 14-33 33-33s33 12 33 33z"/>',
    "users": '<circle class="f" cx="27" cy="38" r="12"/><path class="f" d="M5 86c0-17 10-27 22-27s22 10 22 27z"/>'
             '<circle class="f" cx="73" cy="38" r="12"/><path class="f" d="M51 86c0-17 10-27 22-27s22 10 22 27z"/>'
             '<circle class="f" cx="50" cy="30" r="15"/><path class="f" d="M24 92c0-21 11-33 26-33s26 12 26 33z"/>',
    "browser": '<rect class="f" x="8" y="14" width="84" height="72" rx="10"/><path class="s" d="M8 32h84M22 52h42M22 66h28"/>'
               '<circle class="k" cx="20" cy="23" r="3.5"/><circle class="k" cx="31" cy="23" r="3.5"/><circle class="k" cx="42" cy="23" r="3.5"/>',
    "phone": '<rect class="f" x="28" y="8" width="44" height="84" rx="10"/><path class="s" d="M43 80h14"/>',
    "lb": '<circle class="f" cx="50" cy="50" r="40"/><path class="s" d="M24 50h18M42 50 60 33h14M42 50 60 67h14M68 27l7 6-7 6M68 61l7 6-7 6"/>',
    "api": '<rect class="f" x="10" y="14" width="80" height="72" rx="12"/>'
           '<path class="s" d="M41 32c-8 0-8 4-8 10s-2 8-8 8c6 0 8 2 8 8s0 10 8 10M59 32c8 0 8 4 8 10s2 8 8 8c-6 0-8 2-8 8s0 10-8 10"/>',
    "doc": '<path class="f" d="M22 6h40l18 18v70H22z"/><path class="s" d="M62 6v18h18M34 44h34M34 60h34M34 76h22"/>',
    "folder": '<path class="f" d="M6 22h30l8 9h50v55H6z"/><path class="s" d="M6 40h88"/>',
    "lock": '<path class="s" d="M31 44V31c0-21 38-21 38 0v13"/><rect class="f" x="18" y="44" width="64" height="46" rx="10"/><path class="s" d="M50 61v12"/>',
    "key": '<circle class="f" cx="31" cy="50" r="17"/><path class="s" d="M48 50h42M76 50v14M88 50v10"/>',
    "shield": '<path class="f" d="M50 6 86 20v28c0 30-16 42-36 46C30 90 14 78 14 48V20z"/><path class="s" d="m34 50 12 12 22-24"/>',
    "gear": '<path class="f" d="M44 6h12l2 12 10 4 10-8 8 8-8 10 4 10 12 2v12l-12 2-4 10 8 10-8 8-10-8-10 4-2 12H44l-2-12-10-4-10 8-8-8 8-10-4-10-12-2V44l12-2 4-10-8-10 8-8 10 8 10-4z"/>'
            '<circle class="f" cx="50" cy="50" r="13"/>',
    "globe": '<circle class="f" cx="50" cy="50" r="40"/><ellipse class="s" cx="50" cy="50" rx="17" ry="40"/><path class="s" d="M10 50h80M17 30q33 10 66 0M17 70q33-10 66 0"/>',
    "clock": '<circle class="f" cx="50" cy="50" r="40"/><path class="s" d="M50 24v26l18 12"/>',
    "mail": '<rect class="f" x="8" y="20" width="84" height="60" rx="9"/><path class="s" d="m8 27 42 30 42-30"/>',
    "bell": '<path class="f" d="M50 10c-18 0-28 13-28 30v20l-8 12h72l-8-12V40c0-17-10-30-28-30z"/><path class="s" d="M40 84a10 10 0 0 0 20 0"/>',
    "chart": '<path class="s" d="M10 88h80"/><rect class="f" x="17" y="54" width="15" height="34" rx="2"/><rect class="f" x="42" y="36" width="15" height="52" rx="2"/>'
             '<rect class="f" x="67" y="16" width="15" height="72" rx="2"/>',
    "search": '<circle class="f" cx="42" cy="42" r="27"/><path class="s" d="M62 62l26 26" style="stroke-width:10"/>',
    "bulb": '<path class="f" d="M50 8c17 0 30 12 30 29 0 12-8 19-14 26v11H34V63c-6-7-14-14-14-26C20 20 33 8 50 8z"/><path class="s" d="M38 86h24M42 95h16"/>',
    "eye": '<path class="f" d="M6 50q44-44 88 0-44 44-88 0z"/><circle class="k" cx="50" cy="50" r="13"/>',
    "check": '<circle class="f" cx="50" cy="50" r="40"/><path class="s" d="m31 51 13 13 25-27" style="stroke-width:9"/>',
    "cross": '<circle class="f" cx="50" cy="50" r="40"/><path class="s" d="m34 34 32 32M66 34 34 66" style="stroke-width:9"/>',
    "warn": '<path class="f" d="M50 8 94 88H6z"/><path class="s" d="M50 38v22"/><circle class="k" cx="50" cy="73" r="5"/>',
    "layers": '<path class="f" d="m50 56 42 16-42 16L8 72z"/><path class="f" d="m50 35 42 16-42 16L8 51z"/><path class="f" d="m50 14 42 16-42 16L8 30z"/>',
    "box": '<path class="f" d="M10 30 50 12l40 18v44L50 92 10 74z"/><path class="s" d="m10 30 40 18 40-18M50 48v44M30 21l40 18"/>',
    "code": '<rect class="f" x="8" y="14" width="84" height="72" rx="10"/><path class="s" d="M38 36 24 50l14 14M62 36l14 14-14 14M55 30 45 70"/>',
    "branch": '<circle class="f" cx="28" cy="20" r="10"/><circle class="f" cx="28" cy="80" r="10"/><circle class="f" cx="72" cy="36" r="10"/>'
              '<path class="s" d="M28 30v40M72 46c0 18-44 10-44 24"/>',
    "spark": '<path class="f" d="M50 8c4 28 12 38 42 42-30 4-38 14-42 42-4-28-12-38-42-42 30-4 38-14 42-42z"/>',
    "bot": '<rect class="f" x="16" y="28" width="68" height="56" rx="15"/><path class="s" d="M50 28V15"/><circle class="k" cx="50" cy="12" r="6"/>'
           '<circle class="k" cx="37" cy="52" r="6.5"/><circle class="k" cx="63" cy="52" r="6.5"/><path class="s" d="M38 68q12 9 24 0"/>',
    "terminal": '<rect class="f" x="8" y="16" width="84" height="68" rx="10"/><path class="s" d="m24 40 12 10-12 10M44 62h22"/>',
    "map": '<path class="f" d="M8 22 36 12l28 10 28-10v66L64 88 36 78 8 88z"/><path class="s" d="M36 12v66M64 22v66"/>',
    "camera": '<path class="f" d="M8 30h22l8-12h24l8 12h22v52H8z"/><circle class="f" cx="50" cy="55" r="16"/>',
    "ticket": '<path class="f" d="M8 28h84v14a8 8 0 0 0 0 16v14H8V58a8 8 0 0 0 0-16z"/><path class="s" d="M30 28v44" style="stroke-dasharray:5 7"/><path class="s" d="M42 44h34M42 56h22"/>',
}


def icon_svg(name, px):
    if name not in ICONS:
        raise SystemExit(f"flow: unknown icon {name!r} (have: {', '.join(sorted(ICONS))})")
    return f'<svg class="ic" viewBox="0 0 100 100" width="{r1(px)}" height="{r1(px)}">{ICONS[name]}</svg>'


# ------------------------------------------------------------------ CSS + JS verbs (added once to the kit)
FLOW_CSS = """
      .fl { position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:0 0; }
      .flsvg { position:absolute; left:0; top:0; overflow:visible; pointer-events:none; }
      .ic { display:block; overflow:visible; }
      .ic .s { fill:none; stroke:currentColor; stroke-width:6; stroke-linecap:round; stroke-linejoin:round; }
      .ic .f { fill:var(--ifill); stroke:currentColor; stroke-width:6; stroke-linejoin:round; stroke-linecap:round; }
      .ic .k { fill:currentColor; }
      .fn { position:absolute; opacity:0; }
      .fn.v { opacity:1; }
      .fni { position:absolute; left:0; top:0; width:100%; height:100%; }
      .ft { position:absolute; left:0; top:0; width:100%; height:100%; box-sizing:border-box; border-radius:24px; border:3px solid var(--c);
        background:var(--tile); color:var(--c); box-shadow:var(--tile-shadow); display:flex; align-items:center; justify-content:center; }
      .fn.bare .ft { border-color:transparent; background:transparent; box-shadow:none; }
      .fn.box .ft { border-radius:18px; font-family:'Inter', system-ui, sans-serif; font-weight:800; color:var(--text); white-space:nowrap; }
      .ft img { display:block; max-width:72%; max-height:72%; }
      .fcp { position:absolute; box-sizing:border-box; border-radius:24px; border:3px solid var(--c); background:var(--tile); opacity:0.55; }
      .fo { position:absolute; left:-11px; top:-11px; right:-11px; bottom:-11px; border-radius:32px; border:4px solid var(--accent-1);
        box-shadow:0 0 30px rgba(var(--accent-rgb),0.55); opacity:0; }
      .fn.mini .fo { left:-6px; top:-6px; right:-6px; bottom:-6px; border-width:3px; border-radius:14px; }
      .flb { position:absolute; left:50%; transform:translateX(-50%); font-family:'Inter', system-ui, sans-serif; font-weight:800; font-size:28px;
        line-height:34px; color:var(--text); white-space:nowrap; }
      .flb.side { transform:none; }
      .fsb { position:absolute; left:50%; transform:translateX(-50%); font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:22px;
        letter-spacing:1.5px; text-transform:uppercase; color:var(--text-2); white-space:nowrap; }
      .fzw { position:absolute; left:0; top:0; width:0; height:0; }
      .fz { position:absolute; box-sizing:border-box; border-radius:28px; opacity:0; }
      .fz.acc { background:rgba(var(--accent-rgb),0.11); border:2.5px solid rgba(var(--accent-rgb),0.55); }
      .fz.flow { background:rgba(var(--flow-rgb),0.11); border:2.5px solid rgba(var(--flow-rgb),0.55); }
      .fz.s2 { background:color-mix(in srgb, var(--s2) 13%, transparent); border:2.5px solid color-mix(in srgb, var(--s2) 60%, transparent); }
      .fz.s3 { background:color-mix(in srgb, var(--s3) 13%, transparent); border:2.5px solid color-mix(in srgb, var(--s3) 60%, transparent); }
      .fz.ok { background:color-mix(in srgb, var(--ok) 12%, transparent); border:2.5px solid color-mix(in srgb, var(--ok) 60%, transparent); }
      .fz.bad { background:color-mix(in srgb, var(--bad) 12%, transparent); border:2.5px solid color-mix(in srgb, var(--bad) 60%, transparent); }
      .fz.grey { background:var(--track); border:2.5px dashed var(--line-2); }
      .fz.dash { border-style:dashed; }
      .fzl { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:24px; letter-spacing:2.5px;
        text-transform:uppercase; white-space:nowrap; opacity:0; color:var(--text-2); }
      .fzl.acc { color:var(--accent-1); } .fzl.flow { color:var(--flow); } .fzl.s2 { color:var(--s2); } .fzl.s3 { color:var(--s3); }
      .fzl.ok { color:var(--ok); } .fzl.bad { color:var(--bad); }
      .fw { fill:none; stroke:var(--wire); stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }
      .fw.dot { stroke-width:5; }
      .fwlw { position:absolute; left:0; top:0; width:0; height:0; }
      .fwl { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:700; font-size:24px; line-height:32px; letter-spacing:1px;
        text-transform:uppercase; color:var(--text-2); white-space:nowrap; padding:0 10px; border-radius:8px; background:var(--bg); opacity:0; }
      .ftk { position:absolute; left:0; top:0; width:24px; height:24px; margin:-12px 0 0 -12px; border-radius:50%; background:var(--flow);
        box-shadow:0 0 18px rgba(var(--flow-rgb),0.85); opacity:0; z-index:6; }
      .ftk.pk { width:auto; height:36px; margin:-18px 0 0 -36px; padding:0 14px; border-radius:10px; box-sizing:border-box;
        font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:21px; line-height:36px; letter-spacing:1px; color:#101318; white-space:nowrap; }
      .ftk.ok { background:var(--ok); box-shadow:0 0 18px rgba(61,220,151,0.8); } .ftk.bad { background:var(--bad); box-shadow:0 0 18px rgba(255,77,94,0.8); color:#fff; }
      .ftk.acc { background:var(--accent-1); box-shadow:0 0 18px rgba(var(--accent-rgb),0.85); }
      .fbg { position:absolute; font-family:'JetBrains Mono', ui-monospace, monospace; font-weight:800; font-size:24px; line-height:32px; letter-spacing:1.5px;
        text-transform:uppercase; padding:3px 12px; border-radius:8px; white-space:nowrap; opacity:0; z-index:7; background:var(--accent-1); color:var(--on-acc); }
      .fbg.ok { background:var(--ok); color:#101318; } .fbg.bad { background:var(--bad); color:#fff; } .fbg.warn { background:var(--warn); color:#101318; }
      .fbg.flow { background:var(--flow); color:#101318; } .fbg.dim { background:var(--panel-2); color:var(--text-2); border:2px solid var(--line-2); }
      .fmk { position:absolute; opacity:0; z-index:8; }
      .frg { position:absolute; border-radius:50%; border:5px solid var(--accent-1); opacity:0; z-index:5; pointer-events:none; }
      .flmini { position:absolute; box-sizing:border-box; border-radius:20px; background:var(--panel); border:2px solid var(--line); opacity:0.94; }
"""

FLOW_JS = """
      function nIn(sel, t) {
        tl.fromTo(sel, { opacity: 0, scale: 0.55 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.9)", immediateRender: false }, t);
      }
      function nOut(sel, t) { tl.to(sel, { opacity: 0, scale: 0.85, duration: 0.3, ease: "power2.in" }, t); }
      function wDraw(sel, t, d) { tl.fromTo(sel, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d || 0.6, ease: "power2.inOut", immediateRender: false }, t); }
      function tk(sel, t, d, P, hit) {
        tl.set(sel, { x: P[0], y: P[1] }, 0);
        tl.to(sel, { opacity: 1, duration: 0.1 }, t);
        let L = 0; const seg = [];
        for (let i = 2; i < P.length; i += 2) { const l = Math.hypot(P[i] - P[i - 2], P[i + 1] - P[i - 1]); seg.push(l); L += l; }
        let c = t;
        for (let i = 0; i < seg.length; i++) {
          const dd = d * seg[i] / L;
          tl.fromTo(sel, { x: P[2 * i], y: P[2 * i + 1] }, { x: P[2 * i + 2], y: P[2 * i + 3], duration: dd, ease: "none", immediateRender: false }, c);
          c += dd;
        }
        tl.to(sel, { opacity: 0, duration: 0.12 }, t + d - 0.1);
        if (hit) tl.fromTo(hit, { scale: 1 }, { scale: 1.09, duration: 0.11, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t + d - 0.06);
      }
      function pathmv(sel, t, d, P) {
        let L = 0; const seg = [];
        for (let i = 2; i < P.length; i += 2) { const l = Math.hypot(P[i] - P[i - 2], P[i + 1] - P[i - 1]); seg.push(l); L += l; }
        let c = t;
        for (let i = 0; i < seg.length; i++) { const dd = d * seg[i] / L; tl.fromTo(sel, { x: P[2 * i], y: P[2 * i + 1] }, { x: P[2 * i + 2], y: P[2 * i + 3], duration: dd, ease: "none", immediateRender: false }, c); c += dd; }
      }
      function march(sel, t, d, per) { tl.fromTo(sel, { strokeDashoffset: 0 }, { strokeDashoffset: -per * Math.max(1, Math.round(d * 3.4)), duration: d, ease: "none", immediateRender: false }, t); }
      function ring(sel, t) { tl.fromTo(sel, { opacity: 0.95, scale: 0.7 }, { opacity: 0, scale: 1.7, duration: 0.7, ease: "power2.out", immediateRender: false }, t); }
      function shake(sel, t) { tl.to(sel, { keyframes: { x: [0, -9, 8, -6, 4, 0], easeEach: "none" }, duration: 0.42, ease: "none" }, t); }
"""

if "function nIn(" not in kit.COMMON_JS:
    kit.COMMON_JS = kit.COMMON_JS + FLOW_JS
    kit.COMMON_CSS = kit.COMMON_CSS + FLOW_CSS

DASH = (3, 14)          # dotted wires: dash, gap (round caps make dots)
COLOR_TOKENS = {"acc": "accent-1", "ok": "ok", "bad": "bad", "warn": "warn", "flow": "flow", "s2": "s2", "node": "node", "wire": "wire",
                "draft": "draft", "text": "text", "text-2": "text-2"}


def col(name):
    """semantic colour name or literal -> literal hex from the active skin"""
    if name is None:
        return tok("node")
    if name.startswith("#"):
        return name
    return tok(COLOR_TOKENS.get(name, name))


def tw_inter(s, fs=28):
    em = sum(0.3 if c in " .,:;'·" else 0.72 if (c.isupper() or c.isdigit()) else 0.6 for c in s)
    return em * fs


def tw_mono(s, fs=24, ls=1.0):
    return len(s) * (fs * 0.6 + ls)


# ------------------------------------------------------------------ geometry
def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l = math.hypot(dx, dy) or 1.0
    return dx / l, dy / l, l


def _clean(pts):
    out = []
    for p in pts:
        p = (r1(p[0]), r1(p[1]))
        if out and abs(out[-1][0] - p[0]) < 0.5 and abs(out[-1][1] - p[1]) < 0.5:
            continue
        out.append(p)
    k = 1
    while k < len(out) - 1:   # drop collinear middles
        a, b, c = out[k - 1], out[k], out[k + 1]
        if abs((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) < 0.5:
            out.pop(k)
        else:
            k += 1
    return out


def _rounded(pts, rad=20.0):
    """polyline -> (svg d with rounded corners, token polyline sampled through the corners, length)"""
    if len(pts) < 2:
        return "", pts, 0.0
    d = f"M{pts[0][0]},{pts[0][1]}"
    poly = [pts[0]]
    L = 0.0
    cur = pts[0]
    for i in range(1, len(pts) - 1):
        p, q, n = pts[i - 1], pts[i], pts[i + 1]
        ux, uy, l1 = _unit(p, q)
        vx, vy, l2 = _unit(q, n)
        r = min(rad, l1 / 2, l2 / 2)
        a = (r1(q[0] - ux * r), r1(q[1] - uy * r))
        b = (r1(q[0] + vx * r), r1(q[1] + vy * r))
        d += f" L{a[0]},{a[1]} Q{q[0]},{q[1]} {b[0]},{b[1]}"
        L += math.hypot(a[0] - cur[0], a[1] - cur[1])
        poly.append(a)
        for s in (0.5, 1.0):   # two samples through the corner (tokens follow the curve)
            x = (1 - s) ** 2 * a[0] + 2 * (1 - s) * s * q[0] + s * s * b[0]
            y = (1 - s) ** 2 * a[1] + 2 * (1 - s) * s * q[1] + s * s * b[1]
            L += math.hypot(x - poly[-1][0], y - poly[-1][1])
            poly.append((r1(x), r1(y)))
        cur = b
    end = pts[-1]
    d += f" L{end[0]},{end[1]}"
    L += math.hypot(end[0] - cur[0], end[1] - cur[1])
    poly.append(end)
    return d, poly, L


# ------------------------------------------------------------------ the diagram
class Flow:
    """One living diagram. (ox, oy, k) transform the builder's canvas coordinates (k < 1 = a mini)."""

    def __init__(self, S, id, ox=0.0, oy=0.0, k=1.0, labels=True, allvis=False, add=True, mini=False):
        self.S, self.id, self.ox, self.oy, self.k = S, id, ox, oy, k
        self.labels, self.allvis, self.is_mini = labels, allvis, mini
        self.nodes, self.zones, self.wires = {}, {}, {}
        self.order = []          # keys in creation order (for focus)
        self.zone_html, self.node_html, self.over_html, self.tok_html = [], [], [], []
        self.svg_defs, self.svg_wires, self.svg_over = [], [], []
        self._ntk = 0
        self._nov = 0
        self.dimmed = set()
        self.wrap_style = ""     # inline style of the camera wrapper (e.g. "opacity:0" before an entrance)
        if add and S is not None:
            S.add(self)

    # ---------- coordinates
    def P(self, x, y):
        return (r1(self.ox + x * self.k), r1(self.oy + y * self.k))

    def nid(self, key):
        return f"{self.id}-{key}"

    def _vis(self, vis):
        return self.allvis if vis is None else vis

    # ---------- nodes
    def node(self, key, x, y, icon=None, label=None, size=120, sub=None, logo=None, look="tile", color=None,
             w=None, h=None, text=None, fs=30, lpos="b", copies=0, vis=None):
        """A node centred at (x, y). look: tile | bare | box (text inside, w x h). Label <= 4 words."""
        cx, cy = self.P(x, y)
        W = r1((w or size) * self.k)
        H = r1((h or w or size) * self.k)
        c = col(color)
        nid = self.nid(key)
        vis = self._vis(vis)
        if text is not None:
            look = "box"
        if look == "box" and text is not None:
            inner = f'<span style="font-size:{r1(fs * (self.k if self.is_mini else 1))}px;">{esc(text)}</span>' if not self.is_mini else ""
        elif logo:
            inner = f'<img src="{logo}" alt="logo">'
        elif icon:
            inner = icon_svg(icon, min(W, H) * (0.78 if look == "bare" else 0.62))
        else:
            inner = ""
        cps = "".join(f'<div class="fcp" style="left:{r1(10 * (i + 1) * self.k)}px; top:{r1(-10 * (i + 1) * self.k)}px; width:{W}px; height:{H}px; '
                      f'"></div>' for i in range(copies))
        lab = ""
        lh = 0
        if label and self.labels:
            if lpos == "b":
                lab = f'<div id="{nid}-l" class="flb" style="top:{r1(H + 12)}px;">{esc(label)}</div>'
                lh = 46
            elif lpos == "t":
                lab = f'<div id="{nid}-l" class="flb" style="top:-48px;">{esc(label)}</div>'
                lh = 48
            elif lpos == "r":
                lab = f'<div id="{nid}-l" class="flb side" style="left:{r1(W + 18)}px; top:{r1(H / 2 - 17)}px;">{esc(label)}</div>'
            elif lpos == "l":
                lab = f'<div id="{nid}-l" class="flb side" style="right:{r1(W + 18)}px; left:auto; top:{r1(H / 2 - 17)}px;">{esc(label)}</div>'
            if sub and lpos == "b":
                lab += f'<div id="{nid}-sb" class="fsb" style="top:{r1(H + 52)}px;">{esc(sub)}</div>'
                lh = 80
        cls = "fn" + (" v" if vis else "") + ("" if look == "tile" else f" {look}") + (" mini" if self.is_mini else "")
        self.node_html.append(
            f'<div id="{nid}" class="{cls}" style="left:{r1(cx - W / 2)}px; top:{r1(cy - H / 2)}px; width:{W}px; height:{H}px; --c:{c};">'
            f'<div id="{nid}-i" class="fni">{cps}<div id="{nid}-o" class="fo"></div><div id="{nid}-t" class="ft">{inner}</div>{lab}</div></div>')
        lw = tw_inter(label) if (label and self.labels) else 0
        self.nodes[key] = {"x": cx, "y": cy, "w": W, "h": H, "lpos": lpos if lab else None, "lh": lh, "lw": lw, "c": c, "label": label}
        self.order.append(("n", key))
        return nid

    def bbox(self, key, labels=True):
        if key in self.nodes:
            n = self.nodes[key]
            x0, y0, x1, y1 = n["x"] - n["w"] / 2, n["y"] - n["h"] / 2, n["x"] + n["w"] / 2, n["y"] + n["h"] / 2
            if labels and n["lpos"] == "b":
                y1 += n["lh"]
                x0, x1 = min(x0, n["x"] - n["lw"] / 2), max(x1, n["x"] + n["lw"] / 2)
            elif labels and n["lpos"] == "t":
                y0 -= n["lh"]
            elif labels and n["lpos"] == "r":
                x1 += n["lw"] + 18
            elif labels and n["lpos"] == "l":
                x0 -= n["lw"] + 18
            return x0, y0, x1, y1
        if key in self.zones:
            z = self.zones[key]
            return z["x"], z["y"] - (44 if z["label"] else 0), z["x"] + z["w"], z["y"] + z["h"]
        raise SystemExit(f"flow {self.id}: no node/zone {key!r}")

    def anchor(self, key, side, off=0.0, gap=10):
        n = self.nodes[key]
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        lab = n["lh"] if n["lpos"] == side else 0
        if side == "r":
            return (r1(x + w / 2 + gap), r1(y + off))
        if side == "l":
            return (r1(x - w / 2 - gap), r1(y + off))
        if side == "t":
            return (r1(x + off), r1(y - h / 2 - gap - lab))
        if side == "b":
            return (r1(x + off), r1(y + h / 2 + gap + lab))
        raise ValueError(side)

    # ---------- zones
    def zone(self, key, x, y, w, h, label=None, tint="acc", dash=False, lpos="tl", vis=None):
        """translucent group rectangle (canvas px of its box), label tab outside its top edge"""
        X, Y = self.P(x, y)
        W, H = r1(w * self.k), r1(h * self.k)
        zid = self.nid(key)
        vis = self._vis(vis)
        op = "" if not vis else " style=\"opacity:1\""
        lab = ""
        if label and self.labels:
            lx = X + 6 if lpos == "tl" else X + W - tw_mono(label, 24, 2.5) - 6
            lab = (f'<div id="{zid}-l" class="fzl {tint}" style="left:{r1(lx)}px; top:{r1(Y - 40)}px;{" opacity:1;" if vis else ""}">'
                   f'{esc(label)}</div>')
        self.zone_html.append(
            f'<div id="{zid}" class="fzw"><div id="{zid}-b" class="fz {tint}{" dash" if dash else ""}" '
            f'style="left:{X}px; top:{Y}px; width:{W}px; height:{H}px;{" opacity:1;" if vis else ""}"></div>{lab}</div>')
        self.zones[key] = {"x": X, "y": Y, "w": W, "h": H, "label": label if (label and self.labels) else None}
        self.order.append(("z", key))
        return zid

    # ---------- wires
    def wire(self, key, a, b, sa=None, sb=None, route="auto", via=None, pts=None, dash=False, head="end", label=None,
             color=None, oa=0.0, ob=0.0, mid=None, lt=None, lside=None, vis=None, rad=20):
        """Routed connector a -> b (node keys; or pts=[(x, y), ...] canvas px for a free path).
        sa/sb: anchor sides l|r|t|b (auto from geometry); route: auto | straight | hvh | vhv | hv | vh;
        via: extra canvas points; oa/ob: offset the anchors sideways (parallel request/reply pairs);
        dash: dotted wire (draws through a mask, can march); head: end | start | both | None."""
        wid = self.nid(key)
        if pts is None:
            A, B = self.nodes[a], self.nodes[b]
            dx, dy = B["x"] - A["x"], B["y"] - A["y"]
            if sa is None:
                sa = ("r" if dx > 0 else "l") if abs(dx) >= abs(dy) else ("b" if dy > 0 else "t")
            if sb is None:
                sb = ("l" if dx > 0 else "r") if abs(dx) >= abs(dy) else ("t" if dy > 0 else "b")
            p0, p1 = self.anchor(a, sa, oa), self.anchor(b, sb, ob)
            if via:
                mids = [self.P(*v) for v in via]
            else:
                hz0, hz1 = sa in "lr", sb in "lr"
                r_ = route
                if r_ == "auto":
                    if hz0 and hz1:
                        r_ = "straight" if abs(p0[1] - p1[1]) < 1 else "hvh"
                    elif not hz0 and not hz1:
                        r_ = "straight" if abs(p0[0] - p1[0]) < 1 else "vhv"
                    else:
                        r_ = "hv" if hz0 else "vh"
                if r_ == "straight":
                    mids = []
                elif r_ == "hvh":
                    mx = self.P(mid, 0)[0] if mid is not None else (p0[0] + p1[0]) / 2
                    mids = [(mx, p0[1]), (mx, p1[1])]
                elif r_ == "vhv":
                    my = self.P(0, mid)[1] if mid is not None else (p0[1] + p1[1]) / 2
                    mids = [(p0[0], my), (p1[0], my)]
                elif r_ == "hv":
                    mids = [(p1[0], p0[1])]
                elif r_ == "vh":
                    mids = [(p0[0], p1[1])]
                else:
                    raise ValueError(route)
            P_ = _clean([p0] + mids + [p1])
        else:
            P_ = _clean([self.P(*p) for p in pts])
        d, poly, L = _rounded(P_, rad * self.k if self.is_mini else rad)
        vis = self._vis(vis)
        c = col(color) if color else None
        st = f"stroke:{c};" if c else ""
        heads = ""
        for end in (("end",) if head == "end" else ("start",) if head == "start" else ("end", "start") if head == "both" else ()):
            if end == "end":
                q, p = P_[-1], P_[-2]
            else:
                q, p = P_[0], P_[1]
            ux, uy, _ = _unit(p, q)
            hs = 15 if not self.is_mini else max(6, 15 * self.k * 1.6)
            a1 = (r1(q[0] - hs * ux + hs * 0.62 * uy), r1(q[1] - hs * uy - hs * 0.62 * ux))
            a2 = (r1(q[0] - hs * ux - hs * 0.62 * uy), r1(q[1] - hs * uy + hs * 0.62 * ux))
            hid = f"{wid}-h" if end == "end" else f"{wid}-h2"
            heads += (f'<path id="{hid}" class="fw" d="M{a1[0]},{a1[1]} L{q[0]},{q[1]} L{a2[0]},{a2[1]}" '
                      f'style="{st}{"" if vis else "opacity:0;"}"/>')
        if dash:
            self.svg_defs.append(f'<mask id="{wid}-m" maskUnits="userSpaceOnUse" x="-200" y="-200" width="2320" height="1480">'
                                 f'<path id="{wid}-mp" d="{d}" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" pathLength="1" '
                                 f'style="stroke-dasharray:1; stroke-dashoffset:{0 if vis else 1};"/></mask>')
            body = (f'<path id="{wid}-p" class="fw dot" d="{d}" mask="url(#{wid}-m)" '
                    f'style="{st}stroke-dasharray:{DASH[0]} {DASH[1]};{"" if vis else " opacity:0;"}"/>')
        else:
            body = (f'<path id="{wid}-p" class="fw" d="{d}" pathLength="1" style="{st}stroke-dasharray:1; stroke-dashoffset:{0 if vis else 1};{"" if vis else " opacity:0;"}"/>')
        self.svg_wires.append(f'<g id="{wid}">{body}{heads}</g>')
        lab_pos = None
        if label and self.labels:
            segs = [(P_[i], P_[i + 1]) for i in range(len(P_) - 1)]
            if lt is not None:
                s0, s1 = segs[min(int(lt), len(segs) - 1)]
            else:
                s0, s1 = max(segs, key=lambda s: math.hypot(s[1][0] - s[0][0], s[1][1] - s[0][1]))
            mx, my = (s0[0] + s1[0]) / 2, (s0[1] + s1[1]) / 2
            lw = tw_mono(label) + 20
            horiz = abs(s1[1] - s0[1]) < abs(s1[0] - s0[0])
            side = lside or ("t" if horiz else "r")
            if side == "t":
                lx, ly = mx - lw / 2, my - 44
            elif side == "b":
                lx, ly = mx - lw / 2, my + 14
            elif side == "r":
                lx, ly = mx + 16, my - 15
            else:
                lx, ly = mx - 16 - lw, my - 15
            self.over_html.append(f'<div id="{wid}-lw" class="fwlw"><div id="{wid}-l" class="fwl" style="left:{r1(lx)}px; top:{r1(ly)}px;'
                                  f'{" opacity:1;" if vis else ""}">{esc(label)}</div></div>')
            lab_pos = (lx, ly, lw)
        self.wires[key] = {"pts": P_, "poly": poly, "len": L, "dash": dash, "a": a, "b": b, "label": lab_pos,
                           "heads": [h for h in (("end",) if head == "end" else ("start",) if head == "start" else ("end", "start") if head == "both" else ())]}
        self.order.append(("w", key))
        return wid

    def bundle(self, key, a, b, n=5, spread=18, **kw):
        """n parallel straight wires a -> b (volume: five lines of reads vs one write)"""
        keys = []
        for i in range(n):
            o = (i - (n - 1) / 2) * spread
            self.wire(f"{key}{i}", a, b, route="straight", oa=o, ob=o, **kw)
            keys.append(f"{key}{i}")
        return keys

    # ---------- reveal
    def show(self, t, *keys, d=None, stagger=0.0):
        """pop nodes / wipe zones / draw wires on the spoken word (keys in any mix)"""
        for i, key in enumerate(keys):
            tt = r2(max(0.02, t + i * stagger))
            if key in self.nodes:
                self.S.J(f'nIn("#{self.nid(key)}", {tt});')
            elif key in self.zones:
                zid = self.nid(key)
                self.S.J(f'tl.fromTo("#{zid}-b", {{ opacity: 0, clipPath: "inset(0% 100% 0% 0%)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0%)", '
                         f'duration: {d or 0.65}, ease: "power3.out", immediateRender: false }}, {tt});')
                if self.zones[key]["label"]:
                    self.S.J(f'tl.fromTo("#{zid}-l", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, immediateRender: false }}, {r2(tt + 0.25)});')
            elif key in self.wires:
                w = self.wires[key]
                wid = self.nid(key)
                dd = d or round(min(1.0, max(0.35, w["len"] / 900)), 2)
                vis_sel = [f"#{wid}-p"] + [f"#{wid}-h" if h == "end" else f"#{wid}-h2" for h in w["heads"]]
                self.S.J(f'tl.set("{", ".join(vis_sel[:1])}", {{ opacity: 1 }}, {tt});')   # undrawn paths start at opacity 0 (and undo a hide)
                self.S.J(f'wDraw("#{wid}-{"mp" if w["dash"] else "p"}", {tt}, {dd});')
                for h in w["heads"]:
                    hid = f"{wid}-h" if h == "end" else f"{wid}-h2"
                    ht = tt + dd - 0.08 if h == "end" else tt
                    self.S.J(f'tl.to("#{hid}", {{ opacity: 1, duration: 0.15 }}, {r2(ht)});')
                if w["label"]:
                    self.S.J(f'tl.fromTo("#{wid}-l", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, immediateRender: false }}, {r2(tt + dd * 0.5)});')
            else:
                raise SystemExit(f"flow {self.id}: show() unknown key {key!r}")
        return self

    def build(self, t0, keys, step=0.35):
        """reveal keys one after another (a node, then its wire, then the next node ...)"""
        for i, k in enumerate(keys):
            self.show(t0 + i * step, k)
        return t0 + len(keys) * step

    def hide(self, t, *keys, d=0.3):
        for key in keys:
            if key in self.nodes:
                self.S.J(f'nOut("#{self.nid(key)}", {r2(t)});')
            elif key in self.zones:
                self.S.J(f'tl.to("#{self.nid(key)}-b, #{self.nid(key)}-l", {{ opacity: 0, duration: {d} }}, {r2(t)});')
            elif key in self.wires:
                # hide the paths (not the group): focus()/unfocus() own the group's opacity
                wid = self.nid(key)
                sels = [f"#{wid}-p"] + [f"#{wid}-h" if h == "end" else f"#{wid}-h2" for h in self.wires[key]["heads"]]
                if self.wires[key]["label"]:
                    sels.append(f"#{wid}-l")
                self.S.J(f'tl.to("{", ".join(sels)}", {{ opacity: 0, duration: {d} }}, {r2(t)});')
        return self

    # ---------- motion along wires
    def flow(self, key, t0, t1, every=0.8, speed=460, label=None, cls="", back=False, hit=True, n=None, size=None):
        """tokens travel the wire from t0 until t1 (a new one every `every` s). label= makes packets
        ("GET", "200"); cls = ok | bad | acc recolours them; back=True runs b -> a; hit pulses the target.
        Tokens are LIFE, not information: the static gate ignores small movers, so pair a long flow
        with a big change every <= 4 s (zone wipe, focus, camera, fband)."""
        w = self.wires[key]
        P_ = list(reversed(w["poly"])) if back else w["poly"]
        trip = round(min(2.6, max(0.5, w["len"] / speed)), 2)
        starts, t = [], t0
        while t + trip <= t1 + 1e-6 and (n is None or len(starts) < n):
            starts.append(round(t, 2))
            t += every
        if not starts:
            starts = [round(t0, 2)]
            trip = round(max(0.35, min(trip, t1 - t0)), 2)
        tgt = (w["a"] if back else w["b"])
        hit_sel = f'"#{self.nid(tgt)}-t"' if (hit and tgt in self.nodes) else "null"
        flat = ",".join(f"{p[0]},{p[1]}" for p in P_)
        for ts in starts:
            tid = f"{self.id}-tk{self._ntk}"
            self._ntk += 1
            if label:
                self.tok_html.append(f'<div id="{tid}" class="ftk pk {cls}" data-fit-allow="text">{esc(label)}</div>')
            else:
                sz = f" width:{size}px; height:{size}px; margin:-{size / 2}px 0 0 -{size / 2}px;" if size else ""
                self.tok_html.append(f'<div id="{tid}" class="ftk {cls}" style="{sz}"></div>')
            self.S.J(f'tk("#{tid}", {ts}, {trip}, [{flat}], {hit_sel});')
        return starts[-1] + trip

    def march(self, key, t0, t1):
        """dotted wire: the dots crawl a -> b from t0 to t1 (the ByteByteGo 'flow' look)"""
        if not self.wires[key]["dash"]:
            WARN.append(f"flow {self.id}: march({key}) needs dash=True")
            return self
        self.S.J(f'march("#{self.nid(key)}-p", {r2(t0)}, {r2(t1 - t0)}, {DASH[0] + DASH[1]});')
        return self

    def carry(self, key, sel, t, d=1.2, back=False):
        """move an existing element (a ticket card, a file) along the wire's path; sel is positioned by
        its centre at (0, 0) of the flow (use a div with left:0; top:0 and a negative margin)"""
        w = self.wires[key]
        P_ = list(reversed(w["poly"])) if back else w["poly"]
        flat = ",".join(f"{p[0]},{p[1]}" for p in P_)
        self.S.J(f'pathmv("{sel}", {r2(t)}, {d}, [{flat}]);')
        return self

    # ---------- states
    def on(self, t, *keys, lit=True):
        """accent ring on (or off) a node: 'this one'"""
        for k in keys:
            self.S.J(f'tl.to("#{self.nid(k)}-o", {{ opacity: {1 if lit else 0}, duration: 0.35, ease: "power2.out" }}, {r2(t)});')
        return self

    def off(self, t, *keys):
        return self.on(t, *keys, lit=False)

    def paint(self, t, key, color, d=0.35):
        """recolour a node (tile border + icon) or a wire: color = ok | bad | warn | acc | flow | node | #hex"""
        c = col(color)
        if key in self.nodes:
            self.S.J(f'tl.to("#{self.nid(key)}", {{ "--c": "{c}", duration: {d}, ease: "power2.out" }}, {r2(t)});')
        elif key in self.wires:
            wid = self.nid(key)
            sels = [f"#{wid}-p"] + [f"#{wid}-h" if h == "end" else f"#{wid}-h2" for h in self.wires[key]["heads"]]
            self.S.J(f'tl.to("{", ".join(sels)}", {{ stroke: "{c}", duration: {d}, ease: "power2.out" }}, {r2(t)});')
        return self

    def _overlay_in_node(self, key, html):
        """append html inside the node's dim wrapper (rides with the node)"""
        nid = self.nid(key)
        for i, h in enumerate(self.node_html):
            if h.startswith(f'<div id="{nid}" '):
                self.node_html[i] = h[:-len("</div></div>")] + html + "</div></div>"
                return
        raise SystemExit(f"flow {self.id}: no node {key!r}")

    def badge(self, key, text, t, cls="", pos="tr", t_out=None):
        """filled chip pinned to a node corner (PRIMARY, x3, HIT, 200 OK). <= 2 words."""
        n = self.nodes[key]
        bid = f"{self.nid(key)}-bg{self._nov}"
        self._nov += 1
        bw = tw_mono(text, 24, 1.5) + 24
        W, H = n["w"], n["h"]
        x, y = {"tr": (W - 26, -24), "tl": (-bw + 26, -24), "t": ((W - bw) / 2, -46), "r": (W + 16, H / 2 - 18),
                "l": (-bw - 16, H / 2 - 18), "b": ((W - bw) / 2, H + 12)}[pos]
        self._overlay_in_node(key, f'<div id="{bid}" class="fbg {cls}" style="left:{r1(x)}px; top:{r1(y)}px;">{esc(text)}</div>')
        self.S.J(f'tl.fromTo("#{bid}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)", immediateRender: false }}, {r2(t)});')
        if t_out:
            self.S.J(f'tl.to("#{bid}", {{ opacity: 0, duration: 0.25 }}, {r2(t_out)});')
        return bid

    def _mark(self, key, t, kind):
        n = self.nodes[key]
        mid = f"{self.nid(key)}-mk{self._nov}"
        self._nov += 1
        s = 58 if not self.is_mini else 24
        svg = icon_svg("cross" if kind == "x" else "check", s)
        fill = "var(--bad)" if kind == "x" else "var(--ok)"
        svg = svg.replace('class="ic"', f'class="ic" style="color:#FFFFFF; --ifill:{fill};"')
        self._overlay_in_node(key, f'<div id="{mid}" class="fmk" style="left:{r1(n["w"] - s * 0.55)}px; top:{r1(-s * 0.45)}px;">{svg}</div>')
        self.S.J(f'tl.fromTo("#{mid}", {{ opacity: 0, scale: 1.8, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "power4.in", immediateRender: false }}, {r2(t)});')
        return mid

    def fail(self, t, key, shake_it=True):
        """red X slams on the node, the node turns red and shakes"""
        self._mark(key, t, "x")
        self.paint(t + 0.05, key, "bad")
        if shake_it:
            self.S.J(f'shake("#{self.nid(key)}-t", {r2(t + 0.12)});')
        return self

    def ok(self, t, key):
        """green check badge on the node"""
        self._mark(key, t, "ok")
        return self

    def pulse(self, t, key, color=None):
        """one expanding ring around a node (attention without a label)"""
        n = self.nodes[key]
        rid = f"{self.nid(key)}-rg{self._nov}"
        self._nov += 1
        s = max(n["w"], n["h"]) + 30
        st = f" border-color:{col(color)};" if color else ""
        self._overlay_in_node(key, f'<div id="{rid}" class="frg" style="left:{r1((n["w"] - s) / 2)}px; top:{r1((n["h"] - s) / 2)}px; width:{r1(s)}px; height:{r1(s)}px;{st}"></div>')
        self.S.J(f'ring("#{rid}", {r2(t)});')
        return self

    def relabel(self, t, key, text):
        self.S.J(f'tl.call(function () {{ const e = document.querySelector("#{self.nid(key)}-l"); if (e) e.textContent = {text!r}; }}, null, {r2(t)});')
        return self

    # ---------- attention: focus (dim the rest) + camera
    def _dimsel(self, kind, key):
        i = self.nid(key)
        if kind == "n":
            return [f"#{i}-i"]
        if kind == "z":
            return [f"#{i}"]
        s = [f"#{i}"]
        if self.wires[key]["label"]:
            s.append(f"#{i}-lw")
        return s

    def focus(self, t, keys, o=0.16, d=0.45, wires=True):
        """dim everything except keys (wires between two kept nodes stay lit when wires=True)"""
        keep = set(keys)
        if wires:
            for k, w in self.wires.items():
                if w["a"] in keep and w["b"] in keep:
                    keep.add(k)
        dim, lit = [], []
        for kind, k in self.order:
            (lit if k in keep else dim).extend(self._dimsel(kind, k))
        if dim:
            self.S.J(f'tl.to("{", ".join(dim)}", {{ opacity: {o}, duration: {d}, ease: "power2.out" }}, {r2(t)});')
        if lit:
            self.S.J(f'tl.to("{", ".join(lit)}", {{ opacity: 1, duration: {d}, ease: "power2.out" }}, {r2(t)});')
        return self

    def unfocus(self, t, d=0.45):
        allsel = [s for kind, k in self.order for s in self._dimsel(kind, k)]
        self.S.J(f'tl.to("{", ".join(allsel)}", {{ opacity: 1, duration: {d}, ease: "power2.out" }}, {r2(t)});')
        return self

    def frame(self, t, keys=None, pad=80, d=1.1, kmax=1.9, cx=960, cy=560, area=(1700, 760), ease="power3.inOut"):
        """camera: fit the bbox of keys (nodes / zones, labels included) into area around (cx, cy);
        frame(t) with no keys returns to the full board. Keep the result on canvas (DESIGN.md)."""
        if not keys:
            x = y = 0
            k = 1
        else:
            bb = [self.bbox(k_) for k_ in keys]
            x0, y0 = min(b[0] for b in bb) - pad, min(b[1] for b in bb) - pad
            x1, y1 = max(b[2] for b in bb) + pad, max(b[3] for b in bb) + pad
            k = min(area[0] / (x1 - x0), area[1] / (y1 - y0), kmax)
            x = cx - k * (x0 + x1) / 2
            y = cy - k * (y0 + y1) / 2
        self.S.J(f'tl.to("#{self.id}", {{ x: {r1(x)}, y: {r1(y)}, scale: {round(k, 3)}, transformOrigin: "0 0", duration: {d}, ease: "{ease}" }}, {r2(t)});')
        return self

    def move(self, t, x=0, y=0, k=1.0, d=0.9, ease="power3.inOut"):
        """move/scale the whole diagram (transform origin = canvas 0,0): result = k * p + (x, y)"""
        self.S.J(f'tl.to("#{self.id}", {{ x: {r1(x)}, y: {r1(y)}, scale: {k}, transformOrigin: "0 0", duration: {d}, ease: "{ease}" }}, {r2(t)});')
        return self

    def all_keys(self):
        return [k for _, k in self.order]

    def extent(self, labels=True):
        bb = [self.bbox(k, labels) for kind, k in self.order if kind in "nz"]
        return min(b[0] for b in bb), min(b[1] for b in bb), max(b[2] for b in bb), max(b[3] for b in bb)

    # ---------- render
    def html(self):
        svg = (f'<svg class="flsvg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs>{"".join(self.svg_defs)}</defs>'
               f'{"".join(self.svg_wires)}{"".join(self.svg_over)}</svg>')
        st = f' style="{self.wrap_style}"' if self.wrap_style else ""
        return (f'<div id="{self.id}" class="fl" data-layout-allow-overflow{st}>' + "".join(self.zone_html) + svg + "".join(self.node_html)
                + "".join(self.over_html) + "".join(self.tok_html) + "</div>")


# ------------------------------------------------------------------ the persistent object, small
def mini(S, id, builder, box, lit=(), panel=True, t_in=None):
    """Mount the video's system builder again as a locator inside box=(x, y, w, h): every part visible,
    no labels, the nodes in `lit` ringed. Returns the Flow (use .on/.off/.paint/.fail on it).
    builder(G) must only call G.node / G.zone / G.wire (no reveal verbs)."""
    probe = Flow(None, id + "-probe", add=False, allvis=True, labels=False)
    builder(probe)
    x0, y0, x1, y1 = probe.extent(labels=False)
    bx, by, bw, bh = box
    padx, pady = 22, 22
    k = min((bw - 2 * padx) / (x1 - x0), (bh - 2 * pady) / (y1 - y0))
    ox = bx + (bw - k * (x1 - x0)) / 2 - k * x0
    oy = by + (bh - k * (y1 - y0)) / 2 - k * y0
    if panel:
        hid = " opacity:0;" if t_in is not None else ""
        S.add(f'<div id="{id}-pn" class="flmini" style="left:{bx}px; top:{by}px; width:{bw}px; height:{bh}px;{hid}"></div>')
    G = Flow(S, id, ox, oy, k, labels=False, allvis=True, mini=True)
    builder(G)
    for key in lit:   # lit in the markup (a tl.set at 0 would not render frame 0)
        o = f'id="{G.nid(key)}-o" class="fo"'
        G.node_html = [h.replace(o, o + ' style="opacity:1;"') for h in G.node_html]
    if t_in is not None:
        G.wrap_style = "opacity:0"          # hidden in the markup (a tl.set at 0 would not render frame 0)
        msel = f"#{id}, #{id}-pn" if panel else f"#{id}"
        S.J(f'tl.fromTo("{msel}", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out", immediateRender: false }}, {r2(t_in)});')
    return G
