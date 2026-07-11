# Connecting any MCP client (stdio)

The server speaks MCP over stdio, so any MCP-capable client can use it.

**Command the client must launch:**

```
python -m infinite_brain_mcp --vault /absolute/path/to/your/vault
```

Or set the vault via environment variable and omit the flag:

```
INFINITE_BRAIN_VAULT=/absolute/path/to/your/vault python -m infinite_brain_mcp
```

Vault root resolution order: `--vault` arg → `$INFINITE_BRAIN_VAULT` → current directory.

**What the client sees**

- **14 tools** — node CRUD + validate, index read/rebuild, graph query/neighbors,
  audit, confidence decay, raw inbox.
- **6 resources** — the agent contract and schema files:
  `infinite-brain://system/agents`, `.../node-types`, `.../edge-types`,
  `.../frontmatter-schema`, `.../okf-mapping`, and `infinite-brain://index`.
- **5 prompts** — `convert-note`, `query-vault`, `organize-vault`, `vault-health`,
  `init-vault`.

**First call from any agent:** read `infinite-brain://system/agents`, then
`index_read` (or `graph_query`) before writing anything.
