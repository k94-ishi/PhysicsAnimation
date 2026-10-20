"""Scene 3: Show the flow of time and changes to the initial position.

Implements storyboard.md > Scene 3, following its five beats:
  1. The object starts at wherever scene02 ended (for a seamless cut), then
     glides smoothly back to x=0 and comes to rest there — an animated
     transition, not a jump. A dashed line already links it to a matching
     point on the graph's x-axis, exactly as in scene02, and stays on screen
     continuously from here through the rest of the scene.
  2. Guide lines at t=3 and t=6 quickly preview where points will land,
     while the object stays at rest at x=0.
  3. Motion resumes from t=0, x=0 together with the timer: the object and
     the same graph point (now sweeping along t too) move together,
     plotting a trajectory until the curve runs off the visible screen.
  4. The starting position changes; a fresh trajectory and timer are drawn
     from t=0, again running until off-screen.
  5. The t-axis extends to show t<0: its existing tick marks/numbers are
     detached first, then the bare line is stretched to its full new length,
     then fresh tick marks/numbers are regenerated for the whole new range —
     so the existing 0-7 portion never visibly rescales mid-transition.
     Motion (and the same timer) continue from t=-2, again until off-screen.

Per the user's review: beat durations are no longer specified in
storyboard.md (each plotting beat now runs until the curve leaves the
visible frame, so a fixed duration wouldn't be meaningful); the layout
(face axis + separate x-t graph, same position/scale) matches scene02's, for
a visually consistent cut between the two scenes.

No narration text is rendered on screen; narration is delivered as separate
voiceover per the project's workflow (see CLAUDE.md > Development Workflow).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import RIGHT, UP, Create, DashedLine, Dot, FadeIn, MathTex, Scene, TracedPath, ValueTracker, linear
from manim.mobject.text.numbers import DecimalNumber

from common.colors import BACKGROUND, FORMULA, PRIMARY
from common.graph_layout import (
    CONNECTOR_LINE_COLOR,
    CONNECTOR_Z_INDEX,
    FACE_AXIS_X,
    FACE_Z_INDEX,
    GRAPH_ORIGIN,
    find_offscreen_time,
    make_t_axis,
    make_vertical_x_axis,
)
from common.motion_profile import MAIN_X0, SCENE2_END_T, position
from common.position_track import make_tracked_face

# Start exactly where scene02 ended, so the cut into this scene shows no jump.
SCENE3_START_X0 = position(SCENE2_END_T, MAIN_X0)

BEAT1_FADE_IN_TIME = 0.5
BEAT1_HOLD_TIME = 1.5
BEAT1_RETURN_TO_ZERO_TIME = 1.5  # smooth glide from SCENE3_START_X0 down to x=0, not a jump

BEAT2_GUIDE_LINE_TIME = 0.5  # x2, for t=3 then t=6
BEAT2_HOLD_TIME = 2.0  # object stays at rest at x=0 while the guide lines sit as reference

BEAT3_TIMER_FADE_TIME = 0.5

BEAT4_FADE_IN_TIME = 0.3
BEAT4_NEW_X0 = 5.0

BEAT5_STRETCH_TIME = 1.2
BEAT5_NEW_TICKS_TIME = 0.8
BEAT5_T_START = -2.0


def _compute_scene3_end_state() -> tuple[float, float]:
    """The exact (t, x) the "😁" is at on this scene's last frame, computed by
    replaying beat 5's own axis-stretch/off-screen-search geometry without
    actually rendering anything. Scene04 imports SCENE3_END_X from here so it
    can open with the "😁" already at this position, for a seamless cut."""
    t_axis = make_t_axis(GRAPH_ORIGIN)
    x_axis = make_vertical_x_axis(GRAPH_ORIGIN)
    new_start_point = t_axis.number_to_point(BEAT5_T_START)
    t_axis.put_start_and_end_on(new_start_point, t_axis.get_end())
    t_axis.x_range = np.array([BEAT5_T_START, 7.0, 1.0])
    x_of_t = lambda t: position(t, BEAT4_NEW_X0)  # noqa: E731
    end_t = find_offscreen_time(BEAT5_T_START, t_axis, x_axis, x_of_t)
    return end_t, x_of_t(end_t)


SCENE3_END_T, SCENE3_END_X = _compute_scene3_end_state()


def make_timer(position_on_screen, get_time_value):
    """A "t = X.X s" readout. get_time_value() is called each frame to fetch
    the value to display, so callers can point it at whatever clock is
    currently active.

    Does NOT attach the live-tracking updaters (returns them instead): a
    DecimalNumber's glyph count can change mid-animation as its value
    changes, which conflicts with FadeIn/Write's own frame interpolation if
    the updater is already attached. Callers should play any entrance
    animation first, then call the two update_* functions once and attach
    them as updaters."""
    timer_label = MathTex("t=", color=FORMULA)
    timer_value = DecimalNumber(get_time_value(), num_decimal_places=1, color=FORMULA)
    timer_unit = MathTex("\\mathrm{s}", color=FORMULA)
    timer_label.move_to(position_on_screen)

    def update_timer_value(mob: DecimalNumber) -> None:
        mob.set_value(get_time_value())
        mob.next_to(timer_label, buff=0.15)

    def update_timer_unit(mob: MathTex) -> None:
        mob.next_to(timer_value, buff=0.1)

    update_timer_value(timer_value)
    update_timer_unit(timer_unit)
    return timer_label, timer_value, timer_unit, update_timer_value, update_timer_unit


def make_plot_group(vertical_x_axis, t_axis, get_t, x_of_t, face):
    """A Dot plotted at (get_t(), x_of_t(get_t())), a dashed line connecting
    it to face (drawn behind face, styled distinctly from the graph's own
    blue curve), and a TracedPath drawing its trajectory as get_t()
    advances."""
    dot = Dot(color=PRIMARY)
    connector_line = DashedLine(color=CONNECTOR_LINE_COLOR)
    connector_line.set_z_index(CONNECTOR_Z_INDEX)

    def update_dot(mob: Dot) -> None:
        t_value = get_t()
        x_value = x_of_t(t_value)
        t_screen_x = t_axis.number_to_point(t_value)[0]
        x_screen_y = vertical_x_axis.number_to_point(x_value)[1]
        mob.move_to([t_screen_x, x_screen_y, 0])

    def update_connector_line(mob: DashedLine) -> None:
        mob.put_start_and_end_on(face.get_center(), dot.get_center())

    # Set the correct initial position before anything watches this dot, so
    # TracedPath never samples its default (uninitialized) construction point.
    update_dot(dot)
    update_connector_line(connector_line)

    dot.add_updater(update_dot)
    connector_line.add_updater(update_connector_line)
    traced_path = TracedPath(dot.get_center, stroke_color=PRIMARY, stroke_width=3)

    return dot, connector_line, traced_path, update_dot, update_connector_line


class Scene03TimeAndInitialPosition(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # Same layout as scene02: the "😁"'s own axis, separate from the graph.
        face_axis = make_vertical_x_axis(np.array([FACE_AXIS_X, GRAPH_ORIGIN[1], 0.0]))
        graph_x_axis = make_vertical_x_axis(GRAPH_ORIGIN)
        graph_t_axis = make_t_axis(GRAPH_ORIGIN)
        x_axis_label = MathTex("x", color=FORMULA).next_to(graph_x_axis.get_end(), UP, buff=0.3)
        t_axis_label = MathTex("t", color=FORMULA).next_to(graph_t_axis.get_end(), RIGHT, buff=0.3)

        t_tracker = ValueTracker(0.0)
        x0_tracker = ValueTracker(SCENE3_START_X0)
        face, update_face = make_tracked_face(face_axis, lambda: position(t_tracker.get_value(), x0_tracker.get_value()))
        face.set_z_index(FACE_Z_INDEX)

        # A point on the graph's x-axis at the same height as the object, and a
        # dashed line linking them - exactly like scene02's, kept on screen
        # continuously (not just during the plotting beats).
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

        # --- Beat 1: start at scene02's ending position, then glide smoothly
        # back to x=0 and come to rest there (no timer yet) ---
        self.play(
            FadeIn(face_axis, graph_x_axis, graph_t_axis, x_axis_label, t_axis_label, face, axis_point, connector_line),
            run_time=BEAT1_FADE_IN_TIME,
        )
        self.wait(BEAT1_HOLD_TIME)
        self.play(x0_tracker.animate.set_value(0.0), run_time=BEAT1_RETURN_TO_ZERO_TIME)

        # --- Beat 2: guide lines quickly preview t=3 and t=6; the object stays
        # at rest at x=0. The lines span the x-axis's full height, including
        # x<0, not just the region above the t-axis. ---
        guide_top_y = graph_x_axis.get_end()[1]
        guide_bottom_y = graph_x_axis.get_start()[1]

        def make_guide_line(t_value: float) -> DashedLine:
            base = graph_t_axis.number_to_point(t_value)
            return DashedLine([base[0], guide_bottom_y, 0], [base[0], guide_top_y, 0], color=PRIMARY, stroke_width=2)

        guide_line_3 = make_guide_line(3)
        guide_line_6 = make_guide_line(6)
        self.play(Create(guide_line_3), run_time=BEAT2_GUIDE_LINE_TIME)
        self.play(Create(guide_line_6), run_time=BEAT2_GUIDE_LINE_TIME)
        self.wait(BEAT2_HOLD_TIME)

        # --- Beat 3: timer and plot both start together from t=0, x=0; runs
        # until the curve leaves the visible screen. axis_point (already
        # linked to face via connector_line) becomes the plotted, moving
        # point instead of a fresh one, so the connector line never disappears. ---
        x_of_t_3 = lambda t: position(t, 0.0)  # noqa: E731

        axis_point.remove_updater(update_axis_point_height_only)

        def update_dot_3(mob: Dot) -> None:
            t_value = t_tracker.get_value()
            x_value = x_of_t_3(t_value)
            t_screen_x = graph_t_axis.number_to_point(t_value)[0]
            x_screen_y = graph_x_axis.number_to_point(x_value)[1]
            mob.move_to([t_screen_x, x_screen_y, 0])

        update_dot_3(axis_point)
        axis_point.add_updater(update_dot_3)
        traced_path = TracedPath(axis_point.get_center, stroke_color=PRIMARY, stroke_width=3)
        self.add(traced_path)

        timer_label_3, timer_value_3, timer_unit_3, update_timer_value_3, update_timer_unit_3 = make_timer(
            [-5.5, -3.0, 0], t_tracker.get_value
        )
        self.play(FadeIn(timer_label_3, timer_value_3, timer_unit_3), run_time=BEAT3_TIMER_FADE_TIME)
        timer_value_3.add_updater(update_timer_value_3)
        timer_unit_3.add_updater(update_timer_unit_3)

        beat3_stop_t = find_offscreen_time(0.0, graph_t_axis, graph_x_axis, x_of_t_3)
        self.play(t_tracker.animate.set_value(beat3_stop_t), run_time=beat3_stop_t, rate_func=linear)

        axis_point.remove_updater(update_dot_3)
        connector_line.remove_updater(update_connector_line)
        face.remove_updater(update_face)
        self.remove(
            axis_point, connector_line, traced_path, guide_line_3, guide_line_6,
            timer_label_3, timer_value_3, timer_unit_3,
            face,
        )

        # --- Beat 4: change the starting position; a fresh timer and trajectory
        # start together from t=0, again running until off-screen ---
        t_tracker = ValueTracker(0.0)
        face, update_face = make_tracked_face(face_axis, lambda: position(t_tracker.get_value(), BEAT4_NEW_X0))
        face.set_z_index(FACE_Z_INDEX)
        x_of_t_4 = lambda t: position(t, BEAT4_NEW_X0)  # noqa: E731

        timer_label_4, timer_value_4, timer_unit_4, update_timer_value_4, update_timer_unit_4 = make_timer(
            [-5.5, -3.0, 0], t_tracker.get_value
        )
        dot, connector_line, traced_path, update_dot, update_connector_line = make_plot_group(
            graph_x_axis, graph_t_axis, t_tracker.get_value, x_of_t_4, face
        )
        self.play(
            FadeIn(face, dot, connector_line, timer_label_4, timer_value_4, timer_unit_4),
            run_time=BEAT4_FADE_IN_TIME,
        )
        timer_value_4.add_updater(update_timer_value_4)
        timer_unit_4.add_updater(update_timer_unit_4)
        self.add(traced_path)
        beat4_stop_t = find_offscreen_time(0.0, graph_t_axis, graph_x_axis, x_of_t_4)
        self.play(t_tracker.animate.set_value(beat4_stop_t), run_time=beat4_stop_t, rate_func=linear)

        # --- Beat 5: extend the t-axis to show t<0 without a mid-transition
        # scale change: detach the existing ticks/numbers, stretch the bare
        # line to its full new length, then regenerate ticks/numbers for the
        # whole new range in one consistent pass. Motion (and the same timer)
        # continue from t=-2, until off-screen. ---
        dot.remove_updater(update_dot)
        connector_line.remove_updater(update_connector_line)
        self.remove(dot, connector_line, traced_path)

        old_ticks, old_numbers = graph_t_axis.ticks, graph_t_axis.numbers
        graph_t_axis.remove(old_ticks, old_numbers)

        new_start_point = graph_t_axis.number_to_point(BEAT5_T_START)
        self.play(
            graph_t_axis.animate.put_start_and_end_on(new_start_point, graph_t_axis.get_end()),
            run_time=BEAT5_STRETCH_TIME,
        )
        # The line itself is now stretched to cover t=-2..7, but number_to_point
        # still assumes the original x_range; update it to match the new extent.
        graph_t_axis.x_range = np.array([BEAT5_T_START, 7.0, 1.0])

        graph_t_axis.add_ticks()
        graph_t_axis.add_numbers()
        # FadeIn(graph_t_axis.ticks, graph_t_axis.numbers) here breaks the
        # parent axis line's own rendering (its stroke silently stops
        # showing, even though stroke_width/opacity/points all still read as
        # correct) - use a plain opacity animate on the children instead,
        # same as the reveal in scene01.
        graph_t_axis.ticks.set_opacity(0)
        graph_t_axis.numbers.set_opacity(0)
        self.play(
            graph_t_axis.ticks.animate.set_opacity(1),
            graph_t_axis.numbers.animate.set_opacity(1),
            run_time=BEAT5_NEW_TICKS_TIME,
        )

        t_tracker.set_value(BEAT5_T_START)
        x_of_t_5 = x_of_t_4  # same starting position as beat4
        dot, connector_line, traced_path, update_dot, update_connector_line = make_plot_group(
            graph_x_axis, graph_t_axis, t_tracker.get_value, x_of_t_5, face
        )
        self.add(traced_path, dot, connector_line)
        # SCENE3_END_T mirrors this same find_offscreen_time call, computed
        # once at module load (see _compute_scene3_end_state above) so
        # scene04 can read the exact ending state without re-deriving it.
        self.play(
            t_tracker.animate.set_value(SCENE3_END_T),
            run_time=SCENE3_END_T - BEAT5_T_START,
            rate_func=linear,
        )

        face.remove_updater(update_face)
        dot.remove_updater(update_dot)
        connector_line.remove_updater(update_connector_line)
