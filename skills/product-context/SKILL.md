---
name: product-context
description: REQUIRED orientation for any Revelica workspace session. Revelica is your team's shared memory for product work — ideas, bets, hypotheses, specs, and all research (customer, competitive, industry, technology). Load this to learn the access patterns (lookup/save/update), the catalog of workflow-specific skills, and sync-as-you-work expectations — which include checking Revelica before doing fresh web research, saving findings and sources from anything you fetch so future agents don't redo the work, capturing ideas as they come up, and keeping task/idea status current. Without this you'll re-derive what's already saved, re-fetch pages already researched, miss skills that apply, and leave no trace for the next agent or human.
compatibility: Requires a Revelica workspace (sign up at revelica.com) and the Revelica plugin which provides the MCP server with lookup, save, update, and load_skill tools.
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

# Product Context

## Why this matters to you

Your context resets between sessions. Everything you learn, derive, and decide disappears. But if you save it to Revelica, the next version of you starts with full context instead of a blank slate. The more you capture now, the more useful you are next time. **This is your long-term memory.**

When the user says "look up idea X in Revelica," you get back the hypothesis, all supporting and contradicting evidence, the activity log, connections to opportunities and segments, and the current status. That's hours of conversation compressed into one `lookup` call.

## What Revelica is

**Revelica is where your team's product work lives.** If Revelica is connected to your session, it's the team's source of truth for:

- **Ideas, bets, hypotheses, assumptions** — what the team is considering, committing to, and testing
- **Customer knowledge** — segments, interview snapshots, experience maps, opportunities
- **Competitive landscape** — companies, solutions, value propositions
- **Strategic context** — project goals, findings, evidence, strategy docs
- **Specs** — story maps, documents, and implementation plans attached to ideas
- **Tasks** — concrete work items under ideas, status-tracked

You're not a read-only consumer. When Revelica is connected, the team expects you to participate:

- **Orient before acting.** Check what exists before re-deriving it or doing web research. Answers and prior research are usually already saved.
- **Sync as you work.** When new information emerges — user mentions an idea, you find a competitor, you finish a task, you see evidence that supports or contradicts a hypothesis — record it in Revelica. Don't leave it in your chat window.
- **Act as a peer.** Other humans and agents are working in this workspace too. Your writes are their reads. Presence shows them what you're focused on. Treat the workspace like a shared desk, not a personal notebook.

This isn't optional. Agents who don't participate leave no trace and let the workspace drift out of sync with the actual work being done. Agents who do make the team meaningfully more effective.

## Session start

At the beginning of a session, or when the user mentions an idea, project, or area of work:

```
lookup(query="*", artifact_type="idea", depth="summary")
```

If results come back, briefly tell the user what's there: "There are 3 ideas in Revelica — 'Knowledge graph for evidence ingestion' (discovery, 5 evidence entries), 'MCP dogfooding' (backlog, 3 entries), 'Cursor marketplace listing' (backlog). Want to continue one of these?"

If no results and the user is clearly exploring a product idea, offer: "Want me to track this as an idea in Revelica? I can capture what we figure out so it's there next time."

## Tool surface

Three MCP tools cover almost everything:

- **`lookup(query, artifact_type?, depth?)`** — search. Returns the schema of the type plus matching resources. Default `depth="summary"`; pass `depth="full"` when you need whole content.
- **`save(artifact_type, name, content, parent_id?, project_id?)`** — create a new artifact or entity. Pass `parent_id` to create a new version of an existing artifact instead of a fresh one.
- **`update(artifact_id, updates, artifact_type?)`** — patch specific fields without a full rewrite.

Every `artifact_type` has a schema — call `lookup(query="*", artifact_type="<type>")` to see it before creating.

### Update patch operators

Use these instead of full-field replacement whenever possible:

| Shape | Effect |
|---|---|
| `{"field": value}` | Set the field (full replacement) |
| `{"field.0.nested": value}` | Target a specific nested path |
| `{"list.-": item}` | Append to a list |
| `{"field": null}` | Remove |
| `{"text.append": ["line 1", "line 2"]}` | Append lines to a long-text field (array joined with `\n`) |

### Array form on save for long text

For long text content (like `document.text`), prefer the array form:

```
save(artifact_type="document", name="...", content={
  "text": ["line 1", "line 2", "line 3"]
})
```

Server joins the array with newlines on receipt. Dramatically easier to generate correctly than one big escaped string. Use the same pattern for `text.append` on subsequent updates.

## Related skills — load when the trigger applies

Load these with `load_skill("<name>")` when the task calls for them. Each is a focused instruction set for a specific workflow:

- **write-spec** — commit a feature design to writing as a document attached to an idea (use when an idea moves from backlog → discovery, or before implementation starts)
- **interview-snapshot** — process a customer interview transcript into structured insights attached to a segment
- **story-map** — build or edit a story map (structured requirements doc) for an idea
- **map-competitive-landscape** — build a competitive landscape graph anchored on a value proposition
- **research-company-solution** — enrich a known company and its solutions via outside-in research
- **research-target-customer** — discover a new customer segment via market/customer research
- **find-and-research-competitors** — discover new competitors in a market and summarize them
- **brainstorm-ideas**, **refine-idea** — ideation skills that read workspace context to generate or sharpen ideas
- **data-mining** — pull quantitative evidence from connected analytics tools (e.g., PostHog)

If your task matches a trigger, load the skill before improvising. If no skill matches, use the lookup/save/update pattern directly — it covers everything.

## 1. Before asking the user, check the workspace

When the user asks you to build something, or when you need context to make a decision, look there first. Answers are often already saved.

```
lookup(query="*", artifact_type="customer-segment", depth="full")   # target customer, JTBD, use cases
lookup(query="*", artifact_type="value-proposition", depth="full")  # competitive positioning, differentiation
lookup(query="*", artifact_type="company", depth="full")            # competitors and own company
lookup(query="*", artifact_type="idea", depth="full")               # the hypotheses being bet on
lookup(query="*", artifact_type="opportunity", depth="full")        # customer pain points and unmet needs
lookup(query="*", artifact_type="hypothesis", depth="full")         # active bets with idea refs + impacts
```

Hypotheses read as "If we [idea_refs] then we'll move [impacts.key_result] assuming [assumptions] are true." That tells you WHY the thing you're building is expected to work. Evidence and assumptions attached show what supports or contradicts it. Use this to inform implementation decisions.

## 2. Work with requirements (story maps)

Story maps are structured requirements — activities, tasks, user stories, acceptance criteria — that the user sees in a graph UI while you work in JSON.

**Check if requirements already exist:**

```
lookup(query="*", artifact_type="story-map", depth="full")
```

If a story map exists, read the acceptance criteria before implementing. They're the spec.

**Create requirements to clarify scope:**

When planning implementation, create a story map to confirm your understanding with the user. The visual graph is much easier for them to review than a wall of text.

```
save(artifact_type="story-map", name="Onboarding flow", content={...})
```

Call `lookup(query="*", artifact_type="story-map")` first to get the schema.

**Update requirements as you go:**

```
update(artifact_id="<id>", artifact_type="story-map", updates={
  "activities.0.tasks.-": {"name": "Upload first document", "stories": [...]},
  "activities.1.tasks.2.acceptance_criteria": ["File appears in evidence list"]
})
```

## 3. Capture ideas as they come up

When the user says "what if we..." or you notice an opportunity during implementation, save it before it's lost:

```
save(artifact_type="idea", name="<short name>", content={
  "name": "<short name>",
  "description": "<what changes, for whom, why now>",
  "status": "backlog"
})
```

This keeps the user focused on current work while making sure good ideas don't evaporate. Ideas are cheap — a one-liner is fine. They get evaluated later.

**Keep ideas up to date as you work:**

Status values: `backlog | discovery | ready | delivery | launched | cancelled`. Log activity so the next person (or agent) has context:

```
update(artifact_id="<idea_id>", artifact_type="idea", updates={
  "status": "delivery",
  "activity.-": {
    "actor": "claude-code",
    "action": "status_changed",
    "summary": "Started implementation — story map created, first PR open."
  }
})
```

Valid `action` values: `created | evaluated | evidence_added | status_changed | comment`. Use `comment` for anything that isn't one of the named lifecycle actions (e.g., linking a PR, noting a blocker, recording a decision).

Link PRs, specs, or related ideas:

```
update(artifact_id="<idea_id>", artifact_type="idea", updates={
  "activity.-": {
    "actor": "claude-code",
    "action": "comment",
    "summary": "Edge table migration drafted at github.com/org/repo/pull/42."
  },
  "related_idea_ids.-": "<other_idea_id>"
})
```

### Testable claims → hypotheses (not just ideas)

**When a user makes a testable claim, save it as a `hypothesis` entity before discussing — not just as an idea.** A testable claim is any statement of the shape:

- "X will cause Y by Z amount" (quantitative: "tutorials will reduce churn by 20%")
- "If we do X then Y because Z" (causal: "if we add SSO, enterprise leads convert because IT gatekeepers sign off faster")

That's hypothesis-shaped, not idea-shaped. Hypotheses are project-scoped and structured around `idea_refs` + `impacts` + `assumption_ids`. Call `lookup(query="*", artifact_type="hypothesis")` once to see the full schema before creating. Typical flow:

1. If the claim references a new idea, `save(artifact_type="idea", ...)` first to get an idea_id
2. `save(artifact_type="hypothesis", ...)` referencing that idea_id in `idea_refs`, the relevant project's `project_id`, the KR being claimed in `impacts`, and any assumptions the claim depends on
3. THEN discuss with the user

Capture first, discuss second. A hypothesis is testable — that's its value; losing it to the chat window means losing the ability to test it.

## 4. Research loop — check first, save what you find

Product discovery work is constant: market research, customer research, technology research, industry news. It's also expensive (time, tokens, dev attention). The team and past agents have likely already researched some of what you're about to look up. **Always check Revelica before doing web research:**

```
lookup(query="<topic>", artifact_type="evidence-source", depth="full")
lookup(query="<topic>", artifact_type="evidence-finding", depth="full")
```

If what you need is already saved, use it and move on. If not, do the research — and save what you find so the next agent (or future you) doesn't redo it.

### Save what you fetch — immediately

**After any fetch of a URL, paper, or data, save before responding to the user.** The research was expensive; discarding it is the biggest single waste pattern. Don't just describe what you found in your response — save it as a persistent record first, then continue to the user's question. The user can wait two tool calls.

Two levels of save:

**`evidence-source`** — the raw thing you looked at:

```
save(artifact_type="evidence-source", name="<descriptive label>", content={
  "source_type": "url",
  "category": "<one of the five — see below>",
  "normalized_text": "<what you found>",
  "source_url": "<where you found it>"
})
```

**`evidence-finding`** — the actionable insight you extracted:

```
save(artifact_type="evidence-finding", name="<short label>", content={
  "evidence_source_id": "<source_id>",
  "title": "<one-line active observation>",
  "category": "<same as source>",
  "impact": "high|medium|low",
  "strategic_context": "<2-4 sentences: why this matters for current work>"
})
```

Findings are the scannable layer; sources are where drill-in goes. Link findings to hypotheses they support or contradict via the hypothesis's `evidence[]` array.

### Classify by domain (`category` field value — NOT an `artifact_type`)

The values below go in the **`category` field** inside the content payload of `evidence-source` and `evidence-finding`. They are **NOT** valid values for `artifact_type`. `artifact_type` is always either `evidence-source` or `evidence-finding`. Passing `artifact_type="competitive-landscape"` will fail with an unknown-type error.

- **`competitive-landscape`** — competitor products, pricing, features, market moves
- **`customer-research`** — interviews, reviews, social, analytics, surveys (both qualitative and quantitative)
- **`enabling-technology`** — research papers, API docs, emerging capabilities
- **`industry`** — market trends, regulation, analyst reports, thought leadership
- **`strategic-context`** — the company's own vision, strategy, OKRs, positioning

### Why this matters

Unsaved research is wasted research. Next session, future-you or another agent will re-fetch the same pages, re-read the same papers, re-derive the same conclusions. Every save you make shortcuts future work for the whole team — humans and agents both.

## Signal vs. noise — what's worth saving?

Lean toward capturing. The cost of a redundant record is tiny; the cost of a lost insight is real.

**Save:**

- Ideas the user says "what if we..." about, or opportunities you spot during implementation
- Testable claims — quantitative or causal statements — as hypothesis entities (see Section 3)
- Evidence: competitor approaches, libraries you considered, customer quotes from docs, technical constraints that affected a decision, market signals
- Status changes: when you finish a task, move an idea forward, or learn something that supports/refutes a hypothesis
- New entities: a competitor you hadn't seen before, a customer segment the user describes, a new solution being proposed
- Decisions: architectural choices, trade-offs — attach as an idea activity (`action: "comment"`) or as a finding

**Don't save:**

- Thinking-out-loud that didn't go anywhere
- Things already in the workspace (`lookup` first to check for duplicates)
- Repo conventions or code patterns — those belong in local agent memory, not Revelica
- Personal or ephemeral notes unrelated to the product

When in doubt, save. The worst case is a small cleanup later; the alternative is a lost insight and re-derivation next session.

## Tone

Don't interrupt the flow. When you capture something, mention it briefly — "added that as evidence on the knowledge graph idea" or "saved that as a hypothesis so we can track it" — and keep going. The user should feel like the system is quietly accumulating intelligence, not like they're filling out forms.

If you're unsure whether something is worth capturing, err toward capturing. Evidence is cheap, missing context is expensive.

## Before a context reset

If you sense the conversation is wrapping up and you've been working on an idea, do a final update:

1. Update the idea status if it's changed (to `discovery`, `ready`, `delivery`, or wherever the work landed)
2. Add a final activity entry summarizing what was accomplished — use `action: "comment"` or `action: "status_changed"` as appropriate
3. If new evidence accumulated, make sure it's linked via findings or the hypothesis's `evidence[]` array
4. Mention to the user what's saved: "The knowledge graph idea is in Revelica with 8 evidence entries and a chosen spec. Next session, just say 'look up the knowledge graph idea' and I'll have full context."
