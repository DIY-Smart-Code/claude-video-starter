# flow-explainer API (what `build/video_scenes.py` may call)

All times are scene-local seconds from `S.p("unique phrase", k=0, end=False)` (word k of a phrase that occurs
exactly once in the narration; `k=-1` is its last word), plus small offsets. Ids are unique per scene.
Positions are canvas px on a 1920 x 1080 frame. Start from the demo (`build/video_scenes.py`).

## Scene plumbing (`kit`, `atoms`)

| Call | Does |
|---|---|
| `S = Stage("id")` … `S.write(title)` | one scene file; `S.dur` = scene length; `S.tail_ok = "reason"` for the last scene |
| `S.p(phrase, k=0, end=False)` | the time of a word |
| `S.add(html)` / `S.J(js)` | raw markup / one GSAP line (`tl.to(...)`, `pop("#id", t)`) when no atom fits |
| `S.cam(t, scale, x, y)` | camera on the whole scene |
| `atoms.setup(VIDEO)` | skin + palette + marker language; call right after `VIDEO` |
| `appear(S, id, t, how)` | reveal: `pop` `l` `r` `up` `slam` `fade` |
| `out(S, sel, t)` / `to(S, sel, t, "x: 40, opacity: 0.3")` | hide / tween transforms, opacity, colours |
| `grow_x(S, sel, t)` | a bar grows from the left |
| `el(S, id, cls, x, y, inner, style)` | a positioned div with an atom class |
| `fill(S, G.nid(key), t, tok("ok"))` / `unfill(S, G.nid(key), t)` | solid colour fill of a node (the big state change on paper) / back to plain |
| `tok("accent-1")` / `rgba(hex, a)` | literal colours for GSAP (never `var()` in a tween) |

## The living diagram (`flow.Flow`)

Build (inside `SYSTEM(G)` only these three):
`G.node(key, x, y, icon, label, size=120, sub=None, logo=None, color=None, text=None, w=None, h=None, lpos="b", copies=0)`,
`G.zone(key, x, y, w, h, label, tint="acc", lpos="tl")`,
`G.wire(key, a, b, sa=None, sb=None, route="auto", pts=None, dash=False, head="end", label=None, oa=0, ob=0, mid=None)`.
`color` / `tint`: `acc` `flow` `ok` `bad` `warn` `node` `grey`. `text=` makes a box node. `pts=[(x, y), ...]` is a free wire.

Icons (39): server db cache queue cloud cpu user users browser phone lb api doc folder lock key shield gear
globe clock mail bell chart search bulb eye check cross warn layers box code branch spark bot terminal map camera ticket.

Mount: `G = Flow(S, "G", ox, oy, k, allvis=False)` then `SYSTEM(G)`; `allvis=True` shows everything at once.
`mini(S, "loc", SYSTEM, (96, 112, 520, 120), lit=["q"], t_in=0.05)` mounts it again as a small locator
(returns a Flow: `.on` `.off` `.pulse` `.flow` work on it).

Animate: `G.show(t, *keys, stagger=0)`, `G.build(t0, keys, step=0.35)`, `G.hide(t, *keys)`,
`G.flow(wire, t0, t1, every=0.8, label=None, cls="", back=False, n=None)` (packets; `n=1` one packet, `t1=99` = no end),
`G.march(wire, t0, t1)` (dotted wires), `G.carry(wire, sel, t)`, `G.on/off(t, *keys)` (ring), `G.pulse(t, key, color)`,
`G.paint(t, key, color)`, `G.badge(key, text, t, cls, pos="tr", t_out=None)` (<= 3 words), `G.fail(t, key)`, `G.ok(t, key)`,
`G.relabel(t, key, text)`, `G.focus(t, keys, o=0.16)` / `G.unfocus(t)`, `G.frame(t, keys)` (zoom to fit), `G.move(t, x, y, k)`.
`G.nid(key)` is a node's DOM id (for `fill`).

## Atoms (`atoms`)

| Atom | Shows | Topic shapes it fits |
|---|---|---|
| `chp(S, id, txt, x, y, kind, t, big=False, center=False, occl=False)` → (x, w) | mono chip, <= 4 words; kind `acc ok bad flow ink warn draft ghost` | any label, value, verdict |
| `strike_bar(S, id, x, y, w, t)` | red strike through a chip (give the chip `occl=True`) | "doesn't exist", "not sent", "no promise" |
| `recommend(S, id, x, y, t)` / `open_q(S, id, txt, x, y, t)` | green RECOMMENDED / amber OPEN · … | proposals, open questions |
| `example_tag(S, id, x, y, t)` / `draft_stamp(S, id, x, y, t, txt)` | violet EXAMPLE / slammed NOT MEASURED | made-up or derived numbers |
| `chapter_card(S, id, "D1", "Signature", t)` | the chapter's card top right | every chapter |
| `title_xl(S, id, "4 decisions", kw=["4"])` | frame-0 title | the hook |
| `deck(...)` → `deck_jostle` / `deck_row` / `deck_hop` | a pile of cards that files into a row; a card hops on its part | "N decisions / steps / reasons" hooks |
| `board(S, id, groups, y0)` → `board_in` / `board_lit` / `board_rect` | grouped cards in columns | decisions in groups, options, a recap |
| `track` / `ticks` / `ticks_to` / `events` / `span` / `span_to` / `target` | a time track, marks that re-space, event docs, a worst-case gap, a deadline | cadences, retries, SLAs, "by tomorrow" |
| `pages(...)` + `scan(...)` / `lens_sweep(...)` | pages read row by row until a hit; a magnifier sweep | search, pagination, audits, "how do we know" |
| `dials(...)` / `dials_turn(...)` | setting dials per item | per-customer / per-tenant settings |
| `value_card(...)` / `row_mark(...)` | a small ledger, rows tinted | bills, before/after, balances |
| `gantt(...)` / `gantt_bar(...)` | phases x workstreams, bars grow; dashed = waiting | rollouts, migrations, who does what when |
| `capacity(S, id, parts, limit, x0, y, unit, t_frame)` | stacked parts vs a limit line, red overflow | quotas, rate limits, budgets, load |
| `bar(S, id, x, y, w, frac, t, kind, label, dashed)` | a progress bar | partial payment, coverage, equivalence |
| `list_card` / `list_fail` / `cross` | a big card that breaks and is crossed out | "there is no list / feed / report" |

## Explainer helpers (`explain`)

`anatomy(S, id, parts, x, y, fs)` + `anat_in` / `anat_part` (a header, URL, key or command taken apart),
`fband(S, prefix, [(t, (x, y, w, h)), (t, None)])` (attention frame; start a step only when its content is there),
`heads(S, prefix, [(t, text, kw)])` (a headline that swaps, <= 6 words), `ladder` / `ladder_go` (steps joined
by arrows), `gloss` / `gloss_in` (term = meaning rail), `sprawl` / `sprawl_order` (chaos to order hook),
`bubble` (a quote, <= 5 words), `slam_plate` (once per video), `meter` / `meter_to`, `cells` / `cells_fill`,
`table` / `row_hl` / `table_scan`, `road` / `road_go` (a roadmap of stops), `recap` / `recap_row`,
`cnt` + `tick` (a counter), `tag` / `tag_row`, `note_card`.

Evidence components (`kit`, optional, need real captures): `Ev` (a screenshot card), `Br` (browser frame),
`Term` (recorded terminal lines), `Code` (real code, line reveals), `player` (a muted screen recording).

## Recipes (from a proven 4.5-minute decision briefing)

- **Hook:** `title_xl` + a `deck` pile on frame 0 → the pile jostles on the first stake word → files into a
  row while the system builds as a ghost below → each card hops while its part pulses.
- **Map:** the whole `SYSTEM` as a ghost (`allvis=True` + `focus(0.05, [first])`), each part lit on its word,
  one packet per wire as it is named.
- **Decision chapter:** `chapter_card` → `focus` on the parts it touches → the problem (chips, a failing packet,
  `fail`, strikes) → `recommend` on "recommended" → `open_q` for what is open → `fband` follows the narration.
- **Close-up:** `mini()` locator top left + one atom (pages + scan, a track, a capacity bar, a gantt).
- **Close:** `board` of the chapters + `mini` of the system; each group lights with its parts ringed; one
  packet race; the verdict as an ink chip.
