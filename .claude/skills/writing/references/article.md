# Surface: Long-Form Article

Blog posts on alfredo-perez.dev, Medium cross-posts, build logs, tutorials, deep dives.

Load `core-voice.md` first. For anything over ~800 words, also load `structure.md`, which governs how
the argument is built. This file governs format.

## Hard Rules (this surface)

- **Zero em dashes.** Body, headings, the H1, code comments, captions. Grep for `—` before export.
- **No markdown tables.** Medium doesn't render them. Convert to lists: bold header plus bullet items.
- **Bracket every visual.** Lead-in sentence before, read-out after. Heroes under the H1 are exempt.
- **Heroes carry no text.** The blog renders the title as its own H1, so a hero with baked-in text
  duplicates it.

## Choose the Article Mode

Pick the mode from the article's intent before outlining it. Record the choice in the outline.

- **Practitioner essay:** observation → mental model → patterns → lived example → revised principle
- **Product explainer:** release or friction → why it exists → mechanism → use cases → limitation →
  getting started
- **Tutorial:** desired outcome → prerequisites → steps → verification → failure modes → next move

Use the smallest structure that fits the argument. Don't force a comparison, FAQ, recap, or CTA
when it adds no new information.

## Word Count Targets

- Short (intro, overview): 500-900 words
- Standard (tutorial, how-to): 900-1600 words
- Deep dive (essay, comparison, case study): 1400-2500+ words

These are planning guides, not caps. Never remove context needed to understand or trust the argument
just to hit a range.

## Page Shape

Every article opens the same way on every surface: hero image, title, subtitle, then the body.

- The hero is the first line of `## Content`, before any prose. Never mid-body.
- `subtitle:` is a frontmatter field, and it is the text people see before they decide to click:
  Medium shows it in every listing, and a publication editor reads it before the body. So it is
  descriptive and it carries a hook. One or two sentences that continue the title as a story and end
  on what the reader gets: "Nine months of spec-driven development left me with a folder nobody
  opened, including my own AI agent. Here's what made the specs readable again." It is not the SEO
  description; `summary:` still holds that. A subtitle that only restates the title is a defect.
  Two more rules, learned on the 22nd SpecKit piece: the subtitle says what the reader gets, not what
  the author did ("one page per run, review the agent applies in place, and a pipeline you can bend",
  not "here's the extension I built"), and it never repeats a word the title already uses, product
  names included, because Medium shows the pair as one line and a repeated word wastes the length.
- On Medium the reader arrives from outside. The opening names the project in time and in plain
  words before any number about it ("A year ago I started a spec-driven project and shared it with
  the world. The repo now holds 94 spec folders..."). That puts the product in context, tells the
  reader what it is, and reads as a story rather than self-promotion. The blog can skip it; Medium
  cannot. One publication accepted the piece in this shape, and the same shape gets the next one in.
- The title comes from the `# H1`. The body never repeats it.

## Markdown Conventions

- `**Bold**` only for a coined term where it is defined. Not tool names, not emphasis, not the
  quotable line
- Blockquotes for pull quotes or alternative approaches
- Horizontal rules (`---`) between major sections
- Image placeholders as `![[IMG-slug.png]]`, always with the explicit file extension, plus an HTML
  comment describing what to capture
- Code blocks carry emoji labels (`// 📃 filename.ts`, `// 👇 Important`)

## Headings

- `##` for major sections, `###` for subsections and steps
- Never deeper than `###`. Keep the hierarchy flat.
- Plain and descriptive. Question headers ("Why HTML?") and noun phrases are fine because they're
  plain. No wordplay, no dash headers.

## Readability

- Flesch reading ease: target 60-70 (conversational technical writing)
- Short paragraphs, one self-contained claim each

## Checklist

- [ ] Opening fits the article mode and puts the most visceral asset before the feature tour
- [ ] Grep for `—`: zero hits, including the H1
- [ ] Zero markdown tables; comparisons are lists
- [ ] Contractions throughout, no "it is / do not" stiffness
- [ ] Numbers are verified and decision-relevant; no manufactured precision
- [ ] Technical claims use current user-facing names, defaults, versions, and limitations
- [ ] Every visual has a lead-in and a read-out that adds an inference
- [ ] Every image embed has an explicit `.png` extension
- [ ] Ending leaves forward momentum, an implication, or an earned invitation; no generic summary
- [ ] Headings plain, flat, and free of wordplay
- [ ] No section repeats the thesis at lower resolution; FAQ/recap/CTA modules are earned, not automatic
- [ ] **Read the opening and one middle section aloud.** Anything you stumble over gets rewritten. A sentence that is hard to say is hard to read, and this catches the stiffness that the em-dash and contraction checks miss
- [ ] The reader is one named person, not an audience (see **Before the traits: name the reader** in `core-voice.md`)
