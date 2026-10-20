# Concept Map: Acceleration and Uniformly Accelerated Motion

This topic shipped before `concept_map.md` became part of the process, so
this was written retroactively. See `docs/physics_teaching_principles.md`
for how to write one.

## Prerequisites (from earlier topics)

- Velocity v, the x-t graph, the v-t graph (from "How to Express Motion")
  - not re-derived; reused as-is, with the existing synced layout, for contrast.

## Concept atoms (teaching order)

1. There is motion where velocity changes - contrasted with constant-velocity motion [depends on: velocity v (previous topic)]
2. Acceleration = a quantity describing how much velocity changes - name it intuitively before giving the formula [depends on: 1]
3. A concrete numerical example of velocity changing - v=0,2,4,6 m/s at t=0,1,2,3s, shown as a plain "v=" readout [depends on: 2]
4. Δv, Δt - name the amount of change and the time it took [depends on: 3]
5. a=Δv/Δt, acceleration = the change in velocity per unit time - give the formula only after the numeric example [depends on: 4]
6. The unit of acceleration, m/s² - derive it from the fraction (m/s)/s; don't present it out of nowhere [depends on: 5]
7. v-t graph slope = acceleration - compute Δv/Δt between two points and confirm it matches the slope before concluding [depends on: 5, v-t graph (previous topic)]
8. Uniformly accelerated motion - a is constant. Use a clearly distinct value like a=4, filling the screen [depends on: 2]
9. a-t graph - a horizontal line. Add it after x-t -> v-t, emphasizing how flat it is [depends on: 8, 7]
10. Area under the v-t graph = distance traveled - show it by converging a staircase approximation (2 -> 4 -> 8 -> 16 divisions) onto a smooth line [depends on: 8]
11. Area when v0≠0 (a trapezoid) - briefly repeat the same procedure as 10 [depends on: 10]
12. v=v0+at (Formula 1) - directly from the intercept v0 and slope a [depends on: 7]
13. x=v0t+(1/2)at² (Formula 2) - decompose the trapezoid into a rectangle and a triangle [depends on: 10]
14. v²-v0²=2ax (Formula 3) - eliminate t from Formulas 1 and 2, showing the steps explicitly [depends on: 12, 13]

## New vocabulary, symbols, and colors

- a (acceleration), v0 (initial velocity), Δv, Δt
- Colors: ACCELERATION (#EF4444) = a, the a-t curve, and its label (see `docs/visual_language.md`)
- Layout: the compressed two-row (x-t/v-t) and three-row (x-t/v-t/a-t) stacks, and the "compress a large axis down into the face-axis slot (object follows along)" transform - see this topic's `layout.py` and `manim_notes.md`

## Cut from this topic

- **Free fall** - a Scene for this was built once, but was removed in review
  to keep the topic focused on the graph/algebra relationships. Candidate
  for the next topic: everything here carries over directly by substituting
  g for a.
