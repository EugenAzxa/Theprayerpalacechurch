# Build prompt

Create a single-page, cinematic WebGL experience for **The Prayer Palace**, a
multicultural non-denominational church at 1111 Arrow Road, Toronto: a five-chapter
walk from the forecourt at blue hour, up the steps and through the portal, down the
hall to the screen wall, and out through the oculus of the dome into full daylight.
The result should feel like an editorial art book moving through a live 3D world,
not a conventional church landing page.

## Experience

- Use a fixed full-viewport Three.js canvas as the environmental layer.
- Build the palace, forecourt, reflecting pool, avenue, lamps, sky, moon, stars and
  atmosphere procedurally. No model files.
- The building is a palace because the church is called one: a broad limestone mass,
  a portico of six columns over a wide flight of steps, twin towers with lead domes
  at the front corners, and a ribbed dome on a windowed drum over the middle of the
  hall. Put a cross on the lantern and leave the oculus open, because chapter 05
  leaves through it.
- Drive one continuous camera path from page scroll. Each section should feel like
  a new composed shot rather than a hard scene replacement.
- Take the camera inside. Build the room the church actually meets in: a broad
  auditorium, a raked floor of chairs rather than pews, a platform with planters and
  a podium, framed panels down both side walls, and a screen wall that is the
  brightest thing in the building.
- Articulate the drum. Looking up from the floor you are inside it, not under the
  dome, and a bare cylinder reads as a flat disc for a third of the ascent.
- Run one continuous look from blue hour to daylight rather than three separate
  scenes. Sky, fog, lights, moon, exposure, bloom and the page scrim are one config
  per state, interpolated.
- At blue hour a building is darker than the sky. Light pale limestone at full key
  and it comes out at exactly the value of the sky behind it and disappears.
- Add restrained bloom, film grain, vignette, depth haze, warm window light and cold
  moonlight.
- Keep the palette midnight blue, chrome, bone, brand steel-blue and gilt.

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
- Author every scene colour in sRGB and linearise on the way in, because the
  composite pass applies its own gamma. Skipping this renders the night as an
  overcast afternoon.
- Hand-roll the bloom on core Three.js: bright pass, mip chain, separable blur,
  additive upsample, filmic composite. Do not pull in `examples/jsm`.
- Draw the sky first, with the depth test off. A sky is a background, not a distant
  object, and left to the ordinary opaque sort it will paint over the building.
- Swap the interior and the shell rather than cross-fading them, keyed to where the
  camera is rather than to scroll position, and cover the cut with a veil that
  reaches full black. Take the veil from the two surfaces the lens genuinely
  crosses, the portal and the oculus, and from nothing else.
- Clamp the camera above the floor while indoors.
- A metal with no environment map has almost no diffuse term. Gilding that reads
  outdoors under a directional key will render as nothing indoors under point light.
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
