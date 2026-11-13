<p align="center">
  <img src="plugins/revelica/assets/revelica-icon-512.png" alt="Revelica" width="96" height="96">
</p>

<h1 align="center">Revelica Skills</h1>

Revelica's plugin package connects an agent to shared product context: customer research, competitive analysis, goals, bets and product specs. It declares the Revelica MCP server and one skill for each job Revelica does. The full workflows live on the server, which names the one for each job in its instructions and loads it with `load_skill`.

There is one plugin, `plugins/revelica/`, with a manifest for each host beside it. Each host's catalog sits at the repository root, where that host looks for it. Installation and OAuth support depend on the client.

## Repository Structure

```
revelica/skills
├── plugins/revelica/            # The plugin, shared by every host
│   ├── .claude-plugin/          # Claude plugin manifest
│   ├── .codex-plugin/           # OpenAI (ChatGPT and Codex) plugin manifest
│   ├── .mcp.json                # The Revelica MCP server
│   ├── skills/                  # Starting skills (also slash commands in Claude Code)
│   └── assets/                  # Brand icons
├── .claude-plugin/marketplace.json   # Claude Code marketplace catalog
├── .agents/plugins/marketplace.json  # Codex marketplace catalog
├── server.json                  # MCP registry manifest (registry.modelcontextprotocol.io)
├── scripts/package-openai.sh    # Exports the portable ZIP for OpenAI's plugin portal
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

### Other clients

Cursor, Gemini CLI and any other client that speaks Streamable HTTP with OAuth can connect the server directly (see [Connecting the MCP Server Directly](#connecting-the-mcp-server-directly)). We only ship and test plugins for Claude and OpenAI hosts. Release 1.10.1 removed the Cursor and Gemini manifests, which nobody was testing.

## Starting prompts

The plugin adds one skill for each job Revelica does, the same jobs the Revelica app runs. Each one is a short stand-in that loads the full skill from the Revelica server, so the method is always current. In Claude Code each is also a slash command:

| Skill | What it does |
|---|---|
| `/revelica:setup-revelica` | Set up Revelica on your own product: your business, a goal and a researched customer, then a first result and a handover to planning. ChatGPT runs it from its **Set up** prompt after install; in Claude, ask to "set up Revelica". |
| `/revelica:drive-product-outcome` | Plan the work toward our goal: read the goal, its measurements, the active bets and their evidence, then recommend the next action and plan it as work. Use it for a new goal, or work that needs several jobs in sequence. |
| `/revelica:business-strategy` | Set or rethink the business strategy: target customers, business model, a value proposition for each customer, and the goals that matter now. |
| `/revelica:product-insights` | Find where you can win: research the customer and the products they use today. Also saves a link, file, note or interview as evidence and connects it to what it bears on. |
| `/revelica:product-strategy` | Decide which bets to make and which to decline, say why, and say what evidence would change the call. |
| `/revelica:discover-solutions` | Find a solution customers will love that works for the business, and write the leading one as a spec with a story map. |
| `/revelica:test-product-risks` | Find the riskiest assumptions in a bet or spec and test each with the quickest method that settles it, then make the call. |
| `/revelica:implement-spec` | Build a feature from its spec, stories and decisions, and write back what you learn. |

Older skill names such as `ingestion`, `interview-snapshot` and `frame-bet` still work with `load_skill`: the server routes each to the job that now holds it.

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

Almost everything changes on the server, not here. Skill instructions (`load_skill`), tool descriptions and schemas, and the server instructions all live on the Revelica server, so a server deploy updates every host at once. OpenAI's continuous review picks up server changes from its daily scan (or a Rescan in the portal) without a new plugin version; a changed tool keeps its old definition live until the new one passes automated checks, so keep the server accepting calls in the old shape.

This package is what needs a release, and an OpenAI release means a new ZIP and a new review by people. So it is kept small and stable:

- **Stand-in skills are frozen.** Each `SKILL.md` is a name, a description and a first prompt, plus the instruction to call `load_skill`. Tune routing and wording on the server (its instructions and the skills themselves, measured with the evals in the monorepo), not here. Change a stand-in only on purpose, as part of a package release: adding or removing a job skill, or a description that measurably routes better.
- **The package has its own version.** Bump the version in the three package manifests together (`plugins/revelica/.claude-plugin/plugin.json`, `plugins/revelica/.codex-plugin/plugin.json`, `.claude-plugin/marketplace.json`) only when the package's contents change. `server.json`, the MCP registry entry, follows the server's `SERVER_VERSION` (`packages/mcp/revelica_mcp/server.py` in the revelica monorepo) and is updated with server releases.
- **Review cases describe behaviour.** OpenAI's review test cases say what the agent should do and save, never which skill runs it, so regrouping server skills doesn't invalidate them (`scripts/tests` checks this).

Name package releases `Revelica X.Y.Z` and list the targeted platforms in the release notes. A package release that depends on new server behaviour ships after that server is deployed: installing the package doesn't deploy the server.

Run `bash scripts/package-openai.sh` to build `dist/revelica-openai-<version>.zip`
for OpenAI's submission portal. It exports the Codex manifest's listing fields
under `extensions.com.openai.interface` in a portable root `plugin.json`, and
exports `.mcp.json` as `mcp.json` with the Streamable HTTP transport name. Review
cases and publication metadata are retained. The shared plugin's Claude and
Codex compatibility manifests are not included in this public upload.
Package validation does not complete the portal's reviewer access, demo,
country targeting, scans, or attestations.

The exporter refuses to overwrite an existing archive. For a verification build,
choose a new path: `bash scripts/package-openai.sh --output /tmp/revelica-check.zip`.
ZIP entry timestamps and permissions are fixed, so builds with the same
Python/zlib toolchain produce identical bytes. Run the packaging checks with
`python3 -m unittest discover -s scripts/tests -v`.

Keep one private copy of the exact ZIP uploaded for review. `dist/` stays ignored.
Reviewer account details, recordings and submission notes belong outside this
public repository. The public manifest contains reusable test cases; supply
submission-specific workspace instructions and recording metadata privately when
preparing an upload. A fresh export is not a replacement for the original upload.

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
