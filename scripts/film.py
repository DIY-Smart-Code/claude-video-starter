#!/usr/bin/env python3
"""Cinematic template pipeline: score -> cut -> mix -> finish -> sheet.

Usage (from the repo root):
    python scripts/film.py all    videos/<slug>     # cut + mix + finish + contact sheet
    python scripts/film.py cut    videos/<slug>     # lint, then render the picture: build/cut.mp4 (24 fps, motion blur)
    python scripts/film.py mix    videos/<slug>     # music + voice + hits -> build/mix.wav, ducked and loudness-normalised
    python scripts/film.py finish videos/<slug>     # write build/finish.html (grade, grain, bars, mix) and render out/<slug>.mp4
    python scripts/film.py sheet  videos/<slug>     # contact sheet of the finished film
    python scripts/film.py score  videos/<slug>     # generate missing music / hits with ElevenLabs (film.json "score")
    python scripts/film.py board  videos/<slug>     # storyboard.html from film.json "shots" (with stills once the cut exists)
    python scripts/film.py stills videos/<slug> 1.5 7 12.2   # full-size frames from the cut, for checking a moment

Everything the finish needs is in videos/<slug>/film.json (look, aspect, audio cues, score prompts).
The cut is index.html. Needs ffmpeg/ffprobe and Node (npx). Python 3.8+, standard library only.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HF = "hyperframes@0.9.29"          # motion blur and the grading shader need 0.9.x
NPX = "npx.cmd" if os.name == "nt" else "npx"
REPO = Path(__file__).resolve().parent.parent

# Named looks: HyperFrames colour-grading payloads (data-color-grading) for the finish.
# Values are deliberately restrained; the cut's lighting does the heavy lifting.
LOOKS = {
    # deep blue-black shadows, warm highlights, soft bloom, fine grain: night, tech, premium
    "night": {"adjust": {"exposure": 0.06, "contrast": 0.08, "blacks": 0.03, "saturation": -0.03},
              "wheels": {"shadows": {"hue": 222, "amount": 0.10, "level": 0}, "highlights": {"hue": 36, "amount": 0.08, "level": 0.02}},
              "details": {"vignette": 0.3, "vignetteFeather": 0.8, "grain": 0.28, "grainSize": 0.3},
              "effects": {"bloom": 0.42, "bloomRadius": 24, "chromaticAberration": 0.05}},
    # the blockbuster split: teal shadows, orange highlights, more contrast
    "teal-orange": {"adjust": {"contrast": 0.18, "blacks": 0.01, "vibrance": 0.08},
                    "wheels": {"shadows": {"hue": 190, "amount": 0.16, "level": 0}, "highlights": {"hue": 30, "amount": 0.14, "level": 0.02}},
                    "details": {"vignette": 0.3, "vignetteFeather": 0.75, "grain": 0.25, "grainSize": 0.3},
                    "effects": {"bloom": 0.5, "bloomRadius": 20, "chromaticAberration": 0.05}},
    # warm, lifted blacks, heavier grain: human, nostalgic, lifestyle
    "warm-film": {"adjust": {"contrast": 0.06, "blacks": 0.05, "temperature": 0.10, "saturation": -0.06},
                  "wheels": {"shadows": {"hue": 28, "amount": 0.06, "level": 0.01}, "highlights": {"hue": 42, "amount": 0.08, "level": 0}},
                  "details": {"vignette": 0.36, "vignetteFeather": 0.8, "grain": 0.42, "grainSize": 0.4},
                  "effects": {"bloom": 0.7, "bloomRadius": 28, "chromaticAberration": 0.04}},
    # brand colour stays true; only contrast, bloom and a whisper of grain: product films
    "clean": {"adjust": {"contrast": 0.08},
              "details": {"vignette": 0.22, "vignetteFeather": 0.85, "grain": 0.14, "grainSize": 0.25},
              "effects": {"bloom": 0.45, "bloomRadius": 18}},
    # black and white, hard: drama, statements
    "noir": {"adjust": {"contrast": 0.3, "saturation": -1, "blacks": -0.02},
             "details": {"vignette": 0.45, "vignetteFeather": 0.7, "grain": 0.4, "grainSize": 0.35},
             "effects": {"bloom": 0.4, "bloomRadius": 18}},
}


def die(msg: str) -> None:
    sys.exit(f"film.py: {msg}")


def run(cmd, **kw):
    print("$", " ".join(str(c) for c in cmd), flush=True)
    r = subprocess.run([str(c) for c in cmd], **kw)
    if r.returncode != 0:
        die(f"command failed ({r.returncode}): {cmd[0]} {cmd[1] if len(cmd) > 1 else ''}")
    return r


def hf(*args, cwd=None):
    return run([NPX, "--yes", HF, *args], cwd=cwd)


def load(vdir: Path) -> dict:
    f = vdir / "film.json"
    if not f.exists():
        die(f"{f} not found (copy one from templates/cinematic/film.json)")
    film = json.loads(f.read_text(encoding="utf-8"))
    html = (vdir / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<[^>]*data-composition-id="main"[^>]*>', html)
    if not m:
        die("index.html has no data-composition-id=\"main\" root")
    tag = m.group(0) if m else ""

    def attr(k: str, default: str) -> str:
        hit = re.search(rf'{k}="([^"]+)"', tag)
        return hit.group(1) if hit else default

    film.setdefault("duration", float(attr("data-duration", "0")))
    film.setdefault("width", int(attr("data-width", "1920")))
    film.setdefault("height", int(attr("data-height", "1080")))
    film.setdefault("fps", int(attr("data-fps", "24")))
    film.setdefault("aspect", attr("data-aspect", "2.39"))
    return film


def bar_px(film: dict) -> int:
    a = str(film.get("aspect", "2.39"))
    if ":" in a:
        return 0
    return max(0, round((film["height"] - film["width"] / float(a)) / 2))


def probe_duration(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


# ---------------------------------------------------------------- cut
def cmd_cut(vdir: Path, film: dict) -> None:
    hf("lint", str(vdir))
    (vdir / "build").mkdir(exist_ok=True)
    out = vdir / "build" / "cut.mp4"
    # Mezzanine quality: the finish re-encodes once, so keep this one nearly lossless.
    hf("render", str(vdir), "-o", str(out), "--fps", str(film["fps"]), "--crf", "10")
    print(f"cut: {out} ({probe_duration(out):.2f}s)")


# ---------------------------------------------------------------- mix
def env_expr(points):
    """Piecewise-linear gain envelope in dB -> ffmpeg volume expression (linear gain)."""
    pts = sorted(points)
    expr = f"{pts[-1][1]}"
    for (t0, d0), (t1, d1) in reversed(list(zip(pts, pts[1:]))):
        seg = f"{d0}+({d1}-{d0})*(t-{t0})/({t1}-{t0})" if t1 > t0 else f"{d1}"
        expr = f"if(lt(t,{t1}),{seg},{expr})"
    expr = f"if(lt(t,{pts[0][0]}),{pts[0][1]},{expr})"
    return f"pow(10,({expr})/20)"


def cmd_mix(vdir: Path, film: dict) -> Path:
    a = film.get("audio", {})
    D = film["duration"]
    build = vdir / "build"
    build.mkdir(exist_ok=True)
    inputs, chains, labels = [], [], []
    fmt = "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"

    def add_input(src):
        p = vdir / src
        if not p.exists():
            die(f"audio file missing: {p} (run: python scripts/film.py score {vdir})")
        inputs.extend(["-i", str(p)])
        return len(inputs) // 2 - 1

    voice = a.get("voice")
    music = a.get("music")
    mlabel = ""
    if music:
        k = add_input(music["src"])
        ms = int(round(music.get("start", 0) * 1000))
        c = f"[{k}:a]{fmt},atrim=start={music.get('offset', 0)},asetpts=PTS-STARTPTS,adelay={ms}|{ms},volume={music.get('volume', 0.8)}"
        if music.get("envelope"):
            c += f",volume='{env_expr(music['envelope'])}':eval=frame"
        fo = music.get("fadeOut", 1.5)
        c += f",afade=t=in:st=0:d={music.get('fadeIn', 0.01)},afade=t=out:st={max(0, D - fo)}:d={fo}[m0]"
        chains.append(c)
        mlabel = "m0"
    if voice:
        # Either the whole file from `start`, or `segments`: [[at, from, to], ...] places each spoken
        # line at its own time in the film (cut the narration on the transcript's word times).
        segs = voice.get("segments") or [[voice.get("start", 0), 0, None]]
        parts = []
        for j, (at, t0, t1) in enumerate(segs):
            k = add_input(voice["src"])
            ms = int(round(at * 1000))
            trim = f"atrim=start={t0}" + (f":end={t1}" if t1 is not None else "")
            chains.append(f"[{k}:a]{fmt},{trim},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.02,adelay={ms}|{ms}[vs{j}]")
            parts.append(f"[vs{j}]")
        vin = "".join(parts)
        chains.append(f"{vin}amix=inputs={len(parts)}:normalize=0,volume={voice.get('volume', 1.0)},asplit=2[v][vsc]" if len(parts) > 1
                      else f"{vin}volume={voice.get('volume', 1.0)},asplit=2[v][vsc]")
        labels.append("v")
        if music and a.get("duck", 0.35):
            # Music ducks under the voice: sidechain compression keyed by the narration.
            chains.append(f"[{mlabel}][vsc]sidechaincompress=threshold=0.02:ratio=8:attack=25:release=450:makeup=1[m1]")
            mlabel = "m1"
        else:
            chains.append("[vsc]anullsink")
    if music:
        labels.insert(0, mlabel)
    for i, cue in enumerate(a.get("sfx", [])):
        k = add_input(cue["src"])
        ms = int(round(cue["at"] * 1000))
        c = f"[{k}:a]{fmt},volume={cue.get('volume', 1.0)}"
        if cue.get("dur"):
            c += f",atrim=0:{cue['dur']},afade=t=out:st={max(0, cue['dur'] - 0.15)}:d=0.15"
        chains.append(c + f",adelay={ms}|{ms}[s{i}]")
        labels.append(f"s{i}")
    if not labels:
        die("film.json audio has no music, voice or sfx")
    chains.append("".join(f"[{l}]" for l in labels) +
                  f"amix=inputs={len(labels)}:normalize=0:duration=longest,apad=whole_dur={D},atrim=0:{D}[mix]")
    script = build / "mix.filter"
    script.write_text(";\n".join(chains), encoding="utf-8")
    pre = build / "premix.wav"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex_script", str(script), "-map", "[mix]", "-ar", "48000", str(pre)])
    # Two-pass loudness normalisation to the target (default -14 LUFS, -1 dBTP: web and social).
    target = a.get("loudness", -14)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(pre), "-af", f"loudnorm=I={target}:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):])
    out = build / "mix.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(pre), "-af",
         f"loudnorm=I={target}:TP=-1.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
         f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", "48000", str(out)])
    print(f"mix: {out} (input {m['input_i']} LUFS -> {target} LUFS)")
    return out


# ---------------------------------------------------------------- finish
def grade_payload(film: dict) -> dict:
    g = film.get("grade")
    if isinstance(g, dict):
        return g
    look = film.get("look", "night")
    if look not in LOOKS:
        die(f"unknown look '{look}'; pick one of {', '.join(LOOKS)} or give an explicit \"grade\" payload")
    return LOOKS[look]


def write_finish(vdir: Path, film: dict) -> Path:
    W, H, D, fps = film["width"], film["height"], film["duration"], film["fps"]
    bar = bar_px(film)
    grade = json.dumps(grade_payload(film), separators=(",", ":"))
    has_mix = (vdir / "build" / "mix.wav").exists()
    bars = "" if bar == 0 else (
        f'      <div class="bar clip" style="top:0" data-start="0" data-duration="{D}" data-track-index="1"></div>\n'
        f'      <div class="bar clip" style="bottom:0" data-start="0" data-duration="{D}" data-track-index="2"></div>\n')
    audio = (f'      <audio id="mix" class="clip" src="mix.wav" data-start="0" data-duration="{D}" data-track-index="5"></audio>\n'
             if has_mix else "")
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <!-- THE FINISH. Generated by scripts/film.py from film.json: do not edit by hand.
         The cut (build/cut.mp4) is graded by the HyperFrames colour shader, then letterboxed and scored. -->
    <script src="../assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #plate {{ position: absolute; inset: 0; width: {W}px; height: {H}px; }}
      .bar {{ position: absolute; left: 0; width: {W}px; height: {bar}px; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="finish" data-start="0" data-duration="{D}" data-width="{W}" data-height="{H}" data-fps="{fps}">
      <video id="plate" class="clip" src="cut.mp4" muted playsinline data-start="0" data-duration="{D}" data-track-index="0"
        data-color-grading='{grade}'></video>
{bars}{audio}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, {D});
      window.__timelines["finish"] = tl;
    </script>
  </body>
</html>
"""
    old = vdir / "finish.html"            # older layout: a second root composition breaks lint
    if old.exists():
        old.unlink()
    f = vdir / "build" / "finish.html"
    f.write_text(html, encoding="utf-8")
    return f


def cmd_finish(vdir: Path, film: dict) -> Path:
    if not (vdir / "build" / "cut.mp4").exists():
        die("build/cut.mp4 missing: run the cut first")
    write_finish(vdir, film)
    slug = vdir.name
    (vdir / "out").mkdir(exist_ok=True)
    out = vdir / "out" / f"{slug}.mp4"
    hf("render", str(vdir), "-c", "build/finish.html", "-o", str(out), "--fps", str(film["fps"]), "--quality", "delivery")
    print(f"finish: {out} ({probe_duration(out):.2f}s)")
    return out


def cmd_sheet(vdir: Path, film: dict) -> None:
    out = vdir / "out" / f"{vdir.name}.mp4"
    run([sys.executable, str(REPO / "scripts" / "contact-sheet.py"), str(out)])


def cmd_board(vdir: Path, film: dict) -> None:
    """storyboard.html from film.json "shots": one card per shot (what, light, camera, type, sound, out).
    Before the cut exists the cards are text only; after `cut` each card gets a real still."""
    import html as H
    shots = film.get("shots")
    if not shots:
        die('film.json has no "shots" list (see templates/cinematic/film.json)')
    cut = vdir / "build" / "cut.mp4"
    bdir = vdir / "build" / "board"
    if cut.exists():
        bdir.mkdir(parents=True, exist_ok=True)
    bar = bar_px(film)
    cards = []
    for sh in shots:
        t0, t1 = float(sh["start"]), float(sh["end"])
        img = ""
        if cut.exists():
            key = float(sh.get("key", (t0 + t1) / 2))
            p = bdir / f"{sh['id']}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{key:.3f}", "-i", str(cut), "-frames:v", "1", "-vf", "scale=640:-1", "-q:v", "3", str(p)])
            img = f'<img src="build/board/{sh["id"]}.jpg" alt="">'
        else:
            img = f'<div class="ph">{H.escape(sh.get("shot", ""))}</div>'
        rows = "".join(f"<dt>{k}</dt><dd>{H.escape(str(sh[k]))}</dd>" for k in ("shot", "light", "camera", "type", "sound", "out") if sh.get(k))
        cards.append(f'<article><div class="frame">{img}</div><h2>{H.escape(sh["id"])} <span>{t0:.2f}–{t1:.2f} s · {t1 - t0:.1f} s</span></h2><dl>{rows}</dl></article>')
    title = H.escape(film.get("title", vdir.name))
    page = f"""<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>{title}: storyboard</title><style>
body{{margin:0;padding:32px;background:#0b0b0e;color:#e8e6e1;font:15px/1.45 system-ui,sans-serif}}
h1{{font-weight:600;margin:0 0 4px}} p.meta{{color:#8d8a83;margin:0 0 24px}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:20px}}
article{{background:#15151a;border:1px solid #26262e;border-radius:10px;overflow:hidden}}
.frame{{aspect-ratio:16/9;background:#000;position:relative}} .frame img{{width:100%;display:block}}
.frame::before,.frame::after{{content:"";position:absolute;left:0;right:0;height:{bar / 10.8:.2f}%;background:#000;z-index:1}}
.frame::before{{top:0}} .frame::after{{bottom:0}}
.ph{{position:absolute;inset:0;display:grid;place-items:center;padding:24px;text-align:center;color:#6f6c66;font-style:italic}}
h2{{font-size:16px;margin:12px 14px 6px}} h2 span{{color:#8d8a83;font-weight:400}}
dl{{display:grid;grid-template-columns:70px 1fr;gap:3px 10px;margin:0 14px 14px}} dt{{color:#8d8a83}} dd{{margin:0}}
</style></head><body><h1>{title}</h1><p class="meta">{len(shots)} shots · {film["duration"]:.1f} s · {film["fps"]} fps · {film.get("aspect")} · look: {film.get("look", "custom")}</p>
<main>{"".join(cards)}</main></body></html>"""
    out = vdir / "storyboard.html"
    out.write_text(page, encoding="utf-8")
    print(f"board: {out} ({len(shots)} shots{', with stills' if cut.exists() else ', text only: run cut for stills'})")


def cmd_stills(vdir: Path, film: dict, times) -> None:
    src = vdir / "build" / "cut.mp4"
    if not src.exists():
        src = vdir / "out" / f"{vdir.name}.mp4"
    d = vdir / "build" / "stills"
    d.mkdir(parents=True, exist_ok=True)
    for t in times:
        p = d / f"t{float(t):06.2f}.png"
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(src), "-frames:v", "1", str(p)])
        print(p)


# ---------------------------------------------------------------- score (ElevenLabs)
def el_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    env = REPO / ".env"
    if not key and env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("ELEVENLABS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        die("ELEVENLABS_API_KEY not set (.env); or drop your own music and hits into assets/score/")
    return key


def cmd_score(vdir: Path, film: dict) -> None:
    sc = film.get("score", {})
    key = el_key()
    jobs = []
    m = sc.get("music")
    if m and not (vdir / m["out"]).exists():
        short = [s["name"] for s in m["sections"] if int(s["ms"]) < 3000]
        if short:
            die(f"music sections must be at least 3000 ms (ElevenLabs): {', '.join(short)}")
        plan = {"positive_global_styles": m.get("styles", []), "negative_global_styles": m.get("negative", ["vocals", "singing"]),
                "sections": [{"section_name": s["name"], "positive_local_styles": s.get("styles", []), "negative_local_styles": s.get("negative", []),
                              "duration_ms": int(s["ms"]), "lines": []} for s in m["sections"]]}
        jobs.append(("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192", {"composition_plan": plan}, vdir / m["out"]))
    for name, spec in sc.get("sfx", {}).items():
        out = vdir / spec.get("out", f"assets/score/sfx/{name}.mp3")
        if not out.exists():
            jobs.append(("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192",
                         {"text": spec["prompt"], "duration_seconds": spec.get("seconds", 1.5), "prompt_influence": spec.get("influence", 0.6)}, out))
    if not jobs:
        print("score: everything already exists (delete a file to regenerate it)")
        return

    def post(job):
        url, payload, out = job
        out.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"xi-api-key": key, "Content-Type": "application/json"}, method="POST")
        try:
            data = urllib.request.urlopen(req, timeout=600).read()
            out.write_bytes(data)
            return f"ok   {out.relative_to(vdir)} ({len(data) // 1024} KB)"
        except urllib.error.HTTPError as e:
            return f"FAIL {out.relative_to(vdir)}: {e.code} {e.read()[:300]!r}"

    with ThreadPoolExecutor(5) as ex:
        for line in ex.map(post, jobs):
            print("score:", line)


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, vdir = sys.argv[1], Path(sys.argv[2]).resolve()
    if not vdir.is_dir():
        die(f"{vdir} is not a folder")
    film = load(vdir)
    if cmd == "cut":
        cmd_cut(vdir, film)
    elif cmd == "mix":
        cmd_mix(vdir, film)
    elif cmd == "finish":
        cmd_finish(vdir, film)
    elif cmd == "sheet":
        cmd_sheet(vdir, film)
    elif cmd == "score":
        cmd_score(vdir, film)
    elif cmd == "board":
        cmd_board(vdir, film)
    elif cmd == "stills":
        cmd_stills(vdir, film, sys.argv[3:])
    elif cmd == "all":
        cmd_cut(vdir, film)
        if film.get("audio"):
            cmd_mix(vdir, film)
        cmd_finish(vdir, film)
        cmd_sheet(vdir, film)
        if film.get("shots"):
            cmd_board(vdir, film)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
