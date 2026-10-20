"""Combine a topic's rendered scene videos into a single file.

Usage:
    uv run python scripts/combine_scenes.py <topic_dir> [-ql|-qm|-qh|-qk]

Reads the topic's own render.py for its SCENES list, so the combined video
always matches the order render.py actually renders in. Every scene in
SCENES must already be rendered at the given quality (defaults to -ql).
Stream-copies with ffmpeg (no re-encoding, since every scene in a topic
shares the same Manim render settings) and writes the result to
output/preview/<topic_name>.mp4 (-ql/-qm) or output/final/<topic_name>.mp4
(-qh/-qk).
"""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

QUALITY_DIRS = {
    "-ql": "480p15",
    "-qm": "720p30",
    "-qh": "1080p60",
    "-qk": "2160p60",
}
OUT_SUBDIRS = {
    "-ql": "preview",
    "-qm": "preview",
    "-qh": "final",
    "-qk": "final",
}

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_scenes(topic_dir: Path) -> list[tuple[str, str]]:
    spec = importlib.util.spec_from_file_location("render", topic_dir / "render.py")
    render = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(render)
    return render.SCENES


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <topic_dir> [-ql|-qm|-qh|-qk]")

    topic_dir = Path(sys.argv[1]).resolve()
    quality_flag = sys.argv[2] if len(sys.argv) > 2 else "-ql"
    if quality_flag not in QUALITY_DIRS:
        sys.exit(f"Unknown quality flag {quality_flag!r}; expected one of {sorted(QUALITY_DIRS)}")

    quality_dir = QUALITY_DIRS[quality_flag]
    scenes = load_scenes(topic_dir)
    clips = [
        REPO_ROOT / "media" / "videos" / Path(scene_file).stem / quality_dir / f"{scene_class}.mp4"
        for scene_file, scene_class in scenes
    ]

    missing = [clip for clip in clips if not clip.exists()]
    if missing:
        missing_list = "\n".join(f"  {clip}" for clip in missing)
        sys.exit(
            f"Missing rendered scene(s) at {quality_dir} - render the topic first "
            f"(uv run python {topic_dir}/render.py {quality_flag}):\n{missing_list}"
        )

    out_dir = REPO_ROOT / "output" / OUT_SUBDIRS[quality_flag]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{topic_dir.name}.mp4"

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as list_file:
        for clip in clips:
            list_file.write(f"file '{clip}'\n")
        list_path = Path(list_file.name)

    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_path), "-c", "copy", str(out_path)],
            check=True,
        )
    finally:
        list_path.unlink(missing_ok=True)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
