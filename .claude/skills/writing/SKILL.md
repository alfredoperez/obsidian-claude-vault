---
name: writing
description: >
  Alfredo's writing voice, structure, and house rules. Load this before drafting, editing, or
  polishing ANY prose a human will read: blog and Medium articles, LinkedIn or X posts, CFP
  abstracts, vault notes, READMEs, release notes, video scripts, summaries, and persuasive copy
  (landing pages, ads, launch copy, product descriptions, sales emails, promo scripts) via the
  Ogilvy persuasion profile. Use this skill whenever the user says '/writing', asks to write,
  draft, edit, rewrite, or polish something, asks whether something "sounds like me", wants copy
  that sells rather than copy that wins awards, or when another skill needs voice calibration.
  Make sure to use it even when the user does not explicitly mention voice or tone.
metadata:
  author: alfredo
  source: kaiju
---

# Writing

The single source of truth for how Alfredo writes. One invariant core, plus one profile per surface.
Other skills that produce prose (`obsidian`, `create-decision`, `product-prd`, `capture-youtube`) load from here instead of carrying their own copy of the voice.

Persuasion is a surface like any other: copy that sells lives in `references/persuasion.md` (the
Ogilvy profile), not in a separate skill.

## When to Use

- Drafting or editing anything a person will read.
- Writing or reviewing copy that has to sell: a landing page, ad, launch announcement, product
  description, sales email, or promo script.
- Another skill needs voice calibration.
- The user asks "does this sound like me?" or wants a voice pass on an existing draft.

## Workflow

### Step 1: Load the core voice (always)

Read `references/core-voice.md`. These are the invariants. They apply to every surface unless a
profile explicitly overrides them.

### Step 2: Load exactly one surface profile

Pick from the surface, not from the topic. Read only the matching file.

| Surface | Profile | Notes |
|---------|---------|-------|
| Blog / Medium article, build log, tutorial | `references/article.md` | Also read `references/structure.md` for anything longer than ~800 words. |
| LinkedIn, X, thread, caption | `references/social.md` | |
| CFP abstract, talk description, speaker bio | `references/cfp.md` | Bilingual EN/ES. |
| Obsidian vault note, knowledge note | `references/vault-note.md` | Overrides the em-dash and table bans. |
| Editorial hub, digest or summary meant for scanning, audio script or narration, video script, any doc whose reader may not know the vocabulary | `references/explainer.md` | Define-as-you-go explanatory register, modeled on the AI Daily Brief at the user's request. |
| Landing page, ad, launch copy, product description, sales email, promo video script | `references/persuasion.md` | The Ogilvy profile. Only for explicit promotional intent. It also loads `references/ogilvy-principles.md` when drafting or reviewing. |
| README, release note, PR body, ticket, status update, anything else | `references/general.md` | Fallback leaf. Use it rather than guessing. |

### Step 3: Write, then run the checks

Each profile ends with its own checklist. Run it before declaring the draft done. For long-form,
`references/structure.md` carries the full apply checklist.

## Non-negotiables

These get violated most often, so they are repeated here. Details and rationale live in
`references/core-voice.md`.

1. **Zero em dashes in shipping content.** Body, headings, the H1, code comments, captions.
   Grep for `—` before you call it done. Vault notes are the one exception.
2. **Contractions.** "it's / that's / don't / here's." Expanding them is a defect, not formality.
3. **Problem before solution.** Establish the pain, then reveal the fix.
4. **Keep the "because."** Attach the mechanism to the claim in the same breath.
5. **Bracket every visual.** Lead-in before, read-out after. No naked image drops.
6. **Plain headings.** No clever wordplay, no AI-ish dash headers.
7. **Practitioner stance.** Report what you observed, tried, and changed your mind about. Don't turn
   personal evidence into a universal law.
8. **Verified claims.** Check user-facing commands, defaults, versions, beta status, and numbers
   before shipping technical prose.

## Checking an existing draft

Read the core voice and the matching profile, then report violations as a list with file:line
pointers and a suggested fix for each. Do not silently rewrite unless the user asked for edits.
