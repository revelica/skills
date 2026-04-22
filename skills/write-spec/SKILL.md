---
name: write-spec
description: Author a feature spec attached to an idea, following the Revelica spec template. Walks the agent through gathering context, drafting a markdown document section by section, and attaching it to the parent idea via IdeaSpec. Designed for incremental writes that stay within tool-call generation budgets across coding-agent harnesses.
metadata:
  tools: query read create update
  status: ready
  available-in: mcp
  outputs:
  - document
---

# Write Spec

Write a feature spec for an idea. The spec is a markdown document with a fixed section structure that lets fresh agents (and humans) skim, understand, and act without re-deriving the reasoning. The output is a `document` artifact attached to the parent idea via `IdeaSpec`.

**Use this when:** the user (or you) decided to commit a design to writing for an idea — typically because the idea is moving from `backlog` to `discovery`, or because there's enough thinking to capture before implementation starts. Don't use this for tiny one-line ideas; the format expects there to be something worth saying in each section.

**The format's contract:** every entry in the **Decisions log** MUST include a one-line `**Why:**` rationale. Future readers (you in two months, another agent picking up the work) read the Decisions section first to know what NOT to re-litigate. Without the Why lines, decisions are unmotivated assertions and the spec loses its most valuable property.

**Per-call size budget:** keep each save/update call to ~1-3KB of body content. Don't try to write the whole spec in one save. The skill walks you through this section by section so each call stays small and a partial failure only loses the in-flight section.

## Step 1: Gather context

Look up everything you'll need before you start writing. The goal is to know what already exists so the spec can reference it instead of re-deriving it.

1. **The parent idea.** This skill operates on a specific idea — find it.

   ```
   query(query="<idea name or topic>", artifact_type="idea", depth="full")
   ```

   If the idea was passed via canvas context, use that ID. If multiple ideas match the query, ask the user which one before proceeding.

2. **Project goals.** The Why and Goals sections should reference what the idea is trying to achieve in the project.

   ```
   query(query="<project name or relevant terms>", artifact_type="objective", depth="full")
   ```

   (Note: project / objective lookup may return nothing today if the MCP project graph isn't yet exposed. If so, fall back to asking the user for the project's objectives in their own words.)

3. **Related ideas and existing work.** Anything in `idea.related_idea_ids` is worth fetching. Also look up entities the design will touch — solutions, customer segments, value propositions, hypotheses — so the Current state section can cite them.

   ```
   query(query="<area>", artifact_type="solution", depth="summary")
   query(query="<area>", artifact_type="hypothesis", depth="summary")
   ```

4. **The document schema.** Confirm what shape `document` content takes.

   ```
   query(query="*", artifact_type="document", depth="summary")
   ```

   You'll see the content is `{text: <markdown string>, format: "markdown"}`. The `text` field accepts either a single string OR an array of strings (lines), which the server joins with newlines on receipt. **Always prefer the array form for long content** — each list element is a short normal string with no embedded newlines, which is dramatically friendlier to generate correctly than one giant escaped string.

5. **The canonical example.** If you've never written a spec in this format before, read the Event-driven skill triggers spec for reference:

   ```
   query(query="event-driven skill triggers", artifact_type="document", depth="full")
   ```

## Step 2: Save the initial document

Start with a tiny document that has just the title and status block. Use the array form for `text`.

```
create(
  artifact_type="document",
  name="<idea name> spec",
  content={
    "text": [
      "# <Spec title>",
      "",
      "**Status:** draft",
      "**Updated:** <today's date YYYY-MM-DD>",
      "**Owners:** @<username>",
      "**Related:**",
      "- <relevant existing idea, spec, or code path>",
      "",
      "> <One-paragraph summary. Read in 15 seconds, decide whether to read the rest.>"
    ]
  }
)
```

Note the document `id` from the response — call it `spec_id` below. You'll need it for every subsequent update call.

## Step 3: Append each section in order

For each section in the template, append via `text.append`:

```
update(artifact_id=<spec_id>, updates={
  "text.append": [
    "",
    "## <Section name>",
    "",
    "<paragraph or bulleted content>",
    ...
  ]
})
```

The append operator concatenates the joined array onto the end of the existing text. Each call should write **one section**. Don't batch. Keeping calls bounded is the whole point — if any single call fails, you only lose that section, not the whole spec.

The sections, in order:

### Why

Write this as **prose, not bullets**. One short paragraph (or two if needed) explaining what problem this solves, who hurts without it, and what the world looks like if it exists. This is the spec's north star — every other section serves it.

If you find yourself writing bullets here, stop and rewrite as a paragraph. The Why section is the place where the *story* of the work lives, and stories aren't bullet-shaped.

### Goals

Bulleted, observable. Each goal is checkable: "When this is done, X will be true." Avoid aspirational language ("better UX") — be concrete ("the cold-start chain runs without manual user clicks").

3-8 goals is the right range. Fewer means the work is too small for a spec; more means you're conflating things.

### Non-goals

Bulleted. "This spec is not about Y." Be **specific** — vague non-goals don't defend against scope creep. Each non-goal should rule out a real possible expansion of scope that someone might propose.

This section is more important than it looks. Writing it forces you to commit to what you're NOT doing, which anchors every decision downstream.

### Constraints (optional)

Bulleted. Things that must remain true that you DON'T get to change. Examples: "Multi-machine deployment," "Stateless HTTP transport," "Existing audit log must keep working."

**Note:** constraints are *given from outside* (existing systems, immovable user preferences, technical limits). Decisions are *chosen from within* (we considered alternatives and picked one). If you find yourself debating whether something is a constraint or a decision, it's almost certainly a decision — move it to the Decisions log.

Skip this section if there are no real constraints to call out.

### Current state

What exists today, with file:line references where useful. The goal is to let a fresh reader skip the grep phase. Cite specific files, function names, table names. Be honest about what doesn't exist yet — a "Doesn't exist yet" subsection is often more important than the "Already exists" one because it's where the work is.

**Important caveat:** anything you cite here is your best understanding at write time. A reader picking the spec up later should verify file paths and line numbers before acting on them. The format doesn't enforce verification — it's a writing discipline. Note this in the section if the spec is going to sit for a while before being implemented.

### How we got here (optional)

**Narrative prose paragraphs.** This is the section that captures the *story* of how you arrived at the chosen design — what you tried first, what you ruled out, what made the answer obvious. **Don't bullet this.** Write it as a flowing narrative.

This section is what makes the spec readable to fresh agents. The Decisions log captures *what* was chosen; this section captures *how* you got to those choices. It's the part of a spec that's hardest to capture in any other shape — the thinking-evolution prose that doesn't fit in bullet lists or typed nodes.

Skip for very small specs where the design is obvious. Include for anything where the reasoning matters more than the outcome.

### Design

How the proposed solution actually works. Subsections per major piece (use `### Subsection name`). Mix prose and structure freely — code blocks for data shapes, ASCII or mermaid diagrams for flows, tables for comparisons, prose for explanation.

Decisions made in the Design section should ALSO appear in the Decisions log (with rationale) so they're queryable separately. Design is the explanation; the log is the index.

If this section gets very long (5+ subsystems with deep detail), consider splitting it into linked sub-documents. For most specs, inline subsections under one Design section is fine.

### Plan

Numbered, ordered steps. Each step:
- Small enough to finish in one focused work session (~half day)
- References the files to create or modify
- Has a clear acceptance criterion

Format:

```
- [ ] **1. <Step name>**
  - Files: `<paths>`
  - Acceptance: <how we know it's done>
```

**Note:** the Plan section maps directly to task records that get attached to the idea via `idea_id`. After saving the spec, you (or the user) may want to walk the Plan and create one task per step using `create(artifact_type='task', ...)`. That's not part of this skill but it's the natural follow-up.

### Open questions

Things to resolve before or during build. Each entry tagged with what work it blocks, so questions don't get lost.

```
- [ ] **Q:** <question>
  - **Blocking:** <which step or piece of work this gates>
  - **Notes:** <any relevant context>
```

Drains as the spec matures. An empty Open questions section is a good sign — it means the design is ready to act on. A long one means the spec is still in discovery.

### Decisions log

**This is the most important section. Read this carefully.**

Format:

```
- **<Short decision name>.** <What was decided.> **Why:** <one-line rationale>.
```

The format's contract: **every entry MUST have a `**Why:**` line.** No exceptions. Future readers read this section first to understand what's locked in. Without the Why lines, decisions are unmotivated assertions that get re-litigated by the next person who picks up the work.

Capture both product decisions ("we're targeting cold-start as the demo flow") and technical decisions ("Postgres LISTEN/NOTIFY for backend dispatch instead of Realtime subscription"). Same shape for both. The Why line is the difference between a useful spec and a useless one.

If you catch yourself writing a decision without a Why, stop. Either figure out the rationale, or it's not actually a decision — it's a placeholder.

### Alternatives considered

Approaches you looked at and rejected. Each entry: name, verdict, one-paragraph reason. Prevents future rediscovery and re-rejection.

```
- **<Alternative name>.** Rejected/Deferred/Parked. <One-paragraph reason.>
```

This is the *negative space* of the design. Just as important as Decisions for fresh readers — it tells them what was already considered and why it didn't work, so they don't waste time re-evaluating.

### References

Links to related specs, code paths, external docs, conversation pointers. Optional — inline links elsewhere in the spec are fine if you don't need a separate roll-up.

## Step 4: Attach the spec to the parent idea via IdeaSpec

After all sections are written, attach the document to the idea by appending an entry to the idea's `specs` list:

```
update(
  artifact_id=<idea_id>,
  artifact_type="idea",
  updates={
    "specs.-": {
      "title": "<spec title>",
      "deliverable_id": "<spec_id>",
      "deliverable_type": "document",
      "is_chosen": true
    }
  }
)
```

`is_chosen=true` marks this as THE spec for the idea. If the idea has multiple competing specs, only one should be `is_chosen` at a time — the others stay as alternatives. If you're writing a competing spec rather than the chosen one, set `is_chosen=false` and don't unset other entries.

## Step 5: Log activity on the idea

Append an activity entry so the idea's audit trail records who created the spec:

```
update(
  artifact_id=<idea_id>,
  artifact_type="idea",
  updates={
    "activity.-": {
      "actor": "<your agent identity, e.g. claude-code>",
      "action": "created",
      "summary": "Drafted feature spec via write-spec skill."
    }
  }
)
```

## Step 6: Wrap up

Summarize for the user, conversationally:

- The spec ID and title
- The idea it's attached to
- A 1-2 sentence summary of the design (the elevator pitch from the Why section is fine)
- Any open questions you captured and what they block
- Suggested next steps:
  - The user reviews the spec and edits anything they disagree with
  - Walk the Plan section and create task records (one per step) attached to the idea
  - Move the idea from `backlog` to `discovery` if the design is solid enough to invest more in

## Fallbacks if tool capabilities aren't live yet

This skill assumes two tool capabilities that may not be live in every environment:

1. **Array form for string content fields.** `content={text: ["line 1", "line 2"]}`. If a save call returns a validation error about list-vs-string, fall back to passing `text` as a single string with `\n` between lines. The output is identical; only the input shape changes. Less friendly to less capable models, but functionally equivalent.

2. **`text.append` operator on update.** `updates={"text.append": [...]}`. If an update call returns a validation error about an unknown path operator, fall back to: (a) `query` the current document text, (b) concatenate the new section onto it, (c) `update` with the full new text. This works but each call grows in size as the spec lengthens, and the final call is just as big as a one-shot save. Still better than failing — the user can always read the partial spec from the document.

Both fallbacks let the skill still produce correct output when the new capabilities aren't yet live. See the "Incremental spec authoring via MCP" idea for the work to land them properly.

## Quality checks before declaring the spec done

Before wrapping up, walk through these and fix any that fail:

- [ ] Every entry in Decisions log has a `**Why:**` line. (If not, either add the rationale or remove the entry.)
- [ ] Non-goals is non-empty and specific. (If empty, write at least 2-3 things you're explicitly NOT doing. If vague, sharpen.)
- [ ] Plan items each have files and an acceptance criterion. (If missing, the step isn't well-defined enough to be a task.)
- [ ] Open questions each have a `Blocking:` tag. (If untagged, decide whether they're blocking anything or just future-thinking.)
- [ ] Alternatives considered has at least the major rejected approaches. (If empty, you probably haven't really considered alternatives — go back and think about what you didn't pick and why.)
- [ ] How we got here is prose, not bullets. (If bullets, rewrite as narrative. If skipped, that's fine for small specs.)
- [ ] The spec is self-contained — a fresh reader could pick it up and act without needing the original conversation. (If not, what's missing?)

If any check fails, do another `text.append` to add the missing content rather than trying to edit in place.
