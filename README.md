# Revelica Skills

Official Claude Code plugin for Revelica — provides MCP-connected slash commands for
product intelligence directly in your terminal.

## Repository Structure

```
revelica/skills
├── .claude-plugin/
│   └── marketplace.json       # Marketplace catalog (points to ./plugin)
└── plugin/
    ├── .claude-plugin/
    │   └── plugin.json        # Plugin manifest (name, version, mcpServers ref)
    ├── .mcp.json              # MCP server connection config
    └── commands/
        └── project-brief.md  # /revelica:project-brief skill
```

## How It Works

### Install flow (one-time per user)

```
User: /plugin marketplace add revelica/skills
  └─ Claude Code clones this repo
        └─ reads .claude-plugin/marketplace.json
              └─ source: "./plugin" → registers the plugin/ subdirectory

User: /plugin install revelica@revelica
  └─ Claude Code reads plugin/.claude-plugin/plugin.json
        ├─ registers /revelica:<command> slash commands (from commands/)
        └─ reads mcpServers: "./.mcp.json"
              └─ registers MCP server:
                 type: sse
                 url: https://api.revelica.com/sse
```

### Runtime flow (per skill invocation)

```
User: /revelica:project-brief [project-id]
  │
  ├─ Claude Code: GET /sse → 401 + OAuth metadata
  │     └─ OAuth flow: browser → Supabase → /auth/consent → JWT
  │
  └─ Claude executes commands/project-brief.md instructions:
        │
        ├─ MCP tool: get_project_artifacts(project_id)
        │     └─ POST /messages/ → MCP server → Supabase (RLS enforced)
        │
        ├─ MCP tools (parallel): get_artifact(id) × up to 5
        │
        └─ Claude synthesizes and returns the project brief
```

### Transport

Claude Code's plugin system only accepts `stdio`, `sse`, and `sse-ide` transport types.
The Revelica backend exposes both SSE (for the plugin) and streamable-HTTP (for other clients)
from the same MCP server instance.

## Plugin File Formats

### `plugin/.claude-plugin/plugin.json`

```json
{
  "name": "revelica",
  "description": "Revelica MCP tools and skills for product intelligence",
  "version": "1.0.0",
  "mcpServers": "./.mcp.json"
}
```

`mcpServers` must be explicitly declared. Claude Code does not auto-discover `.mcp.json`.

### `plugin/.mcp.json`

```json
{
  "revelica": {
    "type": "sse",
    "url": "https://api.revelica.com/sse"
  }
}
```

The plugin `.mcp.json` format has **no `mcpServers` wrapper** — the server name is the
top-level key. This is different from the project-level `.mcp.json` format used in codebases.

### `.claude-plugin/marketplace.json`

```json
{
  "name": "revelica",
  "owner": { "name": "Revelica" },
  "plugins": [
    {
      "name": "revelica",
      "source": "./plugin",
      "description": "Revelica MCP tools and skills for product intelligence",
      "version": "1.0.0"
    }
  ]
}
```

`source: "./plugin"` uses a relative path within this repo. This avoids a Claude Code
deduplication issue where pointing both the marketplace and plugin source to the same GitHub
repo results in an empty plugin install cache.

## Adding a New Skill

1. Create a Markdown file in `plugin/commands/`:
   ```bash
   touch plugin/commands/my-skill.md
   ```

2. Write it with frontmatter and step-by-step instructions:
   ```markdown
   ---
   description: What this skill does and when to use it.
   argument-hint: [optional-arg]
   ---

   Instructions for Claude to follow.

   If an argument was provided, use it directly.
   Otherwise, call list_artifacts to discover available data.
   ```

   The file is invoked as `/revelica:my-skill`. `$ARGUMENTS` is replaced with whatever
   the user types after the command — it is an empty string when no argument is provided,
   so write instructions that handle both cases explicitly.

3. Commit and push. Users get the update by running:
   ```
   /plugin marketplace update revelica
   /plugin update revelica@revelica
   ```

No changes to the backend are needed unless the skill requires a new MCP tool.

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

## User Installation

See [how-to-install.md](https://github.com/revelica/scryfast/blob/main/skills/how-to-install.md)
for the end-user guide.

Quick version:
```
/plugin marketplace add revelica/skills
/plugin install revelica@revelica
```
