# Teaching Plan: Acceleration and Uniformly Accelerated Motion

Maps concept atoms 1-14 from `concept_map.md` onto which Scene teaches what,
and how. Camera positioning and exact narration wording live in
`storyboard.md`.
(This topic had already shipped through `storyboard.md`, so this was written
retroactively to match what was actually built.)

## Scene1: Introducing motion whose velocity changes

- Concept atom taught: 1 (there is motion where velocity changes)
- Approach (revised per video review): using the synced layout (😁 + x-t +
  v-t), show constant-velocity motion and then accelerating motion, each
  through the same three stages ("alone -> on the vertical axis -> synced
  with the graphs"), then contrast them.
  **The word "acceleration" is never used in this Scene** - the naming from
  concept atom 2 is moved entirely to Scene2. Scene1 ends on the question
  "How much is it accelerating?" (without answering it).
- Reused: velocity v, the x-t graph, the v-t graph, the synced layout
  (previous topic) - not re-derived
- New: none (only poses the question)
- Load distribution: the only new thing in this Scene is noticing "there is
  motion where velocity changes" and posing "how much?" - no name or
  formula given yet.

## Scene2: What acceleration means

- Concept atoms taught: 2 (acceleration = a quantity describing how much
  velocity changes; named here for the first time), 3 (a concrete numeric
  example), 4 (Δv, Δt), 5 (a=Δv/Δt), 6 (the unit m/s²)
- Approach: rebuild Scene1's composition and build it up 1 Beat = 1 concept
  atom at a time (confirm the numbers -> name Δv/Δt -> formula -> unit).
  Zoom into the v-t graph while deriving the formula; the word
  "acceleration" itself appears on screen for the first time here.
- Reused: Scene1's composition. Velocity display stays a plain "v=" readout
  (not turned into a meter).
- New: the word "acceleration" itself, Δv, Δt, a=Δv/Δt, m/s²
- Load distribution: Δv and Δt are introduced together as a pair, both born
  from the same concrete example (v=2->4 over 1 second), but the new symbol
  `a` is withheld until the next Beat. The "no more than one new symbol at a
  time" rule is read here as applying to Δv/Δt as a single named pair
  describing one relationship, avoided by not adding an independent third
  new symbol (a) in the same moment.

## Scene3: The v-t graph and acceleration

- Concept atom taught: 7 (v-t graph slope = acceleration)
- Approach (revised per video review): since Scene2's revised version
  already finishes computing Δv/Δt between two points on the zoomed-in v-t
  graph, this Scene picks up from that state as-is and adds only the
  concluding part: "a line through the origin -> a proportional
  relationship," "v=at," "the proportionality constant a = acceleration =
  the graph's slope." The derivation steps that overlapped with Scene2
  (picking two points, computing Δv/Δt) are not implemented again.
- Reused: a=Δv/Δt (from Scene2, including the zoomed state), the v-t graph
  (previous topic)
- New: the proportional-relationship framing itself, and the correspondence
  between slope and acceleration
- Load distribution: 1 Scene = 1 concept atom. Avoiding the overlap with
  Scene2 keeps this Scene itself much shorter.

## Scene4: What uniformly accelerated motion is

- Concept atoms taught: 8 (uniformly accelerated motion), 9 (the a-t graph)
- Approach: first show a clearly distinct example (v0=0, a=4) with 😁 alone,
  filling the screen, then add the x-t -> v-t -> a-t graphs one at a time.
- Reused: acceleration (Scenes 1-3), v-t graph slope = acceleration (Scene3)
- New: the name "uniformly accelerated motion," the a-t graph
- Load distribution: add only one new graph per Beat (😁 -> +x-t -> +v-t ->
  +a-t). The contrasting acceleration value (a=4) is chosen to be clearly
  distinguishable in magnitude from the a=2 used in Scenes 1-3.

## Scene5: Area under the v-t graph and distance traveled

- Concept atoms taught: 10 (area under the v-t graph = distance traveled),
  11 (the trapezoid case when v0≠0)
- Approach: rather than asserting it, show it by converging a staircase
  approximation (2 -> 4 -> 8 -> 16 divisions) onto the line. Complete the
  v0=0 case first, then repeat for v0≠0 (simple -> complex).
- Reused: uniformly accelerated motion (Scene4)
- New: the correspondence between area and distance traveled
- Load distribution: this whole Scene is one single convergence process, and
  is allowed to take its time (per the shared storyboard rule, "it's fine to
  spend real time here").

## Scene6: Deriving the formulas

- Concept atoms taught: 12 (Formula 1: v=v0+at), 13 (Formula 2:
  x=v0t+(1/2)at²), 14 (Formula 3: v²-v0²=2ax)
- Approach: 1 Beat = 1 formula. Derive Formula 1 from the intercept and
  slope, Formula 2 from Scene5's area decomposition, and Formula 3 by
  explicitly eliminating t from Formulas 1 and 2.
- Reused: v-t graph slope = acceleration (Scene3), area under the v-t graph
  = distance traveled (Scene5)
- New: Formulas 1, 2, and 3
- Load distribution: holding all three formulas statically on screen at the
  end is a static pause over "reading an already-displayed formula," so it
  falls outside the no-pausing rule.

## Scene7: Wrap-up

- Concept atoms taught: none (review only, of 2, 5, 7, 8, 10, 12-14)
- Approach: cycle through the review items one at a time, then close by
  replaying 😁 + x-t + v-t's synced motion once more, start to finish.
- Reused: every concept atom
- New: none
- Load distribution: the end point of the video. Since there's no new
  content to learn, it's fine to reuse the existing synced layout as-is.

## Out of scope

- Free fall is not included in this topic (see `concept_map.md`; a
  candidate for the next topic).
