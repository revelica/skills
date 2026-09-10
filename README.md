<p align="center">
  <img src="assets/revelica-icon-512.png" alt="Revelica" width="96" height="96">
</p>

<h1 align="center">Revelica Skills</h1>

Revelica's plugin package connects an agent to shared product context: customer research, competitive analysis, goals, bets and product specs. It bundles `use-revelica` as a general starting point and `product-for-coding-agents` as an implementation specialization. Product workflows are discovered and loaded from the connected Revelica MCP server with `list_skills` and `load_skill`.

The repository includes client-specific manifests and an [Agent Skills](https://agentskills.io/specification) directory. Installation, skill discovery and OAuth support depend on the client; these files do not establish support for the emerging skills-over-MCP extension in every host.

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
│   ├── use-revelica/            # General starting point; loads server orientation
│   └── product-for-coding-agents/  # Coding-specific orientation
├── assets/                      # Brand icons (README, directory submissions)
├── server.json                  # MCP registry manifest (registry.modelcontextprotocol.io)
├── .mcp.json                    # MCP config for Cursor/Gemini
├── gemini-extension.json        # Gemini CLI extension manifest
└── LICENSE                      # Apache-2.0
```

## Installation by Platform

### Claude Code

```
/plugin marketplace add revelica/skills
/plugin install revelica@revelica
```

The plugin manifest points to the bundled orientation and MCP configuration. Authorize the server connection in your client before using workspace tools.

### Cowork

Add `https://api.revelica.com/mcp` as a custom connector in your organization's
settings. A connector connection is separate from installing this bundled orientation. Discover server workflows through `list_skills` and `load_skill` when the client exposes those tools.

### Cursor

The `.cursor-plugin/plugin.json` manifest declares the `skills/` directory and `.mcp.json` server configuration. Use the installation and authorization flow supported by your Cursor version.

### Gemini CLI

```
gemini extensions install revelica/skills
```

The `gemini-extension.json` manifest declares the skills directory and MCP server configuration. Check that the installed client exposes both after authorization.

## Available MCP Tools

These tools are provided by the Revelica MCP server and callable from any skill:

| Tool | Description |
|------|-------------|
| `query` | Search or filter the workspace by criteria. Returns ranked matches, plus the schema template when `artifact_type` is set. |
| `read` | Read a single artifact or entity in full by id, or navigate to a subtree with a dotted field `path`. |
| `create` | Create new artifacts or entities. Content validated against registered schemas. |
| `update` | Apply partial field-level updates via dot-path notation. |
| `load_skill` | Load a server skill's instructions and supported context or references. This does not itself execute a playbook. |
| `list_skills` | List the skills this workspace exposes to MCP clients. |

All tools require OAuth authentication and enforce Supabase RLS — users only see their
own workspace's data.

## Bundled orientation and server workflows

| Location | Skill | Purpose |
|---|---|---|
| This package | `use-revelica` | Load the server orientation, reuse available context and discover the task that matches the user's request. |
| This package | `product-for-coding-agents` | Orient on the Idea/spec, customer problem and bet; save implementation references and feasibility evidence. |
| Connected MCP server | `write-product-spec` | Author or revise the canonical product spec using the current server instructions and schema. Discover availability with `list_skills`, then load it with `load_skill`. |

The bundled `use-revelica` is a thin bootstrap: it calls the connected server's `load_skill` for the server skill with the same name. Product workflow instructions stay on the server. The coding orientation adds implementation-specific guidance and is optional for general product work. Current task entries include `frame-bet`, `write-product-spec` and `test-idea`; use the live catalog to check availability.

An Idea is the product spec. Its story map, structured document and Markdown are representations of the same spec. The package does not bundle a second spec-authoring implementation.

The live `list_skills` response is authoritative for the connected server and user. Loading instructions lets the current agent follow a workflow using the available tools; it does not start a server-side playbook/DAG. These tool-based workflows do not require a host to implement the skills-over-MCP extension.

## Updating skills

Keep client orientation and package configuration here. Maintain product workflow instructions on the Revelica server so the app and connected agents can discover the same canonical workflow. Add a bundled skill only when it serves a client-side purpose that cannot be covered by the orientation and server discovery.

Package updates and server deployments are separate. A newly documented server workflow must be deployed before a connected client can load it. Deploy the backend canonical skills (`use-revelica`, `frame-bet`, `write-product-spec` and `test-idea`) before releasing this package update. Do not assume installing this package deploys them.

## Connecting the MCP Server Directly

If you'd rather connect the server without the plugin, add it as a remote MCP
server / custom connector:

| | |
|---|---|
| **Server URL** | `https://api.revelica.com/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | OAuth 2.0 with dynamic client registration — no API key to manage |
| **Prerequisite** | A Revelica workspace ([sign up](https://app.revelica.com)) |

Server metadata is published at
[`/.well-known/mcp/server-card.json`](https://api.revelica.com/.well-known/mcp/server-card.json).

## Privacy Policy

Revelica's privacy policy — covering what data is collected, how it is used and
stored, third-party sharing, retention, and how to contact us — is published at
[revelica.com/privacy](https://revelica.com/privacy). Terms of service are at
[revelica.com/terms](https://revelica.com/terms).

The MCP server reads and writes only the product data in your own Revelica
workspace. Every request is authenticated with OAuth and enforced by Supabase
row-level security, so a connected agent can never see another workspace's data.
The server does not query your chat history, conversation summaries, or files.

## Support

- **Issues with the plugin or skills:** [open a GitHub issue](https://github.com/revelica/skills/issues)
- **Account, workspace, or MCP server issues:** ask@revelica.com

## License

[Apache-2.0](LICENSE) © Revelica

# About Revelica

Revelica is an AI-native product discovery platform. It helps product teams gather customer insights, perform competitive analysis, and experimentally validate ideas that feed into their AI development workflow.

🔗 Homepage with free Pro trial: https://revelica.com

🔗 Template library with playbooks, skills, and insight templates: https://revelica.com/templates

🔗 Free AI tools with no signup required: https://revelica.com/tools
