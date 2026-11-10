/* cine.js: camera, lens, light, type and edit moves for the cinematic template.
   Every function adds finite tweens to one paused GSAP timeline. Nothing here reads the clock,
   calls Math.random or runs a loop, so frame N always renders the same picture.

   const tl = cine.film("main", 30);     // paused timeline, registered on window.__timelines
   cine.push(tl, "#s1 .cam", 0, 4);      // slow dolly in
   cine.reveal(tl, "#s1 .kicker", "track", 0.6);
   cine.end(tl, 30);                     // pins the timeline to the film length
*/
(function () {
  const g = window.gsap;
  const $ = (q, root) => (typeof q === "string" ? (root || document).querySelector(q) : q);
  const $$ = (q, root) => (typeof q === "string" ? Array.from((root || document).querySelectorAll(q))
    : Array.isArray(q) ? q.flatMap((x) => $$(x, root)) : q ? [q] : []);   // arrays may mix selectors and elements
  const FRAME = 1 / 24;

  /* Deterministic noise: mulberry32 seeded per call site. */
  function rng(seed) {
    let a = (seed >>> 0) || 1;
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const cine = { rng, FRAME };

  /* ---------- Film ---------- */
  cine.film = function (id, duration) {
    window.__timelines = window.__timelines || {};
    const tl = g.timeline({ paused: true });
    window.__timelines[id] = tl;
    cine._duration = duration;
    const root = Array.from(document.querySelectorAll("[data-composition-id]")).find((n) => n.dataset.compositionId === id);
    // Aspect band from data-aspect on #root ("2.39", "2", "1.85", "16:9", "9:16").
    if (root) {
      const H = Number(root.dataset.height) || 1080, W = Number(root.dataset.width) || 1920;
      const a = String(root.dataset.aspect || "2.39");
      let bar = 0;
      if (!a.includes(":")) bar = Math.max(0, Math.round((H - W / Number(a)) / 2));
      const s = document.documentElement.style;
      s.setProperty("--W", W + "px"); s.setProperty("--H", H + "px"); s.setProperty("--bar", bar + "px");
    }
    return tl;
  };
  cine.end = function (tl, duration) { tl.set({}, {}, duration ?? cine._duration); return tl; };

  /* ---------- Camera (2D: scale / x / y / rotation on .cam) ----------
     Real camera moves are slow and constant. Default ease is a gentle inOut; use "none"
     for a locked-off dolly that runs through the cut. */
  cine.move = function (tl, el, at, dur, to, opts = {}) {
    const from = opts.from;
    const vars = Object.assign({ duration: dur, ease: opts.ease || "sine.inOut" }, to);
    if (from) tl.fromTo($(el), from, vars, at); else tl.to($(el), vars, at);
    return tl;
  };
  /* Dolly in: scale up slowly over the whole shot. amount 0.04 subtle, 0.08 default, 0.15 strong. */
  cine.push = (tl, el, at, dur, amount = 0.08, opts = {}) =>
    cine.move(tl, el, at, dur, { scale: 1 + amount, x: opts.x || 0, y: opts.y || 0 }, { from: { scale: 1, x: 0, y: 0 }, ease: opts.ease || "none" });
  /* Pull out: the reverse; good for reveals ("it was a phone all along"). */
  cine.pull = (tl, el, at, dur, amount = 0.08, opts = {}) =>
    cine.move(tl, el, at, dur, { scale: 1, x: 0, y: 0 }, { from: { scale: 1 + amount, x: opts.x || 0, y: opts.y || 0 }, ease: opts.ease || "power2.out" });
  /* Truck: lateral slide; pair with depth layers moving at different rates for parallax. */
  cine.truck = (tl, el, at, dur, dx = -120, opts = {}) =>
    cine.move(tl, el, at, dur, { x: dx }, { from: { x: opts.fromX || 0 }, ease: opts.ease || "none" });
  /* Parallax: each [data-depth] child of `scope` trucks by dx * depth (depth 0 = locked, 1 = camera speed). */
  cine.parallax = function (tl, scope, at, dur, dx = -200, dy = 0, ease = "none") {
    $$("[data-depth]", $(scope)).forEach((el) => {
      const d = Number(el.dataset.depth);
      tl.fromTo(el, { x: 0, y: 0 }, { x: dx * d, y: dy * d, duration: dur, ease }, at);
    });
    return tl;
  };
  /* Crash zoom: a violent push in the last frames of a shot (motion blur does the rest). */
  cine.crash = (tl, el, at, dur = 0.22, amount = 0.6) =>
    tl.to($(el), { scale: 1 + amount, duration: dur, ease: "power4.in" }, at);

  /* ---------- 3D (slow moves only: 3D layers get no motion blur) ---------- */
  cine.orbit = function (tl, world, at, dur, from, to, ease = "sine.inOut") {
    tl.fromTo($(world), Object.assign({ rotationY: 0, rotationX: 0, z: 0, x: 0, y: 0 }, from), Object.assign({ duration: dur, ease }, to), at);
    return tl;
  };
  /* Keep .plane layers at their authored size whatever their depth (--z). */
  cine.depth = function (stage) {
    const st = $(stage); if (!st) return;
    const P = parseFloat(getComputedStyle(st).perspective) || 1800;
    $$(".plane", st).forEach((p) => {
      const z = parseFloat(getComputedStyle(p).getPropertyValue("--z")) || 0;
      p.style.setProperty("--zs", ((P - z) / P).toFixed(4));
    });
  };

  /* ---------- Handheld ----------
     Sum of three sines per axis, sampled at 12 Hz into keyframes (linear between samples).
     amp in px, rot in degrees. 3-5 px reads as "operator on a tripod head", 10+ as handheld. */
  cine.handheld = function (tl, el, at, dur, opts = {}) {
    const amp = opts.amp ?? 5, rot = opts.rot ?? 0.25, seed = opts.seed ?? 7, rate = opts.rate ?? 1;
    const r = rng(seed);
    const ph = Array.from({ length: 9 }, () => r() * Math.PI * 2);
    const fq = [0.23, 0.51, 0.97].map((f) => f * rate);
    const n = Math.max(2, Math.ceil(dur * 12));
    const wave = (t, o) => (Math.sin(t * fq[0] * 6.283 + ph[o]) * 0.6 + Math.sin(t * fq[1] * 6.283 + ph[o + 1]) * 0.3 + Math.sin(t * fq[2] * 6.283 + ph[o + 2]) * 0.1);
    const kf = [];
    for (let i = 1; i <= n; i++) {
      const t = (i / n) * dur;
      kf.push({ x: amp * wave(t, 0), y: amp * 0.7 * wave(t, 3), rotation: rot * wave(t, 6), duration: dur / n, ease: "none" });
    }
    g.set($(el), { x: amp * wave(0, 0), y: amp * 0.7 * wave(0, 3), rotation: rot * wave(0, 6) });   // build-time start pose (a tl.set at 0 never renders)
    tl.to($(el), { keyframes: kf }, at);
    return tl;
  };

  /* ---------- Lens ---------- */
  /* Focus pull on one layer: --dof px from -> to. */
  cine.focus = (tl, el, at, dur, from, to, ease = "power2.inOut") =>
    tl.fromTo($$(el), { "--dof": from + "px" }, { "--dof": to + "px", duration: dur, ease }, at);
  /* Rack focus: near goes soft while far comes sharp (or back). */
  cine.rack = function (tl, near, far, at, dur = 0.9, max = 14) {
    cine.focus(tl, near, at, dur, 0, max);
    cine.focus(tl, far, at, dur, max, 0);
    return tl;
  };

  /* ---------- Light ---------- */
  /* Specular sweep across a .sweep / .sweep-text element. */
  cine.sweep = (tl, el, at, dur = 1.1, ease = "power2.inOut") =>
    tl.fromTo($$(el), { "--sweep": "120%" }, { "--sweep": "-20%", duration: dur, ease }, at);
  /* Light on: fade a light layer up from black (key, beam, rays). */
  cine.lightOn = (tl, el, at, dur = 1.6, to = 1, ease = "power2.inOut") =>
    tl.fromTo($$(el), { opacity: 0 }, { opacity: to, duration: dur, ease }, at);
  /* Anamorphic flare pass: the streak slides through frame and fades. */
  cine.flare = function (tl, el, at, dur = 1.4, opts = {}) {
    const e = $(el), x0 = opts.fromX ?? -500, x1 = opts.toX ?? 500;
    tl.fromTo(e, { x: x0, opacity: 0, scaleX: 0.6 }, { x: (x0 + x1) / 2, opacity: opts.peak ?? 0.9, scaleX: 1, duration: dur * 0.45, ease: "power2.out" }, at);
    tl.to(e, { x: x1, opacity: 0, scaleX: 1.2, duration: dur * 0.55, ease: "power2.in" }, at + dur * 0.45);
    return tl;
  };
  /* Motes: dust in a light beam, embers, or stars. Builds `count` dots inside `box` and
     drifts each one once across the shot. Positions come from the seed, not Math.random. */
  cine.motes = function (tl, box, at, dur, opts = {}) {
    const b = $(box), r = rng(opts.seed ?? 11), n = opts.count ?? 40;
    const W = b.clientWidth || 1920, H = b.clientHeight || 1080;
    const [s0, s1] = opts.size || [2, 6], drift = opts.drift || [40, -60], blur = opts.blur ?? 1.5;
    const color = opts.color || null, op = opts.opacity || [0.25, 0.8];
    for (let i = 0; i < n; i++) {
      const d = document.createElement("i");
      d.className = "mote";
      const s = s0 + r() * (s1 - s0);
      const near = s / s1; // bigger = nearer = softer and faster
      Object.assign(d.style, { left: (r() * W).toFixed(1) + "px", top: (r() * H).toFixed(1) + "px", width: s.toFixed(1) + "px", height: s.toFixed(1) + "px",
        opacity: (op[0] + r() * (op[1] - op[0])).toFixed(2), filter: `blur(${(blur * (0.4 + near)).toFixed(2)}px)` });
      if (color) d.style.background = color;
      if (opts.glow) d.style.boxShadow = `0 0 ${(s * 3).toFixed(0)}px ${opts.glow}`;
      b.appendChild(d);
      const k = 0.5 + near;
      tl.fromTo(d, { x: 0, y: 0 }, { x: drift[0] * k * (0.6 + r() * 0.8), y: drift[1] * k * (0.6 + r() * 0.8), duration: dur, ease: "none" }, at);
    }
    return tl;
  };
  /* Stars: a fixed field (no drift) for skies. */
  cine.stars = function (box, opts = {}) {
    const b = $(box), r = rng(opts.seed ?? 3), n = opts.count ?? 260;
    const W = b.clientWidth || 1920, H = b.clientHeight || 1080;
    for (let i = 0; i < n; i++) {
      const d = document.createElement("i");
      d.className = "mote";
      const big = r() > 0.94, s = big ? 2.2 + r() * 1.8 : 0.8 + r() * 1.4;
      Object.assign(d.style, { left: (r() * W).toFixed(1) + "px", top: (Math.pow(r(), opts.bias ?? 1.4) * H).toFixed(1) + "px", width: s.toFixed(2) + "px", height: s.toFixed(2) + "px",
        opacity: (0.35 + r() * 0.65).toFixed(2), boxShadow: big ? `0 0 ${(s * 4).toFixed(0)}px rgba(255,255,255,0.7)` : "none" });
      b.appendChild(d);
    }
  };

  /* ---------- Type ----------
     reveal(tl, el, style, at, opts): styles
       "track"  fades in out of a blur while the letters keep spreading (the trailer card)
       "focus"  a lens focus pull on the words: blur 24 -> 0, scale 1.06 -> 1
       "rise"   each line rises out of a mask, staggered
       "chars"  letter by letter out of a blur
       "slam"   lands hard from 1.3x in 0.2 s (pair with cine.flash and a hit)
       "fade"   plain fade
     hide(tl, el, style, at): "fade" | "blur" | "track" | "up" */
  function split(el) {
    if (el.dataset.split) return $$(".ch", el);
    const text = el.textContent; el.textContent = "";
    for (const c of text) { const s = document.createElement("span"); s.className = "ch"; s.textContent = c; el.appendChild(s); }
    el.dataset.split = "1";
    return $$(".ch", el);
  }
  function masks(el) {
    if (el.dataset.masked) return $$(".mask > *", el);
    Array.from(el.children).forEach((c) => { const m = document.createElement("span"); m.className = "mask"; el.insertBefore(m, c); m.appendChild(c); });
    el.dataset.masked = "1";
    return $$(".mask > *", el);
  }
  cine.reveal = function (tl, el, style = "focus", at = 0, opts = {}) {
    const e = $(el);
    const dur = opts.dur;
    switch (style) {
      case "track": {
        const ls0 = opts.from ?? 0.12, ls1 = opts.to ?? 0.34, hold = opts.hold ?? 3.5;
        tl.fromTo(e, { opacity: 0, filter: "blur(12px)" }, { opacity: 1, filter: "blur(0px)", duration: dur ?? 1.2, ease: "power2.out" }, at);
        tl.fromTo(e, { "--ls": ls0 + "em" }, { "--ls": ls1 + "em", duration: hold, ease: "power1.out" }, at);
        break;
      }
      case "focus":
        tl.fromTo(e, { opacity: 0, filter: "blur(24px)", scale: opts.scale ?? 1.06 }, { opacity: 1, filter: "blur(0px)", scale: 1, duration: dur ?? 1.3, ease: "power3.out" }, at);
        break;
      case "rise": {
        tl.fromTo(e, { opacity: 0 }, { opacity: 1, duration: FRAME }, at);
        tl.fromTo(masks(e), { yPercent: 110 }, { yPercent: 0, duration: dur ?? 0.9, ease: "power4.out", stagger: opts.stagger ?? 0.1 }, at);
        break;
      }
      case "chars": {
        tl.fromTo(e, { opacity: 0 }, { opacity: 1, duration: FRAME }, at);
        tl.fromTo(split(e), { opacity: 0, filter: "blur(10px)", y: opts.y ?? 0 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: dur ?? 0.6, ease: "power2.out", stagger: opts.stagger ?? 0.04 }, at);
        break;
      }
      case "slam":
        tl.fromTo(e, { opacity: 0, scale: opts.scale ?? 1.3 }, { opacity: 1, scale: 1, duration: dur ?? 0.2, ease: "expo.out" }, at);
        break;
      default:
        tl.fromTo(e, { opacity: 0 }, { opacity: 1, duration: dur ?? 0.8, ease: "power1.inOut" }, at);
    }
    return tl;
  };
  cine.hide = function (tl, el, style = "fade", at = 0, dur = 0.5) {
    const e = $(el);
    if (style === "blur") tl.to(e, { opacity: 0, filter: "blur(14px)", duration: dur, ease: "power2.in" }, at);
    else if (style === "track") { tl.to(e, { opacity: 0, duration: dur, ease: "power1.in" }, at); tl.to(e, { "--ls": "0.6em", duration: dur, ease: "power1.in" }, at); }
    else if (style === "up") tl.to(e, { opacity: 0, y: -24, duration: dur, ease: "power2.in" }, at);
    else tl.to(e, { opacity: 0, duration: dur, ease: "power1.in" }, at);
    return tl;
  };

  /* ---------- Edit ---------- */
  /* White flash on a hit: up in one frame, decays over `decay`. */
  cine.flash = function (tl, at, decay = 0.35, peak = 1, el = ".fx-flash") {
    tl.fromTo($(el), { opacity: 0 }, { opacity: peak, duration: FRAME, ease: "none", immediateRender: false }, at - FRAME);
    tl.to($(el), { opacity: 0, duration: decay, ease: "power2.out" }, at);
    return tl;
  };
  /* Dip to black and back (or just down: back = 0). */
  cine.dip = function (tl, at, down = 0.4, hold = 0.1, back = 0.4, el = ".fx-black") {
    tl.to($(el), { opacity: 1, duration: down, ease: "power1.in" }, at);
    if (back > 0) tl.to($(el), { opacity: 0, duration: back, ease: "power1.out" }, at + down + hold);
    return tl;
  };
  /* Fade up from black at the head of the film. */
  cine.fadeIn = (tl, at = 0, dur = 1.2, el = ".fx-black") => tl.fromTo($(el), { opacity: 1 }, { opacity: 0, duration: dur, ease: "power1.out" }, at);
  /* Light-leak burn across a cut: `at` is the cut time; the burn peaks on it. */
  cine.burn = function (tl, at, dur = 0.8, el = ".fx-leak") {
    tl.fromTo($(el), { opacity: 0, x: -300 }, { opacity: 1, x: 0, duration: dur / 2, ease: "power2.in" }, at - dur / 2);
    tl.to($(el), { opacity: 0, x: 300, duration: dur / 2, ease: "power2.out" }, at);
    return tl;
  };
  /* Whip pan between two shots' .cam wrappers. `cut` is the hard cut time between the clips.
     Only 2D content smears; keep 3D stages out of whipped shots. */
  cine.whip = function (tl, outCam, inCam, cut, dir = -1, dur = 0.24) {
    const W = 2200 * dir;
    tl.to($(outCam), { x: W, duration: dur, ease: "power3.in" }, cut - dur);
    tl.fromTo($(inCam), { x: -W }, { x: 0, duration: dur * 1.4, ease: "power3.out" }, cut);
    return tl;
  };

  /* ---------- Devices ---------- */
  /* Build the phone's edge (thickness) and glass. Call once per .phone3d at load. */
  cine.phone = function (el, opts = {}) {
    $$(el).forEach((p) => {
      if (p.dataset.built) return;
      const depth = opts.depth ?? 18, slabs = opts.slabs ?? 7;
      const body = document.createElement("div"); body.className = "p-body";
      const screen = p.querySelector(".p-screen");
      for (let i = slabs; i >= 1; i--) {
        const s = document.createElement("div"); s.className = "p-slab";
        s.style.transform = `translateZ(${(-depth * i / slabs).toFixed(1)}px)`;
        p.insertBefore(s, p.firstChild);
      }
      p.appendChild(body);
      if (screen) body.appendChild(screen);
      const island = document.createElement("div"); island.className = "p-island"; body.appendChild(island);
      const glare = document.createElement("div"); glare.className = "p-glare"; body.appendChild(glare);
      if (opts.shadow) { const sh = document.createElement("div"); sh.className = "p-shadow"; p.insertBefore(sh, p.firstChild); }
      p.dataset.built = "1";
    });
  };
  /* Turn a phone (or its .world) and slide the glass glare with it, so the light feels fixed in the room. */
  cine.turn = function (tl, el, at, dur, from, to, ease = "sine.inOut") {
    const e = $(el);
    tl.fromTo(e, Object.assign({ rotationY: 0, rotationX: 0 }, from), Object.assign({ duration: dur, ease }, to), at);
    const gx = (ry) => 60 - (ry || 0) * 2.2 + "%";
    const glare = e.querySelector(".p-glare");
    if (glare) tl.fromTo(glare, { "--gx": gx(from.rotationY) }, { "--gx": gx(to.rotationY), duration: dur, ease }, at);
    return tl;
  };

  /* ---------- Lines that draw ---------- */
  /* SVG strokes draw on, one after another. <line>s grow from (x1,y1) to (x2,y2), so they also work
     with vector-effect: non-scaling-stroke; <path>s need pathLength="1" and draw by dash offset. */
  cine.draw = function (tl, el, at, dur = 0.8, stagger = 0.12, ease = "power2.inOut") {
    $$(el).forEach((e, i) => {
      const t = at + i * stagger;
      if (e.tagName.toLowerCase() === "line") {
        const x2 = e.getAttribute("x2"), y2 = e.getAttribute("y2");
        tl.fromTo(e, { attr: { x2: e.getAttribute("x1"), y2: e.getAttribute("y1") } }, { attr: { x2, y2 }, duration: dur, ease }, t);
      } else {
        tl.fromTo(e, { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur, ease }, t);
      }
    });
    return tl;
  };

  window.cine = cine;
})();
