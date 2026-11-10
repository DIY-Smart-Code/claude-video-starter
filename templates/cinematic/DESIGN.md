# Cinematic template: design contract

What makes a marketing film read as *cinema* instead of *motion graphics*, and how this template
does each part. Read this before the first shot. `API.md` lists every call; `index.html` (the Nocturne
demo) uses all of them.

The previous templates animate a layout. This one films a world: the product sits in darkness, light
falls on it from one direction, a camera moves through it, and the result is graded, grained and
letterboxed like a film print.

## 1. The two passes

| Pass | File | What happens | Why |
|---|---|---|---|
| **Cut** | `index.html` | picture only: shots, lighting, camera, type, edit. 24 fps, native motion blur at a 180° shutter | where the craft happens; previewable live |
| **Finish** | `build/finish.html` (generated) | the cut as one `<video>` graded by the HyperFrames colour shader (wheels, contrast, bloom, channel separation, vignette, film grain), clean letterbox bars, the mixed score | the grade sits over *everything*, type included, so it all looks like one piece of film |

`scripts/film.py all videos/<slug>` runs both, plus the mix and a contact sheet. The finish exists as
a second pass for a technical reason too: capture motion blur and the WebGL grade can't share a page.

## 2. Format

- **24 fps** (`data-fps="24"`). Film cadence; 30 fps reads as video.
- **180° shutter** (`data-motion-blur-shutter="180"`): each frame is exposed for half the frame
  interval, 1/48 s, which is the motion blur the eye expects from cinema ([StudioBinder](https://www.studiobinder.com/blog/what-is-the-180-degree-shutter-rule/)).
  HyperFrames 0.9's capture blur draws it for real on moving 2D layers.
- **2.39:1 inside 16:9** (`data-aspect="2.39"`): 138 px bars top and bottom of a 1080 frame. Every read
  stays inside the band (`.band`). Use `2` for a softer widescreen, `16:9` for full frame, and a 1080 x 1920
  root with `data-aspect="9:16"` for vertical (no bars).

## 3. Light (the biggest difference)

1. **Start from black.** Every shot is lit *out of* `--void`. Nothing sits on a flat colour field.
2. **One key, one direction.** A `.key-pool` sets where the light falls; everything else falls off.
3. **Separate with rim light, reveal with fill.** Apple-style product films hide the product's face with
   backlight on its edges, then fade a fill in for the reveal, and pass a moving light across the
   edges ([Manfrotto: shooting tech like Apple](https://www.manfrotto.com/global-uk/stories/how-to-shoot-cinematic-tech-videos-like-apple)).
   Here: `.rim-*` glows behind the device, `cine.lightOn` for the fill, `cine.sweep` / the phone's glare for
   the moving light.
4. **Air.** One atmospheric layer per shot: `.haze`, `.beam`, `.rays` or `cine.motes` (dust in the beam,
   embers, stars). It is what turns a layout into a space.
5. **Warm key, cool fill** (`--key`, `--fill`) unless the brand says otherwise. The finish's wheels push
   the same split (cool shadows, warm highlights).

## 4. Camera

| Move | Call | When | Feel |
|---|---|---|---|
| Dolly in | `cine.push` (4-8 %) | almost every hold | attention, tension |
| Pull out | `cine.pull` | reveals: "it was the phone all along" | context |
| Truck + parallax | `cine.parallax` on `[data-depth]` layers | landscapes, worlds | depth without 3D |
| Orbit | `cine.orbit` on a `.world` (3D) | product heroes | the product turns toward us |
| Handheld | `cine.handheld` (3-6 px) | human or tense beats | presence |
| Whip pan | `cine.whip` | energetic cuts between 2D shots | momentum, motion-blurred |
| Crash zoom | `cine.crash` | the last frames before a hit | impact |
| Rack focus | `cine.rack` / `cine.focus` | handing attention from one plane to another | lens, depth |

Rules:
- **Every shot moves.** A locked frame is a choice for one beat (a title card), never the default. That
  also satisfies the repo rule that something changes at least every 3 seconds.
- **Moves are slow and constant.** Dollies run `ease: "none"` across the whole shot and through the cut.
  Easing in and out of every move is the motion-graphics tell.
- **3D only for slow moves.** Layers inside a `.stage` / `.world` get no motion blur, so orbits and dollies
  in 3D stay slow; whips and crash zooms go on 2D `.cam` wrappers.

## 5. Edit

Trailers start high with a cold open, set up the world, turn hard on one beat (a music drop, a title, a
hit), escalate with shorter and shorter cuts, then land the title card and a button
([Filmmaker Genius](https://filmmakergenius.com/academy/how-to-make-a-film-trailer/trailer-three-act-structure),
[Derek Lieu via Jonny Elwyn](https://jonnyelwyn.co.uk/film-and-video-editing/how-to-edit-a-movie-trailer)).
Trailer editors build three music cues for three acts and never resolve everything
([Filmmaker Magazine](https://filmmakermagazine.com/37093-first-impressions)). For a 30-60 s marketing film:

| Act | Share | Job | Typical shots |
|---|---|---|---|
| Cold open | 10-15 % | a picture and a question, almost no type | light in the dark, a detail |
| Act 1 | 20-25 % | the world and the problem, in a few words | landscape, title cards |
| **The turn** | 1 beat | silence, then the hit (flash + boom) | the product lit for the first time |
| Act 2 | 30-35 % | the product's promise, one idea per shot | hero orbit, macro, feature |
| Act 3 | 10-15 % | escalation: 3-5 cuts under a second each | montage on the beat |
| Title + button | 15 % | name, line, where to get it | wordmark catching the light |

- **Cut on the music.** Shot boundaries sit on beats or hits; the score's sections match the acts.
- **Silence before the hit.** Pull the music down (`envelope` in `film.json`) for 1.5-2.5 s before the
  turn, put a riser in the gap, hit on the cut.
- **Hard cuts by default.** Dissolves are for time passing. Flash cuts (`cine.flash`) mark hits, whips
  (`cine.whip`) carry energy, light-leak burns (`cine.burn`) mark a mood change, dips (`cine.dip`) end acts.
- **Shots are short.** 2-5 s for holds, 0.5-0.8 s in the montage. Nothing over 6 s without a new move.

## 6. Type

- **Less is more.** A marketing film has 5-8 cards in total. Each one is a short line, one idea.
- **Small, spaced, lit.** Kickers at 40 px with 0.4 em tracking; display lines in Cormorant Garamond at
  80-112 px; Anton caps (`.trailer`) only for the one line that hits. The wordmark tracks out slowly
  (`cine.reveal(..., "track")`) and catches the light (`.sweep-text` + `cine.sweep`).
- **Type enters like a lens, not like a slide.** `focus` (blur pull), `track` (spreading letters), `rise`
  (masked lines), `chars`. Never bounce, never pop.
- **Inside the band**, centred, or bottom-third under a hero. Never on a busy area without darkness behind it.
- Repo floor still applies: 40 px minimum on 16:9, 48 px on 9:16.

## 7. Sound

Sound is half of the cinematic feel. Every film has:
1. **A score in sections that match the acts** (`score.music.sections` in `film.json`; ElevenLabs music,
   each section 3 s or longer).
2. **Designed hits:** a drone under the cold open, a riser into the turn, a boom on the hit, whooshes on
   whips, ticks on montage cuts, a shimmer on the light sweep (`score.sfx`, generated once).
3. **Dynamics:** the envelope pulls the music down before the hit; the voice (if any) ducks the music by
   sidechain; the mix is normalised to -14 LUFS / -1 dBTP.

The repo's default is no music; choosing this template is the request for a score.

## 8. Grade

`film.json` `look`: `night` (default: blue-black shadows, warm highlights), `teal-orange`, `warm-film`,
`clean` (brand colours stay true), `noir`. Or give a full `grade` payload (any HyperFrames
`data-color-grading` keys: `adjust`, `wheels`, `curves`, `details`, `effects`). Keep grain ≤ 0.45, bloom
≤ 0.8 and channel separation ≤ 0.08: past that it reads as an effect, not a film.

## 9. Checks before you hand over

- The first frame already shows light and a subject, not an empty void.
- Every shot has a key, darkness and one air layer; every shot moves.
- No read sits outside the band; nothing important is clipped by a bar.
- The turn has silence before it and a hit on it; the montage cuts are on beats.
- Contact sheet (`film.py sheet`): no two neighbouring shots share a composition.
- Then the user runs `/video-review`.
