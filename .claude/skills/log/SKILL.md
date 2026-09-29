---
name: log
description: "Append a dated record to one of the four tracking files, with what-to-log as an argument. `log achievement <text>` → Work/Achievements.md (year + quarter, for the yearly review). `log activity <details|screenshot>` → Personal/GDE/GDE-Activities.md (the GDE/Advocu table). `log demo <type> <note>` → Work/Weekly Demos.md (feature / flag-add / flag-remove / devx, by week). `log retro <note>` → Work/Retros.md (what went well / what could improve / action items). Use when the user says '/log', '/log achievement', '/log activity', '/log demo', '/log retro', ships something significant or demo-worthy, mentions an accomplishment or milestone, completes a feature or flag change or DevX improvement, mentions a GDE activity, conference talk, meetup, blog post, video, or open source contribution, shares a screenshot of activity metrics or an event page, or wants to note something for the next retro or retrospective."
argument-hint: "achievement <text> | activity <details|screenshot> | demo <type> <note> | retro <note>"
# effort: records what happened, no analysis
effort: low
---

# Log

One skill, four tracking files. Every mode is the same shape — read the target file, find or create
the right dated section, append one record, save, confirm — but each has its own target path, its own
structure, and its own prompts. Pick the mode from the first argument.

| Mode | Target file | Grouped by | Record shape |
|---|---|---|---|
| `log achievement` | `Work/Achievements.md` | `## YYYY` → `### Q#` | bullet |
| `log activity` | `Personal/GDE/GDE-Activities.md` | the `## Activities` table | table row, newest first |
| `log demo` | `Work/Weekly Demos.md` | `## Week of YYYY-MM-DD` → type section | bullet |
| `log retro` | `Work/Retros.md` | `## YYYY-MM-DD` → category | bullet |

## When to Use

- `/log achievement` (or `/log`) — the user ships something significant, mentions an accomplishment or milestone, or wants something tracked for the yearly review.
- `/log activity` (or `/log`) — a GDE-trackable activity: a conference talk, meetup, blog post, video, podcast, workshop, open source release. Also when the user shares a screenshot of activity metrics or an event page.
- `/log demo` (or `/log`) — the user shipped something demo-worthy: a feature, a feature-flag change, a DevX improvement.
- `/log retro` (or `/log`) — the user mentions a retro / retrospective, or wants to note something for the next one.
- Bare `/log` — ask which of the four. Never guess.

## Inputs

- **Mode** (first argument, required): `achievement` | `activity` | `demo` | `retro`. Missing or unrecognized → ask which.
- **Payload** (rest of the argument): free text for `achievement` and `retro`; `<type> <note>` for `demo`; text, a screenshot path, or nothing (interactive) for `activity`.

If the payload is missing, ask for it interactively using the mode's prompt below — never invent the
content.

---

## Mode: `achievement` → `Work/Achievements.md`

Log an achievement for yearly review tracking.

### Step 1: Get the description

If an argument was provided, use it. Otherwise ask: **"What's the achievement? Describe what you accomplished."**

### Step 2: Determine the quarter

From today's date:

- **Q1** — January through March
- **Q2** — April through June
- **Q3** — July through September
- **Q4** — October through December

### Step 3: Read and update the file

1. Read `Work/Achievements.md`.
2. Look for the current year section (`## YYYY`). If it doesn't exist, create it **at the top**.
3. Look for the current quarter subsection (`### Q#`). If it doesn't exist, create it under the year.
4. Append the achievement as a bullet (`- Achievement description`) under the current quarter.

Expected structure:

```markdown
## 2026

### Q1
- Achievement one
- Achievement two

### Q2
- ...
```

### Step 4: Confirm

> Added achievement to **YYYY Q#**: "[description]"

---

## Mode: `activity` → `Personal/GDE/GDE-Activities.md`

Log a GDE activity to the tracking table for later Advocu sync. **This is the GDE/Advocu one** — it
writes the `## Activities` table that a stats sync can later refresh with install and download
counts, so the row shape below must stay exact.

### Activity types

These align with Advocu's GDE submission tools:

| Type | Use for |
|------|---------|
| Content Creation | Articles, blog posts, videos, podcasts, screencasts |
| Public Speaking | Conference talks, meetup presentations, panels |
| Open Source | Package releases, contributions, maintenance |
| Workshop | Training sessions, hands-on labs |
| Mentoring | Mentoring activities |
| Product Feedback | Google product feedback |
| Googler Interaction | Interactions with Google employees |

### Step 1: Get activity details

Three input modes:

**Text argument** — parse from natural language. Example:
`/log activity Talk at GDG Austin on March 10, 45 attendees, https://meetup.com/...`

**Screenshot** — if the user provides an image path, read it with the Read tool. Extract: activity
type, title, date, platform, reach metrics, and any URLs visible in the screenshot. If any field is
unclear, ask the user.

**Interactive** — if no argument or insufficient details, ask for each field:

1. What type of activity? (Content Creation, Public Speaking, Open Source, Workshop, Mentoring, Product Feedback, Googler Interaction)
2. Title/description?
3. Date? (default: today)
4. Platform? (e.g. Blog/Website, YouTube, Angular Air, DevFest, npm, VS Code Marketplace)
5. Reach/metrics? (e.g. 1500 views, 90 attendees)
6. Link?

### Step 2: Normalize fields

- **Date** — `YYYY-MM-DD`. Default to today if not specified.
- **Type** — must match one of the types in the table above.
- **Title** — short description of the activity.
- **Platform** — where it was published/presented.
- **Reach** — numeric metric. Use `-` if unknown.
- **Metric** — what Reach measures: Views, Attendees, Installs, Downloads. Use `-` if unknown.
- **Link** — URL to the activity. Use `-` if none.
- **Advocu** — always `No` for new entries.

### Step 3: Read and update the file

1. Read `Personal/GDE/GDE-Activities.md`.
2. Find the `## Activities` section and the markdown table.
3. Insert the new row **directly after the header separator row** (`|------|...`), so newest entries appear first.

### Step 4: Confirm

> Added GDE activity: **[Type]** — "[Title]" ([Date])

---

## Mode: `demo` → `Work/Weekly Demos.md`

Log a demo item to the weekly demos file.

### Type to section mapping

| Type | Section |
|------|---------|
| `feature` | New Features |
| `flag-add` | Feature Flags > Added |
| `flag-remove` | Feature Flags > Removed |
| `devx` | DevX Enhancements |

### Step 1: Parse inputs

1. The argument after the mode is the **type**. Must be one of: `feature`, `flag-add`, `flag-remove`, `devx`.
2. Remaining text is the **description**.
3. If type is missing or invalid, ask: **"What type? (feature, flag-add, flag-remove, devx)"**
4. If description is missing, ask: **"What did you ship? Describe the demo item."**

### Step 2: Read and update the file

1. Read `Work/Weekly Demos.md`.
2. Find the most recent week section. Week sections use `## Week of YYYY-MM-DD` format (Monday date).
3. If no section exists for this week, calculate the Monday of the current week and create a new section **at the top**:
   ```markdown
   ## Week of YYYY-MM-DD

   ### New Features
   -

   ### Feature Flags
   #### Added
   -
   #### Removed
   -

   ### DevX Enhancements
   -
   ```
4. Append the description as a bullet under the mapped section.

### Step 3: Confirm

> Logged **[type]** demo for week of [date]: "[description]"

---

## Mode: `retro` → `Work/Retros.md`

Add a retrospective note to the current retro file.

### Step 1: Get the note

If an argument was provided, use it as the note text. Otherwise ask:
**"What's the retro note? I'll also need to know the category."**

### Step 2: Determine the category

Ask which category the note belongs to (if not obvious from context):

- **What went well** — positive outcomes, wins, things to keep doing
- **What could improve** — pain points, frustrations, inefficiencies
- **Action items** — concrete next steps or changes to make

If the note clearly fits one category (a complaint is "What could improve", a win is "What went
well"), assign it automatically and confirm.

### Step 3: Read and update the file

1. Read `Work/Retros.md`.
2. Find the most recent date section. Date sections use `## YYYY-MM-DD` format.
3. If no section exists for today's date, create a new one **at the top** with today's date and all three subsections:
   ```markdown
   ## YYYY-MM-DD

   ### What went well
   -

   ### What could improve
   -

   ### Action items
   -
   ```
4. Append the note as a bullet (`- Note text`) under the appropriate subsection.

### Step 4: Confirm

> Added to **[Category]** in retro for [date]: "[note text]"

---

## Examples

| Input | Result |
|---|---|
| `/log achievement Shipped the SpecKit Companion 1.0 release` | Bullet under `## 2026` → `### Q3` in `Work/Achievements.md`. |
| `/log activity Talk at GDG Austin on March 10, 45 attendees, https://…` | Row at the top of the `## Activities` table: Public Speaking, 2026-03-10, 45 Attendees, Advocu `No`. |
| `/log activity ~/Desktop/metrics.png` | Reads the screenshot, extracts type/title/date/platform/reach/link, asks about anything unclear, then writes the row. |
| `/log demo flag-remove Removed the legacy billing flag` | Bullet under `### Feature Flags` → `#### Removed` for the current week. |
| `/log retro Standups ran long every day this sprint` | Bullet under `### What could improve` for today's date. |
| `/log` | Asks which of the four to log. |

## Quality Checklist

- [ ] The mode was taken from the argument, not guessed from vibes.
- [ ] The record landed in the correct target file from the table at the top.
- [ ] Year / quarter / week / date section existed or was created with the exact structure shown.
- [ ] New sections were inserted **at the top**, not appended at the bottom.
- [ ] `activity`: the table row has all eight fields, `-` for unknowns, `Advocu: No`, and sits directly under the separator row.
- [ ] `demo`: the type was one of the four valid values and mapped to the right section.
- [ ] Nothing else in the file was reordered, reformatted, or edited.
- [ ] The confirmation line was printed.

## Tips

- **Never invent the payload.** If the description is thin, ask — these files feed the yearly review, Advocu submissions, and the weekly demo; a fabricated entry is worse than a missing one.
- **`log activity` is a table other tooling reads.** Keep the column set and the `-` placeholders intact so a later stats sync can find the rows it needs to update.
- **Newest first everywhere.** Year sections, week sections, date sections, and activity rows all lead with the most recent — don't append to the end of the file.
- A demo item is often also an achievement, and a talk is often both an activity and an achievement. Log each one where the user asked; offer the second only if it clearly belongs, and never write two records off one request without asking.
- Only add/append. Never rewrite existing bullets or rows to "tidy" them.
