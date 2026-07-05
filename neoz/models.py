"""Declarative data model for the NeoZ Toolkit.

The whole arsenal lives in ``catalog.json``. This module turns it into typed
``Tool`` / ``Category`` objects and builds the search + tag indexes. No tool
logic is hand-written — add a tool by adding a JSON entry.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from functools import lru_cache

CATALOG_PATH = Path(__file__).resolve().parent.parent / "catalog.json"


@dataclass(frozen=True)
class Tool:
    title: str
    description: str
    install: tuple[str, ...] = ()
    run: tuple[str, ...] = ()
    uninstall: tuple[str, ...] = ()
    url: str = ""
    tags: tuple[str, ...] = ()
    os: tuple[str, ...] = ("linux", "macos")
    archived: bool = False
    archived_reason: str = ""
    requires_root: bool = False
    installable: bool = True
    runnable: bool = True
    subgroup: str = ""

    def short_description(self) -> str:
        first = (self.description or "—").splitlines()[0]
        return first if first else "—"


@dataclass(frozen=True)
class Category:
    id: str
    title: str          # French display title
    title_fr: str
    icon: str
    tools: tuple[Tool, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Catalog:
    author: str
    version: str
    source: str
    categories: tuple[Category, ...]

    @property
    def tool_count(self) -> int:
        return sum(len(c.tools) for c in self.categories)


def _tool_from_dict(d: dict) -> Tool:
    return Tool(
        title=d.get("title", ""),
        description=d.get("description", ""),
        install=tuple(d.get("install", [])),
        run=tuple(d.get("run", [])),
        uninstall=tuple(d.get("uninstall", [])),
        url=d.get("url", ""),
        tags=tuple(d.get("tags", [])),
        os=tuple(d.get("os", ["linux", "macos"])),
        archived=bool(d.get("archived", False)),
        archived_reason=d.get("archived_reason", ""),
        requires_root=bool(d.get("requires_root", False)),
        installable=bool(d.get("installable", True)),
        runnable=bool(d.get("runnable", True)),
        subgroup=d.get("subgroup", ""),
    )


@lru_cache(maxsize=1)
def load_catalog() -> Catalog:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    categories = tuple(
        Category(
            id=c["id"],
            title=c["title"],
            title_fr=c.get("title_fr", c["title"]),
            icon=c.get("icon", "•"),
            tools=tuple(_tool_from_dict(t) for t in c.get("tools", [])),
        )
        for c in data.get("categories", [])
    )
    return Catalog(
        author=meta.get("author", "NeoZ"),
        version=meta.get("version", "3.0.0"),
        source=meta.get("source", ""),
        categories=categories,
    )


# ── Cross-cutting queries ──────────────────────────────────────────────────────

def all_tools() -> list[tuple[Tool, Category]]:
    """Every (tool, category) pair across the catalog."""
    pairs: list[tuple[Tool, Category]] = []
    for cat in load_catalog().categories:
        for tool in cat.tools:
            pairs.append((tool, cat))
    return pairs


def search(query: str) -> list[tuple[Tool, Category]]:
    q = query.lower().strip()
    if not q:
        return []
    hits = []
    for tool, cat in all_tools():
        haystack = f"{tool.title} {tool.description} {' '.join(tool.tags)}".lower()
        if q in haystack:
            hits.append((tool, cat))
    return hits


# Auto-tag rules: derive tags from a tool's title + description so filtering
# works even when a tool declares no explicit tags.
_TAG_RULES: dict[str, str] = {
    r"(osint|harvester|maigret|holehe|spiderfoot|sherlock|recon)": "osint",
    r"(subdomain|subfinder|amass|sublist)": "recon",
    r"(scanner|scan|nmap|masscan|rustscan|nikto|nuclei|trivy)": "scanner",
    r"(brute|gobuster|ffuf|dirb|dirsearch|hashcat|john|kerbrute)": "bruteforce",
    r"(web|http|proxy|zap|xss|sql|wafw00f|arjun|mitmproxy)": "web",
    r"(wireless|wifi|wlan|airgeddon|bettercap|wifite|fluxion|deauth)": "wireless",
    r"(phish|social.?media|evilginx|setoolkit|social.?engineer)": "social-engineering",
    r"(c2|sliver|havoc|mythic|pwncat|reverse.?shell|pyshell)": "c2",
    r"(privesc|peass|linpeas|winpeas)": "privesc",
    r"(tunnel|pivot|ligolo|chisel|anon)": "network",
    r"(password|credential|hash|crack|secret|trufflehog|gitleaks)": "credentials",
    r"(forensic|memory|volatility|binwalk|autopsy|wireshark|pspy)": "forensics",
    r"(reverse.?eng|ghidra|radare|jadx|androguard|apk)": "reversing",
    r"(cloud|aws|azure|gcp|kubernetes|prowler|scout|pacu)": "cloud",
    r"(mobile|android|ios|frida|mobsf|objection|droid)": "mobile",
    r"(active.?directory|bloodhound|netexec|impacket|responder|certipy|kerberos|smb|ldap)": "active-directory",
    r"(ddos|dos|slowloris|goldeneye|ufonet)": "ddos",
    r"(payload|msfvenom|fatrat|venom|stitch|enigma)": "payload",
    r"(crawler|spider|katana|gospider)": "crawler",
    r"(steg|steganograph)": "steganography",
}


@lru_cache(maxsize=1)
def tag_index() -> dict[str, list[tuple[Tool, Category]]]:
    index: dict[str, list[tuple[Tool, Category]]] = {}
    for tool, cat in all_tools():
        tags = set(tool.tags)
        blob = f"{tool.title} {tool.description}".lower()
        for pattern, tag in _TAG_RULES.items():
            if re.search(pattern, blob):
                tags.add(tag)
        for tag in tags:
            index.setdefault(tag, []).append((tool, cat))
    return index


# Task -> tags mapping for the advisor.
ADVISOR: dict[str, list[str]] = {
    "Scan a network": ["scanner"],
    "Find subdomains": ["recon"],
    "Scan for vulnerabilities": ["scanner", "web"],
    "Crack passwords": ["bruteforce", "credentials"],
    "Find leaked secrets": ["credentials"],
    "Run a phishing campaign": ["social-engineering"],
    "Post-exploitation / C2": ["c2", "privesc"],
    "Pivot through a network": ["network"],
    "Pentest Active Directory": ["active-directory"],
    "Pentest a web app": ["web", "scanner"],
    "Pentest the cloud": ["cloud"],
    "Pentest a mobile app": ["mobile"],
    "Reverse engineer a binary": ["reversing"],
    "Capture a Wi-Fi handshake": ["wireless"],
    "Forensic analysis": ["forensics"],
    "Create payloads": ["payload"],
    "OSINT / recon a target": ["osint", "recon"],
    "Stay anonymous": ["network"],
}

ADVISOR_FR: dict[str, str] = {
    "Scan a network": "Scanner un réseau",
    "Find subdomains": "Trouver des sous-domaines",
    "Scan for vulnerabilities": "Chercher des vulnérabilités",
    "Crack passwords": "Casser des mots de passe",
    "Find leaked secrets": "Trouver des secrets exposés",
    "Run a phishing campaign": "Lancer une campagne de phishing",
    "Post-exploitation / C2": "Post-exploitation / C2",
    "Pivot through a network": "Pivoter dans un réseau",
    "Pentest Active Directory": "Auditer Active Directory",
    "Pentest a web app": "Auditer une application web",
    "Pentest the cloud": "Auditer le cloud",
    "Pentest a mobile app": "Auditer une application mobile",
    "Reverse engineer a binary": "Rétro-ingénierie d'un binaire",
    "Capture a Wi-Fi handshake": "Capturer un handshake Wi-Fi",
    "Forensic analysis": "Analyse forensique",
    "Create payloads": "Créer des payloads",
    "OSINT / recon a target": "OSINT / reconnaissance",
    "Stay anonymous": "Rester anonyme",
}
