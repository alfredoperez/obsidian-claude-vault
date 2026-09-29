# Knowledge-mode extras

`groom knowledge <topic>` runs the same verdict pass as `groom vault` (see `references/verdicts.md`)
over ONE `Knowledge/<topic>/` folder, then adds the four things a topic folder needs and a
vault-wide sweep can't give it: stub detection, frontmatter completeness, broken-link detection, and
a regenerable `index.md`.

## Scan rules

1. List all `.md` files in the target folder (**non-recursive** — do not descend into subfolders).
2. **Skip entirely**: `index.md` (it is an output of this mode, not an input), `Done/`, `~Archive/`, anything starting with `_` or `~`.
3. If the folder is empty, report "Nothing to groom — folder is empty" and stop.

## Per-file capture

Read each file's full contents. For each note, capture:

- **Word count** and **line count**.
- **Frontmatter completeness** — presence/absence of `created`, `tags`, `source`, and `lifespan` (Knowledge notes are `lifespan: durable`; see `Vault-Guide.md` → Lifecycle & Grooming Rules).
- **Top keywords** — 3–5 noun phrases or proper nouns that best describe the content. Filter stopwords. Prefer multi-word phrases (e.g. "claude code", "rule files") over single words. These power the clustering below.
- **Wiki links out** — every `[[Target]]` reference. Note any that resolve to non-existent files (broken links).
- **Stub signals** — any of: word count below 100; sections that end with a heading but no body (abrupt end); `TODO`, `FIXME`, `WIP`, "stub" markers in the body; body is just a redirect to another note ("see `[[X]]`").
- **Stale signals** — any of: references to specific tool versions older than the current ecosystem (e.g. "Angular 14" when current is 18+); `created:` date more than 12 months old AND no recent edits visible in the file; references to files or URLs that no longer exist.

## Clustering (near-duplicate candidates)

- Two files are in the same cluster if they share **2 or more top keywords**.
- A cluster of 2+ files is a **merge candidate**, not a guarantee. Propose; the user decides.
- For each cluster, pick one file as the **likely canonical** (longest body, most cross-references, most recent `created` date). Note the others as merge-into candidates.

The heuristic (2+ shared keywords) is intentionally loose — it finds *candidates* the user can
quickly accept or reject. Tightening it risks missing real duplication.

## Report block

```
Grooming: <target folder> (<N> files)

Stubs (<count> — consider expanding or deleting):
  - <filename> [<W> words] — <reason: too short / abrupt end / TODO marker / redirect-only>

Duplication clusters (<count> — consider merging):
  Cluster: <topic name>
    - <filename A> [<W> words] (likely canonical)
    - <filename B> [<W> words] → merge into A
    - <filename C> [<W> words] → merge into A

Stale signals (<count>):
  - <filename> — <reason: old tool version / stale date / broken link to X>

Missing frontmatter (<count>):
  - <filename> — missing: <created, tags, source>

Broken wiki links (<count>):
  - <filename> → [[<target>]]

Index proposal — <target folder>/index.md:
  ## <Top-level grouping 1>
    - [[<note>]] — <one-line summary>
    - [[<note>]] — <one-line summary>
  ## <Top-level grouping 2>
    - [[<note>]] — <one-line summary>
```

If a section has no findings, omit it entirely (don't print "Stubs (0)").

## The write menu

```
What would you like to do?
  1. Write/update index.md
  2. Backfill missing frontmatter (created, tags, source) on flagged notes
  3. Add follow-up tasks to Hub.md for proposed merges and stub fixes
  4. Stamp `groom: review` on notes that got a verdict
  5. All of the above
  6. None — exit
```

- **Option 1** — write the proposed index to `<target folder>/index.md`. Overwrite if it exists. Include:
  ```yaml
  ---
  type: index
  generated_by: groom
  generated_at: <ISO date>
  ---
  ```
  This frontmatter signals that the file is regenerable and should not be hand-edited.
- **Option 2** — for each flagged note, add a minimal frontmatter block with `created: <today>`, an empty `tags: []`, `source:` if known, and `lifespan: durable` (every `Knowledge/` note is durable). **Never overwrite existing frontmatter values — only fill blanks.**
- **Option 3** — append a section to `Hub.md` under `## Knowledge Grooming`:
  ```
  ## Knowledge Grooming — <target folder> — <date>
  - [ ] Merge <filename B> into <filename A> (cluster: <topic>)
  - [ ] Decide: expand or delete <stub filename>
  - [ ] Fix broken link in <filename> → [[<target>]]
  ```
  The `Hub.md` task format intentionally uses Obsidian Tasks checkboxes so the user can complete
  them inline with their normal task flow. Don't add dates to these tasks; the grooming context is
  enough.
- **Option 4** — the `groom_*` stamp from `references/verdicts.md`.
- **Option 6** — exit cleanly. Print "No changes made."

After execution report one line: `Wrote index.md, backfilled 3 frontmatter blocks, added 5 tasks to Hub.md`.

## Clean folder

If the audit finds nothing — no stubs, no clusters, no stale signals, no missing frontmatter — report:

```
Nothing to groom in <folder>. <N> files all look healthy.
Generate an index.md anyway? (y/n)
```

If yes, write a fresh `index.md` grouping the notes by their existing tags or by inferred topic.

## Tips

- For folders with mixed content, the index proposal works best when grouped by **content type**, not by chronology. Top-level groupings like "Rule Systems", "Patterns", "Learning & Memory" beat "January notes", "February notes".
- **Knowledge/Sources boundary** applies here too — see `references/verdicts.md`. Flag as misfiled; proposal only.
