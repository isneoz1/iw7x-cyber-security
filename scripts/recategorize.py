#!/usr/bin/env python3
"""Add missing categories and route existing tools into the RIGHT category.

Moves tools out of the generic buckets (other_tools / information_gathering /
blue_team) into a better-matching category using tight, unambiguous patterns —
first match wins. Dry-run by default; pass --save to apply. New categories with
too few real tools are not created.

    python scripts/recategorize.py          # preview
    python scripts/recategorize.py --save    # apply
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"

# New categories to create (id -> title, title_fr, icon)
NEW_CATS = [
    ("reporting", "Reporting & Documentation", "Rapports & Documentation", "📝"),
    ("adversary_emulation", "Adversary Emulation / Purple Team", "Émulation d'adversaire / Purple Team", "🟣"),
]

# Only pull FROM these generic buckets — never disturb well-placed niche tools.
SOURCES = {"other_tools", "information_gathering", "blue_team", "web_attack"}

# target_id -> tight regex (first match wins). Keep these specific to avoid noise.
RULES = [
    ("reporting", re.compile(r"\b(dradis|faraday|serpico|pwndoc|ghostwriter|writehat|reconmap|nipper|vulnreport|attackforge|pentest[- ]?report|report generator|reporting framework|reporting tool)\b")),
    ("adversary_emulation", re.compile(r"(atomic[- ]?red[- ]?team|\bcaldera\b|adversary emulation|purple[- ]?team|stratus[- ]?red[- ]?team|\bleonidas\b|infection[- ]?monkey|apt[- ]?simulator|\bflightsim\b|red[- ]?team automation|breach and attack|\bvectr\b|prelude operator)")),
]

MIN_TOOLS = 12   # don't ship a near-empty category


def main() -> None:
    save = "--save" in sys.argv
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    cats = {c["id"]: c for c in data["categories"]}

    moved: dict[str, list] = {tid: [] for tid, _ in RULES}
    for cid in list(cats):
        if cid not in SOURCES:
            continue
        keep = []
        for t in cats[cid].get("tools", []):
            blob = f"{t.get('title','')} {t.get('description','')} {' '.join(t.get('tags',[]))}".lower()
            target = next((tid for tid, rx in RULES if rx.search(blob)), None)
            if target and target != cid:
                moved[target].append((t, cid))
            else:
                keep.append(t)
        cats[cid]["tools"] = keep

    # Decide which new categories are worth creating.
    created, dropped = [], []
    for tid, title, title_fr, icon in NEW_CATS:
        items = moved.get(tid, [])
        if len(items) < MIN_TOOLS:
            dropped.append((tid, len(items)))
            # put the (few) matches back where they came from
            for t, src in items:
                cats[src].setdefault("tools", []).append(t)
            moved[tid] = []
            continue
        created.append((tid, title, title_fr, icon, len(items)))

    print(f"{'target':>22}  count")
    print("-" * 60)
    for tid, _ in RULES:
        print(f"{tid:>22}: {len(moved[tid])}")
        for t, src in moved[tid][:6]:
            print(f"      - {t['title'][:44]:<44} (from {src})")
    if dropped:
        print("dropped (too few):", dropped)

    if not save:
        print("\n[DRY RUN] nothing written. Re-run with --save to apply.")
        return

    # Create categories (before update_uninstall) and attach moved tools.
    idx = next((i for i, c in enumerate(data["categories"]) if c["id"] == "update_uninstall"), len(data["categories"]))
    to_add = []
    for tid, title, title_fr, icon, _n in created:
        cat = {"id": tid, "title": title, "title_fr": title_fr, "icon": icon,
               "tools": [t for t, _src in moved[tid]]}
        to_add.append(cat)
    data["categories"] = data["categories"][:idx] + to_add + data["categories"][idx:]

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})["tools"] = total
    data["meta"]["categories"] = len(data["categories"])
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[SAVED] created {len(created)} categories · {len(data['categories'])} total · {total} tools")


if __name__ == "__main__":
    main()
