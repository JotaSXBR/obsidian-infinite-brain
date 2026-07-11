#!/usr/bin/env python3
"""Validate an Infinite Brain vault: OKF v0.1 conformance + extension integrity.

Usage:  python validate.py [VAULT_ROOT]   (default: current directory)

Exit code 1 if any hard errors (broken OKF conformance or graph integrity);
warnings never fail the build (OKF's permissive-consumption model).
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "mcp-server"))
from infinite_brain_mcp.vault import Vault          # noqa: E402
from infinite_brain_mcp import schema               # noqa: E402


def main(root: str = ".") -> int:
    vault = Vault(root)
    nodes = vault.load_all()
    known = [n.get("id") for n in nodes if n.get("id")]
    known_set = set(known)

    errors, warnings = [], []

    # duplicate ids (hard error — breaks graph integrity)
    seen = {}
    for nid in known:
        seen[nid] = seen.get(nid, 0) + 1
    for nid, c in seen.items():
        if c > 1:
            errors.append(f"[duplicate-id] '{nid}' appears {c} times")

    for n in nodes:
        path = n.get("_path", "?")
        if "_error" in n:
            errors.append(f"[unparseable] {path}: {n['_error']}")
            continue
        res = schema.validate_node(n, known_set)
        for e in res["errors"]:
            errors.append(f"[error] {path}: {e}")
        for w in res["warnings"]:
            warnings.append(f"[warn]  {path}: {w}")

    print(f"Infinite Brain validator — {len(nodes)} nodes\n")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print("  " + w)
        print()
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print("  " + e)
        print("\nFAIL — OKF conformance / integrity errors present.")
        return 1
    print("OK — vault is OKF-conformant and graph integrity holds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
