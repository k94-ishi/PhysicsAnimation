"""Render all scenes for this topic, in order.

Usage:
    uv run python render.py [-ql|-qm|-qh|-qk]

Defaults to -ql (preview quality) if no flag is given, matching this
project's Preview -> Final -> Publish workflow (see CLAUDE.md).
"""

import subprocess
import sys
from pathlib import Path

SCENES = [
    ("scene01_velocity_change.py", "Scene01VelocityChange"),
    ("scene02_acceleration_definition.py", "Scene02AccelerationDefinition"),
    ("scene03_vt_slope.py", "Scene03VtSlope"),
    ("scene04_uniform_acceleration.py", "Scene04UniformAcceleration"),
    ("scene05_vt_area.py", "Scene05VtArea"),
    ("scene06_formulas.py", "Scene06Formulas"),
    ("scene07_summary.py", "Scene07Summary"),
]

VALID_QUALITY_FLAGS = {"-ql", "-qm", "-qh", "-qk"}


def main() -> None:
    quality_flag = "-ql"
    if len(sys.argv) > 1:
        if sys.argv[1] not in VALID_QUALITY_FLAGS:
            sys.exit(f"Unknown quality flag {sys.argv[1]!r}; expected one of {sorted(VALID_QUALITY_FLAGS)}")
        quality_flag = sys.argv[1]

    topic_dir = Path(__file__).resolve().parent
    for scene_file, scene_class in SCENES:
        print(f"--- Rendering {scene_class} ({quality_flag}) ---")
        subprocess.run(
            [sys.executable, "-m", "manim", quality_flag, str(topic_dir / scene_file), scene_class],
            check=True,
        )


if __name__ == "__main__":
    main()
