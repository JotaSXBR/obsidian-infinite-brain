# Frontmatter Schema Reference

Every node in the vault must include a frontmatter block at the top of the markdown file. Fields marked **required** are mandatory; fields marked **optional** may be omitted but should be populated when available.

---

## Complete Field Specification

### id
- **Type:** string
- **Format:** `type-slug` in kebab-case (e.g., `hyp-creators-will-pay-29mo`)
- **Required:** yes
- **Notes:** Must be unique across the entire vault. Combine node type abbreviation with a descriptive slug. No spaces, no uppercase (except acronyms in slug).

### title
- **Type:** string
- **Required:** yes
- **Notes:** Human-readable, 5–80 characters. Should be recognizably unique across nodes of the same type.

### type
- **Type:** string
- **Required:** yes
- **Allowed Values:** exactly one of: `pillar`, `decision`, `concept`, `question`, `playbook`, `task`, `event`, `pattern`, `hypothesis`, `fact`, `source`, `bookmark`, `note`, `contact`, `reference`, `custom`, `log`
- **Notes:** Must match the canonical name in `NODE-TYPES.md` exactly (lowercase, singular).

### namespace
- **Type:** string
- **Required:** yes
- **Notes:** Represents the project, team, or domain area. Use kebab-case (e.g., `product-ops`, `growth`, `infra`). Enables scoped filtering and reduces cross-namespace collisions.

### visibility
- **Type:** string
- **Required:** yes
- **Allowed Values:** exactly one of: `public`, `namespace`, `private`, `system`
- **Default:** `namespace`
- **Notes:** Controls when an AI agent may use the node during retrieval. Use `public` for broadly reusable knowledge, `namespace` for content that should only be used inside its namespace, `private` for sensitive or personal material, and `system` for vault instructions or agent-facing operating rules.

### summary
- **Type:** string
- **Required:** yes
- **Length:** 1–2 sentences maximum (aim for under 200 characters)
- **Notes:** Written for an AI agent scanning the graph. Must convey the core idea at a glance. Avoid jargon unless defined in a concept node.

### auto_inject
- **Type:** boolean
- **Required:** yes
- **Allowed Values:** `true` or `false`
- **Notes:** When `true`, the system may automatically insert related content or triggers into this node. Default to `false` unless explicitly designed for automation hooks.

### applicable_when
- **Type:** string
- **Default:** `"Empty"`
- **Notes:** Describes the context or trigger conditions under which this node becomes relevant. Use `"Empty"` if the node is universally applicable or context-independent.

### confidence
- **Type:** float
- **Range:** 0.0 to 1.0
- **Required:** yes
- **Notes:** Reflects the author's confidence in the node's accuracy or validity. 1.0 = certain, 0.0 = pure speculation. Revisit and update as evidence accumulates.

### verified_at
- **Type:** string (date)
- **Format:** `MM/DD/YYYY`
- **Default:** `"Empty"`
- **Notes:** Date on which the node's content or conclusions were last reviewed or confirmed by a human. Use `"Empty"` until first verification.

### verified_by
- **Type:** string
- **Default:** `"Empty"`
- **Notes:** Name or id of the person who last verified this node. Use `"Empty"` until verified.

### staleness_signal
- **Type:** string
- **Required:** yes
- **Notes:** A specific, observable condition that, if met, indicates this node may be outdated, incorrect, or invalidated. Write it as a conditional statement (e.g., "If revenue growth drops below 5% for two consecutive quarters, re-evaluate this assumption"). Agents should monitor for staleness signals.

### tags
- **Type:** array of strings
- **Required:** yes
- **Notes:** Array syntax: `["tag-one", "tag-two"]`. Tags are lowercase, kebab-case. Include 2–8 relevant tags. Tags are used for filtering and cross-referencing.

### edges
- **Type:** array of JSON objects
- **Required:** yes
- **Structure:** Each object must contain exactly four keys:

| Key | Type | Notes |
|---|---|---|
| `target` | string | The `id` of the destination node |
| `type` | string | One of the 10 edge types from `EDGE-TYPES.md` |
| `weight` | float | 0.0 to 1.0, indicating relationship strength |
| `note` | string | Brief explanation of the connection |

- **Example:**

```yaml
edges: [
  {"target": "pillar-example-philosophy", "type": "related_to", "weight": 0.7, "note": "Provides grounding for this decision"}
]
```

### related
- **Type:** array of strings
- **Required:** no
- **Notes:** Wikilinks (`[[Node Title]]`) or bare node ids for casual cross-references that don't warrant a formal edge. Useful for discovery and browsing.

### source_url
- **Type:** string
- **Default:** `"Empty"`
- **Notes:** URL of the external resource this node was derived from, if any. Use `"Empty"` when no source applies.

---

## Example Frontmatter Block

```yaml
---
id: hyp-creators-will-pay-29mo
title: Creators Will Pay for Analytics After 29 Months
type: hypothesis
namespace: product-ops
visibility: namespace
summary: Creators who have been posting consistently for 29+ months are more likely to convert to paid analytics tiers than newer creators.
auto_inject: false
applicable_when: When evaluating creator monetization strategies
confidence: 0.65
verified_at: 03/15/2026
verified_by: Alice Chen
staleness_signal: If free tier retention exceeds 60% at 12 months, re-evaluate
tags: ["creator-economy", "monetization", "analytics", "conversion"]
edges: [
  {"target": "fact-cohort-retention-q4", "type": "derived_from", "weight": 0.8, "note": "Cohort data directly informs this hypothesis"},
  {"target": "decision-analytics-pricing", "type": "contradicts", "weight": 0.5, "note": "Pricing model assumes shorter conversion window"}
]
related: ["[[fact-cohort-retention-q4]]", "decision-analytics-pricing"]
source_url: "Empty"
---
```

---

---

## Log Node Schema

`log` nodes use a reduced schema designed for minimal token cost. Do NOT apply the full frontmatter checklist to log nodes.

### Fields

| Field | Type | Notes |
|---|---|---|
| `id` | string | Format: `log-[operation]-[YYYYMMDD-HHmmss]` (e.g., `log-convert-note-20260515-143022`) |
| `type` | string | Always `log` |
| `operation` | string | One of: `convert-note`, `query-vault`, `organize-vault`, `vault-health`, `init-vault` |
| `date` | string | ISO 8601: `"YYYY-MM-DDTHH:MM:SS"` |
| `namespace` | string | Namespace(s) affected, or `"vault"` if global |
| `summary` | string | One sentence, under 150 chars |
| `affected_nodes` | array | Node IDs created or modified. Empty array `[]` if none. |
| `tags` | array | Always includes `"log"` and the operation name |

### Example

```yaml
---
id: log-convert-note-20260515-143022
type: log
operation: convert-note
date: "2026-05-15T14:30:22"
namespace: personal
summary: "Processed raw/karpathy-llm-wiki.md → 3 nodes created (concept, source, fact)"
affected_nodes: ["concept-llm-wiki-pattern", "source-karpathy-llm-wiki", "fact-rag-vs-compounding"]
tags: ["log", "convert-note"]
---
```

### Body

Log body should be 30–80 words. Cover: what ran, what changed, any notable finding or error. No markdown headers — plain prose.

### Rules

- Log nodes are **never edited** after creation.
- Log nodes are **not indexed** in `_system/INDEX.md` — the `logs/` folder is self-contained.
- Log nodes are **not subject to confidence decay** in `/vault-health`.
- Log nodes have `visibility: system` implicitly — agents do not use them for query answers.

---

## Field-by-Field Validation Checklist

- [ ] `id` is unique, kebab-case, prefixed with type
- [ ] `title` is non-empty, human-readable
- [ ] `type` matches one of the 16 canonical types
- [ ] `namespace` is kebab-case
- [ ] `visibility` is one of `public`, `namespace`, `private`, `system`
- [ ] `summary` is 1–2 sentences, under 200 chars
- [ ] `auto_inject` is boolean
- [ ] `applicable_when` is a string or `"Empty"`
- [ ] `confidence` is between 0.0 and 1.0
- [ ] `verified_at` is MM/DD/YYYY or `"Empty"`
- [ ] `verified_by` is a string or `"Empty"`
- [ ] `staleness_signal` is a non-empty conditional string
- [ ] `tags` is a non-empty array of kebab-case strings
- [ ] `edges` is a non-empty array of objects with `target`, `type`, `weight`, `note`
- [ ] `related` is an array of wikilinks or ids (optional)
- [ ] `source_url` is a URL string or `"Empty"`
