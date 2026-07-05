# 🗂️ The iw7x Arsenal

A reference of what ships in [`catalog.json`](catalog.json). Every entry installs and launches straight from the menu or the shell.

> **38 categories · 10,068 tools** in the shipped catalog — and the built‑in scanner (`python3 neoz.py --update`) keeps adding more from BlackArch, Kali and dozens of awesome‑lists.

Find any tool instantly:

```bash
python3 neoz.py search "kerberos"     # search everything
python3 neoz.py list                  # all categories
python3 neoz.py list "active directory"   # tools in a category
python3 neoz.py bloodhound            # install (if needed) + run
```

---

## Categories & featured tools

| # | Category | Tools | A few of what's inside |
|--:|----------|:-----:|------------------------|
| 1 | 🧰 Other Tools / OSINT | 1576 | Utility & niche tooling across domains |
| 2 | 🌐 Web Attack | 1498 | Burp Suite, Gobuster, wafw00f, ffuf, dirsearch |
| 3 | 🔍 Information Gathering | 1342 | Nmap, Masscan, Dracnmap, asnmap, nmapAutomator |
| 4 | 🕵️ OSINT / Recon | 1297 | theHarvester, Amass, SpiderFoot, Subfinder, Sherlock |
| 5 | 🔬 Forensics / DFIR | 700 | Autopsy, Wireshark, Volatility 3, Binwalk, Sleuth Kit |
| 6 | 🧠 Reverse Engineering | 509 | Ghidra, radare2, JadX, Frida |
| 7 | 🛡️ Blue Team / Defense | 474 | YARA, Sigma, detection & monitoring tooling |
| 8 | 📶 Sniffing & Network MITM | 369 | Bettercap, Responder, Wireshark, Hydra |
| 9 | 🔌 IoT / Firmware / Hardware | 234 | Firmware extraction & hardware hacking tools |
| 10 | 🏰 Active Directory | 214 | BloodHound, NetExec, Impacket, Responder, Certipy |
| 11 | 🔑 Wordlist / Password | 210 | Hashcat, John the Ripper, THC‑Hydra |
| 12 | 💥 Exploit Framework | 204 | Metasploit, Impacket, Pacu |
| 13 | 🧬 Malware Analysis | 201 | Sandboxes, unpackers, static/dynamic analysis |
| 14 | 🧨 Binary Exploitation / CTF | 149 | pwn tooling, ROP, heap, CTF helpers |
| 15 | 📱 Mobile Security | 131 | MobSF, Frida, objection |
| 16 | 📡 Wireless Attack | 127 | Wifite, Aircrack‑ng, Bettercap |
| 17 | 🎯 Payload Creation | 105 | msfvenom‑style generators & obfuscators |
| 18 | 🩻 Vulnerability Scanning | 93 | Nuclei, Nikto, WPScan |
| 19 | 🐝 Fuzzing | 75 | Coverage‑guided & protocol fuzzers |
| 20 | 🎛️ Post‑Exploitation / C2 | 68 | Sliver, Havoc, PowerShell Empire |
| 21 | 🎣 Phishing | 61 | Campaign frameworks & credential harvesters |
| 22 | 🖼️ Steganography | 55 | Hide/extract data in media |
| 23 | 🚗 Automotive / CAN | 50 | CAN bus & vehicle security tooling |
| 24 | 🎭 Social Engineering | 46 | SET & pretext tooling |
| 25 | 💣 DDoS / Stress Test | 44 | Load & stress‑testing utilities |
| 26 | 📦 Container / Kubernetes | 38 | Trivy, kube‑hunter, kube‑bench |
| 27 | ☁️ Cloud Security | 36 | Prowler, Pacu |
| 28 | 📻 Radio / SDR / RF | 31 | SDR & RF analysis |
| 29 | ⛓️ Blockchain / Web3 | 26 | Smart‑contract & chain analysis |
| 30 | 💉 SQL Injection | 21 | SQLmap, NoSQLMap |
| 31 | ☎️ VoIP Security | 18 | SIP & VoIP testing |
| 32 | 🩹 XSS Attack | 14 | XSS discovery & exploitation |
| 33 | 🥷 Anonymity / Hiding | 13 | Tor, proxychains, anon tooling |
| 34 | 🖥️ Remote Admin (RAT) | 11 | Authorized remote‑access frameworks |
| 35 | 🤖 AI / ML Security | 9 | Model & LLM security tooling |
| 36 | 🛰️ Satellite / GNSS / Space | 9 | GNSS & satellite research |
| 37 | 🏭 ICS / SCADA / OT | 8 | Industrial control system testing |
| 38 | 🔁 Update / Uninstall | — | Maintain iw7x and installed tools |

---

## How entries are structured

Each tool is a JSON object — this is all it takes to add one:

```json
{
  "title": "Nuclei",
  "description": "Fast, template-based vulnerability scanner.",
  "install": ["go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"],
  "run": ["nuclei -u https://example.com"],
  "url": "https://github.com/projectdiscovery/nuclei",
  "tags": ["scanner", "web"],
  "os": ["linux", "macos"],
  "requires_root": false
}
```

Want to add yours? See [CONTRIBUTING.md](CONTRIBUTING.md) — it's a 5‑minute pull request.

---

> ⚠️ For **authorized security testing and education only.** See the [README disclaimer](README.md#-legal--ethical-use).
