---
name: manim-storyboard
description: Plans out a Manim (3Blue1Brown-style) math/coding animation BEFORE any Manim code gets written. Turns a raw idea — a LeetCode/DSA problem, a math concept, a proof, or a short story — into two approval-gated documents, a Scene Brief and a shot-by-shot Storyboard, that a downstream code-writing step then converts into scene.py. Use this skill whenever the user asks to "build a video", "make a manim animation", "storyboard this", "turn this problem into an animation", mentions Manim or 3Blue1Brown-style explainers, or wants a math/coding explainer for Instagram/Reels/Shorts (vertical) or YouTube (horizontal) — even if they never say the word "storyboard". Do NOT use this skill to write actual Manim Python code, pick colors in code, or render video — that only happens after the Scene Brief and Storyboard are both explicitly approved by the user.
---

# Manim Scene & Storyboard Planner

## Why this workflow exists

Manim videos are expensive to iterate on once code exists: timing, voiceover sync, and camera
cuts are all baked into the Python. Fixing a bad narrative choice after `scene.py` is written
usually means rewriting large chunks of it. This skill front-loads all the creative and structural
decisions into two lightweight, cheap-to-edit documents, each with its own approval gate, so that
by the time code gets written there are no open questions left — only translation work.

This skill's job stops at a well-defined, approved Storyboard. It does not write Manim code and
does not render anything.

## The workflow

1. **Gather config** — aspect ratio, duration, voiceover on/off, content type. Ask only for what
   you can't infer (see Configuration below).
2. **Stage 1 — Scene Brief.** Draft it, present it, get explicit approval or revise. Do not move
   to Stage 2 until the user approves.
3. **Stage 2 — Storyboard.** Draft it using the approved Scene Brief as the source of truth and
   the conventions in `references/manim-conventions.md`. Present it, get explicit approval or
   revise.
4. **Handoff.** Write both documents to disk (`scene_brief.md`, `storyboard.md`) so the
   code-writing step can read them. Tell the user they're ready to hand to the coding agent — do
   not start writing `scene.py` yourself as part of this skill.

Never skip a gate. If the user tries to jump straight to "just write the storyboard" without a
Scene Brief, produce a quick Scene Brief first anyway (it's short) and ask for a fast approval —
skipping it is exactly the failure mode this skill exists to prevent.

## Configuration

Ask about these up front only if they're not already obvious from context or from a project config
file (check for `manim.config.md` or similar in the working directory first — if one exists, use
it and only ask about what it doesn't cover):

- **Aspect ratio**: vertical `1080x1920` (Instagram Reels / Shorts / TikTok) vs horizontal
  `1920x1080` (YouTube). This changes composition dramatically (stacked vs. side-by-side layouts,
  font sizes, and how much can be on screen at once). Honor any format the user explicitly
  requests. If the user explicitly requests horizontal or landscape, use `1920x1080`; if they
  explicitly request vertical or portrait, use `1080x1920`. When the user does not specify a
  format, default to vertical `1080x1920` rather than asking or inferring horizontal from the
  publishing platform.
- **Target duration**: short-form (30–90s) vs longer explainer (3–10 min). Affects how much detail
  a storyboard beat can afford.
- **Voiceover**: on or off. If on, the storyboard needs word-level sync notes; if off, it needs
  on-screen text/caption timing instead.
- **Content type**: coding/DSA problem, math concept/proof, or general narrative — this determines
  which beat template to use (see `references/manim-conventions.md`).

Reasonable defaults if the user just says "build me a video" with no other detail: vertical
9:16 (`1080x1920`), voiceover on, 60–120 seconds. State the assumption you're making rather than
blocking on it.

## Stage 1 — Scene Brief

The Scene Brief is a short concept document, not a shot list. It should be readable in under a
minute. Use this template:

```markdown
# Scene Brief: [Working Title]

**Format:** [vertical 1080x1920 | horizontal 1920x1080] · **Target length:** [Xs / Xmin] · **Voiceover:** [on/off]

## Hook (first 3 seconds)
What appears on screen / what's said in the very first beat, to earn the watch.

## Core idea
One or two sentences: the single thing this video is teaching or telling.

## Why this idea, this way
The insight or "aha" the video is built around, and why an animation (vs. just an explanation)
is the right medium for it — usually because something needs to be *seen changing*.

## Audience & assumed background
What the viewer is assumed to already know, so the storyboard doesn't over- or under-explain.

## Narrative arc
3–6 bullets, plain language, no Manim jargon yet: the emotional/logical shape of the video from
hook to payoff (e.g. "confusion → constraint spotted → insight → generalization → punchline").

## Key visuals
The 2-4 visual metaphors or objects the video will lean on (e.g. "a sliding window drawn as a
highlighted sub-array", "a number line that folds in half").
```

Present this to the user and ask explicitly: **"Does this Scene Brief look right, or should I
change the angle, scope, or hook before I turn it into a storyboard?"** Revise until they approve.
Don't proceed to Stage 2 on an implicit approval like silence — wait for a clear yes.

## Stage 2 — Storyboard

Once the Scene Brief is approved, expand it into beats. Read
`references/manim-conventions.md` before drafting this — it has the mapping from narrative
intent to actual Manim primitives (which animation class to use when, how cuts/sections work,
how voiceover sync is usually expressed) and the beat templates for coding vs. math content.
This is the part of the skill that most needs those specifics, since a downstream coding agent
will treat this document as its literal spec — anything left vague here becomes an ambiguous
guess in the code.

Each beat must specify: timecode range, what's visually on screen (and where, respecting the
chosen aspect ratio's safe zones), which Manim animation family accomplishes that, the voiceover
line or caption text for that beat, and whether the beat ends in a hard cut, a soft transition, or
continues into the next beat.

Present the full storyboard and ask: **"Does this storyboard look right beat-by-beat, or are
there sections you want re-paced, re-cut, or re-worded before this goes to code?"** Iterate on
the whole document (re-present it in full after edits, not just the diff) until approved.

## Handoff

Once approved, save:
- `scene_brief.md` — the approved Stage 1 document
- `storyboard.md` — the approved Stage 2 document

Tell the user these are ready for the code-writing step. If you don't have visibility into that
step's own conventions, don't guess at them here — the storyboard's job is to be an unambiguous
creative spec, not Manim code.

## A note on iteration

Treat every round of feedback as a full rewrite of the affected document, not a patch. Storyboards
in particular tend to have knock-on effects — changing beat 3's pacing usually shifts every
timecode after it — so re-derive the whole document rather than editing in place and risking
inconsistent timecodes.
