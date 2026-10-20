---
name: physics-video-review
description: Physics animation design rules accumulated from user feedback. Read before implementing or reviewing Manim scenes.
---

# Physics Video Review

Concrete implementation/review rules accumulated over time. Teaching
principles (granularity, ordering, cognitive load, forbidden patterns) live
in `docs/physics_teaching_principles.md` - read that too before
implementing.

## Continuity of motion

- Scenes are continuous by default. Unless `storyboard.md` says otherwise,
  preserve the object's position, graph state, timer, and camera position.
- No teleporting. Connect scenes smoothly.
- Don't stop motion just because a UI element needs to appear.

## Implementing the storyboard

- `Goal` = what the student should understand
- `Narration` = what gets explained
- `Visual` = what gets shown
- Don't invent extra explanation on your own
- If `storyboard.md` is ambiguous or contradictory, ask before implementing

## Layout

- Keep important objects visually clear
- Keep coordinate systems consistent across related scenes
- Keep the object and the graph as separate objects
- Put shared layout code in `common/`
- For visual conventions on object-to-graph connectors, tangent-line
  conditions, text backgrounds, animation verbs (Write/FadeIn), multi-line
  text alignment, and z-index, see `docs/visual_language.md`.
- When contrasting acceleration/velocity values, make the difference clear
  (e.g. a=1 vs a=4)

## Label presentation pattern

- A label that names a motion or formula should first appear large, right
  below the object; as the object settles into its final position (e.g. on
  an axis), shrink the label and move it to a corner at the same time.
  Don't start it small and in the corner.

## Showing derivation steps

- For derivations (area, algebraic manipulation), briefly show the working
  steps (construction lines, provisional equations, brackets), then clear
  the working and leave only the concise result (bold text, highlight
  color, etc.) on the shape or graph.
- Hold each line of an algebraic derivation longer than normal text display
  (roughly 5 seconds), so students have time to verify the step themselves.
- Don't label a value that carries no information (e.g. a zero-area
  rectangle).

## Code structure

- Extract shared code only after it's reused a second time
- Don't abstract ahead of need

## Accumulating feedback

When a new reusable insight comes up:
- Teaching order / cognitive load -> `docs/physics_teaching_principles.md`
- Concrete implementation/review rules -> this file
- Manim-specific technical discoveries -> `manim_notes.md`
