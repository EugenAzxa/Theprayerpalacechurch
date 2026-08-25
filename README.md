# The Prayer Palace

A five-chapter walk into a Toronto church, rendered live in Three.js and layered
with editorial typography: across the forecourt at blue hour, up the steps and
through the portal, down the hall to the screen wall, and out through the oculus
of the dome into the light.

The Prayer Palace is at 1111 Arrow Road, Toronto. It is Canada's first established
multicultural, non-denominational church, founded by the late Reverend Paul
Melnichuk, Kathy and Pastor Tom Melnichuk, with over sixty years in ministry and
more than fifty nationalities in the congregation.

**[Build prompt](PROMPT.md)**

## What it does

- Walks a live WebGL camera through a procedural palace as the page scrolls,
  outside and in: a limestone mass, a portico of six columns over a flight of
  steps, twin towers with lead domes, and a ribbed dome on a windowed drum.
- Takes the camera inside, into the room the church actually meets in: a broad
  auditorium with a raked floor of chairs, a platform with planters, framed panels
  down both side walls, and a screen wall that is the brightest thing in the
  building.
- Leaves through the oculus. The drum is articulated with twelve lit windows and
  twelve pilasters, the dome carries eight meridian ribs and three rings, and the
  camera passes through the 2.4m hole at the top of it into open sky.
- Runs one continuous look from blue hour to full daylight. Sky, fog, four lights,
  the moon, exposure, the bloom and the page scrim are all held in one config per
  state and interpolated, so the world moves from night to glory without anything
  being rebuilt.
- Carries the whole church: service times, what to expect on a first visit, the
  founding family, the prayer of salvation, the memorial to Pastor Paul, and the
  Clarendon rebuild in Jamaica.
- Hands over to four flat pages for the things a church site has to actually do:
  Give, Events, Connect &amp; Serve, and Visit.

## How it is made

A deliberately small static site. `index.html` holds the document structure, the
procedural scene, the scroll choreography and the interaction logic. `site.css` is
shared by all five pages. A vendored Three.js r149 build provides WebGL rendering
with no package manager and no build step.

```
index.html          the home page and the whole scene
site.css            one stylesheet, every page
give.html           generated
events.html         generated
connect.html        generated
contact.html        generated
vendor/three.min.js MIT, copied in
assets/             graded photographs and the brand marks
tools/              the two scripts that produce the above
```

Serve over HTTP. Opened off the disk some browsers will refuse the local font and
image requests:

```
python3 -m http.server 4173
```

`tools/build_pages.py` regenerates the four flat pages from shared partials, so a
change to the phone number or the menu cannot land on three pages and miss the
fourth. `tools/prep_assets.py` regrades the photographs from their sources.

### The five systems

**A fixed canvas.** `position: fixed; inset: 0; z-index: 0`. Everything else floats
over it. The page scrolls, the canvas never moves.

**A camera on a curve.** Twelve waypoints, a Catmull-Rom through them, and the
scroll mapped onto it. Each chapter owns a stretch of the curve and the fraction
within a chapter is smoothed, which puts velocity at zero on every anchor rather
than snapping from a forty-metre stride outdoors to a two-metre one indoors. The
camera lags the scrollbar on purpose: scroll is a step function, and the lag is
what turns it into a walk.

**An editorial layer.** Real HTML at `z-index: 10`, revealed by IntersectionObserver,
with headings split word by word into clipping boxes so a line assembles rather
than fading in.

**Post-processing.** Hand-rolled on core Three.js: render to a half-float target,
bright pass into a five-level mip chain, separable blur, additive upsample, and one
composite with a filmic shoulder, vignette, grain and gamma. Nothing comes from
`examples/jsm`, so the site stays at one vendored file. The composite also carries
the veil that covers the two world swaps.

**Two worlds and two doors.** The exterior and the interior are separate groups and
only one is ever drawn. Which one is a box test. How much to hide is the distance
to the surface the lens actually crosses, and there are only two of those: the
portal on the way in and the oculus on the way out.

## Things that cost the most time

**The sky was painting over the palace.** For several passes the building simply
was not there: clean blue sky where forty-eight metres of limestone should have
been. Every check said it was fine. It was in the frustum, it was visible, a
raycast down the middle of the screen hit the pediment at forty-eight metres. The
sky dome is a 620m sphere with `depthWrite: false`, which should make it harmless,
but left to the ordinary opaque sort it was drawing *after* the building and
passing the depth test anyway. A sky is a background, not a distant object: give it
`renderOrder = -1000` and `depthTest = false` so it paints first and everything
lands on top of it.

**Looking up from the nave, you are inside the drum, not under the dome.** Three
passes went into making the dome ribs read, adding rings, adding a lamp, changing
the gilding. None of it did anything, because the flat disc filling the frame was
the drum wall eight metres below the dome. Tinting each candidate surface a
different flat colour and rendering one frame answered in seconds what an hour of
reasoning had not.

**A metal with no environment map has almost no diffuse term.** The gold ribs read
beautifully outdoors, where a directional key gives them a specular to catch, and
rendered as nothing at all indoors under point light. The interior uses a matte
gilt at `metalness: 0.18` with a little emissive, so it reads as gilding at any
hour instead of disappearing whenever the lamps come down.

**Half the drum windows were facing the wrong way.** They were built from the same
loop as the exterior set and rotated by an extra `Math.PI`, so the room saw their
back faces and the renderer culled them. Twelve light sources, silently absent.

**At blue hour a building is darker than the sky.** Pale limestone lit at nearly
full key came out at exactly the value of the sky behind it. The same mistake
appeared again at the other end of the journey, where the glory blew both sky and
stone to the same white. Both ends needed the lights pulled down until the
building sat below the sky rather than beside it.

**A 1px gap over a coloured container is a lovely way to draw a grid** right up
until a row is not full, and then the container shows through as a grey block.
Borders on the cells give the same single-pixel rules with nothing left over.

**A vertical field of view crops sideways as the viewport narrows,** which on a
phone put the lens inside the building. The shots are composed at 16:9 and anything
narrower widens the angle to hold the same horizontal field.

**Reading matter over a lit scene needs a ground, not a shadow.** A text shadow
works against the night and fails completely against the screen wall. Each column
carries a feathered panel that deepens as the world brightens, driven by the same
`--scrim` the scene sets.

## Verified, not assumed

Driven headlessly at 1440x900, 1024x768 and 390x844, on all five pages: no console
errors, no failed requests, no horizontal overflow. Plus `prefers-reduced-motion`,
where every reveal is visible and nothing waits on a scroll trigger, and WebGL
unavailable, where the canvas is removed and the page stands up as a flat
editorial document with all six thousand characters of it readable.

`?freeze` holds the camera where it is so the scene can be inspected by hand while
the rig keeps running.

## Content and assets

Copy and photographs are the church's own, taken from theprayerpalace.com. The
photographs are cropped away from the promotional type set over them and graded
into the site palette by `tools/prep_assets.py`; the brand marks have their alpha
rebuilt from luminance, because the supplied logo has a black panel baked into it
that it otherwise carries onto every background. Three.js is MIT and vendored
unmodified.

The idiom owes a debt to MengTo's Kage, which publishes a build prompt for exactly
this purpose. No code and no artwork from it is used here: the geometry, the
palette, the palace and the post chain are original to this project.

## Open items

- The registration forms (baptism, dedication, connect card, hospital notice, serve
  team) link out to the church's existing forms. They need pointing at whatever
  system the office actually wants to receive them.
- The prayer request form composes a message in the sender's own mail client, which
  is the honest behaviour for a site with no backend. A real endpoint would be
  better.
- Photography is limited to what the old site published. Proper exterior
  photographs of 1111 Arrow Road would improve the editorial layer, and would let
  the modelled palace be checked against the real building.
