# Edge Types Reference

This document defines all valid edge types within the Obsidian knowledge graph vault. Edges represent directed relationships between two nodes via their `id` fields.

---

## Core Relationship Edges

### 1. related_to
Bidirectional or loosely associated connection. Used when two nodes share thematic overlap but lack a stronger semantic bond.

**Example:** A concept "compound interest" is `related_to` a decision about reinvestment strategy.

---

### 2. depends_on
Indicates that the source node cannot proceed, be validated, or be meaningfully understood without the target node first being established or resolved.

**Example:** A hypothesis node `depends_on` a fact node that provides baseline data.

---

### 3. derived_from
The source node was created by analyzing, inferring, or synthesizing the target node. Common from data-to-insight flows.

**Example:** A pattern node is `derived_from` three separate fact nodes.

---

### 4. contradicts
The source node stands in opposition or tension with the target node. Use for debate tracking and hypothesis conflicts.

**Example:** Hypothesis A `contradicts` Hypothesis B in their predicted outcome.

---

### 5. supports
The source node provides evidence, justification, or logical backing for the target node. Opposite direction of `contradicts`.

**Example:** A fact node `supports` a decision node by providing data-backed rationale.

---

### 6. part_of
The source node is a component or sub-element of the target node. Used for hierarchical decomposition.

**Example:** A task node `part_of` a playbook node.

---

## Temporal / Sequential Edges

### 7. preceded_by
Indicates the source node occurred after the target node in time or in a logical sequence.

**Example:** A decision node is `preceded_by` a discovery event.

---

### 8. followed_by
Indicates the source node occurred before the target node in time or in a logical sequence.

**Example:** A hypothesis node is `followed_by` a validation experiment.

---

## Attribution / Tagging Edges

### 9. authored_by
Links a node to the person or organization, represented as a contact node, that created or owns it.

**Example:** A decision node is `authored_by` contact: alice-chen.

---

### 10. tagged_with
Categorical association for filtering, grouping, or taxonomy purposes. Unlike `related_to`, `tagged_with` is strictly organizational.

**Example:** A fact node is `tagged_with` ["data", "finance", "Q1-2026"].

---

## Edge Weight Guidelines

| Weight Range | Meaning |
|---|---|
| 0.0 – 0.3 | Weak or circumstantial connection |
| 0.4 – 0.6 | Moderate correlation or partial support |
| 0.7 – 1.0 | Strong, well-evidenced relationship |

- Weights are set by the author at creation time and should be revisited when new evidence emerges.
- Agents should weight edges proportionally when inferring or summarizing.
- Edges with weight 0.0 should be treated as placeholders awaiting evidence.

---

## Edge Validity Rules

- Every edge must specify `target` (valid node id), `type` (one of the 10 above), `weight` (0.0–1.0), and `note`.
- Self-referencing edges (`target` equals source `id`) are invalid.
- Duplicate edge types between the same pair of nodes should be merged or disambiguated with a note.
- Edge type must be lowercase, and must match the canonical name above exactly.
