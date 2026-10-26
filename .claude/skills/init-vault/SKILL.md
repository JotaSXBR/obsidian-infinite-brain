---
name: init-vault
description: >
  Scaffold a fresh Infinite Brain vault from scratch in the current directory.
  Creates all folders, system files, template, and example nodes.
  Invoked with /init-vault [namespace].
argument-hint: "[namespace]"
allowed-tools: Read, Write, Glob
---

# Init Vault — Scaffold a Fresh Infinite Brain

You are creating a new Infinite Brain vault from scratch in the current directory.

Namespace: $ARGUMENTS

## Steps

1. Check for an existing vault: if `_system/INDEX.md` already exists, stop and say "A vault already exists here — run /vault-health to audit it instead." Never overwrite an existing vault.
2. If the namespace above is empty, ask: "What namespace should this vault start with? (e.g. 'personal', 'work', 'research')". Normalize it to kebab-case.
3. Create the 21 folders:
   - 16 content folders: `pillars decisions concepts questions playbooks tasks events patterns hypotheses facts sources bookmarks notes contacts references custom`
   - 5 operational folders: `raw raw/processed logs _system _templates`
4. Create `.gitkeep` in each empty folder so git tracks them (the Write tool creates parent folders).
5. Create `_system/` files:
   - `INDEX.md` — master node index, one section per content type with `*No nodes created yet.*`, plus a `log` section stating logs are not indexed
   - `NODE-TYPES.md` — definitions for the 16 content types plus the operational `log` type
   - `EDGE-TYPES.md` — definitions for all 10 edge types
   - `FRONTMATTER-SCHEMA.md` — full field reference, including the reduced log node schema
   - `LOCAL-TYPES.md` — placeholder for custom types
   - `AGENTS.md` — agent operating rules
   - `WORKFLOWS.md` — scheduled and on-demand workflow definitions (`/vault-health auto` weekly, `/convert-note` on demand)
   - `_prompts/.gitkeep` — empty folder (skills replace these)
6. Create `_templates/Template - Infinite Node.md` with empty frontmatter.
7. Create `CLAUDE.md` at root pointing agents to `_system/AGENTS.md` and the 5 skills (`/init-vault`, `/convert-note`, `/query-vault`, `/organize-vault`, `/vault-health`).
8. Create two example nodes in the chosen namespace:
   - `pillars/pillar-[namespace]-foundation.md`
   - `decisions/decision-[namespace]-first.md`
   - Wire them with reciprocal `supports` edges so neither is an orphan.
9. Update `_system/INDEX.md` with both example nodes.
10. Write a log node to `logs/log-init-vault-YYYYMMDD-HHmmss.md` using the log schema (`operation: init-vault`, `affected_nodes` = the two example node IDs).
11. Confirm: "Vault initialized. 21 folders created, 2 example nodes wired. Open in Obsidian, drop files into `raw/`, and run /convert-note to start ingesting content."
