# Physics Animation Project

## Goal

Make high-school physics explainer videos with Manim, in English.

Current focus: ship the first lesson. Don't over-engineer for the future.

Future: more advanced physics/math topics, AI/ML visualization.

---

# Workflow

The direction of each topic comes from conversation. Create the following
in order, with a human review after each stage before moving on (see
`docs/physics_teaching_principles.md` for why):

1. Draft `concept_map.md` (check existing topics' `concept_map.md` in the
   same section for prerequisites/reuse)
2. Human review
3. Draft `teaching_plan.md`
4. Human review
5. Draft `storyboard.md` (each Beat's `Narration` is the actual script)
6. Human review
7. Manim implementation
8. Preview -> Final -> Publish

When working through this workflow, think like a **beloved, meticulous
teacher**. Constantly imagine where students will get stuck and what they'll
find interesting, and design around that.

---

# Topic structure

```
topic/
├── concept_map.md
├── teaching_plan.md
├── storyboard.md
├── sceneXX_*.py
└── render.py
```

- `concept_map.md` / `teaching_plan.md` / `storyboard.md` are all drafted by
  Codex and reviewed by a human.
- Don't implement from a draft that hasn't been reviewed yet.
- 1 Scene = 1 concept atom (see `docs/physics_teaching_principles.md`).

---

# Development

```bash
source .venv/bin/activate
```

Run Manim via `uv run`.

Only extract shared code into `common/` once it's reused a second time.

---

# Documentation

Read these:

- `docs/physics_teaching_principles.md` - required reading before writing
  `concept_map.md`/`teaching_plan.md`
- `docs/visual_language.md` - color, icon, and camera-work conventions
- `skills/physics-video-review/SKILL.md` - required reading before
  implementation; accumulated concrete review notes
- `skills/physics-video-review/manim_notes.md` - reference when a
  Manim-specific issue comes up

Before implementing:

- Read `concept_map.md`, `teaching_plan.md`, `storyboard.md`
- Implement only what `storyboard.md` says
- Follow the educational intent stated in each Scene's Goal
- Don't invent narration, visuals, or scene transitions on your own
- Ask rather than guess when something is unclear
- Keep Scenes small
- Prioritize educational clarity and physical correctness
- Append reusable insights to `SKILL.md`, Manim-specific discoveries to
  `manim_notes.md`, and insights about teaching principles to
  `docs/physics_teaching_principles.md`
