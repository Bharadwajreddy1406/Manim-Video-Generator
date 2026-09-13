# Storyboard: Why the Derivative Is Instantaneous Slope

## Core visual thesis

The tangent line is not introduced as a separate construction. It emerges continuously as the limiting position of secant lines while the interval between two points shrinks toward zero.

## Format and pacing

- 16:9 landscape, approximately 75-85 seconds.
- One continuous Manim scene with six visual beats.
- Narration is generated and synchronized through `manim-voiceover` using the approved `script.md`. Beat timings are controlled by the active speech service and must be re-checked if that service or the narration changes.
- Keep the curve and the fixed point visible from Beat 2 through the ending. This continuity is central to the explanation.
- Use the repository's shared visual style if one is defined before implementation. At present, the shared color and typography modules are empty, so no new series-wide palette is established here.

## Visual beats

### Beat 1 - Average speed versus speed right now (0:00-0:12)

**Narration:** "Imagine driving along a winding road... how fast are you moving right now?"

**Visible at the start:** A simple horizontal time interval marked from 0 to 10 seconds, with a start position and an end position above it.

**Change:** A bracket spans the full interval and a simple fraction appears: total distance over 10 seconds, labeled "average speed." The bracket then fades while a single point at the end of the interval is highlighted beside a compact speedometer reading, labeled "speed right now." The phrases "over an interval" and "at one instant" are briefly contrasted. Keep this as a clean conceptual comparison, without animating a road or a moving car.

**What this proves:** Average change uses two moments; an instantaneous rate concerns one moment.

**Transition:** The horizontal time interval becomes the graph's x-axis, and the highlighted instant becomes the fixed point on the curve.

### Beat 2 - A secant measures average slope (0:12-0:28)

**Narration:** "A graph has the same distinction... change in y, divided by change in x."

**Visible at the start:** Clean coordinate axes and a smooth nonlinear curve. The highlighted point, P, sits left of center with enough open space to its right. A second point, Q, appears farther along the curve.

**Change:** A line grows through P and Q and is labeled "secant." Dashed horizontal and vertical guides form a rise/run triangle between the points. The symbolic slope

`Delta y / Delta x`

appears near the triangle, with numerator and denominator highlighted in the same colors as the corresponding guide segments.

**What this proves:** The secant slope is an average rate of change across the visible interval from P to Q.

### Beat 3 - The interval shrinks (0:28-0:48)

**Narration:** "Now keep the first point fixed and slide the second point closer... the tangent line."

**Implementation emphasis:** This is the conceptual and visual centerpiece of the video. It should receive the greatest implementation attention, screen time, and polish. The viewer's understanding depends on clearly seeing one secant line transform continuously into the tangent line.

**Visible at the start:** P remains fixed. Q, the secant, the rise/run triangle, and the slope expression are all visible.

**Central animation:** Q slides smoothly along the curve toward P. Throughout the motion:

- P does not move.
- The horizontal gap and vertical rise shrink continuously.
- The rise/run triangle updates continuously.
- The secant line rotates continuously rather than being replaced by a sequence of disconnected lines.
- A small numeric slope readout changes and settles toward a stable value.

As Q nears P, the "secant" label fades and the line settles into its limiting orientation. The label "tangent" appears only after that orientation has become visually clear. A faint short trail of earlier secant positions may remain briefly, showing convergence without cluttering the graph.

**What this proves:** Examining smaller intervals makes the average slope approach one particular line and one particular slope.

### Beat 4 - Why the points cannot simply coincide (0:48-0:59)

**Narration:** "We cannot simply put the two points in exactly the same place... zero divided by zero."

**Visible at the start:** Q is extremely close to P; the nearly tangent line remains visible.

**Change:** The animation pauses just before Q reaches P. The horizontal and vertical changes are magnified in a small inset so the viewer can still see them. When Q is placed directly on P in the inset, both guide lengths collapse to zero and the fraction changes to `0 / 0`, marked as undefined. Do not remove the nearly settled line from the main graph.

**What this proves:** Instantaneous slope cannot be found by substituting a zero-width interval into the average-slope fraction.

### Beat 5 - The limit defines the derivative (0:59-1:13)

**Narration:** "Instead, the derivative uses a limit... the slope at an instant."

**Visible at the start:** The main graph still shows P and the limiting line. The `0 / 0` inset is present but visually secondary.

**Change:** The inset fades. Beside the graph, build the derivative formula progressively rather than displaying it all at once. Begin with the familiar change in output, `f(x+h) - f(x)`. Place it over the input change, `h`, to reconnect it to the secant slope. Then add `lim_(h -> 0)` to express the shrinking interval. Finally reveal `f'(x) =` as the name of the value approached:

`f'(x) = lim_(h -> 0) [f(x+h) - f(x)] / h`.

The `h -> 0` part is emphasized as Q makes one short replay of its approach toward P. The slope readout settles at the derivative value at the same moment the line is confirmed as the tangent. A compact correspondence appears:

`derivative = instantaneous rate = tangent slope`.

**What this proves:** The derivative is the value approached by secant slopes, provided they settle to a single limit.

### Beat 6 - Final distinction (1:13-1:22)

**Narration:** "So instantaneous slope is not measured across a tiny fixed interval... as the interval vanishes."

**Visible at the start:** The curve, P, tangent line, and limit expression remain.

**Change:** Briefly show a nearby Q and a thin bracket labeled "tiny, but nonzero." Its secant slope appears as an approximation. Then Q glides toward P once more; the bracket tends to zero, the secant merges with the tangent, and the approximation symbol changes to an equals sign in the final statement:

`f'(x) = tangent slope at P`.

End on the curve, fixed point, and tangent line with generous empty space. Remove supporting labels except the final statement.

**What this proves:** A small fixed interval only approximates instantaneous slope; the derivative is defined by the limiting process.

## Continuity and layout notes

- Place the graph slightly left of center from Beat 2 onward, reserving the right side for the slope fraction, limit notation, and final statement.
- Keep P in a consistent accent color. Give Q a distinct color that becomes less prominent as it approaches P. Use a third color for the secant/tangent line so its rotation is easy to track.
- Avoid a full-screen title card. The spoken hook should begin immediately, with the title optionally appearing small and briefly over the opening comparison.
- Keep labels short: P, Q, secant, tangent, average slope, and instantaneous slope.
- The limit equation should be the only dense mathematical expression. Reveal it in meaningful pieces rather than all at once.
- The key thumbnail/poster frame would be the graph during Beat 3: P fixed, Q approaching, several faint secant positions, and the tangent highlighted.

## Voiceover implementation

The scene uses one continuously controlled position for Q so the point, guides, secant, and slope readout remain synchronized. Narration is divided into sentence-level voiceover blocks that map to these beats, and animation runtimes are derived from each voiceover tracker's duration rather than fixed waits.
