# Concept Map: How to Express Motion

This topic shipped before `concept_map.md` became part of the process, so
this was written retroactively. See `docs/physics_teaching_principles.md`
for how to write one.

## Prerequisites (from earlier topics)

None (first topic in the course)

## Concept atoms (teaching order)

1. Position x - express an object's location as a number on a number line
2. Coordinate axis - add ticks and numbers to turn the line into a coordinate axis [depends on: position x]
3. Time t - motion involves the passage of time; show it alongside a timer [depends on: position x]
4. x-t graph axes - set up a separate coordinate system (vertical x, horizontal t), apart from the object itself [depends on: coordinate axis, time t]
5. Correspondence between the object's position and a point on the graph - match them by height alone, without yet using the t axis [depends on: 4]
6. Tracing the path - actually plot (t, x) as time passes [depends on: 5]
7. Different initial positions x0 - the same shape of motion shifts the curve horizontally if the starting position changes [depends on: 6]
8. The t<0 region - extend the time axis into the past [depends on: 6]
9. There is a quantity called velocity - introduced as a quantity distinct from position (not yet formalized) [depends on: position x]
10. The instants where velocity is 0 / maximum / minimum - identified by observing the actual motion [depends on: 9]
11. Correspondence between velocity and the tangent line's slope - the instants from 10 line up with how steep/shallow the graph's tangent is [depends on: 10, 6]
12. Computing the tangent's slope (Δx/Δt) - zoom in, compute numerically, confirm it matches the actual speed [depends on: 11]
13. Average velocity = displacement/time - generalize 12 to an arbitrary interval [depends on: 12]
14. v-t graph - plot velocity against time; built the same way as the x-t graph [depends on: 13]
15. Comparing multiple motion patterns - line up different motions' x-t/v-t shapes side by side [depends on: 14]

## New vocabulary, symbols, and colors

- x, t, v (velocity as a slope)
- Colors: PRIMARY = x-t curve, VELOCITY (#22C55E) = v and the v-t curve (see `docs/visual_language.md`)
- "😁" is used as the moving object going forward. The vertical position axis + horizontal dotted connector to the x-t graph is established here and reused in later topics.
