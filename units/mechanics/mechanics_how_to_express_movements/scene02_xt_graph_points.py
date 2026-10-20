"""Scene 2: Build an x-t graph, and represent position as a point.

Implements storyboard.md > Scene 2, following its two beats:
  1. The "😁"'s own track rotates into a vertical position indicator; a
     separate x-t graph (its own x-axis and t-axis) appears beside it (5s).
  2. Connect the object's live position to a point on the graph's x-axis
     with a line; the point tracks height only, matching "ignoring time" —
     no curve is plotted against t yet (that's scene03's job) (4s).

(The beat that marked the object's position as a lone point on the x-axis,
independent of the connecting line, was cut — see outline.md/script.md/
storyboard.md and skills/physics-video-review/SKILL.md.)

Continuity with scene01: this scene rebuilds the exact same position track
(common.position_track's shared constants) and starts its own clock at
common.motion_profile.SCENE1_END_T, so the "😁"'s position and velocity carry
over across the cut with no jump. The "😁"'s own track and the graph's x-axis
are kept as two separate, side-by-side number lines (same scale, same
height) rather than one merged line, so the object's motion is never
obscured by the graph. The "😁" keeps moving continuously throughout,
including while the graph is being built, via the self-advancing t_tracker
(see common.position_track).

No narration text is rendered on screen; narration is delivered as separate
voiceover per the project's workflow (see CLAUDE.md > Development Workflow).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from manim import RIGHT, UP, Create, DashedLine, Dot, FadeIn, MathTex, Scene, Transform, Write

from common.colors import BACKGROUND, FORMULA, PRIMARY
from common.graph_layout import (
    CONNECTOR_LINE_COLOR,
    CONNECTOR_Z_INDEX,
    FACE_AXIS_X,
    FACE_Z_INDEX,
    GRAPH_ORIGIN,
    make_t_axis,
    make_vertical_x_axis,
)
from common.motion_profile import MAIN_X0, SCENE1_END_T, position
from common.position_track import make_autonomous_time_tracker, make_position_track, make_tracked_face

BEAT1_ROTATE_TIME = 2.0
BEAT1_GRAPH_FADE_TIME = 1.5
BEAT1_LABELS_TIME = 1.5

BEAT2_CONNECT_INTRO_TIME = 0.5
BEAT2_HOLD_TIME = 3.5


class Scene02XtGraphPoints(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        # Continue exactly where scene01 left off: same track, same clock value.
        number_line = make_position_track()
        t_tracker = make_autonomous_time_tracker(start=SCENE1_END_T)
        face, update_face = make_tracked_face(number_line, lambda: position(t_tracker.get_value(), MAIN_X0))
        face.set_z_index(FACE_Z_INDEX)
        self.add(number_line, t_tracker, face)

        # --- Beat 1: rotate the "😁"'s track into its own position indicator,
        # and build a separate x-t graph beside it (5s). The object keeps moving. ---
        face_axis_target = make_vertical_x_axis(np.array([FACE_AXIS_X, GRAPH_ORIGIN[1], 0.0]))
        self.play(Transform(number_line, face_axis_target), run_time=BEAT1_ROTATE_TIME)

        graph_x_axis = make_vertical_x_axis(GRAPH_ORIGIN)
        graph_t_axis = make_t_axis(GRAPH_ORIGIN)
        self.play(FadeIn(graph_x_axis, graph_t_axis), run_time=BEAT1_GRAPH_FADE_TIME)

        x_axis_label = MathTex("x", color=FORMULA).next_to(graph_x_axis.get_end(), UP, buff=0.3)
        t_axis_label = MathTex("t", color=FORMULA).next_to(graph_t_axis.get_end(), RIGHT, buff=0.3)
        self.play(Write(x_axis_label), Write(t_axis_label), run_time=BEAT1_LABELS_TIME)

        # --- Beat 2: connect the "😁" to a point on the graph's x-axis at the same
        # height; the point tracks height only, ignoring elapsed time (4s) ---
        axis_point = Dot(color=PRIMARY)
        connector_line = DashedLine(color=CONNECTOR_LINE_COLOR)
        connector_line.set_z_index(CONNECTOR_Z_INDEX)

        def update_axis_point(mob: Dot) -> None:
            mob.move_to(graph_x_axis.number_to_point(position(t_tracker.get_value(), MAIN_X0)))

        def update_connector_line(mob: DashedLine) -> None:
            mob.put_start_and_end_on(face.get_center(), axis_point.get_center())

        update_axis_point(axis_point)
        update_connector_line(connector_line)
        axis_point.add_updater(update_axis_point)
        connector_line.add_updater(update_connector_line)

        self.play(Create(axis_point), Create(connector_line), run_time=BEAT2_CONNECT_INTRO_TIME)
        self.wait(BEAT2_HOLD_TIME)

        face.remove_updater(update_face)
        axis_point.remove_updater(update_axis_point)
        connector_line.remove_updater(update_connector_line)
