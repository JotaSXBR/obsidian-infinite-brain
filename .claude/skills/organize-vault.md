---
name: organize-vault
description: >
  Periodic vault maintenance: audit orphans, contradictions, confidence gaps,
  stale nodes, cross-link opportunities, taxonomy health, and summary quality.
  Run weekly or bi-weekly. Invoked with /organize-vault.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Organize Vault — Periodic Maintenance

You are auditing the Infinite Brain knowledge graph for health issues.

## Steps

1. Read `_system/INDEX.md` for current state baseline.
2. Run the 8 checks below.
3. Deliver the report.
4. Ask: "Which of these actions should I execute?" — never auto-fix without confirmation.

## Checks

**1. Orphan Census**
Find nodes with zero edges and zero `related` links. For each: suggest 2-3 connection targets with edge types. If truly standalone, flag with `#standalone`.

**2. Contradiction Scan**
Compare nodes in the same namespace for conflicting claims. Report as: `[node-a] contradicts [node-b] about [topic]`.

**3. Confidence Gaps**
Find nodes where `confidence` is missing, 0.0, or inconsistent with content. Flag nodes with high confidence but a triggered staleness signal.

**4. Stale Node Detection**
Check `staleness_signal` conditions. Flag nodes where `verified_at` is over 90 days old. Priority: pillars > decisions > facts > patterns > hypotheses.

**5. Cross-Link Opportunities**
Find nodes sharing 2+ tags with no edge. Suggest specific edge types and weights.

**6. Taxonomy Health**
Compile tag list. Flag inconsistent spellings (e.g. "AI" vs "ai"). Suggest merges for near-identical tags.

**7. Visibility Health**
Find nodes missing `visibility`. Flag conflicts between content sensitivity and current visibility setting.

**8. Summary Quality**
Flag summaries over 200 chars, placeholder text ("TBD", "1-2 sentences..."), or summaries that don't match node content.

## Output Format

```
## Vault Health — [Date]

### Summary
- Total nodes: XX | Orphans: XX | Contradictions: XX | Stale: XX | Cross-link opportunities: XX

### Priority Actions (Top 5)
1. [ ] [high] ...
2. [ ] [med]  ...
...

### Details
[File path | Issue | Suggested fix]
```

## After Execution

After delivering the report and applying any user-selected fixes:

Write a log node to `logs/log-organize-vault-YYYYMMDD-HHmmss.md` using the log schema from `_system/FRONTMATTER-SCHEMA.md`:
- `operation: organize-vault`
- `affected_nodes`: node IDs modified (empty array if user selected "none")
- `summary`: one sentence — node count, issue count, fixes applied
- Body (30–80 words): total nodes audited, how many issues found per check, how many fixes the user approved and applied.
