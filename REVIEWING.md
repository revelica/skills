# Reviewing the Revelica plugin

Use the test account, workspace and sign-in instructions supplied privately for
the directory submission. Reviewer account details and recordings are not
published in this repository.

## Connect the plugin

Install the submitted Revelica plugin in the intended client. To test the MCP
server directly, add this custom connector:

| | |
|---|---|
| **Server URL** | `https://api.revelica.com/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | OAuth 2.0 with dynamic client registration |

Complete Revelica sign-in and consent if prompted, using the supplied test
account. Start a fresh conversation after disconnecting/reconnecting; old
conversation cards can retain stale connection references.

## Try the review cases

Reusable examples are in
[`extensions.com.openai.review.test_cases`](plugins/revelica/.codex-plugin/plugin.json).
For a directory review, follow the cases and workspace instructions included in
that submission. Run the goal case before the bets case in the same conversation,
or identify the test project first.

The planning example proposes next steps and asks for separate approval before
saving or changing anything. The synthetic note and interview examples use fixed
titles and ask the agent to check existing records, reuse matching analysis, and
create only what is missing. Repeat the identical prompt and compare returned
links/IDs and persisted records. These instructions aim to support sequential
reruns; they do not guarantee duplicate prevention during concurrent runs.

Do not approve destructive actions while running the negative cases. They should
not delete records, expose another company's private data or invoke Revelica
tools to book travel. Ordinary clarification or a safe fallback is allowed.

The plugin's starting skills are also available:

- **Set up Revelica** (`setup-revelica`)
- **Plan the work toward our goal** (`drive-product-outcome`)
- **Add insights to our knowledge graph** (`ingestion`)
- **Analyze a customer interview** (`interview-snapshot`)

Questions: ask@revelica.com.
