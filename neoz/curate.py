"""Shared tool-text cleanup so every entry — curated or auto-imported — reads
cleanly in the terminal table: one short title per tool, one honest per-tool
description.

Both the live updater (``updater.py``) and any one-off catalog pass use these
functions, so the two can never disagree. In particular ``clean_title`` is a
pure, deterministic, idempotent function of the raw name: the updater cleans a
scraped name *before* computing its dedup key, which means a name that was
already cleaned in the catalog collapses to the same key and is recognised as
existing instead of being re-added as a near-duplicate.
"""

from __future__ import annotations

import re

# Honest fallback description per category — used only when the scraped one is
# a markdown section header, a bare year, or just the tool name repeated.
CATEGORY_BLURB: dict[str, str] = {
    "anonymously_hiding": "Anonymity, privacy and traffic-hiding utility.",
    "information_gathering": "Reconnaissance and information-gathering tool.",
    "wordlist_generator": "Wordlist / password-list generation tool.",
    "wireless_attack": "Wi-Fi and wireless network attack tool.",
    "sql_injection": "SQL injection testing tool.",
    "phishing_attack": "Phishing and social-engineering toolkit.",
    "web_attack": "Web application attack and testing tool.",
    "post_exploitation": "Post-exploitation and lateral-movement tool.",
    "forensics": "Digital forensics and incident-response tool.",
    "payload_creation": "Payload generation and delivery tool.",
    "exploit_framework": "Exploitation framework / exploit toolkit.",
    "reverse_engineering": "Reverse-engineering and binary-analysis tool.",
    "ddos_attack": "Network stress-testing (DoS) tool.",
    "remote_admin_rat": "Remote administration (RAT) tool.",
    "xss_attack": "Cross-site scripting (XSS) testing tool.",
    "steganography": "Steganography and data-hiding tool.",
    "active_directory": "Active Directory attack and audit tool.",
    "cloud_security": "Cloud security assessment tool.",
    "mobile_security": "Mobile application security tool.",
    "other_tools": "Security utility or resource.",
    "network_sniffing": "Network sniffing and traffic-analysis tool.",
    "malware_analysis": "Malware analysis tool.",
    "ics_scada": "ICS / SCADA security tool.",
    "iot_hardware": "IoT and hardware security tool.",
    "blockchain_web3": "Blockchain / Web3 security tool.",
    "blue_team": "Blue-team / defensive security tool.",
    "container_k8s": "Container and Kubernetes security tool.",
    "radio_sdr": "Radio / SDR analysis tool.",
    "automotive": "Automotive / CAN-bus security tool.",
    "voip": "VoIP security testing tool.",
    "binary_exploitation": "Binary exploitation (pwn) tool.",
    "fuzzing": "Fuzzing tool.",
    "vuln_scanning": "Vulnerability scanning tool.",
    "satellite": "Satellite / space security tool.",
    "social_engineering": "Social-engineering toolkit.",
    "ai_ml_security": "AI / ML security tool.",
    "osint": "OSINT / open-source intelligence tool.",
    "cryptography": "Cryptography and encryption tool.",
    "api_security": "API security testing tool.",
    "privilege_escalation": "Privilege-escalation tool.",
    "threat_intel": "Threat-intelligence tool.",
    "physical_security": "Physical security and access tool.",
    "devsecops": "DevSecOps / secure-pipeline tool.",
    "honeypots": "Honeypot / deception tool.",
    "game_hacking": "Game hacking / memory-editing tool.",
    "ctf_tools": "CTF / challenge-solving tool.",
    "supply_chain": "Supply-chain security tool.",
    "threat_hunting": "Threat-hunting tool.",
    "sandbox_analysis": "Sandbox / dynamic-analysis tool.",
    "data_exfiltration": "Data-exfiltration / covert-channel tool.",
    "cli_utilities": "Command-line utility.",
    "self_hosted": "Self-hosted open-source application.",
    "sysadmin_devops": "System administration / DevOps tool.",
    "security_learning": "Learning resource, notes or cheat sheet.",
    "update_uninstall": "Maintenance action.",
}

_DEFAULT_BLURB = "Security tool."

# Whole-description tokens that are markdown section headers, not descriptions.
_HEADER_STOP = {
    "misc", "tools", "tool", "frameworks", "framework", "other lists", "collections",
    "collection", "open source", "opensource", "web", "free", "ssl/tls", "csrf", "xss",
    "web servers", "other", "others", "general", "resources", "resource", "links",
    "onion links", "guides", "guide", "articles", "article", "books", "book", "courses",
    "course", "talks", "videos", "video", "blogs", "blog", "cheatsheets", "cheat sheets",
    "cheatsheet", "cheat sheet", "lists", "list", "paid", "commercial", "online", "offline",
    "windows", "linux", "macos", "mac", "android", "ios", "hardware", "software",
    "payment", "payments", "reference", "references", "training", "labs", "lab", "wiki",
    "practice", "challenges", "writeups", "write-ups", "podcasts", "newsletters", "slides",
    "presentations", "papers", "research", "standards", "frameworks & standards",
    "open-source security tool.", "open source security tool.",
}

# Words that must not dangle at the end of a shortened label.
_STOP_EDGE = {
    "a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with", "from",
    "by", "at", "as", "is", "are", "how", "&",
}

_DEDUP = re.compile(r"[^a-z0-9]+")
_ALREADY_NUMBERED = re.compile(r".* \(\d+\)$")


def dedup_key(name: str) -> str:
    """Alphanumeric-only lowercase key (mirrors updater._dedup_key)."""
    return _DEDUP.sub("", (name or "").lower())


def _collapse(text: str) -> str:
    """First non-empty line, whitespace-collapsed and trimmed."""
    for line in (text or "").splitlines():
        line = " ".join(line.split())
        if line:
            return line
    return ""


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


def _looks_like_sentence(title: str) -> bool:
    return len(title) > 48 or len(title.split()) >= 8


def _trim_edges(words: list[str]) -> list[str]:
    while words and re.sub(r"[^a-z]", "", words[-1].lower()) in _STOP_EDGE:
        words.pop()
    return words


def _shorten(title: str) -> str:
    """Turn a whole-sentence title into a short, readable label (<=7 words)."""
    t = _collapse(title)
    for delim in (":", " - ", " – ", " — ", " | ", " (", ", "):
        if delim in t:
            head = t.split(delim, 1)[0].strip()
            if 2 <= len(head.split()) <= 8 and len(head) <= 46:
                t = head
                break
    words, out = t.split(), []
    for w in words:
        if len(out) >= 7 or (out and len(" ".join(out + [w])) > 46):
            break
        out.append(w)
    out = _trim_edges(out) or words[:1]
    t = " ".join(out)
    letters = [c for c in t if c.isalpha()]
    if letters and all(c.isupper() for c in letters):   # ALL CAPS -> Title Case
        t = t.title()
    return t.strip(" -–—:|,\"'") or _collapse(title)[:46]


def clean_title(name: str) -> str:
    """Normalise a tool name and shorten it when it is really a whole sentence.

    Pure and idempotent: cleaning an already-clean title returns it unchanged,
    so the updater's pre-dedup key stays stable across scans."""
    t = _collapse(name)
    if not t or _ALREADY_NUMBERED.match(t):
        return t
    if _looks_like_sentence(t):
        t = _shorten(t)
    return t


def is_junk_description(desc: str, title: str) -> bool:
    """True when the description carries no per-tool information (empty, a repeat
    of the title, a markdown section header, or a bare year/number)."""
    d = _collapse(desc)
    if not d:
        return True
    if dedup_key(d) == dedup_key(title):
        return True
    if d.lower().strip().rstrip(".") in _HEADER_STOP:
        return True
    if re.fullmatch(r"[\(\)\[\]0-9\-–— .]+", d):
        return True
    return False


def clean_description(desc: str, title: str, category_id: str) -> str:
    """Return a clean, single-line, per-tool description. Junk/empty scraped
    descriptions become an honest category-based sentence so the table row still
    tells the reader what the tool is for."""
    if is_junk_description(desc, title):
        return CATEGORY_BLURB.get(category_id, _DEFAULT_BLURB)
    return _cap(_collapse(desc))


# Ordered keyword -> category routing for the generic "other_tools" bucket, so
# imported misc tools land where the reader expects them. First match wins;
# specific patterns are listed before generic ones. Used both by the live
# updater and the one-off recategorisation pass, so both agree.
_ROUTES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(cheat[- ]?sheets?|notes?|study|roadmap|awesome|write[- ]?ups?|walkthroughs?|tutorials?|guides?|methodology|mindmaps?|courses?|training|e?books?|certification|oscp|ejpt|pnpt|resources?|reference|wiki|playbooks?|checklists?)\b", re.I), "security_learning"),
    (re.compile(r"\b(active[- ]?directory|kerberoast\w*|bloodhound|ntlm|impacket|netexec|crackmapexec|responder|adcs|certipy|password[- ]?spray\w*|silver[- ]?ticket|golden[- ]?ticket)\b", re.I), "active_directory"),
    (re.compile(r"\b(sqlmap|sql[- ]?injection|sqli)\b", re.I), "sql_injection"),
    (re.compile(r"\b(xss|cross[- ]?site[- ]?scripting)\b", re.I), "xss_attack"),
    (re.compile(r"\b(wi[- ]?fi|wpa2?|\bwps\b|deauth\w*|802\.11|wireless|bluetooth|zigbee|evil[- ]?twin|aircrack\w*|wifite)\b", re.I), "wireless_attack"),
    (re.compile(r"\b(burp\w*|\bwaf\b|xxe|ssrf|csrf|\blfi\b|\brfi\b|web[- ]?shell|webshell|owasp|gobuster|ffuf|dirb|dirsearch|web[- ]?app\w*)\b", re.I), "web_attack"),
    (re.compile(r"\b(android|\bios\b|\bapk\b|frida|objection|smali|\bdex\b|\bipa\b|jailbreak|mobsf)\b", re.I), "mobile_security"),
    (re.compile(r"\b(aws|azure|\bgcp\b|s3[- ]?bucket|\biam\b|lambda|serverless|cloudtrail|pacu|prowler|scoutsuite)\b", re.I), "cloud_security"),
    (re.compile(r"\b(docker|kubernetes|k8s|kubectl|helm|container)\b", re.I), "container_k8s"),
    (re.compile(r"\b(reverse[- ]?engineer\w*|ghidra|radare2?|\bida\b|disassembl\w*|decompil\w*|debugger|binary[- ]?analysis)\b", re.I), "reverse_engineering"),
    (re.compile(r"\b(malware|ransomware|trojan|botnet|yara|unpack\w*|stealer|implant|\bc2\b|command[- ]?and[- ]?control)\b", re.I), "malware_analysis"),
    (re.compile(r"\b(forensics?|dfir|volatility|autopsy|disk[- ]?imag\w*|carv\w*|incident[- ]?response|memory[- ]?forensics?)\b", re.I), "forensics"),
    (re.compile(r"\b(privesc|privilege[- ]?escalation|linpeas|winpeas|peass)\b", re.I), "privilege_escalation"),
    (re.compile(r"\b(payload\w*|msfvenom|obfuscat\w*|dropper|maldoc|reverse[- ]?shell|backdoor|shellcode)\b", re.I), "payload_creation"),
    (re.compile(r"\b(exploit\w*|cve-\d|\brce\b|metasploit|0day|vulnerabilit\w*)\b", re.I), "exploit_framework"),
    (re.compile(r"\b(password\w*|wordlists?|hashcat|john[- ]?the[- ]?ripper|brute[- ]?forc\w*|credential\w*|hash[- ]?crack\w*)\b", re.I), "wordlist_generator"),
    (re.compile(r"\b(phish\w*|smish\w*|social[- ]?engineer\w*|evilginx|gophish)\b", re.I), "phishing_attack"),
    (re.compile(r"\b(steg\w*|steganograph\w*)\b", re.I), "steganography"),
    (re.compile(r"\b(sniff\w*|packet[- ]?captur\w*|\bmitm\b|arp[- ]?spoof\w*|wireshark|tcpdump)\b", re.I), "network_sniffing"),
    (re.compile(r"\b(subdomain\w*|recon\w*|osint|whois|dns[- ]?enum\w*|fingerprint\w*|nmap|masscan|port[- ]?scan\w*|footprint\w*)\b", re.I), "information_gathering"),
    (re.compile(r"\b(ddos|dos[- ]?attack|stress[- ]?test\w*|flood\w*|slowloris)\b", re.I), "ddos_attack"),
    (re.compile(r"\b(api[- ]?security|graphql|swagger|openapi)\b", re.I), "api_security"),
    (re.compile(r"\b(cipher\w*|encryption|cryptograph\w*|cryptanalys\w*)\b", re.I), "cryptography"),
]


def refine_category(title: str, description: str, cid: str) -> str:
    """When a tool lands in the generic 'other_tools' bucket, route it to a
    clearer category by keyword. Leaves every other category untouched."""
    if cid != "other_tools":
        return cid
    blob = f"{title} {description}"
    for pat, target in _ROUTES:
        if pat.search(blob):
            return target
    return cid
