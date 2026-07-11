# Infinite Brain

**Portable, persistent memory for any AI — stored as plain files you own.**

AI forgets everything between sessions. Infinite Brain gives any AI a long-term memory
that lives as ordinary markdown files: readable by you, writable by the AI, browsable in
Obsidian, shippable over git. No database, no proprietary store, no lock-in. If you can
open a text file, you can read your AI's memory. If you can `git clone`, you can move it.

The memory is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
bundle — an open, permissive standard — so it stays portable across tools and time.

---

## Why

- **You own it.** Memory is plain markdown on your disk, not rows in someone's cloud.
- **Any AI can use it.** An MCP server exposes the memory to Claude, ChatGPT, Cursor, or
  any MCP-capable client. Point a new model at the same files and it picks up where the
  last one left off.
- **It stays clean.** The server does the mechanical work — parsing, validation, linking,
  indexing, forgetting stale entries — and refuses malformed writes, so the memory doesn't
  rot even when a weaker model is writing to it.
- **You can read it like a mind map.** Open the folder in Obsidian for a live graph of how
  memories connect.

## How it works

Every memory is one small markdown file — a **node** — with a bit of YAML at the top saying
what kind of memory it is and how sure the AI is of it. Nodes link to each other, so the
memory is a graph the AI can traverse instead of re-reading everything. The AI decides what
to remember and how confident to be; the server keeps it consistent.

That's the whole idea. The type/edge vocabulary and trust fields are implementation details
the AI and the server handle for you — you don't have to learn them to use it. If you want
the full contract, it lives in [`_system/AGENTS.md`](_system/AGENTS.md) and
[`_system/OKF-MAPPING.md`](_system/OKF-MAPPING.md).

## Quickstart

```bash
# 1. Install the memory server
cd mcp-server && pip install -e .

# 2. Point any MCP client at your vault (see mcp-server/clients/ for ready configs)
INFINITE_BRAIN_VAULT=/path/to/your/vault python -m infinite_brain_mcp

# 3. Talk to your AI. Ask it to remember things, then ask what it knows — across sessions.
```

The server gives any client **tools** (read/write/validate memories, search the graph,
audit, decay), **resources** (the memory contract + schema), and **prompts** (capture a
note, answer from memory, run maintenance). Full detail: [`mcp-server/README.md`](mcp-server/README.md).

## Read it in Obsidian

Open the vault folder in Obsidian. The graph view and wikilinks render the memory as an
interactive map — useful for spotting what's connected, what's isolated, and what's stale.
Obsidian is the **human reader**; the AI reads and writes through the MCP server.

## Using it with Claude Code

Claude Code users also get five slash-command skills in [`.claude/skills/`](.claude/skills)
(`init-vault`, `convert-note`, `query-vault`, `organize-vault`, `vault-health`). These are a
thin **adapter** over the same memory contract the MCP server exposes — one way in among
many, not the source of truth.

## Design notes

- **Portable by construction.** OKF-conformant: the memory is just files with a `type`.
  Unknown fields are preserved, never stripped. `python validate.py` checks conformance +
  graph integrity, and runs in CI on every push. See [`_system/OKF-MAPPING.md`](_system/OKF-MAPPING.md).
- **Deterministic in the server, judgment in the model.** Parsing, validation, indexing,
  and confidence decay are code; deciding what to remember is the AI's job.
- **Memory forgets.** Confidence decays over time and drops when newer evidence contradicts
  an old belief — so the memory reflects what's currently true, not everything ever said.

## Credits

Inspired by the Infinite Brain methodology from [AI Impact](https://www.youtube.com/@AIImpact).

## License

[MIT](LICENSE.md)
