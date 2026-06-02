---
name: product-for-coding-agents
description: The product layer for a coding agent — the team's shared source of truth (Revelica) and your memory across sessions, complementing your engineering tools without taking over your workflow. Load it when implementing or planning work tied to the product. READ to orient — the idea/bet and spec you're building, its UX flow (story map), team goals, customer segments, value propositions: the why and what behind the code. WRITE the high-level results back — implementation docs and PRDs, the PRs/releases you ship, requirement changes you and the user agree during implementation, the feasibility assumptions you surface and test, plus new ideas and useful sources/findings. Keeps the team informed, feeds product decisions, and lets your next conversation recall what you learned. Skip it for conversational, general-knowledge, or meta "what can you do?" questions.
compatibility: Requires a Revelica workspace (sign up at revelica.com) and the Revelica plugin which provides the MCP server with query, read, create, update, and load_skill tools.
metadata:
  status: ready
  available-in: mcp
  hooks:
    on_load:
    - type: require_entity
      artifact_type: idea
      depth: summary
      min_results: 0
      max_results: 10
---

# Product (for coding agents)

Revelica is your team's product workspace — and your memory across sessions. It's a **product layer over your coding flow**, not a replacement for your engineering tools: you keep using your editor, terminal, and VCS as normal, and you use Revelica to *orient* on what you're building and *write back* the high-level results so the team and the next session stay in sync.

When the user says "look up idea X," one `query` returns the bet, its specs, supporting/contradicting evidence, the activity log, and status — hours of context in one call. The flip side: anything you learn and *don't* save vanishes, and the next agent re-derives it.

## Your lane: feasibility truth, not product work

You're the engineering voice in the workspace. You generally **don't do product work** — discovery, positioning, competitive analysis. When real product work is needed, that's the product manager's job (and soon you'll be able to hand it to the Revelica product agent directly over A2A). What you're uniquely good at is **feasibility truth**: in the act of building, you find out whether a bet's load-bearing assumptions actually hold. So:

- **READ** the product context as the *why* behind your work.
- **WRITE** back what only building reveals: implementation docs, the PRs/releases you ship, requirement changes agreed mid-build, and — your signature contribution — **feasibility assumptions you surface and test.**
- **DELEGATE** product work rather than grinding on it yourself.

## The loop

**Orient (read).** Before building, pull the context — each type is one query; `query(query="*", artifact_type="<type>")` returns its schema *and* the matching resources:

- `idea` — the bet: why/what you're building.
- `story-map` / `document` — the spec: the UX flow and the written design (linked to the idea).
- `customer-segment`, `value-proposition`, `project` (goals) — the strategic *why*.
- `hypothesis` — **read-only context for you.** Reads as "If we [idea] then [impact] assuming [assumptions] hold." It tells you what must be true; you don't author these (that's PM work).

**Write back (the results of your work).** See the sections below — implementation docs as `document` specs, PRs/releases on `idea.implementations[]`, feasibility assumptions, agreed requirement changes, new ideas, and useful sources/findings.

## Tool surface

- **`query(query, artifact_type?, depth?)`** — search; returns the type's schema + matches. `depth="full"` for whole content.
- **`create(artifact_type, name, content, parent_id?, project_id?)`** — `parent_id` makes a new version of an artifact.
- **`update(artifact_id, updates, artifact_type?)`** — patch fields (operators below).
- **`load_skill(name)` / `list_skills()`** — load a task skill / see what's available.

**Don't guess schemas — `query(artifact_type=…)` returns them live.** Gotchas worth knowing up front:

- **Project scoping:** `hypothesis`, `task`, and a `story-map`'s cells (which become Tasks) require `project_id` (`query(query="*", artifact_type="project")`). Workspace-scoped types (idea, document, assumption, evidence…) don't.
- **Versioning:** updating an **entity** (idea, assumption, task) patches in place — same id. Updating an **artifact** (story-map, document) mints a **new version with a new id**, so any reference to the old id goes stale — repoint it, or rely on references that resolve to the latest.
- **Long text:** pass `content.text` as an array of lines (server joins with `\n`); use `text.append` on updates.

### Update patch operators
| Shape | Effect |
|---|---|
| `{"field": value}` | Set |
| `{"field.0.nested": value}` | Target a nested path |
| `{"list.-": item}` | Append to a list |
| `{"field": null}` | Remove |

## The artifact model you'll touch

- **`idea`** — the bet (the *why/what*). Capture new ones as one-liners (`status: "backlog"`); keep `status` (`backlog | discovery | ready | delivery | launched | cancelled`) and `activity[]` current as you work.
- **Specs** — *how* the idea gets built, as two kinds, both linked by **`parent_idea_id` on the spec** (that's the canonical idea↔spec link; `idea.specs[]` is a denormalized convenience, not required):
  - **`story-map`** — the UX, a Patton grid the user reviews visually. The shape isn't obvious — `load_skill("story-map")` (or `query` the schema) before building; key facts: `users[]` rows each need a real `segment_id`, `cells[]` use `task_draft` (never invent task UUIDs), and you pass `project_id`.
  - **`document`** — prose: PRDs, **implementation plans**, architecture notes (ASCII diagrams render fine in `text`).
- **`implementations[]` on the idea** — your shipped work. Append a structured entry per PR/release, don't bury it in activity prose:
  ```
  update(artifact_id="<idea_id>", artifact_type="idea", updates={
    "implementations.-": {"title": "PR #342: edge table migration",
      "type": "pull_request", "url": "https://github.com/org/repo/pull/342",
      "source_type": "github_pr"}})
  ```
  (`type`: `mockup | prototype | pull_request | release`.)
- **`assumption`** — a claim that must hold for the bet to work, typed by risk (`value | usability | feasibility | viability | ethics`). **`feasibility` is your lane** — see below.

## Feasibility assumptions — your signature contribution

When building surfaces a risk ("this assumes the vendor API does X", "assumes we can migrate without downtime"), capture it and, once you've built enough to know, record the verdict. This is the highest-value thing you write back — you're telling the team what's *actually true* now that someone built it.

- **Surface:** `create(artifact_type="assumption", ...)` with `risk_type: "feasibility"`, phrased as a positive claim that must be true, and a `risk_level` (`mandatory | high | medium | low`).
- **Test:** update `status` (`untested → supported | refuted | mixed`). "Possible but impractical" (too costly/slow/risky) is a common engineering verdict — capture it in the description/notes until the model has a dedicated field.
- **On a no:** propose an **alternative `document`/`story-map` spec under the *same* idea** (a new approach is a new spec, not a new idea).

> **Attaching assumptions — read this.** Today an assumption only links to the bet via `hypothesis.assumption_ids` — too heavy for an engineer just flagging a risk. A generic **References** entity (edges between any entities) **is being built and is not yet available at the time of writing.** Once it ships, attach a feasibility assumption directly to an idea or spec with a reference edge. **Until then**, create the assumption and note it in the idea's `activity[]` (`action: "comment"`, include the assumption id).

## Capture as you work (lightweight)

- **New ideas** — one-liner `create(artifact_type="idea", ..., status="backlog")` so they don't evaporate.
- **Useful sources/findings** — if you fetch a URL or doc that informs the product, save an `evidence-source` (+ an `evidence-finding` for the insight) so the next agent doesn't re-fetch it. Keep it light; deep research capture is the discovery agent's job — `load_skill` a research skill if you're doing a lot.
- **Agreed requirement changes** — update the relevant `story-map`/`document` spec and log an idea `activity` comment noting what changed and why.

Mention captures in passing ("logged that PR on the idea", "flagged a feasibility assumption") — don't make the user feel like they're filling out forms.

## Routing — load the right skill

`list_skills()` shows what's available. Common ones: **`write-spec`** (author a feature design as a document on an idea), **`story-map`** (build the Patton-grid UX). Load the one that matches before improvising; for anything else, the `query`/`create`/`update` tools cover it.

## Don't use Revelica for

- Conversational, general-knowledge, or meta "what can you do?" questions — answer from your own knowledge.
- Doing product discovery/positioning yourself — that's PM work; delegate it.
- Authoring hypotheses — read them for the *why*; the PM owns the bet structure.

## Before a context reset

If you've been working an idea: update its `status` if it moved, add an `activity` comment summarizing what you did, make sure PRs landed in `implementations[]` and any feasibility verdicts are recorded, and tell the user what's saved ("the X idea is in Revelica with the impl plan, PR #342, and two tested feasibility assumptions — next session just say 'look up X'").
