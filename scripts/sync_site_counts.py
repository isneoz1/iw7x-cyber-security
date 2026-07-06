#!/usr/bin/env python3
"""Regenerate the site's category grid (the `var CATS=[...]` array in
docs/index.html) from the live catalog counts — sorted, bilingual labels kept.

Run after the catalog grows so the public site stays accurate without hand edits.

    python scripts/sync_site_counts.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
SITE = ROOT / "docs" / "index.html"

# catalog id -> English display name used in the site grid (update_uninstall omitted)
ID_TO_EN = {
    "osint": "OSINT / Recon", "other_tools": "Other Tools / OSINT", "web_attack": "Web Attack",
    "information_gathering": "Information Gathering", "forensics": "Forensics / DFIR",
    "reverse_engineering": "Reverse Engineering", "network_sniffing": "Sniffing & Network MITM",
    "malware_analysis": "Malware Analysis", "honeypots": "Honeypots / Deception",
    "cryptography": "Cryptography / Encryption", "wordlist_generator": "Wordlist / Password",
    "iot_hardware": "IoT / Firmware / Hardware", "blue_team": "Blue Team / Defense",
    "mobile_security": "Mobile Security", "exploit_framework": "Exploit Framework",
    "active_directory": "Active Directory", "api_security": "API Security",
    "privilege_escalation": "Privilege Escalation", "wireless_attack": "Wireless Attack",
    "payload_creation": "Payload Creation", "binary_exploitation": "Binary Exploitation / CTF",
    "threat_intel": "Threat Intelligence", "vuln_scanning": "Vulnerability Scanning",
    "ctf_tools": "CTF / Wargames", "fuzzing": "Fuzzing", "phishing_attack": "Phishing",
    "automotive": "Automotive / CAN", "physical_security": "Physical / RFID / Badge",
    "steganography": "Steganography", "post_exploitation": "Post-Exploitation / C2",
    "social_engineering": "Social Engineering", "ddos_attack": "DDoS / Stress Test",
    "radio_sdr": "Radio / SDR / RF", "blockchain_web3": "Blockchain / Web3",
    "container_k8s": "Container / Kubernetes", "voip": "VoIP Security",
    "cloud_security": "Cloud Security", "threat_hunting": "Threat Hunting",
    "data_exfiltration": "Data Exfiltration", "devsecops": "DevSecOps / SAST-DAST",
    "sql_injection": "SQL Injection", "supply_chain": "Supply Chain / SBOM",
    "sandbox_analysis": "Malware Sandbox / Detonation", "xss_attack": "XSS Attack",
    "anonymously_hiding": "Anonymity / Hiding", "remote_admin_rat": "Remote Admin (RAT)",
    "ics_scada": "ICS / SCADA / OT", "satellite": "Satellite / GNSS / Space",
    "ai_ml_security": "AI / ML Security", "game_hacking": "Game Hacking",
}

ENTRY = re.compile(r'\["((?:[^"\\]|\\.)*)","([^"]*)",(\d+),"((?:[^"\\]|\\.)*)"\]')


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    count_by_en = {ID_TO_EN[c["id"]]: len(c.get("tools", []))
                   for c in data["categories"] if c["id"] in ID_TO_EN}

    html = SITE.read_text(encoding="utf-8")
    m = re.search(r"var CATS=\[(.*?)\];", html, re.S)
    if not m:
        raise SystemExit("CATS array not found in docs/index.html")

    entries = ENTRY.findall(m.group(1))
    if not entries:
        raise SystemExit("no CATS entries parsed")

    # Keep emoji + FR label from the site; take the count from the live catalog.
    rebuilt = []
    for en, emoji, old_count, fr in entries:
        cnt = count_by_en.get(en, int(old_count))
        rebuilt.append((en, emoji, cnt, fr))
    rebuilt.sort(key=lambda e: -e[2])

    arr = "[" + ",".join(
        f'["{en}","{emoji}",{cnt},"{fr}"]' for en, emoji, cnt, fr in rebuilt
    ) + "]"
    new_html = html[:m.start()] + "var CATS=" + arr + ";" + html[m.end():]
    SITE.write_text(new_html, encoding="utf-8")
    print(f"Synced {len(rebuilt)} categories · total {sum(e[2] for e in rebuilt)} tools in grid")


if __name__ == "__main__":
    main()
