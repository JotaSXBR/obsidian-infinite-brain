# Refactor Plan — Infinite Brain v2

**Goal:** turn Infinite Brain from a Claude-Code-only skill set into a tool-agnostic
memory system that (1) any AI can read and write through an **MCP server**, (2) stays
**OKF-conformant** so the corpus is portable across tools and organizations, and
(3) uses **Obsidian purely as the human reader** (graph view, Dataview, wikilinks).

Decisions locked in with the maintainer:

1. **Refactor in place** — keep the repo, history, folder structure, and example nodes.
2. **MCP server** is the any-AI bridge (matches the "Memoria Markdown para IA com MCP" intent).
3. **Layered schema** — an OKF-conformant *core* any agent can read, plus the rich
   *extensions* (typed edges, trust metadata) capable agents use.

---

## 1. Where we are

The vault is a rich, opinionated knowledge graph:

- 17 node types, 10 typed edges (in frontmatter: `target/type/weight/note`),
  trust metadata (`confidence`, `verified_at`, `staleness_signal`, `visibility`, `namespace`).
- Obsidian-compatible already (wikilinks in `related`).
- **All executable logic lives in `.claude/skills/`** (5 slash commands) — this is the
  Claude-Code coupling we are removing. `_system/AGENTS.md` is the only portable contract today.

## 2. Where we are going

```
                 +------------------------------------------+
   any MCP  ---> |  infinite-brain MCP server               | ---> vault/ (markdown)
   client        |  tools . resources . prompts             |      OKF core + extensions
 (Claude, GPT,   |  deterministic: parse . validate . index |
  Cursor, ...)   |  . graph traversal . decay               | <--- Obsidian (human reader)
                 +------------------------------------------+
```

**Principle — deterministic in code, reasoning in the client.** The server owns everything
mechanical: frontmatter parsing, schema validation, ID uniqueness, index maintenance, edge
integrity, orphan detection, confidence decay, file moves. The *judgment* parts
(classification, decomposition, synthesis) stay in the calling LLM, surfaced as MCP **prompts**.
This is what makes the system safe with a weaker model: the server refuses to let the graph
be corrupted.

## 3. OKF: how the layers map

OKF v0.1 conformance needs only: every non-reserved `.md` has parseable YAML frontmatter
with a non-empty `type`. The vault already satisfies this. The work is making the corpus
*interoperable*, not just *conformant*:

| OKF concept            | Infinite Brain today            | Plan |
|------------------------|----------------------------------|------|
| `type` (required)      | `type` (17 values) [ok]          | keep — OKF tolerates unknown types |
| `description`          | `summary`                        | treat `summary` as the OKF `description`; document alias |
| `resource`             | `source_url`                     | map `source_url` -> OKF `resource` semantics |
| `timestamp` (ISO 8601) | `verified_at` (MM/DD/YYYY)       | **migrate dates to ISO 8601** (sortable, unambiguous) |
| body markdown links    | frontmatter `edges` + `related`  | keep edges as the rich layer; optionally mirror key edges as body links for pure-OKF consumers |
| `index.md` per dir     | single `_system/INDEX.md`        | add a root OKF `index.md` (progressive disclosure) + keep `_system/INDEX.md` as the agent index |
| `log.md` per dir       | `logs/` folder of `type: log`    | keep — no conflict (no `log.md` files exist) |
| `okf_version`          | —                                | declare `okf_version: "0.1"` in root `index.md` |

New doc `_system/OKF-MAPPING.md` records this contract so the mapping is explicit and testable.

## 4. MCP server surface (draft)

**Tools** (deterministic):
- `node_read(id)` . `node_create(fields)` . `node_update(id, patch)` . `node_validate(id|draft)`
- `index_read()` . `index_rebuild()`
- `graph_query(question|filters)` — scoped traversal (the ~600-token retrieval path)
- `graph_neighbors(id, edge_types?)`
- `vault_audit()` — orphans, contradictions, stale, cross-link gaps (read-only)
- `confidence_decay(dry_run=true)` — deterministic, reversible via git
- `raw_list()` . `raw_mark_processed(file)`

**Resources** (auto-loaded contract): `_system/AGENTS.md`, `NODE-TYPES.md`, `EDGE-TYPES.md`,
`FRONTMATTER-SCHEMA.md`, `OKF-MAPPING.md`, `INDEX.md`.

**Prompts** (the judgment workflows): `convert-note`, `query-vault`, `organize-vault`,
`vault-health`, `init-vault` — the existing skill bodies, generalized off Claude-only phrasing.

Client configs shipped for Claude Desktop, Cursor, and generic MCP (`stdio`).

Open choice: **Python (FastMCP)** recommended — cleanest frontmatter/graph handling — vs
TypeScript. Flag before Milestone 2.

## 5. Milestones

- **M0 — Foundations (this session):** repo analyzed, this plan, GitHub access wired. *(in progress)*
- **M1 — OKF layer (done):** `OKF-MAPPING.md`, root `index.md` + `okf_version`, ISO 8601 date
  migration, field alias docs.
- **M2 — MCP server:** `mcp-server/` package with tools/resources/prompts + client configs.
- **M3 — De-Claude-ify:** `AGENTS.md` canonical (agents.md convention), `.claude/skills`
  demoted to one adapter, README rewrite around "any AI via MCP + Obsidian reader".
- **M4 — Obsidian reader:** `_system/DASHBOARD.md` (Dataview), graph-view config for typed
  edges, Web Clipper note.
- **M5 — Verification:** `validate.py` (OKF conformance + schema), MCP smoke tests,
  GitHub Action running the validator on push.

## 6. Non-goals

- Not building a hosted service or query infrastructure (OKF non-goal too).
- Not replacing Obsidian's editor — Obsidian stays read/browse only.
- Not inventing a new schema registry — types remain free strings, documented locally.
