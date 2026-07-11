"""The five judgment workflows, exposed as MCP prompts. Tool-agnostic:
no slash-command or Claude-specific phrasing. Any MCP client can invoke them."""

CONVERT_NOTE = """You are ingesting raw source material into the Infinite Brain graph.
Read the vault contract first (resource: infinite-brain://system/agents).

1. Call `raw_list` and pick the target file (ask the user if ambiguous). Treat raw files as immutable.
2. Read the file. First triage it (GTD): is any part actionable? Split into knowledge to
   remember, `task` nodes for actions, `reference`/`source` for pointers, and discard noise.
   Tier-1 filtering is deterministic (you decide with simple rules); use a cheap model for
   bulk tagging if the client offers one. Then decompose the keep-pile into ATOMIC nodes —
   one idea per node, 50–300 words.
3. For each node, build frontmatter per infinite-brain://system/frontmatter-schema:
   pick exactly one content type, a kebab-case `id`, a <=200-char `summary`,
   honest `confidence`, a specific `staleness_signal`, 2–8 `tags`, and at least one
   typed `edge` to an existing node (use `graph_query`/`index_read` to find targets).
4. Validate each draft with `node_validate`; fix errors before writing.
5. Stamp provenance: call `raw_hash` on the source file and put the returned hash in each
   derived node's frontmatter (`source_hash`), plus a `derived_from` edge to a `source` node
   representing the original. Then write each node with `node_create`.
6. Call `raw_mark_processed` on the source file.
7. Call `index_rebuild`.
8. Write a log node (type: log) recording operation, affected_nodes, and a one-line summary.
Never merge distinct ideas; err toward more atomic nodes. Never modify raw files by hand."""

QUERY_VAULT = """You are answering a question by traversing the Infinite Brain graph —
read few nodes, not the whole vault.

1. Call `graph_query` with the question (pass namespace/visibility if the user scoped it).
2. From the hits, follow `graph_neighbors` along supports/contradicts/derived_from/depends_on
   to find evidence and counter-positions. Read full nodes only when a hit clearly matches.
3. Never surface `system` nodes as answer content.
4. Answer in: **Answer** (1–3 paragraphs) · **Sources** (node ids + what each contributed) ·
   **Confidence** (mean of source confidences) · **Related nodes to explore**.
5. Offer to save the synthesis as a new node, then write a query-vault log node."""

ORGANIZE_VAULT = """You are auditing the graph for health issues. Never auto-fix.
1. Call `vault_audit` for orphans, integrity errors, stale nodes, and warnings.
2. Call `confidence_decay` and `belief_revision` with dry_run=true to preview both temporal
   decay and memories contradicted by newer, stronger evidence.
3. For each orphan, propose 2–3 concrete edges (target + type + weight).
4. Present a prioritized action list and ask which to apply. Apply only what the user approves
   (via `node_update`), then `index_rebuild` and write an organize-vault log node."""

VAULT_HEALTH = """Maintenance workflow. Two modes.
- interactive: run audit + dry-run decay, present priority actions, apply only approved fixes.
- auto (unattended): call `confidence_decay` and `belief_revision` with dry_run=false, then `vault_audit`, then write a
  health report node (type: note, visibility: system) and `index_rebuild`. NO other fixes, NO prompts.
Decay never deletes and is reversible via git. Every run writes a node — the audit trail lives in the vault."""

INIT_VAULT = """Scaffold a fresh Infinite Brain vault in an empty directory.
1. Ask for the starting namespace.
2. Create the type folders + _system, _templates, raw/processed, logs (with .gitkeep).
3. Copy the schema/contract files into _system and a root OKF `index.md` (okf_version 0.1).
4. Create two wired example nodes (a pillar and a decision, linked by a `supports` edge).
5. `index_rebuild`. Confirm the vault is ready and OKF-conformant."""

REGISTRY = {
    "convert-note": CONVERT_NOTE,
    "query-vault": QUERY_VAULT,
    "organize-vault": ORGANIZE_VAULT,
    "vault-health": VAULT_HEALTH,
    "init-vault": INIT_VAULT,
}
