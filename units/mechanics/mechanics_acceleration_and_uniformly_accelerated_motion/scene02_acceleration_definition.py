"""Scene 2: What acceleration means (revised per video review).

Implements storyboard.md > Scene 2's revised beats, continuing scene01's
face-axis / x-t / v-t layout (rebuilt fresh here, per this project's
"continuity rebuild" idiom):
  1. The main running example (v0=0, a=motion.ACCEL_A) plays once (no
     second replay - review says it's unnecessary) while a plain "v="
     readout counts up and a live tangent line rides the x-t curve; a
     "+2 m/s" delta label appears, delayed, during the *next* second's
     travel.
  2. Layout transition: face/x-t shrink into the upper-left corner, the
     v-t graph grows to fill most of the screen (both axes' t-range also
     extends left, in one smooth simultaneous resize) - review: enlarge it
     since we're now focusing on the v-t graph.
  3. Two points at t=1,2 are marked on the (now large) v-t line; a
     horizontal Δt arrow is drawn (`GrowArrow`), then a vertical Δv arrow -
     both dynamically drawn, neither removed afterward.
  4. The camera zooms onto that region and stays zoomed for the algebra:
     a=Δv/Δt=... is revealed one "=" segment at a time (never several at
     once - review's common note), then the unit derivation keeps the
     original fraction on screen and animates the simplification to the
     right of a new "=", rather than replacing it in place.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    MathTex,
    MovingCameraScene,
    Succession,
    Text,
    TracedPath,
    Transform,
    ValueTracker,
    VMobject,
    Wait,
    Write,
    linear,
)

from common.colors import ACCELERATION, BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.graph_layout import make_t_axis, make_value_axis
from units.mechanics.mechanics_acceleration_and_uniformly_accelerated_motion import layout, motion

X_RANGE = [0, 9, 3]
V_RANGE = [0, 6, 2]

SEGMENT_RUN_TIME = 1.4
INTRO_TIME = 0.4
FADE_TIME = 0.5
DELTA_HOLD_TIME = 0.7
TANGENT_HALF_SPAN = 0.3

BEAT_GAP_TIME = 0.8

# --- Layout-transition targets: face/x-t shrink to a corner, v-t grows. ---
SMALL_AXIS_LENGTH = 1.1
SMALL_UPPER_Y = 2.7
BIG_V_AXIS_LENGTH = 3.9
BIG_V_ORIGIN_Y = -2.3
T_AXIS_LENGTH_NEW = 7.0
GRAPH_ORIGIN_X_NEW = -2.5
RESIZE_TIME = 1.6

SENTENCE_TEXT = "Divide the change in velocity by the change in time"
DEFINITION_TEXT = "acceleration = the change in velocity per unit time"

ZOOM_SCALE = 0.5


class Scene02AccelerationDefinition(MovingCameraScene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --- Continuity: rebuild scene01's ending layout. ---
        upper_origin = np.array([layout.GRAPH_ORIGIN_X, layout.TWO_ROW_UPPER_Y, 0.0])
        lower_origin = np.array([layout.GRAPH_ORIGIN_X, layout.TWO_ROW_LOWER_Y, 0.0])
        face_axis, graph_x_axis = layout.make_face_and_x_axis(X_RANGE, layout.TWO_ROW_AXIS_LENGTH, layout.TWO_ROW_UPPER_Y)
        graph_t_axis = make_t_axis(upper_origin, layout.T_RANGE, layout.T_AXIS_LENGTH)
        v_axis = make_value_axis(lower_origin, V_RANGE, layout.TWO_ROW_AXIS_LENGTH)
        v_t_axis = make_t_axis(lower_origin, layout.T_RANGE, layout.T_AXIS_LENGTH)
        x_axis_label = MathTex("x", color=PRIMARY, font_size=32).next_to(graph_x_axis.get_end(), UP, buff=0.2)
        t_axis_label = MathTex("t", color=FORMULA, font_size=32).next_to(graph_t_axis.get_end(), RIGHT, buff=0.2)
        v_axis_label = MathTex("v", color=VELOCITY, font_size=32).next_to(v_axis.get_end(), UP, buff=0.2)
        x_title = layout.make_graph_title("x-t graph", x_axis_label, color=PRIMARY)
        v_title = layout.make_graph_title("v-t graph", v_axis_label, color=VELOCITY)

        self.play(
            FadeIn(face_axis, graph_x_axis, graph_t_axis, v_axis, v_t_axis),
            Write(x_axis_label), Write(t_axis_label), Write(v_axis_label), Write(x_title), Write(v_title),
            run_time=INTRO_TIME,
        )

        def x_point(t: float, x: float) -> np.ndarray:
            return np.array([graph_t_axis.number_to_point(t)[0], graph_x_axis.number_to_point(x)[1], 0.0])

        def v_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        # --- Beat 1: watch velocity change through a concrete numeric example (single pass, no replay). ---
        t_tracker = ValueTracker(0.0)
        face, face_update = layout.make_tracked_face(face_axis, lambda: motion.position_ua(t_tracker.get_value()))
        x_dot = Dot(color=PRIMARY)
        v_dot = Dot(color=VELOCITY)
        face_connector = layout.make_connector()
        tangent_line = layout.make_tangent_line(x_point, 0.0, 0.0, 0.0, TANGENT_HALF_SPAN, VELOCITY)

        def update_x_dot(mob) -> None:
            t = t_tracker.get_value()
            mob.move_to(x_point(t, motion.position_ua(t)))

        def update_v_dot(mob) -> None:
            t = t_tracker.get_value()
            mob.move_to(v_point(t, motion.velocity_ua(t)))

        def update_face_connector(mob) -> None:
            mob.put_start_and_end_on(face.get_center(), x_dot.get_center())

        def update_tangent_line(mob) -> None:
            t = t_tracker.get_value()
            mob.become(layout.make_tangent_line(x_point, t, motion.position_ua(t), motion.velocity_ua(t), TANGENT_HALF_SPAN, VELOCITY))

        update_x_dot(x_dot)
        update_v_dot(v_dot)
        update_face_connector(face_connector)
        update_tangent_line(tangent_line)

        readout_group, update_readout = layout.make_readout(
            "v=", lambda: motion.velocity_ua(t_tracker.get_value()), layout.READOUT_POS, color=VELOCITY
        )

        self.play(
            FadeIn(face, x_dot, v_dot, face_connector, tangent_line), Write(readout_group), run_time=INTRO_TIME
        )

        x_dot.add_updater(update_x_dot)
        v_dot.add_updater(update_v_dot)
        face_connector.add_updater(update_face_connector)
        tangent_line.add_updater(update_tangent_line)
        readout_group.add_updater(update_readout)

        x_traced = TracedPath(x_dot.get_center, stroke_color=PRIMARY, stroke_width=3)
        v_traced = TracedPath(v_dot.get_center, stroke_color=VELOCITY, stroke_width=3)
        self.add(x_traced, v_traced)

        def make_delta_label() -> MathTex:
            label = MathTex("+2\\,\\mathrm{m/s}", color=VELOCITY, font_size=32)
            label.next_to(readout_group, RIGHT, buff=0.4)
            return label

        delta1 = make_delta_label()
        delta2 = make_delta_label()
        delta3 = make_delta_label()

        def segment(end_t: float, fade_in=None, fade_out=None) -> None:
            anims = [t_tracker.animate(run_time=SEGMENT_RUN_TIME, rate_func=linear).set_value(end_t)]
            if fade_out is not None:
                anims.append(FadeOut(fade_out, run_time=0.3))
            if fade_in is not None:
                anims.append(Succession(Wait(SEGMENT_RUN_TIME * 0.5), Write(fade_in, run_time=SEGMENT_RUN_TIME * 0.5)))
            self.play(*anims)

        segment(1.0)
        segment(2.0, fade_in=delta1)
        segment(3.0, fade_in=delta2, fade_out=delta1)
        self.play(FadeOut(delta2), Write(delta3), run_time=FADE_TIME)
        self.wait(DELTA_HOLD_TIME)
        self.play(FadeOut(delta3), run_time=FADE_TIME)

        x_traced.clear_updaters()
        v_traced.clear_updaters()
        face.remove_updater(face_update)
        x_dot.remove_updater(update_x_dot)
        v_dot.remove_updater(update_v_dot)
        face_connector.remove_updater(update_face_connector)
        tangent_line.remove_updater(update_tangent_line)
        readout_group.remove_updater(update_readout)
        self.play(
            FadeOut(face, x_dot, v_dot, face_connector, tangent_line, readout_group, x_traced, v_traced),
            run_time=FADE_TIME,
        )

        # --- Layout transition: shrink face/x-t into the corner, grow v-t
        # to fill most of the screen; both t-axes extend leftward too, all
        # in one smooth simultaneous resize (review: focus on the v-t graph). ---
        new_upper_origin = np.array([GRAPH_ORIGIN_X_NEW, SMALL_UPPER_Y, 0.0])
        new_lower_origin = np.array([GRAPH_ORIGIN_X_NEW, BIG_V_ORIGIN_Y, 0.0])
        face_axis_target = make_value_axis(np.array([layout.FACE_AXIS_X, SMALL_UPPER_Y, 0.0]), X_RANGE, SMALL_AXIS_LENGTH)
        graph_x_axis_target = make_value_axis(new_upper_origin, X_RANGE, SMALL_AXIS_LENGTH)
        graph_t_axis_target = make_t_axis(new_upper_origin, layout.T_RANGE, T_AXIS_LENGTH_NEW)
        v_axis_target = make_value_axis(new_lower_origin, V_RANGE, BIG_V_AXIS_LENGTH)
        v_t_axis_target = make_t_axis(new_lower_origin, layout.T_RANGE, T_AXIS_LENGTH_NEW)

        def detach(axis):
            ticks, numbers = axis.ticks, axis.numbers
            axis.remove(ticks, numbers)
            return ticks, numbers

        face_axis_tn = detach(face_axis)
        graph_x_axis_tn = detach(graph_x_axis)
        v_axis_tn = detach(v_axis)
        graph_t_axis_tn = detach(graph_t_axis)
        v_t_axis_tn = detach(v_t_axis)

        x_axis_label_target = MathTex("x", color=PRIMARY, font_size=22).next_to(graph_x_axis_target.get_end(), UP, buff=0.12)
        t_axis_label_target = MathTex("t", color=FORMULA, font_size=22).next_to(graph_t_axis_target.get_end(), RIGHT, buff=0.12)
        v_axis_label_target = MathTex("v", color=VELOCITY, font_size=32).next_to(v_axis_target.get_end(), UP, buff=0.15)
        x_title_target = layout.make_graph_title("x-t", x_axis_label_target, color=PRIMARY)
        v_title_target = layout.make_graph_title("v-t graph", v_axis_label_target, color=VELOCITY)

        self.play(
            face_axis.animate.put_start_and_end_on(face_axis_target.get_start(), face_axis_target.get_end()),
            graph_x_axis.animate.put_start_and_end_on(graph_x_axis_target.get_start(), graph_x_axis_target.get_end()),
            graph_t_axis.animate.put_start_and_end_on(graph_t_axis_target.get_start(), graph_t_axis_target.get_end()),
            v_axis.animate.put_start_and_end_on(v_axis_target.get_start(), v_axis_target.get_end()),
            v_t_axis.animate.put_start_and_end_on(v_t_axis_target.get_start(), v_t_axis_target.get_end()),
            Transform(x_axis_label, x_axis_label_target),
            Transform(t_axis_label, t_axis_label_target),
            Transform(v_axis_label, v_axis_label_target),
            Transform(x_title, x_title_target),
            Transform(v_title, v_title_target),
            run_time=RESIZE_TIME,
        )

        for axis, (ticks, numbers) in [
            (face_axis, face_axis_tn), (graph_x_axis, graph_x_axis_tn), (v_axis, v_axis_tn),
            (graph_t_axis, graph_t_axis_tn), (v_t_axis, v_t_axis_tn),
        ]:
            axis.add_ticks()
            axis.add_numbers()
            axis.ticks.set_opacity(0)
            axis.numbers.set_opacity(0)
        self.play(
            *[axis.ticks.animate.set_opacity(1) for axis in (face_axis, graph_x_axis, v_axis, graph_t_axis, v_t_axis)],
            *[axis.numbers.animate.set_opacity(1) for axis in (face_axis, graph_x_axis, v_axis, graph_t_axis, v_t_axis)],
            run_time=0.6,
        )

        def x_point_new(t: float, x: float) -> np.ndarray:
            return np.array([graph_t_axis.number_to_point(t)[0], graph_x_axis.number_to_point(x)[1], 0.0])

        def v_point_new(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        sample_ts = np.linspace(0.0, layout.T_RANGE[1], 100)
        x_curve = VMobject(color=PRIMARY, stroke_width=2)
        x_curve.set_points_smoothly([x_point_new(t, motion.position_ua(t)) for t in sample_ts])
        v_line = VMobject(color=VELOCITY, stroke_width=3)
        v_line.set_points_smoothly([v_point_new(t, motion.velocity_ua(t)) for t in sample_ts])
        self.play(FadeIn(x_curve, v_line), run_time=INTRO_TIME)

        # --- Beat 2: mark A, B, then Δt (arrow) then Δv (arrow) - both kept. ---
        t1, t2 = 1.0, 2.0
        v1, v2 = motion.velocity_ua(t1), motion.velocity_ua(t2)
        dot_a = Dot(v_point_new(t1, v1), color=VELOCITY, radius=0.06)
        dot_b = Dot(v_point_new(t2, v2), color=VELOCITY, radius=0.06)
        self.play(FadeIn(dot_a), run_time=INTRO_TIME)
        self.wait(0.3)
        self.play(FadeIn(dot_b), run_time=INTRO_TIME)
        self.wait(BEAT_GAP_TIME * 0.5)

        dt_arrow = Arrow(v_point_new(t1, v1), v_point_new(t2, v1), color=FORMULA, buff=0.0, stroke_width=5)
        dt_label = MathTex("\\Delta t", color=FORMULA, font_size=28).next_to(dt_arrow, DOWN, buff=0.15)
        self.play(GrowArrow(dt_arrow), run_time=0.8)
        self.play(Write(dt_label), run_time=INTRO_TIME)
        self.wait(BEAT_GAP_TIME)

        dv_arrow = Arrow(v_point_new(t2, v1), v_point_new(t2, v2), color=VELOCITY, buff=0.0, stroke_width=5)
        dv_label = MathTex("\\Delta v", color=VELOCITY, font_size=28).next_to(dv_arrow, RIGHT, buff=0.15)
        self.play(GrowArrow(dv_arrow), run_time=0.8)
        self.play(Write(dv_label), run_time=INTRO_TIME)
        self.wait(BEAT_GAP_TIME)

        # --- Beat 3: zoom onto this region for the algebra. ---
        zoom_center = (v_point_new(t1, v1) + v_point_new(t2, v2)) / 2 + np.array([0.0, 0.6, 0.0])
        self.play(self.camera.frame.animate.scale(ZOOM_SCALE).move_to(zoom_center), run_time=1.4)

        sentence = Text(SENTENCE_TEXT, color=FORMULA, font_size=16)
        sentence.move_to(zoom_center + np.array([0.0, 1.3, 0.0]))
        sentence_bg = layout.make_text_bg(sentence)
        self.add(sentence_bg)
        self.play(Write(sentence), run_time=INTRO_TIME)
        self.wait(BEAT_GAP_TIME)

        # Reveal each "=" of the equation one at a time (review: don't show
        # multiple "="s at once). The second-half explanation overlaps the
        # v-t graph's line, so as in Scene4, put a background-colored
        # rectangle behind each element for readability (review). Always
        # add the background immediately with self.add - with
        # self.play(FadeIn(...)) the graph behind it can show through
        # (manim_notes.md).
        formula_parts = [
            MathTex("a", color=ACCELERATION, font_size=26),
            MathTex("=\\dfrac{\\Delta v}{\\Delta t}", color=FORMULA, font_size=26),
            MathTex("=\\dfrac{2\\,\\mathrm{m/s}}{1\\,\\mathrm{s}}", color=FORMULA, font_size=26),
            MathTex("=2\\,\\mathrm{m/s^2}", color=FORMULA, font_size=26),
        ]
        formula_parts[0].move_to(zoom_center + np.array([-1.0, 0.7, 0.0]), aligned_edge=RIGHT)
        for prev, part in zip(formula_parts, formula_parts[1:]):
            part.next_to(prev, RIGHT, buff=0.12)
        for part in formula_parts:
            part_bg = layout.make_text_bg(part)
            self.add(part_bg)
            self.play(Write(part), run_time=0.5)
            self.wait(BEAT_GAP_TIME * 0.7)

        definition = Text(DEFINITION_TEXT, color=FORMULA, font_size=16)
        definition.move_to(zoom_center + np.array([0.0, 0.15, 0.0]))
        definition_bg = layout.make_text_bg(definition)
        self.add(definition_bg)
        self.play(Write(definition), run_time=INTRO_TIME)
        self.wait(BEAT_GAP_TIME)

        # --- Beat 4: the unit - keep the original fraction, animate the
        # simplification to the right of a new "=". ---
        unit_fraction = MathTex("\\dfrac{\\mathrm{m/s}}{\\mathrm{s}}", color=FORMULA, font_size=24)
        unit_fraction.move_to(zoom_center + np.array([-0.7, -0.6, 0.0]))
        unit_fraction_bg = layout.make_text_bg(unit_fraction)
        self.add(unit_fraction_bg)
        self.play(Write(unit_fraction), run_time=INTRO_TIME)
        self.wait(BEAT_GAP_TIME * 0.6)

        unit_eq = MathTex("=", color=FORMULA, font_size=24).next_to(unit_fraction, RIGHT, buff=0.15)
        unit_intermediate = MathTex("\\dfrac{\\mathrm{m}}{\\mathrm{s}\\cdot\\mathrm{s}}", color=FORMULA, font_size=24).next_to(unit_eq, RIGHT, buff=0.15)
        unit_eq_bg = layout.make_text_bg(unit_eq)
        unit_intermediate_bg = layout.make_text_bg(unit_intermediate)
        self.add(unit_eq_bg, unit_intermediate_bg)
        self.play(Write(unit_eq), Write(unit_intermediate), run_time=INTRO_TIME)
        self.wait(BEAT_GAP_TIME * 0.6)

        unit_result = MathTex("\\mathrm{m/s^2}", color=FORMULA, font_size=24)
        unit_result.move_to(unit_intermediate.get_center())
        unit_result_bg = layout.make_text_bg(unit_result)
        self.play(Transform(unit_intermediate, unit_result), Transform(unit_intermediate_bg, unit_result_bg), run_time=1.0)
        self.wait(BEAT_GAP_TIME)

        self.play(FadeOut(*self.mobjects), run_time=FADE_TIME)
