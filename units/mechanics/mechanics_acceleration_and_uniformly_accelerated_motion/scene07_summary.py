"""Scene 7: Wrap-up (revised per video review). Ends the video.

Implements storyboard.md > Scene 7: the "😁" rests center, x-t graph at
left, v-t graph at right (this scene's own side-by-side layout, distinct
from every earlier scene's stacked one). The opening plot is a live synced
pass (dot+trace+face moving together, with a live tangent line on the x-t
curve) rather than a pre-drawn static curve, matching every other scene's
convention - review: when showing a graph, sync the plotting with 😁's
motion. A persistent "Uniformly accelerated motion" label names the motion
throughout.

Beat 2's "briefly replaying the corresponding visual for each checklist
item" is a brief, in-place highlight per
checklist item (an `Indicate` pulse, held longer per review, plus a real
tangent line drawn on the v-t graph for the slope item and an area flash
for the area item) rather than reconstructing every earlier scene's full
animation. The three formulas are not part of the checklist column; they
are their own stacked group in the bottom-right empty space.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import LEFT, RIGHT, UP, Dot, FadeIn, FadeOut, Indicate, MathTex, Polygon, Scene, Text, TracedPath, ValueTracker, VGroup, Write, linear

from common.colors import ACCELERATION, BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.graph_layout import make_t_axis, make_value_axis
from units.mechanics.mechanics_acceleration_and_uniformly_accelerated_motion import layout, motion

X_RANGE = [0, 9, 3]
V_RANGE = [0, 6, 2]
T_MAX = 3.0

FACE_AXIS_X = -5.0  # left-to-right order: 😁, x-t, v-t (review)
MID_ORIGIN_X = -1.0
RIGHT_ORIGIN_X = 3.5
ROW_Y = 0.1  # lowered so the "x-t/v-t graph" titles above the axes stay on screen (review)
AXIS_LENGTH = 3.0
T_AXIS_LENGTH = 3.0
TANGENT_HALF_SPAN = 0.3

CHECKLIST_X = -6.3
CHECKLIST_TOP_Y = -1.2
CHECKLIST_GAP = 0.6
CHECKLIST_FONT = 20

FORMULA_POS = np.array([4.2, -1.3, 0.0])
FORMULA_GAP = 0.55

LABEL_POS = np.array([-3.25, 3.7, 0.0])  # aligned with the x-t/v-t graph titles' height (review)

INTRO_TIME = 0.6
DRAW_TIME = 2.6
ITEM_TIME = 0.5
ITEM_GAP = 0.45
INDICATE_TIME = 1.3
INDICATE_GAP = 0.6
FINAL_HOLD = 2.0
FINAL_FADE = 2.5


class Scene07Summary(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        mid_origin = np.array([MID_ORIGIN_X, ROW_Y, 0.0])
        right_origin = np.array([RIGHT_ORIGIN_X, ROW_Y, 0.0])
        face_axis = make_value_axis(np.array([FACE_AXIS_X, ROW_Y, 0.0]), X_RANGE, AXIS_LENGTH)
        graph_x_axis = make_value_axis(mid_origin, X_RANGE, AXIS_LENGTH)
        graph_t_axis = make_t_axis(mid_origin, layout.T_RANGE, T_AXIS_LENGTH)
        v_axis = make_value_axis(right_origin, V_RANGE, AXIS_LENGTH)
        v_t_axis = make_t_axis(right_origin, layout.T_RANGE, T_AXIS_LENGTH)
        x_axis_label = MathTex("x", color=PRIMARY, font_size=28).next_to(graph_x_axis.get_end(), UP, buff=0.15)
        t_axis_label_left = MathTex("t", color=FORMULA, font_size=28).next_to(graph_t_axis.get_end(), RIGHT, buff=0.15)
        v_axis_label = MathTex("v", color=VELOCITY, font_size=28).next_to(v_axis.get_end(), UP, buff=0.15)
        t_axis_label_right = MathTex("t", color=FORMULA, font_size=28).next_to(v_t_axis.get_end(), RIGHT, buff=0.15)
        x_title = layout.make_graph_title("x-t graph", x_axis_label, color=PRIMARY)
        v_title = layout.make_graph_title("v-t graph", v_axis_label, color=VELOCITY)

        def x_point(t: float, x: float) -> np.ndarray:
            return np.array([graph_t_axis.number_to_point(t)[0], graph_x_axis.number_to_point(x)[1], 0.0])

        def v_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        label = Text("Uniformly accelerated motion", color=FORMULA, font_size=18)
        label.move_to(LABEL_POS)

        self.play(
            FadeIn(face_axis, graph_x_axis, graph_t_axis, v_axis, v_t_axis),
            Write(x_axis_label), Write(t_axis_label_left), Write(v_axis_label), Write(t_axis_label_right),
            Write(x_title), Write(v_title), Write(label),
            run_time=INTRO_TIME,
        )

        # --- Opening: a live synced pass (review: sync the plotting with
        # 😁's motion), with a live tangent line on the x-t curve. ---
        t_tracker = ValueTracker(0.0)
        face, face_update = layout.make_tracked_face(face_axis, lambda: motion.position_ua(t_tracker.get_value()))
        x_dot = Dot(color=PRIMARY)
        v_dot = Dot(color=VELOCITY)
        # Only "😁"<->x-t is connected - x-t and v-t don't need a line
        # between them, just synced timing (review).
        x_connector = layout.make_connector()
        tangent_line = layout.make_tangent_line(x_point, 0.0, 0.0, 0.0, TANGENT_HALF_SPAN, VELOCITY)

        def update_x_dot(mob) -> None:
            t = t_tracker.get_value()
            mob.move_to(x_point(t, motion.position_ua(t)))

        def update_v_dot(mob) -> None:
            t = t_tracker.get_value()
            mob.move_to(v_point(t, motion.velocity_ua(t)))

        def update_x_connector(mob) -> None:
            mob.put_start_and_end_on(face.get_center(), x_dot.get_center())

        def update_tangent_line(mob) -> None:
            t = t_tracker.get_value()
            mob.become(layout.make_tangent_line(x_point, t, motion.position_ua(t), motion.velocity_ua(t), TANGENT_HALF_SPAN, VELOCITY))

        update_x_dot(x_dot)
        update_v_dot(v_dot)
        update_x_connector(x_connector)
        update_tangent_line(tangent_line)

        self.play(FadeIn(face, x_dot, v_dot, x_connector, tangent_line), run_time=INTRO_TIME)

        x_dot.add_updater(update_x_dot)
        v_dot.add_updater(update_v_dot)
        x_connector.add_updater(update_x_connector)
        tangent_line.add_updater(update_tangent_line)

        x_curve = TracedPath(x_dot.get_center, stroke_color=PRIMARY, stroke_width=3)
        v_curve = TracedPath(v_dot.get_center, stroke_color=VELOCITY, stroke_width=3)
        self.add(x_curve, v_curve)

        self.play(t_tracker.animate.set_value(T_MAX), run_time=DRAW_TIME, rate_func=linear)
        self.wait(0.4)

        x_curve.clear_updaters()
        v_curve.clear_updaters()
        x_dot.remove_updater(update_x_dot)
        v_dot.remove_updater(update_v_dot)
        x_connector.remove_updater(update_x_connector)
        # The x-t graph's tangent keeps being shown (review) - not removed here.
        self.play(FadeOut(x_dot, v_dot, x_connector), run_time=0.5)

        # --- Beat 1: checklist, one item at a time (formulas are their
        # own group, in the bottom-right empty space - not part of this
        # column). ---
        item1 = Text("Acceleration is: the change in velocity per unit time", color=FORMULA, font_size=CHECKLIST_FONT)
        item2 = Text("On a v-t graph: slope = acceleration", color=FORMULA, font_size=CHECKLIST_FONT)
        item3 = Text("On a v-t graph: area = distance traveled", color=FORMULA, font_size=CHECKLIST_FONT)
        item4 = Text("Motion with constant acceleration: uniformly accelerated motion", color=FORMULA, font_size=CHECKLIST_FONT)
        items = [item1, item2, item3, item4]
        for i, item in enumerate(items):
            item.move_to(np.array([CHECKLIST_X, CHECKLIST_TOP_Y - i * CHECKLIST_GAP, 0.0]), aligned_edge=LEFT)

        for item in items:
            self.play(Write(item), run_time=ITEM_TIME)
            self.wait(ITEM_GAP)

        formula_lines = [
            MathTex("v=v_0+at", color=FORMULA, font_size=24),
            MathTex("x=v_0t+\\tfrac{1}{2}at^2", color=FORMULA, font_size=24),
            MathTex("v^2-v_0^2=2ax", color=FORMULA, font_size=24),
        ]
        for i, formula in enumerate(formula_lines):
            formula.move_to(FORMULA_POS + np.array([0.0, -i * FORMULA_GAP, 0.0]))
        for formula in formula_lines:
            self.play(Write(formula), run_time=ITEM_TIME)
            self.wait(ITEM_GAP)

        # --- Beat 2: brief, in-place recall of each item - held longer
        # (review: take more time while emphasizing). ---
        self.play(Indicate(item1, color=ACCELERATION), run_time=INDICATE_TIME)
        self.wait(INDICATE_GAP)

        tangent_t = 1.5
        tangent_highlight = layout.make_tangent_line(
            v_point, tangent_t, motion.velocity_ua(tangent_t), motion.ACCEL_A, 0.6, ACCELERATION, stroke_width=5
        )
        self.play(Indicate(item2, color=VELOCITY), FadeIn(tangent_highlight), run_time=INDICATE_TIME)
        self.wait(INDICATE_GAP)
        self.play(FadeOut(tangent_highlight), run_time=0.4)

        area_flash = Polygon(v_point(0, 0), v_point(T_MAX, 0), v_point(T_MAX, motion.velocity_ua(T_MAX)), color=VELOCITY, fill_color=VELOCITY, fill_opacity=0.4, stroke_width=0)
        self.play(Indicate(item3, color=VELOCITY), FadeIn(area_flash), run_time=INDICATE_TIME)
        self.wait(INDICATE_GAP)
        self.play(FadeOut(area_flash), run_time=0.4)

        self.play(Indicate(item4, color=ACCELERATION), run_time=INDICATE_TIME)
        self.wait(INDICATE_GAP)
        self.play(Indicate(VGroup(*formula_lines), color=FORMULA), run_time=INDICATE_TIME)
        self.wait(FINAL_HOLD)

        # --- Final: fade out everything, ending the video. tangent_line's
        # updater was deliberately never removed (it stays live throughout -
        # review) but that same live .become() each frame fights FadeOut's
        # opacity animation, leaving it on screen; freeze it here so it
        # fades out with everything else (review: the tangent line was the
        # only thing left behind on screen).
        tangent_line.remove_updater(update_tangent_line)
        self.play(FadeOut(*self.mobjects), run_time=FINAL_FADE)
