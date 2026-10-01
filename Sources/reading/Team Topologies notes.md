---
type: book-notes
lifespan: durable
description: Team Topologies explains why Worky's three front-end teams should not share one calendar component; the interaction mode matters more than the code reuse
tags: [reading, teams, architecture]
---

# Team Topologies notes

> [!note] Choose the interaction mode first, then the code you share.
> A shared component forces two teams into collaboration mode for its whole life. Sharing an API keeps them in the cheaper X-as-a-Service mode.

> [!quote]
> The shape of the teams becomes the shape of the software, whether you plan for it or not.

The book names four team types (stream-aligned, enabling, complicated-subsystem, platform) and three ways they interact (collaboration, X-as-a-Service, facilitating). Most pain comes from teams stuck in collaboration mode with no end date.

## What it changes at Worky

- The three front-end teams are stream-aligned; Core Services is closer to a platform team.
- A shared calendar in the Infra library would put all three front-ends in permanent collaboration with Infra. That is the strongest argument for option one in [[One calendar or three]].
- The `scheduling` API is the X-as-a-Service boundary the [[Crew Scheduling Design]] is already drawing.

The quote above is my paraphrase of the book's argument, not a line from it.
