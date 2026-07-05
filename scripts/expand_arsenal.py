#!/usr/bin/env python3
"""Add new categories to catalog.json and reclassify existing tools into them.

Adds 7 dedicated categories (Honeypots, CTF, Game Hacking, Supply Chain,
Threat Hunting, Malware Sandbox, Data Exfiltration) and MOVES existing tools
that clearly belong there (tight, high-precision regex on title + description).
Reclassification preserves the total tool count — it only redistributes.

The updater is wired to route future scrapes into these categories too
(see neoz/updater.py `_GROUP_MAP` / `_section_to_group`).

Run:  python scripts/expand_arsenal.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"

# id -> (title, title_fr, icon, compiled precise pattern). Order = priority.
NEW_CATEGORIES: list[tuple[str, str, str, str, str]] = [
    ("honeypots", "Honeypots / Deception", "Honeypots / Déception", "🍯",
     r"\b(honeypot|honeypots|honeynet|honeytoken|honeytrap|canary ?token|cowrie|"
     r"dionaea|kippo|glastopf|conpot|t-?pot|honeyd|honeydb|deception (grid|platform|technology)|"
     r"decoy (system|network|host))\b"),
    ("game_hacking", "Game Hacking", "Piratage de jeux", "🎮",
     r"(game[ -]?hacking|game[ -]?hack\b|game[ -]?cheat|cheat[ -]?engine|game[ -]?trainer|"
     r"anti[ -]?cheat|memory[ -]?hacking|\bhack(ing)? (a |your )?game|game[ -]?exploit)"),
    ("ctf_tools", "CTF / Wargames", "CTF / Wargames", "🚩",
     r"(ctf[ -]?(tools?|framework|toolkit|platform|solver|helper|challenge|player|d\b)|"
     r"capture the flag|\bwargames?\b|picoctf|jeopardy-style|host(ing)? ctf|create ctf)"),
    ("supply_chain", "Supply Chain / SBOM", "Supply Chain / SBOM", "🧱",
     r"(supply[ -]?chain|\bsbom\b|dependency[ -]?confusion|typosquat|"
     r"software[ -]?composition[ -]?analysis|dependency[ -]?track|cyclonedx|\bspdx\b|"
     r"package[ -]?(hijack|confusion))"),
    ("threat_hunting", "Threat Hunting", "Chasse aux menaces", "🐺",
     r"(threat[ -]?hunting|sigma[ -]?rules?|hunting[ -]?(query|queries|ruleset|platform)|"
     r"\bthreat hunt\b|detection[ -]?engineering)"),
    ("sandbox_analysis", "Malware Sandbox / Detonation", "Sandbox de malware", "🧪",
     r"(malware[ -]?sandbox|sandbox.{0,20}malware|cuckoo[ -]?sandbox|\bcuckoo\b|cape[ -]?sandbox|"
     r"drakvuf|detonat(e|ion|ing)|dynamic[ -]?malware[ -]?analysis|automated[ -]?malware[ -]?analysis)"),
    ("data_exfiltration", "Data Exfiltration", "Exfiltration de données", "📤",
     r"(exfiltrat|data[ -]?exfil|dns[ -]?(tunnel|exfil)|dnscat|icmp[ -]?tunnel|"
     r"covert[ -]?channel|egress[ -]?(test|check|busting))"),
]


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    categories = data["categories"]
    by_id = {c["id"]: c for c in categories}

    # 1) Ensure the new categories exist (insert before the update/uninstall menu).
    patterns: list[tuple[str, re.Pattern]] = []
    insert_at = next((i for i, c in enumerate(categories) if c["id"] == "update_uninstall"),
                     len(categories))
    for cid, title, title_fr, icon, pat in NEW_CATEGORIES:
        patterns.append((cid, re.compile(pat, re.IGNORECASE)))
        if cid not in by_id:
            cat = {"id": cid, "title": title, "title_fr": title_fr,
                   "full_title": title, "icon": icon, "tools": []}
            categories.insert(insert_at, cat)
            by_id[cid] = cat
            insert_at += 1
            print(f"  + category {cid}")

    new_ids = {cid for cid, *_ in NEW_CATEGORIES}

    # 2) Reclassify existing tools by first-matching precise pattern.
    moves: dict[str, list[str]] = {cid: [] for cid in new_ids}
    for cat in categories:
        if cat["id"] in new_ids:
            continue
        keep = []
        for tool in cat.get("tools", []):
            blob = f"{tool.get('title','')} {tool.get('description','')}"
            target = next((cid for cid, rx in patterns if rx.search(blob)), None)
            if target and target != cat["id"]:
                by_id[target]["tools"].append(tool)
                moves[target].append(tool.get("title", "?"))
            else:
                keep.append(tool)
        cat["tools"] = keep

    # 3) Report + refresh meta.
    for cid, *_ in NEW_CATEGORIES:
        titles = moves.get(cid, [])
        sample = ", ".join(titles[:4])
        print(f"  {cid:<18} +{len(titles):>4}  e.g. {sample}")

    total = sum(len(c.get("tools", [])) for c in categories)
    data.setdefault("meta", {})
    data["meta"]["tools"] = total
    data["meta"]["categories"] = len(categories)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Total categories: {len(categories)}  |  total tools: {total}")


if __name__ == "__main__":
    main()
