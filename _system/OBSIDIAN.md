# Obsidian — the human reader

Obsidian is how *you* read the memory. The AI reads and writes through the MCP server;
you open the same folder in Obsidian to see it as a map. Nothing here is required for the
memory to work — it's a viewing layer.

## Setup

1. Open the vault folder as an Obsidian vault (`Open folder as vault`).
2. That's it. Files are plain markdown; wikilinks and frontmatter already resolve.

## What the graph view actually shows (read this)

Obsidian's **core graph view reads links, not arbitrary frontmatter.** It renders the
`[[wikilinks]]` in each node's `related` field — a lightweight association map. It does
**not** read the typed `edges` array (direction, weight, type) natively; those are an
extension the MCP server understands.

To visualize the *typed* graph in Obsidian, install one community plugin:

- **Breadcrumbs** — reads relationships from frontmatter fields and builds a navigable,
  directional hierarchy. The closest match to our typed `edges`.
- **Juggl** — an interactive graph that can style nodes/edges by type.

Without a plugin you still get: the core graph over `related`, folder-colored groups, and
full-text search. That's enough to spot clusters, orphans, and stale corners at a glance.

Suggested core-graph color groups (Settings → Graph → Groups): one color per top-level
folder (`pillars`, `decisions`, `facts`, …) so node type is visible by color.

## Capturing sources — Obsidian Web Clipper

To feed the memory from the web without leaving the browser, use the **Obsidian Web
Clipper** extension and point it at `raw/`:

- Save location: `raw/`
- Filename template: `raw/{{date}}-{{title}}.md`
- It lands in the immutable inbox; later the AI runs the `convert-note` workflow, decomposes
  it into typed nodes, stamps a provenance hash, and moves the original to `raw/processed/`.

No manual tagging needed — that happens during conversion.

## Dataview (optional, deferred)

If you install **Dataview**, you can write live tables over frontmatter — e.g. "memories
with confidence < 0.5", "everything tagged `contradicted`", "nodes never verified". A
prebuilt dashboard is intentionally left for later; decide if you want one once the memory
has grown enough to need it.
