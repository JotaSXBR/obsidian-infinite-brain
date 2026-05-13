---
name: init-vault
description: >
  Scaffold a fresh Infinite Brain vault from scratch in the current directory.
  Creates all folders, system files, template, and example nodes.
  Invoked with /init-vault.
allowed-tools: Read, Write, Glob
---

# Init Vault — Scaffold a Fresh Infinite Brain

You are creating a new Infinite Brain vault from scratch in the current directory.

## Steps

1. Ask: "What namespace should this vault start with? (e.g. 'personal', 'work', 'research')"
2. Create the 17 root folders:
   `pillars decisions concepts questions playbooks tasks events patterns hypotheses facts sources bookmarks notes contacts references custom raw _system _templates`
3. Create `.gitkeep` in each empty folder so git tracks them.
4. Create `_system/` files:
   - `INDEX.md` — master node index, empty tables per type
   - `NODE-TYPES.md` — definitions for all 16 node types
   - `EDGE-TYPES.md` — definitions for all 10 edge types
   - `FRONTMATTER-SCHEMA.md` — full field reference
   - `LOCAL-TYPES.md` — placeholder for custom types
   - `AGENTS.md` — agent operating rules
   - `_prompts/` — empty folder (skills replace these)
5. Create `_templates/Template - Infinite Node.md` with empty frontmatter.
6. Create `CLAUDE.md` at root pointing agents to `_system/AGENTS.md` and the 4 skills.
7. Create two example nodes in the user's chosen namespace:
   - `pillars/pillar-[namespace]-foundation.md`
   - `decisions/decision-[namespace]-first.md`
   - Wire them with a `supports` edge.
8. Update `_system/INDEX.md` with both example nodes.
9. Confirm: "Vault initialized. X folders created, 2 example nodes wired. Open in Obsidian and run /convert-note to start ingesting content."
