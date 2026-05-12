# Infinite Brain Vault

An AI-first Obsidian vault that turns your notes into a typed knowledge graph — built for agents to read, retrieve, and reason over with precision.

## What Is This

Most personal knowledge systems store information as long, loosely linked documents. That works fine for humans browsing manually, but it fails when AI agents need to retrieve context. Agents read too much, links don't explain *why* two notes connect, and metadata is too weak for reliable scoped retrieval.

Infinite Brain Vault solves this with five design principles:

1. **Atomic nodes** — one concept per note, 50–300 lines max.
2. **Typed nodes** — every note is one of 16 canonical types (decision, concept, hypothesis, fact, etc.).
3. **Typed edges** — relationships are explicit, directional, and weighted.
4. **Trust metadata** — each node carries confidence, verification date, and staleness signals.
5. **Namespaced visibility** — agents filter context by scope before reading content.

This repository is a **starter vault**. Clone it, open it in Obsidian, and start building your own AI-optimized second brain.

## Quick Start

1. **Clone** this repository (or use the "Use this template" button):
   ```bash
   git clone https://github.com/JotaSXBR/obsidian-infinite-brain.git
   ```
2. **Open** the cloned folder as a vault in [Obsidian](https://obsidian.md).
3. **Read** `_system/INDEX.md` to see the current state of the graph.
4. **Create** your first node using the template in `_templates/Template - Infinite Node.md`.
5. **Drop** raw material into the `raw/` folder and use the Convert Note prompt to break it into atomic nodes.

## Vault Structure

```
pillars/        Foundational beliefs and principles
decisions/      Recorded choices with rationale
concepts/       Ideas, models, and frameworks
questions/      Known unknowns and open inquiries
playbooks/      Repeatable procedures
tasks/          Actionable items
events/         Dated occurrences
patterns/       Observed regularities
hypotheses/     Testable assumptions
facts/          Verified statements
sources/        External origins and references
bookmarks/      Saved but unprocessed links
notes/          Freeform captures
contacts/       People or organizations
references/     Glossary, schema, or pinned data
custom/         Domain-specific node types
raw/            Unprocessed inbox (not a node type)
_system/        Schema, ontology, prompts, agent instructions
_templates/     Reusable note templates
```

## Node Types

Every node declares exactly one `type` in its frontmatter:

| Type | Purpose |
|---|---|
| `pillar` | Foundational belief or value |
| `decision` | Recorded choice with rationale |
| `concept` | Abstract idea or mental model |
| `question` | Known unknown being tracked |
| `playbook` | Repeatable procedure |
| `task` | Actionable item |
| `event` | Timestamped occurrence |
| `pattern` | Recurring validated solution |
| `hypothesis` | Testable assumption |
| `fact` | Verifiable ground truth |
| `source` | External origin reference |
| `bookmark` | Saved link (unprocessed) |
| `note` | Freeform capture |
| `contact` | Named person with metadata |
| `reference` | Glossary or terminology link |
| `custom` | Domain-specific (documented in `_system/LOCAL-TYPES.md`) |

Full definitions: [`_system/NODE-TYPES.md`](_system/NODE-TYPES.md)

## Edge Types

Edges are directional relationships between nodes. Each edge has a `target`, `type`, `weight` (0.0–1.0), and `note`.

| Edge | Meaning |
|---|---|
| `supports` | Source backs target |
| `contradicts` | Source opposes target |
| `depends_on` | Source requires target |
| `derived_from` | Source synthesized from target |
| `related_to` | Loose thematic association |
| `part_of` | Source is sub-component of target |
| `preceded_by` | Source happened after target |
| `followed_by` | Source happened before target |
| `authored_by` | Source created by target (person) |
| `tagged_with` | Categorical organization |

Full reference: [`_system/EDGE-TYPES.md`](_system/EDGE-TYPES.md)

## Included Prompts

The vault ships with four operational prompts in [`_system/_prompts/`](_system/_prompts):

| Prompt | What it does |
|---|---|
| **Create Vault** | Scaffold a fresh vault from scratch |
| **Convert Note** | Decompose raw content into atomic typed nodes |
| **Query Vault** | Retrieve answers using scoped graph traversal |
| **Organize Vault** | Audit and maintain graph health |

## How It Works With AI Agents

The structured frontmatter on every node enables AI agents (Claude, Cursor, Copilot, etc.) to:

- **Filter by visibility** — agents only read nodes appropriate to the current scope (`public`, `namespace`, `private`, `system`).
- **Traverse typed edges** — instead of guessing relationships, agents follow explicit, weighted connections between nodes.
- **Assess trust** — `confidence`, `verified_at`, and `staleness_signal` let agents weigh information quality before using it.
- **Scope by namespace** — agents avoid cross-contaminating context between unrelated projects.

Point your agent at `_system/AGENTS.md` for the full operating prompt, or use the included prompts to create, convert, query, and organize nodes.

## Credits & Inspiration

This project was inspired by the Infinite Brain methodology presented by [AI Impact](https://www.youtube.com/@AIImpact) in this video:

📺 [**How to Build an Infinite Brain with AI**](https://www.youtube.com/watch?v=z02Y-1OvWSM)

## License

This project is released under the [MIT License](LICENSE.md).
