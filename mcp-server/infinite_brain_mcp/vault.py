"""Vault I/O — load, save, and index Infinite Brain nodes."""
from __future__ import annotations
import os
from pathlib import Path
import frontmatter
from . import schema


class Vault:
    def __init__(self, root: str | os.PathLike):
        self.root = Path(root).resolve()
        if not self.root.exists():
            raise FileNotFoundError(f"vault root not found: {self.root}")

    # ---- discovery ----
    def _node_files(self):
        skip = {".git", ".obsidian", ".claude", "_templates", "_system", "raw", "mcp-server", "node_modules"}
        for p in self.root.rglob("*.md"):
            rel = p.relative_to(self.root)
            if rel.parts and rel.parts[0] in skip:
                continue
            if p.name in ("index.md", "log.md", "README.md", "PLAN.md", "TODO.md",
                          "CLAUDE.md", "LICENSE.md"):
                continue
            yield p

    def load_all(self) -> list[dict]:
        nodes = []
        for p in self._node_files():
            try:
                post = frontmatter.load(p)
            except Exception as e:
                nodes.append({"_path": str(p.relative_to(self.root)), "_error": str(e)})
                continue
            meta = dict(post.metadata)
            meta["_path"] = str(p.relative_to(self.root))
            meta["_body"] = post.content
            nodes.append(meta)
        return nodes

    def id_map(self) -> dict[str, str]:
        m = {}
        for n in self.load_all():
            if n.get("id"):
                m[n["id"]] = n["_path"]
        return m

    def known_ids(self) -> set[str]:
        return set(self.id_map().keys())

    # ---- single node ----
    def read(self, node_id: str) -> dict | None:
        path = self.id_map().get(node_id)
        if not path:
            return None
        post = frontmatter.load(self.root / path)
        meta = dict(post.metadata)
        meta["_path"] = path
        meta["_body"] = post.content
        return meta

    def path_for(self, node_id: str, node_type: str) -> Path:
        return self.root / schema.folder_for(node_type) / f"{node_id}.md"

    def write(self, meta: dict, body: str) -> str:
        meta = {k: v for k, v in meta.items() if not k.startswith("_")}
        ntype = meta["type"]
        nid = meta["id"]
        target = self.path_for(nid, ntype)
        target.parent.mkdir(parents=True, exist_ok=True)
        post = frontmatter.Post(body or "", **meta)
        target.write_bytes(frontmatter.dumps(post).encode("utf-8"))
        return str(target.relative_to(self.root))

    # ---- raw inbox ----
    def raw_list(self) -> list[str]:
        raw = self.root / "raw"
        out = []
        if raw.exists():
            for p in sorted(raw.glob("*")):
                if p.is_file() and p.name != ".gitkeep":
                    out.append(p.name)
        return out

    def raw_mark_processed(self, filename: str) -> str:
        src = self.root / "raw" / filename
        if not src.exists():
            raise FileNotFoundError(f"raw/{filename} not found")
        dst_dir = self.root / "raw" / "processed"
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / filename
        src.rename(dst)
        return str(dst.relative_to(self.root))

    # ---- system files ----
    def read_system(self, name: str) -> str | None:
        p = self.root / "_system" / name
        return p.read_text(encoding="utf-8") if p.exists() else None
