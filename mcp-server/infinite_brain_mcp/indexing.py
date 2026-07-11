"""Rebuild _system/INDEX.md from the current node set."""
from __future__ import annotations
from datetime import date
from .vault import Vault
from . import schema


def build_index(vault: Vault) -> str:
    nodes = [n for n in vault.load_all() if "_error" not in n and n.get("type") != "log"]
    by_type: dict[str, list] = {t: [] for t in schema.CONTENT_TYPES}
    for n in nodes:
        by_type.setdefault(n.get("type", "custom"), []).append(n)

    lines = [
        "# Knowledge Graph Vault — Master Index",
        "",
        "> **Entry point for AI agents.** Every content node, grouped by type, with "
        "summary and edge count for rapid scanning. Rebuilt by the MCP server "
        "(`index_rebuild`).",
        "",
        "---",
        "",
    ]
    for t in schema.CONTENT_TYPES:
        lines.append(f"## {t}\n")
        rows = by_type.get(t, [])
        if not rows:
            lines.append("*No nodes created yet.*\n")
        else:
            lines.append("| ID | Summary | Edges |")
            lines.append("|---|---|---|")
            for n in sorted(rows, key=lambda x: str(x.get("id"))):
                summ = str(n.get("summary", "")).replace("|", "\\|")
                lines.append(f"| `{n.get('id')}` | {summ} | {len(n.get('edges') or [])} |")
            lines.append("")
        lines.append("---\n")
    lines += [
        "## log\n",
        "> Log nodes are not indexed here. They live in `logs/` and are self-contained.\n",
        "---\n",
        f"*Last rebuilt: {date.today().isoformat()} by infinite-brain MCP server*",
        "",
    ]
    return "\n".join(lines)
