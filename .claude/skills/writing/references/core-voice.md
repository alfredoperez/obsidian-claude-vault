# Core Voice

The invariants. These hold on every surface unless a profile explicitly overrides them. Derived from
published articles on alfredo-perez.dev.

## Voice Summary

**Conversational, dev-to-dev.** Like explaining something to a smart colleague over coffee. Not
academic, not salesy. Practical and direct.

## Before the traits: name the reader

Write for **one specific person**, not an audience. Name them before you draft: the
colleague who hit this exact problem last week, the engineer who tried the tool and
bounced, the person who asked you about it at a conference.

An audience makes you hedge, because you are covering everyone. One reader makes you
choose what to explain and what to assume, which is the same decision the whole piece
rests on. If you cannot name the reader, the draft will read as written for no one.

## Core Traits

### 1. Problem-First Structure
Establish the pain before revealing the fix. Readers should nod along thinking "yes, I've been
there" before you offer the solution.

- Open with a relatable scenario
- Describe the frustration concretely
- Introduce the solution as the natural answer

Example from "Introducing ngx-dev-toolbar":
> How many times have you said "let me just update the configuration in the database really quick"?

### 2. Practitioner Stance
Write as someone reporting from the work, not presenting a finished doctrine.

- Default to a concrete observation, changed belief, or moment from the work
- Show the initial assumption, what complicated it, and the model that replaced it
- Use "I've found", "I tend to", and "in my experience" when the evidence is personal
- Don't promote one experience into a universal rule without broader evidence
- Treat the product or technique as evidence for the lesson, not as the hero of the article
- Put a limitation beside the claim it constrains, not in a disclaimer at the end

Rhetorical questions are optional. Use one only when it sounds like something the author would
actually ask a colleague. The default opener is declarative: "I kept running into...", "Last week,
we released...", or "Markdown has become...".

### 3. Short Sentences for the Takeaway, Not for Lists
Short sentences for key takeaways. Longer sentences for explanation and context.

**Impact:** "This is vibe coding."
**Explanation:** "Instead of jumping to code, you first make your intent explicit through
specifications that become executable artifacts."

A chain of fragments is not impact, it is a tell. "It was rewrites. Refactors. Deletions." reads
generated; the author's own edit on publish was "It was rewrites, refactors, and reversals: decisions
I made in March and undid in June." One fragment per section at most, never three in a row. Same
for the "X. Not Y." reversal: "That's a problem SDD creates. It doesn't solve it." became "SDD is
what created that problem. It shouldn't be that way." Say the plain sentence.

### 4. Conversational Transitions
Natural bridges between sections, not generic headings.

Use: "Here's the thing:", "The consequences compound.", "Let me walk you through...", "Now let's see
this in action.", "Well, one thing you can do is..."

Avoid: "In this section, we will...", "As previously mentioned...", "It is important to note that..."

### 5. Code Examples with Emoji Labels
Emoji annotations in code blocks guide the reader's eye.

```typescript
// 📃 app.component.ts        ← File name
// 👇 Add the toolbar here    ← Attention pointer
```

### 6. Quantify When the Number Is Real
Don't say "it's faster" when a verified measurement exists. Use the real figure: "5-minute setup"
or "fails 1 in 50 runs." Never invent precision or force a number into a claim that is better
expressed as a concrete consequence.

### 7. End with What's Next
Never end with a generic "in conclusion" summary. End with forward momentum.

Good: "Next up: a deep dive into SpecKit Companion's sidebar." / "Check out ngx-dev-toolbar on GitHub
and give it a try. Your future self (and your flow state) will thank you!" / a CTA with a link.

Bad: "In conclusion, we have covered..." / "To summarize the key points..." / "Happy developing!"

### 8. Forward-Momentum Sign-Offs
End with a call to action, a link, or a teaser for what's next. Not a generic sign-off.

A sentence that only points at the next heading ("That drift flag is the next question.") is
packaging. The heading does that job; cut the sentence.

### 9. Write in Contractions (Register)
Coffee-chat cadence, not essay register. "it's / that's / don't / you're / here's / can't" is the
default. A default, not a rule: the author expands one on purpose for weight ("I would have done the
same", "That is why there are 94 of them") and at the start of a paragraph. Never flag a single
expanded contraction as a defect; flag a paragraph where every sentence is stiff.

### 10. Bracket Every Visual
Never drop an image, diagram, or screenshot naked. **Lead-in before** (a sentence telling the reader
what they're about to see and why) and **read-out after** (the inference or consequence the visual
earns). Don't narrate labels or arrows the reader can already see. An embed with no setup and no
payoff is a defect to flag. Heroes directly under the H1 are the one exception, since there's
nothing to lead in from.

The read-out is an inference, never a description. "Before, on the left: the agent sweeps past a
grid of dim, closed spec cards..." is a caption pretending to be a paragraph, and the author cut all
four of those from the last article on publish. What the picture shows goes in the alt text. What
the picture proves goes in the sentence before it. If there is nothing to prove, the image goes.

### 11. Lead With Your Most Visceral Asset
Open on the most concrete, share-worthy thing you've got: the pain, the reversal, the live demo, the
failing terminal. Demote the feature tour to evidence that comes *after*. If your best moment is
sitting at 60-85% depth, you've buried the lede. The build logs are the in-house exemplars: BL0 opens
on "I built my own tool, and I'm about to stop shipping it."

Visceral does not mean cold. A number the reader cannot parse yet is a riddle, not an opening.
"Right now the repo holds 94 spec folders, 238 markdown files" was rewritten on publish to three
short paragraphs first: what I built, what the tool is, what my project is. Then the number. Orient
in under 80 words, then hit. The reversal still lands above the fold.

### 12. Keep the "Because"
Attach the mechanism to the claim, in the same breath. "It runs the full pipeline, *because* the safe
default is never to silently drop a phase." Cut length elsewhere. Never cut the because. Show the
gear so the reader can generalize, not memorize.

## What to Avoid

- **Em dashes in shipping content.** HARD RULE: zero em dashes (—) in body, headings, code comments,
  or captions. Use periods, commas, or colons. This includes the H1: the Build Log series uses
  "Build Log N: Subtitle" with a colon. Scan for `—` before export. (Vault notes override this.)
- **Uniformly stiff paragraphs.** Every sentence in "it is / that is / do not" form reads generated.
  One expanded contraction for weight is the author's voice. See Trait 9.
- **Fragment chains and "X. Not Y." reversals.** Three fragments in a row, or the two-sentence
  reversal, is the most reliable AI tell in a body. See Trait 3.
- **Caption paragraphs.** A paragraph after an image that describes the image. See Trait 10.
- **Bold in the body.** No bold on the quotable line, no bold on the two things being contrasted.
  Bold a coined term once, where it is defined, and nothing else.
- **The clever verb.** "drags", "demoted", "flips", "reach for", "own the confusion", "filing
  failure" all became "pulls", "relegated", "reverses", "go for", "take the blame", "organization
  issue" on publish. Use the word the author would say out loud, not the punchier synonym.
- **Section-bridge teasers.** "That drift flag is the next question." The heading already does it.
- **Slogan openers and aphorism captions.** A short tagline sentence followed by a list with no verb,
  or a caption built as a neat parallel, reads as launch copy, not as someone explaining to a friend.
  "One colour means yours. A hook you added, a node you rewrote, a template section you replaced, all
  carry the same mark" became "Anything your project changed carries the same color: a hook you added,
  a node you rewrote, a template section you replaced." "One half lives in the editor, the other in
  the terminal." became "Two installs: the VS Code extension you look at, and the spec-kit extension
  that runs in the terminal." Say what the reader sees and what it means, in a plain sentence with a
  verb. The test: would you say it out loud to the colleague across the table?
- **Closing a door.** "That doesn't help." is a wall. "It shouldn't be that way." opens onto the
  fix the piece is about to give. The opening states the problem, then points at the way out,
  because the reader has to want to keep going.
- **An opening that reads generated.** Medium is penalizing text that scores as AI, and
  publications reject it to protect themselves. The introduction is the part they paste into a
  detector. Before export, read the first five paragraphs aloud and run them through a detector;
  if it scores high, the fixes above (orient, un-fragment, plain verbs, one expanded contraction)
  are the ones that move the score.
- **Unsourced facts in the close.** "MIT-licensed" was cut on publish because nothing in the piece
  backed it. Every factual claim in the closing paragraphs has a source inside the piece, or goes.
- **AI-ish headings with dashes.** "Start Lean — What We Cut" feels generated. Use plain, direct
  headings: "What We Cut".
- **Catchy or clever subheaders.** No forced wordplay, no marketing hooks in headings. Descriptive
  and natural.
- **Naked image drops.** An embed with no lead-in and no read-out. See Trait 10.
- **Buried lede.** The most visceral asset sitting past ~40% depth behind a feature tour. See Trait 11.
- **Jargon without context.** Define terms on first use if the audience might not know them.
- **Passive voice.** "The toolbar is loaded" becomes "The toolbar loads".
- **Filler qualifiers.** "very", "really", "just", "simply", unless genuinely conversational.
- **Apologetic language.** "This is a bit complex" becomes a clear explanation.
- **Generic intros.** "In today's fast-paced world..." becomes the specific problem.
- **Launch-copy pressure.** If a sentence could move unchanged onto a landing page, rewrite it as an
  observation, mechanism, or example. Use a tagline at most once. Avoid repeated triplets, "what
  this buys you", "for free", and "the payoff".
- **False universals.** Keep "I've found" when the evidence is one person's repeated experience.
- **Forced metrics.** Quantify only with verified, decision-relevant numbers.

## Reference Articles

Read these for calibration when the voice feels off:

- `Projects/Content/Writing/SpecKit/01 - Stop Vibe Coding Start Shipping.md` — problem-first structure
- `Projects/Content/Writing/Angular/ngx-dev-toolbar/01 - Introducing ngx-dev-toolbar.md` — rhetorical
  questions, quantified benefits
- `Projects/Content/Writing/My SDD/Build Log 0 - Kickoff.md` — leading with the visceral asset, the
  tight five-beat template

(Paths are relative to the author's own vault; they are examples of the voice, not files in this repo.)
