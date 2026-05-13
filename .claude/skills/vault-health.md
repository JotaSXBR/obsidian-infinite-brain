---
name: vault-health
description: >
  Vault maintenance workflow: confidence decay + full health audit + report node.
  Two modes: interactive (/vault-health) asks before fixing; automated (/vault-health auto)
  only writes the report and decays confidence — zero fixes, zero prompts.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Vault Health — Maintenance Workflow

## Mode Detection

**Check the first argument:**
- No argument → **interactive mode**: run all phases, ask before executing fixes.
- Argument is `auto` → **auto mode**: run phases 1–3 only, stop before phase 4. No questions. No fixes. Write report and exit.

Auto mode is designed for scheduled runs where no human is present.

---

## Phase 1 — Confidence Decay

Safe to run in both modes. Decay is deterministic and reversible via git.

1. Read `_system/INDEX.md` for the full node list.
2. For each node: read frontmatter, calculate days since `verified_at`.
3. Apply decay:

| Days since verified | Action |
|---|---|
| 91–180 | Reduce `confidence` by 0.1 (floor: 0.1) |
| 181–365 | Reduce `confidence` by 0.2 (floor: 0.1) |
| > 365 | Set `confidence` to 0.1, append `needs-review` to tags |
| > 90 AND staleness_signal is triggered | Set `confidence` to 0.1 |

4. Update only the `confidence` field (and `tags` for >365 case). Touch nothing else.
5. Track: nodes scanned, nodes decayed, breakdown by type.

**Skip:** `visibility: system` nodes, `verified_at: "Empty"` nodes, nodes created < 30 days ago.

---

## Phase 2 — Health Audit

Collect findings only. Do not modify any node during this phase.

1. **Orphan Census** — zero edges AND zero `related` links.
2. **Contradiction Scan** — conflicting claims within the same namespace.
3. **Confidence Gaps** — `confidence` missing, 0.0, or high confidence on a triggered staleness signal.
4. **Stale Nodes** — `verified_at` > 90 days. Priority: pillars > decisions > facts > patterns > hypotheses.
5. **Cross-Link Opportunities** — nodes sharing 2+ tags with no edge.
6. **Taxonomy Health** — inconsistent tag spellings, near-duplicate tags.
7. **Visibility Health** — missing `visibility` or visibility conflicting with content sensitivity.
8. **Summary Quality** — summaries > 200 chars, placeholder text, or mismatched content.

---

## Phase 3 — Write Health Report Node

Run in both modes. This is the only write operation in auto mode (besides decay).

Create `notes/note-vault-health-YYYYMMDD.md`:

```yaml
---
id: note-vault-health-YYYYMMDD
title: "Vault Health Report — YYYY-MM-DD"
type: note
namespace: system
visibility: system
summary: "Automated health report: X nodes audited, Y decayed, Z issues found."
auto_inject: false
applicable_when: "Empty"
confidence: 1.0
verified_at: "MM/DD/YYYY"
verified_by: "vault-health-workflow"
staleness_signal: "Superseded by a newer health report node"
tags: ["vault-health", "automated", "maintenance"]
edges: []
related: []
source_url: "Empty"
---

## Vault Health — YYYY-MM-DD

### Mode
auto | interactive

### Decay Summary
- Nodes scanned: XX
- Nodes decayed: XX
- By type: concept: X, decision: X, fact: X, ...

### Audit Summary
- Total nodes: XX
- Orphans: XX | Contradictions: XX | Stale: XX | Cross-link opportunities: XX

### Priority Actions
1. [ ] [high] ...
2. [ ] [med]  ...

### Details
| File | Issue | Suggested fix |
|---|---|---|
```

Update `_system/INDEX.md` with the new note.

---

## Phase 4 — Interactive Fix Loop

**Auto mode: skip this phase entirely. Exit after phase 3.**

Interactive mode only:

Output the Priority Actions list and ask:

"Health report written to `notes/note-vault-health-YYYYMMDD.md`. Which actions should I execute? (reply with numbers, or 'none')"

Execute only what the user selects. For each fix: confirm the change, apply it, mark the action as `[x]` in the report node.
