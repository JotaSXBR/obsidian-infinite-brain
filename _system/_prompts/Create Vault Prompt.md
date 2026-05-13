You are scaffolding a fresh AI-first knowledge graph vault in Obsidian-compatible markdown. Work in the current directory.

1. Create the following folders at the root: pillars, decisions, concepts, questions, playbooks, tasks, events, patterns, hypotheses, facts, sources, bookmarks, notes, contacts, references, custom, raw, _system, and _templates. `raw/` is an inbox for unprocessed material, not a node type.

2. Inside `_system`, create the operating files: INDEX.md, NODE-TYPES.md, EDGE-TYPES.md, FRONTMATTER-SCHEMA.md, LOCAL-TYPES.md, AGENTS.md, and `_prompts/`.

3. Inside `_templates`, create `Template - Infinite Node.md` with the complete required frontmatter.

4. NODE-TYPES.md must define all 16 node types: pillar, decision, concept, question, playbook, task, event, pattern, hypothesis, fact, source, bookmark, note, contact, reference, custom.

5. EDGE-TYPES.md must define all 10 edge types: related_to, depends_on, derived_from, contradicts, supports, part_of, preceded_by, followed_by, authored_by, tagged_with.

6. FRONTMATTER-SCHEMA.md must list every required and optional field based on this exact structure:
- id: kebab-case string, format type-slug (e.g., hyp-creators-will-pay-29mo)
- title: human-readable string
- type: exact string matching one of the 16 node types
- namespace: string representing the project or area (e.g., product-ops)
- visibility: one of public, namespace, private, system. Default to namespace unless the node is broadly reusable public knowledge, explicitly private, or agent-facing system content.
- summary: exactly 1-2 sentences summarizing the core idea for the agent to read.
- auto_inject: boolean
- applicable_when: string or "Empty"
- confidence: float between 0.0 and 1.0
- verified_at: date (MM/DD/YYYY) or "Empty"
- verified_by: string or "Empty"
- staleness_signal: specific condition that invalidates the node
- tags: array of strings
- edges: array of JSON objects. Each object MUST have: "target" (the id of the linked node), "type" (one of the 10 edge types), "weight" (float 0.0 to 1.0), and "note" (brief string explaining the connection).
- related: array of wikilinks or node ids
- source_url: string or "Empty"

7. INDEX.md is the agent entry point. Include a master markdown table grouped by node type with the following columns: ID | Summary | Edges.

8. Once the structure is created, create one example pillar at pillars/pillar-example-philosophy.md and one example decision at decisions/decision-example-action.md. 

9. Wire the example decision to the example pillar using a typed edge in the JSON array inside the decision's frontmatter edges property. Both example files must stay between 50 and 300 words and include the full required frontmatter.
