# Physics Animation Project

Educational physics animations built with **Manim Community**.

The project aims to create reusable educational content rather than standalone videos.

## Current Status

Phase 1 focuses on publishing the first lesson.

Future plans include:

* More advanced physics and university-level mathematics
* Machine Learning / AI visualization

## Repository Structure

```text
physics-animation/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── common/
├── assets/
├── units/
├── output/
├── docs/
└── skills/
```

### Topic Structure

Each lesson lives in its own directory under `units/`.

Example:

```text
units/
└── mechanics/
    └── mechanics_how_to_express_movements/
        ├── concept_map.md
        ├── teaching_plan.md
        ├── storyboard.md
        ├── scene01_*.py
        ├── scene02_*.py
        ├── ...
        └── render.py
```

## Workflow

The content production workflow is:

1. Draft `concept_map.md` (check earlier topics' `concept_map.md` for prerequisites/reuse)
2. Review it
3. Draft `teaching_plan.md`
4. Review it
5. Draft `storyboard.md` (its per-Beat narration fields are the script)
6. Review it
7. Implement Manim scenes
8. Render a preview
9. Render the final video
10. Publish

## Development

Create and activate a virtual environment.

```bash
uv venv .venv
source .venv/bin/activate
```

Install dependencies.

```bash
uv pip install -r requirements.txt
```

Run Manim with `uv run`.

Example:

```bash
uv run python units/mechanics/mechanics_how_to_express_movements/render.py
```

## Project Principles

* Educational clarity comes first.
* Physics correctness is never sacrificed.
* Keep animations language-independent whenever possible.
* Extract reusable code only after it has been used at least twice.
* Prefer simple, maintainable implementations over premature abstraction.

## Documentation

* `CLAUDE.md` / `AGENTS.md` — Instructions for coding agents.
* `docs/physics_teaching_principles.md` — Pedagogical design principles (concept sizing, cognitive load, forbidden patterns).
* `docs/visual_language.md` — Color palette, icon, and camera-work conventions.
* `skills/physics-video-review/SKILL.md` — Review checklist and accumulated feedback.
* `skills/physics-video-review/manim_notes.md` — Manim-specific implementation notes.
