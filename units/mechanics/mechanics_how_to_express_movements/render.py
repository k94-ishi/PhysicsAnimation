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
    ("scene01_observe_position.py", "Scene01ObservePosition"),
    ("scene02_xt_graph_points.py", "Scene02XtGraphPoints"),
    ("scene03_time_and_initial_position.py", "Scene03TimeAndInitialPosition"),
    ("scene04_velocity_and_slope.py", "Scene04VelocityAndSlope"),
    ("scene05_velocity_time_graph.py", "Scene05VelocityTimeGraph"),
    ("scene06_summary.py", "Scene06Summary"),
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
