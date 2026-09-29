<p align="center">
  <img src="plugins/revelica/assets/revelica-icon-512.png" alt="Revelica" width="96" height="96">
</p>

<h1 align="center">Revelica Skills</h1>

Revelica's plugin package connects an agent to shared product context: customer research, competitive analysis, goals, bets and product specs. It declares the Revelica MCP server and three starting skills. The full workflows live on the server, which names the one for each job in its instructions and loads it with `load_skill`.

There is one plugin, `plugins/revelica/`, with a manifest for each host beside it. Each host's catalog sits at the repository root, where that host looks for it. Installation and OAuth support depend on the client.

## Repository Structure

```
revelica/skills
├── plugins/revelica/            # The plugin, shared by every host
│   ├── .claude-plugin/          # Claude plugin manifest and icon
│   ├── .codex-plugin/           # OpenAI (ChatGPT and Codex) plugin manifest
│   ├── .cursor-plugin/          # Cursor plugin manifest
│   ├── .mcp.json                # The Revelica MCP server
│   ├── skills/                  # Starting skills (also slash commands in Claude Code)
│   └── assets/                  # Brand icons
├── .claude-plugin/marketplace.json   # Claude Code marketplace catalog
├── .agents/plugins/marketplace.json  # Codex marketplace catalog
├── .cursor-plugin/marketplace.json   # Cursor marketplace catalog
├── gemini-extension.json        # Gemini CLI extension manifest (must be at the root)
├── server.json                  # MCP registry manifest (registry.modelcontextprotocol.io)
├── scripts/package-openai.sh    # Builds the ZIP for OpenAI's plugin portal
├── REVIEWING.md                 # Test setup for directory reviewers
└── LICENSE                      # Apache-2.0
```

## Installation by Platform

### Claude Code

```
/plugin marketplace add revelica/skills
/plugin install revelica@revelica
```

The plugin bundles the starting skills and the MCP server configuration. Authorize the server connection in your client before using workspace tools.

### Cowork

Add `https://api.revelica.com/mcp` as a custom connector in your organization's
settings. The server's instructions name the skill for each job, and `list_skills` lists the rest.

### Codex

```
codex plugin marketplace add revelica/skills
codex plugin add revelica@revelica
```

In ChatGPT, install Revelica from the plugin directory once it is listed.

### Cursor

The root `.cursor-plugin/marketplace.json` points Cursor at `plugins/revelica/`, whose manifest declares the `.mcp.json` server configuration. Use the installation and authorization flow supported by your Cursor version.

### Gemini CLI

```
gemini extensions install revelica/skills
```

The `gemini-extension.json` manifest declares the MCP server configuration. Check that the installed client exposes it after authorization.

## Starting prompts

The plugin adds three skills, the same starting points the Revelica app offers. In Claude Code each is also a slash command:

| Skill | What it does |
|---|---|
| `/revelica:drive-product-outcome` | Plan the work toward our goal: read the goal, its measurements, the active bets and their evidence, then recommend the next action and plan it as work. Sets up anything the workspace is missing along the way. |
| `/revelica:ingestion` | Add insights to the knowledge graph: save a URL, file or note as product evidence, then choose the next useful work. |
| `/revelica:interview-snapshot` | Analyze a customer interview: turn a transcript into a snapshot and the customer problems worth solving. |

## What the plugin connects to and sends

The plugin runs no code on your machine. It declares one remote MCP server, `https://api.revelica.com/mcp` (Streamable HTTP), and bundles Markdown skills that start common work with it.

- **Sign-in:** OAuth 2.0 with dynamic client registration, handled by your client. The plugin reads no credentials, tokens or files from your machine.
- **What it sends:** the tool calls your agent makes (`query`, `read`, `create`, `update`, `load_skill`, `list_skills`) and their arguments, which carry the product data you ask it to save to your workspace.
- **What it receives:** records from your own Revelica workspace, and skill instructions.

Nothing else is sent anywhere. See [Privacy Policy](#privacy-policy) for how Revelica handles your data.

## Available MCP Tools

These tools are provided by the Revelica MCP server and callable from any skill:

| Tool | Description |
|------|-------------|
| `query` | Search or filter the workspace by criteria. Returns ranked matches, plus the schema template when `artifact_type` is set. |
| `read` | Read a single artifact or entity in full by id, or navigate to a subtree with a dotted field `path`. |
| `create` | Create new artifacts or entities. Content validated against registered schemas. |
| `update` | Apply partial field-level updates via dot-path notation. |
| `load_skill` | Load a server skill's instructions, its readiness and a summary of the records it starts from. This does not itself execute a playbook. |
| `list_skills` | List the skills you can load, with each one's name, description and any required inputs. |

All tools require OAuth authentication and enforce Supabase row-level security, so users only see their
own workspace's data.

## Skills

The product workflows are skills on the connected Revelica MCP server: `drive-product-outcome`, `frame-bet`, `write-product-spec`, `design-experiment`, `product-for-coding-agents` and others. The server's instructions say which one fits which job, and `list_skills` shows the full catalog for the connected user.

An Idea is the product spec. Its story map, structured document and Markdown are representations of the same spec.

Loading a skill lets the current agent follow the workflow using the available tools; it does not start a server-side playbook. These tool-based workflows do not require a host to implement the skills-over-MCP extension.

## Updating

Product workflow instructions live on the Revelica server, so the app and connected agents discover the same canonical workflow. The package's three skills share the names and descriptions of the server skills they start, and load the full workflow from the server with `load_skill`, so the workflow and the workspace readiness it reports are always current. Release 1.9.0 removed the bundled `use-revelica` and `product-for-coding-agents` routers: every supported Claude host shows the server's instructions, which carry the same routing.

Release 1.10.0 moved the plugin into `plugins/revelica/`, turned the commands into skills so every host can use them, and added the OpenAI manifest. Bump the version in every manifest together.

Package updates and server deployments are separate. A newly documented server workflow must be deployed before a connected client can load it. Installing this package does not deploy server changes.

The skills in `plugins/revelica/skills/` carry the name, description and starting prompt of the server skill with the same name (scryfast `revelica_agents/app/agents/revelica/skills/`). Keep them in step when those change.

## Connecting the MCP Server Directly

If you'd rather connect the server without the plugin, add it as a remote MCP
server / custom connector:

| | |
|---|---|
| **Server URL** | `https://api.revelica.com/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | OAuth 2.0 with dynamic client registration, so there's no API key to manage |
| **Prerequisite** | A Revelica workspace ([sign up](https://app.revelica.com)) |

Server metadata is published at
[`/.well-known/mcp/server-card.json`](https://api.revelica.com/.well-known/mcp/server-card.json).

## Privacy Policy

Revelica's privacy policy covers what data is collected, how it is used and
stored, third-party sharing, retention, and how to contact us. It is published at
[revelica.com/privacy](https://revelica.com/privacy). Terms of service are at
[revelica.com/terms](https://revelica.com/terms).

The MCP server reads and writes only the product data in your own Revelica
workspace. Every request is authenticated with OAuth and enforced by Supabase
row-level security, so a connected agent can never see another workspace's data.
The server does not query your chat history, conversation summaries, or files.

## Support

- **Reviewing the plugin for a directory:** see [REVIEWING.md](REVIEWING.md)

- **Issues with the plugin:** [open a GitHub issue](https://github.com/revelica/skills/issues)
- **Account, workspace, or MCP server issues:** ask@revelica.com

## License

[Apache-2.0](LICENSE) © Revelica

# About Revelica

Revelica is an AI-native product discovery platform. It helps product teams gather customer insights, perform competitive analysis, and experimentally validate ideas that feed into their AI development workflow.

🔗 Homepage with free Pro trial: https://revelica.com

🔗 Template library with playbooks, skills, and insight templates: https://revelica.com/templates

🔗 Free AI tools with no signup required: https://revelica.com/tools
