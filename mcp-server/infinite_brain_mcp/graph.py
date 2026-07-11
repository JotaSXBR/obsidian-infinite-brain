"""Graph operations — scoped retrieval, neighbors, orphans."""
from __future__ import annotations
import re
from .vault import Vault


def _content_nodes(vault: Vault):
    return [n for n in vault.load_all()
            if n.get("type") != "log" and "_error" not in n]


def neighbors(vault: Vault, node_id: str, edge_types=None):
    """Outgoing edges of node_id, plus incoming edges from other nodes."""
    out, incoming = [], []
    for n in _content_nodes(vault):
        if n.get("id") == node_id:
            for e in (n.get("edges") or []):
                if edge_types and e.get("type") not in edge_types:
                    continue
                out.append(e)
        else:
            for e in (n.get("edges") or []):
                if e.get("target") == node_id:
                    if edge_types and e.get("type") not in edge_types:
                        continue
                    incoming.append({"source": n.get("id"), **e})
    return {"id": node_id, "outgoing": out, "incoming": incoming}


def orphans(vault: Vault):
    """Nodes with no outgoing edges, no related, and no incoming edges."""
    nodes = _content_nodes(vault)
    targeted = set()
    for n in nodes:
        for e in (n.get("edges") or []):
            if e.get("target"):
                targeted.add(e["target"])
    result = []
    for n in nodes:
        has_out = bool(n.get("edges")) or bool(n.get("related"))
        has_in = n.get("id") in targeted
        if not has_out and not has_in:
            result.append({"id": n.get("id"), "type": n.get("type"),
                           "path": n.get("_path")})
    return result


def query(vault: Vault, q: str, namespace=None, visibility=None, limit=12):
    """Lightweight scoped retrieval: score nodes by term overlap with
    title/summary/tags, honoring namespace + visibility filters. Returns
    compact hits (no bodies) so the calling LLM traverses selectively."""
    terms = [t for t in re.split(r"\W+", q.lower()) if len(t) > 2]
    hits = []
    for n in _content_nodes(vault):
        vis = n.get("visibility")
        if vis == "system":
            continue
        if visibility and vis != visibility:
            continue
        if namespace and n.get("namespace") not in (namespace, "public") \
                and vis != "public":
            continue
        hay = " ".join([
            str(n.get("title", "")), str(n.get("summary", "")),
            " ".join(n.get("tags", []) if isinstance(n.get("tags"), list) else []),
        ]).lower()
        score = sum(hay.count(t) for t in terms)
        # small boost if a term appears in the id
        score += sum(2 for t in terms if t in str(n.get("id", "")).lower())
        if score > 0:
            hits.append({
                "id": n.get("id"), "type": n.get("type"),
                "namespace": n.get("namespace"), "visibility": vis,
                "summary": n.get("summary"),
                "confidence": n.get("confidence"),
                "edge_count": len(n.get("edges") or []),
                "score": score,
            })
    hits.sort(key=lambda h: h["score"], reverse=True)
    return hits[:limit]
