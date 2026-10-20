"""Physics functions for this topic (acceleration and uniformly accelerated
motion), shared across scene01-07.

Running example used by scenes 1-3 and 6: a uniformly accelerated motion
with ACCEL_A = 2.0 m/s^2 and v0 = 0 (so x(t) = t^2, v(t) = 2t - the same
numbers storyboard.md itself gives: t=0,1,2,3 -> v=0,2,4,6).

Scene 4 contrasts this with ACCEL_A_CONTRAST = 4.0 m/s^2, a clearly
different value (per docs/physics_teaching_principles.md's "a clearly
distinct value, not a marginal one" rule), also carried into scene 5's
v0=0 staircase demo.

Scene 5 (v0 != 0 beat) and scene 6 (trapezoid-area derivation) use V0, a
nonzero initial velocity paired with the same ACCEL_A so the numbers stay
consistent: v(t) = V0 + ACCEL_A*t, and over t in [0, V0_DEMO_T] the
trapezoid-area check v0*t + (1/2)*a*t^2 == (v0+v)/2*t holds with clean
numbers (v0=1, a=2, t=2 -> v=5, x=6).

Free fall was scoped out in concept_map.md's review (a candidate for the
next topic).
"""

ACCEL_A = 2.0  # m/s^2, main running example (scenes 1-3, 6)
ACCEL_A_CONTRAST = 4.0  # m/s^2, scene4's clearly-different contrast value
V0 = 1.0  # m/s, nonzero initial velocity for scene5's v0!=0 beat and scene6
V0_DEMO_T = 2.0  # s, the demo window used with V0 above (v: 1->5, x=6)


def velocity_ua(t: float, v0: float = 0.0, a: float = ACCEL_A) -> float:
    """v(t) = v0 + a*t, for the uniformly accelerated running example."""
    return v0 + a * t


def position_ua(t: float, x0: float = 0.0, v0: float = 0.0, a: float = ACCEL_A) -> float:
    """x(t) = x0 + v0*t + (1/2)*a*t^2, for the uniformly accelerated running example."""
    return x0 + v0 * t + 0.5 * a * t**2
