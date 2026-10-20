"""The horizontal position number line and the moving "😁" that tracks a
point on it, shared by every scene after scene01 introduces them
(see storyboard.md, all scenes)."""

import numpy as np
from manim import RIGHT, ValueTracker
from manim.mobject.graphing.number_line import NumberLine
from manim.mobject.svg.svg_mobject import SVGMobject

from common.colors import FORMULA
from common.face import make_face

# Shared by scene01 and scene02's opening: scene02 rebuilds this exact same
# track (same range, length, and height) so the cut between the two scenes
# shows no jump in the "😁"'s screen position.
TRACK_X_MIN = -1
TRACK_X_MAX = 11
TRACK_X_STEP = 1
TRACK_LENGTH = 13
TRACK_Y = 0.0

FACE_HEIGHT = 0.6
FACE_GAP = 0.4  # distance from the track to the face's center, kept perpendicular to it


def make_position_track(y: float = TRACK_Y, x_min: float = TRACK_X_MIN, x_max: float = TRACK_X_MAX, x_step: float = TRACK_X_STEP) -> NumberLine:
    """A fully visible horizontal NumberLine representing position x, at height y."""
    track = NumberLine(
        x_range=[x_min, x_max, x_step],
        length=TRACK_LENGTH,
        color=FORMULA,
        include_ticks=True,
        include_numbers=True,
    )
    track.move_to([0, y, 0])
    return track


def make_autonomous_time_tracker(start: float = 0.0, speed: float = 1.0) -> ValueTracker:
    """A ValueTracker that advances itself by `speed` model-seconds per real
    second, so the object it drives keeps moving through every self.play/
    self.wait call without needing an explicit t_tracker.animate call.
    Must be added to the scene (self.add(...)) for its updater to run."""
    tracker = ValueTracker(start)
    tracker.add_updater(lambda mob, dt: mob.increment_value(dt * speed))
    return tracker


def make_tracked_face(track: NumberLine, get_x) -> SVGMobject:
    """A face mobject that follows get_x() along track, offset perpendicular
    to the track's current direction (and away from its number labels) so
    the offset stays correct even while track is being rotated, e.g. in
    scene02. get_x is a zero-arg callable returning the current position
    value; pass e.g. `lambda: position(t_tracker.get_value(), x0)`, or
    something reading a dynamic x0 (a ValueTracker) for a smooth transition
    between starting positions. Caller is responsible for calling
    face.remove_updater(...) with the returned updater function once the
    motion is done."""
    face = make_face(height=FACE_HEIGHT)

    def update_face(mob):
        point = track.number_to_point(get_x())
        direction = track.get_end() - track.get_start()
        norm = np.linalg.norm(direction)
        direction = direction / norm if norm > 0 else RIGHT
        perpendicular = np.array([-direction[1], direction[0], 0.0])

        numbers_center = track.numbers.get_center()
        toward_numbers = (point + perpendicular * FACE_GAP - numbers_center)
        away_from_numbers = (point - perpendicular * FACE_GAP - numbers_center)
        sign = -1.0 if np.linalg.norm(toward_numbers) < np.linalg.norm(away_from_numbers) else 1.0

        mob.move_to(point + perpendicular * FACE_GAP * sign)

    update_face(face)  # correct position before anything watches this face
    face.add_updater(update_face)
    return face, update_face
