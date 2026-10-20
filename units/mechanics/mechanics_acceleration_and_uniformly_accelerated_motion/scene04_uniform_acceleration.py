"""Scene 4: What uniformly accelerated motion is.

Implements storyboard.md > Scene 4's four beats:
  1. A purely cinematic full-screen left-to-right "teaser" (no axis, no
     numbers - storyboard's "no axis") of the contrast example (v0=0,
     a=motion.ACCEL_A_CONTRAST, clearly different from scenes 1-3's a=2).
     A bare line then appears along its path and rotates 90° counter-
     clockwise while shrinking into the real (ticked) face_axis used from
     beat 2 on - bridging into this topic's usual vertical-axis convention.
  2-4. The demonstration restarts from t=0 on the real face_axis (this
     teaser was cinematic, not numerically tied to the graphs) and is
     replayed once per beat, each time with one more compressed row
     (x-t, then +v-t, then +a-t) stacked below face_axis - all sized
     up front to fit the full three-row stack without a camera zoom
     (see manim_notes.md > "Progressive multi-row graph stacks"). Beat 4
     ends with a brief real camera zoom onto the a-t row (a genuine change
     of scale, unlike the plain stacking above) to emphasize its flatness
     against the other two rows' slopes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import LEFT, RIGHT, UP, Dot, FadeIn, FadeOut, Line, MathTex, MovingCameraScene, Text, TracedPath, ValueTracker, Write, linear

from common.colors import ACCELERATION, BACKGROUND, FORMULA, PRIMARY, VELOCITY
from common.face import make_face
from common.graph_layout import make_t_axis, make_value_axis
from units.mechanics.mechanics_acceleration_and_uniformly_accelerated_motion import layout, motion

X_RANGE4 = [0, 18, 6]
V_RANGE4 = [0, 12, 4]
A_RANGE4 = [0, 4, 2]
T_MAX = 3.0

TEASER_T_MAX = 2.0
TEASER_START_X = -6.2
TEASER_END_X = 5.8


def teaser_x(t: float) -> float:
    return TEASER_START_X + 3.0 * t**2


TEASER_RUN_TIME = 3.0
ROTATE_RUN_TIME = 1.8
TICKS_REVEAL_TIME = 0.6
INTRO_TIME = 0.4
FADE_TIME = 0.5
DRAW_RUN_TIME = 2.6
HOLD_TIME = 0.8

LABEL_BIG_FONT = 30
LABEL_SMALL_FONT = 22
LABEL_START_POS = np.array([0.0, -1.3, 0.0])  # right below the teaser's motion path (y=0), matching scene01
LABEL_END_POS = np.array([2.6, 3.7, 0.0])
LABEL_SCALE = LABEL_SMALL_FONT / LABEL_BIG_FONT


def position4(t: float) -> float:
    return motion.position_ua(t, a=motion.ACCEL_A_CONTRAST)


def velocity4(t: float) -> float:
    return motion.velocity_ua(t, a=motion.ACCEL_A_CONTRAST)


def accel4(_: float) -> float:
    return motion.ACCEL_A_CONTRAST


class Scene04UniformAcceleration(MovingCameraScene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # --- Beat 1: cinematic teaser, no axis/numbers. A persistent label
        # names this motion; kept until beat 2 needs that screen space
        # (review: don't clear text until it actually gets in the way). ---
        t_tracker = ValueTracker(0.0)
        face = make_face(height=layout.FACE_HEIGHT)
        face.set_z_index(layout.FACE_Z_INDEX)

        label = Text("Motion with constant acceleration = uniformly accelerated motion", color=FORMULA, font_size=LABEL_BIG_FONT)
        label.move_to(LABEL_START_POS)

        def update_face_horizontal(mob) -> None:
            mob.move_to(np.array([teaser_x(t_tracker.get_value()), 0.0, 0.0]))

        update_face_horizontal(face)
        face.add_updater(update_face_horizontal)

        self.play(FadeIn(face), Write(label), run_time=INTRO_TIME)
        self.play(t_tracker.animate.set_value(TEASER_T_MAX), run_time=TEASER_RUN_TIME, rate_func=linear)
        face.remove_updater(update_face_horizontal)

        # --- Rotate the traveled path 90° counterclockwise while shrinking
        # it into the real, ticked face_axis used from beat 2 on; the label
        # migrates to the corner in the same motion, as "😁" moves left
        # (review: same arrangement as scene01's "Accelerating motion"). ---
        source_line = Line(np.array([TEASER_START_X, 0.0, 0.0]), np.array([TEASER_END_X, 0.0, 0.0]), color=FORMULA)
        self.play(FadeIn(source_line), run_time=INTRO_TIME)

        face_axis = make_value_axis(np.array([layout.FACE_AXIS_X, layout.THREE_ROW_TOP_Y, 0.0]), X_RANGE4, layout.THREE_ROW_AXIS_LENGTH)
        face_axis_ticks, face_axis_numbers = face_axis.ticks, face_axis.numbers
        face_axis.remove(face_axis_ticks, face_axis_numbers)

        self.play(
            face.animate.move_to(face_axis.number_to_point(0.0) + RIGHT * layout.FACE_GAP),
            source_line.animate.put_start_and_end_on(face_axis.get_start(), face_axis.get_end()),
            label.animate.scale(LABEL_SCALE).move_to(LABEL_END_POS),
            run_time=ROTATE_RUN_TIME,
        )
        self.remove(source_line)
        self.add(face_axis)
        face_axis.add_ticks()
        face_axis.add_numbers()
        face_axis.ticks.set_opacity(0)
        face_axis.numbers.set_opacity(0)
        self.play(face_axis.ticks.animate.set_opacity(1), face_axis.numbers.animate.set_opacity(1), run_time=TICKS_REVEAL_TIME)

        def update_face_on_axis(mob) -> None:
            mob.move_to(face_axis.number_to_point(position4(t_tracker.get_value())) + RIGHT * layout.FACE_GAP)

        t_tracker.set_value(0.0)
        update_face_on_axis(face)
        face.add_updater(update_face_on_axis)

        # --- Shared graph geometry for beats 2-4. ---
        top_origin = np.array([layout.GRAPH_ORIGIN_X, layout.THREE_ROW_TOP_Y, 0.0])
        mid_origin = np.array([layout.GRAPH_ORIGIN_X, layout.THREE_ROW_MID_Y, 0.0])
        bottom_origin = np.array([layout.GRAPH_ORIGIN_X, layout.THREE_ROW_BOTTOM_Y, 0.0])
        graph_x_axis = make_value_axis(top_origin, X_RANGE4, layout.THREE_ROW_AXIS_LENGTH)
        graph_t_axis = make_t_axis(top_origin, layout.T_RANGE, layout.T_AXIS_LENGTH)
        v_axis = make_value_axis(mid_origin, V_RANGE4, layout.THREE_ROW_AXIS_LENGTH)
        v_t_axis = make_t_axis(mid_origin, layout.T_RANGE, layout.T_AXIS_LENGTH)
        a_axis = make_value_axis(bottom_origin, A_RANGE4, layout.THREE_ROW_AXIS_LENGTH)
        a_t_axis = make_t_axis(bottom_origin, layout.T_RANGE, layout.T_AXIS_LENGTH)
        x_axis_label = MathTex("x", color=PRIMARY, font_size=28).next_to(graph_x_axis.get_end(), UP, buff=0.15)
        t_axis_label = MathTex("t", color=FORMULA, font_size=28).next_to(graph_t_axis.get_end(), RIGHT, buff=0.15)
        v_axis_label = MathTex("v", color=VELOCITY, font_size=28).next_to(v_axis.get_end(), UP, buff=0.15)
        a_axis_label = MathTex("a", color=ACCELERATION, font_size=28).next_to(a_axis.get_end(), UP, buff=0.15)

        def x_point(t: float, x: float) -> np.ndarray:
            return np.array([graph_t_axis.number_to_point(t)[0], graph_x_axis.number_to_point(x)[1], 0.0])

        def v_point(t: float, v: float) -> np.ndarray:
            return np.array([v_t_axis.number_to_point(t)[0], v_axis.number_to_point(v)[1], 0.0])

        def a_point(t: float, a: float) -> np.ndarray:
            return np.array([a_t_axis.number_to_point(t)[0], a_axis.number_to_point(a)[1], 0.0])

        def play_synced_pass(rows, tangent_spec=None) -> None:
            """rows: list of (point_fn, value_fn, color) already-visible
            graphs to draw together, in sync, on this pass. tangent_spec, if
            given, is (point_fn, value_fn, slope_fn, color) for exactly one
            row's live tangent line - review: show the x-t graph's tangent
            only while the v-t graph is being added, and the v-t graph's
            tangent only while the a-t graph is being added (never both,
            never on beat 2's x-t-only pass)."""
            t_tracker.set_value(0.0)
            # Force face's own (persistent) updater to re-run immediately -
            # otherwise face.get_center() below still reflects its position
            # from the *end* of the previous pass for one frame, drawing the
            # face<->row0 connector diagonally until the next render tick
            # (review: the connector line briefly glitches and renders at a
            # diagonal for one frame if this update is skipped).
            face.update()
            dots = [Dot(color=color) for _, _, color in rows]
            # Only "😁"<->x-t (row 0, the same quantity/axis as "😁" itself)
            # is connected - not chained on into v-t/a-t (review: there's no
            # need to force a dotted connection between 😁's motion and the
            # v-t graph).
            connectors = [layout.make_connector()]

            def make_dot_updater(point_fn, value_fn):
                def update(mob) -> None:
                    t = t_tracker.get_value()
                    mob.move_to(point_fn(t, value_fn(t)))
                return update

            dot_updates = [make_dot_updater(point_fn, value_fn) for point_fn, value_fn, _ in rows]
            for dot, update in zip(dots, dot_updates):
                update(dot)

            def make_connector_updater(mob_a, mob_b):
                def update(mob) -> None:
                    mob.put_start_and_end_on(mob_a.get_center(), mob_b.get_center())
                return update

            connector_updates = [make_connector_updater(face, dots[0])]
            for connector, update in zip(connectors, connector_updates):
                update(connector)

            tangent_mobs = []
            update_tangent_line = None
            if tangent_spec is not None:
                t_point_fn, t_value_fn, t_slope_fn, t_color = tangent_spec
                tangent_line = layout.make_tangent_line(t_point_fn, 0.0, t_value_fn(0.0), t_slope_fn(0.0), 0.2, t_color)

                def update_tangent_line(mob) -> None:
                    t = t_tracker.get_value()
                    mob.become(layout.make_tangent_line(t_point_fn, t, t_value_fn(t), t_slope_fn(t), 0.2, t_color))

                tangent_mobs = [tangent_line]

            self.play(FadeIn(*dots, *connectors, *tangent_mobs), run_time=INTRO_TIME)
            for dot, update in zip(dots, dot_updates):
                dot.add_updater(update)
            for connector, update in zip(connectors, connector_updates):
                connector.add_updater(update)
            if tangent_mobs:
                tangent_mobs[0].add_updater(update_tangent_line)

            traced_paths = [TracedPath(dot.get_center, stroke_color=color, stroke_width=3) for dot, (_, _, color) in zip(dots, rows)]
            self.add(*traced_paths)

            self.play(t_tracker.animate.set_value(T_MAX), run_time=DRAW_RUN_TIME, rate_func=linear)
            self.wait(HOLD_TIME)

            for path in traced_paths:
                path.clear_updaters()
            for dot, update in zip(dots, dot_updates):
                dot.remove_updater(update)
            for connector, update in zip(connectors, connector_updates):
                connector.remove_updater(update)
            if tangent_mobs:
                tangent_mobs[0].remove_updater(update_tangent_line)
            self.play(FadeOut(*dots, *connectors, *tangent_mobs), run_time=FADE_TIME)

            # Freeze each settled TracedPath into a plain VMobject - a
            # TracedPath left in the scene does not reliably get covered by
            # the zoom section's make_text_bg captions later (manim_notes.md).
            frozen_paths = [layout.freeze_traced_path(p) for p in traced_paths]
            self.remove(*traced_paths)
            self.add(*frozen_paths)

        # --- Beat 2: x-t graph joins face_axis; the intro label is no
        # longer needed once the graph rows start claiming its space. No
        # tangent yet (review: only show it once the v-t graph is added). ---
        x_title = layout.make_graph_title("x-t graph", x_axis_label, color=PRIMARY)
        self.play(FadeOut(label), FadeIn(graph_x_axis, graph_t_axis), Write(x_axis_label), Write(t_axis_label), Write(x_title), run_time=INTRO_TIME)
        play_synced_pass([(x_point, position4, PRIMARY)])

        # --- Beat 3: v-t graph joins; x-t's tangent is shown this pass only. ---
        v_title = layout.make_graph_title("v-t graph", v_axis_label, color=VELOCITY)
        self.play(FadeIn(v_axis, v_t_axis), Write(v_axis_label), Write(v_title), run_time=INTRO_TIME)
        play_synced_pass(
            [(x_point, position4, PRIMARY), (v_point, velocity4, VELOCITY)],
            tangent_spec=(x_point, position4, velocity4, VELOCITY),
        )

        # --- Beat 4: a-t graph joins; v-t's tangent is shown this pass
        # (echoing that its slope - the acceleration - never changes),
        # then zoom to emphasize the a-t graph's flatness. ---
        a_title = layout.make_graph_title("a-t graph", a_axis_label, color=ACCELERATION)
        self.play(FadeIn(a_axis, a_t_axis), Write(a_axis_label), Write(a_title), run_time=INTRO_TIME)
        play_synced_pass(
            [(x_point, position4, PRIMARY), (v_point, velocity4, VELOCITY), (a_point, accel4, ACCELERATION)],
            tangent_spec=(v_point, velocity4, accel4, ACCELERATION),
        )

        v_a_center = (v_point(T_MAX / 2, velocity4(T_MAX / 2)) + a_point(T_MAX / 2, accel4(T_MAX / 2))) / 2
        self.play(self.camera.frame.animate.scale(0.55).move_to(v_a_center), run_time=1.3)

        # "Acceleration is constant" -> "-> the v-t graph is a straight
        # line" -> "-> the a-t graph is a horizontal line", one at a time,
        # left edges aligned, centered on screen, each with an opaque
        # background so it stays legible over the graphs.
        zoom_texts = [
            Text("Acceleration is constant", color=ACCELERATION, font_size=20),
            Text("-> the v-t graph is a straight line", color=VELOCITY, font_size=20),
            Text("-> the a-t graph is a horizontal line", color=ACCELERATION, font_size=20),
        ]
        zoom_texts[0].move_to(v_a_center + np.array([0.0, 1.6, 0.0]))
        for prev, text in zip(zoom_texts, zoom_texts[1:]):
            text.next_to(prev, np.array([0.0, -1.0, 0.0]), buff=0.2)
            text.align_to(prev, LEFT)
        for text in zoom_texts:
            bg = layout.make_text_bg(text)
            self.add(bg)
            self.play(Write(text), run_time=0.6)
            self.wait(HOLD_TIME * 1.3)

        self.wait(HOLD_TIME)
        self.play(self.camera.frame.animate.scale(1 / 0.55).move_to(np.array([0.0, 0.0, 0.0])), run_time=1.0)

        self.play(FadeOut(*self.mobjects), run_time=1.0)
