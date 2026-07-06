#!/usr/bin/env python3
"""Third wave of essential-tool curation with correct, Kali-ready commands.

Same upgrade-in-place logic as curate_flagships.py / curate_essentials.py.
Run:  python scripts/curate_essentials2.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


ESSENTIALS: dict[str, list[dict]] = {
    "information_gathering": [
        {"title": "massdns", "description": "High-performance DNS stub resolver for bulk lookups and subdomain brute force.",
         "install": ["sudo apt install -y massdns"], "run": ["massdns -h"], "url": "https://github.com/blechschmidt/massdns", "tags": ["recon"]},
        {"title": "httprobe", "description": "Take a list of domains and probe for working HTTP/HTTPS servers.",
         "install": ["go install github.com/tomnomnom/httprobe@latest"], "run": ["httprobe -h"], "url": "https://github.com/tomnomnom/httprobe", "tags": ["recon", "web"]},
        {"title": "github-subdomains", "description": "Find subdomains of a target by scraping GitHub.",
         "install": ["go install github.com/gwen001/github-subdomains@latest"], "run": ["github-subdomains -h"], "url": "https://github.com/gwen001/github-subdomains", "tags": ["recon", "osint"]},
        {"title": "dnsvalidator", "description": "Build reliable lists of valid DNS resolvers for mass DNS tools.",
         "install": ["pipx install git+https://github.com/vortexau/dnsvalidator.git"], "run": ["dnsvalidator -h"], "url": "https://github.com/vortexau/dnsvalidator", "tags": ["recon"]},
    ],
    "osint": [
        {"title": "GHunt", "description": "Investigate Google accounts (Gmail, docs, reviews, devices) from an email.",
         "install": ["pipx install ghunt"], "run": ["ghunt --help"], "url": "https://github.com/mxrch/GHunt", "tags": ["osint"]},
        {"title": "Toutatis", "description": "Extract information (email, phone) from Instagram accounts.",
         "install": ["pipx install toutatis"], "run": ["toutatis -h"], "url": "https://github.com/megadose/toutatis", "tags": ["osint"]},
        {"title": "Ignorant", "description": "Check if a phone number is used on sites via account-recovery leaks.",
         "install": ["pipx install ignorant"], "run": ["ignorant --help"], "url": "https://github.com/megadose/ignorant", "tags": ["osint"]},
    ],
    "web_attack": [
        {"title": "dirb", "description": "Classic web content scanner — dictionary-based directory/file brute force.",
         "install": ["sudo apt install -y dirb"], "run": ["dirb"], "url": "https://gitlab.com/kalilinux/packages/dirb", "tags": ["web", "bruteforce"]},
        {"title": "DotDotPwn", "description": "Directory-traversal fuzzer for finding path-traversal vulnerabilities.",
         "install": ["sudo apt install -y dotdotpwn"], "run": ["dotdotpwn -h"], "url": "https://github.com/wireghoul/dotdotpwn", "tags": ["web"]},
    ],
    "wireless_attack": [
        {"title": "Wifiphisher", "description": "Rogue Access Point framework for red-team Wi-Fi phishing and MITM.",
         "install": ["sudo apt install -y wifiphisher"], "run": ["sudo wifiphisher"], "url": "https://github.com/wifiphisher/wifiphisher", "tags": ["wireless", "social-engineering"]},
        {"title": "pixiewps", "description": "Offline WPS brute-force (Pixie-Dust attack).",
         "install": ["sudo apt install -y pixiewps"], "run": ["pixiewps -h"], "url": "https://github.com/wiire-a/pixiewps", "tags": ["wireless"]},
    ],
    "forensics": [
        {"title": "RegRipper", "description": "Extract and parse data from Windows Registry hives for forensics.",
         "install": ["sudo apt install -y regripper"], "run": ["regripper"], "url": "https://github.com/keydet89/RegRipper3.0", "tags": ["forensics"]},
        {"title": "Plaso", "description": "Automatic timeline generation from forensic artifacts (log2timeline).",
         "install": ["sudo apt install -y plaso"], "run": ["log2timeline.py -h"], "url": "https://github.com/log2timeline/plaso", "tags": ["forensics"]},
    ],
    "reverse_engineering": [
        {"title": "Rizin", "description": "Free reverse-engineering framework (radare2 fork) — disassembler & analysis.",
         "install": ["sudo apt install -y rizin"], "run": ["rizin -h"], "url": "https://github.com/rizinorg/rizin", "tags": ["reversing"]},
        {"title": "edb-debugger", "description": "Cross-platform x86/x86-64 debugger with a Qt GUI (Evan's Debugger).",
         "install": ["sudo apt install -y edb-debugger"], "run": ["edb"], "url": "https://github.com/eteran/edb-debugger", "tags": ["reversing"]},
    ],
    "mobile_security": [
        {"title": "APKiD", "description": "Identify packers, obfuscators and compilers in Android APKs.",
         "install": ["pipx install apkid"], "run": ["apkid -h"], "url": "https://github.com/rednaga/APKiD", "tags": ["mobile", "reversing"]},
        {"title": "frida-tools", "description": "CLI toolkit for Frida — dynamic instrumentation for mobile/desktop apps.",
         "install": ["pipx install frida-tools"], "run": ["frida --help"], "url": "https://github.com/frida/frida", "tags": ["mobile", "reversing"]},
    ],
    "cloud_security": [
        {"title": "Cloudsplaining", "description": "AWS IAM security assessment that finds risky policies and generates a report.",
         "install": ["pipx install cloudsplaining"], "run": ["cloudsplaining --help"], "url": "https://github.com/salesforce/cloudsplaining", "tags": ["cloud"]},
    ],
    "wordlist_generator": [
        {"title": "crowbar", "description": "Brute-forcing tool for protocols not supported by most crackers (RDP, OpenVPN, SSH keys).",
         "install": ["sudo apt install -y crowbar"], "run": ["crowbar -h"], "url": "https://github.com/galkan/crowbar", "tags": ["bruteforce"]},
        {"title": "RSMangler", "description": "Take a wordlist and mangle it (permutations, leet, case) to expand candidates.",
         "install": ["sudo apt install -y rsmangler"], "run": ["rsmangler -h"], "url": "https://github.com/digininja/RSMangler", "tags": ["wordlist"]},
    ],
    "vuln_scanning": [
        {"title": "Jaeles", "description": "Powerful, flexible framework for building and running web vuln signatures.",
         "install": ["go install github.com/jaeles-project/jaeles@latest"], "run": ["jaeles -h"], "url": "https://github.com/jaeles-project/jaeles", "tags": ["web", "scanner"]},
    ],
    "api_security": [
        {"title": "graphql-cop", "description": "Security auditor for GraphQL endpoints (common misconfigurations).",
         "install": ["pipx install graphql-cop"], "run": ["graphql-cop -h"], "url": "https://github.com/dolevf/graphql-cop", "tags": ["web"]},
    ],
    "binary_exploitation": [
        {"title": "ropr", "description": "Blazing-fast ROP gadget finder for building exploit chains.",
         "install": ["cargo install ropr"], "run": ["ropr -h"], "url": "https://github.com/Ben-Lichtman/ropr", "tags": ["reversing"]},
    ],
    "data_exfiltration": [
        {"title": "dnscat2", "description": "Command-and-control and data exfiltration over the DNS protocol.",
         "install": ["sudo apt install -y dnscat2"], "run": ["dnscat2 --help"], "url": "https://github.com/iagox86/dnscat2", "tags": ["c2", "network"]},
        {"title": "iodine", "description": "Tunnel IPv4 data through a DNS server (DNS tunneling).",
         "install": ["sudo apt install -y iodine"], "run": ["iodine -h"], "url": "https://github.com/yarrick/iodine", "tags": ["network"]},
    ],
    "radio_sdr": [
        {"title": "rtl_433", "description": "Decode ISM-band radio signals (433/868/915 MHz) from cheap RTL-SDR dongles.",
         "install": ["sudo apt install -y rtl-433"], "run": ["rtl_433 -h"], "url": "https://github.com/merbanan/rtl_433", "tags": ["wireless"]},
        {"title": "Universal Radio Hacker", "description": "Investigate wireless protocols end-to-end (demodulate, decode, fuzz).",
         "install": ["pipx install urh"], "run": ["urh"], "url": "https://github.com/jopohl/urh", "tags": ["wireless"]},
        {"title": "inspectrum", "description": "Offline radio-signal analyser for reverse-engineering captured transmissions.",
         "install": ["sudo apt install -y inspectrum"], "run": ["inspectrum"], "url": "https://github.com/miek/inspectrum", "tags": ["wireless"]},
    ],
    "automotive": [
        {"title": "can-utils", "description": "Linux SocketCAN userspace tools (candump, cansend, cangen) for car hacking.",
         "install": ["sudo apt install -y can-utils"], "run": ["candump"], "url": "https://github.com/linux-can/can-utils", "tags": ["automobile"]},
    ],
    "voip": [
        {"title": "SIPVicious", "description": "Suite for auditing SIP-based VoIP systems (svmap, svwar, svcrack).",
         "install": ["sudo apt install -y sipvicious"], "run": ["svmap -h"], "url": "https://github.com/enablesecurity/sipvicious", "tags": ["network"]},
    ],
    "network_sniffing": [
        {"title": "netsniff-ng", "description": "High-performance zero-copy networking toolkit (sniffer, pcap, traffic gen).",
         "install": ["sudo apt install -y netsniff-ng"], "run": ["netsniff-ng --help"], "url": "https://github.com/netsniff-ng/netsniff-ng", "tags": ["network"]},
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
                existing = cats[loc_cid]["tools"][idx]
                existing.update({
                    "description": new["description"], "install": new["install"], "run": new["run"],
                    "url": new["url"] or existing.get("url", ""),
                    "tags": sorted(set(existing.get("tags", [])) | set(new["tags"])),
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
    print(f"Essentials wave 3 — upgraded: {upgraded}  |  added: {added}  |  total tools now: {total}")


if __name__ == "__main__":
    main()
