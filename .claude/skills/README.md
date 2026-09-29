# Skills

Thirteen Claude Code skills, copied from the author's collection and made standalone: no absolute paths, no references to skills that are not here. Each folder is one skill; `SKILL.md` is the entry point and `references/` holds what it loads on demand.

## Install

```bash
cp -r .claude/skills/* ~/.claude/skills/
# or symlink, so a git pull updates them:
ln -s "$PWD/.claude/skills/"* ~/.claude/skills/
```

Two scripts in `.claude/scripts/` are run from the vault root: `generate-terms-index.mjs` builds `Terms.md`, `checkup.mjs` runs the read-only health checks. Both accept `VAULT_DIR=` when run from elsewhere.

## The list

| Skill | What it does |
|---|---|
| `obsidian` | How a note is built: frontmatter, `lifespan:`, the component vocabulary, diagrams, where a note goes. Load before writing any note. Owns the structure; `writing` owns the voice |
| `writing` | The writing voice and house rules: one core, one profile per surface (article, social, CFP, vault note, explainer, persuasion, general) |
| `create-decision` | Escalate a decision out of chat into a document the reader answers in place: findings, questions with a recommended option, an empty answer slot per question |
| `create-doc` | Produce a document that leaves the vault: a self-contained HTML page with a named theme, a PDF, or a `.docx` |
| `product-prd` | Write a PRD for a feature at `Projects/<project>/product/<feature>/<Feature Name> PRD.md`, requirements numbered `R001…` |
| `product-roadmap` | Slice a PRD into now / next / later, each slice citing the requirement IDs it covers, with a coverage table that catches orphans |
| `product-story-map` | Lay a feature out as a `.canvas` wall: lanes, short cards on a fixed grid, arrows for the real dependencies |
| `product-stories` | Decompose a release slice into one story file each, Given/When/Then acceptance criteria, INVEST checked before finalising |
| `create-github-issue` | Turn a description or screenshot into a GitHub issue with a type and a priority label, after showing the draft |
| `capture` | Smart capture: detects a URL, a YouTube link, a task, a quote or a title and routes it to the right place in the vault |
| `capture-youtube` | Extract a video into topic notes, harvest the links it names into link cards, archive the transcript |
| `log` | Append a dated record to one of four tracking files: achievement, activity, demo, retro |
| `groom` | Grooming with scope as an argument: `vault` sweeps orphaned images and flags misfiled or stale notes; `knowledge` audits one topic folder; `project` moves finished items to `Done/` |
| `checkup` | Every read-only health check over the vault in one command; changes nothing |

## What changed from the originals

Every edit was to remove a dependency on the author's machine, not to change what a skill does:

- Vault paths (`~/dev/GitHub/obsidian-vault/...`) became paths relative to the vault root.
- `obsidian://open?vault=obsidian-vault` became `vault=<vault-name>`.
- References to skills not bundled here (`product-journey-map`, `create-diagram`, `create-jira-ticket`, `create-audio`, `create-notebooklm`, `capture-bookmarks`, `reading-level`, `plan`, `sync-gde-stats`, the `article-*` family) were replaced with a one-line inline instruction, or with the bundled equivalent.
- `checkup` is a vault-only cut. The original also graded published articles, skill usage and upstream drift, which need the author's skills repo.
- `product-stories` reads the roadmap when there is one, and falls back to the story map's release rows or the PRD's milestones when there is not. Its canonical template lost a section of tracker-specific ids.
- The generated `README.md` inside each skill folder is left as it was; it documents the original's connections and may name skills that are not here.
