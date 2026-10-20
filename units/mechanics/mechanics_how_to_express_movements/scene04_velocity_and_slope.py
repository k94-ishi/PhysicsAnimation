"""Scene 4: Tangent slope and velocity.

Implements storyboard.md > Scene 4, following its seven beats:
  1. The "😁" keeps moving beside the x-t graph with a live "v=" readout;
     the x-t graph plots live in sync, and zero/max/min-velocity moments are
     marked on the curve as they're crossed — the plot never stops or
     pauses for these markers.
  2. The same motion simply replays from t=0 to t=7 again.
  3. The "😁" settles at the max-velocity point (this beat's subject); its
     live "v=" readout — now showing v_max — moves to sit near the graph so
     it stays visible through beat 4's zoom. A tangent line is drawn there.
  4. The camera zooms into that point and its tangent line; the "v="
     readout stays in view.
  5. The points 1s before/after the tangent point are marked, and Δt/Δx are
     computed explicitly (Δt = t2 - t1 = ..., Δx = x2 - x1 = ...) before
     beat 6's division.
  6. Δx/Δt is computed from those two values.
  7. The camera zooms back out; the slope result and the original "v="
     readout are highlighted together to emphasize they're the same number.

Continuity with scene03: this scene opens with the "😁" at
common.motion_profile.position(scene03's SCENE3_END_T, scene03's
BEAT4_NEW_X0) — imported directly as SCENE3_END_X — then glides smoothly to
common.motion_profile.MAIN_X0 before beat 1's own demonstration begins, the
same "start where the previous scene ended, then reset" idiom scene03 itself
used against scene02. The layout (face axis + separate x-t graph) is rebuilt
fresh at its standard (non-extended) range, matching every prior scene's
starting state rather than scene03's extended-for-t<0 ending state: only the
"😁"'s position value carries over, not the axis's shape.

x0 is kept at MAIN_X0 (not 0) for beats 1-2 purely so the "😁"'s x(t) stays
within the shared axis's range for this t window.

The tangent line in beats 3-6 is built directly from the analytic velocity
at the max point (a straight-line extrapolation), not sampled from the
curve, so the Δx/Δt computed in beat 6 is exactly the max velocity from
beat 1's readout, not merely close to it — beat 7's final emphasis relies
on this being an exact match, not an approximation.

No narration text is rendered on screen; narration is delivered as separate
voiceover per the project's workflow (see CLAUDE.md > Development Workflow).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    MathTex,
    MovingCameraScene,
    TracedPath,
    ValueTracker,
    VGroup,
    linear,
)
from manim.mobject.text.numbers import DecimalNumber

from common.colors import BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.graph_layout import (
    CONNECTOR_LINE_COLOR,
    CONNECTOR_Z_INDEX,
    FACE_AXIS_X,
    FACE_Z_INDEX,
    GRAPH_ORIGIN,
    make_t_axis,
    make_vertical_x_axis,
)
from common.motion_profile import MAIN_X0, find_key_velocity_events, position, velocity
from common.position_track import make_tracked_face
from units.mechanics.mechanics_how_to_express_movements.scene03_time_and_initial_position import SCENE3_END_X

# The window searched for velocity events; matches the x-t graph's t-axis
# range (common.graph_layout.GRAPH_T_RANGE), so events found here land
# inside the graph's visible span.
EVENT_T_MIN = 0.0
EVENT_T_MAX = 7.0

EVENT_LABELS = {"zero": "v=0", "min": "v_{\\min}", "max": "v_{\\max}"}

CONTINUITY_FADE_TIME = 0.6
CONTINUITY_GLIDE_TIME = 1.2  # smooth glide from SCENE3_END_X to MAIN_X0, not a jump

BEAT1_TRAVEL_BUDGET = 6.0  # one continuous t=0..7 pass; markers pop in as crossed, no pausing

BEAT1_FADE_OUT_TIME = 0.6  # beat 1's finished plot fades out, rather than rewinding
BEAT2_INTRO_TIME = 0.4  # fade back in at t=0 for beat 2's fresh replay
BEAT2_TRAVEL_BUDGET = 4.0  # a plain repeat, faster than beat 1's first pass

SETTLE_AT_MAX_TIME = 1.5  # glide back from t=7 to max_event_t, where beat 3 picks up
V_GROUP_MOVE_TIME = 1.0

BEAT3_TANGENT_TIME = 1.5
BEAT3_HOLD_TIME = 2.0
TANGENT_HALF_SPAN = 1.5  # seconds of t shown by the (unzoomed) tangent line

BEAT4_ZOOM_TIME = 3.0
BEAT4_HOLD_TIME = 2.0
ZOOM_SCALE = 0.4  # camera.frame shrinks to this fraction of its normal size

BEAT5_MARKER_TIME = 1.0
BEAT5_BRACE_TIME = 1.5
BEAT5_DELTA_T_EQ_TIME = 1.2
BEAT5_DELTA_X_EQ_TIME = 1.2
BEAT5_HOLD_TIME = 1.0
DELTA_T_HALF = 1.0  # "1 second on each side of the tangent point"

BEAT6_SLOPE_EQ_TIME = 1.5
BEAT6_HOLD_TIME = 1.0

BEAT7_UNZOOM_TIME = 2.0
BEAT7_CONFIRM_TIME = 1.5
BEAT7_HOLD_TIME = 1.5

# Computed once at import time (not per-render) so scene05 can read exactly
# where this scene's "😁" comes to rest — settled at the max-velocity point
# from beat 3 onward, and never moved again — and open with it already at
# this position, for a seamless cut.
_EVENTS = find_key_velocity_events(EVENT_T_MIN, EVENT_T_MAX)
SCENE4_END_T = next(t for t, kind in _EVENTS if kind == "max")
SCENE4_END_X = position(SCENE4_END_T, MAIN_X0)


class Scene04VelocityAndSlope(MovingCameraScene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        events = _EVENTS
        max_event_t = SCENE4_END_T
        v_max = velocity(max_event_t)
        x_at_max = position(max_event_t, MAIN_X0)

        # --- Layout: same standard (non-extended) axes every prior scene
        # starts with; only the "😁"'s position value carries over from
        # scene03, not its ending axis shape. ---
        face_axis = make_vertical_x_axis(np.array([FACE_AXIS_X, GRAPH_ORIGIN[1], 0.0]))
        graph_x_axis = make_vertical_x_axis(GRAPH_ORIGIN)
        graph_t_axis = make_t_axis(GRAPH_ORIGIN)
        x_axis_label = MathTex("x", color=FORMULA).next_to(graph_x_axis.get_end(), UP, buff=0.3)
        t_axis_label = MathTex("t", color=FORMULA).next_to(graph_t_axis.get_end(), RIGHT, buff=0.3)

        def graph_point(t: float, x: float) -> np.ndarray:
            return np.array([graph_t_axis.number_to_point(t)[0], graph_x_axis.number_to_point(x)[1], 0.0])

        t_tracker = ValueTracker(0.0)
        x0_tracker = ValueTracker(SCENE3_END_X)
        face, update_face = make_tracked_face(face_axis, lambda: position(t_tracker.get_value(), x0_tracker.get_value()))
        face.set_z_index(FACE_Z_INDEX)

        axis_point = Dot(color=PRIMARY)
        connector_line = DashedLine(color=CONNECTOR_LINE_COLOR)
        connector_line.set_z_index(CONNECTOR_Z_INDEX)

        def update_axis_point_height_only(mob: Dot) -> None:
            x_value = position(t_tracker.get_value(), x0_tracker.get_value())
            mob.move_to(graph_x_axis.number_to_point(x_value))

        def update_connector_line(mob: DashedLine) -> None:
            mob.put_start_and_end_on(face.get_center(), axis_point.get_center())

        update_axis_point_height_only(axis_point)
        update_connector_line(connector_line)
        axis_point.add_updater(update_axis_point_height_only)
        connector_line.add_updater(update_connector_line)

        # --- Continuity: start at scene03's ending position, then glide
        # smoothly to MAIN_X0 (kept within the axis's range for beats 1-2). ---
        self.play(
            FadeIn(face_axis, graph_x_axis, graph_t_axis, x_axis_label, t_axis_label, face, axis_point, connector_line),
            run_time=CONTINUITY_FADE_TIME,
        )
        self.play(x0_tracker.animate.set_value(MAIN_X0), run_time=CONTINUITY_GLIDE_TIME)

        # --- Beat 1: the "😁" keeps moving with a live "v=" readout, while
        # the x-t graph plots live in sync; zero/max/min-velocity moments are
        # marked on the curve as they're crossed, without ever stopping the
        # plot. ---
        axis_point.remove_updater(update_axis_point_height_only)

        def update_axis_point_plot(mob: Dot) -> None:
            t_value = t_tracker.get_value()
            mob.move_to(graph_point(t_value, position(t_value, MAIN_X0)))

        update_axis_point_plot(axis_point)
        axis_point.add_updater(update_axis_point_plot)

        # A fixed screen position, not next_to(face, ...): face_axis's own
        # tick numbers sit immediately left of wherever the "😁" is, so a
        # label attached above/beside the face collides with them at most
        # heights (see skills/physics-video-review/SKILL.md).
        v_label = MathTex("v=", color=VELOCITY)
        v_value = DecimalNumber(velocity(0.0), num_decimal_places=1, color=VELOCITY)
        v_label.move_to([FACE_AXIS_X, -3.0, 0.0])
        v_group = VGroup(v_label, v_value)

        def update_v_group(group: VGroup) -> None:
            label, value = group
            value.set_value(velocity(t_tracker.get_value()))
            value.next_to(label, buff=0.15)

        # Appear already-correct, not via an entrance animation: any fade-in
        # here leaves a brief window where the label's position/value lags
        # the moving face, which reads as a visible glitch (see scene01).
        update_v_group(v_group)
        self.add(v_group)
        v_group.add_updater(update_v_group)

        traced_path = TracedPath(axis_point.get_center, stroke_color=PRIMARY, stroke_width=3)
        self.add(traced_path)

        # Markers pop in the instant their event's t is crossed, driven by an
        # invisible watcher's updater — not by pausing self.play calls — so
        # the plot never stops for them (see skills/.../manim_notes.md).
        # These markers (both dots and labels) stay on screen for the rest
        # of the scene once shown — they are never faded out or removed,
        # only temporarily dimmed (labels only) during beat 4's zoom, since
        # at that scale they'd sit right where beat 5's equations go.
        pending_events = list(events)
        event_marker_labels = []

        def check_events(mob: Dot) -> None:
            while pending_events and pending_events[0][0] <= t_tracker.get_value():
                t_event, kind = pending_events.pop(0)
                dot = Dot(graph_point(t_event, position(t_event, MAIN_X0)), color=VELOCITY, radius=0.07)
                label = MathTex(EVENT_LABELS[kind], color=VELOCITY, font_size=28).next_to(dot, RIGHT, buff=0.1)
                event_marker_labels.append(label)
                self.add(dot, label)

        event_watcher = Dot(radius=0)
        event_watcher.add_updater(check_events)
        self.add(event_watcher)

        self.play(t_tracker.animate.set_value(EVENT_T_MAX), run_time=BEAT1_TRAVEL_BUDGET, rate_func=linear)
        event_watcher.clear_updaters()
        self.remove(event_watcher)
        traced_path.clear_updaters()

        # --- End of beat 1: fade the finished plot out (curve, dot, "😁",
        # velocity readout) instead of animating a "rewind" back to t=0 — a
        # rewind reads as the motion reversing, which isn't what beat 2 means
        # by "replay". The event markers (dots/labels for v=0, v_min, v_max)
        # are NOT included here: they stay visible for the rest of the scene,
        # not just for beat 1. Cut straight to t=0 while hidden, then fade
        # back in and plot forward again with a fresh curve (the old
        # TracedPath was just faded out, so it can't keep drawing). ---
        self.play(
            FadeOut(traced_path, axis_point, face, v_group),
            run_time=BEAT1_FADE_OUT_TIME,
        )
        t_tracker.set_value(0.0)
        update_face(face)
        update_axis_point_plot(axis_point)
        update_v_group(v_group)

        # --- Beat 2: simply replay the same motion's plot from t=0 to t=7. ---
        traced_path = TracedPath(axis_point.get_center, stroke_color=PRIMARY, stroke_width=3)
        self.add(traced_path)
        self.play(FadeIn(face, axis_point, v_group), run_time=BEAT2_INTRO_TIME)
        self.play(t_tracker.animate.set_value(EVENT_T_MAX), run_time=BEAT2_TRAVEL_BUDGET, rate_func=linear)
        traced_path.clear_updaters()

        # --- Settle at the max-velocity point (this is beat 3's subject):
        # glide back there, then move the live "v=" readout (now showing
        # v_max) to sit near the graph, so it stays visible through beat 4's
        # zoom instead of being left behind at its original fixed corner.
        # These are two separate plays, not one combined: while t_tracker is
        # still moving, velocity() crosses zero (its sign flips between
        # t=7 and max_event_t), changing v_value's DecimalNumber glyph count
        # every frame — animating v_group itself at the same time hits the
        # DecimalNumber-updater/animation-interpolation crash documented in
        # manim_notes.md. Moving v_group only after t_tracker is at rest
        # (so velocity(), and the glyph count, stays fixed) avoids it. ---
        self.play(t_tracker.animate.set_value(max_event_t), run_time=SETTLE_AT_MAX_TIME, rate_func=linear)
        v_group_target = graph_point(max_event_t - 2.0, x_at_max + 3.0)
        self.play(v_group.animate.move_to(v_group_target), run_time=V_GROUP_MOVE_TIME)

        # --- Beat 3: draw the tangent line at the max-velocity point. ---
        tangent_line = Line(
            graph_point(max_event_t - TANGENT_HALF_SPAN, x_at_max - v_max * TANGENT_HALF_SPAN),
            graph_point(max_event_t + TANGENT_HALF_SPAN, x_at_max + v_max * TANGENT_HALF_SPAN),
            color=VELOCITY,
            stroke_width=4,
        )
        self.play(Create(tangent_line), run_time=BEAT3_TANGENT_TIME)
        self.wait(BEAT3_HOLD_TIME)

        # --- Beat 4: zoom the camera into the tangent point. The axes' own
        # ticks/numbers, the face-to-graph connector line (it runs the full
        # distance from the far-off face_axis to axis_point, so within this
        # zoom it's just a near-horizontal line crossing straight through the
        # same area beat 5's equations need), and the event markers' text
        # labels (their job of identifying which point is which is already
        # done, and at this zoom scale they sit right where beat 5's
        # equations need to go — the dots themselves stay, only the labels
        # dim) are all faded out for the zoomed-in beats. The "v=" readout
        # (already moved near the graph) stays in view. ---
        zoom_center = graph_point(max_event_t, x_at_max)
        self.play(
            self.camera.frame.animate.scale(ZOOM_SCALE).move_to(zoom_center),
            graph_t_axis.ticks.animate.set_opacity(0),
            graph_t_axis.numbers.animate.set_opacity(0),
            graph_x_axis.ticks.animate.set_opacity(0),
            graph_x_axis.numbers.animate.set_opacity(0),
            connector_line.animate.set_opacity(0),
            *[label.animate.set_opacity(0) for label in event_marker_labels],
            run_time=BEAT4_ZOOM_TIME,
        )
        self.wait(BEAT4_HOLD_TIME)

        # --- Beat 5: mark the +-1s window, then show Δt and Δx computed
        # explicitly, before beat 6's division. The bracket lines get their
        # own "Δt"/"Δx" tags right on the diagram, in addition to (not
        # instead of) the full equations shown afterward. ---
        t1, t2 = max_event_t - DELTA_T_HALF, max_event_t + DELTA_T_HALF
        x1, x2 = x_at_max - v_max * DELTA_T_HALF, x_at_max + v_max * DELTA_T_HALF
        delta_t_value = t2 - t1
        delta_x_value = x2 - x1
        p1, p2 = graph_point(t1, x1), graph_point(t2, x2)
        corner = np.array([p2[0], p1[1], 0.0])

        window_marker_1 = Dot(p1, color=FORMULA, radius=0.04)
        window_marker_2 = Dot(p2, color=FORMULA, radius=0.04)
        self.play(FadeIn(window_marker_1, window_marker_2), run_time=BEAT5_MARKER_TIME)

        delta_t_line = Line(p1, corner, color=FORMULA, stroke_width=2)
        delta_x_line = Line(corner, p2, color=FORMULA, stroke_width=2)
        # Above the line, not below: the line sits close to the zoomed
        # frame's bottom edge, and a label below it would be clipped.
        delta_t_label = MathTex("\\Delta t", color=FORMULA, font_size=28).next_to(delta_t_line, UP, buff=0.1)
        delta_x_label = MathTex("\\Delta x", color=FORMULA, font_size=28).next_to(delta_x_line, RIGHT, buff=0.1)
        self.play(
            Create(delta_t_line), Create(delta_x_line),
            FadeIn(delta_t_label, delta_x_label),
            run_time=BEAT5_BRACE_TIME,
        )

        # Left-aligned, not centered: at this zoom level these equations are
        # wide relative to the visible frame, and a centered anchor placed
        # this close to the left edge let them clip past it (measured
        # widths ~2.8-3.1 against a ~5.7-wide visible frame at ZOOM_SCALE).
        equation_anchor = graph_point(max_event_t - 2.6, x_at_max + 1.3)
        delta_t_eq = MathTex(f"\\Delta t = {t2:.2f} - {t1:.2f} = {delta_t_value:.2f}", color=FORMULA, font_size=26)
        delta_t_eq.move_to(equation_anchor, aligned_edge=LEFT)
        self.play(FadeIn(delta_t_eq), run_time=BEAT5_DELTA_T_EQ_TIME)

        delta_x_eq = MathTex(f"\\Delta x = {x2:.2f} - {x1:.2f} = {delta_x_value:.2f}", color=FORMULA, font_size=26)
        delta_x_eq.next_to(delta_t_eq, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(delta_x_eq), run_time=BEAT5_DELTA_X_EQ_TIME)
        self.wait(BEAT5_HOLD_TIME)

        # --- Beat 6: compute Δx / Δt from the two values shown above. The
        # numeric result is its own MathTex part so beat 7 can highlight it
        # specifically, alongside the original "v=" readout.
        #
        # The exact analytic ratio (delta_x_value / delta_t_value) equals
        # v_max to floating-point precision, but rounding it to 2 decimals
        # here (3.45) while v_value displays only 1 decimal (3.4, from
        # DecimalNumber's num_decimal_places=1) makes the two look like they
        # disagree even though they don't. As a stopgap, round this result to
        # the same 1 decimal place as v_value and use "≈" instead of "=", so
        # beat 7's side-by-side comparison always shows matching digits. ---
        slope_value = delta_x_value / delta_t_value
        slope_eq = MathTex(
            f"\\Delta x / \\Delta t = {delta_x_value:.2f}/{delta_t_value:.2f} \\approx ",
            f"{slope_value:.1f}",
            color=FORMULA,
            font_size=26,
        )
        slope_eq.next_to(delta_x_eq, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(slope_eq), run_time=BEAT6_SLOPE_EQ_TIME)
        self.wait(BEAT6_HOLD_TIME)

        # --- Beat 7: zoom back out and emphasize that the slope result and
        # the original "v=" readout are the same number. Beats 5-6's
        # construction (window markers, Δt/Δx brackets and their tags, the
        # Δt/Δx/slope equations) is specific to this derivation and is faded
        # out here; only the final numeric result (slope_eq[1]) survives, to
        # be compared against v_value. The tangent line (beat 3) and the
        # event markers (beat 1) stay, since they're lasting graphical
        # devices, not scratch computation — the event markers' labels are
        # simply restored to full opacity here, same as the axes'. ---
        self.play(
            FadeOut(
                window_marker_1, window_marker_2, delta_t_line, delta_x_line,
                delta_t_label, delta_x_label, delta_t_eq, delta_x_eq, slope_eq[0],
            ),
            self.camera.frame.animate.scale(1.0 / ZOOM_SCALE).move_to(ORIGIN),
            graph_t_axis.ticks.animate.set_opacity(1),
            graph_t_axis.numbers.animate.set_opacity(1),
            graph_x_axis.ticks.animate.set_opacity(1),
            graph_x_axis.numbers.animate.set_opacity(1),
            connector_line.animate.set_opacity(1),
            *[label.animate.set_opacity(1) for label in event_marker_labels],
            run_time=BEAT7_UNZOOM_TIME,
        )
        self.play(
            Indicate(slope_eq[1], color=VELOCITY, scale_factor=1.3),
            Indicate(v_value, color=VELOCITY, scale_factor=1.3),
            run_time=BEAT7_CONFIRM_TIME,
        )
        self.wait(BEAT7_HOLD_TIME)
