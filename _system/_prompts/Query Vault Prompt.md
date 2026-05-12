# Query Vault — Scoped Retrieval Prompt

Use this prompt when you want to ask a question to your Infinite Brain vault. The AI will navigate the knowledge graph using edges and types instead of reading every note, reducing token cost from ~9000 to ~600.

---

## Instructions

1. Read `_system/INDEX.md` first — get the map of what exists.
2. Determine the query scope:
   - If the user names a namespace, prefer nodes from that namespace.
   - If no namespace is named, use `public` nodes and only use `namespace` nodes when their summary clearly matches the query.
   - Use `private` nodes only when the user explicitly asks for private/personal context.
   - Use `system` nodes only for operating the vault, not as answer content unless asked.
3. Identify which node types are likely to contain the answer:
   - "why" questions → `pillar`, `decision`
   - "how" questions → `playbook`, `pattern`
   - "what if" questions → `hypothesis`
   - open unknowns or unresolved curiosities → `question`
   - "what is" questions → `concept`, `fact`
   - "when/where" questions → `event`, `note`
   - "who" questions → `contact`
4. Do NOT read every node. Navigate via edges:
   - Use `supports` and `contradicts` to find polarized positions
   - Use `derived_from` to trace conclusions back to evidence
   - Use `depends_on` to find prerequisites
5. Read only the nodes whose `summary`, `applicable_when`, `namespace`, and `visibility` match the query.
6. Synthesize the answer from the nodes you read, citing node IDs.

## Output Format

### Answer
<direct answer to the question, 1-3 paragraphs>

### Sources
- `[[node-id]]` — <1-line summary of what it contributed>
- `[[node-id]]` — <1-line summary of what it contributed>

### Confidence (aggregate)
Average of source nodes' numeric confidence (0.0–1.0). Based on the same scale used in every node's frontmatter.

### Related Nodes You Could Explore
- `[[node-id]]` — <why it's relevant>
