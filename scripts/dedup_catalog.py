#!/usr/bin/env python3
"""Remove near-duplicate tools from catalog.json.

Two entries are duplicates when their titles collapse to the same
alphanumeric-only key (so 'cloud_enum', 'cloud-enum' and 'CloudEnum' are one).
The best copy is kept — preferring flagship entries, then those with real
install/run commands and a fuller description. Run: python scripts/dedup_catalog.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"


def key(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def score(t: dict) -> int:
    s = 0
    if t.get("flagship"):
        s += 100
    if t.get("install"):
        s += 10
    if t.get("run"):
        s += 5
    s += min(len(t.get("description") or ""), 60) // 10
    return s


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))

    # Pick the single best tool object for each dedup key across the whole catalog.
    best: dict[str, tuple[int, dict]] = {}
    for c in data["categories"]:
        for t in c.get("tools", []):
            k = key(t.get("title", ""))
            if not k:
                continue
            sc = score(t)
            if k not in best or sc > best[k][0]:
                best[k] = (sc, t)

    removed = 0
    for c in data["categories"]:
        kept = []
        for t in c.get("tools", []):
            k = key(t.get("title", ""))
            if not k or best[k][1] is t:
                kept.append(t)          # unique, or this is the winning copy
            else:
                removed += 1            # a duplicate — drop it
        c["tools"] = kept

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})["tools"] = total
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Removed {removed} duplicate tools — {total} unique tools remain.")


if __name__ == "__main__":
    main()
