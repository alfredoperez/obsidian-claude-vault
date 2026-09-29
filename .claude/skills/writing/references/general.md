# Surface: General

The fallback. READMEs, release notes, PR bodies, tickets, status updates, docs, summaries, emails,
video scripts, anything not covered by another profile.

Load `core-voice.md` first. Use this file rather than guessing at a profile.

## The Governing Rule: Human First

Lead with plain language, then separate the technical detail.

- **Plain first.** Open with what it does and why it matters, in words a non-engineer could follow.
  No inline-code soup. No slash commands, symbol names, schema keys, or file paths inside the
  explanation itself.
- **Split the two.** A short human section ("What it does", "How to test") sits above a clearly
  labeled technical section ("Under the hood", "Details") that holds the jargon, file names, flags,
  and snippets.
- **Don't sound like notes for an AI.** Write like you're explaining to a smart colleague over
  coffee. Full sentences, plain verbs. If a sentence is mostly `code spans`, rewrite it.
- Technical precision still matters. It just lives in the labeled details section, not smeared
  through the explanation.

## Hard Rules

- **Zero em dashes** in anything shipping outward (READMEs, release notes, changelogs, emails).
- **Lead with the outcome.** The first sentence answers "what happened" or "what does this do." The
  reasoning comes after, for readers who want it.
- **Tables only for short enumerable facts.** Explanations belong in the prose around the table, not
  inside the cells.
- **No headers-and-sections on a simple answer.** Match the format to the size of the question.

## Summaries

End any plan or execution report with a concise, human-readable summary. Easy to digest at a glance,
focused on what happened or what's proposed, not on how.

## Checklist

- [ ] The opening sentence is plain enough for a non-engineer
- [ ] Jargon is quarantined in a labeled technical section
- [ ] Leads with the outcome, not the process
- [ ] Grep for `—`: zero hits in outward-facing content
- [ ] Full sentences, not a bullet list of identifiers
