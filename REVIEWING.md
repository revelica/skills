# Reviewing the Revelica plugin

The test account, workspace, sign-in details and review cases are supplied privately with each directory submission.

## Connect

Install the submitted plugin in the intended client, or add the server as a custom connector:

| | |
|---|---|
| **Server URL** | `https://api.revelica.com/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | OAuth 2.0 with dynamic client registration |

Sign in with the supplied test account. After disconnecting and reconnecting, start a new conversation: old ones can keep a stale connection.

## Notes for the review cases

- Run the goal case before the bets case in the same conversation, or name the test project first.
- Planning proposes next steps and asks before saving anything.
- The note and interview cases use fixed titles and reuse existing records, so repeating a prompt shouldn't create duplicates. Run them one after another, not at the same time.
- In the negative cases, don't approve destructive actions. The agent shouldn't delete records, show another company's data, or use Revelica for unrelated tasks.

Questions: ask@revelica.com
