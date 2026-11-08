"""Timing for flow-explainer: transcript words -> composition seconds.

Single source of truth for scene cuts and beat anchors. Every beat time in
build/scenes.py comes from a PHRASE (S.p("phrase")), so a re-TTS keeps every
cut and every beat on its word.

Two modes:
  * transcript.json present (a real video): words from `npx hyperframes
    transcribe` / scripts/tts.py ({text|word, start, end}), with a flat
    LAG pulled off every start (eleven_v4 word starts trail the audio ~0.15 s;
    set VIDEO["lag"] to re-measure it, 0 for a local Kokoro voice).
  * no transcript.json (the bare template): words are SYNTHESISED from
    script.txt at a fixed speaking rate. Nothing is spoken; the builder emits
    no narration <audio> in this mode.

Composition clock = narration clock + one optional pre-rendered midroll insert
(VIDEO["midroll"]): narration pauses while the midroll plays its own audio.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TRANSCRIPT = os.path.join(ROOT, "transcript.json")
SCRIPT = os.path.join(ROOT, "script.txt")

LEAD = 0.25          # a scene cuts in this long before its first word
SYNTH_RATE = 0.30    # synthetic seconds per word (+0.012 s per character)
SYNTH_PAUSE = 0.32   # synthetic pause after . ? !


def _load_words():
    if os.path.exists(TRANSCRIPT):
        raw = json.load(open(TRANSCRIPT, encoding="utf-8"))
        if isinstance(raw, dict):
            raw = raw.get("words") or raw.get("segments") or []
        words = [{"word": w.get("word", w.get("text", "")), "start": float(w["start"]), "end": float(w["end"])} for w in raw]
        return words, False
    text = open(SCRIPT, encoding="utf-8").read()
    words, t = [], 0.4
    for tok in text.split():
        d = SYNTH_RATE + 0.012 * len(tok)
        words.append({"word": tok, "start": round(t, 3), "end": round(t + d - 0.04, 3)})
        t += d + (SYNTH_PAUSE if tok[-1] in ".?!" else 0.0)
    return words, True


WORDS, SYNTHETIC = _load_words()
LAG = 0.0 if SYNTHETIC else 0.15     # VIDEO["lag"] overrides it (configure)


def _n(s):
    # unicode-aware (German / French narration): keep letters + digits of any script, drop the rest
    return re.sub(r"[\W_]", "", s.lower())


_TOK = [_n(w["word"]) for w in WORDS]


def _find(phrase):
    """(index of first word, word count) of a phrase that occurs exactly once."""
    want = [_n(p) for p in phrase.split() if _n(p)]
    hits = [i for i in range(len(_TOK) - len(want) + 1) if _TOK[i:i + len(want)] == want]
    if len(hits) != 1:
        raise SystemExit(f"timing: phrase {phrase!r} has {len(hits)} matches in the transcript (need exactly 1)")
    return hits[0], len(want)


# ---------------------------------------------------------------- configured by build.py
VIDEO = None
ORDER, FIRST, INSERT = [], {}, None


def raw_start(i):
    return max(0.0, WORDS[i]["start"] - LAG)


def configure(video):
    """Bind the scene table (scenes.VIDEO) to the transcript."""
    global VIDEO, ORDER, FIRST, INSERT, LAG
    VIDEO = video
    if not SYNTHETIC and video.get("lag") is not None:
        LAG = float(video["lag"])
    ORDER = [s["id"] for s in video["scenes"]]
    FIRST = {}
    for s in video["scenes"]:
        FIRST[s["id"]] = 0 if not s.get("first") else _find(s["first"])[0]
    m = video.get("midroll")
    INSERT = None
    if m:
        i = _find(m["before"])[0]
        INSERT = {"raw": round(raw_start(i) - LEAD, 3), "dur": float(m["dur"]), "word": i}


def comp(raw):
    """raw narration seconds -> composition seconds"""
    if INSERT and raw >= INSERT["raw"]:
        return round(raw + INSERT["dur"], 3)
    return round(raw, 3)


def wt(i, end=False):
    """composition time of word i (start, lag-corrected; or end)"""
    return comp(WORDS[i]["end"] if end else raw_start(i))


def insert_start():
    return INSERT["raw"] if INSERT else None


def insert_end():
    return round(INSERT["raw"] + INSERT["dur"], 3) if INSERT else None


def scene_cut(sid):
    i = FIRST[sid]
    if i == 0:
        return 0.0
    if INSERT and i == INSERT["word"]:
        return insert_end()
    # never mount the next scene before the previous scene's last word has ended (motion-breathing.md)
    return round(max(wt(i) - LEAD, min(comp(WORDS[i - 1]["end"]) + 0.05, comp(WORDS[i]["start"]) - 0.01)), 3)


def total():
    return round(comp(WORDS[-1]["end"]) + float(VIDEO.get("terminal_hold", 3.0)), 3)


def scene_end(sid):
    k = ORDER.index(sid)
    if k + 1 < len(ORDER):
        nxt = ORDER[k + 1]
        if INSERT and FIRST[nxt] == INSERT["word"]:
            return insert_start()
        return scene_cut(nxt)
    return total()


def scene_dur(sid):
    return round(scene_end(sid) - scene_cut(sid), 3)


def phrase_t(phrase, k=0, end=False):
    """composition time of word k (k<0 counts from the end) of a unique phrase"""
    i, n = _find(phrase)
    k = n + k if k < 0 else k
    return wt(i + k, end)


if __name__ == "__main__":
    import scenes  # noqa: E402  (prints the scene table of the current scenes.py)
    configure(scenes.VIDEO)
    print("mode:", "SYNTHETIC (no transcript.json, no narration audio)" if SYNTHETIC else "transcript.json")
    for s in ORDER:
        print(f"{s:10s} cut={scene_cut(s):8.2f} dur={scene_dur(s):7.2f} first={WORDS[FIRST[s]]['word']!r}")
    if INSERT:
        print("midroll insert", insert_start(), "->", insert_end())
    print("total", total())
