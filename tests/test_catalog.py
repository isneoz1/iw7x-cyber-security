"""Smoke/invariant tests for the iw7x catalog and engine.

Run:  pytest -q
"""

import json
from pathlib import Path

from neoz.models import load_catalog
from neoz import bundles
from neoz.cli import _resolve
from neoz.updater import _repo_tool_name

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
