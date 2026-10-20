"""Scene 6: Wrap-up.

Implements storyboard.md > Scene 6 (a single beat):
  Scene05's ending layout (face axis, x-t graph, v-t graph, all in its
  compressed upper/lower arrangement) is rebuilt, then compressed further —
  horizontally only, same vertical scale/position — and moved into the left
  half of the screen, leaving the right half free for the storyboard's
  "on the right side of the screen" checklist. The main demo's completed x-t/v-t curves are then
  drawn, followed by four checkmarked takeaways appearing one at a time.
  Finally, a colored guide line connects the x-t graph's tangent point to
  the v-t graph's corresponding point, emphasizing that the two graphs show
  the same motion from different perspectives, before the whole scene
  fades out.

Continuity with scene05: this scene rebuilds scene05's exact ending
geometry (common.graph_layout constants plus scene05's own
COMPRESSED_AXIS_LENGTH/UPPER_ORIGIN_Y/LOWER_ORIGIN_Y/V_VALUE_RANGE/
COMPRESSED_NUMBERS_TO_EXCLUDE, imported directly) before compressing it
again — horizontally only this time — rather than jumping straight to an
already-doubly-compressed state.

As in scene05's own horizontal (t-)axes, the two t-axes here change length,
so their ticks/numbers are detached/regenerated around the animation rather
than given to a naive Transform, which would visibly warp the number
glyphs mid-animation (see manim_notes.md > NumberLine). The vertical axes
and face_axis only change position here (not length), so a plain shift is
safe for them.

The checklist lines are the one exception to this project's usual "no
narration text on screen" rule: storyboard.md lists them under this beat's
Visual, not its Narration, so they are meant to be read on screen.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import LEFT, RIGHT, UP, Create, Dot, FadeIn, FadeOut, Line, MathTex, Scene, Text, VMobject

from common.colors import BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.graph_layout import FACE_AXIS_X, GRAPH_ORIGIN, make_t_axis, make_value_axis, make_vertical_x_axis
from common.motion_profile import MAIN_X0, find_key_velocity_events, position_v5, velocity_v5
from common.position_track import TRACK_X_MIN, make_tracked_face
from units.mechanics.mechanics_how_to_express_movements.scene05_velocity_time_graph import (
    COMPRESSED_AXIS_LENGTH,
    COMPRESSED_NUMBERS_TO_EXCLUDE,
    LOWER_ORIGIN_Y,
    UPPER_ORIGIN_Y,
    V_VALUE_RANGE,
)

FINAL_T = 7.0  # the main demo's end of range, matching scene05's t-window

# This scene's own further (horizontal-only) compression: same vertical
# scale/position as scene05 (UPPER_ORIGIN_Y/LOWER_ORIGIN_Y/
# COMPRESSED_AXIS_LENGTH, all imported, unchanged), just a shorter t-axis
# moved further left, to clear the right half for the checklist.
FACE_AXIS_X_NEW = -6.5
GRAPH_ORIGIN_X_NEW = -4.3
T_AXIS_LENGTH_NEW = 3.3

CHECKLIST_X = 0.3
CHECKLIST_TOP_Y = 2.2
CHECKLIST_LINE_GAP = 0.9
CHECKLIST_FONT_SIZE = 20
CHECKLIST_LINES = [
    "Motion can be expressed through position and time",
    "The x-t graph shows how position changes",
    "The slope of the tangent on the x-t graph is the velocity",
    "The v-t graph shows how velocity changes",
]

CONTINUITY_FADE_TIME = 0.6
COMPRESS_TIME = 1.5
TICKS_REVEAL_TIME = 0.8
CURVE_DRAW_TIME = 1.5

CHECKLIST_ITEM_TIME = 0.6
CHECKLIST_ITEM_GAP = 0.5
GUIDE_LINE_TIME = 1.2
HOLD_TIME = 2.0
FINAL_FADE_TIME = 2.0


class Scene06Summary(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --- Continuity: rebuild scene05's exact ending layout (bare axes,
        # its own compressed upper/lower arrangement, no curves/face). ---
        upper_origin = np.array([GRAPH_ORIGIN[0], UPPER_ORIGIN_Y, 0.0])
        lower_origin = np.array([GRAPH_ORIGIN[0], LOWER_ORIGIN_Y, 0.0])
        face_axis = make_vertical_x_axis(
            np.array([FACE_AXIS_X, UPPER_ORIGIN_Y, 0.0]),
            length=COMPRESSED_AXIS_LENGTH,
            extra_numbers_to_exclude=COMPRESSED_NUMBERS_TO_EXCLUDE,
        )
        graph_x_axis = make_vertical_x_axis(
            upper_origin, length=COMPRESSED_AXIS_LENGTH, extra_numbers_to_exclude=COMPRESSED_NUMBERS_TO_EXCLUDE
        )
        graph_t_axis = make_t_axis(upper_origin)
        v_axis = make_value_axis(lower_origin, V_VALUE_RANGE, COMPRESSED_AXIS_LENGTH)
        v_t_axis = make_t_axis(lower_origin)
        x_axis_label = MathTex("x", color=FORMULA).next_to(graph_x_axis.get_end(), UP, buff=0.2)
        t_axis_label = MathTex("t", color=FORMULA).next_to(graph_t_axis.get_end(), RIGHT, buff=0.2)
        v_axis_label = MathTex("v", color=VELOCITY).next_to(v_axis.get_end(), UP, buff=0.2)

        self.play(
            FadeIn(face_axis, graph_x_axis, graph_t_axis, v_axis, v_t_axis, x_axis_label, t_axis_label, v_axis_label),
            run_time=CONTINUITY_FADE_TIME,
        )

        # --- Compress further, horizontally only, and move into the left
        # half: same vertical scale/position as scene05, just a shorter
        # t-axis moved further left. graph_t_axis/v_t_axis's ticks/numbers
        # are detached/regenerated around the length change (see module
        # docstring); face_axis/graph_x_axis/v_axis only shift position, so
        # a plain shift is safe for them. ---
        new_upper_origin = np.array([GRAPH_ORIGIN_X_NEW, UPPER_ORIGIN_Y, 0.0])
        new_lower_origin = np.array([GRAPH_ORIGIN_X_NEW, LOWER_ORIGIN_Y, 0.0])
        face_shift = np.array([FACE_AXIS_X_NEW - FACE_AXIS_X, 0.0, 0.0])
        graph_shift = np.array([GRAPH_ORIGIN_X_NEW - GRAPH_ORIGIN[0], 0.0, 0.0])

        graph_t_axis_target = make_t_axis(new_upper_origin, length=T_AXIS_LENGTH_NEW)
        v_t_axis_target = make_t_axis(new_lower_origin, length=T_AXIS_LENGTH_NEW)

        graph_t_ticks, graph_t_numbers = graph_t_axis.ticks, graph_t_axis.numbers
        graph_t_axis.remove(graph_t_ticks, graph_t_numbers)
        v_t_ticks, v_t_numbers = v_t_axis.ticks, v_t_axis.numbers
        v_t_axis.remove(v_t_ticks, v_t_numbers)

        self.play(
            face_axis.animate.shift(face_shift),
            graph_x_axis.animate.shift(graph_shift),
            v_axis.animate.shift(graph_shift),
            x_axis_label.animate.shift(graph_shift),
            v_axis_label.animate.shift(graph_shift),
            graph_t_axis.animate.put_start_and_end_on(graph_t_axis_target.get_start(), graph_t_axis_target.get_end()),
            v_t_axis.animate.put_start_and_end_on(v_t_axis_target.get_start(), v_t_axis_target.get_end()),
            t_axis_label.animate.move_to(graph_t_axis_target.get_end()).shift(RIGHT * 0.3),
            run_time=COMPRESS_TIME,
        )

        graph_t_axis.add_ticks()
        graph_t_axis.add_numbers()
        v_t_axis.add_ticks()
        v_t_axis.add_numbers()
        # A plain opacity animate on the freshly regenerated children, not
        # FadeIn: FadeIn(parent.ticks, parent.numbers) breaks the parent
        # axis line's own rendering (see manim_notes.md).
        graph_t_axis.ticks.set_opacity(0)
        graph_t_axis.numbers.set_opacity(0)
        v_t_axis.ticks.set_opacity(0)
        v_t_axis.numbers.set_opacity(0)
        self.play(
            graph_t_axis.ticks.animate.set_opacity(1),
            graph_t_axis.numbers.animate.set_opacity(1),
            v_t_axis.ticks.animate.set_opacity(1),
            v_t_axis.numbers.animate.set_opacity(1),
            run_time=TICKS_REVEAL_TIME,
        )

        def x_graph_point(t: float, x: float) -> np.ndarray:
            return np.array([graph_t_axis.number_to_point(t)[0], graph_x_axis.number_to_point(x)[1], 0.0])

        def v_graph_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        # --- The main demo's completed curves, and the "😁" at its final
        # resting position. ---
        face_x = position_v5(FINAL_T, MAIN_X0)
        face, _ = make_tracked_face(face_axis, lambda: face_x)

        sample_ts = np.linspace(0.0, FINAL_T, 200)
        x_curve = VMobject(color=PRIMARY, stroke_width=3)
        x_curve.set_points_smoothly([x_graph_point(t, position_v5(t, MAIN_X0)) for t in sample_ts])
        v_curve = VMobject(color=VELOCITY, stroke_width=3)
        v_curve.set_points_smoothly([v_graph_point(t, velocity_v5(t)) for t in sample_ts])

        self.play(FadeIn(face), Create(x_curve), Create(v_curve), run_time=CURVE_DRAW_TIME)

        # --- Checklist, one line at a time. ---
        for index, line in enumerate(CHECKLIST_LINES):
            text = Text(f"✓ {line}", color=FORMULA, font_size=CHECKLIST_FONT_SIZE)
            text.move_to([CHECKLIST_X, CHECKLIST_TOP_Y - index * CHECKLIST_LINE_GAP, 0.0], aligned_edge=LEFT)
            self.play(FadeIn(text), run_time=CHECKLIST_ITEM_TIME)
            self.wait(CHECKLIST_ITEM_GAP)

        # --- Connect the x-t graph's tangent point and the v-t graph's
        # corresponding point with a colored guide line, at the same
        # max-velocity moment emphasized in scenes 4-5. ---
        events = find_key_velocity_events(0.0, FINAL_T, velocity_fn=velocity_v5)
        max_t = next(t for t, kind in events if kind == "max")
        x_point = x_graph_point(max_t, position_v5(max_t, MAIN_X0))
        v_point = v_graph_point(max_t, velocity_v5(max_t))

        guide_dots = (Dot(x_point, color=VELOCITY, radius=0.05), Dot(v_point, color=VELOCITY, radius=0.05))
        guide_line = Line(x_point, v_point, color=VELOCITY, stroke_width=3)
        self.play(FadeIn(*guide_dots), Create(guide_line), run_time=GUIDE_LINE_TIME)
        self.wait(HOLD_TIME)

        self.play(FadeOut(*self.mobjects), run_time=FINAL_FADE_TIME)
