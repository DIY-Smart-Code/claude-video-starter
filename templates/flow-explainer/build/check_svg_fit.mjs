#!/usr/bin/env node
/**
 * check_svg_fit.mjs -- blocking gate: built diagrams must not collide with their own text.
 *
 * `hyperframes check` audits HTML boxes; the flow diagrams are SVG wires, rings and zones, so a wire
 * through a label or a chip on a zone border slips past it. This sweep catches them.
 *
 * Loads the bundled composition in headless Chrome (the same path `hyperframes snapshot` uses), seeks
 * the timeline every --step seconds and, among VISIBLE elements (effective opacity >= 0.25), reports:
 *   text_crosses_box   SVG/HTML text whose ink box straddles an SVG <rect> edge (partly in, partly out)
 *   text_overlaps_text two text runs overlapping (> 12 % of the smaller)
 *   stroke_through_text a stroked SVG line/path/circle passing through a text's ink box
 *   box_crosses_box    two SVG rects that overlap without one containing the other
 *   text_off_canvas    SVG text running past the frame (the root composition's data-width x data-height)
 *   text_under_box     SVG text left at full opacity under an opaque rect painted after it in the same <svg>:
 *                      a label or pill that was never hidden when the card replacing it landed on top. It shows
 *                      through every fade (a pill orphaned under the card that replaced it).
 * A defect blocks when it persists >= --min-span seconds (default 0.5): elements mid-motion pass each other.
 *
 * Opt-outs (for deliberate overlaps only): data-fit-allow on the element or any ancestor skips it
 * entirely; data-fit-allow="stroke" exempts only its strokes (e.g. a strike line drawn through text).
 * The decorative chrome behind every scene (#shape-backdrop, the grid ground) is skipped,
 * and a stroke point covered by an opaque SVG rect painted after it (a label knocked out of a line) is hidden.
 *
 * Usage:  node build/check_svg_fit.mjs <video folder> [--step 0.25] [--from s] [--to s] [--min-span 0.5] [--json out.json]
 * Exit 0 = clean, 2 = blocking defects, 1 = the sweep itself failed.
 * Waiver (one line in <video folder>/notes.md): svg-fit: waived -- <reason>
 */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
if (!argv.length || argv[0].startsWith("--")) {
  console.log("usage: node build/check_svg_fit.mjs <video folder> [--step 0.25] [--from s] [--to s] [--min-span 0.5] [--json out.json]");
  process.exit(1);
}
const project = path.resolve(argv[0]);
const opt = (k, d) => (argv.includes(k) ? argv[argv.indexOf(k) + 1] : d);
const STEP = parseFloat(opt("--step", "0.25"));
const MIN_SPAN = parseFloat(opt("--min-span", "0.5"));
const FROM = parseFloat(opt("--from", "0"));
const TO = opt("--to", null);
const JSON_OUT = opt("--json", null);

const notes = path.join(project, "notes.md");
if (fs.existsSync(notes) && fs.readFileSync(notes, "utf8").split(/\r?\n/).some((l) => l.trim().toLowerCase().startsWith("svg-fit: waived"))) {
  console.log(`[svg-fit] waived via ${notes}`);
  process.exit(0);
}

// hyperframes internals, located by export name so a re-hashed chunk still resolves; a missing export fails loudly.
const require = createRequire(path.join(project, "package.json"));   // resolves the repo's pinned hyperframes
const dist = path.join(path.dirname(require.resolve("hyperframes/package.json")), "dist");
async function load(name) {
  for (const f of fs.readdirSync(dist).filter((f) => f.endsWith(".js"))) {
    const src = fs.readFileSync(path.join(dist, f), "utf8");
    if (new RegExp(`export \\{[^}]*\\b${name}\\b[^}]*\\}\\s*;?\\s*$`).test(src)) {
      const mod = await import(pathToFileURL(path.join(dist, f)).href);
      if (typeof mod[name] === "function") return mod[name];
    }
  }
  throw new Error(`hyperframes export not found: ${name} (hyperframes upgraded? update build/check_svg_fit.mjs)`);
}

const AUDIT = (t) => {
  // frame size from the root composition (1080x1920 Shorts, 1920x1080 long-form)
  const rootEl = document.querySelector("[data-composition-id][data-width][data-height]");
  const W = (rootEl && parseFloat(rootEl.getAttribute("data-width"))) || 1920;
  const H = (rootEl && parseFloat(rootEl.getAttribute("data-height"))) || 1080;
  const memo = new Map();
  const opac = (el) => {
    if (!el || el.nodeType !== 1) return 1;
    if (memo.has(el)) return memo.get(el);
    const cs = getComputedStyle(el);
    let o = cs.display === "none" || cs.visibility === "hidden" ? 0 : parseFloat(cs.opacity || "1");
    if (o > 0.01) o *= opac(el.parentElement || (el.parentNode && el.parentNode.host));
    memo.set(el, o);
    return o;
  };
  // decorative chrome painted behind every scene (ghosted topic shapes, ground marks)
  const DECOR = "#mark-a, #mark-b, #paper, .mark, #shape-backdrop";
  const allowed = (el, what) => {
    if (el.closest(DECOR)) return true;
    const a = el.closest("[data-fit-allow]");
    if (!a) return false;
    const v = a.getAttribute("data-fit-allow");
    return !v || v === "all" || v.split(/\s+/).includes(what);
  };
  const key = (el) => {
    if (el.id) return "#" + el.id;
    const host = el.closest("[id]");
    const sib = host ? Array.from(host.querySelectorAll(el.tagName)).indexOf(el) : -1;
    return (host ? "#" + host.id : "") + ">" + el.tagName.toLowerCase() + (sib >= 0 ? "[" + sib + "]" : "");
  };
  const onCanvas = (r) => r.right > 0 && r.left < W && r.bottom > 0 && r.top < H && r.width > 0 && r.height > 0;
  const inter = (a, b) => {
    const w = Math.min(a.right, b.right) - Math.max(a.left, b.left);
    const h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    return w > 0 && h > 0 ? { w, h, area: w * h } : null;
  };
  const contains = (o, i, tol) => i.left >= o.left - tol && i.right <= o.right + tol && i.top >= o.top - tol && i.bottom <= o.bottom + tol;
  const paint = (cs, prop) => {
    const v = cs[prop];
    if (!v || v === "none" || v === "transparent") return false;
    const m = v.match(/rgba?\(([^)]+)\)/);
    if (m) { const p = m[1].split(",").map(Number); if (p.length === 4 && p[3] < 0.08) return false; }
    return true;
  };

  // text runs: SVG <text> and HTML text nodes, as approximate INK boxes (font boxes carry ascent/descent padding)
  const texts = [];
  const ink = (r) => {
    const padY = r.height * 0.2;
    return { left: r.left + 1, right: r.right - 1, top: r.top + padY, bottom: r.bottom - padY, width: r.width - 2, height: r.height - 2 * padY };
  };
  for (const el of document.querySelectorAll("svg text")) {
    if (!el.textContent.trim() || allowed(el, "text")) continue;
    const o = opac(el);
    if (o < 0.25) continue;
    const r = el.getBoundingClientRect();
    if (!(r.width > 0)) continue;
    texts.push({ el, key: key(el), txt: el.textContent.trim().slice(0, 40), r: ink(r), raw: r, svg: true });
  }
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const range = document.createRange();
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const el = n.parentElement;
    if (!el || !n.nodeValue.trim() || el.closest("svg, script, style, template") || allowed(el, "text")) continue;
    if (opac(el) < 0.25) continue;
    range.selectNodeContents(n);
    for (const r of range.getClientRects()) {
      if (r.width < 4 || !onCanvas(r)) continue;
      texts.push({ el, key: key(el), txt: n.nodeValue.trim().slice(0, 40), r: ink(r), raw: r, svg: false });
    }
  }

  // boxes: visible SVG rects with paint, not full-frame grounds. Opaque ones also occlude strokes drawn before them
  // (a label knocked out of a line on a paper patch is deliberate, not a collision).
  const boxes = [], occluders = [], rotated = [];
  const opaqueFill = (cs) => {
    if (!paint(cs, "fill")) return false;
    const m = cs.fill.match(/rgba\(([^)]+)\)/);
    return !(m && Number(m[1].split(",")[3]) < 0.9) && parseFloat(cs.fillOpacity || "1") >= 0.9;
  };
  for (const el of document.querySelectorAll("svg rect, svg circle, svg ellipse")) {
    const o = opac(el);
    if (o < 0.25) continue;
    const r = el.getBoundingClientRect();
    if (!onCanvas(r)) continue;
    const cs = getComputedStyle(el);
    if (o >= 0.9 && opaqueFill(cs)) occluders.push({ el, r });
    if (el.tagName.toLowerCase() !== "rect" || allowed(el, "box")) continue;
    if (!paint(cs, "fill") && !paint(cs, "stroke")) continue;
    // a rotated rect (a tilted beam, a tipped card): its screen bbox is far larger than the shape, so trace its
    // outline instead and test it like a stroke
    const ctm = el.getScreenCTM();
    if (ctm && (Math.abs(ctm.b) > 0.01 * Math.abs(ctm.a) || Math.abs(ctm.c) > 0.01 * Math.abs(ctm.d))) {
      const x0 = el.x.baseVal.value, y0 = el.y.baseVal.value, w0 = el.width.baseVal.value, h0 = el.height.baseVal.value;
      const svg = el.ownerSVGElement, pts = [];
      const corners = [[x0, y0], [x0 + w0, y0], [x0 + w0, y0 + h0], [x0, y0 + h0], [x0, y0]];
      for (let c = 0; c < 4; c++) {
        const [ax, ay] = corners[c], [bx, by] = corners[c + 1];
        const n = Math.max(4, Math.round(Math.hypot(bx - ax, by - ay) / 6));
        for (let i = 0; i < n; i++) {
          const q = svg.createSVGPoint(); q.x = ax + ((bx - ax) * i) / n; q.y = ay + ((by - ay) * i) / n;
          const s = q.matrixTransform(ctm); pts.push([s.x, s.y]);
        }
      }
      rotated.push({ el, key: key(el), pts });
      continue;
    }
    if (r.width < 40 || r.height < 24 || (r.width >= W * 0.9 && r.height >= H * 0.9)) continue;
    // a translucent, strokeless band is a spotlight laid behind content, not a box anything can spill out of
    const m = (cs.fill || "").match(/rgba\(([^)]+)\)/);
    const fillA = (m ? Number(m[1].split(",")[3]) : 1) * parseFloat(cs.fillOpacity || "1") * o;
    if (!paint(cs, "stroke") && fillA < 0.5) continue;
    boxes.push({ el, key: key(el), r });
  }
  const hidden = (stroke, x, y) => occluders.some((oc) =>
    x > oc.r.left && x < oc.r.right && y > oc.r.top && y < oc.r.bottom &&
    (stroke.compareDocumentPosition(oc.el) & Node.DOCUMENT_POSITION_FOLLOWING));

  // strokes: sample points along every visible stroked line/path/circle
  const strokes = [];
  for (const el of document.querySelectorAll("svg line, svg path, svg polyline, svg circle, svg ellipse")) {
    if (allowed(el, "stroke")) continue;
    if (opac(el) < 0.25) continue;
    const cs = getComputedStyle(el);
    if (!paint(cs, "stroke") || parseFloat(cs.strokeWidth) < 2) continue;
    // dash-drawn but not yet drawn (draw verb at dashoffset ~1) -> skip
    if (cs.strokeDasharray !== "none" && el.getAttribute("pathLength") === "1" && parseFloat(cs.strokeDashoffset) > 0.97) continue;
    let len = 0;
    try { len = el.getTotalLength(); } catch (e) { continue; }
    const ctm = el.getScreenCTM();
    if (!ctm || !(len > 0)) continue;
    const n = Math.max(8, Math.min(400, Math.round(len / 6)));
    const pts = [];
    const svg = el.ownerSVGElement;
    for (let i = 0; i <= n; i++) {
      const p = el.getPointAtLength((len * i) / n);
      const q = svg.createSVGPoint(); q.x = p.x; q.y = p.y;
      const s = q.matrixTransform(ctm);
      pts.push([s.x, s.y]);
    }
    strokes.push({ el, key: key(el), pts });
  }
  for (const r of rotated) if (!allowed(r.el, "stroke")) strokes.push(r);

  const out = [];
  const add = (code, a, b, extra) => out.push({ code, a: a.key, b: b ? b.key : "", txt: a.txt || "", btxt: b && b.txt ? b.txt : "", ...extra });

  for (const tx of texts) {
    if (tx.svg && (tx.r.left < -2 || tx.r.right > W + 2 || tx.r.top < -2 || tx.r.bottom > H + 2) && onCanvas(tx.raw))
      add("text_off_canvas", tx, null, { at: [Math.round(tx.r.left), Math.round(tx.r.top)] });
    for (const bx of boxes) {
      const i = inter(tx.r, bx.r);
      if (!i || i.w < 3 || i.h < 3) continue;
      if (contains(bx.r, tx.r, 2)) continue;
      add("text_crosses_box", tx, bx, { at: [Math.round(tx.r.left), Math.round(tx.r.top)] });
    }
    // within one <svg> document order is paint order, so a later opaque rect over the text is covering it
    if (tx.svg) {
      const svg = tx.el.ownerSVGElement;
      for (const oc of occluders) {
        if (oc.el.tagName.toLowerCase() !== "rect" || oc.el.ownerSVGElement !== svg || allowed(oc.el, "box")) continue;
        if (!(tx.el.compareDocumentPosition(oc.el) & Node.DOCUMENT_POSITION_FOLLOWING)) continue;
        const i = inter(tx.r, oc.r);
        if (!i || i.area < 0.5 * tx.r.width * tx.r.height) continue;
        add("text_under_box", tx, { key: key(oc.el) }, { at: [Math.round(tx.r.left), Math.round(tx.r.top)] });
        break;
      }
    }
    for (const st of strokes) {
      let hit = 0;
      for (const [x, y] of st.pts)
        if (x > tx.r.left + 2 && x < tx.r.right - 2 && y > tx.r.top + 1 && y < tx.r.bottom - 1 && !hidden(st.el, x, y)) hit++;
      if (hit >= 2) add("stroke_through_text", tx, st, { at: [Math.round(tx.r.left), Math.round(tx.r.top)] });
    }
  }
  for (let i = 0; i < texts.length; i++)
    for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i], b = texts[j];
      if (a.el === b.el || a.el.contains(b.el) || b.el.contains(a.el)) continue;
      const x = inter(a.r, b.r);
      if (x && x.area > 0.12 * Math.min(a.r.width * a.r.height, b.r.width * b.r.height))
        add("text_overlaps_text", a, b, { at: [Math.round(a.r.left), Math.round(a.r.top)] });
    }
  for (let i = 0; i < boxes.length; i++)
    for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], b = boxes[j];
      const x = inter(a.r, b.r);
      if (!x || x.w < 4 || x.h < 4) continue;
      if (contains(a.r, b.r, 2) || contains(b.r, a.r, 2)) continue;
      add("box_crosses_box", a, b, { at: [Math.round(Math.max(a.r.left, b.r.left)), Math.round(Math.max(a.r.top, b.r.top))] });
    }
  return out;
};

const main = async () => {
  const bundle = await load("bundleWithLocalizedFonts");
  const serve = await load("serveStaticProjectHtml");
  const open = await load("openSettledCompositionPage");
  const seek = await load("seekCompositionTimeline");
  const html = await bundle(project);
  const server = await serve(project, html, undefined, []);
  const { browser, page } = await open(html, server.url, { renderReadyTimeoutMs: 20000, renderReadyWarningSuffix: "svg-fit may be inaccurate" });
  const runs = new Map();
  let n = 0;
  try {
    await page.evaluate(() => document.fonts.ready);
    const duration = await page.evaluate(() => {
      const p = window.__player;
      if (p && typeof p.getDuration === "function") { const d = p.getDuration(); if (d > 0) return d; }
      const root = document.querySelector("[data-composition-id][data-duration]");
      return root ? parseFloat(root.getAttribute("data-duration")) : 0;
    });
    const end = TO ? Math.min(parseFloat(TO), duration) : duration;
    if (!(end > 0)) throw new Error("composition duration is 0");
    for (let t = FROM; t <= end + 1e-6; t = Math.round((t + STEP) * 1000) / 1000) {
      await seek(page, t, { fallbackToBridgeAndTimelines: true, animationFrameSettle: "double", waitForFontsMs: 0, settleMs: 0 });
      const found = await page.evaluate(AUDIT, t);
      n++;
      for (const f of found) {
        const k = `${f.code}|${f.a}|${f.b}`;
        const r = runs.get(k);
        if (r && t - r.last <= STEP * 1.5) { r.last = t; r.hits++; }
        else {
          if (r) (r.done ||= []).push([r.first, r.last]);
          runs.set(k, { ...f, first: t, last: t, hits: 1, done: r ? r.done : undefined });
        }
      }
      if (n % 400 === 0) process.stdout.write(`[svg-fit] ${t.toFixed(1)}s / ${end.toFixed(1)}s\n`);
    }
  } finally {
    await browser.close().catch(() => {});
    await server.close().catch(() => {});
  }
  const defects = [];
  for (const r of runs.values()) {
    const spans = [...(r.done || []), [r.first, r.last]];
    const long = spans.filter(([a, b]) => b - a >= MIN_SPAN - 1e-6);
    if (long.length) defects.push({ ...r, spans: long });
  }
  defects.sort((a, b) => a.spans[0][0] - b.spans[0][0]);
  const fmt = (s) => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, "0")}`;
  for (const d of defects) {
    const when = d.spans.map(([a, b]) => `${fmt(a)}-${fmt(b)}`).join(", ");
    const what = [d.txt && `"${d.txt}"`, d.btxt && `vs "${d.btxt}"`].filter(Boolean).join(" ");
    console.log(`  ${d.code.padEnd(20)} ${when.padEnd(22)} ${d.a}${d.b ? "  x  " + d.b : ""}  ${what}  @${d.at.join(",")}`);
  }
  if (JSON_OUT) fs.writeFileSync(JSON_OUT, JSON.stringify(defects, null, 1));
  console.log(`[svg-fit] ${n} samples, ${defects.length} blocking defect(s)`);
  process.exit(defects.length ? 2 : 0);
};

main().catch((e) => { console.error(`[svg-fit] sweep failed: ${e && e.stack ? e.stack : e}`); process.exit(1); });
