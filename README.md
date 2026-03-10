# Revelica Skills

Official Revelica plugin for AI coding tools — provides MCP-connected skills for
product intelligence. Follows the [Agent Skills open standard](https://agentskills.io/specification),
compatible with Claude Code, Cursor, Gemini CLI, OpenAI Codex, and more.

## Repository Structure

```
revelica/skills
├── .claude-plugin/
│   ├── marketplace.json         # Claude Code marketplace catalog
│   ├── plugin.json              # Claude Code plugin manifest
│   └── mcp.json                 # MCP config for Claude Code plugin (no mcpServers wrapper)
├── .cursor-plugin/
│   └── plugin.json              # Cursor plugin manifest
├── agents/
│   └── AGENTS.md                # Fallback bundle for tools without a plugin system
├── skills/                      # Skill definitions (Agent Skills open standard)
│   └── project-brief/
│       └── SKILL.md             # Model-invoked when user asks for a project brief
├── .mcp.json                    # MCP config for Cursor/Gemini (mcpServers wrapper format)
└── gemini-extension.json        # Gemini CLI extension manifest
```

## Installation by Platform

### Claude Code

```
/plugin marketplace add revelica/skills
/plugin install revelica@revelica
```

Skills are **model-invoked** — Claude automatically uses them based on context. Ask Claude
to generate a project brief and it will use the skill. The MCP server is registered automatically.

### Cursor

Install via the `.cursor-plugin/plugin.json` manifest. Cursor will discover skills from
the `skills/` directory and connect to the MCP server via `.mcp.json` automatically.

### Gemini CLI

```
gemini extensions install revelica/skills
```

The `gemini-extension.json` manifest registers both skills and the MCP server.

### Other tools (Codex, raw API, etc.)

See `agents/AGENTS.md` for a self-contained skill bundle you can paste into your
agent's context. Configure the MCP server separately:

```
URL:  https://scryfast-development.fly.dev/mcp
Auth: OAuth 2.1 (browser flow on first use)

Transport type varies by client:
  Claude Code:  "type": "http"
  Cursor:       "type": "streamable-http"
  Gemini CLI:   "url" only (auto-detects)
```

## How It Works

### Claude Code install flow (one-time per user)

```
User: /plugin marketplace add revelica/skills
  └─ Claude Code clones this repo
        └─ reads .claude-plugin/marketplace.json
              └─ source: "./" → repo root is the plugin root

User: /plugin install revelica@revelica
  └─ Claude Code reads .claude-plugin/plugin.json
        ├─ auto-discovers skills/ → loads SKILL.md files into Claude's context
        └─ reads mcpServers: "./.claude-plugin/mcp.json"
              └─ registers MCP server (type: "http", OAuth 2.1)
```

### Runtime flow (per skill invocation)

```
User: "can you generate a project brief for my Revelica project?"
  │
  ├─ Claude recognises intent → loads skills/project-brief/SKILL.md
  │
  ├─ Claude Code: POST /mcp → 401 + OAuth metadata
  │     └─ OAuth flow: browser → Supabase → /auth/consent → JWT
  │
  └─ Claude follows SKILL.md instructions:
        │
        ├─ MCP tool: get_project_artifacts(project_id)
        │     └─ POST /mcp → MCP server → Supabase (RLS enforced)
        │
        ├─ MCP tools (parallel): get_artifact(id) × up to 5
        │
        └─ Claude synthesizes and returns the project brief
```

### Transport

The backend exposes one transport:
- `POST /mcp` — Streamable HTTP (all MCP clients; transport type key varies by client, see above)

## Skill Format

Skills follow the [Agent Skills open standard](https://agentskills.io/specification).
Each skill is a folder under `skills/` containing a `SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: One-line description of what the skill does — used by Claude to decide when to invoke it.
version: 1.0.0
---

## When This Skill Applies

Use this skill when the user asks to:
- [trigger condition 1]
- [trigger condition 2]

## Overview

Brief description of what the skill does.

## Steps

Step-by-step instructions for Claude to follow...
```

Skills are **model-invoked**: Claude reads the `description` and "When This Skill Applies"
section to decide when to use the skill. There is no user-facing slash command.

## Adding a New Skill

1. Create a folder under `skills/`:
   ```bash
   mkdir skills/my-skill
   touch skills/my-skill/SKILL.md
   ```

2. Write `SKILL.md` with frontmatter, trigger conditions, and instructions:
   ```markdown
   ---
   name: my-skill
   description: What this skill does — Claude uses this to decide when to invoke it.
   version: 1.0.0
   ---

   ## When This Skill Applies

   Use this skill when the user asks to:
   - [describe trigger conditions clearly]

   ## Steps

   Step-by-step instructions for Claude to follow.
   ```

3. Add the skill to `agents/AGENTS.md` for cross-platform fallback support.

4. Commit and push. Users get the update by running:
   ```
   /plugin marketplace update revelica
   /plugin update revelica@revelica
   ```

No backend changes are needed unless the skill requires a new MCP tool.

## Plugin File Formats

### `.claude-plugin/plugin.json`

```json
{
  "name": "revelica",
  "description": "Revelica MCP tools and skills for product intelligence",
  "version": "1.2.0",
  "mcpServers": "./.claude-plugin/mcp.json"
}
```

Skills are auto-discovered from the `skills/` directory — no explicit listing needed.
`mcpServers` must be explicitly declared; Claude Code does not auto-discover `.mcp.json`.

### `.claude-plugin/mcp.json` (Claude Code plugin format)

```json
{
  "revelica": {
    "type": "http",
    "url": "https://scryfast-development.fly.dev/mcp"
  }
}
```

Server name is the top-level key — **no `mcpServers` wrapper**. This is the format
required when referenced from `plugin.json`. Claude Code uses `"type": "http"` for
streamable HTTP transport.

### `.mcp.json` (Cursor / cross-platform format)

```json
{
  "mcpServers": {
    "revelica": {
      "type": "streamable-http",
      "url": "https://scryfast-development.fly.dev/mcp"
    }
  }
}
```

Uses the standard `mcpServers` wrapper expected by Cursor. Cursor uses
`"type": "streamable-http"` (different from Claude Code's `"type": "http"`).

### `.claude-plugin/marketplace.json`

```json
{
  "name": "revelica",
  "owner": { "name": "Revelica" },
  "plugins": [
    {
      "name": "revelica",
      "source": "./",
      "description": "Revelica MCP tools and skills for product intelligence",
      "version": "1.2.0"
    }
  ]
}
```

`source: "./"` points to the repo root as the plugin root. Paths in `plugin.json`
are relative to this directory.

## Available MCP Tools

These tools are provided by the Revelica MCP server and callable from any skill:

| Tool | Description |
|------|-------------|
| `list_artifacts` | List artifacts across projects. Supports `artifact_type`, `project_id`, `limit` filters. |
| `get_artifact` | Fetch full `json_content` for a single artifact by ID. |
| `get_project_artifacts` | Fetch project metadata + all artifacts grouped by type for a given `project_id`. |
| `list_playbook_runs` | List recent playbook runs with status and timestamps. |

All tools require OAuth authentication and enforce Supabase RLS — users only see their
own workspace's data.

# About Revelica

Revelica is an AI-native product discovery platform. It helps product managers create customer insights, competitive analysis, and validated specs that feed into their AI development workflow.

🔗 https://revelica.com
