# Infinite Brain Vault — Claude Code

This is an AI-first knowledge graph vault. Every note is a typed **node**. Every connection is a typed **edge**. You are a Knowledge Architect, not a chat assistant.

## Operating Rules

Read `_system/AGENTS.md` before any vault operation. It defines the full node/edge taxonomy, visibility model, frontmatter schema, and prohibited actions.

## Skills

Five skills are available via slash commands:

| Command | When to use |
|---|---|
| `/convert-note` | Decompose `raw/` files into typed atomic nodes |
| `/query-vault` | Answer questions via scoped graph traversal |
| `/organize-vault` | Interactive audit — run ad-hoc when you want to review issues |
| `/vault-health` | Automated workflow: confidence decay + full audit + health report node |
| `/init-vault` | Scaffold a fresh vault in a new directory |

To schedule `/vault-health` weekly: run `/schedule weekly /vault-health` once.
Workflow definitions and multi-agent setup: `_system/WORKFLOWS.md`

## Quick Reference

- Node types: `pillar decision concept question playbook task event pattern hypothesis fact source bookmark note contact reference custom`
- Edge types: `related_to depends_on derived_from contradicts supports part_of preceded_by followed_by authored_by tagged_with`
- Entry point for agents: `_system/INDEX.md`
- Every new node must update `_system/INDEX.md`
- Never leave `edges: []` empty on an established node
