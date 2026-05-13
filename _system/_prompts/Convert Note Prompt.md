# Convert Note — Raw-to-Atomic Decompiler

Use this prompt to ingest raw content from the `raw/` folder and decompose it into atomic Infinite Brain nodes. The AI scans `raw/`, processes each file, and outputs individual markdown nodes with proper frontmatter and edges into the appropriate folders.

---

## Instructions

1. Scan all files inside the `raw/` directory.
2. For each file, decompose it into atomic concepts — each 50-300 words, one idea per node. Do NOT exceed 300 words per node; longer notes defeat scoped retrieval.
3. Classify each node with exactly one of the 16 types:
   `pillar`, `decision`, `concept`, `question`, `playbook`, `task`, `event`,
   `pattern`, `hypothesis`, `fact`, `source`, `bookmark`, `note`, `contact`,
   `reference`, `custom`
4. Assign a unique `id` in `type-descriptive-slug` format.
5. Populate all required frontmatter fields per `_system/FRONTMATTER-SCHEMA.md`.
6. Wire nodes together using the 10 edge types:
   `related_to`, `depends_on`, `derived_from`, `contradicts`, `supports`,
   `part_of`, `preceded_by`, `followed_by`, `authored_by`, `tagged_with`
7. Every node MUST have at least one edge to another node in the output set or to an existing node in the vault.
8. Place each node file in its corresponding folder:
   - `type: pillar` → `pillars/<id>.md`
   - `type: decision` → `decisions/<id>.md`
   - `type: concept` → `concepts/<id>.md`
   - `type: question` → `questions/<id>.md`
   - `type: playbook` → `playbooks/<id>.md`
   - `type: task` → `tasks/<id>.md`
   - `type: event` → `events/<id>.md`
   - `type: pattern` → `patterns/<id>.md`
   - `type: hypothesis` → `hypotheses/<id>.md`
   - `type: fact` → `facts/<id>.md`
   - `type: source` → `sources/<id>.md`
   - `type: bookmark` → `bookmarks/<id>.md`
   - `type: note` → `notes/<id>.md`
   - `type: contact` → `contacts/<id>.md`
   - `type: reference` → `references/<id>.md`
   - `type: custom` → `custom/<id>.md`

## Rules

- Never merge concepts — err on the side of more atomic nodes.
- `summary` must be 1-2 sentences, under 200 chars.
- `confidence` must reflect actual certainty from the source text.
- `visibility` must be one of `public`, `namespace`, `private`, or `system`; default to `namespace` unless the source clearly indicates another scope.
- `staleness_signal` must be a specific observable condition.
- `tags`: 2-8 per node, lowercase kebab-case.
- `namespace`: infer from the content domain.
- `raw/` is only an inbox. Do not create nodes with `type: raw`.
- **MANDATORY:** After creating every node, you MUST append the node's `id`, `summary`, and edge count to the master table in `_system/INDEX.md` under the correct type section. If the index is not updated, the scoped retrieval in the Query Prompt will fail and the vault becomes blind.

## Output Format

Return each node as a complete markdown file block separated by `===`.

=== nodes: concepts/my-new-concept.md ===
---frontmatter---
# Title
body (50-300 words)
===

=== nodes: facts/my-new-fact.md ===
...repeat for each node...
