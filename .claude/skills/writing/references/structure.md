# Structural Playbook

The structure-and-flow layer above `core-voice.md`. Use it for articles longer than about 800 words.
Choose an article mode first, then use only the modules the argument earns.

## Contents

- Choose the mode
- Shared spine
- Mode blueprints
- Flow and explanation
- Structural economy
- Technical claim audit
- Visual and formatting rules
- Taste filters
- Apply checklist

## Choose the mode

### Practitioner essay

Use for field guides, lessons learned, changed beliefs, and "how I work" pieces. The author is
reporting from experience, not announcing a universal method.

**Shape:** observation → mental model → patterns or techniques → lived case → revised principle.

### Product explainer

Use for releases, feature explanations, and build stories. The product is the implementation of a
lesson, not the hero of a sales page.

**Shape:** release or felt friction → why it exists → mechanism → strong use cases → limitation →
getting started.

### Tutorial

Use when the reader primarily wants to accomplish a task.

**Shape:** outcome → prerequisites → ordered steps → verification → failure modes → next move.

## Shared spine

- Open on a concrete observation, release, changed belief, or desired outcome. A rhetorical question
  is optional, never the default.
- Credit the status quo fairly before pivoting. State its real virtue in one or two sentences so the
  disagreement reads as discovery rather than positioning.
- Pivot into first-person friction when the evidence is personal: "I kept finding...", "I've
  found...", or "I initially thought...".
- State one load-bearing thesis in plain English. A reader who stops there should still understand
  the point.
- Make the thesis tangible with evidence appropriate to the topic: a scenario, prompt, code sample,
  screenshot, diff, failure, or measured result.
- Put motivation before mechanics, then walk the mechanism end to end so the reader can verify each
  hop.
- Place caveats beside the claim they limit. Don't defer all honesty to a late disclaimer.
- Close with the implication, the next experiment, or a light invitation. A CTA is optional.

## Mode blueprints

### Practitioner essay blueprint

1. Open with the observation or old belief.
2. Name and define the mental model only if the label makes the idea easier to reuse.
3. Show how the model changes decisions through a small set of patterns.
4. Include one lived example that connects the patterns into a real sequence.
5. End with the revised principle or next experiment.

### Product explainer blueprint

1. Start with the friction that made the feature necessary or the news that changed the workflow.
2. Explain the design choice and the intuitive alternative that failed.
3. Walk the mechanism with enough detail to verify the claim.
4. Use three to five strong cases at most; one vivid case beats a feature catalog.
5. State the wrong-fit case or adoption cost.
6. Give the minimum first move.

### Tutorial blueprint

1. State the finished outcome and what the reader needs before starting.
2. Give ordered, runnable steps with complete examples.
3. Add a verification point after each risky transition.
4. Explain the common failure modes and recovery path.
5. End with the next useful extension, not a recap of completed steps.

## Flow and explanation

- Run the intuitive-but-wrong loop when it reveals a real design decision: initial approach → why it
  failed → better approach. Don't manufacture a failed alternative for every section.
- Anchor abstractions quickly: claim → because → concrete instance. Never let theory float for more
  than a paragraph.
- Use occasional one-line sentences after dense passages as cognitive rest stops, not as a repeated
  copywriting tic.
- Keep one template per repeated section so the reader learns the rhythm once.
- Distill a technique into "The key is..." or "The trick is..." only when the line carries a
  portable heuristic.
- Coin a term only when it gives the reader useful vocabulary. Define it immediately and show one
  instance.
- Use complete, paste-ready prompts when prompting is the subject. For other topics, use the artifact
  that best demonstrates the claim.
- Point out self-demonstrating evidence when the article or diagram was produced by the method being
  discussed.

## Structural economy

Every section must add new information, evidence, or a useful decision.

- Choose a FAQ or a recap when one is genuinely useful. Don't include both by default.
- Repeat the thesis once at the close at most, not after every major section.
- Cut packaging before substance: slogans, transitions, repeated assurances, image narration, and
  summaries go before mechanisms, caveats, examples, or setup context.
- Use a tagline at most once.
- Treat word-count ranges as diagnostics, not limits. A long article should be long because the
  argument needs the space, not because the template has many modules.
- Keep use-case lists to three to five information-dense entries. Remove near-duplicates.
- Don't add a comparison, "When not to use", FAQ, cheat sheet, or CTA solely because a template lists
  it.

## Technical claim audit

Before shipping a technical or product article:

- Verify commands as the reader actually types them, not only internal or canonical IDs.
- Verify defaults, beta status, thresholds, provider differences, version numbers, dates, and install
  requirements against the current source of truth.
- Distinguish current behavior from planned, experimental, or latent behavior.
- Use verified, decision-relevant numbers. Never invent precision to make a claim sound credible.
- Link or name the evidence behind surprising claims when the surface allows it.
- Qualify or flag anything that couldn't be verified.

## Visual and formatting rules

- Use plain, descriptive headings. Questions and noun phrases are fine; forced wordplay is not.
- Keep the hierarchy flat at `##` and `###`.
- Bold a coined term when defining it and an imperative in a recap list when a recap is earned.
- Prefer lists over tables in articles because the blog and Medium must both render cleanly.
- Keep paragraphs short, with one self-contained claim each.
- Bracket visuals with a lead-in and a read-out, but make the read-out add an inference. Don't write
  "follow the arrows" or repeat labels already visible in the image.
- Set example prompts apart as artifacts rather than blending them into the prose.

## Taste filters

- **Landing-page test:** If a sentence could move unchanged onto a landing page, rewrite it as an
  observation, mechanism, or example.
- **Launch-copy pressure:** Avoid repeated triplets, "what this buys you", "for free", "the payoff",
  and taglines echoed through the body.
- **False universals:** Preserve "I've found" and "I tend to" when the evidence is experiential.
- **List inflation:** One vivid example beats eight near-parallel use cases.
- **Mechanism-free bullets:** A list of benefits without the because reads as an announcement, not an
  explanation.
- **Repeated caveats:** State a limitation once, beside the claim it constrains.
- **Sentimental close:** Land the human stake in one beat, then stop.
- **Soft qualifiers as substance:** Remove "very", "really", "just", and "simply" when they stand in
  for evidence.

## Apply checklist

- Is the article mode explicit and appropriate to the reader's job?
- Does the opening use a concrete observation, release, changed belief, or outcome rather than a
  forced rhetorical question?
- Does personal evidence stay personal instead of becoming an unsupported universal rule?
- Can a header-only skim reconstruct the argument?
- Does every abstraction have a mechanism and a concrete instance nearby?
- Are examples matched to the topic rather than defaulting to prompts?
- Are numbers verified and useful rather than decorative?
- Did the technical claim audit cover public names, defaults, beta state, providers, and limitations?
- Does every section add information, evidence, or a decision?
- Are FAQ, recap, comparison, wrong-fit gate, and CTA included only when earned?
- Does every visual read-out add an inference instead of narrating the image?
- Did the landing-page test catch slogans, repeated taglines, and launch-copy triplets?
- Does the close leave an implication, next experiment, or light invitation without hard selling?
- Are headings plain and flat, lists used instead of tables, and em dashes absent from shipping prose?
