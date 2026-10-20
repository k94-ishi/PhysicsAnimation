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

### Combining rendered scenes into one video

Manim renders each scene to its own file, under
`media/videos/<scene_file_stem>/<quality_dir>/<SceneClassName>.mp4` (the
quality directory is `480p15` for `-ql`, `720p30` for `-qm`, `1080p60` for
`-qh`, and `2160p60` for `-qk`). After rendering every scene for a topic,
concatenate them in the order defined by that topic's `render.py` (so the
lesson plays start to finish) and save the result under `output/preview/`
(for a `-ql`/`-qm` pass) or `output/final/` (for a `-qh`/`-qk` pass).

```bash
TOPIC_DIR=units/mechanics/mechanics_how_to_express_movements
QUALITY_DIR=480p15   # must match the quality flag used to render
OUT_DIR=output/preview   # use output/final for a -qh/-qk render

uv run python - <<PYEOF
import importlib.util, pathlib

topic_dir = pathlib.Path("$TOPIC_DIR")
spec = importlib.util.spec_from_file_location("render", topic_dir / "render.py")
render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)

clips = [
    pathlib.Path("media/videos") / pathlib.Path(scene_file).stem / "$QUALITY_DIR" / f"{scene_class}.mp4"
    for scene_file, scene_class in render.SCENES
]
pathlib.Path("/tmp/concat_list.txt").write_text(
    "".join(f"file '{clip.resolve()}'\n" for clip in clips)
)
PYEOF

mkdir -p "$OUT_DIR"
ffmpeg -f concat -safe 0 -i /tmp/concat_list.txt -c copy "$OUT_DIR/$(basename "$TOPIC_DIR").mp4"
```

Reading `render.py`'s own `SCENES` list keeps the concatenation order in
sync with whatever that topic actually renders, instead of relying on a
second, hand-maintained list. Stream-copying (`-c copy`) avoids
re-encoding, since every scene in a topic shares the same Manim render
settings.

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
