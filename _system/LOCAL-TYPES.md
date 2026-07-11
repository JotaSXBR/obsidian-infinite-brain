# Local Custom Types

Memory stores *what the AI knows*. Capabilities — *how the AI acts* — normally live in the
contract layer (`AGENTS.md`, the MCP tools/prompts), not in memory. But if you want the AI
to be able to read its own capabilities as memory (query them, link them to decisions), you
may register them here as `custom` nodes. This keeps the 16 canonical types minimal while
allowing capability-as-memory when you opt in.

All custom nodes use `type: custom` in frontmatter and live in `custom/`. Add a
`custom_type:` field to disambiguate. Document each below.

---

## Registration Format

- **Custom type:** value of `custom_type` (lowercase, singular)
- **Rationale:** why the 16 canonical types don't fit
- **Usage scope:** which namespace(s) use it

---

## Available operational types (opt-in)

These are pre-blessed `custom_type` values for representing capabilities as memory. Use them
only if you want capabilities to be first-class, queryable nodes; otherwise leave capabilities
in `AGENTS.md` / the MCP surface.

- **tool** — an external tool or function the AI can call. Rationale: a capability, not knowledge.
- **skill** — a reusable procedure/prompt the AI can invoke (e.g. a slash command).
- **rule** — a standing constraint or policy the AI must honor.
- **agent** — a named agent/role with a defined scope of action.
- **workflow** — a multi-step orchestration across tools/skills/agents.

Example frontmatter:

```yaml
type: custom
custom_type: tool
id: tool-web-search
```

---

*No user-defined custom types registered yet.*
