# Manim Notes

Implementation notes collected from past issues.

This file contains Manim-specific bugs, API limitations, and solutions.
Do not add general design rules here.

---

# Animation

## DecimalNumber + updater

Avoid adding live updaters before FadeIn/Write animations.

`DecimalNumber.set_value()` can change internal subobjects when digit count changes, causing animation interpolation errors.

Preferred:
- Set initial value.
- Add updater.
- Add object directly.

---

## TracedPath

When using `TracedPath`:

1. Update the tracked object position once.
2. Then attach TracedPath.

Otherwise the first frame may contain an incorrect line from the default position.

Animating a `VGroup` that contains a live-updating `DecimalNumber` (via
`.animate.move_to(...)`, `.animate.scale(...)`, etc.) hits the same
zip-length crash if the number's value — and therefore its glyph count —
changes *during that same animation* (e.g. a sign flips, adding/removing a
"-"). The animate call snapshots the group's family structure at the start
and end; if the updater changes that structure mid-flight, the two
snapshots disagree and interpolation crashes with `ValueError: zip()
argument 2 is shorter than argument 1`. Fix: don't animate the group at the
same time as whatever drives the updater's value through a glyph-count
change. Split into two sequential `self.play` calls — finish the value
change first (so the number's glyph count is stable), then animate the
group on its own.

`TracedPath` keeps recording every frame for as long as it (and its internal
updater) stays in the scene — including during an unrelated "reset the
tracker back to 0" animation played later. A short reset animation covering
a large value range gets sampled at very few frames, so it retraces the
curve backward as a coarse, jagged polyline that visually overlaps the
original smooth curve. Call `traced_path.clear_updaters()` once the curve is
meant to be finished, before playing any animation that moves the tracked
object again for a different purpose (e.g. a replay/rewind).

---

# Text

## CJK text in `MathTex`

`MathTex` compiles its string through LaTeX; the project's LaTeX setup has
no CJK font, so any CJK characters inside a `MathTex` string (even wrapped
in `\text{...}`, e.g. `MathTex("\\text{<a CJK word>} \\rightarrow
\\text{<another CJK word>}")`) fail with `ValueError: latex error
converting to dvi`. Use `Text(...)` for any label containing CJK text -
including a mix of CJK words and a unicode arrow ("→") - and reserve
`MathTex` for pure math/Latin content (formulas, units, single variable
names). A label that mixes a short CJK phrase with a formula should be
built as two separate mobjects (a `Text` and a `MathTex`), not one
`MathTex` string. (This project's content is now all-English, so this
mainly matters if CJK text is ever reintroduced.)

## CJK `Text` width

`Text` has no automatic line-wrapping. Before placing a Japanese (or mixed
Japanese/Latin) line at a fixed screen position, measure its actual
`.width` at the intended `font_size` — don't guess from character count.
A line that looks like it should fit can overflow past the frame edge by a
wide margin; check `Text(...).width` against the available screen space
first, and pick font_size/position from that, not the reverse.

# Mobjects

## Line

Use:

```python
put_start_and_end_on()
```

Do not use nonexistent methods such as `put_start_and_end_points`.

## NumberLine

Avoid rotating existing NumberLine objects.

Create a new NumberLine with the desired orientation and use Transform.

A rotated NumberLine's own tick numbers sit just off one side of its line
for its entire length — not only near wherever an object on it currently is.
A live label placed via `next_to(moving_object, UP/DOWN/...)` will collide
with those numbers at most positions along the line, since "next to the
object" is usually also "next to the axis's own number column". Give such a
label a fixed screen position instead (like a timer readout), rather than
attaching it relative to an object that moves along a labeled axis.

This "don't rotate, rebuild + Transform" rule is really about any
*structural* change, not just rotation: `Transform(old_axis, new_axis)`
between two NumberLines of **different lengths** (same rotation, ticks and
numbers already attached to both) visibly warps/tilts the number glyphs
mid-animation too — Transform interpolates points without regard for
whether the two glyph sets correspond to the same subdivisions. Changing
only *position* (a pure shift/translate, same length) is safe to Transform
or `.animate.shift(...)` directly. Changing *length* (compressing/
stretching an axis while keeping its numeric range) needs the same
detach/stretch/regenerate technique already used for extending a range:
save `axis.ticks`/`axis.numbers`, `axis.remove(...)` them, animate only the
bare line via `.animate.put_start_and_end_on(new_start, new_end)`, then
`axis.add_ticks()` / `axis.add_numbers()` and reveal via a plain
`set_opacity` animate (never `FadeIn` on the regenerated children — see
above). `add_numbers(excluding=[...])` accepts an explicit exclude list
directly, useful when compressing an axis enough that its usual tick
density would overlap illegibly (same values, just fewer printed).

## Live plotting without ever pausing

To mark points on a live-plotted curve (e.g. zero/max/min-velocity
moments) *without* stopping the plotting animation to do it: don't use a
sequence of `self.play(move to event) -> self.play(FadeIn marker)` pairs —
that's what stops the motion. Instead, attach an updater to an invisible
throwaway mobject (e.g. `Dot(radius=0)`) that checks the driving
`ValueTracker`'s current value each frame against a queue of pending
events, and calls `self.add(...)` directly (not `self.play`/`FadeIn`) the
instant an event's threshold is crossed. Run the whole pass as one
continuous `self.play(tracker.animate.set_value(end), rate_func=linear)`;
markers pop in on their own mid-flight. `self.add()` from inside an
updater is safe — it's the same call any construct() body makes.

## An object riding along an axis transform

When an object's position is driven by `track.number_to_point(get_x())`
inside an updater (e.g. `common.position_track.make_tracked_face`), and
`track` is later reshaped/moved in place via `.animate.put_start_and_end_on(...)`
(not replaced with a new mobject), the object smoothly follows the
transform for free - the updater re-reads the same (mutated) track object
every frame, so no separate "move the object too" animation is needed.
Keep the object's updater attached (and its driving value fixed, e.g. a
`ValueTracker` left resting at its current value) through the axis's own
`.animate` call.

## Progressive multi-row graph stacks fit without a camera zoom

Stacking several compact graphs (e.g. x-t/v-t/a-t) below a shared face
axis doesn't need `MovingCameraScene`/camera zoom if the row positions are
sized up front to fit the whole final stack inside the standard frame
(check the top row's top and the bottom row's bottom against
`config.frame_height`/2 with margin for axis labels). Reveal rows by
fading each one in as its own beat progresses; only reach for a real
camera zoom when the *scale* genuinely needs to change (e.g. a big
full-screen single axis compressing into a small multi-row slot).

## Decluttering a `MovingCameraScene` zoom

When zooming a `MovingCameraScene` into a small region, anything not
central to that beat (an axis's own tick numbers, marker text labels
already read earlier, a long connector line that happens to pass through
the zoomed area) reads as clutter at the magnified scale even if it looked
fine zoomed out. Fade such elements to `opacity=0` in the same `self.play`
as the zoom-in, and back to `opacity=1` in the same `self.play` as the
zoom-out — cheaper and less error-prone than removing/recreating them.

## Chained `camera.frame.animate.scale()` calls compound

`self.camera.frame.animate.scale(k)` multiplies the frame's *current*
size by `k` - it is relative, not absolute. Zooming in twice in the same
scene (e.g. "zoom onto this graph" then, later, "zoom further into one
segment of it") with two independent `scale(k1)` / `scale(k2)` calls
produces a true zoom level of `k1*k2`, not `k2`. Any absolute-position math
done against the *second* zoom's expected frame size (deciding how far a
label can sit from center before it's clipped, an offset meant to land a
brace's label just inside the visible edge, etc.) will be wrong by a factor
of `k1` and clip content that looks like it should fit. Track the intended
*absolute* scale (relative to the default, un-zoomed frame) as its own
named constant, and compute each `scale()` call's argument as
`target_absolute_scale / current_absolute_scale` - never chain relative
factors from memory.

## `Text` can silently drop a bare ASCII letter next to CJK

A `Text(...)` string mixing CJK characters and a single bare Latin letter
as a "variable name" embedded mid-sentence (e.g. a CJK sentence like
"Solve (1) for t:" with the bare `t` inline) can render with that letter
effectively invisible - not an error, just a blank gap where it should be,
easy to miss at low preview quality. Fix by not embedding a bare Latin
variable inside a CJK `Text` string at all: keep the sentence pure CJK and
let the adjacent `MathTex` (which you already need for the real formula,
per the mixed-content rule above) carry the variable instead.

## Absolute-coordinate text placement inside a zoomed camera

When placing text at a fixed absolute coordinate while a `MovingCameraScene`
is zoomed in, don't eyeball/mentally estimate the actual value of the zoom
center (a constant written as a nested expression like `GRAPH_CENTER`) -
always compute and verify it. The visible range is
`center ± (frame_height/2, frame_width/2) * scale`, and misreading the
center coordinate (e.g. mistaking `ORIGIN_Y + 1.7` for plain `1.7`) raises
no error until you actually render - it only shows up as the top of the
frame getting clipped. Frame extraction + visual inspection catches this.

## z-index for keeping something in front

An object that moves across connector lines/background elements (e.g. 😁)
isn't guaranteed to stay in front just from `self.add` ordering. Explicitly
call `set_z_index()` on any object that must stay on top.

## A text background rectangle can fail to hide an existing graph line (important - took a long time to isolate)

Adding a background rectangle behind text that overlaps a graph line/curve,
in order to keep the text readable, can fail **if the rectangle is added as
an animation** (e.g. `self.play(FadeIn(bg), ...)`) - the rectangle itself
renders at the correct position/opacity and correctly sits behind newly
written text, but a line that already existed in the scene (a straight
graph line, a `TracedPath`, etc.) inexplicably ignores the rectangle and
shows through in front of it. Explicitly setting z_index on both the
rectangle and the text doesn't fix it. This reproduces in both `Scene` and
`MovingCameraScene`, and with both `BackgroundRectangle` and
`SurroundingRectangle` (isolated by comparing many variants in standalone
repro code).

Reliable workaround: add the background rectangle **with `self.add(...)`
immediately, not `self.play(FadeIn(...))`, and set its opacity to `1.0`**
(not semi-transparent). The text itself can still be animated with
`Write`/`FadeIn`. Since the rectangle's color matches the scene background,
opacity 1.0 looks identical to semi-transparent wherever there's nothing
behind it (there was never a visual benefit to translucency anyway).

```python
bg = layout.make_text_bg(text)  # already follows this procedure internally
self.add(bg)
self.play(Write(text), ...)
```

This topic's `layout.make_text_bg` bakes in both this procedure and an
explicit z_index setting (as a safeguard). If you write a new background
rectangle by hand, follow the same procedure (`self.add`, opacity 1.0).

Also, when the line behind it is a `TracedPath`, this alone may not be
enough - see "Converting a settled TracedPath to a VMobject" below.

## Converting a settled TracedPath to a VMobject

A `TracedPath`, even after its updates are finished and it's left on screen
only as a static record, can still fail to be correctly covered by an
opaque rectangle added afterward - even combined with `self.add(bg)` and an
explicit z_index (this is a separate, `TracedPath`-specific draw-order issue
from the background-rectangle problem above). Once the curve is fully drawn
and only needs to remain as a static reference, convert it to a plain
`VMobject` with the same point data, then remove the `TracedPath`, to avoid
this issue.

```python
frozen = VMobject(stroke_color=traced_path.stroke_color, stroke_width=traced_path.stroke_width)
frozen.set_points(traced_path.get_points())
scene.remove(traced_path)
scene.add(frozen)
```

This topic's `layout.freeze_traced_path(traced_path)` performs this
conversion.

# Layout

Shared coordinates

When multiple scenes share a layout:

- Put constants in common/.
- Do not copy coordinates between scenes.

# Rendering

Before finalizing:

- Render a preview.
- Check beginning, middle, and end frames.
- Also check frames at specific timings where a transition looks suspect:
  confirm the total frame count with `ffprobe`, then extract with something
  like `ffmpeg -vf "select='eq(n,N)'" -vsync 0` and inspect visually. Some
  bugs (zoom-range clipping, overlapping labels) aren't visible from the
  begin/mid/end frames alone.

Verify:

- no object jumps
- no overlap
- no unexpected disappearance

# Debugging

When rendering appears stuck:

- Check actual process status.
- Use unbuffered output if running in background.
- Confirm whether Manim crashed instead of assuming it is running.

## Stale partial movie file cache

Manim's `media/videos/.../partial_movie_files` cache keys each `self.play(...)`
call by its Animation class + parameters (run_time, rate_func, mobject count,
etc.) — not by the actual mobject geometry/state at that point. On a project
where the same scene file gets edited and re-rendered many times in one
session, an unrelated later edit can produce a `self.play` call whose hash
happens to match one cached from an *earlier* version of the code, and Manim
silently splices in that stale cached clip instead of re-rendering the
current mobject state. Symptom: a curve/element that's clearly present in
the current code appears missing, frozen, or wrong for exactly one segment
of the video, with no error raised. Confirm by re-rendering the same scene
with `--disable_caching` (or after deleting `media/`) and comparing — if the
"bug" disappears, it was a stale cache, not a code defect. During heavy
iterative development of a single scene file, prefer `--disable_caching` (or
periodically clear `media/`) so this never masks (or fakes) a real bug.