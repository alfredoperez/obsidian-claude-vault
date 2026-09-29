# Goal mode — `--goal "question"`

Use when the user brings a **question** to a video rather than just wanting notes on it.

Goal mode is **additive**. The full normal pipeline still runs — topic note, slides, links,
transcripts, concept-layer merge. The goal adds a focused answer note on top and biases how
much depth each part of the main note gets. Never skip the normal processing to answer faster;
the archive is the point.

---

## What the goal changes

| Stage | Without a goal | With a goal |
|---|---|---|
| Main Ideas | even coverage of the talk's arc | goal-relevant ideas developed further; the rest stay proportionate |
| Reference Snapshot | tools the talk names | same, with goal-relevant ones first |
| Concept merge (6.5) | grep the video's core topics | the goal's domain is checked first and merged preferentially |
| Extra output | — | one answer note |
| Report | note + counts | note + counts + **verdict** |

The main note is never truncated or skewed into a goal document. Someone reading it a year later
with no memory of the question should still get a fair account of the talk.

---

## The answer note

Path: `Sources/videos/answers/<slug> — <goal-slug>.md`

`<goal-slug>` is the question kebab-cased and truncated to ~40 chars, so one video can hold
several answers without collision.

```yaml
---
created: YYYY-MM-DD
type: video-answer
goal: "<the question, verbatim as the user asked it>"
video: "[[<Video Title>]]"
source: <YouTube URL>
verdict: answered | partial | not-answered
---
```

### Body

```markdown
# <the question>

<THE ANSWER. 2-4 sentences, first thing on the page. No "in this video the speaker
discusses…" throat-clearing — state the conclusion, then support it below.>

## Evidence

- **[04:12]** <what was said or shown, and why it bears on the question.> Quote verbatim when
  the wording matters. [Watch](https://www.youtube.com/watch?v=<id>&t=252s)
- **[11:48]** ...

## What this video does not answer

- <the honest gap — the part of the question it never touches, or touches only in passing.>
- <a claim it asserts without support, if the question hinges on that claim.>

## Where to look next
- <only when there's a real lead: a resource the talk named, a related vault note, a follow-up
  question worth its own search. Omit the section if there is nothing genuine to say.>
```

### The verdict field

| Value | Means |
|---|---|
| `answered` | the video directly and sufficiently answers the question |
| `partial` | it answers part, or answers it with caveats the user needs to see |
| `not-answered` | the video does not address it — say so plainly and keep the note anyway |

`not-answered` is a **successful** run, not a failure. A note recording "this talk does not cover
X" saves rewatching it later. Never stretch a `partial` into an `answered`.

---

## Citations

Every evidence bullet carries an `[mm:ss]` and a deep link. Timestamps come from
`Sources/videos/raw/<slug>.timestamped.md` (written in Step 7), never guessed.

Deep-link format: `https://www.youtube.com/watch?v=<video_id>&t=<seconds>s`

Convert `mm:ss` to total seconds for the `t=` parameter. Verify the timestamp is the moment the
point is *made*, not the moment a keyword happens to appear — auto-captions lag the speaker by a
second or two, so prefer the cue slightly before the phrase.

---

## Multiple videos, one goal

When several URLs are passed with a single `--goal`, each video still gets its own full
processing (note, transcripts, links, merge). The answer is a **single synthesis note**:

Path: `Sources/videos/answers/<goal-slug>.md` (no video slug — it spans several)

```yaml
type: video-answer
goal: "<question>"
videos:
  - "[[<Video A>]]"
  - "[[<Video B>]]"
verdict: answered | partial | not-answered
```

Body leads with the combined answer, then groups evidence by video, then a
**"Where they disagree"** section when the sources genuinely conflict. Do not resolve the
conflict — present both and cite both, the same way Step 6.5 handles a `> **Tension:**` callout.

---

## Quality bar

- Answer first. If the reader has to scroll to learn the answer, rewrite it.
- Every claim in the answer traces to a cited timestamp in Evidence.
- Never infer beyond the video. If the answer requires knowledge the talk does not contain,
  that belongs in "does not answer", not in the answer.
- The "does not answer" section is not optional padding — it is the part that stops the user
  from over-trusting a partial source. Write it even when the verdict is `answered`.
