# Claude Code adapter

These five skills (`init-vault`, `convert-note`, `query-vault`, `organize-vault`,
`vault-health`) are the **Claude Code adapter** over Infinite Brain's memory contract.

They are one way to drive the memory — convenient if you already work in Claude Code. The
tool-agnostic source of truth is:

- `_system/AGENTS.md` — the memory contract every agent follows.
- `mcp-server/` — the MCP server that exposes the same operations (read/write/validate/query/
  audit/decay) to **any** MCP-capable AI, not just Claude Code.

If you use a different client (ChatGPT, Cursor, …), ignore this folder and connect the MCP
server instead — see `mcp-server/clients/`.
