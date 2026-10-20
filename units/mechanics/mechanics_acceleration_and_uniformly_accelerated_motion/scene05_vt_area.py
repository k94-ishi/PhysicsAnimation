"""Scene 5: Area under the v-t graph and distance traveled (revised per video review).

Implements storyboard.md > Scene 5. A big, centered v-t graph (t: 0-4, this
topic's established SINGLE_* layout slot, review: "use that whole region to
think about the area") with the "😁" on its own labeled position axis at
the left -
a "v=" readout rides right beside it, and a fixed "t=" readout sits between
it and the graph. No dashed line forces a connection between "😁" and the
v-t graph (review) - the sync is conveyed by timing alone.

For every stage (beat 1's constant-v rectangle; each of the 2/4/8/16/32-
division staircases; the ∞ limit; and the v0!=0 repeat), after that
stage's rectangles are shown, a point is played moving along their top
edges (a discontinuous step function for the staircase stages) while the
"😁" climbs its axis by the *accumulating* area in real time. Watching the
two move together *is* the "area = distance" argument; it is also
asserted in words once, at the end, after the ∞ limit.

Per-rectangle width/height/area numbers are only shown for n=2,4
(storyboard: "only the total area from 8 divisions on"), and never for a
zero-area rectangle (review). Beat 8 (v0!=0) repeats this briefly; beat 9
(non-constant acceleration) now also runs the same 2->4->8->16->32->∞
convergence, reusing `build_staircase`/`step_functions` generalized to
take an arbitrary velocity function (2nd reuse - see SKILL.md).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Brace, Dot, FadeIn, FadeOut, Line, MathTex, Polygon, Scene, Text, Transform, ValueTracker, VGroup, VMobject, Write, linear
from manim.mobject.text.numbers import DecimalNumber

from common.colors import BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.graph_layout import make_t_axis, make_value_axis
from units.mechanics.mechanics_acceleration_and_uniformly_accelerated_motion import layout, motion

T_RANGE5 = [0, 4, 1]
X_RANGE5 = [0, 20, 4]  # wide enough for the v0!=0 case's x(4)=20 too (review: use t up to 4)
V_RANGE5 = [0, 10, 2]  # wide enough for the v0!=0 case's v(4)=9 too
T_MAX = 4.0

BEAT1_V = 4.0  # over the full t:0-4 domain, area = 16 (matches X_RANGE5's top tick)

STAGES = [2, 4, 8, 16, 32]  # beats 2-6; beat 7 is the infinite-division limit
DETAILED_STAGES = {2, 4}

INTRO_TIME = 0.5
FADE_TIME = 0.5
GAP_TIME = 0.6
REFINE_TIME = 1.4
SYNCED_MOTION_TIME = 2.2

V0_T_MAX = T_MAX  # the v0!=0 example also uses t up to 4 (review)

CUBIC_T_RANGE = [0, 9, 3]
CUBIC_V_RANGE = [0, 6, 2]
CUBIC_X_RANGE = [0, 30, 10]  # cubic total distance (analytic) ~= 28.65

CONCLUSION_LINE1 = "The area enclosed by the v-t graph and the t axis"
CONCLUSION_LINE2 = "corresponds to the distance traveled"
CONCLUSION_HOLD = 5.0

TOP_RIGHT_POS = np.array([2.7, 3.5, 0.0])
BOTTOM_RIGHT_POS = np.array([4.2, -3.1, 0.0])
T_READOUT_POS = np.array([(layout.FACE_AXIS_X + layout.GRAPH_ORIGIN_X) / 2, layout.SINGLE_ORIGIN_Y - 1.0, 0.0])


def cubic_v(t: float) -> float:
    return (t - 1.0) * (t - 5.0) * (t - 8.0) / 15.0 + 3.0


class Scene05VtArea(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        face_axis = make_value_axis(np.array([layout.FACE_AXIS_X, layout.SINGLE_ORIGIN_Y, 0.0]), X_RANGE5, layout.SINGLE_AXIS_LENGTH)
        v_origin = np.array([layout.GRAPH_ORIGIN_X, layout.SINGLE_ORIGIN_Y, 0.0])
        v_axis = make_value_axis(v_origin, V_RANGE5, layout.SINGLE_AXIS_LENGTH)
        v_t_axis = make_t_axis(v_origin, T_RANGE5, layout.T_AXIS_LENGTH)
        x_axis_label = MathTex("x", color=PRIMARY, font_size=32).next_to(face_axis.get_end(), UP, buff=0.2)
        v_axis_label = MathTex("v", color=VELOCITY, font_size=32).next_to(v_axis.get_end(), UP, buff=0.2)
        t_axis_label = MathTex("t", color=FORMULA, font_size=32).next_to(v_t_axis.get_end(), RIGHT, buff=0.2)
        v_title = layout.make_graph_title("v-t graph",v_axis_label, color=VELOCITY)

        def v_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        face, face_update = layout.make_tracked_face(face_axis, lambda: 0.0)
        face.remove_updater(face_update)

        self.play(
            FadeIn(face_axis, v_axis, v_t_axis, face),
            Write(x_axis_label), Write(v_axis_label), Write(t_axis_label), Write(v_title),
            run_time=INTRO_TIME,
        )

        def play_synced_motion(v_of_t, x_of_t, run_time: float, t_max: float = T_MAX, point_fn=None) -> None:
            """After a stage's rectangles are already on screen, move a
            point along their top edges (v_of_t, possibly discontinuous)
            while "😁" climbs face_axis by the accumulating distance
            (x_of_t) in sync - review: sync the rectangles' top edge with
            😁's motion. A "v=" readout rides beside "😁"; a "t=" readout
            sits at a fixed spot between "😁" and the graph. No connector
            line forces a link between "😁" and the v-t graph (review).
            point_fn defaults to the main v0=0/v0!=0 graph's v_point -
            beat9 (the cubic function) passes cubic_point instead, since
            that graph uses different axes (review: the point's position on
            the graph didn't match the rectangles' top edge - caused by
            still using v_point there)."""
            resolved_point_fn = point_fn if point_fn is not None else v_point
            t2 = ValueTracker(0.0)
            v_dot = Dot(color=VELOCITY)

            v_readout_label = MathTex("v=", color=VELOCITY, font_size=34)
            v_readout_value = DecimalNumber(v_of_t(0.0), num_decimal_places=1, color=VELOCITY, font_size=34)
            t_readout_label = MathTex("t=", color=FORMULA, font_size=26)
            t_readout_value = DecimalNumber(0.0, num_decimal_places=1, color=FORMULA, font_size=26)
            t_readout_label.move_to(T_READOUT_POS, aligned_edge=RIGHT)
            t_readout_value.next_to(t_readout_label, RIGHT, buff=0.1)

            def update_face(mob) -> None:
                mob.move_to(face_axis.number_to_point(x_of_t(t2.get_value())) + RIGHT * layout.FACE_GAP)

            def update_v_dot(mob) -> None:
                t = t2.get_value()
                mob.move_to(resolved_point_fn(t, v_of_t(t)))

            def update_v_readout(group) -> None:
                label, value = v_readout_label, v_readout_value
                value.set_value(v_of_t(t2.get_value()))
                label.next_to(face, RIGHT, buff=0.35)
                value.next_to(label, RIGHT, buff=0.1)

            def update_t_readout_value(mob) -> None:
                mob.set_value(t2.get_value())
                mob.next_to(t_readout_label, RIGHT, buff=0.1)

            update_face(face)
            update_v_dot(v_dot)
            update_v_readout(None)
            update_t_readout_value(t_readout_value)
            self.play(FadeIn(v_dot), Write(v_readout_label), Write(v_readout_value), Write(t_readout_label), Write(t_readout_value), run_time=0.4)

            face.add_updater(update_face)
            v_dot.add_updater(update_v_dot)
            v_readout_label.add_updater(update_v_readout)
            t_readout_value.add_updater(update_t_readout_value)
            self.play(t2.animate.set_value(t_max), run_time=run_time, rate_func=linear)
            face.remove_updater(update_face)
            v_dot.remove_updater(update_v_dot)
            v_readout_label.remove_updater(update_v_readout)
            t_readout_value.remove_updater(update_t_readout_value)
            self.play(FadeOut(v_dot, v_readout_label, v_readout_value, t_readout_label, t_readout_value), run_time=0.3)

        def show_conclusion(point_fn, t_center: float, v_center: float) -> None:
            """Show the "area = distance traveled" conclusion as two lines
            overlaid on that v-t graph (review: show it overlaid, split
            across two lines, with the text's background filled in the
            background color). Shared as a helper since it's called 3
            times (v0=0/v0!=0/cubic function)."""
            line1 = Text(CONCLUSION_LINE1, color=FORMULA, font_size=20)
            line2 = Text(CONCLUSION_LINE2, color=FORMULA, font_size=20)
            group = VGroup(line1, line2).arrange(DOWN, buff=0.12)
            group.move_to(point_fn(t_center, v_center))
            bg = layout.make_text_bg(group)
            self.add(bg)
            self.play(Write(group), run_time=INTRO_TIME)
            self.wait(CONCLUSION_HOLD)
            self.play(FadeOut(bg, group), run_time=FADE_TIME)

        # --- Beat 1: the constant-velocity case (over the full t:0-4 domain). ---
        beat1_title = Text("For motion at constant velocity", color=VELOCITY, font_size=24)
        beat1_title.move_to(TOP_RIGHT_POS)
        self.play(Write(beat1_title), run_time=INTRO_TIME)

        const_line_mob = Line(v_point(0, BEAT1_V), v_point(T_MAX, BEAT1_V), color=VELOCITY, stroke_width=3)
        self.play(FadeIn(const_line_mob), run_time=INTRO_TIME)
        self.wait(GAP_TIME * 0.5)

        rect1 = Polygon(
            v_point(0, 0), v_point(T_MAX, 0), v_point(T_MAX, BEAT1_V), v_point(0, BEAT1_V),
            color=VELOCITY, fill_color=VELOCITY, fill_opacity=0.4, stroke_width=1,
        )
        width_brace = Brace(Line(v_point(0, 0), v_point(T_MAX, 0)), DOWN, color=FORMULA)
        width_label = MathTex("\\Delta t", color=FORMULA, font_size=36).next_to(width_brace, DOWN, buff=0.1)
        width_bg = layout.make_text_bg(width_label)
        height_brace = Brace(Line(v_point(0, 0), v_point(0, BEAT1_V)), LEFT, color=VELOCITY)
        height_label = MathTex("v", color=VELOCITY, font_size=36).next_to(height_brace, LEFT, buff=0.1)
        height_bg = layout.make_text_bg(height_label)
        area_label = MathTex("v\\,\\Delta t = 16\\,\\mathrm{m}", color=VELOCITY, font_size=34)
        area_label.move_to(rect1.get_center())

        self.play(FadeIn(rect1, width_brace, height_brace), run_time=INTRO_TIME)
        self.add(width_bg, height_bg)
        self.play(Write(width_label), Write(height_label), run_time=INTRO_TIME)
        self.wait(GAP_TIME)
        self.play(Write(area_label), run_time=INTRO_TIME)
        self.wait(GAP_TIME)

        play_synced_motion(lambda t: BEAT1_V, lambda t: BEAT1_V * t, SYNCED_MOTION_TIME)
        self.wait(GAP_TIME)

        # Before clearing it, show the "rectangle's area = speed x time =
        # distance traveled" correspondence in one line (review).
        rect_meaning = Text("Rectangle's area = speed × time = distance traveled", color=VELOCITY, font_size=22)
        rect_meaning.next_to(rect1, UP, buff=0.2)
        rect_meaning_bg = layout.make_text_bg(rect_meaning)
        self.add(rect_meaning_bg)
        self.play(Write(rect_meaning), run_time=INTRO_TIME)
        self.wait(5.0)

        self.play(
            FadeOut(
                beat1_title, const_line_mob, rect1, width_brace, width_bg, width_label, height_brace, height_bg, height_label, area_label,
                rect_meaning, rect_meaning_bg,
            ),
            run_time=FADE_TIME,
        )
        self.play(face.animate.move_to(face_axis.number_to_point(0.0) + RIGHT * layout.FACE_GAP), run_time=INTRO_TIME)

        # --- Beats 2-6: staircase approximation, main v0=0 example. ---
        def build_staircase(n: int, t_max: float, v_of_t, point_fn):
            dt = t_max / n
            rects = []
            total = 0.0
            for i in range(n):
                t0 = i * dt
                v0 = v_of_t(t0)
                total += v0 * dt
                rects.append(
                    Polygon(
                        point_fn(t0, 0), point_fn(t0 + dt, 0), point_fn(t0 + dt, v0), point_fn(t0, v0),
                        color=VELOCITY, fill_color=VELOCITY, fill_opacity=0.4, stroke_width=1,
                    )
                )
            return rects, total

        def step_functions(n: int, t_max: float, v_of_t):
            """(step_v, step_x): step_v is the staircase's discontinuous
            top-edge height at t; step_x is the exact running area up to t
            (piecewise-linear - the distance "😁" has covered so far)."""
            dt = t_max / n

            def index_at(t: float) -> int:
                return min(int(t / dt), n - 1)

            def step_v(t: float) -> float:
                return v_of_t(index_at(t) * dt)

            def step_x(t: float) -> float:
                idx = index_at(t)
                base = sum(v_of_t(k * dt) * dt for k in range(idx))
                return base + v_of_t(idx * dt) * (t - idx * dt)

            return step_v, step_x

        def make_detail_labels(n: int, t_max: float, v_of_t, rects_local) -> VGroup:
            """Per-rectangle "height x width" labels - skipped for a
            zero-area rectangle (review: no need to label a zero-area
            rectangle)."""
            dt = t_max / n
            group = VGroup()
            for i, rect in enumerate(rects_local):
                t0 = i * dt
                v0 = v_of_t(t0)
                if v0 == 0.0:
                    continue
                label = MathTex(f"{v0:.1f}\\times{dt:.2f}", color=FORMULA, font_size=16)
                label.move_to(rect.get_center())
                group.add(label)
            return group

        def make_division_label(n) -> VGroup:
            # review: use the math symbol \infty, not the Unicode "∞"
            # character - it can't mix into a Text string with a MathTex,
            # so keep them as separate parts (manim_notes.md).
            if isinstance(n, int):
                parts = [Text("Divided into", color=FORMULA, font_size=22), Text(f"{n}", color=FORMULA, font_size=22), Text("intervals", color=FORMULA, font_size=22)]
            else:
                parts = [Text("Divided into", color=FORMULA, font_size=22), MathTex("\\infty", color=FORMULA, font_size=26), Text("intervals", color=FORMULA, font_size=22)]
            group = VGroup(*parts).arrange(RIGHT, buff=0.1)
            group.move_to(BOTTOM_RIGHT_POS)
            return group

        line_full = Line(v_point(0, 0), v_point(T_MAX, motion.velocity_ua(T_MAX)), color=VELOCITY, stroke_width=3)
        self.play(FadeIn(line_full), run_time=INTRO_TIME)

        increase_title = Text("Velocity increases at a constant rate", color=VELOCITY, font_size=22)
        approx_title = Text("Approximated as a series of constant-velocity motions", color=FORMULA, font_size=22)
        increase_title.move_to(TOP_RIGHT_POS)
        approx_title.next_to(increase_title, DOWN, buff=0.25)
        self.play(Write(increase_title), run_time=INTRO_TIME)
        self.play(Write(approx_title), run_time=INTRO_TIME)

        total_label = Text("Area =", color=VELOCITY, font_size=28)  # review: no extra symbol like "S=", just "Area ="
        total_value = DecimalNumber(0.0, num_decimal_places=1, color=VELOCITY, font_size=30)
        total_label.next_to(approx_title, DOWN, buff=0.5)
        total_value.next_to(total_label, RIGHT, buff=0.15)

        rects, total = build_staircase(STAGES[0], T_MAX, motion.velocity_ua, v_point)

        rect_group = VGroup(*rects)
        division_label = make_division_label(STAGES[0])

        self.play(FadeIn(rect_group), run_time=INTRO_TIME)
        detail_labels = make_detail_labels(STAGES[0], T_MAX, motion.velocity_ua, rects)
        self.play(Write(detail_labels), Write(total_label), Write(total_value), Write(division_label), run_time=INTRO_TIME)
        total_value.set_value(total)
        self.wait(GAP_TIME * 0.5)
        step_v0, step_x0 = step_functions(STAGES[0], T_MAX, motion.velocity_ua)
        play_synced_motion(step_v0, step_x0, SYNCED_MOTION_TIME)
        self.wait(GAP_TIME)

        for n in STAGES[1:]:
            new_rects, new_total = build_staircase(n, T_MAX, motion.velocity_ua, v_point)
            new_group = VGroup(*new_rects)
            new_division_label = make_division_label(n)
            anims = [Transform(rect_group, new_group), total_value.animate.set_value(new_total), Transform(division_label, new_division_label)]
            if n in DETAILED_STAGES:
                new_details = make_detail_labels(n, T_MAX, motion.velocity_ua, new_rects)
                anims.append(Transform(detail_labels, new_details))
            else:
                anims.append(FadeOut(detail_labels))
            self.play(*anims, run_time=REFINE_TIME)
            if n not in DETAILED_STAGES:
                detail_labels = VGroup()
            total = new_total
            self.wait(GAP_TIME * 0.4)
            step_v_n, step_x_n = step_functions(n, T_MAX, motion.velocity_ua)
            play_synced_motion(step_v_n, step_x_n, max(1.2, SYNCED_MOTION_TIME - n * 0.02))
            self.wait(GAP_TIME * 0.4)

        # --- Beat 7: ∞ - shade the true triangle. ---
        triangle = Polygon(v_point(0, 0), v_point(T_MAX, 0), v_point(T_MAX, motion.velocity_ua(T_MAX)), color=VELOCITY, fill_color=VELOCITY, fill_opacity=0.5, stroke_width=0)
        exact_total = 0.5 * motion.ACCEL_A * T_MAX**2
        inf_division_label = make_division_label("inf")
        self.play(
            Transform(rect_group, triangle), total_value.animate.set_value(exact_total), Transform(division_label, inf_division_label),
            run_time=REFINE_TIME,
        )
        self.wait(GAP_TIME * 0.5)
        play_synced_motion(motion.velocity_ua, motion.position_ua, SYNCED_MOTION_TIME)
        self.wait(GAP_TIME)

        show_conclusion(v_point, T_MAX * 0.5, V_RANGE5[1] * 0.65)

        self.play(
            FadeOut(rect_group, line_full, total_label, total_value, division_label, increase_title, approx_title),
            run_time=FADE_TIME,
        )

        # --- Beat 8 (storyboard's own "Beat 7"): the case with a nonzero initial velocity, briefly. ---
        v0_line = Line(v_point(0, motion.V0), v_point(V0_T_MAX, motion.velocity_ua(V0_T_MAX, v0=motion.V0)), color=VELOCITY, stroke_width=3)
        self.play(face.animate.move_to(face_axis.number_to_point(0.0) + RIGHT * layout.FACE_GAP), FadeIn(v0_line), run_time=INTRO_TIME)

        def v0_velocity(t: float) -> float:
            return motion.velocity_ua(t, v0=motion.V0)

        v0_rects, v0_total = build_staircase(4, V0_T_MAX, v0_velocity, v_point)
        v0_group = VGroup(*v0_rects)
        v0_total_value = DecimalNumber(v0_total, num_decimal_places=1, color=VELOCITY, font_size=30)
        v0_total_label = Text("Area =", color=VELOCITY, font_size=28)
        v0_total_label.move_to(np.array([layout.GRAPH_ORIGIN_X + 4.0, layout.SINGLE_ORIGIN_Y + layout.SINGLE_AXIS_LENGTH + 0.6, 0.0]))
        v0_total_value.next_to(v0_total_label, RIGHT, buff=0.15)
        self.play(FadeIn(v0_group), Write(v0_total_label), Write(v0_total_value), run_time=INTRO_TIME)
        self.wait(GAP_TIME * 0.5)

        step_v_v0, step_x_v0 = step_functions(4, V0_T_MAX, v0_velocity)
        play_synced_motion(step_v_v0, step_x_v0, SYNCED_MOTION_TIME, t_max=V0_T_MAX)
        self.wait(GAP_TIME * 0.5)

        v0_trapezoid = Polygon(
            v_point(0, 0), v_point(V0_T_MAX, 0), v_point(V0_T_MAX, motion.velocity_ua(V0_T_MAX, v0=motion.V0)), v_point(0, motion.V0),
            color=VELOCITY, fill_color=VELOCITY, fill_opacity=0.5, stroke_width=0,
        )
        exact_v0_total = motion.V0 * V0_T_MAX + 0.5 * motion.ACCEL_A * V0_T_MAX**2
        self.play(Transform(v0_group, v0_trapezoid), v0_total_value.animate.set_value(exact_v0_total), run_time=REFINE_TIME)
        self.wait(GAP_TIME * 0.5)
        play_synced_motion(v0_velocity, lambda t: motion.position_ua(t, v0=motion.V0), SYNCED_MOTION_TIME, t_max=V0_T_MAX)
        self.wait(GAP_TIME * 0.5)

        show_conclusion(v_point, V0_T_MAX * 0.5, V_RANGE5[1] * 0.65)

        # Don't clear "😁"/face_axis here - they keep playing their synced
        # motion on the left into the cubic-curve part too (review).
        self.play(FadeOut(v0_group, v0_line, v0_total_label, v0_total_value), run_time=FADE_TIME)

        # --- Beat 9 (storyboard's own "Beat 8"): the case where
        # acceleration isn't constant - "A more complex motion", then the
        # same 2->4->...->∞ convergence, reused
        # via the generalized build_staircase/step_functions above. ---
        cubic_origin = np.array([layout.GRAPH_ORIGIN_X - 1.0, layout.SINGLE_ORIGIN_Y, 0.0])
        cubic_v_axis = make_value_axis(cubic_origin, CUBIC_V_RANGE, layout.SINGLE_AXIS_LENGTH)
        cubic_t_axis = make_t_axis(cubic_origin, CUBIC_T_RANGE, layout.T_AXIS_LENGTH)
        cubic_v_axis_label = MathTex("v", color=VELOCITY, font_size=32).next_to(cubic_v_axis.get_end(), UP, buff=0.2)
        cubic_title = layout.make_graph_title("v-t graph",cubic_v_axis_label, color=VELOCITY)

        def cubic_point(t: float, v: float) -> np.ndarray:
            return np.array([cubic_t_axis.number_to_point(t)[0], cubic_v_axis.number_to_point(v)[1], 0.0])

        # face_axis is also swapped for one with a wider range (the cubic's
        # total distance, ~28.65, exceeds X_RANGE5's top) - same origin/
        # length as before, so x_axis_label doesn't need to move (review:
        # keep showing 😁's synced motion on the left of the graph for the
        # cubic curve too).
        face_axis_cubic = make_value_axis(np.array([layout.FACE_AXIS_X, layout.SINGLE_ORIGIN_Y, 0.0]), CUBIC_X_RANGE, layout.SINGLE_AXIS_LENGTH)
        self.play(
            FadeOut(v_axis, v_t_axis, v_axis_label, t_axis_label, v_title, face_axis),
            FadeIn(cubic_v_axis, cubic_t_axis, face_axis_cubic),
            Write(cubic_v_axis_label), Write(cubic_title),
            face.animate.move_to(face_axis_cubic.number_to_point(0.0) + RIGHT * layout.FACE_GAP),
            run_time=FADE_TIME,
        )
        face_axis = face_axis_cubic

        complex_title = Text("A more complex motion", color=VELOCITY, font_size=24)
        complex_title.move_to(TOP_RIGHT_POS)
        self.play(Write(complex_title), run_time=INTRO_TIME)

        sample_ts = np.linspace(0.0, 9.0, 100)
        cubic_curve = VMobject(color=VELOCITY, stroke_width=3)
        cubic_curve.set_points_smoothly([cubic_point(t, cubic_v(t)) for t in sample_ts])
        self.play(FadeIn(cubic_curve), run_time=INTRO_TIME)

        cubic_rects, _ = build_staircase(STAGES[0], 9.0, cubic_v, cubic_point)
        cubic_group = VGroup(*cubic_rects)
        cubic_division_label = make_division_label(STAGES[0])
        cubic_division_label.move_to(BOTTOM_RIGHT_POS + np.array([-1.6, 0.0, 0.0]))
        self.play(FadeIn(cubic_group), Write(cubic_division_label), run_time=INTRO_TIME)
        self.wait(GAP_TIME * 0.5)
        step_v0c, step_x0c = step_functions(STAGES[0], 9.0, cubic_v)
        play_synced_motion(step_v0c, step_x0c, SYNCED_MOTION_TIME, t_max=9.0, point_fn=cubic_point)
        self.wait(GAP_TIME * 0.5)

        for n in [*STAGES[1:], "inf"]:
            # "∞" is approximated with a very fine staircase (a true
            # closed-form fill polygon under a cubic isn't needed here -
            # visually indistinguishable at this resolution).
            n_div = 200 if n == "inf" else n
            new_rects, _ = build_staircase(n_div, 9.0, cubic_v, cubic_point)
            new_cubic_group = VGroup(*new_rects)
            new_label = make_division_label(n)
            new_label.move_to(BOTTOM_RIGHT_POS + np.array([-1.6, 0.0, 0.0]))
            self.play(Transform(cubic_group, new_cubic_group), Transform(cubic_division_label, new_label), run_time=REFINE_TIME)
            # review: right after a Transform the gap is easy to spot, so hold a bit longer.
            self.wait(GAP_TIME * 0.6)
            step_v_n, step_x_n = step_functions(n_div, 9.0, cubic_v)
            play_synced_motion(step_v_n, step_x_n, max(1.2, SYNCED_MOTION_TIME - n_div * 0.01), t_max=9.0, point_fn=cubic_point)
            self.wait(GAP_TIME * 0.4)

        show_conclusion(cubic_point, 4.5, CUBIC_V_RANGE[1] * 0.75)

        self.play(FadeOut(*self.mobjects), run_time=FADE_TIME)
