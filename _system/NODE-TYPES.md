# Node Types Reference

This document defines all valid node types within the Obsidian knowledge graph vault.

---

## Core Entity Types

### 1. pillar
The foundational belief, value, or strategic principle that grounds all downstream decisions and actions. Pillars are rarely changed and serve as the "why" behind everything.

### 2. decision
A recorded choice made (or to be made) with explicit context, alternatives considered, and outcome rationale. Decisions are time-bound and should be revisitable.

### 3. concept
An abstract idea, mental model, or framework. Concepts anchor understanding and enable cross-domain reasoning.

### 4. question
A known unknown being tracked. Questions preserve uncertainty, open inquiry, and may become hypotheses once testable.

### 5. playbook
A repeatable procedure or runbook for producing expected outcomes. Playbooks encode institutional knowledge and reduce decision fatigue.

### 6. task
An actionable item, usually synced from or mapped to a real task system.

### 7. event
A dated event the agent should reason about temporally.

### 8. pattern
An observed regularity in data or behavior. Patterns provide structural guidance for new problems.

---

## Evidential / Informational Types

### 9. hypothesis
An assumption or testable prediction with a measurable validation path.

### 10. fact
An immutable, verifiable statement backed by data or an authoritative source. Facts are ground truth within the graph.

### 11. source
A reference to an external origin — article, book, podcast, talk, paper, dataset — that informs one or more nodes in the graph.

### 12. bookmark
A saved link or pointer to a resource that has not yet been processed into a full node. Bookmarks are raw capture.

### 13. note
A freeform capture — meeting notes, fleeting thoughts, scratchpad entries. Notes may later be promoted into richer nodes.

---

## Relational / Structural Types

### 14. contact
A named person with associated metadata (team, expertise, availability). Contacts are referenced by edge connections.

### 15. reference
A generic cross-link or glossary entry used to standardize terminology and reduce duplication across nodes.

### 16. custom
An ad-hoc node type for domain-specific entities that do not fit the above taxonomy. Custom types should be documented locally in `_system/LOCAL-TYPES.md` with rationale.

---

## Operational Types

### 17. log
A lightweight, immutable record of a single skill execution. Logs are written automatically by skills (`/convert-note`, `/query-vault`, `/organize-vault`) at the end of each operation. They use a reduced frontmatter schema (8 fields, no edges, no confidence decay) and live in `logs/`. See `_system/FRONTMATTER-SCHEMA.md` for the log-specific schema.

Logs are never edited after creation. They are the operational audit trail of the vault.

---

## Type Assignment Guidelines

- Every node **must** have exactly one `type` in its frontmatter.
- Type must be lowercase, singular, and match the canonical name above exactly.
- Do not create new types without updating `NODE-TYPES.md` and `FRONTMATTER-SCHEMA.md` first.
- Types are used by agents to determine interaction patterns, rendering, and edge validity.
- `log` nodes use a reduced schema — do not apply the full frontmatter checklist to them.
