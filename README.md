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

- Follows the calendar and the clock. The car park is in spring, summer, autumn or
  winter by date and in day, dusk or night by hour, changing the foliage, the grass,
  the snow on the ground, the sky, the fog, the stars, the lamps in the lot, the
  light behind the glass and the weather falling through it. The room does not
  change, because a hall with no windows in it is the same at every hour of the
  year, and pretending otherwise is a lie the building itself would contradict.
- Runs one particle field for every season: snow, rain and a summer night's insects
  are the same points with different speed, size, colour and sway, and a negative
  fall speed is what turns snow into insects drifting up. It wraps about the lens on
  all three axes and fades out as the lens goes indoors.
- Carries pickers for both in the hero, and `?season=` and `?time=` for a direct
  link. A change is a two second dissolve, because nothing differs structurally
  between the states: every value on either side is a colour or a scalar.
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
- Fills it. Around a thousand people in the seats, as drawn cut-outs rather than as
  geometry, thinning toward the front and the back and never solid.
  A room this dark facing a screen this bright turns everyone in it into a
  silhouette, and a silhouette is the one form of a person that simple geometry can
  carry. The camera runs down the centre aisle, above head height, so nobody in the
  congregation is ever close enough to the lens to be examined.
- Puts one person on the screen wall. Nobody at the back of a room this size sees a
  face, they see the screens, so the one person on this page rendered as a
  photograph rather than as geometry is the one the room is actually looking at,
  and he appears where the room looks at him. The platform itself carries a single
  distant figure, which is what you would actually see.
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
- Closes on Saylavy, back on a dark ground: what this house keeps (sermons,
  testimonies, the record, the knowledge of the faith), the interactive page with a
  QR code in the hall, the four things Saylavy keeps for a church, and a working
  demonstration of the memory wall with filters. Six fictional people, marked as
  fictional in a notice nobody can miss, because a demonstration that reads as a
  real congregation is a lie about the dead. Each page counts prayers rather than
  candles, and the prayers are offered for the family rather than for the person
  who has died: this church is evangelical, and a candle lit for the departed is
  not its practice. No selling language, and a plain statement that a page is not
  what earns remembrance.

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

**A grade and a lens.** What separates a render from a photograph is mostly not the
geometry. The composite carries a depth of field driven off the scene's own depth
buffer, with the focus plane pulled to whatever the camera is looking at, so the
subject of the shot is sharp and everything else falls away; a split tone that cools
the shadows and warms the highlights; halation, which runs the bloom warm the way
light scattering behind film does; a horizontal spread on the bloom, which is the one
cue that reads as a lens rather than as a gaussian; and a little chromatic aberration
that grows off-axis, because a real lens does not focus every wavelength on the same
spot.

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

**Setting `ColorManagement.enabled = true` did not do what the flag says.** This was
the single most expensive thing here, because it made every other judgement wrong.
On this build `Color.setHex` stores the sRGB value as-is rather than converting it
into the linear working space, so every one of the forty-odd authored colours in
the scene was being used between three and twelve times too bright in the shadows.
Nothing dark would stay dark. Weeks of a real project could go into relighting
around that. It was settled in one measurement: `setHex(0x151a28)` came back as
0.082, 0.102, 0.157 where the linear value is 0.007, 0.011, 0.022. Every authored
colour now goes through one helper that converts explicitly, and the whole rig was
relit afterwards. The lesson is not about three.js: it is that a flag whose name
describes an outcome is not evidence the outcome happened.

**A screen nine metres tall does not fit under a roof eight and a half metres up.**
The wall was built to a size that looked right in isolation, and its top third was
inside the roof cone, so what showed in the room was a screen cropped through the
middle of the pastor's face. Worth checking any large flat thing against the
surface above it rather than against its own proportions. Its plate also has to be
authored at the aspect the geometry actually is, or the face is stretched across
the wall.

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

**A congregation cannot be built out of primitives, and proportions do not save
it.** A capsule with a sphere on top is a skittle. Correcting the head-to-shoulder
ratio to the anatomical third helped and was still a skittle, because what is
missing is the neck, the slope from trapezius to deltoid, and the fact that no two
people in a room have the same outline. They are drawn silhouettes now, sixteen
variants in one atlas, with collars, sleeve seams, hair that is not a larger head,
tilts, leans and a few raised hands, and every one of them dressed from a
wardrobe of eighteen: charcoal, black and navy for most of the room, grey, tan,
brown, olive, burgundy and teal filling in, cream and pale blue for the few the eye
picks out. The colours are authored as clothes you could name and then muted into
the room, because a hall lit only by its stage does not contain postbox red. That
mattered more than all the drawing: sixteen shapes in one tone is still a pattern,
because what tells one person from the next at forty metres is not the outline, it
is that they are not wearing the same thing. alpha tested rather than blended so they keep early-z, and
fixed facing the platform rather than billboarded at the camera: a congregation
that swivels to follow the lens is worse than one seen slightly off axis. The seat
backs came down from 1.13m to 0.87m at the same time, because at the old height a
seated person showed about two hundred millimetres of scalp.

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

**An exponential approach never arrives.** The camera lag is a lerp toward the
scroll target, which halves the remaining distance forever and never closes it, so
the camera was still creeping by fractions of a pixel long after it looked
stationary. On the highest contrast edge in the frame, with bloom and a defocus
over it, that reads as a flicker: the lit doorway flashed against its dark frame
for as long as the page was open. It stops when the remainder is smaller than
anyone could see. The same applies to the focus pull and the season dissolve.

Worth saying how it was found, because the obvious test was the wrong one.
Diffing consecutive frames while scrolling shows enormous change, all of it
legitimate motion, and tells you nothing. Holding the camera still and diffing
over time isolates what actually flickers, and the answer was a single hard-edged
rectangle around the doors.

**A wide lens holds almost everything.** The first depth of field pass ramped
straight out of the focus plane, which put the whole congregation out of focus: that
is a portrait lens in a ninety metre hall. There has to be a band either side of the
focus distance that stays sharp before anything softens. The grade needed the same
restraint, having started as a boost rather than a bias and pushed the building
through the top of the filmic curve until it was white.

**`antialias: true` does nothing to a render target.** The single largest thing
wrong with how this looked, and it hid for the whole build behind art-direction
problems it was actually causing. The renderer flag only ever touches the default
framebuffer; the world here is drawn into a half-float target for the bloom
chain, so nothing in the scene was ever antialiased. Every edge of the building,
every seat back and every one of a thousand people was crawling, and no amount of
relighting or reshaping was going to fix it. The setting has to go on the target,
as `samples: 4`, which needs WebGL2. It costs nothing measurable: 61fps at device
pixel ratio 2 in the fullest shot in the room.

**Film grain applied flat lands hardest where there is nothing to grain.** At a
constant amplitude the noise is a couple of per cent of a midtone and a quarter of
a deep shadow, so the darkest parts of a night scene are the noisiest. Weighted by
luminance it reads as film; unweighted it reads as dirt.

**Clamp the camera against the floor it is actually over.** The rake rises three
and a half metres from the platform to the back wall, so a clamp that only keeps
the lens above `FLOOR_Y` leaves it inside the back rows: a waypoint set by eye at
5.6m sat half a metre below the heads of the row it was flying over, and the shot
was the inside of the crowd. The clamp now reads the rake at the camera's own
distance from the platform, which makes it impossible to set a waypoint that
buries the lens. The rake itself was also written out in three places at a
coefficient that lifted the back row six and a half metres, which is a stadium
rather than a church; it is one function now.

**A fifty-two degree lens in a ninety metre room spends a third of every frame on
ceiling.** Measured rather than argued: at the wide interior shot the ceiling was
37% of the frame height, and it was decorated with a radial star of high-contrast
seams and fifty-two glowing spheres, so the most prominent thing in the middle
three chapters was a graphic pattern on a surface nobody was looking at. The lens
is 42 degrees now, which is an ordinary cinematic one, the seams are structure
rather than decoration, and there are twenty-four lights instead of fifty-two.

**Point the camera at the subject, not at the exit.** The climb out used to look
straight up, so four of twenty-four frames were a blank cone and a flat disc. It
cranes up looking back down the room instead: the congregation falls away
underneath the whole ascent and the roof arrives as something seen from above,
which is both a better shot and one that never has nothing in it.

**A room is only as full as its worst frame.** The seating fan stopped
twenty-eight metres short of the back wall, so entering the sanctuary put the
lens behind an empty plain and two whole frames of the walk were bare floor with
the room squeezed into a strip at the top. The fan runs further back now, the
round plan clips its own corners, and the circulation behind it has the
production desk, the rail and the people standing at both that a hall this size
actually has. Worth walking the whole flight frame by frame rather than checking
the shots you designed: the weak ones are always the handovers nobody composed.

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

**A rake needs a deck and a face.** Thirty-four rows rise three and a half metres and
then the floor dropped straight back to grade, so the bank had no back to it: the
people who stand behind the rail floated over a four-metre void, and past that a
fourteen-metre apron of bare carpet ran to the wall. Coming through the doors the
lens crossed all of it, and the bottom half of the frame was lit floor. A raked bank
is a raised deck with a riser closing it, and the apron in front of that is a cross
aisle, not the subject of the shot.

**No waypoint should rest anywhere there is nothing to look at.** Waypoints are
spaced evenly in the curve parameter however far apart they sit, so one placed on
the apron spends the same slice of the scroll there as one placed on the platform.
Two of them sat on it. Removing them crosses the same ground in a couple of frames.

**Do not fly down the aisle.** An aisle is a three-metre strip of empty carpet
pointed at the stage, which is exactly where the lens was, so it ran at the camera
for the whole approach with the congregation as a thin band above it. Held over the
seating with the aisle to one side, the frame fills with people, and the walk stops
being symmetrical, which is the better shot anyway.

**A filled panel over the scene is a sheet of grey glass laid on the room.** The
service times sat in a translucent box whose hard edge cut across the sanctuary
wherever the column happened to end. The column already carries a ground; the list
only needed rules.

**`MeshNormalMaterial` as `scene.overrideMaterial` measures a composition in one
frame** - what share is floor, what share is ceiling, what share is the thing you
came to see. It answered in a minute what an hour of looking did not. Set
`side: DoubleSide` on it, or every surface you are standing inside is culled and a
closed room reads as empty space.

**Raycasting names geometry, not pixels.** It reported the floor under the pale
field, and the field was still there with the floor painted black. Hiding objects
one at a time and measuring the frame is the attribution that holds; the raycast is
a hypothesis.

**Puppeteer's screenshot `clip` is in page coordinates, not viewport coordinates.**
Sampling a scrolled page reads the top of the document instead, silently, and every
measurement comes back identical - which looks exactly like a variable that has no
effect.

## Verified, not assumed

Driven headlessly at 1440, 1024, 768, 390 and 375 wide, on all five pages: no console
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
- The Saylavy section points at `https://saylavy.com/memory-page`. If the route
  changes it is one edit, in `index.html` and in the footer of `tools/build_pages.py`.
