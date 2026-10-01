---
type: dashboard
project: worky
lifespan: project
description: "Live Dataview tables over the Worky notes: stories by status, open decisions, latest updates and meetings, what changed this week"
cssclasses:
  - dashboard
tags: [worky, dashboard]
---

# Worky dashboard

Live tables over the notes in [[Worky]]. Nothing here is typed by hand; it reads the frontmatter.

## Stories by status

```dataview
TABLE WITHOUT ID "<span class=\"status-chip status-" + lower(replace(key, " ", "-")) + "\">" + key + "</span>" AS Status, length(rows) AS Stories, rows.file.link AS Notes
FROM "Projects/Worky/product/crew-scheduling/stories"
WHERE type = "story"
GROUP BY status
SORT status ASC
```

## Open decisions

```dataview
TABLE WITHOUT ID file.link AS Decision, "<span class=\"status-chip status-" + lower(replace(status, " ", "-")) + "\">" + status + "</span>" AS Status, "<span class=\"dv-date\">" + dateformat(expires, "d MMM yyyy") + "</span>" AS Expires, expires - date(today) AS "Time left"
FROM "Projects/Worky/decisions"
WHERE type = "decision-doc" AND status = "open"
SORT expires ASC
```

## Latest updates and meetings

```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, description AS About, "<span class=\"dv-date\">" + dateformat(date, "d MMM yyyy") + "</span>" AS Date
FROM "Projects/Worky/updates" OR "Projects/Worky/meetings"
WHERE (type = "update" OR type = "meeting") AND date
SORT date DESC
LIMIT 5
```

## Changed this week

```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, file.mtime AS Changed
FROM "Projects/Worky"
WHERE file.mtime >= date(today) - dur(7 days) AND file.name != this.file.name
SORT file.mtime DESC
LIMIT 10
```
