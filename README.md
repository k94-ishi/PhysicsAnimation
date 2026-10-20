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
├── scripts/
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

Every `Text` mobject uses "CMU Serif" by default (see `common/__init__.py`),
to match the Computer Modern font LaTeX already renders every formula in.
That font family ships with most LaTeX distributions but isn't always
registered as a system font fontconfig/Pango can find by name. If it
isn't, register it once:

```bash
mkdir -p ~/Library/Fonts
for f in cmunrm.otf cmunbx.otf cmunti.otf cmunbi.otf; do cp "$(kpsewhich "$f")" ~/Library/Fonts/; done
fc-cache -f ~/Library/Fonts
```

Confirm it resolves correctly (should print `cmunrm.otf`, not a fallback
font):

```bash
fc-match "CMU Serif"
```

Run Manim with `uv run`.

Example:

```bash
uv run python units/mechanics/mechanics_how_to_express_movements/render.py
```

### Combining rendered scenes into one video

Manim renders each scene to its own file, under
`media/videos/<scene_file_stem>/<quality_dir>/<SceneClassName>.mp4`. After
rendering every scene for a topic, `scripts/combine_scenes.py` reads that
topic's own `render.py` for its `SCENES` list (so the combined order always
matches what was actually rendered), concatenates the clips with `ffmpeg`
(stream copy — no re-encoding, since every scene in a topic shares the same
Manim render settings), and writes the result to `output/preview/` (for a
`-ql`/`-qm` render) or `output/final/` (for a `-qh`/`-qk` render), named
after the topic.

```bash
uv run python units/mechanics/mechanics_how_to_express_movements/render.py -ql
uv run python scripts/combine_scenes.py units/mechanics/mechanics_how_to_express_movements -ql
```

The quality flag passed to `combine_scenes.py` must match the one used to
render (defaults to `-ql` if omitted). If a scene hasn't been rendered at
that quality yet, it reports exactly which file is missing and the render
command to produce it.

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
