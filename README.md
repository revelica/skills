# Revelica Skills

Official Revelica plugin for AI coding tools — provides MCP-connected skills for
product intelligence. Follows the [Agent Skills open standard](https://agentskills.io/specification),
compatible with Claude Code, Cursor, Gemini CLI, OpenAI Codex, and more.

## Repository Structure

```
revelica/skills
├── .claude-plugin/
│   ├── marketplace.json         # Claude Code marketplace catalog
│   └── plugin.json              # Claude Code plugin manifest
├── .cursor-plugin/
│   └── plugin.json              # Cursor plugin manifest
├── agents/
│   └── AGENTS.md                # Fallback bundle for tools without a plugin system
├── skills/                      # Skill definitions (Agent Skills open standard)
│   └── project-brief/
│       └── SKILL.md             # /revelica:project-brief
├── .mcp.json                    # MCP config (all platforms)
└── gemini-extension.json        # Gemini CLI extension manifest
```

## Installation by Platform

### Claude Code

```
/plugin marketplace add revelica/skills
/plugin install revelica@revelica
```

Skills are invoked as `/revelica:<skill-name>`. The MCP server is registered automatically.

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
Type: SSE
URL:  https://scryfast-development.fly.dev/sse
```

## How It Works

### Claude Code install flow (one-time per user)

```
User: /plugin marketplace add revelica/skills
  └─ Claude Code clones this repo
        └─ reads .claude-plugin/marketplace.json
              └─ source: "." → repo root is the plugin root

User: /plugin install revelica@revelica
  └─ Claude Code reads .claude-plugin/plugin.json
        ├─ discovers skills/ → registers /revelica:<skill> commands
        └─ reads mcpServers: "./.mcp.json"
              └─ registers MCP server (SSE, OAuth 2.1)
```

### Runtime flow (per skill invocation)

```
User: /revelica:project-brief [project-id]
  │
  ├─ Claude Code: GET /sse → 401 + OAuth metadata
  │     └─ OAuth flow: browser → Supabase → /auth/consent → JWT
  │
  └─ Claude executes skills/project-brief/SKILL.md instructions:
        │
        ├─ MCP tool: get_project_artifacts(project_id)
        │     └─ POST /messages/ → MCP server → Supabase (RLS enforced)
        │
        ├─ MCP tools (parallel): get_artifact(id) × up to 5
        │
        └─ Claude synthesizes and returns the project brief
```

### Transport

The backend exposes two transports from the same MCP server:
- `GET /sse` + `POST /messages/` — SSE (Claude Code plugin system)
- `POST /mcp` — Streamable HTTP (Cursor, MCP Inspector, direct clients)

## Skill Format

Skills follow the [Agent Skills open standard](https://agentskills.io/specification).
Each skill is a folder under `skills/` containing a `SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: What this skill does and when to use it.
argument-hint: [optional-arg]   # Claude Code extension
---

Instructions for Claude to follow...
```

## Adding a New Skill

1. Create a folder under `skills/`:
   ```bash
   mkdir skills/my-skill
   touch skills/my-skill/SKILL.md
   ```

2. Write `SKILL.md` with frontmatter and step-by-step instructions:
   ```markdown
   ---
   name: my-skill
   description: What this skill does and when to use it.
   argument-hint: [optional-arg]
   ---

   Instructions for Claude to follow.

   If an argument was provided in `$ARGUMENTS`, use it directly.
   Otherwise, call list_artifacts to discover available data.
   ```

   Invoked in Claude Code as `/revelica:my-skill`. `$ARGUMENTS` is replaced with whatever
   the user types after the command — handle both empty and non-empty cases explicitly.

3. Add the skill to `agents/AGENTS.md` for cross-platform fallback support.

4. Commit and push. Users get the update by running:
   ```
   # Claude Code
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
  "version": "1.0.0",
  "skills": "./skills",
  "mcpServers": "./.mcp.json"
}
```

`mcpServers` must be explicitly declared — Claude Code does not auto-discover `.mcp.json`.

### `.mcp.json`

```json
{
  "mcpServers": {
    "revelica": {
      "type": "sse",
      "url": "https://scryfast-development.fly.dev/sse"
    }
  }
}
```

### `.claude-plugin/marketplace.json`

```json
{
  "name": "revelica",
  "owner": { "name": "Revelica" },
  "plugins": [
    {
      "name": "revelica",
      "source": ".",
      "description": "Revelica MCP tools and skills for product intelligence",
      "version": "1.0.0"
    }
  ]
}
```

`source: "."` points to the repo root, which is the plugin root.

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
