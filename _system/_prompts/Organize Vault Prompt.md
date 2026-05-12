# Organize Vault — Periodic Maintenance Prompt

Use this prompt periodically (weekly or bi-weekly) to audit, clean, and strengthen the knowledge graph.

---

## Mission

Scan the entire vault and perform the following maintenance operations:

### 1. Orphan Census
- Find all nodes with zero edges and zero `related` links
- For each orphan: suggest 2-3 connection targets with edges
- If a node is truly standalone, leave it but add a `#standalone` tag

### 2. Contradiction Scan
- Compare nodes within the same namespace for conflicting claims
- Flag contradictory edges between hypothesis/fact/decision nodes
- Report with: `[node A] contradicts [node B] about [topic]`

### 3. Confidence Gaps
- Find nodes where `confidence` is missing, 0.0, or clearly wrong
- Suggest updated values based on available evidence
- Flag nodes where confidence is high but staleness signal is triggered

### 4. Stale Node Detection
- Check `staleness_signal` conditions against current vault state
- Flag nodes where `verified_at` is more than 90 days old
- Prioritize: pillars > decisions > facts > patterns > hypotheses

### 5. Cross-Linking Opportunities
- Find nodes that share 2+ tags but have no edge between them
- Suggest specific edge types and weights with rationale
- Look for implicit hierarchies (patterns implementing pillars, etc.)

### 6. Taxonomy Health
- Check all tags against a master list (compile if missing)
- Flag inconsistent tag spellings (e.g., "AI" vs "ai" vs "artificial-intelligence")
- Suggest merges for near-identical tags

### 7. Visibility Health
- Find nodes missing `visibility`
- Flag nodes where `visibility` conflicts with content sensitivity or namespace scope
- Suggest one of: `public`, `namespace`, `private`, `system`

### 8. Summary Quality
- Scan for summaries over 200 chars or 3+ sentences
- Flag empty or placeholder summaries ("TBD", "description", "1-2 sentences...")
- Flag summaries that don't match the node's content

---

## Output Format

Provide a report in this structure:

```
## Vault Health — [Date]

### Summary
- Total nodes: XX
- Orphans: XX (X%)
- Contradictions: XX
- Stale nodes: XX
- Cross-link opportunities: XX

### Priority Actions (Top 5)
1. [ ] [high] Fix contradiction between `node-a` and `node-b`
2. [ ] [high] Connect orphan `node-c` to the graph
3. [ ] [med]  Update confidence on `node-d` (now verified)
4. [ ] [med]  Merge tags "tag-one" and "tag-1"
5. [ ] [low]  Rewrite summary for `node-e` (too long)

### Details
[For each finding, list: file path, issue, suggested fix]
```

---

## Execution Order

1. INDEX scan (current state baseline)
2. Orphan detection
3. Contradiction analysis
4. Confidence and staleness audit
5. Cross-link suggestions
6. Taxonomy cleanup
7. Visibility review
8. Summary review
9. Deliver report

After the report, ask the human which actions to execute. Never auto-fix without confirmation.
