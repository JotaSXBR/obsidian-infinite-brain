"""Maintenance — deterministic confidence decay + read-only audit."""
from __future__ import annotations
from datetime import date, datetime
from .vault import Vault
from . import schema, graph


def _days_since(iso: str):
    try:
        d = datetime.strptime(iso, "%Y-%m-%d").date()
        return (date.today() - d).days
    except (TypeError, ValueError):
        return None


def confidence_decay(vault: Vault, dry_run: bool = True):
    """Reduce confidence on nodes not verified recently. Deterministic,
    reversible via git. Skips system nodes and unverified ('Empty') nodes."""
    changes = []
    for n in vault.load_all():
        if n.get("type") == "log" or "_error" in n:
            continue
        if n.get("visibility") == "system":
            continue
        va = n.get("verified_at")
        if va in (None, "", "Empty"):
            continue
        days = _days_since(va)
        if days is None or days <= 90:
            continue
        conf = n.get("confidence")
        try:
            conf = float(conf)
        except (TypeError, ValueError):
            continue
        new = conf
        add_tag = False
        if days > 365:
            new, add_tag = 0.1, True
        elif days > 180:
            new = max(0.1, round(conf - 0.2, 2))
        else:  # 91–180
            new = max(0.1, round(conf - 0.1, 2))
        if new != conf or add_tag:
            changes.append({"id": n.get("id"), "days": days,
                            "old": conf, "new": new, "needs_review": add_tag})
            if not dry_run:
                meta = {k: v for k, v in n.items() if not k.startswith("_")}
                meta["confidence"] = new
                if add_tag:
                    tags = meta.get("tags") or []
                    if "needs-review" not in tags:
                        tags.append("needs-review")
                    meta["tags"] = tags
                vault.write(meta, n.get("_body", ""))
    return {"dry_run": dry_run, "changed": len(changes), "changes": changes}


def audit(vault: Vault):
    """Read-only health audit. Collects findings; never mutates."""
    nodes = [n for n in vault.load_all() if "_error" not in n and n.get("type") != "log"]
    parse_errors = [n["_path"] for n in vault.load_all() if "_error" in n]
    known = vault.known_ids()

    missing_fields, bad_edges, stale, high_conf_stale = [], [], [], []
    for n in nodes:
        v = schema.validate_node(n, known)
        if v["errors"]:
            bad_edges.append({"id": n.get("id"), "errors": v["errors"]})
        if v["warnings"]:
            missing_fields.append({"id": n.get("id"), "warnings": v["warnings"][:4]})
        va = n.get("verified_at")
        if va not in (None, "", "Empty"):
            d = _days_since(va)
            if d and d > 90:
                stale.append({"id": n.get("id"), "days": d, "type": n.get("type")})

    return {
        "total_nodes": len(nodes),
        "parse_errors": parse_errors,
        "orphans": graph.orphans(vault),
        "integrity_errors": bad_edges,
        "nodes_with_warnings": missing_fields,
        "stale": sorted(stale, key=lambda x: -x["days"]),
        "belief_revisions": belief_revision(vault, dry_run=True)["changes"],
    }


def belief_revision(vault: Vault, dry_run: bool = True):
    """General 'learning from being wrong': when a node is `contradicts`-linked by a
    source that is at least as confident, lower the contradicted node's confidence.
    Deterministic, reversible via git. No metrics, no business logic — memory correction.

    Rule per contradicting edge: new = max(0.1, target_conf - 0.2 * weight), and tag
    the target `contradicted`. The strongest applicable contradiction wins.
    """
    by_id = {}
    for n in vault.load_all():
        if "_error" in n or n.get("type") == "log":
            continue
        if n.get("id"):
            by_id[n["id"]] = n

    proposals = {}  # target_id -> (new_conf, source_id, weight)
    for src in by_id.values():
        try:
            src_conf = float(src.get("confidence"))
        except (TypeError, ValueError):
            continue
        for e in (src.get("edges") or []):
            if e.get("type") != "contradicts":
                continue
            tgt_id = e.get("target")
            tgt = by_id.get(tgt_id)
            if not tgt:
                continue
            try:
                tgt_conf = float(tgt.get("confidence"))
            except (TypeError, ValueError):
                continue
            if src_conf < tgt_conf:
                continue  # weaker evidence does not revise a stronger belief
            try:
                weight = float(e.get("weight", 0.5))
            except (TypeError, ValueError):
                weight = 0.5
            new = max(0.1, round(tgt_conf - 0.2 * weight, 2))
            if new < tgt_conf:
                cur = proposals.get(tgt_id)
                if cur is None or new < cur[0]:
                    proposals[tgt_id] = (new, src.get("id"), weight)

    changes = []
    for tgt_id, (new, src_id, weight) in proposals.items():
        tgt = by_id[tgt_id]
        changes.append({"id": tgt_id, "old": float(tgt.get("confidence")),
                        "new": new, "contradicted_by": src_id, "weight": weight})
        if not dry_run:
            meta = {k: v for k, v in tgt.items() if not k.startswith("_")}
            meta["confidence"] = new
            tags = meta.get("tags") or []
            if "contradicted" not in tags:
                tags.append("contradicted")
            meta["tags"] = tags
            vault.write(meta, tgt.get("_body", ""))
    return {"dry_run": dry_run, "revised": len(changes), "changes": changes}
