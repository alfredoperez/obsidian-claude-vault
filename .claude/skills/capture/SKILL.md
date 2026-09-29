---
name: capture
description: "Smart capture for ideas, tasks, URLs, YouTube videos, and quotes. Auto-detects input type and routes to the right location in the vault. Use when the user says '/capture', wants to save something quickly, shares a YouTube URL, or mentions adding a task, link, or note."
---

# Smart Capture

Capture anything - ideas, tasks, URLs, YouTube videos, quotes - and route directly to the right place.

The user's input is passed as the skill argument.

## Workflow

### 1. Detect Input Type & Route Directly

| Pattern | Type | Destination |
|---------|------|-------------|
| YouTube URL (`youtube.com`, `youtu.be`) | video | **delegate to `/capture-youtube`** |
| Other URL (`http://`, `https://`) | link | Sources/links/ |
| Quoted text or `- from`/`- by` | quote | Sources/links/Phrases.md or relevant note |
| Action words (fix, add, update, create, review, test, check, investigate) | task | `Hub.md` (see Tasks below) |
| Title-like text (capitalized, descriptive) | knowledge | Knowledge/<category>/ |
| Everything else | idea | Ask where it should go |

**The Knowledge/Sources split:** notes ON other people's content (videos, articles, links)
are *sources* and land under `Sources/` — never `Knowledge/`. `Knowledge/` holds only the
user's own distilled thinking (`lifespan: durable`; a `verified:` stamp is added by a human
later, never at capture).

### 2. Handle Each Type

#### YouTube Videos

**Delegate to `/capture-youtube`.** Do not process the video here.

That skill owns the whole path — a dedupe check before anything is downloaded, `yt-dlp` for real
transcripts (WebFetch cannot get them; the page is JS-rendered), link harvesting from the
description and spoken callouts, both archived transcripts, slide capture, and the concept-layer
merge. Capturing a video here instead would write a thinner note to the *same*
`Sources/videos/<Video Title>.md` path with mismatched frontmatter and no dedupe check.

```
/capture-youtube <url>
```

Pass along anything the user asked for: `--slides` for a conference talk, `--goal "<question>"`
if they shared the video to answer something, `--links-only` if they only want the resources
it names.

#### Links (non-YouTube URLs)

**All non-YouTube URLs become per-link notes in `Sources/links/<Title>.md`** with a `cardlink` preview. The `Sources/links/Links.base` dashboard surfaces every saved link as a sortable table — do NOT append to legacy bundle files like `Website Resources.md` or `Inspiration for Personal Blog or Digital Garden.md`.

1. **Fetch metadata** with WebFetch: page title, 1-line description, hostname.
2. **Derive filename** from the title — readable casing, strip site suffixes ("| GitHub", "- Home", etc.). If the name collides with an existing file in `Sources/links/`, append `-2`, `-3`, etc.
3. **Detect category** (required frontmatter field):

   | Signal | Category |
   |---|---|
   | Repo ends in `-skill` / `-claude-*`, README mentions Claude skill or subagent | `claude-code-skill` |
   | DESIGN.md collections, awesome-lists for design, brand-system references | `design-resource` |
   | UI component registry, design tool website, AI design product | `design-tool` |
   | Fonts, typefaces, type foundries | `typography` |
   | General dev library/framework (e.g. Playwright, Vite) | `dev-tool` |
   | Personal blog, portfolio, digital garden | `inspiration` |
   | Ambiguous | Ask the user — don't guess |

4. **Infer 3-5 tags** from content (e.g. `claude-code`, `skill`, `design`, `ui`, `ux`, `frontend`, `testing`, `typography`, `awesome-list`, `ai-agent`).
5. **Create the note** using this template — leave `why:` blank:

   ```markdown
   ---
   url: <full URL>
   description: "<1-line description>"
   host: <hostname>
   category: <detected category>
   tags: [tag1, tag2, tag3]
   added: <today YYYY-MM-DD>
   lifespan: durable
   why:
   ---

   \`\`\`cardlink
   url: <full URL>
   title: "<page title>"
   description: "<full page description>"
   host: <hostname>
   \`\`\`

   ## Notes
   ```

6. **Confirm** path to user: `Saved to Sources/links/<Name>.md — open Links.base to see the table.`

**Fallback if WebFetch fails** (auth-walled, bot-blocked, 404): create the note with `description:` empty and only `url` + `host` in the cardlink block. Warn the user: "Couldn't fetch metadata — title/description blank; edit the note to fill in."

**Multiple URLs in one capture:** loop through, create one note per URL, then give a single summary confirmation.

**A whole pile of saved links** — a bookmarks export, X/LinkedIn saved posts, a Medium reading list, a phone
full of tabs — is a different job: work in batches, `grep -rl "<url>" Sources/links/` to dedupe each URL against what is already carded, classify the survivors first, then card them. That ordering matters at a few hundred links and is pointless at three.

#### Quotes
1. Check if Sources/links/Phrases.md exists
2. If topic-specific quote, search for relevant note
3. Append to appropriate file with attribution

#### Tasks
All tasks go into `Hub.md` at the vault root. Route by keywords to the right section:

| Keywords | Section in Hub.md |
|----------|----------------------|
| work, PR, review, bug, meeting, standup, feature | ## Work |
| speckit, spec-driven | ## SpecKit |
| claude code, skill, command, workflow | ## Claude Code / Workflows |
| blog, article, write, draft, edit, publish, personal | ## Writing & Personal |
| learn, read, watch, course, tutorial, investigate | ## Learn / Investigate |
| ticket follow-up | ## Follow Up Tickets |
| Other | Ask user which section |

Add task with format: `- [ ] <task description>` under the appropriate `## Section` heading.

#### Knowledge Notes (title-like input)
1. Analyze title for category and tags
2. Search Knowledge/ for related notes
3. Ask for content or if user wants to paste/dictate
4. Create at `Knowledge/<category>/<title>.md`

#### Ideas (unclear routing)
1. Present the captured idea
2. Ask: "Where should this go?"
   - Knowledge note (which category?)
   - Task (which section in Hub.md?)
   - Project (which project?)

### 3. Category Detection

Applies to knowledge notes only (own thinking). List the real folders (`ls Knowledge/`) — don't trust this snapshot blindly:

| Keywords | Category |
|----------|----------|
| Angular, NgRx, Signals, RxJS, Component | Angular/ |
| Claude, Cursor, AI, GPT, LLM, prompt | AI/ |
| Nx, Git, ESLint, IDE, VS Code, WebStorm, CLI | DevTools/ |
| workflow, productivity, Mac, Alfred, Obsidian | Productivity/ |
| testing, e2e, fakes, coverage | Testing/ |

Health/fitness content goes to `Personal/Health/`, not Knowledge/.


## Vault conventions

Load the **`obsidian`** skill before writing the note. It owns the structure — frontmatter,
`lifespan:`, components, diagrams, and where a note goes — so this skill does not carry its
own copy of the conventions.

Source notes (video/link/quote) self-identify via `type:` and live in `Sources/`. Knowledge
notes (own thinking) get `lifespan: durable`.

## Examples

**YouTube video:**
```
/capture https://youtube.com/watch?v=abc123
-> Hands off to /capture-youtube (real transcript, link harvest, dedupe check)
```

**Knowledge note:**
```
/capture Angular Signals Best Practices
-> Asks for content, suggests Knowledge/Angular/, creates note with frontmatter
```

**Task:**
```
/capture fix the auth bug in login
-> Adds to Hub.md under ## Work: "- [ ] fix the auth bug in login"
```

**Link:**
```
/capture https://github.com/pbakaus/impeccable
-> Fetches metadata, creates Sources/links/Impeccable.md with frontmatter + cardlink
-> category: claude-code-skill; tags: [claude-code, skill, design, frontend]; why: blank
```

**Multiple links:**
```
/capture https://stitch.withgoogle.com https://21st.dev/home https://fonts.google.com
-> Creates 3 notes in Sources/links/ (Stitch, 21st.dev, Google Fonts)
-> Summary confirmation with all 3 paths
```

**Quote:**
```
/capture "Data beats opinion" - from conference
-> Appends to Sources/links/Phrases.md
```
