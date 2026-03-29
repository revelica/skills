---
name: product-context
description: Get product context fast — look up ideas, evidence, customer segments, and competitive landscape from the Revelica workspace instead of re-deriving them. Optionally save findings as you go so the next session (or agent) picks up where you left off. Not for repo conventions or code patterns — those belong in local memory.
compatibility: Requires a Revelica workspace (sign up at revelica.com) and the Revelica plugin which provides the MCP server with lookup, save, and update tools.
---

# Product Context

You have access to a persistent knowledge graph via the `lookup`, `save`, and `update` tools. Use it to accumulate context across sessions — not as a separate task, but woven into the conversation.

## Why this matters to you

Your context resets between sessions. Everything you learn, derive, and decide disappears. But if you save it to Revelica, the next version of you starts with full context instead of a blank slate.

When the user says "look up idea X in Revelica," you get back the hypothesis, all supporting and contradicting evidence, the activity log, connections to opportunities and segments, and the current status. That's hours of conversation compressed into one `lookup` call.

The more you capture now, the more useful you are next time. This is your long-term memory.

## Session start

At the beginning of a session, or when the user mentions an idea, project, or area of work:

```
lookup(query="*", artifact_type="idea", depth="summary")
```

If results come back, tell the user what's there: "There are 3 ideas in Revelica — 'Knowledge graph for evidence ingestion' (exploring, 5 evidence entries), 'MCP dogfooding' (evaluating, 3 entries), 'Cursor marketplace listing' (proposed). Want to continue one of these?"

If no results and the user is clearly exploring a product idea, ask: "Want me to track this as an idea in Revelica? I can capture what we figure out so it's there next time."

## What to capture and when

### Ideas

Create when the user articulates a hypothesis, proposes a solution approach, or says "what if we...":

```
save(artifact_type="idea", name="<short name>", content={
  "name": "<short name>",
  "hypothesis": "If we [action], then [outcome] because [reason].",
  "status": "proposed"
})
```

The hypothesis can start rough. Update it as the thinking sharpens.

### Evidence

Add evidence as it emerges during the conversation — don't batch it up at the end.

**When the user shares a source (URL, doc, repo, spec):**
```
update(artifact_id="<idea_id>", artifact_type="idea", updates={
  "evidence.-": {
    "added_by": "claude-code",
    "type": "technology_signal",
    "summary": "docling-graph converter is domain-agnostic, ~1500 lines, pydantic + networkx only",
    "supports": true,
    "source_url": "https://github.com/docling-project/docling-graph"
  }
})
```

**When you derive a finding from analysis:**
```
update(artifact_id="<idea_id>", artifact_type="idea", updates={
  "evidence.-": {
    "added_by": "claude-code",
    "type": "agent_assessment",
    "summary": "Domain-typed edges (COMPETES_WITH, BLOCKED_BY) are more queryable than generic scientific labels (SUPPORTS, CONTRADICTS)",
    "supports": true
  }
})
```

**When an approach is rejected:**
```
update(artifact_id="<idea_id>", artifact_type="idea", updates={
  "evidence.-": {
    "added_by": "claude-code",
    "type": "agent_assessment",
    "summary": "Flat taxonomy with static mapping drifts from data model — agent has to guess",
    "supports": false
  }
})
```

**When a blocker is discovered:**
```
update(artifact_id="<idea_id>", artifact_type="idea", updates={
  "evidence.-": {
    "added_by": "claude-code",
    "type": "technology_signal",
    "summary": "Local MCP auth blocked — local Supabase doesn't expose OAuth authorization server endpoint. Requires ES256 migration.",
    "supports": false,
    "source_url": "insights/specs/postgres/supabase_es256_migration.md"
  }
})
```

### Evidence types

Use the type that best describes where the evidence came from:

| Type | When to use |
|---|---|
| `customer_quote` | Direct quote from a user or interview |
| `competitive_insight` | Something learned about a competitor |
| `market_signal` | Market trend, adoption data, industry shift |
| `usage_data` | Product analytics, metrics, behavioral data |
| `technology_signal` | Library, framework, API, emerging tech capability |
| `test_result` | Outcome of an experiment or prototype |
| `agent_assessment` | Your own analysis or derived finding |

### Activity

Log significant actions — not every message, just milestones:

```
update(artifact_id="<idea_id>", artifact_type="idea", updates={
  "activity.-": {
    "actor": "claude-code",
    "action": "evidence_added",
    "summary": "Explored docling-graph as graph conversion layer. Viable — domain-agnostic, lightweight deps."
  }
})
```

Use `action` values: `created`, `evaluated`, `evidence_added`, `status_changed`, `prototype_started`, `prototype_updated`, `test_completed`, `reference_added`, `comment`.

### Connections

When you discover relationships to other entities, add them:

```
update(artifact_id="<idea_id>", artifact_type="idea", updates={
  "opportunity_ids.-": "<opportunity_uuid>",
  "related_idea_ids.-": "<other_idea_uuid>"
})
```

Look up opportunities and other ideas first to get their IDs:
```
lookup(query="context lost across sessions", artifact_type="opportunity")
lookup(query="knowledge graph", artifact_type="idea")
```

### Status transitions

Move status deliberately, not automatically:

| Status | Meaning | Move here when |
|---|---|---|
| `proposed` | Just an idea | User articulates a hypothesis |
| `evaluating` | Gathering evidence | You start looking up data, analyzing approaches |
| `ready` | Evidence sufficient | Impact/confidence scored, recommendation made |
| `in_progress` | Being built | User starts implementing |
| `validating` | Testing with customers | Running experiments or simulations |
| `promoted` | Hypothesis confirmed | Evidence overwhelmingly supports it |
| `killed` | Hypothesis invalidated | Evidence contradicts it — set `kill_reason` |
| `parked` | Deprioritized | Not dead, just not now |

## Lookup is your superpower

You can query the full workspace to build context fast:

```
lookup(query="*", artifact_type="idea", depth="full")           # all ideas with full content
lookup(query="*", artifact_type="customer-segment", depth="summary")  # who are the customers
lookup(query="*", artifact_type="value-proposition", depth="full")    # competitive positioning
lookup(query="Acme Corp", artifact_type="company", depth="full")      # specific company
lookup(query="onboarding", category="qualitative")                    # customer research evidence
```

When the user asks about a topic, check what already exists before starting from scratch. The workspace might already have the answer.

## Tone

Don't interrupt the flow. When you capture something, mention it briefly — "added that as evidence on the knowledge graph idea" — and keep going. The user should feel like the system is quietly accumulating intelligence, not like they're filling out forms.

If you're unsure whether something is worth capturing, err toward capturing. Evidence is cheap, missing context is expensive.

## Before a context reset

If you sense the conversation is wrapping up and you've been working on an idea, do a final update:

1. Update the idea status if it's changed
2. Add a final activity entry summarizing what was accomplished
3. Score impact/confidence if you have enough evidence
4. Mention to the user what's saved: "The knowledge graph idea is in Revelica with 8 evidence entries. Next session, just say 'look up the knowledge graph idea' and I'll have full context."
