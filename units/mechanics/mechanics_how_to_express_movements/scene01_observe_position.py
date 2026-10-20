"""Scene 1: Watch something move, and turn its position into a number.

Implements storyboard.md > Scene 1, strictly following its three beats:
  1. Observe the "😁" moving back and forth along a plain track (6s).
  2. Add evenly spaced tick marks, position numbers, and a live x-value
     label above the object (4s).
  3. Add a timer that keeps counting as the object keeps moving (6s).

The "😁"'s motion runs on one continuous, self-advancing clock for the whole
scene: no beat pauses or resets it. This keeps the motion unbroken within the
scene, and scene02 starts its own clock at common.motion_profile.SCENE1_END_T
(this scene's total duration) so the cut between the two scenes shows no
jump in position or velocity.

No narration text is rendered on screen; narration is delivered as separate
voiceover per the project's workflow (see CLAUDE.md > Development Workflow).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from manim import UP, Create, MathTex, Scene, VGroup
from manim.mobject.text.numbers import DecimalNumber

from common.colors import BACKGROUND, FORMULA
from common.motion_profile import MAIN_X0, position
from common.position_track import make_autonomous_time_tracker, make_position_track, make_tracked_face

X_LABEL_GAP = 0.2  # distance from the face's top to the x-value label

BEAT1_LINE_DRAW_TIME = 0.5
BEAT1_OBSERVE_TIME = 5.5

BEAT2_TICKS_TIME = 2.5
BEAT2_NUMBERS_TIME = 1.0
BEAT2_X_LABEL_TIME = 0.5

BEAT3_TIMER_INTRO_TIME = 1.0
BEAT3_TAIL_TIME = 5.0

SCENE_DURATION = (
    BEAT1_LINE_DRAW_TIME
    + BEAT1_OBSERVE_TIME
    + BEAT2_TICKS_TIME
    + BEAT2_NUMBERS_TIME
    + BEAT2_X_LABEL_TIME
    + BEAT3_TIMER_INTRO_TIME
    + BEAT3_TAIL_TIME
)  # must match common.motion_profile.SCENE1_END_T


class Scene01ObservePosition(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND

        number_line = make_position_track()
        number_line.ticks.set_opacity(0)
        number_line.numbers.set_opacity(0)

        # --- Beat 1: observe the raw motion on a plain track (6s) ---
        self.play(Create(number_line), run_time=BEAT1_LINE_DRAW_TIME)

        t_tracker = make_autonomous_time_tracker(start=0.0)
        face, update_face = make_tracked_face(number_line, lambda: position(t_tracker.get_value(), MAIN_X0))
        self.add(t_tracker, face)
        self.wait(BEAT1_OBSERVE_TIME)

        # --- Beat 2: turn the track into a coordinate by adding ticks and numbers,
        # then show the object's x-value tracking live above it (4s) ---
        self.play(number_line.ticks.animate.set_opacity(1), run_time=BEAT2_TICKS_TIME)
        self.play(number_line.numbers.animate.set_opacity(1), run_time=BEAT2_NUMBERS_TIME)

        x_label = MathTex("x=", color=FORMULA)
        x_value = DecimalNumber(position(t_tracker.get_value(), MAIN_X0), num_decimal_places=1, color=FORMULA)
        x_group = VGroup(x_label, x_value)

        def update_x_group(group: VGroup) -> None:
            label, value = group
            value.set_value(position(t_tracker.get_value(), MAIN_X0))
            value.next_to(label, buff=0.15)
            group.next_to(face, UP, buff=X_LABEL_GAP)

        # Appear instantly, already tracking the face's live position, rather
        # than fading in: any entrance animation here (FadeIn with the updater
        # deferred, or even a manual opacity ramp) leaves a brief window where
        # the label's position/value doesn't match the moving face, which
        # reads as a visible glitch. Popping in already-correct avoids that
        # window entirely.
        update_x_group(x_group)
        x_group.add_updater(update_x_group)
        self.add(x_group)
        self.wait(BEAT2_X_LABEL_TIME)

        # --- Beat 3: add a timer that keeps counting as the motion continues (6s) ---
        timer_label = MathTex("t=", color=FORMULA)
        timer_value = DecimalNumber(t_tracker.get_value(), num_decimal_places=1, color=FORMULA)
        timer_unit = MathTex("\\mathrm{s}", color=FORMULA)
        # Position the three-part timer as one row, left of center, below the number line.
        timer_label.move_to([-1.2, -1.8, 0])

        def update_timer_value(mob: DecimalNumber) -> None:
            mob.set_value(t_tracker.get_value())
            mob.next_to(timer_label, buff=0.15)

        def update_timer_unit(mob: MathTex) -> None:
            mob.next_to(timer_value, buff=0.1)

        update_timer_value(timer_value)
        update_timer_unit(timer_unit)
        timer_value.add_updater(update_timer_value)
        timer_unit.add_updater(update_timer_unit)
        self.add(timer_label, timer_value, timer_unit)
        self.wait(BEAT3_TIMER_INTRO_TIME)
        self.wait(BEAT3_TAIL_TIME)
