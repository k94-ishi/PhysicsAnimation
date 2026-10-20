# Acceleration and Uniformly Accelerated Motion - Storyboard (Revision 6 - 4th round of video review)

Breaks the content of `concept_map.md` -> `teaching_plan.md` down to
implementation-ready detail. General principles (teaching approach,
forbidden patterns) live in `docs/physics_teaching_principles.md`; color,
icon, and camera-work conventions live in `docs/visual_language.md`.
This file records only the layout, numeric values, and per-Beat
instructions specific to this topic.

Revision 6 reflects the 4th round of review feedback on the already-
implemented video. The changes are folded into each Scene's description.
Shared fixes are summarized in the next section (pure layout tweaks, like
fixing a graph title overflowing the screen, aren't recorded here).

## Purpose

Building on the position, x-t graph, v-t graph, and the relationship
between graph slope and velocity learned in the previous lesson ("How to
Express Motion"), visually understand acceleration, what the v-t graph's
slope means, uniformly accelerated motion, and the derivation of its
formulas. The emphasis is on letting the formulas emerge naturally from the
correspondence between the graphs and the motion, rather than memorizing
them (see `teaching_plan.md`).

---

# Implementation approach specific to this topic

## Layout

The baseline composition matches the previous video
(mechanics_how_to_express_movements).

- "😁" moves up and down a vertical position axis on the left (except in
  Scene7, where it sits at the far left).
- The x-t graph shares the same height scale as "😁"'s vertical axis and is
  connected to it with a horizontal dotted line. Don't force a dotted
  connection to the v-t graph (or a-t graph) - show that sync through
  motion timing alone.
- The v-t graph (and a-t graph, where present) stacks below the x-t graph
  (except in Scene7, where 😁 -> x-t -> v-t sit side by side instead).
- When showing multiple graphs, align them on the same t-axis scale and the
  same horizontal position.
- When showing multiple graphs, stack a short title ("x-t graph," "v-t
  graph," "a-t graph") above each axis's single-letter label (x, v, a)
  (`layout.make_graph_title`).

## Persistent objects

"😁", the vertical position axis, the x-t graph, the v-t graph (and a-t
graph where present), the time display. Since each Scene renders as its own
independent file, "persistence" is reproduced by rebuilding the previous
Scene's end state in place.

## ValueTracker

t, x, v, a (kept as a shared interface even in Scenes that don't use all of
them)

## Concrete numeric values used in this video

- Main example (Scenes 1-3, 6, 7): v0=0, a=2 m/s²
- Scene4's contrasting example: v0=0, a=4 m/s² (clearly distinct from the
  main example)
- Scene5: extends the main example's t-axis to 0-4 (v(4)=8, x(4)=16). The
  v0≠0 repetition uses the same values as Scene6.
- Scene6's general example: v0=1.0 m/s, a=2 m/s² (matches the main
  example's a), t: 0-2s

## Fixes common to all Scenes (from the 2nd round of video review)

- **Keep "😁" in front of lines** (round 1): `layout.make_tracked_face` sets
  the z-index automatically.
- **Don't force a dotted connection where it doesn't belong**: there's no
  need to connect "😁" to the v-t/a-t graph, or the x-t graph to the v-t
  graph, with a dotted line. Show sync through motion timing alone. Only
  connect "😁" to the x-t graph (since they share the same value and the
  same vertical axis).
- **Don't draw a tangent on a straight line**: a tangent line exists to show
  "a curve's instantaneous slope," so don't show one when the graph is
  already straight (e.g. the x-t graph of constant-velocity motion).
- **Don't overlap text with graph elements**: place labels, titles, and
  formulas where they don't overlap the axes, curves, or other labels. When
  overlap is unavoidable, use `layout.make_text_bg` to put a
  background-colored rectangle behind the text for readability.
- **Don't reveal multiple "="s at once**: an equation containing multiple
  "="s should reveal one "=" at a time, dynamically.
- **Draw text and formulas with `Write`**: entrance animations should
  default to `Write` rather than `FadeIn` (shapes, dots, rectangles, etc.
  can still use `FadeIn`/`Create` as before).

---

# Scene 1: Introducing motion whose velocity changes

Concept atoms covered (see `concept_map.md`): 1, 2

## Goal

Notice that motion doesn't always have constant velocity, and come away
with the question "how much is it accelerating?" **The word "acceleration"
itself is never used in this Scene** (it's named for the first time in
Scene2).

## Overall structure

Run the same "three-stage reveal" for both constant-velocity motion and
accelerating motion.

1. Show "😁" alone, filling the screen, with no axis, moving left to right
   at constant velocity (or accelerating). Display a large label right
   below the motion describing it ("Motion at constant velocity" /
   "-> Accelerating motion").
2. Rotate the motion's trace 90° counterclockwise while shrinking it down
   onto this topic's shared vertical position axis (with tick marks) - the
   same technique as Scene4's teaser-to-face_axis transition. As "😁" moves
   to the left side of the screen, shrink the label at the same time and
   move it to the upper right.
3. Play the same motion once more on the vertical axis (still no graph).
4. Add the x-t and v-t graphs, and play "😁"'s motion a third time, fully
   synced with both x-t and v-t (each graph gets its own title). Since the
   x-t graph of constant-velocity motion is a straight line, don't show a
   tangent for it. For the accelerating case, show a live tangent on the
   x-t graph (a parabola).

## Beat 1: Motion at constant velocity

Show the label "Motion at constant velocity" large, right below "😁", and
run the four stages above (v=3 m/s constant, t: 0-3s, x: 0->9). Once stage 4
finishes, fade out the whole screen (including the label).

## Beat 2: Accelerating motion

Run the same four stages for the main example (v0=0, a=2 m/s², t: 0-3s,
x: 0->9, v: 0->6). The label reads "-> Accelerating motion" (the name
"uniformly accelerated motion" is not used yet). Don't fade out this Beat's
end state ("😁", x-t graph, and v-t graph all drawn) - carry it straight
into Beat3.

## Beat 3: Leaving a question

Keep the previous Beat's screen as-is, nudge the x-t graph slightly up and
the v-t graph slightly down to open a gap between them, and show "How much
is it accelerating?" in that gap. Hold for a moment, then fade out the
whole screen to end the Scene (the word "acceleration" is never used).

---

# Scene 2: What acceleration means

Concept atoms covered: 3, 4, 5, 6

## Goal

Understand that acceleration is "the change in velocity divided by the
change in time" (this Scene is where the word "acceleration" is used for
the first time).

## Beat 1: Watch velocity change through a concrete numeric example

Rebuild the layout from the end of Scene1 ("😁" + x-t + v-t, the TWO_ROW
composition) and play the main example (v0=0, a=2) through once, synced
(no looping). Show "v=" as a plain readout (not turned into a meter), and
show a live tangent on the x-t graph (meaningful here since it's a
parabola). Each time t=1, 2, 3s is crossed, show a "+2 m/s" label with a
slight delay during the next interval's playback (without pausing - show
just the difference while the motion keeps going). Connect only "😁" and
the x-t graph with a dotted line (no dotted line between x-t and v-t).

## Layout transition: focus on the v-t graph

Shrink "😁" and the x-t graph into the upper-left corner, and enlarge the
v-t graph to take up most of the screen. Stretch both t-axes to the left as
well. Do this zoom in/out smoothly, together, in a single `self.play` call.

## Beat 2: Δt and Δv

Mark points A and B at t=1 and t=2 on the enlarged v-t graph. Then draw a
horizontal Δt arrow dynamically with `GrowArrow`, followed by a vertical Δv
arrow the same way (not at the same time). Keep both arrows on screen from
here on.

## Beat 3-4: Deriving the formula, zoomed in

Zoom the camera in on the region with the arrows (`MovingCameraScene`), and
do the following while still zoomed in.

- Show the sentence "Divide the change in velocity by the change in time."
- Reveal `a = Δv/Δt = 2 m/s/1s = 2 m/s²` one "=" at a time, dynamically.
- Show the definition "acceleration = the change in velocity per unit
  time."
- Transform the unit: keep the original fraction `(m/s)/s` on screen, add a
  new "=" to its right, and animate it transforming through `m/(s·s)` into
  `m/s²` (don't remove the original expression).
- Since all this zoomed-in text/math overlaps the v-t graph's line, put a
  background behind each element with `layout.make_text_bg` for
  readability.

---

# Scene 3: The v-t graph and acceleration

Concept atom covered: 7

## Goal

Understand that the v-t graph's slope represents acceleration.

## Full revision: Beats 1-3 are skipped

Since the end of Scene2's revised version (the zoomed-in v-t graph + points
A, B + the Δt/Δv arrows + `a=Δv/Δt=...=2 m/s²`) already covers the same
explanation as the old Beat2/Beat3, this Scene3 picks up from that state
directly (still zoomed in) and adds only what used to be Beat4's content.

## Beat (equivalent to the old Beat4): From a proportional relationship to slope

1. Highlight the origin point with `Indicate`, and show "A line through the
   origin -> a proportional relationship."
2. (The `a=Δv/Δt=...` display has served its purpose, so fade it out, and
   in the space it leaves) show "The proportional equation v=at," left-
   aligned with "A line through the origin -> a proportional relationship."
3. Reveal, one at a time: "-> the proportionality constant a" ->
   "= acceleration" -> "= the graph's slope." Left-align this line with the
   same left edge.

Since this whole sequence of text ("A line through the origin -> a
proportional relationship," "v=at," "-> the proportionality constant
a=...") overlaps the v-t graph's line, put a background behind it with
`layout.make_text_bg`.

Hold for a moment, then zoom out while fading out, ending the Scene.

---

# Scene 4: What uniformly accelerated motion is

Concept atoms covered: 8, 9

## Goal

Understand that in motion with constant acceleration, velocity changes at a
constant rate. Show that "😁"'s motion, the x-t graph, the v-t graph, and
the a-t graph all move together.

## Beat 1: A clear example of uniformly accelerated motion

Run "😁" left to right, filling the screen with no axis, using v0=0,
a=4 m/s² (clearly distinct from the main example) - a cinematic teaser
unrelated to the actual numeric scale. Show the text "Motion with constant
acceleration = uniformly accelerated motion" right below the motion, in
the same arrangement as Scene1's label (large at first, then shrinking to
the upper right as "😁" moves to the left). Then rotate the trace 90°
counterclockwise while shrinking it onto the ticked face_axis (move the
label at the same time as this rotation).

## Beat 2: Syncing with the x-t graph

Add the x-t graph (with its title). Play "😁" and the x-t graph synced over
t: 0-3s. Don't show a tangent in this Beat.

## Beat 3: Syncing with the v-t graph

Add the v-t graph (with its title), and play "😁", x-t, and v-t synced, all
three together. Show a live tangent on the x-t graph in this Beat (only
while the v-t graph is being added).

## Beat 4: Syncing with the a-t graph

Add the a-t graph (with its title), and play "😁", x-t, v-t, and a-t
synced, all four together. Show a live tangent on the v-t graph in this
Beat (showing that the slope = a doesn't change, by the tangent staying
still). Then zoom the camera into the v-t and a-t rows, and reveal, one at
a time, left-aligned, in the center of the screen: "Acceleration is
constant" -> "-> the v-t graph is a straight line" -> "-> the a-t graph is
a horizontal line," each with a filled text background, emphasizing how
flat the a-t graph is.

---

# Scene 5: Area under the v-t graph and distance traveled

Concept atoms covered: 10, 11

## Goal

Understand that the area under the v-t graph represents distance traveled,
through the process of refining an interval subdivision and syncing "😁"'s
motion with the accumulating area at each step.

## Layout

A large v-t graph slightly right of center (the t-axis uses its full range
of ticks from 0 to 4; v(4)=8, final area = 16). "😁"'s motion sits on the
left (on a vertical axis matched to the area value, labeled "x"). Right
next to "😁", show the current velocity as "v=..." in a fairly large font,
and between "😁" and the v-t graph, show the current elapsed time as
"t=..." at a fixed position (neither is connected to the shapes with a
dotted line). Since the v0≠0 example (Beat8, below) also uses the same
t-axis up to t=4, give the area/position axes a bit more headroom than the
v0=0 example needs (area axis 0-20, velocity axis 0-10).

## Beat 1: The constant-velocity case (using the full t: 0-4 range)

Show "For motion at constant velocity" large in the upper right of the
graph. Show the v-t graph at a constant v=4 m/s, and the rectangle below it
(Δt=4, v=4), with width/height brackets in a fairly large font with a
filled background. Show the area `vΔt=16m` large, in the middle of the
rectangle. Then actually run "😁" at constant velocity, synced with the
corresponding point on the v-t graph (moving along the horizontal line).
Before clearing it, show the line "Rectangle's area = speed × time =
distance traveled" right above the rectangle with a background, and hold
for about 5 seconds.

## Beats 2-6: Refining the subdivision (initial velocity zero)

Keep showing "Velocity increases at a constant rate" in the upper right of
the graph, with "Approximated as a series of constant-velocity motions"
below it. Smoothly morph the staircase graph through 2 -> 4 -> 8 -> 16 ->
32 divisions with Transform (from 8 divisions on, show only the numeric
total area; don't label a zero-area interval). Show the total area as
"Area = 12.0," for example - just "Area =" followed by a number to one
decimal place, with no extra symbol (like "S="). In the lower right of the
graph, show the current division count as "Divided into n intervals."
**At each division count**, move a point along the top edge of the
rectangles (a discontinuous step function), and sync "😁"'s motion with it
(advancing by however much area has accumulated).

## Beat 7: ∞ (the conclusion: area = distance traveled)

Converge the staircase onto the triangle (the lower-right display now reads
"Divided into ∞ intervals" - use the math symbol `\infty`, not the Unicode
"∞" character), and show the true area (16m). Move "😁" and the point on
the v-t graph together along the true line v=2t. Then show the two lines
"The area enclosed by the v-t graph and the t axis" / "corresponds to the
distance traveled," overlaid on the v-t graph with a background, hold for 5
seconds, and fade out (the same two lines are shown again at the end of
Beat8 and Beat9, so implement this as a shared helper).

## Beat 8: The case with a nonzero initial velocity

Using v0=1.0, a=2, over the same t: 0-4s range as the main example
(v(4)=9), repeat the convergence from a 4-division staircase to the
trapezoid, with "😁" synced at each step as before. After it converges, show
the same "area corresponds to distance traveled" two-line text as in Beat7.
Don't clear "😁"/face_axis here - they keep playing their synced motion on
the left into the next Beat (Beat9, the cubic example).

## Beat 9: The case where acceleration isn't constant

Show "A more complex motion" in the upper right of the graph. Show the
cubic example (v=(t-1)(t-5)(t-8)/15+3), and repeat the same 2 -> 4 -> 8 ->
16 -> 32 -> ∞ convergence as Beats 2-7 (reusing `build_staircase`/
`step_functions`, generalized). As in the Beats up through 8, sync "😁"'s
motion on the face_axis at each division count (swap the face_axis to a
wider set of ticks matching this cubic's total distance traveled). Right
after each stage's Transform, the gap is easy to spot, so hold a bit longer
before moving to the next stage. After it converges, show the same "area
corresponds to distance traveled" two lines as in Beat7/Beat8, then end the
Scene.

---

# Scene 6: Deriving the formulas

Concept atoms covered: 12, 13, 14

## Goal

Derive the three uniformly-accelerated-motion formulas from the v-t
graph's line equation and its area equation.

## Layout / camera work

The v-t graph on the left, algebra on the right (continuing Scene5's
v0=1.0, a=2, t: 0-2s example). Since Beat1 and Beat2 (graph work) are
self-contained on the left, zoom the camera into the v-t graph at the start
(staying within the top/bottom edges of the screen), and zoom out once the
algebra on the right is needed. Keep the camera's center slightly to the
right of the graph, so the graph reads as further left on screen, and show
each Beat's heading text in the empty space to the right inside the zoom
(without overlapping the graph on the left). Place the heading text a bit
below the very top of the zoomed frame, not flush against it. Nudge the
algebra column slightly left too, using the margin between it and the
graph, and enlarge its font for readability. Throughout this Scene, hold
displayed text/formulas for about 5 seconds before fading them out, **and
don't clear earlier text when showing the next** (keep text used to explain
a formula on screen until that formula is shown and the step feels
complete).

## Beat 1: The line's equation (Formula 1)

Once inside the zoomed graph, first show "Find the line's equation" large
in the empty space on the right. Leave it on screen, then show the slope
triangle and "a: the graph's slope = acceleration." Leave that too, then
show the intercept point and "v₀: the graph's intercept = initial velocity
(the value of v at t=0)." With all of this still on screen, show "The
line's equation: v = v0 + at" near the line and hold for 5 seconds, then
show "-> Formula 1" as a continuation of the equation and hold for 5
seconds. Only now fade out the explanatory text used so far ("Find the
line's equation," "a: ...," "v₀: ...") - but keep Formula 1 itself on
screen.

## Beat 2: The area equation (Formula 2)

Highlight the whole trapezoid with color, show "This trapezoid's area"
(line break) "= the distance traveled over t seconds" in the empty space on
the right, then restore the color (this is a brief aside, so unlike
Formula 1 it's fine to clear it right away).

Next, highlight the rectangle and show "First, find this rectangle's area"
in the empty space on the right. Show brackets for its base (t) and height
(v0). Then show `t × v0 = v0t` inside the rectangle (combining the working
step and the bold result into one line, with a background). Don't clear
anything here.

Likewise, highlight the triangle and show "Next, find this triangle's
area" right below the rectangle's explanation (without clearing it). Show
brackets for its base (t, shared) and height (at), and
`t × at × 1/2 = (1/2)at²` inside the triangle (again combined into one
line, with a background). Again, don't clear anything.

Zoom the camera out, and show "Add the triangle's area and the rectangle's
area together." Then show `v0t + (1/2)at²` large, centered on screen
(don't clear the rectangle, triangle, or any explanatory text yet). Hold
for 5 seconds, then show "-> Formula 2" continuing from that equation, and
hold for 5 seconds. Only now fade out everything used so far - the line's
equation (Formula 1), the rectangle/triangle set, and their explanations -
and reposition Formula 1 and Formula 2 into the right-hand column, labeling
`x = v0t + (1/2)at²` as "Formula 2."

## Beat 3: Combining them to derive a third equation (Formula 3)

With Formula 1 and Formula 2 still lined up on the right, show "Derive one
more formula from these two" large, centered on screen, then shrink it into
the algebra column's heading. Carefully walk through eliminating t, in the
following explicit steps (keep everything on screen; hold each line for
about 5 seconds. Nudge the column slightly left using the margin next to
the graph, and enlarge the font for readability).

1. Solve Formula 1 for t: `at = v - v0`
2. Rearranging further: `t = (v-v0)/a`
3. Substitute t into Formula 2: `x = v0(v-v0)/a + (1/2)a((v-v0)/a)²`
4. Multiply both sides by 2a: `2ax = 2v0(v-v0) + (v-v0)²`
5. Expanding the right side: `2ax = 2v0v - 2v0² + v² - 2v0v + v0²`
6. Collecting like terms: `2ax = v² - v0²`

Show the conclusion, `v² - v0² = 2ax`, as "Formula 3." Make this line's
font larger than the other six derivation lines, and frame it in the accent
color to make it stand out.

## Close

Fade out everything except the three formulas (keep their derivation steps
as-is), smoothly gather and align all three formulas in the center of the
screen, zoom the camera in, and end the Scene.

---

# Scene 7: Wrap-up

Concept atoms covered: none (review of 2, 5, 7, 8, 10, 12-14)

## Goal

Tie together the relationships between acceleration, uniformly accelerated
motion, the graphs, and the formulas. This Scene ends the video.

## Layout

Arrange "😁" (on a vertical position axis), the x-t graph, and the v-t
graph left to right (side by side, rather than the "stacked vertically"
layout from Scenes 1-6). Connect only "😁" and the x-t graph with a dotted
line (no dotted line between x-t and v-t - sync only the timing of the
motion and the plotting). Show the label "Uniformly accelerated motion" at
the top, a checklist in the lower left, and the three formulas stacked
vertically in the lower right.

## Beat 1: Reviewing what we learned

First, play the main example (v0=0, a=2) through once, fully synced across
"😁", x-t, and v-t (show a live tangent on the x-t graph, and leave it on
screen through the following Beats too). Then reveal the following items as
a checklist, one at a time.

1. Acceleration is: the change in velocity per unit time
2. On a v-t graph: slope = acceleration
3. On a v-t graph: area = distance traveled
4. Motion with constant acceleration: uniformly accelerated motion

Then, in the empty space in the lower right, reveal the three formulas
`v=v0+at`, `x=v0t+(1/2)at²`, `v²-v0²=2ax` one at a time, stacked vertically
(as an independent group, not as another checklist item).

## Beat 2: Bringing it all together

Highlight each item with `Indicate` while briefly replaying the
corresponding visual (hold each highlight a bit longer than usual).

- Item 1: `Indicate` the item text.
- Item 2: pick a point on the v-t graph, draw its tangent, and show it
  together with the `Indicate`.
- Item 3: flash-highlight the area under the v-t graph.
- Item 4: `Indicate` the item text.
- The formulas: `Indicate` all three together.

## Final Animation

Hold for a while, then fade out every element on screen, ending the video.
