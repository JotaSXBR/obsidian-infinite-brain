# Infinite Brain — MCP Server

A tool-agnostic bridge that lets **any MCP-capable AI** read and write the Infinite
Brain knowledge-graph vault. The server owns everything mechanical (frontmatter
parsing, schema validation, id uniqueness, index maintenance, edge integrity, orphan
detection, confidence decay, file moves); the *judgment* work (classification,
decomposition, synthesis) stays in the calling model, surfaced as MCP **prompts**.

The vault is an **OKF v0.1 bundle** (markdown + YAML frontmatter) with a typed-edge
and trust-metadata extension layer. See `../_system/OKF-MAPPING.md`.

## Install

```bash
cd mcp-server
pip install -e .          # or: pip install -e ".[dev]" for tests
```

## Run

```bash
python -m infinite_brain_mcp --vault /path/to/vault
# or
INFINITE_BRAIN_VAULT=/path/to/vault python -m infinite_brain_mcp
```

Vault root resolution: `--vault` → `$INFINITE_BRAIN_VAULT` → current directory.

## Connect a client

See `clients/` for ready configs: `claude_desktop.json`, `cursor.json`, and
`generic-stdio.md` for any other MCP client.

## Surface

| Kind | Names |
|---|---|
| Tools (16) | `list_node_types` `list_edge_types` `node_read` `node_validate` `node_create` `node_update` `index_read` `index_rebuild` `graph_query` `graph_neighbors` `vault_audit` `confidence_decay` `belief_revision` `raw_hash` `raw_list` `raw_mark_processed` |
| Resources (6) | `infinite-brain://system/{agents,node-types,edge-types,frontmatter-schema,okf-mapping}`, `infinite-brain://index` |
| Prompts (5) | `convert-note` `query-vault` `organize-vault` `vault-health` `init-vault` |

## Design guarantees

- **Writes are validated.** `node_create`/`node_update` refuse on hard errors
  (missing `type`, malformed edges, duplicate id, self-edges). Warnings follow OKF's
  permissive-consumption model.
- **Deterministic maintenance.** `confidence_decay` is reversible via git and never deletes.
- **OKF-safe.** The server never strips unknown frontmatter keys.

## Test

```bash
python -m pytest -q tests/
```
