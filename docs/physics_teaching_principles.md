# Physics Teaching Principles

Principles for teaching order and granularity. Concrete implementation/review
rules live in `SKILL.md`. Read this before writing a new topic's
`concept_map.md` / `teaching_plan.md`.

## Concept Atom

A Scene / Beat should correspond to exactly "one cognitive shift" - not a
section heading.

Bad example: `Scene1 What is acceleration / Scene2 Uniformly accelerated
motion / Scene3 Formulas`

Good example: `Velocity can change -> we want to express that change as a
number -> what dividing by time means -> we name it acceleration -> on a
graph, it's the slope`

In `concept_map.md`, check that each item really is a single shift. If it
reads as "A and B," split it into two.

## Reusing prior knowledge

Before writing a new topic's `concept_map.md`, read the `concept_map.md` of
existing topics in the same section and check which concepts already have a
name, symbol, or color assigned.

Reuse concepts the student already knows; don't re-derive them. A short line
like "Last time, we learned that velocity is the slope of the x-t graph" is
enough. If a prerequisite isn't covered by an existing `concept_map.md`, ask
the human.

## Concrete -> abstract, simple -> complex

- Order: phenomenon -> graph -> formula. Never introduce a formula before
  showing the phenomenon.
- Simple cases first (v0=0, constant values, etc.); generalize later.
- Values being contrasted (e.g. different accelerations) must differ
  clearly, not by a marginal amount (use a=1 vs a=4, not a=1 vs 1.2).

## Cognitive load

- Don't introduce multiple new elements (graphs, symbols, displays) at the
  same time, unless the relationship between them is itself the topic.
- Add one thing at a time rather than showing everything and then
  explaining (e.g. the face -> +x-t graph -> +v-t graph -> +a-t graph).
- Static isn't automatically clearer. Pausing in the middle of explaining a
  moving phenomenon can make it *harder* to understand. Use repetition, a
  fade-out hold, or a zoom instead. This doesn't apply to pausing on
  already-static content (e.g. a formula already on screen).
- Once working steps (intermediate equations, construction lines) have
  served their purpose, clear them from the screen and keep only the
  result. Leaving the scratch work on screen keeps already-completed
  reasoning steps around as ongoing cognitive load.

## Forbidden patterns

- Don't show a formula before showing the phenomenon.
- Don't show a graph before showing what it's a graph of.
- Don't introduce two or more new symbols/names at once (don't show `Δv`,
  `Δt`, and `a` simultaneously without explanation).
- Colors carry fixed meaning (see `visual_language.md`). Don't repurpose a
  color or leave a new quantity uncolored.
- Don't cram two concept atoms into one Beat just because they're related.

## Physical correctness over appearance

When accuracy and visual appeal conflict, accuracy wins. Make any
simplification (e.g. ignoring air resistance) explicit.

## Three-stage review

`concept_map.md` (which concept atoms, in what order, depending on what) ->
`teaching_plan.md` (which Scene teaches which concept atom, and how; notes on
load distribution) -> `storyboard.md` (per-Beat Goal/Layout/Narration/Visual/
Animation, detailed enough to implement).

Each stage goes through human review before moving to the next. Don't write
multiple stages ahead of review.
