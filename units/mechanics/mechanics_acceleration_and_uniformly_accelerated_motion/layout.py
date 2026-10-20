"""Shared synced layout for this topic (revised per user feedback).

The "😁" moves *vertically* on its own position axis, exactly like
mechanics_how_to_express_movements's scene05: a horizontal dashed line
connects it to the matching point on an x-t graph's x-axis, which shares
the same value range/length (so the same physical position always lands at
the same screen height on both). v-t (and a-t) graphs stack below the x-t
graph, sharing the same t-axis horizontal scale/position, so everything
lines up in time as well as in the two-row/three-row vertical stack.

Row geometry (TWO_ROW_*/THREE_ROW_*) intentionally reuses
mechanics_how_to_express_movements's own compressed-layout numbers where
there's no reason to differ, for visual continuity between the two topics.
"""

import numpy as np
from manim import LEFT, RIGHT, UP, DashedLine, Line, SurroundingRectangle, Text, VGroup, VMobject
from manim.mobject.text.numbers import DecimalNumber
from manim.mobject.text.tex_mobject import MathTex

from common.colors import BACKGROUND, FORMULA
from common.face import make_face
from common.graph_layout import CONNECTOR_LINE_COLOR, CONNECTOR_Z_INDEX

GRAPH_TITLE_FONT_SIZE = 20

FACE_HEIGHT = 0.6
FACE_GAP = 0.4  # offset from the face axis line, away from its (LEFT) tick numbers
FACE_Z_INDEX = 1

FACE_AXIS_X = -5.5
GRAPH_ORIGIN_X = -1.0

T_RANGE = [0, 3, 1]
T_AXIS_LENGTH = 6.0

# Two-row compressed layout: x-t graph on top, v-t graph below (scenes 1-3).
# Both this topic's value ranges (X_RANGE, V_RANGE) start at 0, so each
# row's own value=0 baseline sits at that row's origin y - the gap between
# rows is UPPER_Y - (LOWER_Y + AXIS_LENGTH), which must stay generous or
# the two rows' tick numbers read as one continuous axis.
TWO_ROW_AXIS_LENGTH = 2.0
TWO_ROW_UPPER_Y = 1.0  # lowered so the "x-t graph" title above it stays on screen (review)
TWO_ROW_LOWER_Y = -2.6

# Three-row compressed layout: x-t, v-t, a-t stacked (scene4). Same
# start-at-0 spacing consideration as the two-row layout above. All three
# shifted down by the same amount (0.4) so the top row's "x-t graph" title
# stays on screen (review) while the gaps between rows - already tuned -
# stay unchanged.
THREE_ROW_AXIS_LENGTH = 1.3
THREE_ROW_TOP_Y = 1.9
THREE_ROW_MID_Y = -0.4
THREE_ROW_BOTTOM_Y = -2.7

# A single large graph filling most of the vertical space (scenes 3/5/6,
# once the topic's focus narrows to just the v-t graph).
SINGLE_AXIS_LENGTH = 4.8
SINGLE_ORIGIN_Y = -2.1

# A shared bottom row, centered under the graph columns (never at the
# screen edges) for the timer and any "v=" style readouts.
BOTTOM_ROW_Y = -3.3
TIMER_POS = np.array([-1.8, BOTTOM_ROW_Y, 0.0])
READOUT_POS = np.array([0.8, BOTTOM_ROW_Y, 0.0])


def make_face_and_x_axis(value_range: list, length: float, y_center: float):
    """A vertical face axis (for the "😁") and an x-t graph's x-axis,
    sharing the same value range/length so a horizontal line between a
    point on each (same value) is always level - see module docstring."""
    from common.graph_layout import make_value_axis

    face_axis = make_value_axis(np.array([FACE_AXIS_X, y_center, 0.0]), value_range, length)
    graph_x_axis = make_value_axis(np.array([GRAPH_ORIGIN_X, y_center, 0.0]), value_range, length)
    return face_axis, graph_x_axis


def make_tracked_face(face_axis, get_value):
    """A "😁" that tracks get_value() along face_axis (a vertical
    make_value_axis NumberLine), offset FACE_GAP to the right of the axis
    line so it clears the axis's own LEFT-side tick numbers. Caller must
    call face.remove_updater(update) once the motion is done (see
    manim_notes.md > TracedPath)."""
    face = make_face(height=FACE_HEIGHT)
    face.set_z_index(FACE_Z_INDEX)  # always in front of connector lines (review: don't let lines render in front of 😁)

    def update(mob) -> None:
        point = face_axis.number_to_point(get_value())
        mob.move_to(point + RIGHT * FACE_GAP)

    update(face)
    face.add_updater(update)
    return face, update


def make_graph_title(label: str, axis_label_mobject, color: str = FORMULA) -> Text:
    """A small "x-t graph" / "v-t graph" style title stacked above a graph's
    own one-letter value label (e.g. the "x" MathTex next to the axis) -
    review: when showing multiple graphs, give each graph a title. Anchored
    to the value label itself (not the bare axis) so the two never overlap
    regardless of the label's own buff from the axis."""
    return Text(label, color=color, font_size=GRAPH_TITLE_FONT_SIZE).next_to(axis_label_mobject, UP, buff=0.15)


def make_tangent_line(point_fn, t: float, value: float, slope: float, half_span: float, color: str, stroke_width: float = 3) -> Line:
    """A short tangent-line segment on a graph at (t, value) with the given
    slope, in the point_fn's screen coordinates - shown alongside a synced
    x-t/v-t connector so the instantaneous slope (=v on an x-t graph) is
    visible, not just the connector dot (review: show a tangent on the x-t graph)."""
    return Line(
        point_fn(t - half_span, value - slope * half_span),
        point_fn(t + half_span, value + slope * half_span),
        color=color,
        stroke_width=stroke_width,
    )


TEXT_BG_Z_INDEX = 10


def make_text_bg(mobject, opacity: float = 1.0, buff: float = 0.06) -> SurroundingRectangle:
    """An opaque, background-colored rectangle sized to `mobject`, meant to
    be added just *before* it (so it draws behind) wherever text
    unavoidably overlaps a graph - review: when text unavoidably overlaps a
    graph, fill the text's background with the background color. Re-add
    after moving `mobject` (it does not auto-follow).

    IMPORTANT - add this with a plain `self.add(bg)`, never
    `self.play(FadeIn(bg), ...)`: confirmed via extensive isolated repro
    that an animated (FadeIn'd), partially-transparent background reliably
    fails to occlude earlier-added content (a graph line, a settled
    TracedPath) in this project's scenes - the earlier content still shows
    straight through at full brightness. A plain `self.add(bg)` at full
    opacity (this function's default) does occlude correctly; only animate
    `mobject` (the text) itself. Since `opacity=1.0` and the rectangle's
    color already matches the scene background, this looks identical to a
    translucent overlay wherever there's nothing underneath, so there is no
    visual cost to the full opacity.

    Deliberately a plain SurroundingRectangle, not manim's own
    BackgroundRectangle (BackgroundRectangle has the same occlusion problem,
    even via plain `self.add`). Also gives both the rectangle and `mobject`
    itself an explicit z_index as a further safeguard. See manim_notes.md
    for the full writeup of this gotcha."""
    rect = SurroundingRectangle(mobject, color=BACKGROUND, fill_color=BACKGROUND, fill_opacity=opacity, stroke_opacity=0, buff=buff)
    rect.set_z_index(TEXT_BG_Z_INDEX)
    mobject.set_z_index(TEXT_BG_Z_INDEX + 1)
    return rect


def freeze_traced_path(traced_path) -> VMobject:
    """Convert a settled (updater-cleared) TracedPath into an equivalent
    static VMobject with the same points/style. TracedPath does not
    reliably respect z_index/occlusion by later-added filled shapes -
    confirmed via isolated repro, in both `Scene` and `MovingCameraScene` -
    so once a traced curve is done being drawn and is meant to persist as a
    static reference for the rest of the scene, replace it with a plain
    VMobject before any later `make_text_bg`-covered text might overlap it.
    Caller must `self.remove(traced_path)` / `self.add(result)`. See
    manim_notes.md."""
    frozen = VMobject(stroke_color=traced_path.stroke_color, stroke_width=traced_path.stroke_width)
    frozen.set_points(traced_path.get_points())
    return frozen


def make_connector() -> DashedLine:
    """A dashed connector line (face<->graph point, or graph<->graph
    point), styled and z-ordered consistently across this topic."""
    line = DashedLine(color=CONNECTOR_LINE_COLOR)
    line.set_z_index(CONNECTOR_Z_INDEX)
    return line


def make_readout(label_tex: str, get_value, position: np.ndarray, color: str = FORMULA, num_decimal_places: int = 1):
    """A simple "label = value" readout (e.g. "v=2.0") at a fixed screen
    position - deliberately plain, not a meter/gauge widget. Same
    unattached-updater contract as make_timer below."""
    label = MathTex(label_tex, color=color)
    value = DecimalNumber(get_value(), num_decimal_places=num_decimal_places, color=color)
    label.move_to(position, aligned_edge=LEFT)
    group = VGroup(label, value)

    def update(group: VGroup) -> None:
        label, value = group
        value.set_value(get_value())
        value.next_to(label, buff=0.15)

    update(group)
    return group, update


def make_timer(position: np.ndarray, get_time_value):
    """A "t = X.X s" readout. Returns the mobjects and their update
    functions, unattached: play any entrance animation first, then attach
    (see manim_notes.md > DecimalNumber + updater)."""
    timer_label = MathTex("t=", color=FORMULA)
    timer_value = DecimalNumber(get_time_value(), num_decimal_places=1, color=FORMULA)
    timer_unit = MathTex("\\mathrm{s}", color=FORMULA)
    timer_label.move_to(position)

    def update_timer_value(mob: DecimalNumber) -> None:
        mob.set_value(get_time_value())
        mob.next_to(timer_label, buff=0.15)

    def update_timer_unit(mob: MathTex) -> None:
        mob.next_to(timer_value, buff=0.1)

    update_timer_value(timer_value)
    update_timer_unit(timer_unit)
    return timer_label, timer_value, timer_unit, update_timer_value, update_timer_unit
