<p align="center">
  <img src="plugins/revelica/assets/revelica-icon-512.png" alt="Revelica" width="96" height="96">
</p>

<h1 align="center">Revelica</h1>

Revelica is your team's product workspace: goals and KPIs, customer research, competitors, decisions, assumptions and specs. This plugin connects your agent to it, so every conversation can start from what your team already knows and save what it learns.

It adds two things to your agent: the Revelica MCP server, and a skill for each job Revelica does. You need a Revelica account ([sign up](https://app.revelica.com)).

## Install

**Claude and Claude Code:** connect Revelica from [Claude's directory](https://claude.ai/directory/revelica). Claude Code picks it up when you're signed in with the same Claude account. [Setup guide](https://revelica.com/docs/integrations/claude).

**ChatGPT and Codex:** add Revelica from [ChatGPT's plugin directory](https://chatgpt.com/plugins/plugin_asdk_app_6abed1e3bde08191bb5676d2a115c308), which Codex shares. [Setup guide](https://revelica.com/docs/integrations/chatgpt).

**Other MCP clients:** add a remote MCP server. [Setup guide](https://revelica.com/docs/mcp).

| | |
|---|---|
| **Server URL** | `https://api.revelica.com/mcp` |
| **Transport** | Streamable HTTP |
| **Sign-in** | OAuth, no API key |

Then sign in to Revelica when your client asks, and run **setup-revelica** first: the other skills need the business, goal and customer it sets up.

## Skills

| Skill | Use it to |
|---|---|
| `setup-revelica` | Set up your workspace: business model, customer profile and goals. Run it first. |
| `drive-product-outcome` | Plan the work toward a goal, see what's next and how it's tracking. |
| `business-strategy` | Set or change vision, business model, value propositions and goals. |
| `product-insights` | Research customers, competitors and markets, and save interviews and notes. |
| `product-strategy` | Decide which bets to make or drop, and whether something is worth building. |
| `discover-solutions` | Generate ideas and write specs and PRDs with stories. |
| `test-product-risks` | Test risky assumptions with surveys, data, experiments or prototypes. |
| `implement-spec` | Build a feature from its spec, and record what shipped. |

Each skill here is a short entry point. The full workflow comes from the Revelica server when the agent loads it, so it stays in step with the tools it uses.

## What it connects to and sends

The plugin runs no code on your machine. It declares one remote MCP server, `https://api.revelica.com/mcp`, and bundles the skills above as Markdown.

- **Sign-in:** OAuth, handled by your client. The plugin reads no credentials, tokens or files from your machine.
- **Sends:** the Revelica tool calls your agent makes (`query`, `read`, `create`, `update`, `show`, `load_skill`, `list_skills`) and their arguments, which carry what you ask it to save. `send_feedback` sends a short report about the tools to Revelica's developers, only when you agree.
- **Receives:** records from your own workspace, skill instructions, and links to open them in Revelica.

The server reads and writes only your own workspace. Every request is authenticated, and row-level security keeps each workspace's data separate. It doesn't read your chat history or files.

[Privacy policy](https://revelica.com/privacy) · [Terms of service](https://revelica.com/terms)

## Support

- Plugin issues: [open an issue](https://github.com/revelica/skills/issues)
- Account or workspace questions: ask@revelica.com

## License

[Apache-2.0](LICENSE) © Revelica
