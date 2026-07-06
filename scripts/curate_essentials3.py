#!/usr/bin/env python3
"""Fourth wave of curation — Kali-ready commands for the thinner categories.
Same upgrade-in-place logic. Run: python scripts/curate_essentials3.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


ESSENTIALS: dict[str, list[dict]] = {
    "honeypots": [
        {"title": "OpenCanary", "description": "Lightweight, multi-protocol honeypot daemon that alerts on intrusions.",
         "install": ["pipx install opencanary"], "run": ["opencanaryd --help"], "url": "https://github.com/thinkst/opencanary", "tags": ["blue_team"]},
        {"title": "Honeypots", "description": "30+ ready-to-run honeypots in a single package (SSH, HTTP, FTP, SMB…).",
         "install": ["pipx install honeypots"], "run": ["honeypots --help"], "url": "https://github.com/qeeqbox/honeypots", "tags": ["blue_team"]},
        {"title": "Heralding", "description": "Credential-catching honeypot for many protocols.",
         "install": ["pipx install heralding"], "run": ["heralding --help"], "url": "https://github.com/johnnykv/heralding", "tags": ["blue_team"]},
    ],
    "ctf_tools": [
        {"title": "socat", "description": "Multipurpose relay for bidirectional data transfer — a CTF/pwn staple.",
         "install": ["sudo apt install -y socat"], "run": ["socat -h"], "url": "http://www.dest-unreach.org/socat/", "tags": ["network"]},
        {"title": "seccomp-tools", "description": "Dump and analyse seccomp rules — essential for sandbox-escape CTF challenges.",
         "install": ["sudo gem install seccomp-tools"], "run": ["seccomp-tools --help"], "url": "https://github.com/david942j/seccomp-tools", "tags": ["reversing"]},
    ],
    "sandbox_analysis": [
        {"title": "firejail", "description": "SUID sandbox to run untrusted programs in a restricted environment.",
         "install": ["sudo apt install -y firejail"], "run": ["firejail --help"], "url": "https://github.com/netblue30/firejail", "tags": ["blue_team"]},
        {"title": "bubblewrap", "description": "Unprivileged sandboxing tool used to detonate/analyse untrusted binaries.",
         "install": ["sudo apt install -y bubblewrap"], "run": ["bwrap --help"], "url": "https://github.com/containers/bubblewrap", "tags": ["blue_team"]},
    ],
    "data_exfiltration": [
        {"title": "ptunnel-ng", "description": "Tunnel TCP connections over ICMP echo (ping) packets.",
         "install": ["sudo apt install -y ptunnel-ng || sudo apt install -y ptunnel"], "run": ["ptunnel-ng -h"], "url": "https://github.com/lnslbrty/ptunnel-ng", "tags": ["network"]},
        {"title": "stunnel", "description": "Wrap arbitrary TCP services in TLS — useful for covert channels and pivoting.",
         "install": ["sudo apt install -y stunnel4"], "run": ["stunnel -help"], "url": "https://www.stunnel.org/", "tags": ["network"]},
    ],
    "supply_chain": [
        {"title": "pip-audit", "description": "Audit Python environments and requirements for known vulnerabilities.",
         "install": ["pipx install pip-audit"], "run": ["pip-audit --help"], "url": "https://github.com/pypa/pip-audit", "tags": ["scanner"]},
        {"title": "Safety", "description": "Check Python dependencies against a database of known security issues.",
         "install": ["pipx install safety"], "run": ["safety --help"], "url": "https://github.com/pyupio/safety", "tags": ["scanner"]},
    ],
    "blockchain_web3": [
        {"title": "Slither", "description": "Static analysis framework for Solidity smart contracts (Trail of Bits).",
         "install": ["pipx install slither-analyzer"], "run": ["slither --help"], "url": "https://github.com/crytic/slither", "tags": ["web3"]},
        {"title": "Mythril", "description": "Security analysis tool for EVM bytecode / smart contracts.",
         "install": ["pipx install mythril"], "run": ["myth version"], "url": "https://github.com/Consensys/mythril", "tags": ["web3"]},
    ],
    "radio_sdr": [
        {"title": "multimon-ng", "description": "Decode digital radio transmissions (POCSAG, FLEX, AFSK, DTMF…).",
         "install": ["sudo apt install -y multimon-ng"], "run": ["multimon-ng -h"], "url": "https://github.com/EliasOenal/multimon-ng", "tags": ["wireless"]},
        {"title": "Gqrx SDR", "description": "Open-source software-defined radio receiver powered by GNU Radio.",
         "install": ["sudo apt install -y gqrx-sdr"], "run": ["gqrx"], "url": "https://github.com/gqrx-sdr/gqrx", "tags": ["wireless"]},
    ],
    "ai_ml_security": [
        {"title": "garak", "description": "LLM vulnerability scanner — probes for jailbreaks, prompt injection and leaks.",
         "install": ["pipx install garak"], "run": ["garak --help"], "url": "https://github.com/NVIDIA/garak", "tags": ["ai"]},
        {"title": "ModelScan", "description": "Scan ML models (pickle, TF, Keras…) for unsafe code and supply-chain risks.",
         "install": ["pipx install modelscan"], "run": ["modelscan -h"], "url": "https://github.com/protectai/modelscan", "tags": ["ai"]},
    ],
    "game_hacking": [
        {"title": "scanmem / GameConqueror", "description": "Memory scanner/editor for Linux (the Cheat Engine equivalent).",
         "install": ["sudo apt install -y scanmem"], "run": ["scanmem -h"], "url": "https://github.com/scanmem/scanmem", "tags": ["reversing"]},
    ],
    "steganography": [
        {"title": "StegCracker", "description": "Brute-force hidden data in files created with steghide.",
         "install": ["pipx install stegcracker"], "run": ["stegcracker --help"], "url": "https://github.com/Paradoxis/StegCracker", "tags": ["steganography"]},
    ],
    "phishing_attack": [
        {"title": "Modlishka", "description": "Reverse-proxy phishing framework that automates 2FA-bypass campaigns.",
         "install": ["go install github.com/drk1wi/Modlishka@latest"], "run": ["Modlishka -h"], "url": "https://github.com/drk1wi/Modlishka", "tags": ["social-engineering"]},
    ],
    "ddos_attack": [
        {"title": "hping3", "description": "Command-line packet crafter/analyser for TCP/IP — flooding, scanning, testing.",
         "install": ["sudo apt install -y hping3"], "run": ["hping3 -h"], "url": "https://github.com/antirez/hping", "tags": ["network", "ddos"]},
        {"title": "slowhttptest", "description": "Test servers against slow-HTTP (Slowloris-style) denial-of-service attacks.",
         "install": ["sudo apt install -y slowhttptest"], "run": ["slowhttptest -h"], "url": "https://github.com/shekyan/slowhttptest", "tags": ["ddos"]},
    ],
}


def to_tool(d: dict) -> dict:
    return {
        "title": d["title"], "description": d["description"],
        "install": list(d.get("install", [])), "run": list(d.get("run", [])),
        "uninstall": list(d.get("uninstall", [])), "url": d.get("url", ""),
        "tags": list(d.get("tags", [])), "os": list(d.get("os", ["linux"])),
        "archived": False, "archived_reason": "", "requires_root": bool(d.get("requires_root", False)),
        "installable": True, "runnable": True, "subgroup": d.get("subgroup", ""), "flagship": True,
    }


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    cats = {c["id"]: c for c in data["categories"]}
    title_loc: dict[str, tuple[str, int]] = {}
    for cid, cat in cats.items():
        for i, tool in enumerate(cat.get("tools", [])):
            title_loc.setdefault(norm(tool.get("title", "")), (cid, i))

    added = upgraded = 0
    for cid, tools in ESSENTIALS.items():
        if cid not in cats:
            print(f"  ! unknown category {cid}, skipping")
            continue
        for spec in tools:
            new = to_tool(spec)
            key = norm(new["title"])
            if key in title_loc:
                loc_cid, idx = title_loc[key]
                cats[loc_cid]["tools"][idx].update({
                    "description": new["description"], "install": new["install"], "run": new["run"],
                    "url": new["url"] or cats[loc_cid]["tools"][idx].get("url", ""),
                    "tags": sorted(set(cats[loc_cid]["tools"][idx].get("tags", [])) | set(new["tags"])),
                    "os": ["linux"], "installable": True, "runnable": True, "archived": False, "flagship": True,
                })
                upgraded += 1
            else:
                cats[cid].setdefault("tools", []).append(new)
                title_loc[key] = (cid, len(cats[cid]["tools"]) - 1)
                added += 1

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})["tools"] = total
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Essentials wave 4 — upgraded: {upgraded}  |  added: {added}  |  total tools now: {total}")


if __name__ == "__main__":
    main()
