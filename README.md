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
│   └── mcp.json                 # MCP config for Claude Code plugin
├── .cursor-plugin/
│   └── plugin.json              # Cursor plugin manifest
├── skills/                      # Skill definitions (Agent Skills open standard)
│   ├── product-for-coding-agents/  # Product layer for coding agents (orientation)
│   └── write-spec/              # Author a feature spec attached to an idea
├── server.json                  # MCP registry manifest (registry.modelcontextprotocol.io)
├── .mcp.json                    # MCP config for Cursor/Gemini
└── gemini-extension.json        # Gemini CLI extension manifest
```

## Installation by Platform

### Claude Code

```
/plugin marketplace add revelica/skills
/plugin install revelica@revelica
```

Skills are **model-invoked** — Claude automatically uses them based on context. The MCP
server is registered automatically.

### Cursor

Install via the `.cursor-plugin/plugin.json` manifest. Cursor will discover skills from
the `skills/` directory and connect to the MCP server via `.mcp.json` automatically.

### Gemini CLI

```
gemini extensions install revelica/skills
```

The `gemini-extension.json` manifest registers both skills and the MCP server.

## Available MCP Tools

These tools are provided by the Revelica MCP server and callable from any skill:

| Tool | Description |
|------|-------------|
| `query` | Search the workspace knowledge base — artifacts, entities, schemas. Filter by `artifact_type`, control detail with `depth`. |
| `read` | Read a single artifact or entity in full by id. |
| `create` | Create new artifacts or entities. Content validated against registered schemas. |
| `update` | Apply partial field-level updates via dot-path notation. |
| `load_skill` | Load a skill's instructions and prefetched workspace data. |

All tools require OAuth authentication and enforce Supabase RLS — users only see their
own workspace's data.

## Available Skills

| Skill | Description |
|-------|-------------|
| `product-for-coding-agents` | Orientation for a coding agent: read the idea/spec/UX behind the code, write high-level results (impl docs, PRs, tested feasibility assumptions, ideas, sources) back. |
| `write-spec` | Author a feature spec attached to an idea, following the Revelica spec template — incremental section-by-section writes that fit coding-agent tool-call budgets. |

## Adding a New Skill

1. Create a folder under `skills/`:
   ```bash
   mkdir skills/my-skill
   touch skills/my-skill/SKILL.md
   ```

2. Write `SKILL.md` following the [Agent Skills spec](https://agentskills.io/specification):
   ```markdown
   ---
   name: my-skill
   description: What this skill does and when to use it.
   compatibility: Requires Revelica MCP server (query, read, create, update tools)
   ---

   Instructions for the agent...
   ```

3. Commit and push. Users get the update by running:
   ```
   /plugin update revelica@revelica
   ```

No backend changes needed unless the skill requires a new MCP tool.

# About Revelica

Revelica is an AI-native product discovery platform. It helps product teams gather customer insights, perform competitive analysis, and experimentally validate ideas that feed into their AI development workflow.

🔗 Homepage with free Pro trial: https://revelica.com

🔗 Template library with playbooks, skills, and insight templates: https://revelica.com/templates

🔗 Free AI tools with no signup required: https://revelica.com/tools
