---
name: query-vault
description: >
  Answer a question by navigating the knowledge graph via typed edges and visibility
  filters. Reduces token cost from ~9000 to ~600 by traversing selectively.
  Invoked with /query-vault.
allowed-tools: Read, Write, Glob, Grep
---

# Query Vault — Scoped Graph Retrieval

You are answering a question by navigating the Infinite Brain knowledge graph.

## Steps

1. Ask: "What would you like to know?"
2. Read `_system/INDEX.md` — get the full map of existing nodes.
3. Determine scope:
   - Named namespace → prefer nodes from that namespace
   - No namespace → use `public` nodes; use `namespace` nodes only if summary clearly matches
   - Explicit private request → use `private` nodes
   - Never present `system` nodes as answer content
4. Select likely node types based on question shape:
   - "why" → `pillar`, `decision`
   - "how" → `playbook`, `pattern`
   - "what if" → `hypothesis`
   - "what is" → `concept`, `fact`
   - "when/where" → `event`, `note`
   - "who" → `contact`
   - open unknowns → `question`
5. Navigate via edges — do NOT read every node:
   - `supports` / `contradicts` → find polarized positions
   - `derived_from` → trace conclusions to evidence
   - `depends_on` → find prerequisites
6. Read only nodes whose `summary`, `applicable_when`, `namespace`, and `visibility` match.
7. Synthesize and output in this format:

---

### Answer
<direct answer, 1-3 paragraphs>

### Sources
- `[[node-id]]` — <what it contributed>

### Confidence
<average of source nodes' confidence values, 0.0–1.0>

### Related Nodes to Explore
- `[[node-id]]` — <why it's relevant>

---

Ask: "Would you like to save this as a synthesis node?"

8. Write a log node to `logs/log-query-vault-YYYYMMDD-HHmmss.md` using the log schema from `_system/FRONTMATTER-SCHEMA.md`:
   - `operation: query-vault`
   - `affected_nodes`: node IDs read during traversal
   - `summary`: one sentence — the question asked (truncated to 100 chars if needed)
   - Body (30–80 words): question asked, nodes traversed, confidence returned, whether a synthesis node was saved.
