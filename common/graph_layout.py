"""Shared x-t graph layout, used by scene02 and scene03 so the "😁"'s own
position axis and the x-t graph sit in the same place on screen in both
scenes (see skills/physics-video-review/SKILL.md > Layout)."""

import numpy as np
from manim import GREY_C, LEFT, PI, config
from manim.mobject.graphing.number_line import NumberLine

from common.colors import FORMULA
from common.position_track import TRACK_X_MAX, TRACK_X_MIN, TRACK_X_STEP

FACE_AXIS_X = -5.5  # screen x of the "😁"'s own (rotated) position indicator
GRAPH_ORIGIN = np.array([-1.5, -2.0, 0.0])  # the graph's x-t origin, separate from the face axis

ROTATED_X_AXIS_LENGTH = 4.5  # on-screen height of a vertical x-axis, after rescaling
GRAPH_T_RANGE = [0, 7, 1]
T_AXIS_LENGTH = 7.0

# The line connecting the "😁" to the graph must be visually distinct from the
# graph's own blue data curve/axes, and must be drawn behind the "😁".
CONNECTOR_LINE_COLOR = GREY_C
FACE_Z_INDEX = 1
CONNECTOR_Z_INDEX = 0

# Treat this much inside the true camera frame edge as "off-screen", so a
# plotted point visibly exits the frame rather than stopping exactly at it.
_FRAME_MARGIN = 0.3
VISIBLE_X_MIN = -config.frame_width / 2 + _FRAME_MARGIN
VISIBLE_X_MAX = config.frame_width / 2 - _FRAME_MARGIN
VISIBLE_Y_MIN = -config.frame_height / 2 + _FRAME_MARGIN
VISIBLE_Y_MAX = config.frame_height / 2 - _FRAME_MARGIN


def make_vertical_x_axis(
    origin: np.ndarray, length: float | None = None, extra_numbers_to_exclude: list | None = None
) -> NumberLine:
    """A vertical position axis (same range as the shared position track,
    but an overridable length) at the given screen origin. "0" and
    TRACK_X_MIN (the tick right below 0) are excluded: where this axis
    crosses a t-axis at the same origin, those two labels land almost
    exactly where the t-axis's own "1" label sits, close enough to overlap
    it. extra_numbers_to_exclude thins out further labels beyond those two
    (same values, just fewer of them printed) for callers compressing this
    axis to a much shorter length than ROTATED_X_AXIS_LENGTH, where the full
    TRACK_X_STEP density would otherwise overlap illegibly."""
    axis = NumberLine(
        x_range=[TRACK_X_MIN, TRACK_X_MAX, TRACK_X_STEP],
        length=length if length is not None else ROTATED_X_AXIS_LENGTH,
        color=FORMULA,
        include_ticks=True,
        include_numbers=True,
        numbers_to_exclude=[0, TRACK_X_MIN, *(extra_numbers_to_exclude or [])],
        rotation=PI / 2,
        label_direction=LEFT,
    )
    axis.shift(origin - axis.number_to_point(0))
    return axis


def make_value_axis(origin: np.ndarray, value_range: list, length: float) -> NumberLine:
    """A vertical value axis (position, velocity, ...) at the given screen
    origin, for an arbitrary range - unlike make_vertical_x_axis above, which
    is hardcoded to the shared position track's range."""
    axis = NumberLine(
        x_range=value_range,
        length=length,
        color=FORMULA,
        include_ticks=True,
        include_numbers=True,
        numbers_to_exclude=[0],
        rotation=PI / 2,
        label_direction=LEFT,
    )
    axis.shift(origin - axis.number_to_point(0))
    return axis


def make_t_axis(origin: np.ndarray = GRAPH_ORIGIN, t_range=None, length: float | None = None) -> NumberLine:
    """A horizontal time axis at the given screen origin. The "0" label is
    excluded for the same reason as make_vertical_x_axis."""
    axis = NumberLine(
        x_range=t_range if t_range is not None else GRAPH_T_RANGE,
        length=length if length is not None else T_AXIS_LENGTH,
        color=FORMULA,
        include_ticks=True,
        include_numbers=True,
        numbers_to_exclude=[0],
    )
    axis.shift(origin - axis.number_to_point(0))
    return axis


def find_offscreen_time(
    t_start: float,
    t_axis: NumberLine,
    vertical_x_axis: NumberLine,
    x_of_t,
    step: float = 0.02,
    t_limit: float = 60.0,
) -> float:
    """The first t >= t_start (marching forward) at which the plotted point
    (t, x_of_t(t)) leaves the visible camera frame, so a plotting animation
    can run until the curve is actually cut off by the screen edge instead of
    stopping at an arbitrary fixed duration."""
    t = t_start
    while t < t_start + t_limit:
        screen_x = t_axis.number_to_point(t)[0]
        screen_y = vertical_x_axis.number_to_point(x_of_t(t))[1]
        if not (VISIBLE_X_MIN <= screen_x <= VISIBLE_X_MAX and VISIBLE_Y_MIN <= screen_y <= VISIBLE_Y_MAX):
            return t
        t += step
    return t_start + t_limit
