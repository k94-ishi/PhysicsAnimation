# storyboard.md

This storyboard was built from the approved flow in `script.md`.

Each scene's **Goal** describes what the viewer should understand by the
end of that scene.

---

# Scene 1: Watch something move, and turn its position into a number

## Goal

Understand that representing motion requires time, not just position.

### Beat 1

**Narration**

"First, let's watch '😁' move back and forth along a straight line. So, how could we express this motion with numbers?"

**Visual**

"😁" moves along a plain straight line, speeding up, slowing down, and reversing.

---

### Beat 2

**Narration**

"To represent its position, let's add ticks to the line like this to make a coordinate axis."

**Visual**

Draw evenly spaced ticks on the line to form a coordinate axis.

Show "😁"'s current position live, as a coordinate value.

---

### Beat 3

**Narration**

"Position alone doesn't really capture motion, does it? Let's make it so we can see where '😁' is together with the time."

**Visual**

Show a timer, and show "😁"'s position changing as time passes.

---

# Scene 2: Build an x-t graph

## Goal

Understand that the real motion and a point on the x-t graph correspond one to one.

### Beat 1

**Narration**

"Now let's set up the axes for an x-t graph. The horizontal axis is t, representing elapsed time; the vertical axis is x, representing position. Let's use this graph to see how we can represent the motion."

**Visual**

Draw the x-t coordinate axes.

Show the axis labels, completing the coordinate system.

---

### Beat 2

**Narration**

"Without worrying about time for now, let's connect '😁''s ever-changing position to the corresponding point on the x axis with a line. You can see the two move in lockstep."

**Visual**

Connect "😁" to the corresponding point on the x-t graph with a guide line, showing that the motion and the graph always correspond.

---

# Scene 3: Plot the x-t graph

## Goal

Understand that the x-t graph gets drawn out over time, and that the same approach works even if the initial position or start time changes.

### Beat 1

**Narration**

"We just said position alone doesn't capture motion. Let's think about plotting the graph over time. First, let's reset the timer to 0 and stop the motion for a moment."

**Visual**

Reset the timer to 0 seconds and stop "😁".

---

### Beat 2

**Narration**

"Now we'll restart the timer and set '😁' moving again. On the graph, as time passes, the point marking the motion moves to the right - so after 3 seconds, a point will land somewhere on this line, and after 6 seconds, somewhere on that line."

**Visual**

Show vertical lines at t=3 and t=6, marking where future points will be plotted.

---

### Beat 3

**Narration**

"Let's start the motion and plot it."

**Visual**

Draw the x-t graph live, in sync with "😁"'s motion.

---

### Beat 4

**Narration**

"Now let's change the initial position and watch again."

**Visual**

Change the initial position and draw a new trace.

---

### Beat 5

**Narration**

"Let's also consider times before zero, so our graph covers the past as well."

**Visual**

Extend the axes to cover t<0, and plot motion starting from t=-2 seconds.

---

# Scene 4: Tangent slope and velocity

## Goal

Understand that the slope of the tangent line on the x-t graph represents the instantaneous velocity.

### Beat 1

**Narration**

"Next, let's focus on speed. We'll add a velocity value to '😁''s motion. Pay attention to the points where the velocity is zero, where it's maximum, and where it's minimum."

**Visual**

"😁" keeps moving with its velocity shown live alongside it.

Highlight the zero/maximum/minimum-velocity points on the x-t graph.

---

### Beat 2

**Narration**

"How did that look? Moving backward corresponds to negative velocity, so note that the point of minimum velocity happens while '😁' is moving backward."

**Visual**

Replay the same motion once more.

---

### Beat 3

**Narration**

"Velocity corresponds to the slope of the tangent line on the graph. For example, at the point of maximum velocity, the tangent's slope is steep."

**Visual**

Show the tangent line at the point of maximum velocity, emphasizing its slope.

---

### Beat 4

**Narration**

"Let's think about how we can actually compute that slope. Let's zoom in on the tangent."

**Visual**

Zoom in on the area around the tangent line.

---

### Beat 5

**Narration**

"Do you remember how to compute a slope? We can do it in two steps.
Step 1: pick an interval, look at the tangent, and find the increase in t and the increase in x."

**Visual**

Illustrate Δt and Δx, revealing in order up through:

Δt = ... - ... = ...

Δx = ... - ... = ...

---

### Beat 6

**Narration**

"Step 2: divide the increase in x by the increase in t. That gives us the slope."

**Visual**

Show the Δx/Δt computation step by step, with intermediate steps.

---

### Beat 7

**Narration**

"It matches the maximum velocity we saw earlier - so we can see that the slope of the tangent on the x-t graph at a point is the velocity at that point."

**Visual**

Return to the normal view, emphasizing that the computed result matches the displayed velocity.

---

# Scene 5: Connecting to the v-t graph

## Goal

Understand that the same motion can be represented on both an x-t graph and a v-t graph, and that the two correspond to each other.

### Beat 1

**Narration**

"Let's look at the same motion again, this time on a velocity-time graph too."

**Visual**

Add a v-t graph below the x-t graph, showing both at once.

---

### Beat 2

**Narration**

"On the position-time graph, we saw 'how much the position changed.'
On the velocity-time graph, we see 'how the speed itself is changing.'"

**Visual**

Update the motion, the x-t graph, and the v-t graph in sync.

Pause at the zero/maximum/minimum-velocity points, and emphasize the correspondence between:

- the tangent on the x-t graph
- the value on the v-t graph

---

### Beat 3

**Narration**

"Let's look at a few different motion patterns."

**Visual**

Compare the following four motions side by side, in the same layout:

- Constant-velocity straight-line motion
- Uniformly accelerated motion, speeding up
- Uniformly accelerated motion, slowing down and reversing
- Simple harmonic motion

Pause for about 1 second between each pattern, to make the differences easy to compare.

---

# Scene 6: Wrap-up

## Goal

Recap that motion can be represented with graphs, and that the x-t and v-t graphs correspond to each other.

### Beat 1

**Narration**

"Do you have a feel for these graphs now?"

**Visual**

Show "😁", the x-t graph, and the v-t graph together, in their final state.

On the right side of the screen, reveal and highlight the following, in order:

✓ Motion can be expressed through position and time

✓ The x-t graph shows how position changes

✓ The slope of the tangent on the x-t graph is the velocity

✓ The v-t graph shows how velocity changes

Finally, connect the tangent on the x-t graph to the corresponding point on the v-t graph with a colored guide line, emphasizing that "the same motion is being shown from two different viewpoints," then fade out.
