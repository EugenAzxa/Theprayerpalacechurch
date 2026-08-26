# The Prayer Palace

A five-chapter walk into a Toronto church, rendered live in Three.js and layered
with editorial typography: across the car park at blue hour, in through the doors
under the canopy, down the fan of the auditorium to the screen wall, and out
through the rooflight at the middle of the roof into the morning.

The building is modelled on the real one. The Prayer Palace is round: a single very
large storey of split-face concrete block with two dark banding courses and a
ribbed metal fascia, under a shallow faceted cone of a roof, with a plain white
cross above the main doors, Canadian flags on the grass island in front of them,
and concentric radial parking all the way round.

The Prayer Palace is at 1111 Arrow Road, Toronto. It is Canada's first established
multicultural, non-denominational church, founded by the late Reverend Paul
Melnichuk, Kathy and Pastor Tom Melnichuk, with over sixty years in ministry and
more than fifty nationalities in the congregation.

**[Build prompt](PROMPT.md)**

## What it does

- Opens on the main doors, from the point on the drive the street photographs are
  taken from: the canopy sweeping up over the glazed front, the block piers it
  stands on, the raised curve of roof behind it, the cross above that, and the
  flags on the island to the left.
- Walks a live WebGL camera through the building as the page scrolls, outside and
  in: the block drum of the walls, the checkerboard course near the head of it, the
  punched dark glazing, four projecting entrance canopies, the twenty-four ridges of
  the roof, the rooflights and plant scattered over it, and the cross.
- Walks in through the doors rather than through the glass. The doorway is a hole
  cut out of the glazing with a lit lobby behind it and a real opening in the wall
  beyond that, so the approach reads as depth and the camera goes through a passage
  it can actually fit down.
- Takes the camera inside, into the room the church actually meets in. A round
  building gives you a fan rather than a nave: concentric tiers of seating swung
  round a platform on one side, under the underside of the same cone that is the
  roof, with a curved screen wall that is the brightest thing in the building.
- Fills it. Around a thousand people in the seats and a dozen on the platform, as
  heads and shoulders above the seat backs in near black. A room this dark facing a
  screen this bright turns everyone in it into a silhouette, and a silhouette is
  the one form of a person that simple geometry can carry.
- Leaves through the rooflight. The ceiling carries the same twenty-four seams,
  converging on a five-metre opening at the middle that the camera climbs out
  through, past the cross, and up until the whole round of the site is in frame.
- Runs one continuous look from blue hour to full daylight. Sky, fog, four lights,
  the moon, exposure, the bloom and the page scrim are all held in one config per
  state and interpolated, so the world moves from night to glory without anything
  being rebuilt.
- Lays the car park out the way it actually is: a ring road hard against the
  building, a kerbed grass island, then four bands of stalls in concentric arcs
  with drive aisles cut through them, light standards, and the industrial yards
  that surround the site as a low horizon.
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

**A loader that means it.** The plan of the roof, one ring and twenty-four ridges
around the rooflight, drawing itself as the page loads and then opening out to
reveal the scene. It is weighted against work that actually happens: the fonts
resolving, each above-the-fold image decoding, the WebGL library landing, the
scene finishing construction, and the first frame reaching the screen. Between
milestones the ring creeps toward the next one without ever arriving at it, so it
keeps moving without claiming to be finished.

**A fixed canvas.** `position: fixed; inset: 0; z-index: 0`. Everything else floats
over it. The page scrolls, the canvas never moves.

**A camera on a curve.** Thirteen waypoints, a Catmull-Rom through them, and the
scroll mapped onto it. Each chapter owns a stretch of the curve. Smoothstep on its
own puts velocity at zero on every anchor, which is right for a waypoint and wrong
for a chapter boundary: five chapters means four dead stops in what is meant to
read as one walk, so a quarter of the linear term is blended back in to keep the
movement alive across the handover. The camera lags the scrollbar on purpose:
scroll is a step function, and the lag is what turns it into a walk.

**An editorial layer.** Real HTML at `z-index: 10`, revealed by IntersectionObserver,
with headings split word by word into clipping boxes so a line assembles rather
than fading in.

**Post-processing.** Hand-rolled on core Three.js: render to a half-float target,
bright pass into a five-level mip chain, separable blur, additive upsample, and one
composite with a filmic shoulder, vignette, grain and gamma. Nothing comes from
`examples/jsm`, so the site stays at one vendored file. The composite also carries
the veil that covers the two world swaps.

**Two worlds and two doors.** The exterior and the interior are separate groups and
only one is ever drawn. Which one is a radius test against the wall and the roof.
How much to hide is the distance to the surface the lens actually crosses, and
there are only two of those: the doors on the way in and the rooflight on the way
out.

## Things that cost the most time

**Nothing in the scene was ever depth tested.** The single worst bug here, and the
cause of several others. The scene renders into a half-float target for the bloom
chain, and that target was created with `depthBuffer: false` along with the mip
targets, which genuinely do not need one. So the whole world was drawn in
submission order: the ground plane painted over the car park laid on top of it,
and the sky painted over the building standing in front of it. It cost hours
across two different symptoms, and every check pointed the wrong way. A raycast
said the asphalt was the topmost surface at that point, because a raycast tests
geometry and the renderer was testing nothing. Tinting the two surfaces red and
green and rendering one frame is what finally showed it.

**The first symptom of that bug looked like a sky problem.** For several passes the
building simply was not there: clean blue sky where the whole facade should have
been. It was in the frustum, it was visible, a raycast down the middle of the
screen hit it. Forcing the sky to `renderOrder = -1000` with `depthTest = false`
made the building appear, which is correct practice for a skybox and is still in
the code, but it was treating a symptom. The depth buffer was the disease.

**The building was wrong, and only photographs could say so.** The first version of
this scene was a domed limestone palace with a portico and twin towers, built off
the name. The real Prayer Palace is a round single-storey building in split-face
block with a shallow cone for a roof. Nothing about the modelled version survived
the photographs: not the geometry, not the material, not the approach, not the
plan of the room inside it. A generic silhouette read as wrong from every angle,
in exactly the way a five-bay porch invented for a building that has none does.

**Constants declared below the code that reads them are silently undefined.**
`DOOR_PLANE` and `R_IN` sat with the room, a hundred lines under the entrance that
measures the lobby off them. `var` hoisting meant no error, just `undefined`, so
the lobby was built out of NaN and never appeared at all. What showed through the
front doors was the far side of the car park, straight through the building and
out of the opening on the opposite side.

**Cutting a hole in the glass is only half a doorway.** The wall behind it was one
unbroken cylinder, so the opening led to solid blockwork. The wall is built in two
bands now: the lower one in four arcs with a gap at each entrance, the upper one
continuous over the top of them.

**The screen wall was facing the wrong way round its own cylinder.**
`CylinderGeometry` measures theta from +Z, so an arc from -0.46 to +0.46 bulges
toward the camera. The screen was standing in the middle of the room with its back
to the platform.

**A loader shipped at the bottom of the page cannot show you the page loading.**
The first version sat at zero for the entire wait and then jumped to done, because
its own code was behind the 600KB of WebGL library it was supposed to be reporting
on. It runs from its own script tag directly under its own markup now, and the main
script checks in against it.

**Four thousand chairs alias into a flat grey field.** At the distance this room is
seen from, a chair is about five pixels wide, and with antialiasing off that many
bright edges read as one light mass rather than as seating. The rows are modelled
as continuous curved arcs instead. Detail below the threshold is not detail, it is
noise.

**At blue hour a building is darker than the sky.** Pale limestone lit at nearly
full key came out at exactly the value of the sky behind it. The same mistake
appeared again at the other end of the journey, where the glory blew both sky and
stone to the same white. Both ends needed the lights pulled down until the
building sat below the sky rather than beside it.

**A 1px gap over a coloured container is a lovely way to draw a grid** right up
until a row is not full, and then the container shows through as a grey block.
Borders on the cells give the same single-pixel rules with nothing left over.

**A sky sphere sitting exactly on the far plane gets clipped into a visible dome.**
This site is three hundred metres across, so both numbers had to grow.

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
palette, the modelled building and the post chain are original to this project.

## Open items

- The registration forms (baptism, dedication, connect card, hospital notice, serve
  team) link out to the church's existing forms. They need pointing at whatever
  system the office actually wants to receive them.
- The prayer request form composes a message in the sender's own mail client, which
  is the honest behaviour for a site with no backend. A real endpoint would be
  better.
- The modelled building is worked up from aerial and street photographs. The
  proportions, the banding, the entrance canopies and the roof are right; the exact
  bay spacing, the wing layout behind the auditorium and the interior finishes are
  informed guesses. Measured drawings, or a walk round with a camera, would settle
  them.
- Photography in the editorial layer is still limited to what the old site
  published.
