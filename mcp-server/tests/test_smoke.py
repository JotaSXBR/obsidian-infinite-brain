import shutil, tempfile, os
from pathlib import Path
from infinite_brain_mcp.vault import Vault
from infinite_brain_mcp import schema, graph, maintenance, indexing


def _fixture_vault(tmp):
    """Minimal OKF vault: folders + one wired pillar."""
    for t, f in schema.TYPE_TO_FOLDER.items():
        (tmp / f).mkdir(parents=True, exist_ok=True)
    (tmp / "_system").mkdir(exist_ok=True)
    (tmp / "raw" / "processed").mkdir(parents=True, exist_ok=True)
    (tmp / "_system" / "INDEX.md").write_text("# idx", encoding="utf-8")
    return Vault(tmp)


def test_create_validate_read_index(tmp_path):
    v = _fixture_vault(tmp_path)
    node = {
        "id": "pillar-test-truth", "title": "Truth over comfort", "type": "pillar",
        "namespace": "test", "visibility": "public",
        "summary": "Prefer accurate models over comfortable ones.",
        "auto_inject": False, "applicable_when": "Empty", "confidence": 0.9,
        "verified_at": "2026-07-11", "verified_by": "jesse",
        "staleness_signal": "If a claim is repeatedly falsified, revisit.",
        "tags": ["epistemics", "values"], "edges": [], "source_url": "Empty",
    }
    res = schema.validate_node(node, v.known_ids())
    assert not res["errors"], res
    path = v.write(node, "# Truth over comfort\n\nBody.")
    assert (tmp_path / path).exists()
    back = v.read("pillar-test-truth")
    assert back["title"] == "Truth over comfort"
    assert "pillar-test-truth" in v.known_ids()
    idx = indexing.build_index(v)
    assert "pillar-test-truth" in idx


def test_edge_integrity_errors(tmp_path):
    v = _fixture_vault(tmp_path)
    bad = {"id": "n-a", "type": "concept",
           "edges": [{"target": "n-a", "type": "supports", "weight": 0.5, "note": "self"}]}
    res = schema.validate_node(bad, {"n-a"})
    assert any("self-referencing" in e for e in res["errors"])


def test_decay_and_query(tmp_path):
    v = _fixture_vault(tmp_path)
    old = {"id": "fact-old", "title": "Old fact", "type": "fact", "namespace": "test",
           "visibility": "public", "summary": "Something about revenue growth.",
           "auto_inject": False, "confidence": 0.9, "verified_at": "2024-01-01",
           "verified_by": "x", "staleness_signal": "n/a", "tags": ["revenue"], "edges": []}
    v.write(old, "body")
    dry = maintenance.confidence_decay(v, dry_run=True)
    assert dry["changed"] == 1 and dry["changes"][0]["new"] == 0.1
    hits = graph.query(v, "revenue growth")
    assert hits and hits[0]["id"] == "fact-old"


def test_okf_conformance_type_required(tmp_path):
    v = _fixture_vault(tmp_path)
    res = schema.validate_node({"id": "x", "title": "no type"}, set())
    assert res["errors"] and "type" in res["errors"][0]


def test_belief_revision(tmp_path):
    from infinite_brain_mcp import maintenance
    v = _fixture_vault(tmp_path)
    old = {"id": "fact-earth-flat", "title": "Earth is flat", "type": "fact",
           "namespace": "test", "visibility": "public", "summary": "An old wrong belief.",
           "auto_inject": False, "confidence": 0.6, "verified_at": "Empty",
           "verified_by": "x", "staleness_signal": "n/a", "tags": ["geo"], "edges": []}
    v.write(old, "body")
    new = {"id": "fact-earth-round", "title": "Earth is round", "type": "fact",
           "namespace": "test", "visibility": "public", "summary": "Contradicts the old belief.",
           "auto_inject": False, "confidence": 0.99, "verified_at": "Empty",
           "verified_by": "x", "staleness_signal": "n/a", "tags": ["geo"],
           "edges": [{"target": "fact-earth-flat", "type": "contradicts",
                      "weight": 1.0, "note": "evidence"}]}
    v.write(new, "body")
    res = maintenance.belief_revision(v, dry_run=False)
    assert res["revised"] == 1
    assert v.read("fact-earth-flat")["confidence"] == 0.4
    assert "contradicted" in v.read("fact-earth-flat")["tags"]
