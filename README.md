# Infinite Brain

Five Claude Code skills that give any AI agent infinite, structured memory — built on a typed knowledge graph.

Drop raw material in. Ask questions. The agent builds, maintains, and searches a semantic graph that grows with you.

---

## The Problem

AI agents forget everything between sessions. Personal knowledge systems store information as long, loosely linked documents — fine for humans, broken for agents. They read too much, links don't explain *why* two notes connect, and metadata is too weak for reliable retrieval.

Infinite Brain solves this with a typed knowledge graph where every note is a **node** and every connection is a typed **edge** — structured for agents to navigate, not just humans to browse.

## The Skills

Copy [`.claude/skills/`](.claude/skills) into your project. Five slash commands become available in Claude Code:

| Command | What it does |
|---|---|
| `/init-vault` | Scaffold the memory structure in any directory |
| `/convert-note` | Decompose raw material into atomic typed nodes |
| `/query-vault` | Answer questions via graph traversal (~600 tokens, not ~9000) |
| `/organize-vault` | Interactive audit: orphans, contradictions, stale nodes, gaps |
| `/vault-health auto` | Scheduled maintenance: confidence decay + health report, no prompts |

### Install

```bash
# 1. Copy the skills into your project
cp -r .claude/skills/ /your-project/.claude/skills/

# 2. Open your project in Claude Code
cd /your-project && claude

# 3. Scaffold the memory structure
/init-vault
```

That's it. The vault is created by the skill — you don't clone a template.

### Schedule automated maintenance (optional)

```bash
# Run once to register weekly health checks
/schedule weekly /vault-health auto
```

The `/vault-health auto` skill runs confidence decay and writes a health report node. It never auto-fixes — fixes require human approval via `/vault-health`.

---

## How the Graph Works

Every node is an atomic markdown file with typed frontmatter. Every connection is an explicit edge with direction, weight, and a reason.

**16 node types** — one per note, no ambiguity:

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
| `custom` | Domain-specific (document in `_system/LOCAL-TYPES.md`) |

**10 edge types** — relationships with intent:

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
| `authored_by` | Source created by target |
| `tagged_with` | Categorical organization |

**Trust metadata on every node:**
- `confidence` (0.0–1.0) — how certain is this?
- `verified_at` + `verified_by` — when and who last confirmed it
- `staleness_signal` — the condition that invalidates this node
- `visibility` — `public` / `namespace` / `private` / `system`

---

## This Repo as a Working Example

The vault files in this repository are a live example of the skills in action — two wired nodes, full system schema, and the `_system/INDEX.md` agent entry point. Clone it to see the structure before running `/init-vault` in your own project.

```
.claude/skills/     ← The skills (the actual product)
_system/            ← Agent instructions, schema, workflows, index
_templates/         ← Node template
pillars/            ← Example node
decisions/          ← Example node
raw/                ← Drop unprocessed material here
[14 other folders]  ← Created by /init-vault, tracked via .gitkeep
```

Full agent operating rules: [`_system/AGENTS.md`](_system/AGENTS.md)
Workflow definitions and scheduling: [`_system/WORKFLOWS.md`](_system/WORKFLOWS.md)

---

## Credits & Inspiration

Inspired by the Infinite Brain methodology from [AI Impact](https://www.youtube.com/@AIImpact):

📺 [**How to Build an Infinite Brain with AI**](https://www.youtube.com/watch?v=z02Y-1OvWSM)

## License

[MIT](LICENSE.md)
