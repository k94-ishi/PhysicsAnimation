"""The "😁" stand-in used as the moving object throughout
mechanics_how_to_express_movements (see storyboard.md, all scenes).

Manim's SVG renderer does not support SVG radial gradients, so the emoji's
main face circle (assets/images/1F601.svg, first path) needs its fill
overridden with a flat color after loading; everything else in the SVG
renders correctly as flat fills.
"""

from pathlib import Path

from manim import SVGMobject

EMOJI_SVG_PATH = Path(__file__).resolve().parent.parent / "assets" / "images" / "1F601.svg"
FACE_FILL_COLOR = "#FDE030"
DEFAULT_FACE_HEIGHT = 0.6


def make_face(height: float = DEFAULT_FACE_HEIGHT) -> SVGMobject:
    """Create one instance of the moving "😁" object at the given height."""
    face = SVGMobject(str(EMOJI_SVG_PATH))
    face.set(height=height)
    face.submobjects[0].set_fill(FACE_FILL_COLOR, opacity=1)
    return face
