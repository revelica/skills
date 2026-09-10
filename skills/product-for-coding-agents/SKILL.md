---
name: product-for-coding-agents
description: Use Revelica as the shared product context for coding work. Read the idea/spec, customer problem, bet and outcome before implementing; discover the current server workflow when writing a product spec; save agreed spec changes, implementation references and feasibility evidence for the team and future sessions. Use when planning or implementing product work connected to a Revelica workspace.
metadata:
  status: ready
  available-in: mcp
---

# Product for coding agents

Requires a connected Revelica MCP server exposing `query`, `read`, `create`, `update`, `list_skills` and `load_skill`.

Use Revelica to understand what to build and why, then keep that product context current as you learn through implementation. Continue using the user's engineering tools for code, tests and version control.

## Discover the current workflow

Call `list_skills` on the connected Revelica server to discover the workflows available to this user. Load the relevant workflow with `load_skill`, using the server's actual tool schema for arguments. Read any shared references it returns through that server's supported loading path.

For creating or revising a product spec, load **`write-product-spec`**. Follow its instructions for reusing the existing Idea and gathering only the context needed for the user's current task. If the workflow is unavailable, report that limitation; do not substitute an obsolete bundled spec workflow or invent its schema.

This package supplies orientation. The server supplies the current product workflows, schemas and workspace context. A loaded skill supplies instructions to the current agent; loading it does not by itself execute a Revelica playbook or DAG.

## Read before building

1. Find the relevant Idea with `query`, then read it and its linked context with `read`. Use the returned schemas and relationships to discover the spec, evidence and current state.
2. Read the associated value proposition and customer segment to understand the customer and job to be done. Read the hypothesis/bet and project outcome when present to understand the intended effect and what must be true.
3. Reuse existing workspace and project context. Ask only when missing information blocks the requested work. Do not invent a customer, product, outcome or measured baseline.

An **Idea is the product spec**. Its story map, structured document and Markdown are representations of the same spec. Preserve that identity when changing representation or implementing a release slice. Do not create competing specs simply because the user switches between a map and prose.

A **hypothesis is a bet**, connecting an opportunity, intended outcome, mechanism and, when selected, ideas. An Idea and a bet are distinct. Read their current relationships rather than treating an Idea as the bet itself.

## Write the results back

- Keep the existing spec current when the user agrees to a requirement change. Load `write-product-spec` for product-spec authoring and follow its persistence contract across representations.
- Record implementation references such as pull requests, releases or prototype previews using the live Idea schema. Include what was actually built and tested, and what remains incomplete.
- Capture feasibility assumptions and evidence revealed by implementation. Distinguish a proposed test, an observed result and an unsupported claim. Link evidence to its actual subject using the relationships supported by the server.
- Save useful sources and findings so later work can reuse them. For formal assumption tests, discover and load the relevant experiment workflow before collecting evidence; follow its saved protocol and reporting requirements.
- Preserve existing Ideas when implementing slices or revising the same solution. For a genuinely different solution, follow the product workflow's guidance on alternatives instead of silently overwriting the original.

Use `query` and `read` to obtain current schemas before writes. Do not assume field names, relationship fields, project scope or versioning behavior from an older package. Check write results for the persisted ID and version, and use returned references for follow-up work.

## Stay within the requested work

A prototype used to test an assumption is discovery work. Production implementation of an agreed spec slice is delivery work. State which one was built and what its evidence supports; a working prototype alone does not establish production readiness or customer value.

If the user asks for product discovery or bet framing, discover and load the appropriate server skill. Do not require a separate plugin copy of each workflow or assume an unavailable remote agent will execute it.

Before ending the session, save the agreed spec changes, implementation references and important findings. Tell the user what was saved and provide the available Revelica links so the team and the next session can continue from the same context.
