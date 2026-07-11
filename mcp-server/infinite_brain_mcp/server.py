"""Infinite Brain MCP server — tool-agnostic bridge over the markdown vault.

Vault root resolution: --vault CLI arg > $INFINITE_BRAIN_VAULT > current dir.
Run:  python -m infinite_brain_mcp            (stdio transport)
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

from .vault import Vault
from . import schema, graph, maintenance, indexing, prompts


def _resolve_root() -> Path:
    root = None
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a == "--vault" and i + 1 < len(argv):
            root = argv[i + 1]
        elif a.startswith("--vault="):
            root = a.split("=", 1)[1]
    root = root or os.environ.get("INFINITE_BRAIN_VAULT") or os.getcwd()
    return Path(root).resolve()


ROOT = _resolve_root()
mcp = FastMCP("infinite-brain")


def _vault() -> Vault:
    return Vault(ROOT)


# ----------------------------- taxonomy -----------------------------
@mcp.tool()
def list_node_types() -> dict:
    """List the valid node types and their target folders."""
    return {"types": list(schema.NODE_TYPES), "folders": schema.TYPE_TO_FOLDER}


@mcp.tool()
def list_edge_types() -> list[str]:
    """List the valid typed-edge names."""
    return list(schema.EDGE_TYPES)


# ----------------------------- nodes -----------------------------
@mcp.tool()
def node_read(node_id: str) -> dict:
    """Read one node (frontmatter + body) by its id."""
    n = _vault().read(node_id)
    if n is None:
        return {"error": f"node '{node_id}' not found"}
    return n


@mcp.tool()
def node_validate(node: dict) -> dict:
    """Validate a node draft against the OKF-core + extension schema.
    Returns {errors, warnings}. Errors break conformance/integrity; warnings are advisory."""
    return schema.validate_node(node, _vault().known_ids())


@mcp.tool()
def node_create(node: dict, body: str = "") -> dict:
    """Create a node. Validates first; refuses to write if there are hard errors.
    `node` is the frontmatter mapping (must include type, id); `body` is the markdown body."""
    v = _vault()
    result = schema.validate_node(node, v.known_ids())
    if result["errors"]:
        return {"written": False, **result}
    if node.get("id") in v.known_ids():
        return {"written": False, "errors": [f"id '{node.get('id')}' already exists"],
                "warnings": result["warnings"]}
    path = v.write(node, body)
    return {"written": True, "path": path, "warnings": result["warnings"]}


@mcp.tool()
def node_update(node_id: str, patch: dict, body: str | None = None) -> dict:
    """Merge `patch` into an existing node's frontmatter (and optionally replace body).
    Re-validates before writing."""
    v = _vault()
    n = v.read(node_id)
    if n is None:
        return {"written": False, "errors": [f"node '{node_id}' not found"]}
    meta = {k: val for k, val in n.items() if not k.startswith("_")}
    meta.update(patch)
    result = schema.validate_node(meta, v.known_ids())
    if result["errors"]:
        return {"written": False, **result}
    path = v.write(meta, n["_body"] if body is None else body)
    return {"written": True, "path": path, "warnings": result["warnings"]}


# ----------------------------- index -----------------------------
@mcp.tool()
def index_read() -> str:
    """Return the current _system/INDEX.md (the rich agent index)."""
    return _vault().read_system("INDEX.md") or "(no INDEX.md)"


@mcp.tool()
def index_rebuild() -> dict:
    """Regenerate _system/INDEX.md from the current node set. Writes the file."""
    v = _vault()
    content = indexing.build_index(v)
    (v.root / "_system" / "INDEX.md").write_text(content, encoding="utf-8")
    return {"written": True, "path": "_system/INDEX.md", "bytes": len(content)}


# ----------------------------- graph -----------------------------
@mcp.tool()
def graph_query(query: str, namespace: str | None = None,
                visibility: str | None = None, limit: int = 12) -> list[dict]:
    """Scoped retrieval. Scores nodes by term overlap with title/summary/tags,
    honoring namespace + visibility. Returns compact hits (no bodies)."""
    return graph.query(_vault(), query, namespace, visibility, limit)


@mcp.tool()
def graph_neighbors(node_id: str, edge_types: list[str] | None = None) -> dict:
    """Outgoing and incoming typed edges for a node, optionally filtered by edge type."""
    return graph.neighbors(_vault(), node_id, edge_types)


# ----------------------------- maintenance -----------------------------
@mcp.tool()
def vault_audit() -> dict:
    """Read-only health audit: orphans, integrity errors, stale nodes, parse errors, warnings."""
    return maintenance.audit(_vault())


@mcp.tool()
def confidence_decay(dry_run: bool = True) -> dict:
    """Apply (or preview) deterministic confidence decay for nodes not verified in 90+ days.
    Reversible via git. Set dry_run=false to write."""
    return maintenance.confidence_decay(_vault(), dry_run)


# ----------------------------- raw inbox -----------------------------
@mcp.tool()
def raw_list() -> list[str]:
    """List unprocessed files in raw/."""
    return _vault().raw_list()


@mcp.tool()
def raw_mark_processed(filename: str) -> dict:
    """Move raw/<filename> to raw/processed/ after conversion."""
    try:
        dst = _vault().raw_mark_processed(filename)
        return {"moved": True, "to": dst}
    except FileNotFoundError as e:
        return {"moved": False, "error": str(e)}


# ----------------------------- resources -----------------------------
def _sys_resource(name):
    def fn() -> str:
        return _vault().read_system(name) or f"(missing _system/{name})"
    return fn

mcp.resource("infinite-brain://system/agents")(_sys_resource("AGENTS.md"))
mcp.resource("infinite-brain://system/node-types")(_sys_resource("NODE-TYPES.md"))
mcp.resource("infinite-brain://system/edge-types")(_sys_resource("EDGE-TYPES.md"))
mcp.resource("infinite-brain://system/frontmatter-schema")(_sys_resource("FRONTMATTER-SCHEMA.md"))
mcp.resource("infinite-brain://system/okf-mapping")(_sys_resource("OKF-MAPPING.md"))


@mcp.resource("infinite-brain://index")
def _index_resource() -> str:
    return _vault().read_system("INDEX.md") or "(no INDEX.md)"


# ----------------------------- prompts -----------------------------
def _register_prompt(name, text):
    @mcp.prompt(name=name)
    def _p() -> str:
        return text
    return _p

for _name, _text in prompts.REGISTRY.items():
    _register_prompt(_name, _text)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
