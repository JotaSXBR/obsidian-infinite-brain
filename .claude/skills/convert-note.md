---
name: convert-note
description: >
  Ingest raw content from raw/ and decompose it into atomic Infinite Brain nodes
  with typed frontmatter and typed edges. Use when you have raw material to process.
  Invoked with /convert-note.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Convert Note — Raw-to-Atomic Decompiler

You are ingesting raw content from the `raw/` folder into the Infinite Brain knowledge graph.

## Steps

1. Ask: "Which file in `raw/` should I convert? (or 'all' to process everything)"
2. Scan the target file(s) with Read. Treat source files as immutable — do not modify them.
3. Decompose into atomic nodes — one concept per node, 50-300 words each.
4. For each node:
   - Classify with exactly one of the 16 content types: `pillar decision concept question playbook task event pattern hypothesis fact source bookmark note contact reference custom`
   - Assign a unique `id` in `type-descriptive-slug` format (kebab-case)
   - Populate all frontmatter fields from `_system/FRONTMATTER-SCHEMA.md`
   - Wire to at least one other node using the 10 edge types: `related_to depends_on derived_from contradicts supports part_of preceded_by followed_by authored_by tagged_with`
   - Place in the correct folder: `type: concept` → `concepts/<id>.md`
5. Write each node file.
6. **Mandatory:** Append each new node's row to `_system/INDEX.md` under the correct type section.
7. Move the processed source file from `raw/` to `raw/processed/` (e.g., `raw/article.md` → `raw/processed/article.md`).
8. Write a log node to `logs/log-convert-note-YYYYMMDD-HHmmss.md` using the log schema from `_system/FRONTMATTER-SCHEMA.md`:
   - `operation: convert-note`
   - `affected_nodes`: list of all node IDs created
   - `summary`: one sentence — source file name + node count
   - Body (30–80 words): what was processed, what nodes were created, any notable decisions made during decomposition.
9. Confirm: "Converted X nodes from `raw/filename`. Original moved to `raw/processed/`. Log written."

## Rules

- Never merge concepts — err toward more atomic nodes.
- `summary` must be 1-2 sentences under 200 chars.
- `confidence` must reflect actual certainty from the source.
- `visibility` defaults to `namespace` unless clearly indicated otherwise.
- `staleness_signal` must be a specific observable condition.
- Do NOT create nodes with `type: raw`.
- Always check `_system/INDEX.md` to avoid duplicate IDs before writing.
