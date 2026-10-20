"""Scene 6: Deriving the formulas (revised per video review, 2nd pass).

Implements storyboard.md > Scene 6, using scene05's own v0!=0 example
(motion.V0, motion.ACCEL_A, over [0, motion.V0_DEMO_T]) for continuity.

The scene opens zoomed onto the v-t graph (screen-left, less tightly than
before - the previous zoom clipped the top/bottom of frame) - all of
beat 1's graph-labeling (a=slope=acceleration, v0=intercept=initial
velocity, then v=v0+at as "Formula 1") and beat 2's area decomposition
(trapezoid -> rectangle + triangle, each colored/measured with its own
working - width/height brackets, a "t x height =" line - shown only while
that shape is active) happen in this zoomed view. Each area value is bold,
saturated, and drawn in front of its shape's fill. The camera zooms back
out for a big, screen-centered addition of the two areas, which condenses
into "Formula 2" beside "Formula 1" at top-right; a large "Derive one more
formula from these two" title then shrinks into a small header for beat
3's step-by-step elimination of t (kept fully visible, ~5s per line). The
scene ends by gathering all three formulas at center screen and zooming in
on them.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Brace, FadeIn, FadeOut, Line, MathTex, MovingCameraScene, Polygon, SurroundingRectangle, Text, VGroup, Write

from common.colors import ACCELERATION, BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.graph_layout import make_t_axis, make_value_axis
from units.mechanics.mechanics_acceleration_and_uniformly_accelerated_motion import layout, motion

GRAPH_ORIGIN_X = -6.3
AXIS_LENGTH = 3.6
ORIGIN_Y = -1.6
T_RANGE = [0, 2, 1]
T_AXIS_LENGTH = 3.2
V_RANGE = [0, 6, 2]

FORMULA_X = -1.3  # closer to the graph - there was unused space between them (review)
FORMULA_TOP_Y = 3.3
LINE_GAP = 0.62

# Shared "top of the zoomed view" spot for a caption in the empty space to
# the right of the graph, rather than above it where it used to overlap the
# graph (review). Lowered from the very top edge of the zoomed frame - it
# read as too high up (review). x tuned against the actual measured widths
# of the longest captions here (~4.1 units) so they clear both the graph on
# the left and the zoomed frame's edge on the right.
TOP_TEXT_POS = np.array([-0.6, 2.3, 0.0])

INTRO_TIME = 0.5
GAP_TIME = 0.8
FADE_TIME = 0.6
ALGEBRA_LINE_HOLD = 5.0  # review: hold each derivation line for about 5 seconds so it can be read
HOLD_BEFORE_FADE = 5.0  # review: wait 5 seconds after showing each piece of text before fading it out

T_MAX = motion.V0_DEMO_T
V0 = motion.V0
A = motion.ACCEL_A
V_END = motion.velocity_ua(T_MAX, v0=V0, a=A)

GRAPH_CENTER = np.array([GRAPH_ORIGIN_X + 2.6, ORIGIN_Y + 1.7, 0.0])  # camera centered further right of the graph, so the graph itself reads as shifted left within the zoomed frame, leaving room for captions on the right (review)
ZOOM_SCALE = 0.78  # less tight than before - the previous 0.62 clipped the top/bottom edge


class Scene06Formulas(MovingCameraScene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        origin = np.array([GRAPH_ORIGIN_X, ORIGIN_Y, 0.0])
        v_axis = make_value_axis(origin, V_RANGE, AXIS_LENGTH)
        v_t_axis = make_t_axis(origin, T_RANGE, T_AXIS_LENGTH)
        v_axis_label = MathTex("v", color=VELOCITY, font_size=30).next_to(v_axis.get_end(), UP, buff=0.15)
        t_axis_label = MathTex("t", color=FORMULA, font_size=30).next_to(v_t_axis.get_end(), RIGHT, buff=0.15)
        v_title = layout.make_graph_title("v-t graph", v_axis_label, color=VELOCITY)

        def v_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        line = Line(v_point(0, V0), v_point(T_MAX, V_END), color=VELOCITY, stroke_width=3)

        self.play(FadeIn(v_axis, v_t_axis, line), Write(v_axis_label), Write(t_axis_label), Write(v_title), run_time=INTRO_TIME)

        # --- Zoom onto the graph: beats 1-2 only need this half of the screen. ---
        self.play(self.camera.frame.animate.scale(ZOOM_SCALE).move_to(GRAPH_CENTER), run_time=1.2)

        # Show what we're about to find, before "a: the graph's slope..."
        # (review). review: don't clear earlier text when showing the next
        # - keep this title on screen too, until Formula 1 is shown and
        # held.
        line_formula_title = Text("Find the line's equation", color=FORMULA, font_size=30)
        line_formula_title.move_to(TOP_TEXT_POS)
        self.play(Write(line_formula_title), run_time=INTRO_TIME)
        self.wait(HOLD_BEFORE_FADE)

        # --- Beat 1: a=slope=acceleration, v0=intercept=initial velocity, then Formula 1 v=v0+at. ---
        slope_dt = T_MAX * 0.4
        slope_triangle = Polygon(
            v_point(0.3, motion.velocity_ua(0.3, v0=V0, a=A)),
            v_point(0.3 + slope_dt, motion.velocity_ua(0.3, v0=V0, a=A)),
            v_point(0.3 + slope_dt, motion.velocity_ua(0.3 + slope_dt, v0=V0, a=A)),
            color=ACCELERATION, stroke_width=2, fill_opacity=0.0,
        )
        a_label = Text("a: the graph's slope = acceleration", color=ACCELERATION, font_size=22)
        a_label.next_to(slope_triangle, RIGHT, buff=0.2)
        self.play(FadeIn(slope_triangle), run_time=INTRO_TIME)
        self.play(Write(a_label), run_time=INTRO_TIME)
        self.wait(HOLD_BEFORE_FADE)

        intercept_dot_label = MathTex("v_0", color=VELOCITY, font_size=26).next_to(v_point(0, V0), LEFT, buff=0.15)
        v0_label = Text("v₀: the graph's intercept = initial velocity", color=VELOCITY, font_size=20)
        v0_label2 = Text("(the value of v at t=0)", color=VELOCITY, font_size=16)
        # Anchored to the graph itself, not the (independently tunable)
        # camera center. Pushed further below the t-axis than a short label
        # would need, so the longer English wording clears the axis's own
        # tick numbers instead of overlapping them.
        v0_label.move_to(v_point(0, 0) + np.array([1.6, -0.95, 0.0]))
        v0_label2.next_to(v0_label, DOWN, buff=0.12)
        self.play(FadeIn(intercept_dot_label), run_time=INTRO_TIME)
        self.play(Write(v0_label), Write(v0_label2), run_time=INTRO_TIME)
        self.wait(HOLD_BEFORE_FADE)

        # Formula 1 is placed close to the line itself (review: a bit
        # closer to the line), first introduced as "The line's equation:
        # v=v0+at", held, then tagged "-> Formula 1" (review).
        # review: keep the text used to explain Formula 1 on screen until
        # Formula 1 is shown and held.
        formula1_lead = Text("The line's equation: ", color=FORMULA, font_size=22)
        formula1 = MathTex("v", "=", "v_0", "+", "a", "t", font_size=32)
        formula1.set_color(FORMULA)
        formula1[0].set_color(VELOCITY)
        formula1[2].set_color(VELOCITY)
        formula1[4].set_color(ACCELERATION)
        formula1_group = VGroup(formula1_lead, formula1).arrange(RIGHT, buff=0.15)
        # Hugs the line's end point closely, low enough to clear TOP_TEXT_POS
        # above it now that both stay on screen together (review).
        formula1_group.move_to(v_point(T_MAX, V_END) + np.array([0.9, -0.35, 0.0]))
        self.play(Write(formula1_lead), Write(formula1), run_time=INTRO_TIME)
        self.wait(HOLD_BEFORE_FADE)
        formula1_tag = Text("-> Formula 1", color=FORMULA, font_size=20).next_to(formula1, RIGHT, buff=0.3)
        self.play(Write(formula1_tag), run_time=INTRO_TIME)
        self.wait(HOLD_BEFORE_FADE)

        # Formula 1's explanatory text has served its purpose here - fade
        # it all out together (Formula 1 itself stays on screen until it
        # later moves into the column).
        self.play(
            FadeOut(line_formula_title, slope_triangle, a_label, intercept_dot_label, v0_label, v0_label2),
            run_time=FADE_TIME,
        )

        # --- Beat 2: the area equation. First, flash the whole trapezoid
        # with its own two-line label (split before "=" - review). ---
        trapezoid = Polygon(v_point(0, 0), v_point(T_MAX, 0), v_point(T_MAX, V_END), v_point(0, V0), color=FORMULA, fill_color=FORMULA, fill_opacity=0.0, stroke_width=0)
        trap_line1 = Text("This trapezoid's area", color=FORMULA, font_size=22)
        trap_line2 = VGroup(Text("= the distance traveled over", color=FORMULA, font_size=22), MathTex("t", color=FORMULA, font_size=22), Text("seconds", color=FORMULA, font_size=22)).arrange(RIGHT, buff=0.08)
        trap_line1.move_to(TOP_TEXT_POS)
        trap_line2.next_to(trap_line1, DOWN, buff=0.15)
        trap_bg1 = layout.make_text_bg(trap_line1)
        trap_bg2 = layout.make_text_bg(trap_line2)

        self.add(trap_bg1, trap_bg2)
        self.play(trapezoid.animate.set_fill(opacity=0.4), Write(trap_line1), Write(trap_line2), run_time=0.8)
        self.wait(HOLD_BEFORE_FADE)
        self.play(trapezoid.animate.set_fill(opacity=0.0), FadeOut(trap_bg1, trap_bg2, trap_line1, trap_line2), run_time=0.6)

        # Rectangle: fill, "First, find this rectangle's area", width(t)/
        # height(v0) brackets, then the working (intermediate step and
        # result) combined into one line inside the shape (review: keep the
        # rectangle's area calculation to one line). review: keep the text
        # used to explain Formula 2 (this rectangle, and the triangle
        # after it) on screen until Formula 2 is shown and held - don't
        # clear anything yet here.
        rect = Polygon(v_point(0, 0), v_point(T_MAX, 0), v_point(T_MAX, V0), v_point(0, V0), color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.5, stroke_width=1)
        rect_text = Text("First, find this rectangle's area", color=PRIMARY, font_size=20)
        rect_text.move_to(TOP_TEXT_POS)
        rect_bg = layout.make_text_bg(rect_text)
        self.play(FadeIn(rect), run_time=INTRO_TIME)
        self.add(rect_bg)
        self.play(Write(rect_text), run_time=INTRO_TIME)

        width_brace = Brace(Line(v_point(0, 0), v_point(T_MAX, 0)), DOWN, color=FORMULA).next_to(v_point(T_MAX / 2, 0), DOWN, buff=0.35)
        width_label = MathTex("t", color=FORMULA, font_size=30).next_to(width_brace, DOWN, buff=0.08)
        rect_height_brace = Brace(Line(v_point(0, 0), v_point(0, V0)), LEFT, color=PRIMARY)
        rect_height_label = MathTex("v_0", color=PRIMARY, font_size=26).next_to(rect_height_brace, LEFT, buff=0.1)
        self.play(FadeIn(width_brace, rect_height_brace), Write(width_label), Write(rect_height_label), run_time=INTRO_TIME)
        self.wait(GAP_TIME * 0.6)

        # Combine the working and the result (bold, saturated) into one line inside the shape (review).
        rect_formula = MathTex("t \\times v_0 = \\mathbf{v_0 t}", color=PRIMARY, font_size=26)
        rect_formula.move_to(rect.get_center())
        rect_formula.set_z_index(5)
        rect_formula_bg = layout.make_text_bg(rect_formula)
        self.add(rect_formula_bg)
        self.play(Write(rect_formula), run_time=INTRO_TIME)
        self.wait(HOLD_BEFORE_FADE)

        # Triangle: same pattern - "Next, find this triangle's area" is
        # shown right below the rectangle's explanation (review: show the
        # next text without clearing the previous one).
        triangle = Polygon(v_point(0, V0), v_point(T_MAX, V0), v_point(T_MAX, V_END), color=ACCELERATION, fill_color=ACCELERATION, fill_opacity=0.5, stroke_width=1)
        tri_text = Text("Next, find this triangle's area", color=ACCELERATION, font_size=20)
        tri_text.next_to(rect_text, DOWN, buff=0.2)
        tri_bg = layout.make_text_bg(tri_text)
        self.play(FadeIn(triangle), run_time=INTRO_TIME)
        self.add(tri_bg)
        self.play(Write(tri_text), run_time=INTRO_TIME)

        tri_height_brace = Brace(Line(v_point(T_MAX, V0), v_point(T_MAX, V_END)), RIGHT, color=ACCELERATION)
        tri_height_label = MathTex("at", color=ACCELERATION, font_size=26).next_to(tri_height_brace, RIGHT, buff=0.1)
        self.play(FadeIn(tri_height_brace), Write(tri_height_label), run_time=INTRO_TIME)
        self.wait(GAP_TIME * 0.6)

        # Combine the working and the result into one line inside the shape
        # (review: also keep the triangle's area calculation to one line).
        tri_formula = MathTex("t \\times at \\times \\dfrac{1}{2} = \\mathbf{\\dfrac{1}{2}at^2}", color=ACCELERATION, font_size=22)
        tri_formula.move_to(triangle.get_center() + np.array([0.3, 0.0, 0.0]))
        tri_formula.set_z_index(5)
        tri_formula_bg = layout.make_text_bg(tri_formula)
        self.add(tri_formula_bg)
        self.play(Write(tri_formula), run_time=INTRO_TIME)
        self.wait(HOLD_BEFORE_FADE)

        # --- Zoom out: the right side is needed from here on. ---
        self.play(self.camera.frame.animate.scale(1 / ZOOM_SCALE).move_to(np.array([0.0, 0.0, 0.0])), run_time=1.3)

        sum_text = Text("Add the triangle's area and the rectangle's area together", color=FORMULA, font_size=24)
        sum_text.move_to(np.array([FORMULA_X + 1.5, 2.6, 0.0]))
        self.play(Write(sum_text), run_time=INTRO_TIME)
        self.wait(GAP_TIME * 0.7)

        # Big, screen-centered addition of the two areas (review), before
        # condensing into Formula 2.
        central_sum = MathTex("v_0 t", "+", "\\dfrac{1}{2}at^2", font_size=44)
        central_sum[0].set_color(PRIMARY)
        central_sum[2].set_color(ACCELERATION)
        central_sum.move_to(np.array([0.0, -0.3, 0.0]))
        self.play(Write(central_sum), run_time=1.0)
        self.wait(HOLD_BEFORE_FADE)

        # Before folding into Formula 2, show "-> Formula 2" as a
        # continuation of the equation (review).
        central_sum_tag = Text("-> Formula 2", color=FORMULA, font_size=22).next_to(central_sum, RIGHT, buff=0.3)
        self.play(Write(central_sum_tag), run_time=INTRO_TIME)
        self.wait(HOLD_BEFORE_FADE)

        # Formula 1 relocates to the right-side column alongside Formula 2
        # (review: line up Formula 1 and Formula 2 on the right side of the
        # screen) - a fresh MathTex at the target spot, cross-faded with
        # the zoomed-in one.
        formula1_target = MathTex("v", "=", "v_0", "+", "a", "t", font_size=32)
        formula1_target.set_color(FORMULA)
        formula1_target[0].set_color(VELOCITY)
        formula1_target[2].set_color(VELOCITY)
        formula1_target[4].set_color(ACCELERATION)
        formula1_target.move_to(np.array([FORMULA_X, FORMULA_TOP_Y, 0.0]), aligned_edge=LEFT)
        formula1_tag_target = Text("Formula 1", color=FORMULA, font_size=20).next_to(formula1_target, RIGHT, buff=0.3)

        formula2 = MathTex("x", "=", "v_0", "t", "+", "\\dfrac{1}{2}", "a", "t^2", font_size=32)
        formula2.set_color(FORMULA)
        formula2[0].set_color(PRIMARY)
        formula2[2].set_color(PRIMARY)
        formula2[6].set_color(ACCELERATION)
        formula2.move_to(np.array([FORMULA_X, FORMULA_TOP_Y - LINE_GAP, 0.0]), aligned_edge=LEFT)
        formula2_tag = Text("Formula 2", color=FORMULA, font_size=20).next_to(formula2, RIGHT, buff=0.3)

        # Formula 2's explanation (the rectangle/triangle set) finally
        # serves its purpose here too (review: don't clear it until Formula
        # 2 is shown and held).
        self.play(
            FadeOut(
                sum_text, central_sum, central_sum_tag, formula1_lead, formula1, formula1_tag,
                rect_text, rect_bg, rect_height_brace, rect_height_label, rect_formula, rect_formula_bg,
                tri_text, tri_bg, tri_height_brace, tri_height_label, tri_formula, tri_formula_bg,
                rect, triangle, width_brace, width_label, trapezoid,
            ),
            FadeIn(formula1_target, formula1_tag_target, formula2, formula2_tag),
            run_time=1.0,
        )
        self.wait(GAP_TIME)

        # --- Beat 3: eliminate t to derive Formula 3. A big, centered
        # title first, then shrunk into a small header for the algebra
        # column (review). ---
        eliminate_title = Text("Derive one more formula from these two", color=FORMULA, font_size=32)
        eliminate_title.move_to(np.array([0.0, 0.0, 0.0]))
        self.play(Write(eliminate_title), run_time=INTRO_TIME)
        self.wait(GAP_TIME * 1.2)

        header_pos = np.array([FORMULA_X, FORMULA_TOP_Y - LINE_GAP * 1.9, 0.0])
        self.play(eliminate_title.animate.scale(0.4).move_to(header_pos, aligned_edge=LEFT), run_time=1.0)
        self.wait(GAP_TIME * 0.3)

        def make_step(lead_text: str, formula_tex: str, y: float) -> VGroup:
            # review: the derivation steps for Formula 3 were too small - enlarge the font.
            lead = Text(lead_text, color=FORMULA, font_size=22)
            lead.move_to(np.array([FORMULA_X, y, 0.0]), aligned_edge=LEFT)
            formula = MathTex(formula_tex, color=FORMULA, font_size=26)
            formula.next_to(lead, RIGHT, buff=0.15)
            return VGroup(lead, formula)

        step_specs = [
            ("Solve Formula 1 for t:", "at = v - v_0"),
            ("Rearranging further:", "t = \\dfrac{v-v_0}{a}"),
            ("Substitute t into Formula 2:", "x = v_0\\dfrac{v-v_0}{a} + \\dfrac{1}{2}a\\left(\\dfrac{v-v_0}{a}\\right)^2"),
            ("Multiply both sides by 2a:", "2ax = 2v_0(v-v_0) + (v-v_0)^2"),
            ("Expanding the right side:", "2ax = 2v_0v - 2v_0^2 + v^2 - 2v_0v + v_0^2"),
            ("Collecting like terms:", "2ax = v^2 - v_0^2"),
        ]
        for i, (lead_text, formula_tex) in enumerate(step_specs):
            step = make_step(lead_text, formula_tex, FORMULA_TOP_Y - LINE_GAP * (2.7 + i))
            self.play(Write(step), run_time=INTRO_TIME)
            self.wait(ALGEBRA_LINE_HOLD)

        # review: make the line where Formula 3 is reached stand out -
        # larger than the six derivation lines, and framed in the accent
        # color.
        formula3 = MathTex("v^2", "-", "v_0^2", "=", "2", "a", "x", font_size=38)
        formula3.set_color(FORMULA)
        formula3[5].set_color(ACCELERATION)
        formula3.move_to(np.array([FORMULA_X, FORMULA_TOP_Y - LINE_GAP * (2.7 + len(step_specs)), 0.0]), aligned_edge=LEFT)
        formula3_tag = Text("Formula 3", color=FORMULA, font_size=22).next_to(formula3, RIGHT, buff=0.3)
        formula3_box = SurroundingRectangle(VGroup(formula3, formula3_tag), color=ACCELERATION, buff=0.15)
        self.play(Write(formula3), Write(formula3_tag), run_time=INTRO_TIME)
        self.play(FadeIn(formula3_box), run_time=0.5)
        self.wait(HOLD_BEFORE_FADE)

        # --- Final: gather all three formulas at center, zoom in, end scene. ---
        self.play(
            FadeOut(*[m for m in self.mobjects if m not in (formula1_target, formula1_tag_target, formula2, formula2_tag, formula3, formula3_tag)]),
            run_time=FADE_TIME,
        )
        final_group = VGroup(
            VGroup(formula1_target, formula1_tag_target),
            VGroup(formula2, formula2_tag),
            VGroup(formula3, formula3_tag),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        final_group.move_to(np.array([0.0, 0.0, 0.0]))
        self.play(
            formula1_target.animate.move_to(final_group[0][0].get_center()),
            formula1_tag_target.animate.move_to(final_group[0][1].get_center()),
            formula2.animate.move_to(final_group[1][0].get_center()),
            formula2_tag.animate.move_to(final_group[1][1].get_center()),
            formula3.animate.move_to(final_group[2][0].get_center()),
            formula3_tag.animate.move_to(final_group[2][1].get_center()),
            run_time=1.3,
        )
        self.wait(GAP_TIME * 0.5)
        self.play(self.camera.frame.animate.scale(0.6).move_to(final_group.get_center()), run_time=1.3)
        self.wait(HOLD_BEFORE_FADE)

        self.play(FadeOut(*self.mobjects), run_time=FADE_TIME)
