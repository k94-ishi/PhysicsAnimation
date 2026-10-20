# Visual Language

Conventions for color, icons, and camera work. `docs/color_guide.md` is
retired and merged into this file.

## Color (single source of truth)

| Use | Color |
|------|-----|
| Background | `#0E1116` |
| Primary (position x) | `#3B82F6` |
| Formula (text / axes) | `#FFFFFF` |
| Velocity (v) | `#22C55E` |
| Acceleration (a) | `#EF4444` |
| Force | `#F97316` |
| Energy | `#EAB308` |

The source of truth lives in `common/colors.py`. Colors are fixed per
quantity. Don't repurpose one, and don't leave a new quantity uncolored
(forbidden patterns are listed in `docs/physics_teaching_principles.md`).

## Icon

- "😁" - the moving object used across all topics.
- Only switch to a different icon if a different physical object is truly
  needed (e.g. a ball). Record the reason in `concept_map.md`.

## Camera work / layout conventions

- When showing the object alongside an x-t graph at the same time, move the
  object along a **vertical position axis** and connect it to the graph's x
  axis with a horizontal dotted line (see
  `mechanics_acceleration_and_uniformly_accelerated_motion/layout.py`). Use
  this dotted connection only between **values that share the same range
  and have a direct correspondence** (the object's position <-> the x-t
  graph's x). Don't draw a dotted connection to graphs of a different
  physical quantity (v-t, a-t); for those, it's enough to **sync the timing**
  of the motion and the plotting.
- Stack v-t and a-t graphs below the x-t graph on a shared t-axis scale.
- When adding more graphs, add them one at a time rather than all at once
  (per the cognitive-load principle).
- Emphasize with a zoom, repetition, or a fade-out hold - not a pause.
- Only use a camera zoom when the scale genuinely needs to change. If the
  scale stays the same, just offset the row's Y coordinate (see
  `manim_notes.md`).
- Only draw a tangent line on a curve segment where the slope is changing.
  Don't draw a tangent on a straight line (constant slope) - unless the
  storyboard explicitly calls for showing that the slope *is* constant as
  its own point, in which case note that intent in `storyboard.md`.
- If text unavoidably overlaps a graph element, put a background-colored
  rectangle (e.g. `layout.make_text_bg`, built on `BackgroundRectangle`)
  behind the text to keep it readable.
- Draw text and formulas with `Write` (so it looks like it's being written).
  Use `FadeIn`/`Create` for shapes, icons, and graph elements.
- Left-align stacked multi-line text/formula blocks.
- A moving object (e.g. 😁) should always render in front of any connector
  line attached to it (z-index).
