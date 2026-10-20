"""Scene 3: The v-t graph and acceleration (revised per video review - drastically shortened).

Storyboard's original beats 1-3 (x-t tangent recall, placing two points,
computing Δv/Δt) are skipped outright: scene02's own revised ending already
makes that same argument (zoomed onto the v-t graph, points A/B marked, Δt/
Δv arrows drawn, a=Δv/Δt=...=2 m/s^2 shown). This scene opens already in
that exact zoomed state (rebuilt fresh, continuity) and adds only the new
conclusion: the line passes through the origin (a proportional
relationship), so v=at, and therefore a - the proportionality constant -
is both the acceleration and the graph's slope.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import LEFT, RIGHT, Arrow, Dot, FadeIn, FadeOut, Indicate, MathTex, MovingCameraScene, Text, VMobject, Write

from common.colors import ACCELERATION, BACKGROUND, FORMULA, VELOCITY
from common.graph_layout import make_t_axis, make_value_axis
from units.mechanics.mechanics_acceleration_and_uniformly_accelerated_motion import layout, motion
from units.mechanics.mechanics_acceleration_and_uniformly_accelerated_motion.scene02_acceleration_definition import (
    BIG_V_AXIS_LENGTH,
    BIG_V_ORIGIN_Y,
    GRAPH_ORIGIN_X_NEW,
    T_AXIS_LENGTH_NEW,
    V_RANGE,
    ZOOM_SCALE,
)

T_MAX = layout.T_RANGE[1]
T1, T2 = 1.0, 2.0

INTRO_TIME = 0.5
GAP_TIME = 0.9
FADE_TIME = 0.6


class Scene03VtSlope(MovingCameraScene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --- Continuity: rebuild scene02's exact ending - zoomed onto the
        # v-t graph, points A/B, Δt/Δv arrows, and the core a=Δv/Δt=...
        # formula (its explanatory sentence/definition/unit derivation are
        # dropped - their job is done - to free room for this scene's own
        # conclusion). ---
        origin = np.array([GRAPH_ORIGIN_X_NEW, BIG_V_ORIGIN_Y, 0.0])
        v_axis = make_value_axis(origin, V_RANGE, BIG_V_AXIS_LENGTH)
        v_t_axis = make_t_axis(origin, layout.T_RANGE, T_AXIS_LENGTH_NEW)

        def v_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        sample_ts = np.linspace(0.0, T_MAX, 100)
        v_line = VMobject(color=VELOCITY, stroke_width=3)
        v_line.set_points_smoothly([v_point(t, motion.velocity_ua(t)) for t in sample_ts])

        v1, v2 = motion.velocity_ua(T1), motion.velocity_ua(T2)
        dot_a = Dot(v_point(T1, v1), color=VELOCITY, radius=0.06)
        dot_b = Dot(v_point(T2, v2), color=VELOCITY, radius=0.06)
        dt_arrow = Arrow(v_point(T1, v1), v_point(T2, v1), color=FORMULA, buff=0.0, stroke_width=5)
        dt_label = MathTex("\\Delta t", color=FORMULA, font_size=28).next_to(dt_arrow, np.array([0.0, -1.0, 0.0]), buff=0.15)
        dv_arrow = Arrow(v_point(T2, v1), v_point(T2, v2), color=VELOCITY, buff=0.0, stroke_width=5)
        dv_label = MathTex("\\Delta v", color=VELOCITY, font_size=28).next_to(dv_arrow, RIGHT, buff=0.15)

        zoom_center = (v_point(T1, v1) + v_point(T2, v2)) / 2 + np.array([0.0, 0.6, 0.0])
        formula_parts = [
            MathTex("a", color=ACCELERATION, font_size=26),
            MathTex("=\\dfrac{\\Delta v}{\\Delta t}", color=FORMULA, font_size=26),
            MathTex("=\\dfrac{2\\,\\mathrm{m/s}}{1\\,\\mathrm{s}}", color=FORMULA, font_size=26),
            MathTex("=2\\,\\mathrm{m/s^2}", color=FORMULA, font_size=26),
        ]
        formula_parts[0].move_to(zoom_center + np.array([-1.0, 0.7, 0.0]), aligned_edge=RIGHT)
        for prev, part in zip(formula_parts, formula_parts[1:]):
            part.next_to(prev, RIGHT, buff=0.12)

        # Open already zoomed (this scene's continuity point), not zooming
        # in again from scratch.
        self.camera.frame.scale(ZOOM_SCALE).move_to(zoom_center)
        self.play(
            FadeIn(v_axis, v_t_axis, v_line, dot_a, dot_b, dt_arrow, dv_arrow),
            Write(dt_label), Write(dv_label), *[Write(part) for part in formula_parts],
            run_time=INTRO_TIME,
        )
        self.wait(GAP_TIME * 0.5)

        # The a=Δv/Δt=... formula's job is done (scene02 already made that
        # argument); free its space for this scene's own conclusion rather
        # than cramming both into the same zoomed view. A small upward pan
        # gives the new 3-line text stack more clearance above the Δv arrow.
        self.play(
            FadeOut(*formula_parts),
            self.camera.frame.animate.move_to(zoom_center + np.array([-0.3, 0.8, 0.0])),
            run_time=FADE_TIME,
        )

        # --- A line through the origin -> a proportional relationship. ---
        origin_dot = Dot(v_point(0.0, 0.0), color=VELOCITY, radius=0.07)
        self.play(Indicate(origin_dot, color=VELOCITY, scale_factor=1.8), FadeIn(origin_dot), run_time=1.0)
        proportional_text = Text("A line through the origin -> a proportional relationship", color=FORMULA, font_size=16)
        proportional_text.move_to(zoom_center + np.array([-0.7, 1.3, 0.0]))
        proportional_text_bg = layout.make_text_bg(proportional_text)
        self.add(proportional_text_bg)
        self.play(Write(proportional_text), run_time=INTRO_TIME)
        self.wait(GAP_TIME)

        # --- The proportional equation v=at. ---
        proportional_formula = MathTex("v", "=", "a", "t", color=FORMULA, font_size=28)
        proportional_formula[2].set_color(ACCELERATION)
        proportional_formula.next_to(proportional_text, np.array([0.0, -1.0, 0.0]), buff=0.35)
        proportional_formula.align_to(proportional_text, LEFT)
        proportional_formula_bg = layout.make_text_bg(proportional_formula)
        self.add(proportional_formula_bg)
        self.play(Write(proportional_formula), run_time=INTRO_TIME)
        self.wait(GAP_TIME)

        # --- -> the proportionality constant a = acceleration = the
        # graph's slope, one clause at a time. Left edge aligned with
        # proportional_text's (review: left-align them). This also overlaps
        # the v-t graph's line, so give each clause a background too
        # (review: the text overlaps the graph here too). Add the
        # background immediately with self.add
        # (self.play(FadeIn(...)) lets the graph behind it show through -
        # manim_notes.md). ---
        conclusion_parts = [
            Text("-> the proportionality constant a", color=ACCELERATION, font_size=16),
            Text("= acceleration", color=ACCELERATION, font_size=16),
            Text("= the graph's slope", color=ACCELERATION, font_size=16),
        ]
        conclusion_parts[0].next_to(proportional_formula, np.array([0.0, -1.0, 0.0]), buff=0.4)
        conclusion_parts[0].align_to(proportional_text, LEFT)
        for prev, part in zip(conclusion_parts, conclusion_parts[1:]):
            part.next_to(prev, RIGHT, buff=0.15)
        for part in conclusion_parts:
            part_bg = layout.make_text_bg(part)
            self.add(part_bg)
            self.play(Write(part), run_time=0.5)
            self.wait(GAP_TIME * 0.8)

        self.wait(GAP_TIME * 2)
        self.play(FadeOut(*self.mobjects), self.camera.frame.animate.scale(1 / ZOOM_SCALE).move_to(np.array([0.0, 0.0, 0.0])), run_time=1.2)
