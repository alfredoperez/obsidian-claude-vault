# Long live Markdown — the example vault

A public, clonable Obsidian vault for the six-article series **Long live Markdown**: using Obsidian and Claude Code to turn a folder of notes into a working system. Every screenshot in the series comes from this vault, and every skill the articles ask you to install is in it.

The vault's subject is **Worky**, a fictional company that schedules painter crews. It exists so the PRDs, story maps, stories and decision docs have something real to argue about.

## The series

1. **Long live Markdown** — why the notes stay plain text and what that buys you
2. **The vault has a shape** — folders, frontmatter, `lifespan:`, and where a note goes (`Reference/Vault conventions.md`)
3. **Components without a plugin** — the callout vocabulary `vault.css` styles: cards, tickets, phases, capability matrices, story maps (`Reference/Components.md`)
4. **A PRD, a story map, four stories** — the product skills, run end to end on Worky's crew scheduling feature
5. **A decision in a document** — escalating a choice out of chat and into a file the reader answers in place (`Projects/Worky/decisions/`)
6. **Grooming a vault that writes itself** — capture, groom, checkup, and the generated `Terms.md` lookup

## Get it running

```bash
git clone https://github.com/alfredoperez/obsidian-claude-vault.git
```

1. **Open it in Obsidian** — *Open folder as vault*, pick the clone.
2. **Install the plugins.** Obsidian lists the eight community plugins it expects under *Settings → Community plugins*; install each from the browser. `.obsidian/README.md` says what each one is for. The notes are plain markdown and work without them.
3. **Turn on `vault.css`** if it is not already on under *Settings → Appearance → CSS snippets*. It is what makes `[!cards]`, `[!phase]` and the rest look like components instead of grey boxes.
4. **Copy the skills** into Claude Code:

   ```bash
   cp -r .claude/skills/* ~/.claude/skills/
   # or keep them linked to the clone:
   ln -s "$PWD/.claude/skills/"* ~/.claude/skills/
   ```

   `.claude/skills/README.md` lists what each one does. Two helper scripts live in `.claude/scripts/`; run them from the vault root.

## What is in here

```
.obsidian/          config, the snippets, and a README on the plugins
.claude/skills/     the thirteen skills the series installs
.claude/scripts/    generate-terms-index.mjs, checkup.mjs
Reference/          the two vocabulary docs readers copy: conventions and components
Projects/Worky/     the fictional company and its crew-scheduling feature
  Worky.md                          the company brief: architecture, five teams, the disbanded sixth
  product/crew-scheduling/          PRD · Story Map.canvas · Design · stories/
  decisions/One calendar or three   a decision doc with its answer blocks left empty
Sources/ ~Attachments/ _Triage/     the folders the conventions name, empty
```

## Worky, in one paragraph

Three front-ends (Client Portal, Crew App, Dispatch Console), three core services (jobs, crew, scheduling), and a billing service in a corner that nobody owns since its team was disbanded. Five teams. The live feature is crew scheduling: replacing a dispatcher's spreadsheet with a board that knows the rules. Start at `Projects/Worky/Worky.md`.

## License

MIT for everything Alfredo wrote. Two CSS snippets carry their own headers: `minimal-cards.css` (MIT, Stephan Ango) and `Obsidian Colored Sidebar.css` (CyanVoxel). The canvas and bases references inside the `obsidian` skill are vendored from kepano/obsidian-skills (MIT).
