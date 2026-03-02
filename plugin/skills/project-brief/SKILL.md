---
name: project-brief
description: Generate a strategic brief for a Revelica project by synthesizing all available research artifacts
---

Generate a project brief for the Revelica project identified by $ARGUMENTS.

## Steps

### 1. Resolve the project

If $ARGUMENTS contains a project ID (UUID), use it directly.

If no project ID is provided, call `list_artifacts` with `limit=50` to discover available projects. Extract the unique `project_id` values from the results, then ask the user which project they want a brief for.

### 2. Fetch the project overview

Call `get_project_artifacts` with the project ID. This returns:
- `project` — name, goal, and outcome
- `artifacts_by_type` — a map of artifact type → list of `{id, name, created_at}`
- `artifacts_count` — total number of artifacts

If `artifacts_count` is 0, report that no research has been run for this project yet and stop.

### 3. Fetch artifact content

For each artifact type in `artifacts_by_type`, take the most recent artifact (first in the list) and call `get_artifact` with its ID to retrieve the full `json_content`.

Limit to **5 `get_artifact` calls total**. If there are more than 5 types, prioritize in this order:
1. `competitive_landscape`
2. `market_segments`
3. `interview_snapshot`
4. Any remaining types in alphabetical order

Make the `get_artifact` calls in parallel where possible.

### 4. Synthesize the brief

Produce the brief in this format:

---

# Project Brief: [project.name]

**Goal:** [project.goal or "Not specified"]
**Outcome:** [project.outcome or "Not specified"]

## Research Coverage

| Type | Artifacts | Latest |
|------|-----------|--------|
[one row per artifact type — use `artifacts_by_type` counts and most recent `created_at`]

## Key Findings

[One section per fetched artifact, using the artifact's name as the heading.
Read `json_content` — the structure varies by type, so extract whatever is meaningful:
summary, key points, findings, segments, competitors, themes, etc.
Present as concise bullet points. Do not dump raw JSON.]

## Gaps & Open Questions

[Note any of the following that apply:
- Artifact types with more than 1 artifact where older versions may contain different data
- Common research types not present (e.g. if no interview data exists, note it)
- Fields in `project.goal` or `project.outcome` that suggest unanswered questions
- Artifacts that were fetched but had empty or minimal `json_content`]

---

Keep the brief scannable. Prefer bullet points over prose. If a section has nothing meaningful to say, omit it.
