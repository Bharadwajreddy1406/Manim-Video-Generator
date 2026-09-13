# Manim Voiceover Guide

This project uses `manim-voiceover` for narration and animation synchronization.

The purpose of voiceover integration is not merely to attach audio to the final video. Narration timing should actively control animation timing.

## Core Rule

When a video has narration, use `VoiceoverScene` instead of manually guessing timing with arbitrary `self.wait()` values.

Prefer animation timing that follows the narration.

The narration in `script.md` is the source of truth for what is spoken.

The storyboard determines what should happen visually while each narration segment is being spoken.

---

# Basic Setup

Import:

```python
from manim_voiceover import VoiceoverScene
```

Use a speech service, for example:

```python
from manim_voiceover.services.gtts import GTTSService
```

A basic scene should look like:

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class ExampleScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())

        circle = Circle()

        with self.voiceover(
            text="This circle appears while this sentence is being spoken."
        ) as tracker:
            self.play(
                Create(circle),
                run_time=tracker.duration,
            )
```

`VoiceoverScene` can also be combined with compatible Manim scene classes such as `MovingCameraScene` when necessary.

Example:

```python
class ExampleScene(MovingCameraScene, VoiceoverScene): ...
```

Use multiple inheritance only when the additional scene type is genuinely needed.

---

# Voiceover Blocks

Use:

```python
with self.voiceover(text="...") as tracker:
```

to associate a narration segment with the animations that accompany it.

The `tracker` exposes timing information for that narration segment.

The most useful value is:

```python
tracker.duration
```

Example:

```python
with self.voiceover(text="Now the second point moves closer to the first.") as tracker:
    self.play(
        h.animate.set_value(0.1),
        run_time=tracker.duration,
    )
```

Do not automatically force every animation to use the entire `tracker.duration`.

Instead, decide how the visual sequence should occupy the narration segment.

For example:

```python
with self.voiceover(
    text="First the secant appears. Then the second point moves closer."
) as tracker:
    self.play(Create(secant), run_time=0.8)

    self.play(
        h.animate.set_value(0.1),
        run_time=max(0.5, tracker.duration - 0.8),
    )
```

Keep timing readable and intentional.

---

# Narration Segmentation

Do not put an entire 60–90 second script inside one `self.voiceover()` block.

Break narration into meaningful visual beats.

Good:

```python
with self.voiceover(text="Choose two points on the curve."):
    ...

with self.voiceover(text="The line through them is called a secant line."):
    ...

with self.voiceover(
    text="Now keep the first point fixed and move the second point closer."
):
    ...
```

Bad:

```python
with self.voiceover(text=ENTIRE_SCRIPT):
    ...
```

Voiceover blocks should normally correspond to storyboard beats or sub-beats.

A narration segment should be long enough to express one coherent idea but short enough that its visual synchronization remains controllable.

---

# script.md Is the Narration Source

Do not silently invent new narration inside `scene.py`.

The spoken text in `scene.py` should come from the approved `script.md`.

Minor changes such as punctuation for speech synthesis are acceptable when they do not alter meaning.

Substantial wording changes require updating `script.md` first and following the approval rules in `AGENTS.md`.

Avoid allowing these two versions to drift:

```text
script.md
scene.py voiceover text
```

When modifying narration, check both.

---

# Storyboard Synchronization

Each voiceover block should correspond to a meaningful visual action described in `storyboard.md`.

Think in this order:

```text
Narration segment
        ↓
Viewer idea
        ↓
Visual action
        ↓
Voiceover block
        ↓
Animation timing
```

Do not structure the narration around convenient Manim code.

Structure the Manim code around the explanation.

---

# Animation Timing

Narration is the timing authority.

Do not use arbitrary timings like:

```python
self.play(..., run_time=2)
self.wait(3)
```

when narration already determines how long the beat lasts.

Use `tracker.duration` where appropriate.

It is acceptable for multiple animations to occur during one narration block.

Example:

```python
with self.voiceover(
    text="The horizontal change shrinks, and the secant rotates toward the tangent."
) as tracker:
    total = tracker.duration

    self.play(
        h.animate.set_value(0.5),
        run_time=total * 0.65,
    )

    self.play(
        Indicate(tangent),
        run_time=total * 0.25,
    )
```

Avoid relying on exact fractional timing everywhere. Use it only when it improves synchronization.

If animations finish before narration, `manim-voiceover` can wait for the narration to finish. Do not add unnecessary manual waits simply to fill time.

---

# Bookmarks

Use Manim Voiceover bookmarks when an animation needs to occur at a specific word or phrase.

Bookmarks are useful when narration and visual timing need precision beyond whole voiceover blocks.

Example conceptually:

```python
with self.voiceover(
    text="The secant <bookmark mark='move'/>moves toward the tangent."
) as tracker:
    self.wait_until_bookmark("move")
    self.play(...)
```

Use bookmarks sparingly.

Prefer separate voiceover blocks when that produces simpler code.

Use bookmarks when:

* a visual must trigger on a specific spoken word;
* a long sentence contains several precisely timed visual events;
* equation highlighting must align with narration;
* a transformation needs to occur exactly when a term is spoken.

Do not add bookmarks merely because the feature exists.

---

# Speech Services

The speech service should be easy to swap.

During development, prefer a convenient TTS service such as:

```python
GTTSService()
```

Example:

```python
self.set_speech_service(GTTSService())
```

gTTS requires an internet connection. The official Manim Voiceover documentation recommends it as a convenient starting service.

Other supported services include:

* `RecorderService`
* `AzureService`
* `ElevenLabsService`
* `OpenAIService`
* `CoquiService`
* `PyTTSX3Service`

Do not hardcode a production-quality provider throughout the scene.

Keep service selection near the beginning of `construct()` or inside a reusable project helper so it can be replaced later.

---

# Development vs Final Voice

A useful workflow is:

```text
script.md
    ↓
temporary TTS
    ↓
animation development
    ↓
timing refinement
    ↓
final TTS or recorded voice
    ↓
final synchronization pass
```

It is acceptable to develop with gTTS and later switch to another service or recorded narration.

The official Manim Voiceover workflow explicitly supports developing with TTS and later switching to `RecorderService` for a human recording.

When changing speech service, re-render and re-check animation timing because different voices may have different durations.

---

# Subcaptions

The text passed to:

```python
self.voiceover(text="...")
```

can also be used for subcaptions.

If the spoken wording and desired subtitle text differ, use the `subcaption` argument.

Example:

```python
with self.voiceover(
    text="The derivative is the limiting slope.",
    subcaption="Derivative = limiting slope",
):
    ...
```

Do not shorten every subtitle unnecessarily.

Prefer the actual spoken narration unless a shorter subtitle materially improves readability.

---

# Rendering Voiceover Scenes

Render voiceover scenes with caching disabled:

```bash
uv run manim -pql videos/<video>/scene.py <SceneName> --disable_caching
```

The official Manim Voiceover documentation recommends `--disable_caching` for this workflow.

The repository's render utility should include this flag automatically.

During development:

```text
low quality
+ voiceover
+ caching disabled
```

Only use high-quality rendering after the visual and narration synchronization is approved.

---

# Audio Generation

Do not manually generate an unrelated MP3 and then independently guess animation timing when Manim Voiceover is already being used.

Allow the configured speech service to generate the narration used by the scene.

Generated audio and metadata may be cached or stored by the voiceover plugin.

Treat generated TTS audio as build output unless the repository explicitly designates it as a final asset.

Do not move or rename plugin-generated files unless there is a clear project reason.

---

# Mathematical Narration

Mathematical expressions often sound unnatural when raw LaTeX is passed directly to a TTS system.

Do not pass narration like:

```text
f prime of x equals backslash lim underscore...
```

Instead write narration as natural speech:

```text
The derivative of f at x is the limit of the secant slope.
```

while displaying the formal mathematical expression visually with `MathTex`.

Spoken explanation and visual notation do not need to be identical.

Prefer:

```text
voice:
"change in y divided by change in x"

visual:
\frac{\Delta y}{\Delta x}
```

This is usually clearer than forcing the voice synthesizer to read symbolic notation literally.

---

# Numerical Narration

Write numbers and symbols so the speech service pronounces them naturally.

If TTS pronunciation is poor, minimally alter the voiceover text without changing the approved meaning.

For example, spoken text may use:

```text
zero divided by zero
```

while the visual shows:

```latex
\frac{0}{0}
```

Do not compromise visual mathematical notation merely to satisfy TTS pronunciation.

---

# Voiceover and Dynamic Animations

For continuously changing mathematical visuals, synchronize the controlling tracker to the narration.

Example:

```python
h = ValueTracker(2.0)

with self.voiceover(
    text="Now move the second point closer and closer to the first."
) as tracker:
    self.play(
        h.animate.set_value(0.08),
        run_time=tracker.duration,
        rate_func=smooth,
    )
```

All dependent objects should derive from the same underlying value.

For example:

```text
h
↓
Q position
↓
secant line
↓
rise/run guides
↓
slope value
```

Do not separately animate each dependent object if a common `ValueTracker` can keep them synchronized.

---

# Scene Structure

A voiceover scene should remain readable.

Prefer helper methods for meaningful sections when a scene becomes large.

For example:

```python
class DerivativeScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())

        self.introduce_rate_of_change()
        self.show_secant()
        self.approach_tangent()
        self.explain_zero_over_zero()
        self.introduce_limit()
        self.finish()
```

Each helper may contain its own voiceover blocks.

Do not split a scene into methods purely to reduce line count. Split according to conceptual beats.

---

# Failure Handling

When voiceover rendering fails, inspect the actual error before changing scene logic.

Common categories include:

* speech service unavailable;
* internet connectivity failure;
* missing API key;
* unsupported speech-service configuration;
* invalid bookmark markup;
* audio-generation failure;
* Manim render failure unrelated to voiceover.

Do not assume every render failure is caused by Manim itself.

If gTTS or another network service fails, report that separately from animation correctness.

---

# API Keys and Secrets

Never place API keys directly inside `scene.py`.

Use environment variables or `.env` where supported.

Examples include:

```text
OPENAI_API_KEY
ELEVEN_API_KEY
AZURE_SUBSCRIPTION_KEY
AZURE_SERVICE_REGION
```

The official Manim Voiceover documentation recommends environment-based credentials for services that require authentication.

Ensure `.env` is ignored by Git.

Never commit secrets.

---

# Voiceover Workflow for New Videos

For a new narrated video:

1. Approve `script.md`.
2. Approve `storyboard.md`.
3. Implement the scene using `VoiceoverScene`.
4. Divide approved narration into logical voiceover blocks.
5. Associate each block with its storyboard animation.
6. Use the narration duration to guide animation timing.
7. Render at low quality with `--disable_caching`.
8. Watch the complete video with audio.
9. Check:

   * whether visuals happen at the correct spoken moment;
   * whether animations finish too early or too late;
   * whether narration sounds natural;
   * whether important equations remain visible long enough;
   * whether pauses feel intentional;
   * whether transitions occur before the viewer can understand the current visual.
10. Revise timing.
11. Re-render.
12. Perform final high-quality rendering only after synchronization is approved.

---

# Review Checklist

Before considering voiceover integration complete, verify:

* narration matches the approved `script.md`;
* every major narration beat has an intentional visual counterpart;
* there are no long stretches where narration continues but nothing meaningful happens;
* there are no important visual changes occurring before narration introduces them;
* animations are not rushed merely to fit speech;
* speech does not sound unnaturally slow merely to accommodate animation;
* equations remain readable long enough;
* mathematical symbols are spoken naturally;
* voiceover and visuals end cleanly;
* no API credentials are committed;
* the scene renders successfully with `--disable_caching`.

The goal is not simply:

```text
animation + audio
```

The goal is:

```text
narration and animation functioning as one explanation
```
