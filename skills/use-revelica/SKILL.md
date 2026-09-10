---
name: use-revelica
description: Connect a product task to Revelica's current workspace context and server workflows. Use when the user wants to use Revelica for strategy, discovery, product specs, bets or assumption tests, including when starting with an existing conversation or connected tools. Load the server's orientation and discover the relevant workflow before proceeding.
---

# Use Revelica

This bundled skill is a starting point for the connected Revelica MCP server. The server owns the current workflow instructions and workspace schemas.

1. Locate Revelica's `list_skills` and `load_skill` tools. If the connection is missing or requires authorization, use the host's normal connection flow or explain what is missing.
2. Call `list_skills` to discover the current server catalog. Load the **server's `use-revelica`** with `load_skill`, following the tool's actual argument schema. This means fetching the server instructions, not reloading this bundled file with the same name.
3. Follow that orientation to reuse available conversation, workspace and connected-tool context. Discover and load the task that matches the user's request. Current task entry names include `frame-bet`, `write-product-spec` and `test-idea`; the live catalog determines which are available.
4. Follow the loaded workflow and its supporting references through the server's supported loading path. Ask only for context that blocks the user's current task. Do not invent missing product facts or substitute a stale local workflow if a server skill is unavailable.

Loading instructions lets you perform the workflow with the available tools; it does not launch a server-side playbook or DAG. Preserve the originating server when resolving tool and reference names.

For implementation work, the bundled `product-for-coding-agents` adds guidance on reading the spec and saving agreed changes, implementation references and feasibility evidence. Use it when relevant; general product work does not require that specialization.
