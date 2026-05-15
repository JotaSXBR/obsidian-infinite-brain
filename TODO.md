# TODO — Future Improvements

This file tracks planned enhancements that are out of scope for the current skill set but worth implementing as the vault matures.

---

## Tool Ecosystem

Infinite Brain was designed to replace Claude Code's session memory with a persistent, structured knowledge graph. The skills work entirely with the official Claude Code toolchain (Read, Write, Edit, Glob, Grep). The tools below are optional enhancements that would improve how humans browse and interact with the vault — they do not affect agent behavior.

### qmd — Local Semantic Search

**What it is:** A local markdown search engine with BM25/vector hybrid ranking and LLM re-ranking.

**What it improves:** `/query-vault` currently traverses the graph via INDEX.md and typed edges. qmd would add full-text + semantic search as a complementary retrieval path — useful when the user doesn't know the exact node type or edge path to follow. Especially valuable as the vault grows past ~200 nodes where INDEX.md scanning becomes slower.

**Implementation:** Run as a local CLI alongside Claude Code. Point at the vault root. Call from `/query-vault` as a first-pass retrieval step before edge traversal.

---

### Obsidian Web Clipper — Source Ingestion

**What it is:** A browser extension that converts web articles to clean markdown and saves them directly into the vault.

**What it improves:** Currently, the user manually drops files into `raw/`. Web Clipper automates this for web content — clip an article in the browser, it lands in `raw/` with frontmatter pre-populated (URL, title, date). Reduces friction between reading and processing.

**Implementation:** Configure Web Clipper to save to `raw/` with a filename template like `raw/YYYY-MM-DD-source-title.md`. No changes needed to `/convert-note`.

---

### Obsidian Graph View — Visual Navigation

**What it is:** Obsidian's built-in graph visualizer that renders all wikilinks and frontmatter connections as an interactive node graph.

**What it improves:** The vault is already Obsidian-compatible. Graph View gives the human a live visual map of how nodes are connected — useful for spotting orphans, dense clusters, and missing bridges at a glance. Complements `/organize-vault` by making structural issues visible without running an audit.

**Implementation:** Open the vault folder in Obsidian. No configuration needed — Graph View reads the existing `[[wikilinks]]` and `related` fields automatically.

---

### Marp — Slide Generation

**What it is:** A markdown-based presentation generator. Converts markdown files to slides with a simple directive.

**What it improves:** Allows the user to export vault content (a `playbook`, a `decision`, a cluster of `facts`) directly into slides for sharing — without leaving the markdown ecosystem. Useful for turning a knowledge artifact into a deliverable.

**Implementation:** Add `marp: true` to a node's frontmatter to enable slide mode. Run `marp <file>.md` to export. No changes to vault structure needed.

---

### Dataview — Dynamic Tables from Frontmatter

**What it is:** An Obsidian plugin that queries frontmatter fields and renders dynamic tables and lists inside notes.

**What it improves:** Enables live dashboards inside the vault — e.g., "all nodes where confidence < 0.5", "all decisions in namespace product-ops verified before 2026", "all questions without edges". Complements `/organize-vault` by giving the human a persistent, self-updating view of vault health without running a skill.

**Implementation:** Install Dataview in Obsidian. Write Dataview queries as inline code blocks in `_system/INDEX.md` or a dedicated `_system/DASHBOARD.md`. No changes to node schema needed — it reads existing frontmatter fields.

---

## Other Planned Work

- **`_system/DASHBOARD.md`** — A human-facing summary view of vault health, using Dataview queries if available, or manually updated stats otherwise.
- **GitHub Actions integration** — Automate `/vault-health auto` on a weekly cron via `.github/workflows/vault-health.yml`. See `_system/WORKFLOWS.md` for the workflow definition.
- **Multi-agent routing** — Extend `_system/AGENTS.md` with role definitions for specialized agents (ingestion agent, query agent, maintenance agent) that can operate concurrently without conflicting writes.
