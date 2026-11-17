---
name: implement-spec
description: "Gives a coding agent a spec's context and records what shipped. Use before and while building. Picks up the spec's release, stories, acceptance criteria and the decisions and research behind them. While building, records feasibility and effort, tradeoffs, new ideas and what shipped. When the request turns out to be product work rather than code, switch to the matching skill."
compatibility: "Requires the Revelica MCP server, connected and signed in, and a Revelica workspace. Revelica doesn't work until setup-revelica has run: it's a mandatory part of workspace onboarding."
---

Help me build this feature. Read its spec, the release and stories in scope, their acceptance criteria, and the decisions and research behind them, then build it and write back what we learn.

This skill lives on the Revelica server, so the workflow and the workspace data it starts from are always current. Call the Revelica `load_skill` tool with `implement-spec` and follow what it returns.
