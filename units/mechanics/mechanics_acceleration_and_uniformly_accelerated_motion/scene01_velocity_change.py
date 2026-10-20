"""Scene 1: Introducing motion whose velocity changes (revised per video review).

Implements storyboard.md > Scene 1's revised three beats:
  1-2. Two parallel "3-stage" build-ups - one for constant velocity, one
     for the topic's main accelerating example (v0=0, a=motion.ACCEL_A) -
     each showing the *same* motion three times: (a) alone, full-screen,
     no axis, with a big label right below the motion; (b) alone again
     after rotating 90° ccw into the vertical face_axis convention, with
     the label migrating to the upper-right corner as "😁" moves left;
     (c) a third time with x-t and v-t graphs newly added and synced (this
     third pass is what earlier drafts called "beat 1"/"beat 2"). The word
     "acceleration" itself is deliberately never shown in this scene
     (deferred to scene 2). No tangent line is drawn for the
     constant-velocity part - its x-t graph is already a straight line, so
     a tangent adds nothing (review: don't draw a tangent on a straight
     line); the accelerating part's x-t graph is a parabola, so its tangent
     is shown as usual. Only "😁"<->x-t is connected by a dashed line -
     forcing one all the way to the v-t graph isn't needed (review).
  3. The accelerating build-up's ending state is kept (not faded): the x-t
     graph shifts up, the v-t graph shifts down, and "How much is it
     accelerating?" appears in the gap between them - ending on a question,
     not an answer.

X_RANGE/V_RANGE ([0,9,3] / [0,6,2]) are shared by both build-ups so both
motions' end values land exactly on the axes' top ticks (v=3 flat ->
x(3)=9; v0=0,a=2 -> x(3)=9, v(3)=6).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import DOWN, RIGHT, UP, Dot, FadeIn, FadeOut, Line, MathTex, Scene, Text, TracedPath, ValueTracker, Write, linear

from common.colors import BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.face import make_face
from common.graph_layout import make_t_axis, make_value_axis
from units.mechanics.mechanics_acceleration_and_uniformly_accelerated_motion import layout, motion

X_RANGE = [0, 9, 3]
V_RANGE = [0, 6, 2]
BEAT1_V = 3.0  # m/s, constant-velocity contrast example

TEASER_START_X = -6.2
TEASER_END_X = 5.8

STAGE_DRAW_TIME = 3.0  # seconds of screen time to cross T_RANGE's full [0,3]
INTRO_TIME = 0.4
ROTATE_TIME = 1.6
TICKS_REVEAL_TIME = 0.5
HOLD_TIME = 0.5
FADE_TIME = 0.6

LABEL_BIG_FONT = 36
LABEL_SMALL_FONT = 24
LABEL_START_POS = np.array([0.0, -1.3, 0.0])  # right below the teaser's motion path (y=0)
LABEL_END_POS = np.array([2.6, 3.7, 0.0])  # upper-right, clear of the x-t graph title above graph_x_axis
LABEL_SCALE = LABEL_SMALL_FONT / LABEL_BIG_FONT
TANGENT_HALF_SPAN = 0.3

QUESTION_TEXT = "How much is it accelerating?"
GRAPH_SHIFT = 0.9  # how far the x-t/v-t rows separate for beat 3


class Scene01VelocityChange(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --- Part A: motion at constant velocity. Fully faded out at the end. ---
        self._play_three_stage_intro(
            label_text="Motion at constant velocity",
            teaser_x_fn=lambda t: TEASER_START_X + (TEASER_END_X - TEASER_START_X) * (t / 3.0),
            teaser_t_max=3.0,
            x_of_t=lambda t: BEAT1_V * t,
            v_of_t=lambda t: BEAT1_V,
            show_tangent=False,  # its x-t graph is already a straight line
        )
        self.wait(HOLD_TIME)
        self.play(FadeOut(*self.mobjects), run_time=FADE_TIME)

        # --- Part B: accelerating motion. Kept on screen for beat 3. ---
        mobs = self._play_three_stage_intro(
            label_text="-> Accelerating motion",
            teaser_x_fn=lambda t: TEASER_START_X + 3.0 * t**2,
            teaser_t_max=2.0,
            x_of_t=motion.position_ua,
            v_of_t=motion.velocity_ua,
            show_tangent=True,
        )
        self.wait(HOLD_TIME)

        # --- Beat 3: shift the two graphs apart and ask the question -
        # no new object, no formula, no mention of "acceleration". ---
        self.play(
            mobs["graph_x_axis"].animate.shift(UP * GRAPH_SHIFT),
            mobs["x_axis_label"].animate.shift(UP * GRAPH_SHIFT),
            mobs["graph_t_axis"].animate.shift(UP * GRAPH_SHIFT),
            mobs["x_title"].animate.shift(UP * GRAPH_SHIFT),
            mobs["v_axis"].animate.shift(DOWN * GRAPH_SHIFT),
            mobs["v_axis_label"].animate.shift(DOWN * GRAPH_SHIFT),
            mobs["v_t_axis"].animate.shift(DOWN * GRAPH_SHIFT),
            mobs["v_title"].animate.shift(DOWN * GRAPH_SHIFT),
            mobs["x_curve"].animate.shift(UP * GRAPH_SHIFT),
            mobs["v_curve"].animate.shift(DOWN * GRAPH_SHIFT),
            run_time=1.2,
        )
        question = Text(QUESTION_TEXT, color=FORMULA, font_size=30)
        question.move_to(np.array([layout.GRAPH_ORIGIN_X + layout.T_AXIS_LENGTH / 2, 0.0, 0.0]))
        self.play(Write(question), run_time=INTRO_TIME)
        self.wait(HOLD_TIME * 2.5)

        self.play(FadeOut(*self.mobjects), run_time=FADE_TIME)

    def _play_three_stage_intro(self, label_text: str, teaser_x_fn, teaser_t_max: float, x_of_t, v_of_t, show_tangent: bool) -> dict:
        """The shared "3 repeats" build-up: (1) alone/full-screen, label big
        right below the motion; (2) alone on the rotated vertical axis,
        label migrating to the upper-right corner as "😁" moves left;
        (3) with x-t+v-t added and synced (a live tangent line too, unless
        show_tangent=False - review: don't draw a tangent on a straight
        line). label_text is
        shown throughout and returned (unfaded) so the caller can decide
        whether/when to remove it. Returns the mobjects the caller may
        still need (used by beat 3 for Part B only)."""
        label = Text(label_text, color=FORMULA, font_size=LABEL_BIG_FONT)
        label.move_to(LABEL_START_POS)

        # --- Stage 1: alone, full screen, no axis. ---
        t_tracker = ValueTracker(0.0)
        face = make_face(height=layout.FACE_HEIGHT)

        def update_face_horizontal(mob) -> None:
            mob.move_to(np.array([teaser_x_fn(t_tracker.get_value()), 0.0, 0.0]))

        update_face_horizontal(face)
        face.add_updater(update_face_horizontal)

        self.play(FadeIn(face), Write(label), run_time=INTRO_TIME)
        self.play(t_tracker.animate.set_value(teaser_t_max), run_time=STAGE_DRAW_TIME, rate_func=linear)
        face.remove_updater(update_face_horizontal)

        # --- Rotate the traveled path 90° ccw while shrinking it into the
        # real, ticked face_axis used from here on (same technique as
        # scene04's own teaser -> face_axis bridge); the label migrates to
        # the corner in the same motion, as "😁" moves left. ---
        source_line = Line(np.array([TEASER_START_X, 0.0, 0.0]), np.array([TEASER_END_X, 0.0, 0.0]), color=FORMULA)
        self.play(FadeIn(source_line), run_time=INTRO_TIME)

        face_axis = make_value_axis(np.array([layout.FACE_AXIS_X, layout.TWO_ROW_UPPER_Y, 0.0]), X_RANGE, layout.TWO_ROW_AXIS_LENGTH)
        face_axis_ticks, face_axis_numbers = face_axis.ticks, face_axis.numbers
        face_axis.remove(face_axis_ticks, face_axis_numbers)

        self.play(
            face.animate.move_to(face_axis.number_to_point(0.0) + RIGHT * layout.FACE_GAP),
            source_line.animate.put_start_and_end_on(face_axis.get_start(), face_axis.get_end()),
            label.animate.scale(LABEL_SCALE).move_to(LABEL_END_POS),
            run_time=ROTATE_TIME,
        )
        self.remove(source_line)
        self.add(face_axis)
        face_axis.add_ticks()
        face_axis.add_numbers()
        face_axis.ticks.set_opacity(0)
        face_axis.numbers.set_opacity(0)
        self.play(face_axis.ticks.animate.set_opacity(1), face_axis.numbers.animate.set_opacity(1), run_time=TICKS_REVEAL_TIME)

        # --- Stage 2: alone again, now on the vertical face_axis. ---
        def update_face_on_axis(mob) -> None:
            mob.move_to(face_axis.number_to_point(x_of_t(t_tracker.get_value())) + RIGHT * layout.FACE_GAP)

        t_tracker.set_value(0.0)
        face.update()
        update_face_on_axis(face)
        face.add_updater(update_face_on_axis)

        self.play(t_tracker.animate.set_value(layout.T_RANGE[1]), run_time=STAGE_DRAW_TIME, rate_func=linear)
        self.wait(HOLD_TIME * 0.5)

        # --- Stage 3: x-t + v-t graphs join; synced replay. Only "😁"<->x-t
        # is connected (review: don't force a connection between 😁 and the
        # v-t graph). ---
        upper_origin = np.array([layout.GRAPH_ORIGIN_X, layout.TWO_ROW_UPPER_Y, 0.0])
        lower_origin = np.array([layout.GRAPH_ORIGIN_X, layout.TWO_ROW_LOWER_Y, 0.0])
        graph_x_axis = make_value_axis(upper_origin, X_RANGE, layout.TWO_ROW_AXIS_LENGTH)
        graph_t_axis = make_t_axis(upper_origin, layout.T_RANGE, layout.T_AXIS_LENGTH)
        v_axis = make_value_axis(lower_origin, V_RANGE, layout.TWO_ROW_AXIS_LENGTH)
        v_t_axis = make_t_axis(lower_origin, layout.T_RANGE, layout.T_AXIS_LENGTH)
        x_axis_label = MathTex("x", color=PRIMARY, font_size=32).next_to(graph_x_axis.get_end(), UP, buff=0.2)
        t_axis_label = MathTex("t", color=FORMULA, font_size=32).next_to(graph_t_axis.get_end(), RIGHT, buff=0.2)
        v_axis_label = MathTex("v", color=VELOCITY, font_size=32).next_to(v_axis.get_end(), UP, buff=0.2)
        x_title = layout.make_graph_title("x-t graph", x_axis_label, color=PRIMARY)
        v_title = layout.make_graph_title("v-t graph", v_axis_label, color=VELOCITY)

        self.play(
            FadeIn(graph_x_axis, graph_t_axis, v_axis, v_t_axis),
            Write(x_axis_label), Write(t_axis_label), Write(v_axis_label), Write(x_title), Write(v_title),
            run_time=INTRO_TIME,
        )

        def x_point(t: float, x: float) -> np.ndarray:
            return np.array([graph_t_axis.number_to_point(t)[0], graph_x_axis.number_to_point(x)[1], 0.0])

        def v_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        t_tracker.set_value(0.0)
        face.remove_updater(update_face_on_axis)
        face.update()
        update_face_on_axis(face)
        face.add_updater(update_face_on_axis)

        x_dot = Dot(color=PRIMARY)
        v_dot = Dot(color=VELOCITY)
        face_connector = layout.make_connector()
        tangent_line = Line(color=VELOCITY, stroke_width=3)

        def update_x_dot(mob) -> None:
            t = t_tracker.get_value()
            mob.move_to(x_point(t, x_of_t(t)))

        def update_v_dot(mob) -> None:
            t = t_tracker.get_value()
            mob.move_to(v_point(t, v_of_t(t)))

        def update_face_connector(mob) -> None:
            mob.put_start_and_end_on(face.get_center(), x_dot.get_center())

        def update_tangent_line(mob) -> None:
            t = t_tracker.get_value()
            new_line = layout.make_tangent_line(x_point, t, x_of_t(t), v_of_t(t), TANGENT_HALF_SPAN, VELOCITY)
            mob.become(new_line)

        update_x_dot(x_dot)
        update_v_dot(v_dot)
        update_face_connector(face_connector)
        if show_tangent:
            update_tangent_line(tangent_line)

        intro_mobs = [x_dot, v_dot, face_connector, *([tangent_line] if show_tangent else [])]
        self.play(FadeIn(*intro_mobs), run_time=INTRO_TIME)

        x_dot.add_updater(update_x_dot)
        v_dot.add_updater(update_v_dot)
        face_connector.add_updater(update_face_connector)
        if show_tangent:
            tangent_line.add_updater(update_tangent_line)

        x_traced = TracedPath(x_dot.get_center, stroke_color=PRIMARY, stroke_width=3)
        v_traced = TracedPath(v_dot.get_center, stroke_color=VELOCITY, stroke_width=3)
        self.add(x_traced, v_traced)

        self.play(t_tracker.animate.set_value(layout.T_RANGE[1]), run_time=STAGE_DRAW_TIME, rate_func=linear)
        self.wait(HOLD_TIME)

        x_traced.clear_updaters()
        v_traced.clear_updaters()
        face.remove_updater(update_face_on_axis)
        x_dot.remove_updater(update_x_dot)
        v_dot.remove_updater(update_v_dot)
        face_connector.remove_updater(update_face_connector)
        if show_tangent:
            tangent_line.remove_updater(update_tangent_line)
        self.play(FadeOut(*intro_mobs), run_time=FADE_TIME)

        return {
            "label": label,
            "face_axis": face_axis,
            "face": face,
            "graph_x_axis": graph_x_axis,
            "graph_t_axis": graph_t_axis,
            "x_axis_label": x_axis_label,
            "t_axis_label": t_axis_label,
            "x_title": x_title,
            "v_axis": v_axis,
            "v_t_axis": v_t_axis,
            "v_axis_label": v_axis_label,
            "v_title": v_title,
            "x_curve": x_traced,
            "v_curve": v_traced,
        }
