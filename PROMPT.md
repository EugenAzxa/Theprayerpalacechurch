# Build prompt

Create a single-page, cinematic WebGL experience for **The Prayer Palace**, a
multicultural non-denominational church at 1111 Arrow Road, Toronto: a five-chapter
walk from the car park at blue hour, in through the doors under the canopy, down
the fan of the auditorium to the screen wall, and out through the rooflight at the
middle of the roof into the morning. The result should feel like an editorial art
book moving through a live 3D world, not a conventional church landing page.

**Model the building that is there, not the one the name suggests.** Work from
aerial and street photographs before writing any geometry. This one is round.

## Experience

- Use a fixed full-viewport Three.js canvas as the environmental layer.
- Build the church, the car park, the landscaping, the lamps, sky, moon, stars and
  atmosphere procedurally. No model files.
- The building is one very large storey of split-face concrete block, circular in
  plan, with two dark banding courses and a ribbed metal fascia, under a shallow
  faceted cone of a roof with about twenty-four ridges running from the eaves to the
  middle. Punched openings of dark tinted glass right round it. Four projecting
  entrance canopies with white metal roofs over glazed fronts, the one at the front
  wider than the rest. A plain white cross on the roof above it. Canadian flags on
  the grass island at the door.
- Leave a rooflight at the middle of the cone, because chapter 05 climbs out
  through it.
- Lay the car park out the way it is: a ring road hard against the building, a
  kerbed grass island, then bands of stalls in concentric arcs with drive aisles cut
  through them, light standards, and low industrial buildings on the horizon.
- Open on the main doors, from the point on the drive the street photographs are
  taken from. That view is the one people recognise, so give it the first chapter
  and keep the approach clear: no lamp post on the axis of the entrance, and the
  trees flanking the doors rather than standing in front of them.
- Walk the finished flight frame by frame at a couple of dozen stops and fix what
  you find. The shots you composed will be fine; the empty ones are always the
  handovers between them, where the lens is pointed at a floor, a ceiling or a
  rectangle of sky that nobody chose.
- Drive one continuous camera path from page scroll. Each section should feel like
  a new composed shot rather than a hard scene replacement.
- Take the camera inside. A round building gives you a fan, not a nave: concentric
  tiers of seating swung round a platform on one side, a podium and planters, and a
  curved screen wall that is the brightest thing in the building. The ceiling is the
  underside of the same cone, carrying the same seams, converging on the rooflight.
- Put one person on the screen wall and let the room look at him. Nobody at the
  back of a hall this size sees a face; they see the screens. The single figure on
  the platform should be small and distant, which is what it actually is.
- Put the congregation in it as drawn cut-outs, not as geometry. Primitives cannot
  carry a person at any proportion: what is missing is the neck, the slope from
  trapezius to deltoid, and the fact that no two people in a room share an outline.
  Draw a handful of silhouettes with those three things, alpha test rather than
  blend them so they keep early-z, and fix them facing the platform rather than
  billboarding them at the camera.
- Tint every one of them separately, and draw the atlas light enough that the tint
  has somewhere to go. A dozen shapes in one tone is still a pattern: what tells one
  person from the next across a room is not the outline, it is that they are not
  wearing the same thing.
- Check the seat backs against the people. A back that stands a metre above its own
  tier leaves a seated person showing two hundred millimetres of scalp.
- Model the seating as continuous curved rows. At the distance the room is seen
  from a chair is about five pixels wide, and several thousand of them alias into a
  flat grey field rather than reading as seating.
- Run one continuous look from blue hour to daylight rather than three separate
  scenes. Sky, fog, lights, moon, exposure, bloom and the page scrim are one config
  per state, interpolated.
- At blue hour a building is darker than the sky. Light pale blockwork at full key
  and it comes out at exactly the value of the sky behind it and disappears.
- Add restrained bloom, film grain, vignette, depth haze, warm window light and cold
  moonlight.
- Keep the palette midnight blue, chrome, bone, brand steel-blue and gilt.
- Give the scene's render target a depth buffer. The bloom mips do not need one and
  it is easy to create them all from the same helper, at which point nothing in the
  world is depth tested and everything draws in submission order: the ground paints
  over the car park, the sky paints over the building, and every symptom points
  somewhere else.

## The loader

- Give it a figure that belongs to this building rather than a spinner. The roof
  plan works: one ring, twenty-four ridges, the rooflight at the middle, drawing
  itself in and then opening out to reveal the scene. It is the same figure the
  last chapter leaves you looking down at.
- Weight it against work that actually happens, not a timer: fonts resolving,
  images decoding, the library landing, the scene built, the first frame drawn.
- Run it from its own script tag under its own markup. Shipped at the bottom with
  everything else it will not execute until the library it is reporting on has
  already arrived, and it will sit at zero for the whole wait and then jump to done.
- Let it creep toward the next milestone between milestones so it keeps moving,
  and cap that creep short of complete so it never lies.

## Layout

- Structure the page as forecourt, threshold, sanctuary, the word, the ascent, and
  then a practical zone on paper: times, address, and where to go next.
- Use oversized serif headings, small technical labels in mono, chapter numbers,
  fine rules and generous negative space.
- Layer graded photographs of the church into editorial cards, and flat SVG
  silhouettes at the bottom of the active viewport.
- Foreground layers should arrive at full opacity, remain pinned while their section
  is active, then fade and blur away during the handoff.
- Carry the practical church underneath: service times, first-visit information, the
  founding family, the prayer of salvation, the memorial, and the missions work.

## Motion

- Reveal headings word by word and supporting elements individually.
- Use slow, precise section transitions, subtle parallax and eased camera
  interpolation.
- Let the navigation, chapter rail and foreground layers respond to the active
  section from one shared source of truth.
- Include reduced-motion behaviour that preserves the complete reading experience.

## Interaction and quality

- Provide working anchor navigation, mobile navigation, responsive layouts, semantic
  landmarks and accessible labels.
- Keep runtime assets local and use relative paths.
- Author every scene colour in sRGB and linearise it on the way in, because the
  composite pass applies its own gamma. Do not trust a colour-management flag to do
  this for you: measure one known colour after setting it and check the stored value
  is the linear one. If it is not, every dark surface in the scene is several times
  too bright and no amount of relighting will fix it.
- Hand-roll the bloom on core Three.js: bright pass, mip chain, separable blur,
  additive upsample, filmic composite. Do not pull in `examples/jsm`.
- Draw the sky first, with the depth test off. A sky is a background, not a distant
  object. Keep its sphere well inside the far plane, or it is clipped into a visible
  dome.
- Walk in through the doors, not through the window. Cut the doorway out of the
  glazing, cut a matching opening in the wall behind it, and put a lit lobby
  between the two. A veil over a lens travelling through a sheet of glass is
  hiding a mistake rather than making a transition.
- Declare every dimension the building is measured off above the code that reads
  it. Hoisting means a constant used before its declaration is `undefined` rather
  than an error, and geometry built out of NaN does not appear at all.
- Swap the interior and the shell rather than cross-fading them, keyed to where the
  camera is rather than to scroll position, and cover the cut with a veil that
  reaches full black. Take the veil from the two surfaces the lens genuinely
  crosses, the doors and the rooflight, and from nothing else.
- Clamp the camera above the floor while indoors.
- A metal with no environment map has almost no diffuse term. Anything that reads
  outdoors under a directional key will render as nothing indoors under point light.
- `CylinderGeometry` measures theta from +Z. An arc meant to stand behind the
  platform will otherwise bulge toward the camera with its back to the stage.
- Give reading matter over a lit scene a ground of its own. A text shadow works
  against the night and fails against the screen wall, and this page has both.
- Hold a constant horizontal field of view. A vertical one crops sideways as the
  viewport narrows and puts the lens inside the building on a phone.
- Watch fill rate, not triangle count: cap the pixel ratio, start the bloom chain
  low, and keep backdrop-filters off anything that repaints while scrolling.
- Survive a WebGL failure: remove the canvas and keep the page readable as a flat
  editorial document. Feature-detect first, so a machine without WebGL gets a quiet
  document rather than a console full of red.
- Avoid frameworks, build tooling, analytics, trackers, placeholder imagery, generic
  glassmorphism, excessive glow, em dashes, emoji, and decorative motion without
  narrative purpose.
- Verify at desktop, tablet and approximately 390 x 844: check every asset for
  404s, parse every inline script, inspect the console, confirm no horizontal
  overflow, and test one complete scroll and navigation interaction before shipping.
- When a surface looks wrong, tint each candidate material a different flat colour
  and render one frame. It answers in seconds what guessing does not answer in an
  hour.
