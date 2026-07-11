"""Taxonomy + validation for Infinite Brain nodes (OKF core + extensions)."""
from __future__ import annotations
import re
from datetime import datetime, date

# 17 node types -> folder name
TYPE_TO_FOLDER = {
    "pillar": "pillars", "decision": "decisions", "concept": "concepts",
    "question": "questions", "playbook": "playbooks", "task": "tasks",
    "event": "events", "pattern": "patterns", "hypothesis": "hypotheses",
    "fact": "facts", "source": "sources", "bookmark": "bookmarks",
    "note": "notes", "contact": "contacts", "reference": "references",
    "custom": "custom", "log": "logs",
}
NODE_TYPES = tuple(TYPE_TO_FOLDER.keys())
CONTENT_TYPES = tuple(t for t in NODE_TYPES if t != "log")

EDGE_TYPES = (
    "related_to", "depends_on", "derived_from", "contradicts", "supports",
    "part_of", "preceded_by", "followed_by", "authored_by", "tagged_with",
)
VISIBILITY = ("public", "namespace", "private", "system")

# Full-node required frontmatter (log nodes use a reduced schema).
REQUIRED_FULL = (
    "id", "title", "type", "namespace", "visibility", "summary",
    "auto_inject", "confidence", "staleness_signal", "tags", "edges",
)
REQUIRED_LOG = ("id", "type", "operation", "date", "namespace", "summary",
                "affected_nodes", "tags")

_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def folder_for(node_type: str) -> str:
    return TYPE_TO_FOLDER.get(node_type, "custom")


def is_iso_date(v) -> bool:
    # YAML parses unquoted YYYY-MM-DD into date/datetime objects — those are valid.
    if isinstance(v, (date, datetime)):
        return True
    if not isinstance(v, str) or not _ISO_DATE_RE.match(v):
        return False
    try:
        datetime.strptime(v, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_node(meta: dict, known_ids: set | None = None) -> dict:
    """Return {'errors': [...], 'warnings': [...]}.

    Errors break OKF conformance or graph integrity. Warnings follow OKF's
    permissive-consumption model — the bundle stays readable.
    """
    errors, warnings = [], []
    ntype = meta.get("type")

    # --- OKF hard requirement (SPEC §9): non-empty type ---
    if not ntype or not str(ntype).strip():
        errors.append("OKF: 'type' is required and must be non-empty")
        return {"errors": errors, "warnings": warnings}
    if ntype not in NODE_TYPES:
        warnings.append(f"unknown type '{ntype}' (OKF tolerates it; document in _system/LOCAL-TYPES.md)")

    if ntype == "log":
        for f in REQUIRED_LOG:
            if f not in meta:
                warnings.append(f"log node missing '{f}'")
        return {"errors": errors, "warnings": warnings}

    # --- extension integrity (warnings) ---
    for f in REQUIRED_FULL:
        if f not in meta:
            warnings.append(f"missing recommended field '{f}'")

    nid = meta.get("id")
    if nid and not _ID_RE.match(str(nid)):
        warnings.append(f"id '{nid}' is not kebab-case")
    if known_ids is not None and nid and list(known_ids).count(nid) > 1:
        errors.append(f"duplicate id '{nid}'")

    if meta.get("visibility") not in VISIBILITY:
        warnings.append(f"visibility '{meta.get('visibility')}' not in {VISIBILITY}")

    conf = meta.get("confidence")
    if conf is not None:
        try:
            if not (0.0 <= float(conf) <= 1.0):
                warnings.append(f"confidence {conf} out of range 0.0–1.0")
        except (TypeError, ValueError):
            warnings.append(f"confidence '{conf}' is not a number")

    va = meta.get("verified_at")
    if va not in (None, "", "Empty") and not is_iso_date(va):
        warnings.append(f"verified_at '{va}' is not ISO 8601 (YYYY-MM-DD) or 'Empty'")

    summ = meta.get("summary")
    if isinstance(summ, str) and len(summ) > 200:
        warnings.append(f"summary is {len(summ)} chars (>200)")

    tags = meta.get("tags")
    if tags is not None and not isinstance(tags, list):
        warnings.append("tags must be a list")

    edges = meta.get("edges")
    if edges is not None:
        if not isinstance(edges, list):
            warnings.append("edges must be a list")
        else:
            if len(edges) == 0:
                warnings.append("edges is empty (fine only for a brand-new isolated node)")
            for i, e in enumerate(edges):
                if not isinstance(e, dict):
                    errors.append(f"edge[{i}] is not an object"); continue
                for k in ("target", "type", "weight", "note"):
                    if k not in e:
                        errors.append(f"edge[{i}] missing '{k}'")
                if e.get("type") and e["type"] not in EDGE_TYPES:
                    warnings.append(f"edge[{i}] type '{e['type']}' not in EDGE_TYPES")
                if e.get("target") == nid:
                    errors.append(f"edge[{i}] is self-referencing")
                w = e.get("weight")
                if w is not None:
                    try:
                        if not (0.0 <= float(w) <= 1.0):
                            warnings.append(f"edge[{i}] weight {w} out of range")
                    except (TypeError, ValueError):
                        warnings.append(f"edge[{i}] weight '{w}' not a number")
                if known_ids is not None and e.get("target") and e["target"] not in known_ids:
                    warnings.append(f"edge[{i}] target '{e['target']}' not found in vault")
    return {"errors": errors, "warnings": warnings}
