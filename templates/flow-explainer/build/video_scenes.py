"""DEMO video for the flow-explainer template: "How a webhook reaches your app" (4 decisions, 7 scenes).

This file is THE per-video file. A new video replaces all of it except the import block and the
`setup(VIDEO)` call; keep the structure:
  VIDEO        the scene table (phrase anchors), chapters, skin + topic palette, language
  SYSTEM(G)    the ONE persistent object (only G.node / G.zone / G.wire), reused in every scene
  scenes       one function per VIDEO["scenes"] row; every time comes from S.p("unique phrase")
Read DESIGN.md (the style contract) and API.md (every atom with an example) before writing scenes.
"""
import kit
from kit import Stage, tok                      # noqa: F401
from flow import Flow, mini                     # noqa: F401
from explain import fband, anatomy, anat_in, anat_part, heads   # noqa: F401
from atoms import *                             # noqa: F401,F403
import atoms

SRC = "demo topic: webhook delivery"

VIDEO = {
    "title": "How a webhook reaches your app",
    "seed": "flow-explainer-demo",          # deterministic backdrop placement
    "skin": "paper",                          # paper | dark
    "palette": {"accent-1": "#2F5BD3", "flow": "#E2683A"},   # subject colour + things in motion
    "lang": "en",
    "backdrop": ["api", "queue", "shield"],  # three icons from the system -> ghosted topic shapes
    "hud_prefix": "",
    "source_label": "TOPIC",
    "chapters": ["Overview", "The path", "D1 Signature", "D2 Retries", "D3 Duplicates", "D4 Load", "Recap"],
    "scenes": [
        {"id": "intro", "first": None, "chapter": 1, "title": "4 decisions, one event", "source": SRC},
        {"id": "path", "first": "Where does the event start?", "enter": "left", "chapter": 2, "title": "The path", "source": SRC},
        {"id": "sig", "first": "Decision one is the signature.", "enter": "left", "chapter": 3, "title": "D1 signature", "source": SRC},
        {"id": "retry", "first": "Decision two is the retry plan.", "enter": "left", "chapter": 4, "title": "D2 retries", "source": SRC},
        {"id": "dupe", "first": "Decision three is duplicates.", "enter": "left", "chapter": 5, "title": "D3 duplicates", "source": SRC},
        {"id": "load", "first": "Decision four is load.", "enter": "left", "chapter": 6, "title": "D4 load", "source": SRC},
        {"id": "close", "first": "Four decisions, one path.", "enter": "up", "chapter": 7, "title": "Recap", "source": SRC},
    ],
    "cta": None,
    "terminal_hold": 3.0,
}
atoms.setup(VIDEO)


def title(sid):
    return next(s["title"] for s in VIDEO["scenes"] if s["id"] == sid)


# ================================================================ THE persistent object
CHAIN = ["shop", "end", "ver", "q", "work", "db"]
BUILD_SEQ = [k for i, c in enumerate(CHAIN) for k in ([c] + ([f"w{i + 1}"] if i < len(CHAIN) - 1 else []))]


def SYSTEM(G):
    """the event path at full size (row y 540): only node / zone / wire calls"""
    G.zone("app", 420, 430, 1400, 270, "your app", "acc", lpos="tr")
    G.node("shop", 220, 540, "browser", "Shop", size=120, color="flow")
    G.node("end", 560, 540, "api", "Endpoint", size=112, color="acc")
    G.node("ver", 820, 540, "shield", "Verify", size=112, color="acc")
    G.node("q", 1080, 540, "queue", "Queue", size=112, sub="seen IDs", color="acc")
    G.node("work", 1340, 540, "gear", "Worker", size=112, color="acc")
    G.node("db", 1640, 540, "db", "Database", size=120, color="acc")
    for i in range(len(CHAIN) - 1):
        G.wire(f"w{i + 1}", CHAIN[i], CHAIN[i + 1])


def sysflow(S, dy=0):
    G = Flow(S, "G", 0, dy, 1.0, allvis=True)
    SYSTEM(G)
    return G


DECKS = [("D1", "Signature"), ("D2", "Retries"), ("D3", "Duplicates"), ("D4", "Load")]


# ================================================================ 1 intro: four decisions, one event
def intro():
    S = Stage("intro")
    title_xl(S, "i-t", "4 decisions", kw=["4"], y=150)             # frame 0: the idea as a picture
    dxy = deck(S, "i-c", DECKS, y=430, scatter=[(330, 520), (760, 650), (1150, 470), (1490, 610)])
    deck_jostle(S, "i-c", 4, S.p("whether a webhook", 1))
    t_w = S.p("walks one event")
    to(S, "#i-t", t_w, "y: -46, scale: 0.56", d=0.7, ease="power3.inOut")
    deck_row(S, "i-c", dxy, t_w)
    G = Flow(S, "G", 0, 250)
    SYSTEM(G)
    G.show(t_w + 0.4, "app")
    G.build(t_w + 0.5, BUILD_SEQ, step=0.06)
    for i in range(5):
        G.flow(f"w{i + 1}", t_w + 1.4 + i * 0.4, 99, n=1)
    t_e = S.p("each decision changes")
    for k, node in enumerate(["ver", "end", "q", "work"], 1):
        th = t_e + (k - 1) * 0.35
        deck_hop(S, "i-c", k, dxy, th)
        G.pulse(th, node, "acc")
    t_a = S.p("At every stop,")
    G.focus(t_a, ["end", "ver", "q", "work", "app"], o=0.35)
    fband(S, "i-fb", [(t_w + 0.9, (90, 410, 1740, 172)), (t_a, (400, 616, 1440, 340)), (t_e + 1.4, None)])
    S.write(title("intro"))


# ================================================================ 2 the path: every part on its word
def path():
    S = Stage("path")
    G = sysflow(S)                       # the whole map as a ghost, each part lit on its word
    G.focus(0.05, ["shop"], o=0.14, d=0.3)
    lit = ["shop"]
    t_s = S.p("A shop sends")
    G.pulse(t_s, "shop", "flow")
    t_e = S.p("to your endpoint.", 2)
    lit += ["app", "w1", "end"]
    G.focus(t_e - 0.3, lit, o=0.14)
    G.flow("w1", t_e + 0.1, 99, n=1, label="EVENT")
    t_c = S.p("The endpoint checks")
    lit += ["w2", "ver"]
    G.focus(t_c, lit, o=0.14)
    G.flow("w2", t_c + 0.3, 99, n=1, label="EVENT")
    t_q = S.p("The queue holds it.")
    lit += ["w3", "q"]
    G.focus(t_q, lit, o=0.14)
    G.flow("w3", t_q + 0.3, 99, n=1, label="EVENT")
    t_w = S.p("a worker writes it")
    lit += ["w4", "work"]
    G.focus(t_w, lit, o=0.14)
    G.flow("w4", t_w + 0.3, 99, n=1, label="EVENT")
    t_d = S.p("into your database.")
    G.unfocus(t_d)
    G.flow("w5", t_d + 0.3, 99, n=1, label="EVENT")
    G.badge("db", "STORED", t_d + 1.0, "ok", pos="t")
    fband(S, "p-fb", [(t_s, (130, 450, 190, 220)), (t_e, (470, 450, 190, 220)), (t_c, (730, 450, 190, 220)),
                      (t_q, (990, 450, 190, 250)), (t_w, (1250, 450, 190, 220)), (t_d, (1550, 450, 190, 220)), (S.dur - 0.5, None)])
    S.write(title("path"))


# ================================================================ 3 D1: the signature
def sig():
    S = Stage("sig")
    G = sysflow(S, dy=-170)
    t_e = S.p("Decision one is")
    chapter_card(S, "s-c", "D1", "Signature", t_e)
    G.focus(t_e + 0.2, ["shop", "end", "ver", "app"], o=0.2)
    # the shop signs the body with a shared secret
    t_s = S.p("signs the body")
    anatomy(S, "sg", [("X-Signature: ", None, ""), ("sha256=", "ALGORITHM", "acc"), ("9f3a\u2026c21", "SIGNATURE", "ok")], 960, 600, fs=56)
    anat_in(S, "sg", 3, t_s)
    anat_part(S, "sg", 2, S.p("signs the body", 1) + 0.3, "ok")
    K = Flow(S, "K")
    K.node("sec", 300, 860, "key", "Shared secret", size=100, lpos="r", color="flow")
    K.show(S.p("a shared secret.", 2), "sec")
    G.flow("w1", t_s + 0.4, 99, n=1, label="SIGNED")
    # the endpoint computes the same signature and compares
    t_c = S.p("computes the same signature")
    anat_part(S, "sg", 1, t_c, "acc")
    x1, w1 = chp(S, "s-a", "9f3a\u2026c21", 960 - 250, 830, "flow", t=t_c + 0.3, big=True, center=True)
    chp(S, "s-eq", "=", 960, 836, "ink", t=S.p("compares the two.") + 0.1, center=True)
    chp(S, "s-b", "9f3a\u2026c21", 960 + 250, 830, "acc", t=S.p("compares the two.") + 0.3, big=True, center=True)
    t_cmp = S.p("compares the two.")
    G.pulse(t_cmp, "ver", "ok")
    fill(S, G.nid("ver"), t_cmp + 0.4, tok("ok"))
    G.focus(t_cmp + 0.4, ["end", "ver"], o=0.2, d=0.3)
    # a wrong signature is rejected
    t_r = S.p("A request with a wrong signature")
    out(S, "#s-a, #s-eq, #s-b", t_r - 0.1)
    G.flow("w1", t_r + 0.1, 99, n=1, label="FAKE", cls="bad")
    G.flow("w2", t_r + 0.9, 99, n=1, label="FAKE", cls="bad")
    t_rej = S.p("signature is rejected.", 2)
    G.focus(t_r, ["shop", "end", "ver", "app"], o=0.2, d=0.3)
    unfill(S, G.nid("ver"), t_rej - 0.1)
    G.fail(t_rej + 0.35, "ver")
    G.badge("end", "401", t_rej + 0.2, "bad", pos="t")
    anat_part(S, "sg", 2, t_rej, "bad", label=False)
    # recommended: reject before anything is stored
    t_m = S.p("Recommended: reject it")
    recommend(S, "s-rec", 1320, 830, t_m)
    G.focus(t_m + 0.2, ["end", "ver", "app"], o=0.2)
    chp(S, "s-ns", "NOTHING STORED", 1080, 176, "ghost", t=S.p("anything is stored.", 1), center=True)
    fband(S, "s-fb", [(t_s, (560, 560, 820, 200)), (t_c - 0.1, None), (t_m, (1300, 812, 330, 90)), (S.dur - 0.4, None)])
    S.write(title("sig"))


# ================================================================ 4 D2: the retry plan
def retry():
    S = Stage("retry")
    G = sysflow(S, dy=-170)
    t_e = S.p("Decision two is")
    chapter_card(S, "r-c", "D2", "Retries", t_e)
    G.focus(t_e + 0.2, ["shop", "end", "app"], o=0.2)
    G.pulse(S.p("the retry plan.", 1), "shop", "flow")
    G.pulse(S.p("When your endpoint", 1), "end", "bad")
    t_d = S.p("your endpoint is down,", 2)
    G.fail(t_d, "end")
    fill(S, G.nid("end"), t_d + 0.5, tok("bad"))
    t_a = S.p("the shop tries again.")
    G.flow("w1", t_a, t_a + 2.4, every=0.8, label="RETRY", hit=False)
    # one minute, ten minutes, an hour (log-spaced track)
    X0, X1, Y = 300, 1760, 720
    track(S, "rt", "RETRY SCHEDULE", X0, X1, Y, t_a + 0.2)
    example_tag(S, "r-ex", 690, Y - 70, t_a + 0.5)
    xs = [X0, 560, 960, 1480]
    ticks(S, "rk", xs[:1], Y, t_a + 0.6)
    S.cam(S.p("First after one minute,"), 1.08, -77, -70, dur=0.8)
    for i, (ph, txt) in enumerate([("after one minute,", "1 MIN"), ("then after ten,", "10 MIN"), ("then after an hour.", "1 HOUR")], 1):
        t = S.p(ph, -1)
        el(S, f"rk{i}", "tmk", xs[i], Y)
        appear(S, f"rk{i}", t)
        chp(S, f"r-l{i}", txt, xs[i], Y + 40, "acc", t=t + 0.1, center=True)
        G.flow("w1", t, 99, n=1, label="TRY " + str(i + 1), hit=False)
        if i == 2:     # the gaps grow: the camera steps closer once more
            S.cam(t - 0.1, 1.13, -125, -100, dur=0.6)
    # after the last try, the event is dropped
    t_x = S.p("the event is dropped.", 2)
    S.cam(t_x - 0.6, 1.0, 0, 0, dur=0.6)
    span(S, "r-sp", 1480, X1, Y + 110, t_x - 0.2, 0.8)
    chp(S, "r-dr", "EVENT DROPPED", 1620, Y + 140, "bad", t=t_x + 0.3, big=True, center=True)
    G.badge("shop", "GAVE UP", t_x + 0.4, "bad", pos="t")
    # open question: how many tries
    t_q = S.p("How many tries")
    open_q(S, "r-oq", "HOW MANY TRIES?", 300, Y + 220, t_q + 0.2)
    fband(S, "r-fb", [(t_a + 0.4, (280, 620, 1500, 190)), (t_x - 0.3, (1396, 590, 400, 344)), (t_q, None)])
    S.write(title("retry"))


# ================================================================ 5 D3: duplicates (scan the seen list)
def dupe():
    S = Stage("dupe")
    mini(S, "loc", SYSTEM, (96, 112, 520, 120), lit=["q"], t_in=0.05)
    chapter_card(S, "d-c", "D3", "Duplicates", 0.2)
    D = Flow(S, "D")
    D.node("shop", 250, 560, "browser", "Shop", size=130, color="flow")
    D.node("q", 760, 560, "queue", "Queue", size=150, color="acc")
    D.wire("a", "shop", "q", oa=-28, ob=-28)
    D.wire("b", "shop", "q", oa=28, ob=28)
    D.build(0.1, ["shop", "q"], step=0.2)
    t_t = S.p("the same event twice.", 3)
    D.show(t_t - 1.2, "a", "b", stagger=0.15)
    D.flow("a", t_t - 0.9, 99, n=1, label="ID 42")
    D.flow("b", t_t - 0.4, 99, n=1, label="ID 42", cls="bad")
    D.badge("q", "TWICE", t_t + 0.3, "bad", pos="t")
    chp(S, "d-tw", "SAME ID \u00b7 TWICE", 505, 680, "bad", t=S.p("the same event", 1), big=True, center=True)
    fill(S, D.nid("q"), t_t + 0.1, tok("bad"))
    out(S, "#d-tw", S.p("keeps a list") - 0.1)
    # the queue keeps a list of every event ID it has seen
    t_l = S.p("keeps a list")
    xs = pages(S, "pl", 2, 1060, 330, gap=340, foot="SEEN IDS")
    for p in range(2):
        appear(S, f"pl-p{p}", t_l + 0.2 + p * 0.2, "up")
    D.wire("lst", None, None, pts=[(850, 560), (1046, 560)], dash=True)
    t_sn = S.p("it has seen.", 1)
    D.show(t_sn, "lst")
    D.pulse(t_sn + 0.2, "q", "acc")
    # it reads the list until it finds a match
    t_r = S.p("It reads the list")
    t_hit = scan(S, "pl", "pl-lens", xs, 330, 8, t_r + 0.3, S.p("finds a match.", 1), stop=(1, 3))
    chp(S, "d-m", "ID 42 \u00b7 MATCH", 1400, 726, "ok", t=t_hit + 0.1)
    # known -> dropped, new -> moves on
    t_k = S.p("A known I D")
    x, w = chp(S, "d-k", "ID 42", 240, 800, "ghost", t=t_k, big=True, occl=True)
    strike_bar(S, "d-ks", x, 800, w, t_k + 0.5, big=True)
    chp(S, "d-kd", "DROPPED", 420, 808, "bad", t=t_k + 0.6)
    t_n = S.p("a new one moves on.", 1)
    chp(S, "d-n", "ID 43", 240, 900, "ok", t=t_n, big=True)
    chp(S, "d-nm", "MOVES ON", 420, 908, "ok", t=t_n + 0.2)
    fill(S, D.nid("q"), t_n + 0.4, tok("ok"))
    fband(S, "d-fb", [(t_l + 0.2, (1040, 314, 700, 414)), (t_k + 0.5, (220, 780, 520, 200)), (S.dur - 0.4, None)])
    S.write(title("dupe"))


# ================================================================ 6 D4: load vs capacity
def load():
    S = Stage("load")
    G = sysflow(S, dy=-170)
    t_e = S.p("Decision four is")
    chapter_card(S, "l-c", "D4", "Load", t_e)
    G.focus(t_e + 0.2, ["q", "work", "app"], o=0.2)
    t_s = S.p("three hundred events")
    t_w = S.p("Your worker handles")
    xl, total = capacity(S, "cap", [("300 events / min", 300, "flow", t_s)], (200, "WORKER MAX 200", t_w + 0.3),
                         x0=300, y=700, unit=4.0, t_frame=t_s - 0.3)
    G.flow("w4", t_s, t_w + 3, every=0.5, label="EVT")
    G.pulse(t_w + 0.3, "work", "bad")
    # without a queue, a hundred are lost
    t_l = S.p("a hundred events are lost.", 1)
    chp(S, "l-lost", "100 LOST", xl + 200, 800, "bad", t=t_l, big=True, center=True)
    G.fail(t_l + 0.2, "q", shake_it=False)
    # with a queue, they wait their turn
    t_q = S.p("With a queue,")
    out(S, "#l-lost, #cap-ov", t_q)
    G.ok(t_q + 0.2, "q")
    fill(S, G.nid("q"), t_q + 0.3, tok("accent-1"))
    chp(S, "l-wait", "100 WAIT THEIR TURN", xl + 200, 800, "flow", t=S.p("wait their turn", 1), big=True, center=True)
    G.flow("w4", S.p("wait their turn"), S.dur, every=0.7, label="EVT")
    t_lt = S.p("arrive a little later.")
    G.unfocus(t_lt - 0.1, d=0.3)
    fill(S, G.nid("db"), t_lt + 0.2, tok("ok"))
    G.pulse(t_lt, "db", "ok")
    G.badge("db", "LATER", t_lt + 0.3, "flow", pos="t")
    # example numbers, not a measurement
    example_tag(S, "l-ex", 300, 860, S.p("an example,", 1))
    G.focus(S.p("These numbers are"), [], o=0.25, d=0.3)
    draft_stamp(S, "l-nm", 1220, 900, S.p("not a measurement.", 2))
    fband(S, "l-fb", [(t_s, (268, 668, 1300, 132)), (t_w + 0.3, (xl - 150, 590, 300, 230)), (t_q, None)])
    S.write(title("load"))


# ================================================================ 7 close: four decisions, one path
def close():
    S = Stage("close")
    S.tail_ok = "the board + the system stay on screen through the terminal hold"
    groups = [("Getting in", [("D1", "Signature"), ("D2", "Retries")]), ("Getting through", [("D3", "Duplicates"), ("D4", "Load")])]
    Y0 = 230
    xs = board(S, "cb", groups, Y0)
    board_in(S, "cb", groups, 0.3)
    S.J(f'tl.fromTo("#cb-g0, #cb-g1", {{ y: 0 }}, {{ y: -10, duration: 0.2, yoyo: true, repeat: 1, immediateRender: false }}, {S.p("one path.", 1)});')
    Z = mini(S, "zm", SYSTEM, (260, 640, 1400, 210), t_in=0.6)
    lits = [["ver"], ["shop", "end"], ["q"], ["q", "work"]]
    words = ["Sign it,", "retry it,", "deduplicate it,", "and queue it."]
    lit = set()
    for k, ph in enumerate(words):
        t = S.p(ph)
        S.J(f'tl.fromTo("#cb-c{k + 1}", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }}, {t});')
        board_lit(S, "cb", 2, 0 if k < 2 else 1, t)
        gone, new = lit - set(lits[k]), set(lits[k]) - lit     # never off+on the same part at one time
        if gone:
            Z.off(t, *sorted(gone))
        if new:
            Z.on(t, *sorted(new))
        lit = set(lits[k])
    t_r = S.p("Get those four right,")
    Z.on(S.p("lands in your database", 1), "db")
    board_lit(S, "cb", 2, None, t_r)
    Z.off(t_r, *sorted(lit))
    for i in range(5):
        Z.flow(f"w{i + 1}", t_r + 0.2 + i * 0.2, t_r + 0.8 + i * 0.2, n=1)
    chp(S, "c-q", "EVERY EVENT \u00b7 ONCE", 960, 900, "ink", t=S.p("in your database once.", 3), big=True, center=True)
    fband(S, "c-fb", [(S.p("Sign it,"), board_rect(groups, 0, Y0, xs)), (S.p("deduplicate it,"), board_rect(groups, 1, Y0, xs)), (t_r, None)])
    S.write(title("close"))


ALL = [intro, path, sig, retry, dupe, load, close]
