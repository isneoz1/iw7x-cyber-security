#!/usr/bin/env python3
"""Curate a second wave of essential tools with correct, Kali-ready commands.

Same upgrade-in-place logic as curate_flagships.py: if a tool with the same
title already exists (from the scraper) we upgrade its install/run commands so
it "just works" after install; otherwise we add it to its category.

Run:  python scripts/curate_essentials.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


# category_id -> essential tools (Kali-ready install/run). Not covered by
# curate_flagships.py / curate_more.py.
ESSENTIALS: dict[str, list[dict]] = {
    "information_gathering": [
        {"title": "Recon-ng", "description": "Full-featured web reconnaissance framework with modules and workspaces.",
         "install": ["sudo apt install -y recon-ng"], "run": ["recon-ng"], "url": "https://github.com/lanmaster53/recon-ng", "tags": ["recon", "osint"]},
        {"title": "Sublist3r", "description": "Fast subdomain enumeration using OSINT search engines.",
         "install": ["sudo apt install -y sublist3r"], "run": ["sublist3r -h"], "url": "https://github.com/aboul3la/Sublist3r", "tags": ["recon"]},
        {"title": "dnsenum", "description": "Enumerate DNS info: hosts, name servers, MX, zone transfers, brute force.",
         "install": ["sudo apt install -y dnsenum"], "run": ["dnsenum"], "url": "https://github.com/fwaeytens/dnsenum", "tags": ["recon"]},
        {"title": "metagoofil", "description": "Extract metadata from a target's public documents (authors, software, paths).",
         "install": ["sudo apt install -y metagoofil"], "run": ["metagoofil -h"], "url": "https://github.com/opsdisk/metagoofil", "tags": ["osint", "recon"]},
        {"title": "hakrawler", "description": "Fast web crawler for gathering URLs and endpoints from a target.",
         "install": ["go install github.com/hakluke/hakrawler@latest"], "run": ["hakrawler -h"], "url": "https://github.com/hakluke/hakrawler", "tags": ["recon", "web"]},
        {"title": "gf", "description": "A wrapper around grep with curated patterns to find bug-bounty gold in URLs.",
         "install": ["go install github.com/tomnomnom/gf@latest"], "run": ["gf -h"], "url": "https://github.com/tomnomnom/gf", "tags": ["recon", "web"]},
        {"title": "anew", "description": "Append lines from stdin to a file only if they don't already exist.",
         "install": ["go install github.com/tomnomnom/anew@latest"], "run": ["anew -h"], "url": "https://github.com/tomnomnom/anew", "tags": ["recon"]},
        {"title": "unfurl", "description": "Pull out bits of URLs (domains, paths, params) from stdin at scale.",
         "install": ["go install github.com/tomnomnom/unfurl@latest"], "run": ["unfurl --help"], "url": "https://github.com/tomnomnom/unfurl", "tags": ["recon", "web"]},
        {"title": "qsreplace", "description": "Replace query-string values, useful for fuzzing and injection testing.",
         "install": ["go install github.com/tomnomnom/qsreplace@latest"], "run": ["qsreplace -h"], "url": "https://github.com/tomnomnom/qsreplace", "tags": ["web"]},
    ],
    "web_attack": [
        {"title": "JoomScan", "description": "OWASP Joomla vulnerability scanner.",
         "install": ["sudo apt install -y joomscan"], "run": ["joomscan --help"], "url": "https://github.com/OWASP/joomscan", "tags": ["web", "scanner"]},
        {"title": "droopescan", "description": "Plugin-based scanner for Drupal, SilverStripe and other CMSs.",
         "install": ["pipx install droopescan"], "run": ["droopescan --help"], "url": "https://github.com/SamJoan/droopescan", "tags": ["web", "scanner"]},
        {"title": "CRLFuzz", "description": "Fast tool to scan CRLF-injection vulnerabilities.",
         "install": ["go install github.com/dwisiswant0/crlfuzz/cmd/crlfuzz@latest"], "run": ["crlfuzz -h"], "url": "https://github.com/dwisiswant0/crlfuzz", "tags": ["web"]},
        {"title": "ParamSpider", "description": "Mine URL parameters from web archives for fuzzing targets.",
         "install": ["pipx install paramspider"], "run": ["paramspider -h"], "url": "https://github.com/devanshbatham/ParamSpider", "tags": ["web", "recon"]},
        {"title": "BeEF", "description": "The Browser Exploitation Framework — hook and control browsers.",
         "install": ["sudo apt install -y beef-xss"], "run": ["sudo beef-xss"], "url": "https://github.com/beefproject/beef", "tags": ["web", "exploit"]},
    ],
    "wordlist_generator": [
        {"title": "Medusa", "description": "Speedy, parallel, modular login brute-forcer for many protocols.",
         "install": ["sudo apt install -y medusa"], "run": ["medusa -h"], "url": "https://github.com/jmk-foofus/medusa", "tags": ["bruteforce"]},
        {"title": "Ncrack", "description": "High-speed network authentication cracking tool from the Nmap project.",
         "install": ["sudo apt install -y ncrack"], "run": ["ncrack"], "url": "https://nmap.org/ncrack/", "tags": ["bruteforce"]},
        {"title": "Patator", "description": "Multi-purpose brute-forcer with a modular design.",
         "install": ["sudo apt install -y patator"], "run": ["patator"], "url": "https://github.com/lanjelot/patator", "tags": ["bruteforce"]},
        {"title": "crunch", "description": "Generate custom wordlists by pattern and character set.",
         "install": ["sudo apt install -y crunch"], "run": ["crunch"], "url": "https://github.com/crunchsec/crunch", "tags": ["bruteforce", "wordlist"]},
        {"title": "CUPP", "description": "Common User Passwords Profiler — build targeted wordlists from OSINT.",
         "install": ["sudo apt install -y cupp"], "run": ["cupp -h"], "url": "https://github.com/Mebus/cupp", "tags": ["wordlist"]},
    ],
    "active_directory": [
        {"title": "evil-winrm", "description": "The ultimate WinRM shell for pentesting Windows/AD.",
         "install": ["sudo apt install -y evil-winrm || sudo gem install evil-winrm"], "run": ["evil-winrm -h"], "url": "https://github.com/Hackplayers/evil-winrm", "tags": ["active-directory"]},
        {"title": "ldapsearch", "description": "Query LDAP/Active Directory directories from the shell (ldap-utils).",
         "install": ["sudo apt install -y ldap-utils"], "run": ["ldapsearch -x -H ldap://TARGET -b 'dc=example,dc=com'"], "url": "https://linux.die.net/man/1/ldapsearch", "tags": ["active-directory"]},
    ],
    "exploit_framework": [
        {"title": "RouterSploit", "description": "Exploitation framework dedicated to embedded devices and routers.",
         "install": ["sudo apt install -y routersploit || pipx install routersploit"], "run": ["routersploit"], "url": "https://github.com/threat9/routersploit", "tags": ["exploit"]},
        {"title": "PowerShell-Empire", "description": "Post-exploitation and C2 framework (PowerShell/Python agents).",
         "install": ["sudo apt install -y powershell-empire"], "run": ["powershell-empire server"], "url": "https://github.com/BC-SECURITY/Empire", "tags": ["c2", "exploit"]},
    ],
    "network_sniffing": [
        {"title": "Scapy", "description": "Interactive packet manipulation: craft, send, sniff and dissect packets.",
         "install": ["sudo apt install -y python3-scapy"], "run": ["scapy"], "url": "https://github.com/secdev/scapy", "tags": ["network"]},
        {"title": "dsniff", "description": "Classic suite of network sniffing/MITM tools (arpspoof, dsniff, urlsnarf…).",
         "install": ["sudo apt install -y dsniff"], "run": ["dsniff -h"], "url": "https://www.monkey.org/~dugsong/dsniff/", "tags": ["network"]},
        {"title": "driftnet", "description": "Watch images travelling across the network from sniffed traffic.",
         "install": ["sudo apt install -y driftnet"], "run": ["driftnet -h"], "url": "https://github.com/deiv/driftnet", "tags": ["network"]},
        {"title": "tshark", "description": "The command-line version of Wireshark for packet capture and analysis.",
         "install": ["sudo apt install -y tshark"], "run": ["tshark -h"], "url": "https://www.wireshark.org/docs/man-pages/tshark.html", "tags": ["network", "forensics"]},
    ],
    "phishing_attack": [
        {"title": "King Phisher", "description": "Phishing campaign toolkit for testing and awareness training.",
         "install": ["sudo apt install -y king-phisher"], "run": ["king-phisher"], "url": "https://github.com/rsmusllp/king-phisher", "tags": ["social-engineering"]},
    ],
    "vuln_scanning": [
        {"title": "Lynis", "description": "Security auditing and hardening tool for Linux/Unix systems.",
         "install": ["sudo apt install -y lynis"], "run": ["sudo lynis audit system"], "url": "https://github.com/CISOfy/lynis", "tags": ["scanner", "blue_team"]},
        {"title": "Legion", "description": "Semi-automated network penetration testing framework (GUI).",
         "install": ["sudo apt install -y legion"], "run": ["sudo legion"], "url": "https://github.com/GoVanguard/legion", "tags": ["scanner"]},
        {"title": "OpenVAS / GVM", "description": "Greenbone Vulnerability Management — full-featured vulnerability scanner.",
         "install": ["sudo apt install -y gvm", "sudo gvm-setup"], "run": ["sudo gvm-start"], "url": "https://github.com/greenbone/gvmd", "tags": ["scanner"]},
    ],
    "fuzzing": [
        {"title": "honggfuzz", "description": "Security-oriented, feedback-driven, evolutionary fuzzer.",
         "install": ["sudo apt install -y honggfuzz"], "run": ["honggfuzz -h"], "url": "https://github.com/google/honggfuzz", "tags": ["fuzzing", "reversing"]},
        {"title": "Radamsa", "description": "General-purpose black-box mutation fuzzer.",
         "install": ["sudo apt install -y radamsa"], "run": ["radamsa --help"], "url": "https://gitlab.com/akihe/radamsa", "tags": ["fuzzing"]},
    ],
    "mobile_security": [
        {"title": "apkleaks", "description": "Scan APKs for URIs, endpoints and secrets.",
         "install": ["pipx install apkleaks"], "run": ["apkleaks -h"], "url": "https://github.com/dwisiswant0/apkleaks", "tags": ["mobile"]},
        {"title": "mobsfscan", "description": "Static analysis tool to find insecure code patterns in Android/iOS apps.",
         "install": ["pipx install mobsfscan"], "run": ["mobsfscan --help"], "url": "https://github.com/MobSF/mobsfscan", "tags": ["mobile"]},
    ],
    "malware_analysis": [
        {"title": "capa", "description": "Identify capabilities in executable files (FLARE).",
         "install": ["pipx install flare-capa"], "run": ["capa -h"], "url": "https://github.com/mandiant/capa", "tags": ["reversing", "forensics"]},
        {"title": "FLOSS", "description": "Automatically extract obfuscated strings from malware (FLARE).",
         "install": ["pipx install flare-floss"], "run": ["floss -h"], "url": "https://github.com/mandiant/flare-floss", "tags": ["reversing", "forensics"]},
    ],
    "cloud_security": [
        {"title": "AWS CLI", "description": "Official AWS command-line client — the base for most AWS attack tooling.",
         "install": ["sudo apt install -y awscli"], "run": ["aws help"], "url": "https://github.com/aws/aws-cli", "tags": ["cloud"]},
        {"title": "Cartography", "description": "Map assets and their relationships across cloud/SaaS into a graph (Neo4j).",
         "install": ["pipx install cartography"], "run": ["cartography --help"], "url": "https://github.com/lyft/cartography", "tags": ["cloud"]},
    ],
    "supply_chain": [
        {"title": "Syft", "description": "Generate a Software Bill of Materials (SBOM) from images and filesystems.",
         "install": ["curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sudo sh -s -- -b /usr/local/bin"], "run": ["syft version"], "url": "https://github.com/anchore/syft", "tags": ["scanner"]},
        {"title": "Grype", "description": "Vulnerability scanner for container images and filesystems (SBOM-driven).",
         "install": ["curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin"], "run": ["grype version"], "url": "https://github.com/anchore/grype", "tags": ["scanner"]},
        {"title": "osv-scanner", "description": "Scan dependencies for known vulnerabilities using the OSV database.",
         "install": ["go install github.com/google/osv-scanner/cmd/osv-scanner@latest"], "run": ["osv-scanner --help"], "url": "https://github.com/google/osv-scanner", "tags": ["scanner"]},
    ],
    "threat_hunting": [
        {"title": "Sigma CLI", "description": "Convert and manage Sigma detection rules for SIEM/EDR backends.",
         "install": ["pipx install sigma-cli"], "run": ["sigma --help"], "url": "https://github.com/SigmaHQ/sigma-cli", "tags": ["blue_team", "forensics"]},
    ],
    "wireless_attack": [
        {"title": "Reaver", "description": "Brute-force attack against WPS to recover WPA/WPA2 passphrases.",
         "install": ["sudo apt install -y reaver"], "run": ["reaver -h"], "url": "https://github.com/t6x/reaver-wps-fork-t6x", "tags": ["wireless"]},
        {"title": "Bully", "description": "WPS brute-force attack implemented in C.",
         "install": ["sudo apt install -y bully"], "run": ["bully"], "url": "https://github.com/aanarchyy/bully", "tags": ["wireless"]},
        {"title": "Kismet", "description": "Wireless network and device detector, sniffer and IDS.",
         "install": ["sudo apt install -y kismet"], "run": ["kismet"], "url": "https://www.kismetwireless.net/", "tags": ["wireless"]},
        {"title": "mdk4", "description": "Wi-Fi testing/attack tool (deauth, beacon flood, and more).",
         "install": ["sudo apt install -y mdk4"], "run": ["mdk4 --help"], "url": "https://github.com/aircrack-ng/mdk4", "tags": ["wireless"]},
        {"title": "airgeddon", "description": "Multi-use bash script to audit wireless networks (menu-driven).",
         "install": ["sudo apt install -y airgeddon"], "run": ["sudo airgeddon"], "url": "https://github.com/v1s1t0r1sh3r3/airgeddon", "tags": ["wireless"]},
        {"title": "hcxtools", "description": "Convert and analyse captures for hashcat (PMKID/handshake).",
         "install": ["sudo apt install -y hcxtools"], "run": ["hcxpcapngtool --help"], "url": "https://github.com/ZerBea/hcxtools", "tags": ["wireless"]},
    ],
    "binary_exploitation": [
        {"title": "Z3", "description": "High-performance theorem prover, widely used for symbolic solving in CTFs.",
         "install": ["sudo apt install -y z3"], "run": ["z3 --help"], "url": "https://github.com/Z3Prover/z3", "tags": ["reversing"]},
    ],
    "forensics": [
        {"title": "dc3dd", "description": "Patched dd for forensic acquisition with hashing and progress.",
         "install": ["sudo apt install -y dc3dd"], "run": ["dc3dd --help"], "url": "https://sourceforge.net/projects/dc3dd/", "tags": ["forensics"]},
        {"title": "ddrescue", "description": "Data-recovery tool that copies data from failing drives/images.",
         "install": ["sudo apt install -y gddrescue"], "run": ["ddrescue --help"], "url": "https://www.gnu.org/software/ddrescue/", "tags": ["forensics"]},
    ],
}


def to_tool(d: dict) -> dict:
    return {
        "title": d["title"],
        "description": d["description"],
        "install": list(d.get("install", [])),
        "run": list(d.get("run", [])),
        "uninstall": list(d.get("uninstall", [])),
        "url": d.get("url", ""),
        "tags": list(d.get("tags", [])),
        "os": list(d.get("os", ["linux"])),
        "archived": False,
        "archived_reason": "",
        "requires_root": bool(d.get("requires_root", False)),
        "installable": True,
        "runnable": True,
        "subgroup": d.get("subgroup", ""),
        "flagship": True,
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
                    "description": new["description"],
                    "install": new["install"],
                    "run": new["run"],
                    "url": new["url"] or existing.get("url", ""),
                    "tags": sorted(set(existing.get("tags", [])) | set(new["tags"])),
                    "os": ["linux"],
                    "installable": True,
                    "runnable": True,
                    "archived": False,
                    "flagship": True,
                })
                upgraded += 1
            else:
                cats[cid].setdefault("tools", []).append(new)
                title_loc[key] = (cid, len(cats[cid]["tools"]) - 1)
                added += 1

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})
    data["meta"]["tools"] = total
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Essentials upgraded: {upgraded}  |  added: {added}  |  total tools now: {total}")


if __name__ == "__main__":
    main()
