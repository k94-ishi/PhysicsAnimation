"""Scene 5: Connecting to the v-t graph.

Implements storyboard.md > Scene 5, following its three beats:
  1. Scene04's ending layout (face axis + x-t graph, no plot/tangent/
     equations — those were specific to that scene's teaching point) is
     rebuilt, then compressed into the upper half of the screen: only the
     vertical scale and position change (same horizontal scale, same tick
     range/values), and the "😁"/its axis shrink and move the same way. A
     v-t graph is then added below.
  2. The "😁", the x-t graph, and the v-t graph update in sync: a dot plots
     each graph live, a live tangent line tracks the x-t curve's slope, and
     a dashed line connects the two graphs' current points (same t). Motion
     pauses briefly at each zero/max/min-velocity moment. The already-drawn
     curve is never cleared while this same motion is still being plotted.
  3. Four contrasting motions are compared, one at a time, in the same
     layout — each shown together with the "😁" moving on its own axis in
     sync, not just as bare curves.

Continuity with scene04: this scene opens with the "😁" at
common.motion_profile.position(scene04's SCENE4_END_T, MAIN_X0) — imported
as SCENE4_END_X — matching scene04's own standard (non-compressed) layout,
then glides x0 to MAIN_X0 (the same "start where the previous scene ended,
then reset" idiom scene04 itself used against scene03) before compressing
that exact layout for beat 1, rather than jumping straight to an
already-compressed state.

The quadratic term in common.motion_profile.QUADRATIC_COEFFICIENT is added
on top of position()/velocity() only here, for beats 1-2's main demo — per
the user's review, it is scoped to "only when considering the v-t graph",
not the shared motion scenes 1-4 use. Beat 3's four comparison patterns are
their own separate, simple motions (not this scene's main demo), chosen to
each show a qualitatively different x-t/v-t shape.

No narration text is rendered on screen; narration is delivered as separate
voiceover per the project's workflow (see CLAUDE.md > Development Workflow).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import (
    RIGHT,
    UP,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Scene,
    TracedPath,
    Transform,
    ValueTracker,
    VMobject,
    linear,
)

from common.colors import BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.graph_layout import (
    CONNECTOR_LINE_COLOR,
    CONNECTOR_Z_INDEX,
    FACE_AXIS_X,
    FACE_Z_INDEX,
    GRAPH_ORIGIN,
    ROTATED_X_AXIS_LENGTH,
    make_t_axis,
    make_value_axis,
    make_vertical_x_axis,
)
from common.motion_profile import MAIN_X0, find_key_velocity_events, position_v5, velocity_v5
from common.position_track import TRACK_X_MIN, make_tracked_face
from units.mechanics.mechanics_how_to_express_movements.scene04_velocity_and_slope import SCENE4_END_X

EVENT_T_MIN = 0.0
EVENT_T_MAX = 7.0

# Beat 1's compressed layout: same horizontal scale/position as scene04
# (GRAPH_ORIGIN's x, FACE_AXIS_X, and the t-axis length are all unchanged),
# only the vertical scale (axis length) and vertical position shrink to fit
# both graphs on screen.
COMPRESSED_AXIS_LENGTH = 3.0
UPPER_ORIGIN_Y = 0.9
LOWER_ORIGIN_Y = -2.3
V_VALUE_RANGE = [-4, 4, 2]
COMPRESSION_FACTOR = COMPRESSED_AXIS_LENGTH / ROTATED_X_AXIS_LENGTH
# At COMPRESSED_AXIS_LENGTH, the shared track's full step=1 density (13
# numbers over a 12-unit range) would overlap illegibly; only every other
# number is kept — same values, just fewer printed. scene06 reuses this
# list too, since it continues this same compressed axis.
COMPRESSED_NUMBERS_TO_EXCLUDE = [1, 3, 5, 7, 9, 11]

TANGENT_HALF_SPAN = 0.6  # seconds of t shown by the live tangent line

CONTINUITY_FADE_TIME = 0.6
CONTINUITY_GLIDE_TIME = 1.0  # smooth glide from SCENE4_END_X to MAIN_X0, not a jump

BEAT1_COMPRESS_TIME = 1.5
BEAT1_TICKS_REVEAL_TIME = 0.8
BEAT1_VT_FADE_TIME = 1.5

BEAT2_INTRO_TIME = 0.5
BEAT2_TRAVEL_BUDGET = 6.0  # seconds of travel time spread across all t=0..7 segments
BEAT2_EVENT_PAUSE_TIME = 0.8

BEAT3_RESET_TIME = 0.3
BEAT3_DRAW_TIME = 3.0
BEAT3_HOLD_TIME = 1.0  # "pause for about 1 second, to make the differences easy to compare"
BEAT3_FADE_OUT_TIME = 0.4


# Beat 3's four comparison motions: constant velocity, speeding up, slowing
# to a stop then reversing, and oscillating. Each is its own simple motion,
# not this scene's main (quadratic-modified) demo, chosen to each produce a
# qualitatively different x-t/v-t shape within the same axis ranges used
# throughout this scene (position within face_axis's shared TRACK range,
# velocity within V_VALUE_RANGE).
COMPARISON_PATTERNS = [
    (lambda t: 1.0 + 1.0 * t, lambda t: 0.0 * t + 1.0),  # constant-velocity straight-line motion
    (lambda t: 1.0 + 0.15 * t**2, lambda t: 0.3 * t),  # uniformly accelerated motion, speeding up
    (lambda t: 2.0 + 2.0 * t - 0.3 * t**2, lambda t: 2.0 - 0.6 * t),  # uniformly accelerated motion, slowing down and reversing
    (lambda t: 2.5 * np.sin(1.3 * t) + 4.5, lambda t: 3.25 * np.cos(1.3 * t)),  # simple harmonic motion
]


class Scene05VelocityTimeGraph(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --- Continuity: rebuild scene04's ending layout (face axis, face
        # at SCENE4_END_X, x-t graph) at its standard scale/position — no
        # plot/tangent/equations, which were specific to that scene's
        # teaching point and don't carry over. ---
        face_axis = make_vertical_x_axis(np.array([FACE_AXIS_X, GRAPH_ORIGIN[1], 0.0]))
        graph_x_axis = make_vertical_x_axis(GRAPH_ORIGIN)
        graph_t_axis = make_t_axis(GRAPH_ORIGIN)
        x_axis_label = MathTex("x", color=FORMULA).next_to(graph_x_axis.get_end(), UP, buff=0.3)
        t_axis_label = MathTex("t", color=FORMULA).next_to(graph_t_axis.get_end(), RIGHT, buff=0.3)

        t_tracker = ValueTracker(0.0)
        x0_tracker = ValueTracker(SCENE4_END_X)
        face, update_face = make_tracked_face(face_axis, lambda: position_v5(t_tracker.get_value(), x0_tracker.get_value()))
        face.set_z_index(FACE_Z_INDEX)

        self.play(
            FadeIn(face_axis, graph_x_axis, graph_t_axis, x_axis_label, t_axis_label, face),
            run_time=CONTINUITY_FADE_TIME,
        )

        # x0_tracker starts at SCENE4_END_X (an absolute position value, not
        # an offset) so the "😁" appears exactly where scene04 left it, then
        # glides to MAIN_X0 — the x0 beat 2's x_dot/tangent_line assume via
        # the plain MAIN_X0 constant — before any plotting begins. Without
        # this glide, x0_tracker would stay at SCENE4_END_X for the rest of
        # the scene while the graph plots against MAIN_X0, permanently
        # offsetting the "😁" from its own x-t graph point (the dashed line
        # between them would never be level). Same idiom as scene04's own
        # glide from SCENE3_END_X.
        self.play(x0_tracker.animate.set_value(MAIN_X0), run_time=CONTINUITY_GLIDE_TIME)

        # --- Beat 1: compress into the upper half — same horizontal scale
        # and tick range/values, only the vertical scale and position
        # change — then add a v-t graph below it.
        #
        # face_axis/graph_x_axis's ticks/numbers are detached before the
        # stretch and regenerated after, exactly like scene03's t-axis
        # extension: a naive Transform between two differently-sized
        # NumberLines (even at the same rotation) mismatches the number
        # glyphs' internal point structure frame-by-frame, visibly warping
        # the digits mid-animation (see manim_notes.md > NumberLine). Only
        # the bare lines are animated directly; graph_t_axis and the "x"/"t"
        # labels only change position (not length), so a plain Transform is
        # safe for them. ---
        upper_origin = np.array([GRAPH_ORIGIN[0], UPPER_ORIGIN_Y, 0.0])
        face_axis_target = make_vertical_x_axis(np.array([FACE_AXIS_X, UPPER_ORIGIN_Y, 0.0]), length=COMPRESSED_AXIS_LENGTH)
        graph_x_axis_target = make_vertical_x_axis(upper_origin, length=COMPRESSED_AXIS_LENGTH)
        graph_t_axis_target = make_t_axis(upper_origin)
        x_axis_label_target = MathTex("x", color=FORMULA).next_to(graph_x_axis_target.get_end(), UP, buff=0.2)
        t_axis_label_target = MathTex("t", color=FORMULA).next_to(graph_t_axis_target.get_end(), RIGHT, buff=0.2)

        face_axis_ticks, face_axis_numbers = face_axis.ticks, face_axis.numbers
        face_axis.remove(face_axis_ticks, face_axis_numbers)
        graph_x_axis_ticks, graph_x_axis_numbers = graph_x_axis.ticks, graph_x_axis.numbers
        graph_x_axis.remove(graph_x_axis_ticks, graph_x_axis_numbers)

        self.play(
            face_axis.animate.put_start_and_end_on(face_axis_target.get_start(), face_axis_target.get_end()),
            graph_x_axis.animate.put_start_and_end_on(graph_x_axis_target.get_start(), graph_x_axis_target.get_end()),
            Transform(graph_t_axis, graph_t_axis_target),
            Transform(x_axis_label, x_axis_label_target),
            Transform(t_axis_label, t_axis_label_target),
            face.animate.scale(COMPRESSION_FACTOR),
            run_time=BEAT1_COMPRESS_TIME,
        )

        face_axis.add_ticks()
        face_axis.add_numbers(excluding=[0, TRACK_X_MIN, *COMPRESSED_NUMBERS_TO_EXCLUDE])
        graph_x_axis.add_ticks()
        graph_x_axis.add_numbers(excluding=[0, TRACK_X_MIN, *COMPRESSED_NUMBERS_TO_EXCLUDE])
        # A plain opacity animate on the freshly regenerated children, not
        # FadeIn: FadeIn(parent.ticks, parent.numbers) breaks the parent
        # axis line's own rendering (see manim_notes.md).
        face_axis.ticks.set_opacity(0)
        face_axis.numbers.set_opacity(0)
        graph_x_axis.ticks.set_opacity(0)
        graph_x_axis.numbers.set_opacity(0)
        self.play(
            face_axis.ticks.animate.set_opacity(1),
            face_axis.numbers.animate.set_opacity(1),
            graph_x_axis.ticks.animate.set_opacity(1),
            graph_x_axis.numbers.animate.set_opacity(1),
            run_time=BEAT1_TICKS_REVEAL_TIME,
        )

        lower_origin = np.array([GRAPH_ORIGIN[0], LOWER_ORIGIN_Y, 0.0])
        v_axis = make_value_axis(lower_origin, V_VALUE_RANGE, COMPRESSED_AXIS_LENGTH)
        v_t_axis = make_t_axis(lower_origin)
        v_axis_label = MathTex("v", color=VELOCITY).next_to(v_axis.get_end(), UP, buff=0.2)
        self.play(FadeIn(v_axis, v_t_axis, v_axis_label), run_time=BEAT1_VT_FADE_TIME)

        def x_graph_point(t: float, x: float) -> np.ndarray:
            return np.array([graph_t_axis.number_to_point(t)[0], graph_x_axis.number_to_point(x)[1], 0.0])

        def v_graph_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        # --- Beat 2: the "😁", the x-t graph, and the v-t graph update in
        # sync; pause briefly at each zero/max/min-velocity moment. The
        # already-drawn curve (TracedPath, below) is never cleared while
        # this same motion is still being plotted. ---
        x_dot = Dot(color=PRIMARY)
        v_dot = Dot(color=VELOCITY)
        connector_line = DashedLine(color=CONNECTOR_LINE_COLOR)
        connector_line.set_z_index(CONNECTOR_Z_INDEX)
        # Links the "😁" to its x-t graph point, matching every prior
        # scene's face<->graph connector (see e.g. scene04); distinct from
        # connector_line above, which links the x-t and v-t graph points.
        face_connector_line = DashedLine(color=CONNECTOR_LINE_COLOR)
        face_connector_line.set_z_index(CONNECTOR_Z_INDEX)
        tangent_line = Line(color=VELOCITY, stroke_width=3)

        def update_x_dot(mob: Dot) -> None:
            t_value = t_tracker.get_value()
            mob.move_to(x_graph_point(t_value, position_v5(t_value, MAIN_X0)))

        def update_v_dot(mob: Dot) -> None:
            t_value = t_tracker.get_value()
            mob.move_to(v_graph_point(t_value, velocity_v5(t_value)))

        def update_connector_line(mob: DashedLine) -> None:
            mob.put_start_and_end_on(x_dot.get_center(), v_dot.get_center())

        def update_face_connector_line(mob: DashedLine) -> None:
            mob.put_start_and_end_on(face.get_center(), x_dot.get_center())

        def update_tangent_line(mob: Line) -> None:
            t_value = t_tracker.get_value()
            x_value = position_v5(t_value, MAIN_X0)
            slope = velocity_v5(t_value)
            mob.put_start_and_end_on(
                x_graph_point(t_value - TANGENT_HALF_SPAN, x_value - slope * TANGENT_HALF_SPAN),
                x_graph_point(t_value + TANGENT_HALF_SPAN, x_value + slope * TANGENT_HALF_SPAN),
            )

        # Set correct initial positions before anything watches these mobjects,
        # so TracedPath never samples a default (uninitialized) construction point.
        update_x_dot(x_dot)
        update_v_dot(v_dot)
        update_connector_line(connector_line)
        update_face_connector_line(face_connector_line)
        update_tangent_line(tangent_line)

        self.play(
            FadeIn(x_dot, v_dot, connector_line, face_connector_line, tangent_line), run_time=BEAT2_INTRO_TIME
        )

        x_dot.add_updater(update_x_dot)
        v_dot.add_updater(update_v_dot)
        connector_line.add_updater(update_connector_line)
        face_connector_line.add_updater(update_face_connector_line)
        tangent_line.add_updater(update_tangent_line)

        x_traced_path = TracedPath(x_dot.get_center, stroke_color=PRIMARY, stroke_width=3)
        v_traced_path = TracedPath(v_dot.get_center, stroke_color=VELOCITY, stroke_width=3)
        self.add(x_traced_path, v_traced_path)

        events = find_key_velocity_events(EVENT_T_MIN, EVENT_T_MAX, velocity_fn=velocity_v5)
        total_travel_t = EVENT_T_MAX - EVENT_T_MIN
        previous_t = EVENT_T_MIN
        for t_stop, kind in [*events, (EVENT_T_MAX, None)]:
            segment_length = t_stop - previous_t
            run_time = BEAT2_TRAVEL_BUDGET * segment_length / total_travel_t
            self.play(t_tracker.animate.set_value(t_stop), run_time=run_time, rate_func=linear)
            if kind is not None:
                self.wait(BEAT2_EVENT_PAUSE_TIME)
            previous_t = t_stop

        # Freeze the traces before beat 3's fresh comparisons reuse the same
        # axes and dots' updaters are removed (see manim_notes.md > TracedPath).
        x_traced_path.clear_updaters()
        v_traced_path.clear_updaters()
        x_dot.remove_updater(update_x_dot)
        v_dot.remove_updater(update_v_dot)
        connector_line.remove_updater(update_connector_line)
        face_connector_line.remove_updater(update_face_connector_line)
        tangent_line.remove_updater(update_tangent_line)
        face.remove_updater(update_face)
        self.remove(face, x_dot, v_dot, connector_line, face_connector_line, tangent_line, x_traced_path, v_traced_path)

        # --- Beat 3: compare four contrasting motions, one at a time, in
        # the same layout — the "😁" moves on its own axis in sync with each
        # pattern's x-t/v-t curves, not just bare curves on their own. Each
        # pattern's curve is only ever cleared (FadeOut) after its full draw
        # and hold are done, never mid-plot. ---
        for position_fn, velocity_fn in COMPARISON_PATTERNS:
            pattern_t_tracker = ValueTracker(0.0)
            pattern_face, pattern_update_face = make_tracked_face(
                face_axis, lambda pf=position_fn: pf(pattern_t_tracker.get_value())
            )
            pattern_face.set_z_index(FACE_Z_INDEX)

            pattern_x_dot = Dot(color=PRIMARY)
            pattern_v_dot = Dot(color=VELOCITY)
            pattern_face_connector = DashedLine(color=CONNECTOR_LINE_COLOR)
            pattern_face_connector.set_z_index(CONNECTOR_Z_INDEX)

            def update_pattern_x_dot(mob: Dot, pf=position_fn) -> None:
                t_value = pattern_t_tracker.get_value()
                mob.move_to(x_graph_point(t_value, pf(t_value)))

            def update_pattern_v_dot(mob: Dot, vf=velocity_fn) -> None:
                t_value = pattern_t_tracker.get_value()
                mob.move_to(v_graph_point(t_value, vf(t_value)))

            def update_pattern_face_connector(mob: DashedLine) -> None:
                mob.put_start_and_end_on(pattern_face.get_center(), pattern_x_dot.get_center())

            update_pattern_x_dot(pattern_x_dot)
            update_pattern_v_dot(pattern_v_dot)
            update_pattern_face_connector(pattern_face_connector)
            pattern_x_dot.add_updater(update_pattern_x_dot)
            pattern_v_dot.add_updater(update_pattern_v_dot)
            pattern_face_connector.add_updater(update_pattern_face_connector)

            pattern_x_traced = TracedPath(pattern_x_dot.get_center, stroke_color=PRIMARY, stroke_width=3)
            pattern_v_traced = TracedPath(pattern_v_dot.get_center, stroke_color=VELOCITY, stroke_width=3)

            self.play(
                FadeIn(pattern_face, pattern_x_dot, pattern_v_dot, pattern_face_connector),
                run_time=BEAT3_RESET_TIME,
            )
            self.add(pattern_x_traced, pattern_v_traced)
            self.play(pattern_t_tracker.animate.set_value(EVENT_T_MAX), run_time=BEAT3_DRAW_TIME, rate_func=linear)
            self.wait(BEAT3_HOLD_TIME)

            pattern_face.remove_updater(pattern_update_face)
            pattern_x_dot.remove_updater(update_pattern_x_dot)
            pattern_v_dot.remove_updater(update_pattern_v_dot)
            pattern_face_connector.remove_updater(update_pattern_face_connector)
            pattern_x_traced.clear_updaters()
            pattern_v_traced.clear_updaters()
            self.play(
                FadeOut(
                    pattern_face, pattern_x_dot, pattern_v_dot, pattern_face_connector,
                    pattern_x_traced, pattern_v_traced,
                ),
                run_time=BEAT3_FADE_OUT_TIME,
            )
