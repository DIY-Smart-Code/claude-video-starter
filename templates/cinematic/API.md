# cine.js / cine.css reference

`lib/cine.js` exposes `window.cine`. Every call adds finite tweens to the paused timeline you pass in;
nothing reads the clock or `Math.random`, so every frame renders the same way twice. Times are seconds
on the film's clock. Selectors can be strings, elements or arrays.

```js
const tl = cine.film("main", 30);      // paused timeline on window.__timelines.main; reads data-aspect
// ... shots ...
cine.end(tl, 30);                       // pin the timeline to the film length
```

## Markup anatomy (cine.css)

```html
<section id="s4" class="shot clip" data-start="11" data-duration="6" data-track-index="3">
  <div class="key-pool" style="--kx:50%; --ky:45%"></div>      <!-- where the light falls -->
  <div class="cam">                                              <!-- 2D camera: blurred natively -->
    <div class="rig">                                            <!-- optional handheld wrapper -->
      <div class="stage"><div class="world">                     <!-- optional 3D lens + world -->
        <div class="plane" style="--z:-600px">...</div>         <!-- a depth layer -->
      </div></div>
    </div>
  </div>
  <div class="band center"><div class="display t">Line</div></div>   <!-- type lives in the band -->
</section>
```

| Class | What it is |
|---|---|
| `.shot` | a full-frame clip with its own `--void` background |
| `.cam` / `.rig` | 2D camera / handheld wrappers (transform-origin centre) |
| `.stage` / `.world` / `.plane` | 3D: static perspective (1800 px), preserve-3d world, depth layer (`--z`) |
| `.band` | the box between the letterbox bars; `.center` stacks and centres its children |
| `.key-pool` (`--kx --ky`) | radial pool of key light |
| `.beam` | volumetric shaft from above (rotate, size and place it inline) |
| `.rays` (`--rx --ry`) | god rays fanning from a point |
| `.haze` | low fog bank |
| `.flare` | anamorphic streak (driven by `cine.flare`) |
| `.dof` | layer whose blur is `--dof` (driven by `cine.focus` / `cine.rack`) |
| `.sweep` / `.sweep-text` / `.sweep-logo` (`--mask:url(...)`) | a band of light crosses an object / the letters / a logo image's own pixels (driven by `cine.sweep`) |
| `.t` | hidden until revealed (`opacity: 0`) |
| `.kicker` `.display` `.trailer` `.wordmark` `.small` | type roles: tracked sans 40 px, Cormorant 112 px, Anton caps 168 px, tracked wordmark 96 px, muted 40 px |
| `.track` | tracked and still centred (pads left by `--ls`) |
| `.glow-text` | key-coloured halo for type over darkness |
| `.phone3d` (`--pw`) + `.p-screen` | a phone with thickness, island and glare (built by `cine.phone`) |
| `.fx-flash` `.fx-black` `.fx-leak` | edit overlays, one each, spanning the film |
| `.bars` | preview-only letterbox in the cut (the finish draws its own) |

Palette and fonts: `--void --ink --muted --key --fill --accent`, `--f-display --f-trailer --f-sans`.
Bundled fonts (OFL): Cormorant Garamond (variable, roman and italic), Anton, Inter 400-700.

## Camera

| Call | Does |
|---|---|
| `cine.move(tl, el, at, dur, to, {from, ease})` | any camera tween (`scale x y rotation`); default `sine.inOut` |
| `cine.push(tl, el, at, dur, amount=0.08, {x, y, ease})` | dolly in: scale 1 → 1+amount, `ease: "none"` |
| `cine.pull(tl, el, at, dur, amount=0.08)` | dolly out from 1+amount, `power2.out` |
| `cine.truck(tl, el, at, dur, dx=-120)` | lateral slide |
| `cine.parallax(tl, scope, at, dur, dx, dy, ease)` | every `[data-depth]` child of `scope` moves by `dx*depth, dy*depth` |
| `cine.crash(tl, el, at, dur=0.22, amount=0.6)` | crash zoom (`power4.in`) into a hit |
| `cine.orbit(tl, world, at, dur, from, to, ease)` | 3D pose tween: `rotationY rotationX z x y` |
| `cine.depth(stage)` | rescale `.plane`s so each keeps its authored size at its `--z` |
| `cine.handheld(tl, el, at, dur, {amp=5, rot=0.25, seed, rate=1})` | seeded three-sine drift sampled at 12 Hz |
| `cine.whip(tl, outCam, inCam, cut, dir=-1, dur=0.24)` | whip pan across a hard cut at `cut` |

Motion blur only applies to 2D layers: anything inside `.stage` / `.world`, or with `mix-blend-mode`,
renders sharp. Keep 3D moves slow; whip and crash on 2D `.cam`s.

## Lens and light

| Call | Does |
|---|---|
| `cine.focus(tl, el, at, dur, from, to, ease)` | tween `--dof` (px) |
| `cine.rack(tl, near, far, at, dur=0.9, max=14)` | near blurs out while far comes sharp |
| `cine.lightOn(tl, el, at, dur=1.6, to=1)` | fade a light layer up from black |
| `cine.sweep(tl, el, at, dur=1.1)` | specular band across `.sweep` / `.sweep-text` |
| `cine.flare(tl, el, at, dur=1.4, {fromX, toX, peak})` | anamorphic streak passes through |
| `cine.motes(tl, box, at, dur, {count, seed, size, drift, color, glow, blur, opacity})` | seeded dust / embers drifting once across the shot |
| `cine.stars(box, {count, seed, bias})` | fixed seeded star field |

## Type

`cine.reveal(tl, el, style, at, opts)`:

| style | Look | opts |
|---|---|---|
| `track` | fades out of a blur while the tracking keeps opening (`--ls`) | `from to` (em), `hold`, `dur` |
| `focus` | lens pull: blur 24 → 0, scale 1.06 → 1 | `scale`, `dur` |
| `rise` | each child line rises out of a mask | `stagger`, `dur` |
| `chars` | letter by letter out of a blur | `stagger`, `y`, `dur` |
| `slam` | lands from 1.3x in 0.2 s (pair with `cine.flash` and a boom) | `scale`, `dur` |
| `fade` | plain fade | `dur` |

`cine.hide(tl, el, style, at, dur)`: `fade`, `blur`, `track`, `up`.

## Edit

| Call | Does |
|---|---|
| `cine.flash(tl, at, decay=0.35, peak=1)` | white frame on a hit |
| `cine.dip(tl, at, down=0.4, hold=0.1, back=0.4)` | dip to black (`back=0` stays black) |
| `cine.fadeIn(tl, at=0, dur=1.2)` | fade up from black |
| `cine.burn(tl, at, dur=0.8)` | light-leak burn peaking on the cut at `at` |
| `cine.draw(tl, el, at, dur=0.8, stagger=0.12)` | SVG lines grow on (paths: dash offset, `pathLength="1"`) |

## Devices

`cine.phone(el, {depth=18, slabs=7, shadow})` builds edge slabs, the island and the glare around the
`.p-screen` you wrote. Put the phone in a `.world` and orbit the world, or turn the phone itself with
`cine.turn(tl, el, at, dur, from, to)`, which also slides the glare so the light stays fixed in the room.
Real product screenshots go in `.p-screen` as `<img>`; never generate fake UI as an image.

## film.json

```jsonc
{
  "look": "night",                 // night | teal-orange | warm-film | clean | noir; or "grade": { ...payload }
  "audio": {
    "loudness": -14,               // LUFS target of the final mix (-1 dBTP)
    "music": { "src": "assets/score/music.mp3", "volume": 0.9, "fadeIn": 0.8, "fadeOut": 1.2,
               "offset": 0, "start": 0,
               "envelope": [[0, 0], [8.2, 0], [8.7, -22], [10.7, -22], [11.0, 0]] },   // [t, dB]
    "voice": { "src": "narration.wav", "start": 0.6, "volume": 1.0 },                   // optional
    // or place each spoken line on its own: "segments": [[at, from, to], ...] (seconds; from/to in the narration)
    "duck": 0.35,                  // music ducks under the voice (sidechain); 0 = off
    "sfx": [ { "at": 11.0, "src": "assets/score/sfx/boom.mp3", "volume": 1.0, "dur": 2.5 } ]
  },
  "score": {                       // `film.py score` generates whatever is missing (ElevenLabs)
    "music": { "out": "assets/score/music.mp3", "styles": [], "negative": [],
               "sections": [ { "name": "Night", "ms": 8000, "styles": [], "negative": [] } ] },  // >= 3000 ms each
    "sfx": { "boom": { "prompt": "massive cinematic trailer boom ...", "seconds": 3 } }
  }
}
```

Format comes from `index.html`'s root: `data-duration`, `data-width`, `data-height`, `data-fps`,
`data-aspect` (`2.39` default, `2`, `1.85`, `16:9`, `9:16`).
