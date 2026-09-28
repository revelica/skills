---
name: use-revelica
description: Do product work in a connected Revelica workspace. Use when the user wants to work toward a product goal (what to do next, planning the work, reviewing progress, weighing several bets), frame a bet, describe the business, set a project goal, write a spec, design an assumption test, or ask what the workspace knows about customers, competitors, bets or specs. Routes to the right skill on the Revelica server.
---

# Use Revelica

This bundled skill routes a product task to the connected Revelica MCP server. The server owns the workflow instructions, schemas and workspace data. This file holds no workflow of its own.

1. Find Revelica's `load_skill`, `list_skills`, `query`, `read`, `create` and `update` tools. If the server is missing or needs authorization, use the host's normal connection flow or tell the user what is missing.
2. If the host showed you the Revelica server's instructions, follow them to pick the skill. They are the current routing. Otherwise pick by the job:
   - Product work toward a goal (what to do next, planning the work, reviewing progress, several bets): `drive-product-outcome`. This is the default when the job is broad or unclear.
   - Frame one bet and find its assumptions: `frame-bet`.
   - Describe the business (company, product, customer, value proposition): `model-your-business`.
   - Set a project's goal and key results: `setup-project-outcome`.
   - Write a spec and user flow for an idea: `write-product-spec`.
   - Design a test for an assumption: `design-experiment`.
   - Build or plan code for product work: `product-for-coding-agents`.
   - Answer a question about what the workspace knows: `query` and `read` directly, or `explore-graph` for how things connect.
   - Anything else: call `list_skills` and choose by description.
3. Call `load_skill` with that name, following the tool's actual argument schema. Pass `project_id` or `context_entities` when you already have them from earlier tool results. Follow the loaded skill in this conversation, using the records it prefetched and `read` for any content it did not include.
4. Reuse what the workspace and this conversation already hold. Ask the user only for what blocks the task: when a skill says to ask, ask in chat and wait for the answer. Use only ids returned by tools. Do not invent missing product facts, and do not substitute a stale local workflow when a server skill is unavailable. Report the gap instead.

Loading a skill gives you instructions to carry out with the available tools. It does not start a server-side playbook, and nothing runs on its own.
