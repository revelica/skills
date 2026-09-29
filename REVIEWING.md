# Reviewing the Revelica plugin

Setup for directory reviewers. The invite link is in the submission's review notes; it isn't published here because it joins a shared demo workspace.

## Set up the test account

1. Open the invite link from the review notes.
2. Sign up with an email address and the one-time code sent to it.
3. Fill in your profile. The invite adds you to the **Scryify** demo workspace, which has example goals, bets, customer segments, research and specs.
4. For team, select **Product Team** and click **Save**.
5. Click **Go to Knowledge Graph**.

## Connect the plugin

Install the Revelica plugin in your client, or add the server as a custom connector:

| | |
|---|---|
| **Server URL** | `https://api.revelica.com/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | OAuth 2.0 with dynamic client registration |

Your client opens a Revelica consent screen. Click **Allow**.

## Try it

Use the plugin's suggested prompts, or its skills:

- **Plan the work toward our goal** (`drive-product-outcome`)
- **Add insights to our knowledge graph** (`ingestion`)
- **Analyze a customer interview** (`interview-snapshot`)

Each one reads from and writes to the Scryify workspace through the `query`, `read`, `create`, `update`, `load_skill` and `list_skills` tools. To see what the agent saved, browse the workspace in the web app, where you're still signed in (optional).

Questions: ask@revelica.com.
