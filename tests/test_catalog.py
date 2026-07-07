"""Smoke/invariant tests for the iw7x catalog and engine.

Run:  pytest -q
"""

import json
from pathlib import Path

from neoz.models import load_catalog
from neoz import bundles
from neoz.cli import _resolve
from neoz.updater import _repo_tool_name, _dedup_key, _GROUP_MAP, _section_to_group

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"


def test_catalog_is_valid_json():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    assert data.get("categories"), "catalog has no categories"


def test_model_loads_a_large_catalog():
    c = load_catalog()
    assert c.tool_count > 10000, f"only {c.tool_count} tools"
    assert len(c.categories) >= 40


def test_every_category_has_id_and_title():
    for cat in load_catalog().categories:
        assert cat.id and cat.title, f"bad category {cat!r}"


def test_no_empty_tool_titles():
    for cat in load_catalog().categories:
        for tool in cat.tools:
            assert tool.title.strip(), f"empty title in {cat.id}"


def test_every_bundle_tool_resolves():
    for name, b in bundles.ALL.items():
        for want in b["tools"]:
            tool, _sugg = _resolve(want)
            assert tool is not None, f"bundle '{name}': '{want}' does not resolve"


def test_flagship_tools_have_install_commands():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    for cat in data["categories"]:
        for tool in cat.get("tools", []):
            if tool.get("flagship"):
                assert tool.get("install"), f"flagship '{tool['title']}' has no install command"


def test_repo_link_name_filter():
    # keeps clean tool names
    assert _repo_tool_name("Nuclei", "nuclei") == "Nuclei"
    # rejects list/cheatsheet/generic noise
    assert _repo_tool_name("Cheat Sheet", "awesome-cheatsheets") is None
    assert _repo_tool_name("tools", "some-tools") is None
    assert _repo_tool_name("awesome-hacking", "awesome-hacking") is None


def test_catalog_meta_matches_actual_counts():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    actual = sum(len(c.get("tools", [])) for c in data["categories"])
    assert data["meta"]["tools"] == actual, "meta.tools out of sync with the catalog"


def test_every_category_has_all_fields():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    for cat in data["categories"]:
        for field in ("id", "title", "title_fr", "icon"):
            assert cat.get(field), f"category {cat.get('id')!r} missing {field}"


def test_no_duplicate_tools():
    seen: set[str] = set()
    for cat in load_catalog().categories:
        for tool in cat.tools:
            key = _dedup_key(tool.title)
            if not key:
                continue
            assert key not in seen, f"duplicate tool: {tool.title}"
            seen.add(key)


def test_dedup_key_collapses_variants():
    assert _dedup_key("cloud_enum") == _dedup_key("cloud-enum") == _dedup_key("CloudEnum") == "cloudenum"
    assert _dedup_key("") == ""


def test_group_routing_is_sane():
    # cloud/container route to their dedicated categories, not the generic bucket
    assert _GROUP_MAP["cloud"] == "cloud_security"
    assert _GROUP_MAP["container"] == "container_k8s"
    assert _section_to_group("AWS Cloud Security") == "cloud"
    assert _section_to_group("Kubernetes hardening") == "container"


def test_bundles_are_well_formed():
    assert len(bundles.ALL) >= 10
    for name, b in bundles.ALL.items():
        assert b.get("title") and b.get("tools"), f"bundle {name} malformed"
        assert bundles.get(name) is b
