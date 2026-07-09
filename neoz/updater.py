"""Automatic catalog updater for iw7x.

Fetches the full public tool catalogs (BlackArch — ~2800 tools) and merges any
new tools into ``catalog.json``, de-duplicated by title. Standard-library only
(``urllib``), fully wrapped in try/except, and writes atomically so a failed or
offline run can never corrupt the catalog or crash the app.

Usage
-----
    from neoz.updater import update_catalog
    added, total, message = update_catalog()

Or headless:  ``python3 iw7x.py --update``
"""

from __future__ import annotations

import html as _html
import json
import os
import re
import socket
import ssl
import tempfile
import time
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import curate
from .models import CATALOG_PATH

_UA = "iw7x-updater/1.5 (+https://github.com/iw7x)"
_TIMEOUT = 18            # per-request; a slow source can't stall the whole scan
_WORKERS = 16           # parallel HTTP fetches

# BlackArch group -> iw7x category id
_GROUP_MAP = {
    "webapp": "web_attack", "scanner": "information_gathering", "recon": "osint",
    "exploitation": "exploit_framework", "cracker": "wordlist_generator", "windows": "active_directory",
    "networking": "network_sniffing", "misc": "other_tools", "forensic": "forensics",
    "automation": "other_tools", "fuzzer": "fuzzing", "crypto": "cryptography",
    "wireless": "wireless_attack", "binary": "reverse_engineering", "social": "social_engineering",
    "backdoor": "payload_creation", "mobile": "mobile_security", "defensive": "blue_team",
    "sniffer": "network_sniffing", "reversing": "reverse_engineering", "malware": "malware_analysis",
    "proxy": "network_sniffing", "radio": "radio_sdr", "fingerprint": "osint",
    "code-audit": "reverse_engineering", "dos": "ddos_attack", "bluetooth": "wireless_attack",
    "voip": "voip", "spoof": "network_sniffing", "decompiler": "reverse_engineering",
    "tunnel": "post_exploitation", "disassembler": "reverse_engineering", "honeypot": "blue_team",
    "stego": "steganography", "debugger": "reverse_engineering", "ai": "ai_ml_security",
    "wordlist": "wordlist_generator", "database": "sql_injection", "hardware": "iot_hardware",
    "automobile": "automotive", "drone": "iot_hardware", "firmware": "iot_hardware",
    "keylogger": "payload_creation", "anti-forensic": "forensics", "packer": "reverse_engineering",
    "nfc": "iot_hardware", "ids": "blue_team", "threat-model": "forensics",
    "web3": "blockchain_web3", "smartcontract": "blockchain_web3",
    "api": "api_security", "privesc": "privilege_escalation",
    "threatintel": "threat_intel", "physical": "physical_security",
    "devsecops": "devsecops",
    # New dedicated categories (2026-07-06)
    "ctf": "ctf_tools", "gamehacking": "game_hacking", "honeypot": "honeypots",
    "supplychain": "supply_chain", "threathunt": "threat_hunting",
    "sandbox": "sandbox_analysis", "exfil": "data_exfiltration", "ics": "ics_scada",
    "cloud": "cloud_security", "container": "container_k8s",
    "cli": "cli_utilities", "selfhosted": "self_hosted", "sysadmin": "sysadmin_devops",
}

_GROUP_TAG = {
    "webapp": "web", "scanner": "scanner", "recon": "recon", "exploitation": "exploit",
    "cracker": "bruteforce", "windows": "active-directory", "networking": "network",
    "forensic": "forensics", "fuzzer": "reversing", "crypto": "reversing", "wireless": "wireless",
    "binary": "reversing", "social": "social-engineering", "backdoor": "payload", "mobile": "mobile",
    "defensive": "blue_team", "sniffer": "network", "reversing": "reversing", "malware": "forensics",
    "proxy": "network", "radio": "wireless", "fingerprint": "recon", "code-audit": "reversing",
    "dos": "ddos", "bluetooth": "wireless", "voip": "network", "spoof": "network",
    "decompiler": "reversing", "tunnel": "network", "disassembler": "reversing", "stego": "steganography",
    "database": "web", "hardware": "reversing", "wordlist": "bruteforce", "keylogger": "payload",
    "ctf": "reversing", "gamehacking": "reversing", "honeypot": "blue_team",
    "supplychain": "scanner", "threathunt": "forensics", "sandbox": "forensics",
    "exfil": "network", "ics": "scanner",
}

_DEFAULT_CATEGORY = "other_tools"
_BLACKARCH_URL = "https://blackarch.org/tools.html"
_KALI_URL = "https://www.kali.org/tools/all-tools/"
# (raw markdown url, fallback group when the section heading is unclear)
_AWESOME_URLS = [
    ("https://raw.githubusercontent.com/enaqx/awesome-pentest/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/apsdehal/awesome-ctf/master/README.md", "ctf"),
    ("https://raw.githubusercontent.com/jivoi/awesome-osint/master/README.md", "recon"),
    ("https://raw.githubusercontent.com/rshipp/awesome-malware-analysis/master/README.md", "malware"),
    ("https://raw.githubusercontent.com/meirwah/awesome-incident-response/master/README.md", "forensic"),
    ("https://raw.githubusercontent.com/paralax/awesome-honeypots/master/README.md", "honeypot"),
    ("https://raw.githubusercontent.com/vavkamil/awesome-bugbounty-tools/main/README.md", "webapp"),
    ("https://raw.githubusercontent.com/qazbnm456/awesome-web-security/master/README.md", "webapp"),
    ("https://raw.githubusercontent.com/caesar0301/awesome-pcaptools/master/README.md", "networking"),
    ("https://raw.githubusercontent.com/cugu/awesome-forensics/main/README.md", "forensic"),
    ("https://raw.githubusercontent.com/decalage2/awesome-security-hardening/master/README.md", "defensive"),
    ("https://raw.githubusercontent.com/sbilly/awesome-security/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/fabacab/awesome-cybersecurity-blueteam/master/README.md", "defensive"),
    ("https://raw.githubusercontent.com/ksluckow/awesome-symbolic-execution/master/README.md", "reversing"),
    ("https://raw.githubusercontent.com/jaredthecoder/awesome-vehicle-security/master/README.md", "automobile"),
    ("https://raw.githubusercontent.com/edoardottt/awesome-hacker-search-engines/main/README.md", "recon"),
    ("https://raw.githubusercontent.com/InQuest/awesome-yara/master/README.md", "malware"),
    ("https://raw.githubusercontent.com/v2-dev/awesome-social-engineering/master/README.md", "social"),
    ("https://raw.githubusercontent.com/0x4D31/awesome-threat-detection/master/README.md", "defensive"),
    ("https://raw.githubusercontent.com/wtsxDev/Penetration-Testing/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/RedHuntLabs/Awesome-Asset-Discovery/master/README.md", "recon"),
    ("https://raw.githubusercontent.com/snoopysecurity/awesome-burp-extensions/master/README.md", "webapp"),
    ("https://raw.githubusercontent.com/PaulSec/awesome-windows-domain-hardening/master/README.md", "windows"),
    ("https://raw.githubusercontent.com/coreb1t/awesome-pentest-cheat-sheets/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/Zeyad-Azima/Offensive-Resources/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/carpedm20/awesome-hacking/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/djadmin/awesome-bug-bounty/master/README.md", "webapp"),
    ("https://raw.githubusercontent.com/Muhammd/Awesome-Pentest/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/saeidshirazi/Awesome-Smart-Contract-Security/main/README.md", "web3"),
    ("https://raw.githubusercontent.com/PreOS-Security/awesome-firmware-security/master/README.md", "firmware"),
    # ── Extended coverage (probed for clean, on-topic yield) ────────────────────
    ("https://raw.githubusercontent.com/cipher387/osint_stuff_tool_collection/main/README.md", "recon"),
    ("https://raw.githubusercontent.com/pluja/awesome-privacy/main/README.md", "misc"),
    ("https://raw.githubusercontent.com/m0nad/awesome-privilege-escalation/master/README.md", "privesc"),
    ("https://raw.githubusercontent.com/joe-shenouda/awesome-cyber-skills/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/4ndersonLin/awesome-cloud-security/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/remiflavien1/awesome-anti-forensic/master/README.md", "forensic"),
    ("https://raw.githubusercontent.com/tcostam/awesome-command-control/master/README.md", "backdoor"),
    ("https://raw.githubusercontent.com/tylerha97/awesome-reversing/master/README.md", "reversing"),
    ("https://raw.githubusercontent.com/infoslack/awesome-web-hacking/master/README.md", "webapp"),
    ("https://raw.githubusercontent.com/engn33r/awesome-bluetooth-security/master/README.md", "bluetooth"),
    ("https://raw.githubusercontent.com/Ph055a/OSINT-Collection/master/README.md", "recon"),
    ("https://raw.githubusercontent.com/magnologan/awesome-k8s-security/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/vaib25vicky/awesome-mobile-security/master/README.md", "mobile"),
    ("https://raw.githubusercontent.com/nebgnahz/awesome-iot-hacks/master/README.md", "hardware"),
    ("https://raw.githubusercontent.com/sobolevn/awesome-cryptography/master/README.md", "crypto"),
    ("https://raw.githubusercontent.com/arainho/awesome-api-security/master/README.md", "api"),
    ("https://raw.githubusercontent.com/guardrailsio/awesome-python-security/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/trimstray/the-book-of-secret-knowledge/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/Astrosp/Awesome-OSINT-For-Everything/main/README.md", "recon"),
    ("https://raw.githubusercontent.com/toniblyx/my-arsenal-of-aws-security-tools/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/fabionoth/awesome-cyber-security/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/meitar/awesome-lockpicking/master/README.md", "physical"),
    ("https://raw.githubusercontent.com/sundowndev/hacker-roadmap/master/README.md", "misc"),
    # ── Batch 3 (2026-07-06): wider tool coverage + new categories ──────────────
    ("https://raw.githubusercontent.com/We5ter/Scanners-Box/master/README.md", "scanner"),
    ("https://raw.githubusercontent.com/hslatman/awesome-industrial-control-system-security/master/README.md", "ics"),
    ("https://raw.githubusercontent.com/Escapingbug/awesome-browser-exploit/master/README.md", "exploitation"),
    ("https://raw.githubusercontent.com/ashishb/android-security-awesome/master/README.md", "mobile"),
    ("https://raw.githubusercontent.com/wtsxDev/reverse-engineering/master/README.md", "reversing"),
    ("https://raw.githubusercontent.com/paragonie/awesome-appsec/master/README.md", "webapp"),
    ("https://raw.githubusercontent.com/dsasmblr/game-hacking/master/README.md", "gamehacking"),
    ("https://raw.githubusercontent.com/zardus/ctf-tools/master/README.md", "ctf"),
    ("https://raw.githubusercontent.com/CyberSecurityUP/Awesome-Red-Team-Operations/main/README.md", "misc"),
    ("https://raw.githubusercontent.com/hahwul/WebHackersWeapons/main/README.md", "webapp"),
    ("https://raw.githubusercontent.com/guardrailsio/awesome-golang-security/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/pe3zx/my-infosec-awesome/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/Hack-with-Github/Awesome-Hacking/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/vitalysim/Awesome-Hacking-Resources/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/rmusser01/Infosec_Reference/master/Draft/Sub_Sections/Web.md", "webapp"),
    ("https://raw.githubusercontent.com/re-cinq/awesome-cloud-native-security/main/README.md", "misc"),
    ("https://raw.githubusercontent.com/decalage2/awesome-security-hardening/master/README.md", "defensive"),
    ("https://raw.githubusercontent.com/EnableSecurity/awesome-rtc-hacking/master/README.md", "voip"),
    ("https://raw.githubusercontent.com/mytechnotalent/Reverse-Engineering/main/README.md", "reversing"),
    ("https://raw.githubusercontent.com/tanprathan/OWASP-Testing-Checklist/master/README.md", "webapp"),
    # ── Batch 4 (2026-07-06): vulnerable labs + serverless security ─────────────
    ("https://raw.githubusercontent.com/kaiiyer/awesome-vulnerable/master/README.md", "misc"),
    ("https://raw.githubusercontent.com/puresec/awesome-serverless-security/master/README.md", "misc"),
    # ── Batch 5 (2026-07-06): broader IT tooling in dedicated categories ────────
    ("https://raw.githubusercontent.com/agarrharr/awesome-cli-apps/master/readme.md", "cli"),
    ("https://raw.githubusercontent.com/alebcay/awesome-shell/master/README.md", "cli"),
    ("https://raw.githubusercontent.com/awesome-selfhosted/awesome-selfhosted/master/README.md", "selfhosted"),
]

# Map an "awesome list" section heading -> a group keyword (fed to _GROUP_MAP).
def _section_to_group(section: str) -> str:
    s = section.lower()
    for kw, group in (
        ("android", "mobile"), ("ios", "mobile"), ("mobile", "mobile"),
        ("wireless", "wireless"), ("wifi", "wireless"), ("bluetooth", "bluetooth"),
        ("web", "webapp"), ("sql", "webapp"), ("xss", "webapp"),
        ("network", "networking"), ("sniff", "sniffer"), ("scanner", "scanner"),
        ("recon", "recon"), ("osint", "recon"), ("intelligence", "recon"),
        ("exploit", "exploitation"), ("cve", "exploitation"),
        ("reverse", "reversing"), ("disassembl", "disassembler"), ("decompil", "decompiler"),
        ("forensic", "forensic"), ("dfir", "forensic"),
        ("password", "cracker"), ("cracker", "cracker"), ("hash", "cracker"), ("brute", "cracker"),
        ("social", "social"), ("phish", "social"),
        ("malware", "malware"), ("steg", "stego"),
        ("contract", "web3"), ("solidity", "web3"), ("blockchain", "web3"),
        ("web3", "web3"), ("ethereum", "web3"), ("crypto", "crypto"),
        ("denial", "dos"), ("ddos", "dos"), ("dos ", "dos"),
        ("kubernetes", "container"), ("container", "container"), ("docker", "container"),
        ("cloud", "cloud"), ("aws", "cloud"), ("azure", "cloud"), ("gcp", "cloud"), ("serverless", "cloud"),
        ("hardware", "hardware"), ("firmware", "firmware"),
        ("radio", "radio"), ("sdr", "radio"), ("smartcard", "nfc"),
        ("c2", "backdoor"), ("post", "backdoor"), ("payload", "backdoor"),
        ("api ", "api"), ("graphql", "api"), ("rest api", "api"), ("swagger", "api"),
        ("privilege", "privesc"), ("privesc", "privesc"), ("escalation", "privesc"),
        ("threat intel", "threatintel"), ("threat-intel", "threatintel"), ("misp", "threatintel"),
        ("indicator", "threatintel"), ("threat hunt", "threatintel"),
        ("rfid", "physical"), ("nfc", "physical"), ("physical", "physical"), ("lockpick", "physical"),
        ("sast", "devsecops"), ("dast", "devsecops"), ("devsecops", "devsecops"),
        ("capture the flag", "ctf"), ("ctf", "ctf"), ("wargame", "ctf"),
        ("game hack", "gamehacking"), ("game-hack", "gamehacking"), ("game security", "gamehacking"),
        ("game cheat", "gamehacking"), ("cheat engine", "gamehacking"),
        ("honeypot", "honeypot"), ("honeynet", "honeypot"), ("deception", "honeypot"),
        ("supply chain", "supplychain"), ("sbom", "supplychain"), ("dependency confusion", "supplychain"),
        ("threat hunt", "threathunt"), ("sigma rule", "threathunt"),
        ("sandbox", "sandbox"), ("detonat", "sandbox"), ("cuckoo", "sandbox"),
        ("exfiltrat", "exfil"), ("dns tunnel", "exfil"), ("covert channel", "exfil"),
        ("industrial control", "ics"), ("scada", "ics"), ("ics ", "ics"), ("ot security", "ics"),
    ):
        if kw in s:
            return group
    return "misc"

# Obvious non-tool system/desktop packages to skip from the Kali list.
_KALI_DENY = {
    "all-tools", "7zip", "apache2", "bind9", "bluez", "chromium", "glibc",
    "util-linux", "samba", "qemu", "lvm2", "llvm-defaults", "android-sdk-meta",
    "calico", "atftp", "bind", "systemd", "network-manager", "firefox-esr",
    "openssh", "openssl", "python3-defaults", "ruby-defaults", "golang-defaults",
    "nodejs", "postgresql", "mariadb", "gnupg", "curl", "wget", "git", "vim",
}


def _http_get(url: str) -> str | None:
    """Fetch a URL as text; return None on any failure (never raises)."""
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=_TIMEOUT, context=ctx) as resp:
            raw = resp.read()
        return raw.decode("utf-8", errors="replace")
    except Exception:
        # Retry once without certificate verification (some environments).
        try:
            ctx = ssl._create_unverified_context()
            req = urllib.request.Request(url, headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=_TIMEOUT, context=ctx) as resp:
                raw = resp.read()
            return raw.decode("utf-8", errors="replace")
        except Exception:
            return None


def _http_get_many(urls: list[str]) -> dict:
    """Fetch many URLs concurrently. Returns {url: text|None}. Never raises."""
    if not urls:
        return {}
    with ThreadPoolExecutor(max_workers=min(_WORKERS, len(urls))) as pool:
        texts = list(pool.map(_http_get, urls))
    return dict(zip(urls, texts))


def _strip(text: str) -> str:
    return _html.unescape(re.sub(r"<.*?>", " ", text)).strip()


def fetch_blackarch() -> list[dict]:
    """Return a list of {name, description, url, group} from BlackArch, or []."""
    page = _http_get(_BLACKARCH_URL)
    if not page:
        return []
    tools: list[dict] = []
    for row in re.findall(r"<tr>(.*?)</tr>", page, re.S):
        cells = re.findall(r"<td.*?>(.*?)</td>", row, re.S)
        if len(cells) < 4:
            continue
        name = _strip(cells[0])
        desc = _strip(cells[2])
        group = _strip(cells[3]).replace("blackarch-", "")
        if not name or not desc:
            continue
        href = re.search(r'href=[\'"]([^\'"]+)[\'"]', cells[4] if len(cells) > 4 else "")
        url = href.group(1).strip() if href else ""
        tools.append({"name": name, "description": desc[:400], "url": url,
                      "group": group, "source": "blackarch"})
    return tools


_MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
_TABLE_SEP = re.compile(r"^\|?[\s:|-]+\|?$")


def _md_plain(text: str) -> str:
    """Strip markdown links/formatting to plain text."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*`_>#]", "", text)
    return _strip(text)


def _dedup_key(name: str) -> str:
    """Alphanumeric-only lowercase key so 'cloud_enum', 'cloud-enum' and
    'CloudEnum' all collapse to one — guarantees no near-duplicate tools."""
    return re.sub(r"[^a-z0-9]+", "", (name or "").lower())


def _awesome_line(line: str, line_re) -> tuple[str, str, str] | None:
    """Extract (name, url, description) from a bullet OR a table row."""
    m = line_re.match(line)
    if m:
        return _strip(m.group(1)), m.group(2).strip(), _md_plain(m.group(3))
    s = line.strip()
    if s.startswith("|") and "](http" in s and not _TABLE_SEP.match(s):
        cells = [c.strip() for c in s.strip("|").split("|")]
        name = url = None
        link_idx = -1
        for i, cell in enumerate(cells):
            lm = _MD_LINK.search(cell)
            if lm:
                name, url, link_idx = _strip(lm.group(1)), lm.group(2), i
                break
        if not name:
            return None
        descs = [
            _md_plain(cell) for j, cell in enumerate(cells)
            if j != link_idx and "![" not in cell
        ]
        descs = [d for d in descs if len(d) > 8 and not d.lower().startswith("http")]
        return (name, url, max(descs, key=len)) if descs else None
    return None


def fetch_awesome() -> list[dict]:
    """Parse 'awesome' markdown lists (bullets or tables), or []."""
    line_re = re.compile(
        r"^[ \t]*[-*] \[([^\]]+)\]\((https?://[^)\s]+)\)\s*[-–—:]\s*(.+?)\s*$")
    head_re = re.compile(r"^#{2,4}\s+(.+?)\s*$")
    tools: list[dict] = []
    seen: set[str] = set()
    pages = _http_get_many([u for u, _ in _AWESOME_URLS])
    for src_url, default_group in _AWESOME_URLS:
        text = pages.get(src_url)
        if not text:
            continue
        section = ""
        for line in text.splitlines():
            h = head_re.match(line)
            if h:
                section = h.group(1)
                continue
            entry = _awesome_line(line, line_re)
            if not entry:
                continue
            name, url, desc = entry
            key = _dedup_key(name)
            if not name or not desc or key in seen:
                continue
            seen.add(key)
            group = _section_to_group(section)
            if group == "misc":
                group = default_group
            tools.append({
                "name": name, "description": desc[:400], "url": url,
                "group": group, "source": "awesome",
            })
    return tools


def fetch_kali() -> list[dict]:
    """Return a list of {name, description, url, group='kali'} from Kali, or []."""
    page = _http_get(_KALI_URL)
    if not page:
        return []
    tools: list[dict] = []
    seen: set[str] = set()
    pattern = (r'<a href=https://www\.kali\.org/tools/([a-z0-9._+-]+)/>'
               r'<i class=ti-archive title="Source Project"></i>\s*([^<]+)</a>')
    for slug, name in re.findall(pattern, page):
        slug = slug.strip().lower()
        name = name.strip()
        if not slug or slug in _KALI_DENY or slug in seen:
            continue
        seen.add(slug)
        tools.append({
            "name": name,
            "description": f"Kali Linux security tool (apt package '{slug}').",
            "url": f"https://www.kali.org/tools/{slug}/",
            "group": "kali", "source": "kali",
        })
    return tools


_CODE_HOST = re.compile(r"(github\.com|gitlab\.com|bitbucket\.org|codeberg\.org)")

# Repos that list tools as markdown headings ("### [name](repo)") with the
# description on the following line — dedicated parser, code-hosts only.
_HEADING_SOURCES = [
    ("https://raw.githubusercontent.com/A-poc/RedTeam-Tools/main/README.md", "misc"),
    ("https://raw.githubusercontent.com/A-poc/BlueTeam-Tools/main/README.md", "defensive"),
]


def fetch_heading_lists() -> list[dict]:
    """Parse heading-based tool repos (name = heading link, desc = next line)."""
    tools: list[dict] = []
    seen: set[str] = set()
    pages = _http_get_many([u for u, _ in _HEADING_SOURCES])
    for url, group in _HEADING_SOURCES:
        text = pages.get(url)
        if not text:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if not re.match(r"^#{2,4}\s", line):
                continue
            links = re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", line)
            if not links:
                continue
            name, tool_url = links[-1]          # last link on the heading = the tool
            name = _strip(name)
            key = _dedup_key(name)
            if not name or key in seen or not _CODE_HOST.search(tool_url):
                continue
            desc = ""
            for j in range(i + 1, min(i + 8, len(lines))):
                s = lines[j].strip()
                if re.match(r"^#{1,6}\s", s):
                    break
                if not s or s[0] in "*<>|[" or s.startswith(("```", "![", "- ")):
                    continue
                d = _md_plain(s)
                if len(d) > 10:
                    desc = d
                    break
            if not desc:
                continue
            seen.add(key)
            tools.append({"name": name, "description": desc[:400], "url": tool_url,
                          "group": group, "source": "awesome"})
    return tools


# Capture tool repos that are linked from awesome lists WITHOUT an inline
# description (the strict parser needs "* [name](url) - desc"). We keep only
# code-host repo links and de-noise the name so real tools land, not prose.
_REPO_URL = re.compile(
    r"^https?://(?:www\.)?(?:github|gitlab|bitbucket|codeberg)\.(?:com|org)/([^/\s]+)/([^/\s#?)]+)",
    re.I)
_NAME_NOISE = re.compile(
    r"(awesome|cheat.?sheet|write.?up|slides?|\btalks?\b|blog|roadmap|\bbook\b|wiki|"
    r"methodology|mindmap|tutorial|course|reference|resources?|collection|understanding|"
    r"introduction|\bguide\b|paper|article|walkthrough|checklist|playbook)", re.I)
_URL_NOISE = re.compile(r"(/blob/|/tree/|/wiki|/releases|/issues|/actions|/sponsors|awesome-)", re.I)
_STOP_NAMES = {
    "source", "open source", "open-source", "tools", "scripts", "tool", "script",
    "docs", "home", "link", "repo", "code", "demo", "example", "misc", "other",
    "project", "projects", "index", "readme", "main", "master", "here", "github",
    "list", "lists", "framework", "library", "utils", "util", "cli", "gui",
}


def _repo_tool_name(text: str, repo: str) -> str | None:
    """Pick a clean tool name: the link text if it's a short token, else the repo
    slug. Returns None when the result is still prose/noise."""
    t = _strip(re.sub(r"[`*_]", "", text or "")).strip()
    words = t.split()
    if (1 <= len(words) <= 4 and 2 <= len(t) <= 42
            and re.match(r"^[A-Za-z0-9]", t) and ":" not in t and "/" not in t
            and not t.endswith((".", ",", ";")) and not _NAME_NOISE.search(t)):
        name = t
    else:
        slug = re.sub(r"\.git$", "", repo).replace("_", " ").replace("-", " ").strip()
        if len(slug) < 2 or _NAME_NOISE.search(slug) or len(slug.split()) > 5:
            return None
        name = slug
    low = name.lower()
    if low in _STOP_NAMES or "open source" in low or "open-source" in low:
        return None
    if len(name.split()) >= 3 and re.search(r"\b(tools?|scripts?|lists?|resources?)\b", low):
        return None
    return name


def fetch_repo_links() -> list[dict]:
    """Looser awesome parser: harvest code-host tool repos even when the bullet has
    no description. Filtered to real repos and de-noised. Everything wrapped."""
    tools: list[dict] = []
    seen: set[str] = set()
    head_re = re.compile(r"^#{2,4}\s+(.+?)\s*$")
    pages = _http_get_many([u for u, _ in _AWESOME_URLS])
    for src_url, default_group in _AWESOME_URLS:
        text = pages.get(src_url)
        if not text:
            continue
        section = ""
        for line in text.splitlines():
            h = head_re.match(line)
            if h:
                section = h.group(1)
                continue
            s = line.lstrip()
            if not (s[:2] in ("- ", "* ", "+ ") or s.startswith("|")):
                continue
            for m in _MD_LINK.finditer(line):
                name, url = m.group(1), m.group(2)
                mm = _REPO_URL.match(url)
                if not mm or _URL_NOISE.search(url):
                    continue
                owner, repo = mm.group(1), mm.group(2)
                if repo.lower().startswith("awesome-"):
                    continue
                nm = _repo_tool_name(name, repo)
                if not nm:
                    continue
                key = _dedup_key(nm)
                if key in seen:
                    continue
                seen.add(key)
                group = _section_to_group(section)
                if group == "misc":
                    group = default_group
                desc = _strip(section) or "Open-source security tool."
                tools.append({
                    "name": nm, "description": desc[:200],
                    "url": mm.group(0), "group": group, "source": "awesome",
                })
    return tools


# ── GitHub topic harvest — the real "every security tool on GitHub" index ────────
#
# GitHub indexes tools by topic. Sorting each security topic by stars and keeping
# only repos above a star floor gives us the tools people actually use, while
# skipping the infinite tail of dead/empty repos that would only add noise. Names
# are de-noised (_repo_tool_name) and descriptions cleaned (curate) like any other
# source, so the catalog stays readable no matter how much we pull in.
_GH_SEARCH = "https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=100&page={page}"

# GitHub topic -> group keyword (routed through _GROUP_MAP to a category id).
_GH_TOPICS: dict[str, str] = {
    "hacking-tool": "misc", "hacking-tools": "misc", "pentesting": "misc",
    "penetration-testing": "misc", "pentest-tool": "misc", "security-tools": "misc",
    "cybersecurity": "misc", "ethical-hacking": "misc", "red-team": "backdoor",
    "redteam": "backdoor", "offensive-security": "exploitation", "blue-team": "defensive",
    "osint": "recon", "reconnaissance": "recon", "information-gathering": "recon",
    "bug-bounty": "webapp", "bugbounty": "webapp", "web-security": "webapp",
    "web-application-security": "webapp", "sql-injection": "database", "xss": "webapp",
    "vulnerability-scanner": "scanner", "vulnerability-scanners": "scanner",
    "vulnerability-detection": "scanner", "network-security": "networking",
    "reverse-engineering": "reversing", "malware-analysis": "malware", "malware": "malware",
    "forensics": "forensic", "dfir": "forensic", "incident-response": "forensic",
    "exploit": "exploitation", "exploitation": "exploitation", "exploit-development": "exploitation",
    "privilege-escalation": "privesc", "post-exploitation": "backdoor", "c2": "backdoor",
    "command-and-control": "backdoor", "wifi": "wireless", "wireless-security": "wireless",
    "wifi-security": "wireless", "bluetooth": "bluetooth", "password-cracking": "cracker",
    "wordlist": "wordlist", "brute-force": "cracker", "active-directory": "windows",
    "cloud-security": "cloud", "aws-security": "cloud", "kubernetes-security": "container",
    "container-security": "container", "mobile-security": "mobile", "android-security": "mobile",
    "ios-security": "mobile", "ctf": "ctf", "ctf-tools": "ctf", "steganography": "stego",
    "phishing": "social", "social-engineering": "social", "threat-intelligence": "threatintel",
    "threat-hunting": "threathunt", "api-security": "api", "fuzzing": "fuzzer",
    "sast": "devsecops", "dast": "devsecops", "devsecops": "devsecops", "iot-security": "hardware",
    "firmware-security": "firmware", "ics": "ics", "scada": "ics", "smart-contract-security": "web3",
    "web3-security": "web3", "blockchain-security": "web3", "honeypot": "honeypot",
    "cryptography": "crypto", "sdr": "radio", "game-hacking": "gamehacking",
    "supply-chain-security": "supplychain", "sandbox": "sandbox", "data-exfiltration": "exfil",
}


def _gh_token() -> str:
    """A GitHub token from the environment, if the user set one. Lifts the search
    rate limit from ~10 to ~30 calls/min so the crawl can go far deeper. A plain
    read-only token (no scopes) is enough — public search needs no permissions."""
    for var in ("IW7X_GITHUB_TOKEN", "GITHUB_TOKEN", "GH_TOKEN"):
        val = os.environ.get(var, "").strip()
        if val:
            return val
    return ""


def _gh_get(url: str, token: str = "") -> str | None:
    """GET a GitHub API URL as text (with auth when a token is present). Never
    raises — returns None on any failure."""
    headers = {"User-Agent": _UA, "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=_TIMEOUT, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def fetch_github_topics(topics: dict | None = None, min_stars: int | None = None,
                        pages: int | None = None, start_page: int = 1,
                        pause: float | None = None) -> list[dict]:
    """Harvest real security tools straight from GitHub's topic index.

    For each topic, pull the most-starred repos (>= ``min_stars``) and turn them
    into tool records. With a token (see ``_gh_token``) the crawl goes far deeper
    and faster (lower star floor, more pages); without one it stays gentle so the
    unauthenticated ~10 calls/min limit is respected. Fully wrapped — a throttled
    or offline run just returns fewer tools, never raises."""
    token = _gh_token()
    if min_stars is None:
        min_stars = 10 if token else 40
    if pages is None:
        pages = 4 if token else 1
    if pause is None:
        pause = 2.2 if token else 6.5
    topics = topics or _GH_TOPICS
    tools: list[dict] = []
    seen: set[str] = set()
    for topic, group in topics.items():
        for page in range(start_page, start_page + max(1, pages)):
            url = _GH_SEARCH.format(q=f"topic:{topic}+stars:>={min_stars}", page=page)
            text = _gh_get(url, token)
            if not text:
                break
            try:
                items = json.loads(text).get("items")
            except Exception:
                items = None
            if not items:                      # rate-limited, empty, or error
                time.sleep(pause)
                break
            for it in items:
                if it.get("fork"):
                    continue
                repo = (it.get("name") or "").strip()
                full = it.get("full_name") or repo
                nm = _repo_tool_name(repo, repo)
                if not nm:
                    continue
                key = _dedup_key(nm)
                if not key or key in seen:
                    continue
                seen.add(key)
                tools.append({
                    "name": nm,
                    "description": (it.get("description") or "")[:400],
                    "url": it.get("html_url") or f"https://github.com/{full}",
                    "group": group,
                    "source": "awesome",       # -> git clone install, reference-safe
                })
            if len(items) < 100:               # no more pages for this topic
                break
            time.sleep(pause)
        time.sleep(pause)
    return tools


# All tool sources, tried in order. Each returns a list of normalized records
# or [] on failure. Add more callables here to widen coverage.
SOURCES = [fetch_blackarch, fetch_kali, fetch_awesome, fetch_heading_lists,
           fetch_repo_links, fetch_github_topics]


def _entry_from_record(rec: dict) -> tuple[str, dict]:
    """Build a (category_id, tool_dict) pair from a normalized source record."""
    name, url, group = rec["name"], rec.get("url", ""), rec.get("group", "")
    src = rec.get("source", "")
    cid = _GROUP_MAP.get(group, _DEFAULT_CATEGORY)
    installable = True
    if src == "kali":
        install = [f"sudo apt install -y {name}"]
    elif _CODE_HOST.search(url):
        install = [f"git clone {url}"]
    elif src == "blackarch":
        install = [f"sudo pacman -S {name}"]     # BlackArch-native
    else:
        install = []                              # awesome/non-repo → reference only
        installable = False
    tags = [_GROUP_TAG[group]] if group in _GROUP_TAG else []
    tool = {
        "title": name,
        "description": curate.clean_description(rec["description"], name, cid),
        "install": install,
        "run": [],
        "uninstall": [],
        "url": url,
        "tags": tags,
        "os": ["linux"],
        "archived": False,
        "archived_reason": "",
        "requires_root": False,
        "installable": installable,
        "runnable": False,          # imported entries carry no verified run cmd
        "has_custom_options": False,
        "source": src or "remote",
    }
    return cid, tool


def _collect_records() -> tuple[list[dict], int]:
    """Fetch every source concurrently (fast). Returns (records, sources_reached)."""
    def _safe(fetch):
        try:
            return fetch()
        except Exception:
            return []

    records: list[dict] = []
    reached = 0
    with ThreadPoolExecutor(max_workers=len(SOURCES)) as pool:
        for got in pool.map(_safe, SOURCES):
            if got:
                reached += 1
                records.extend(got)
    return records, reached


def online(host: str = "blackarch.org", port: int = 443, timeout: float = 4.0) -> bool:
    """Quick reachability probe so a launch-time scan can skip fast when offline."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def update_catalog(catalog_path: Path | None = None, progress=None) -> tuple[int, int, str]:
    """
    Fetch every remote tool source and merge new tools into the catalog.

    Returns ``(added, total, message)``. Never raises; on any failure returns
    ``(0, <current_total>, <reason>)`` and leaves the catalog untouched.

    ``progress``: optional callback ``progress(running_total: int)`` invoked as
    each tool is integrated, so callers can show the count climbing live.
    """
    path = Path(catalog_path) if catalog_path else CATALOG_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return 0, 0, f"cannot read catalog: {exc}"

    categories = data.get("categories", [])
    by_id = {c["id"]: c for c in categories}
    existing = {
        _dedup_key(tl["title"])
        for c in categories for tl in c.get("tools", [])
    }
    current_total = sum(len(c.get("tools", [])) for c in categories)

    records, reached = _collect_records()
    if reached == 0:
        return 0, current_total, "update sources unreachable (offline?)"

    added = 0
    for rec in records:
        # Clean the name *before* the dedup key so a scraped variant of a tool
        # already in the catalog collapses to the same key (no near-duplicates).
        rec["name"] = curate.clean_title(rec.get("name", ""))
        key = _dedup_key(rec["name"])
        if not key or key in existing:
            continue
        cid, tool = _entry_from_record(rec)
        cat = by_id.get(cid) or by_id.get(_DEFAULT_CATEGORY)
        if cat is None:
            continue
        cat.setdefault("tools", []).append(tool)
        existing.add(key)
        added += 1
        if progress and added % 3 == 0:
            try:
                progress(current_total + added)
                time.sleep(0.002)   # let the live counter be visible
            except Exception:
                progress = None     # never let a UI callback break the merge
    if progress and added:
        try:
            progress(current_total + added)
        except Exception:
            pass

    if added == 0:
        return 0, current_total, "catalog already up to date"

    total = sum(len(c.get("tools", [])) for c in categories)
    data.setdefault("meta", {})
    data["meta"]["tools"] = total
    data["meta"]["categories"] = len(categories)

    # Atomic write: temp file in the same dir, then replace.
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        os.replace(tmp, str(path))
    except Exception as exc:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        return 0, current_total, f"write failed: {exc}"

    return added, total, f"added {added} tools ({total} total)"


def watch(interval_minutes: float = 60.0, log=None) -> None:
    """
    Continuously scan every source and auto-add new tools. Runs until stopped
    (Ctrl-C). Each cycle is fully error-wrapped so the watcher never dies.
    """
    if log is None:
        def log(msg):
            print(msg, flush=True)
    interval = max(60.0, float(interval_minutes) * 60.0)
    log(f"[iw7x] Live auto-scan started — checking every {interval/60:.0f} min. Ctrl-C to stop.")
    while True:
        try:
            added, total, msg = update_catalog()
            stamp = time.strftime("%H:%M:%S")
            if added:
                log(f"[iw7x {stamp}] +{added} new tools — {total} total.")
            else:
                log(f"[iw7x {stamp}] no new tools ({msg}).")
        except KeyboardInterrupt:
            log("\n[iw7x] Auto-scan stopped.")
            return
        except Exception as exc:
            log(f"[iw7x] scan error (ignored): {exc}")
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            log("\n[iw7x] Auto-scan stopped.")
            return


# ── Background collector (non-blocking, never stops) ─────────────────────────────
_BG_THREAD: threading.Thread | None = None


def start_background_watch(interval_minutes: float = 20.0, on_added=None) -> None:
    """Spawn a daemon thread that keeps merging new tools from every source while
    the app runs — so the arsenal never stops growing during a session.

    Non-blocking and fully error-wrapped: a bad cycle (offline, rate-limit, parse
    error) can never crash or freeze the UI. Idempotent — only one collector runs.
    After a cycle that adds tools it clears the model caches so a running menu
    shows the new tools (and the climbing count) on its next render.

    ``on_added(added, total)`` is an optional callback fired after each productive
    cycle. The interval is clamped to a responsible minimum (sources refresh at
    most daily; scanning faster just gets you rate-limited, never more tools).
    """
    global _BG_THREAD
    if _BG_THREAD is not None and _BG_THREAD.is_alive():
        return
    interval = max(300.0, float(interval_minutes) * 60.0)

    def _loop() -> None:
        # Let the launch scan settle first, then keep collecting forever.
        time.sleep(interval)
        while True:
            try:
                if online():
                    added, total, _ = update_catalog()
                    if added:
                        try:
                            from .models import load_catalog, tag_index
                            load_catalog.cache_clear()
                            tag_index.cache_clear()
                        except Exception:
                            pass
                        if on_added:
                            try:
                                on_added(added, total)
                            except Exception:
                                pass
            except Exception:
                pass          # one bad cycle must never kill the collector
            time.sleep(interval)

    _BG_THREAD = threading.Thread(target=_loop, name="iw7x-bg-collector", daemon=True)
    _BG_THREAD.start()
