# Manim Storyboarding Conventions

Read this before drafting Stage 2 (the Storyboard). It translates narrative intent into the
vocabulary a Manim code-writing step expects, so the storyboard can be handed off with nothing
left ambiguous.

## Animation family → when to use it

Don't pick animation names decoratively — pick them for what they communicate to a viewer:

- **`Write`** — for text and equations that should feel like they're being handwritten/typed into
  existence. Use for anything the viewer should read carefully (a formula, a key label).
- **`Create` / `DrawBorderThenFill`** — for shapes, graphs, diagrams that should feel *constructed*
  rather than read. Use when the object itself (not its label) is the point.
- **`FadeIn` / `FadeOut`** — for things entering/leaving the scene that aren't the current focus
  (background context, a previous step being dismissed). Low narrative weight — use for
  housekeeping, not for the "aha" moment.
- **`Transform` / `ReplacementTransform`** — for showing that object A *becomes* object B (an
  equation simplifying, a shape morphing into another). This is the single most important
  animation for "math feels alive" moments — if a beat's whole point is "this turns into that,"
  it must be a Transform, not a cut.
- **`Indicate` / `Circumscribe` / `Wiggle`** — for drawing the eye to something already on screen
  without changing it (emphasis, not introduction). Use sparingly, at the exact moment the
  voiceover names the thing.
- **Camera moves (`MovingCameraScene`, `self.camera.frame.animate...`)** — for zooming into
  detail or pulling back to show the bigger picture. Use when the storyboard's intent is "focus
  narrows" or "reveal the whole picture," not as a substitute for a cut.

When drafting a beat, name the *intent* first ("morph the array into a sliding window") and let
that dictate the animation family — don't reach for `Transform` out of habit if the beat is
actually introducing something brand new (that's `Create`/`Write`).

## Cuts vs. transitions vs. continuations

A storyboard beat should mark one of three things at its boundary:

- **Hard cut** — new Manim `Scene` (or clear section break within one). Warranted when the topic,
  visual setup, or camera framing changes completely (e.g. moving from "problem statement" to
  "algorithm walkthrough"). Hard cuts are cheap narratively but every one costs a moment of
  re-orientation for the viewer — don't use them just to avoid animating a transition.
- **Soft transition** — an animated bridge (`Transform`, camera move, `FadeOut`+`FadeIn` cross-
  fade) between beats that are conceptually continuous. Use when beat N's ending state should
  visually lead into beat N+1's opening state.
- **Continuation** — no boundary at all; beat N+1 is just "more of the same shot," e.g. stepping
  through iterations of a loop on the same diagram. Mark these explicitly so the code-writer
  knows not to reset the scene.

Mark every beat's boundary type in the storyboard — this is one of the most common places a
downstream coding agent has to guess if it's left out.

## Voiceover / caption sync

If voiceover is on, each beat's voiceover text should be short enough to read naturally in the
beat's timecode window (roughly 2.5–3 words/second for a calm explainer pace). For beats with a
visual payoff (a Transform landing, an Indicate), name in the storyboard *which word* the visual
should land on — e.g. "the highlight lands on 'left pointer' at the word itself, not before or
after." This is what lets the code-writer wire up `Wait`/animation `run_time` correctly, whether
that's via a TTS-timing library or manually tuned waits.

If voiceover is off, the equivalent is on-screen captions or labels — specify their exact text and
which beat-second they appear/disappear on.

Never leave a beat's voiceover line as a paraphrase or "something like..." — write the exact
words. The coding step will use this text verbatim (for TTS or captions), so vagueness here
becomes a real gap, not just a style note.

## Pacing by format

- **Vertical / short-form (Reels, Shorts, TikTok)**: beats are short (2–6s), cuts are more
  frequent and forgiven, text must be large and centered (viewers are often on mute — captions
  matter more than voiceover polish), and the hook beat is non-negotiable — if the first 2-3
  seconds don't earn the watch, the rest doesn't matter.
- **Horizontal / long-form (YouTube)**: beats can run longer (5–20s), soft transitions and camera
  moves read better than constant hard cuts, and there's room for a beat purely for breathing room
  after a dense insight.

## Beat templates by content type

### Coding / DSA problem (e.g. a LeetCode problem)

A reliable beat sequence:

1. **Problem statement** — show the prompt/constraints, plainly, no animation flourish.
2. **Naive/brute-force framing** — establish why the obvious approach is slow (this is what
   makes the insight land later), often via a complexity callout.
3. **Key insight** — the single "wait, what if..." moment. This deserves your best Transform.
4. **Algorithm walkthrough on a concrete example** — step through actual input values, not
   abstract variables, so the viewer can pattern-match. This is usually several continuation
   beats over one persistent diagram.
5. **Complexity recap** — before/after comparison, often a simple side-by-side or a number
   ticking down.
6. **Code reveal** (optional, format-dependent) — the actual solution code, usually a hard cut
   into a code block, held long enough to read.

### Math concept / proof

A reliable beat sequence:

1. **Intuition-first hook** — a concrete, visual instance of the idea before any formalism.
2. **Formal setup** — introduce notation only once the intuition beat has done its job.
3. **The proof/derivation steps** — each step is usually a Transform from the previous state;
   resist the urge to hard-cut between algebra steps, since the continuity *is* the proof.
4. **Generalization** — pull back (often literally, via camera) to show the specific case as an
   instance of the general one.
5. **Recap / punchline** — restate the core idea from the Scene Brief in one final beat, visually
   echoing the hook.

### General narrative / story

Less rigid — but still benefits from: a hook beat, a clear turning point beat (something visually
distinct marking "this is where it changes"), and a closing beat that echoes the opening visual
so the video feels resolved rather than just stopping.