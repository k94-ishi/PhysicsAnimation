"""Position and velocity functions shared by every scene in
mechanics_how_to_express_movements.

Using one analytic motion for the recurring "😁" demonstration keeps the
x-t graph, the v-t graph, and the tangent-line calculation consistent with
each other across scenes, per storyboard.md.
"""

import numpy as np

# x(t) = AMPLITUDE * sin(ANGULAR_FREQUENCY * t) + DRIFT_VELOCITY * t + x0
# Oscillation gives the back-and-forth motion; the linear drift term gives
# the net rightward motion described in storyboard.md scene 1.
OSCILLATION_AMPLITUDE = 2.5
ANGULAR_FREQUENCY = 1.3
DRIFT_VELOCITY = 0.2

# NOT part of the main position()/velocity() used by scenes 1-3 (adding it
# there stretched the "😁"'s reachable range far beyond what those scenes'
# axes need). Reserved for the v-t graph scene (scene05), which will add
# this on top of position()/velocity() for its own, separate demonstration
# of a non-constant acceleration.
QUADRATIC_COEFFICIENT = 1.0 / 50.0

# Domain used across the lesson: scenes 1-2 animate t in [T_MIN_DEFAULT, T_MAX],
# scene 3 extends the plotted range back to T_MIN to show t < 0.
T_MIN_DEFAULT = 0.0
T_MIN_EXTENDED = -2.0
T_MAX = 8.0

# Model-time value at which scene01's continuous motion ends. scene02 starts
# its own clock here so the "😁"'s position and velocity carry over across the
# cut with no jump (see scene01_observe_position.py's SCENE_DURATION).
SCENE1_END_T = 16.0

# Model-time value at which scene02's continuous motion ends (SCENE1_END_T +
# scene02's own total duration: 2.0 + 1.5 + 1.5 + 0.5 + 3.5 = 9.0), used by
# scene03 to start at the same x-value scene02 ended on.
SCENE2_END_T = SCENE1_END_T + 9.0

# Shared starting-position offset for scene01/scene02's "😁": shifts the whole
# x(t) curve right so it starts a bit off the track's left edge.
MAIN_X0 = 3.0


def position(t: float | np.ndarray, x0: float = 0.0) -> float | np.ndarray:
    """Position x(t) of the demonstration object, in scene units."""
    return OSCILLATION_AMPLITUDE * np.sin(ANGULAR_FREQUENCY * t) + DRIFT_VELOCITY * t + x0


def velocity(t: float | np.ndarray) -> float | np.ndarray:
    """Velocity v(t) = dx/dt. Independent of x0, since x0 only shifts position."""
    return (
        OSCILLATION_AMPLITUDE * ANGULAR_FREQUENCY * np.cos(ANGULAR_FREQUENCY * t)
        + DRIFT_VELOCITY
    )


def position_v5(t: float | np.ndarray, x0: float = 0.0) -> float | np.ndarray:
    """position() plus QUADRATIC_COEFFICIENT * t**2: the v-t graph scenes'
    own motion (scene05's main demo, scene06's summary), showing a
    non-constant acceleration. Not used by scenes 1-4's shared position()."""
    return position(t, x0) + QUADRATIC_COEFFICIENT * t**2


def velocity_v5(t: float | np.ndarray) -> float | np.ndarray:
    """velocity() plus the derivative of QUADRATIC_COEFFICIENT * t**2; see position_v5."""
    return velocity(t) + 2 * QUADRATIC_COEFFICIENT * t


def find_zero_velocity_times(
    t_min: float, t_max: float, num_samples: int = 2000, velocity_fn=None
) -> list[float]:
    """Times in [t_min, t_max] where velocity_fn (defaults to this module's
    own velocity()) crosses zero, found by sampling and bisection so the
    result stays correct even if the underlying motion changes."""
    velocity_fn = velocity_fn if velocity_fn is not None else velocity
    samples = np.linspace(t_min, t_max, num_samples)
    values = velocity_fn(samples)
    crossing_times = []
    for i in range(len(samples) - 1):
        if values[i] == 0.0:
            crossing_times.append(float(samples[i]))
        elif values[i] * values[i + 1] < 0.0:
            crossing_times.append(_bisect_velocity_zero(samples[i], samples[i + 1], velocity_fn))
    return crossing_times


def find_extreme_velocity_time(
    t_min: float, t_max: float, find_max: bool, num_samples: int = 2000, velocity_fn=None
) -> float:
    """Time in [t_min, t_max] where velocity_fn (defaults to this module's
    own velocity()) is largest (find_max=True) or smallest (find_max=False),
    found by dense sampling."""
    velocity_fn = velocity_fn if velocity_fn is not None else velocity
    samples = np.linspace(t_min, t_max, num_samples)
    values = velocity_fn(samples)
    index = int(np.argmax(values) if find_max else np.argmin(values))
    return float(samples[index])


def find_key_velocity_events(
    t_min: float, t_max: float, velocity_fn=None, num_samples: int = 2000
) -> list[tuple[float, str]]:
    """(t, kind) pairs sorted by t for every zero-velocity crossing and every
    interior local max/min of velocity_fn (defaults to this module's own
    velocity()) in [t_min, t_max]. A segment touching the domain edge is
    skipped when looking for an extremum: velocity_fn there is monotonic in
    from the boundary, so its max/min over that segment is just the boundary
    value, not a real peak of the motion."""
    velocity_fn = velocity_fn if velocity_fn is not None else velocity
    zeros = find_zero_velocity_times(t_min, t_max, num_samples, velocity_fn)
    events = [(t, "zero") for t in zeros]
    boundaries = [t_min, *zeros, t_max]
    for seg_start, seg_end in zip(boundaries, boundaries[1:]):
        if seg_start == t_min or seg_end == t_max:
            continue
        find_max = velocity_fn((seg_start + seg_end) / 2) > 0
        t_extreme = find_extreme_velocity_time(seg_start, seg_end, find_max, num_samples, velocity_fn)
        events.append((t_extreme, "max" if find_max else "min"))
    events.sort(key=lambda event: event[0])
    return events


def _bisect_velocity_zero(t_low: float, t_high: float, velocity_fn=None, tolerance: float = 1e-6) -> float:
    velocity_fn = velocity_fn if velocity_fn is not None else velocity
    while t_high - t_low > tolerance:
        t_mid = (t_low + t_high) / 2.0
        if velocity_fn(t_low) * velocity_fn(t_mid) <= 0.0:
            t_high = t_mid
        else:
            t_low = t_mid
    return (t_low + t_high) / 2.0
