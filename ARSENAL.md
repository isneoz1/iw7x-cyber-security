# 🗂️ The iw7x Arsenal

A reference of what ships in [`catalog.json`](catalog.json). Every entry installs and launches straight from the menu or the shell.

> **50 categories · 13,022 tools** in the shipped catalog — and the built‑in scanner (`python3 neoz.py --update`) keeps adding more from BlackArch, Kali and dozens of awesome‑lists.

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
| 1 | 🧰 Other Tools / OSINT | 1512 | Utility & niche tooling across domains |
| 2 | 🌐 Web Attack | 1511 | Burp Suite, Gobuster, wafw00f, ffuf, dirsearch |
| 3 | 🔍 Information Gathering | 1310 | Nmap, Masscan, Dracnmap, asnmap, nmapAutomator |
| 4 | 🕵️ OSINT / Recon | 1282 | theHarvester, Amass, SpiderFoot, Subfinder, Sherlock |
| 5 | 🔬 Forensics / DFIR | 689 | Autopsy, Wireshark, Volatility 3, Binwalk, Sleuth Kit |
| 6 | 🧠 Reverse Engineering | 504 | Ghidra, radare2, JadX, Frida |
| 7 | 🛡️ Blue Team / Defense | 408 | YARA, Sigma, detection & monitoring tooling |
| 8 | 📶 Sniffing & Network MITM | 369 | Bettercap, Responder, Wireshark, Hydra |
| 9 | 🔌 IoT / Firmware / Hardware | 229 | Firmware extraction & hardware hacking tools |
| 10 | 🔐 Cryptography / Encryption | 225 | OpenSSL, GnuPG, age, crypto libs & CTF crypto |
| 11 | 🔑 Wordlist / Password | 213 | Hashcat, John the Ripper, THC‑Hydra |
| 12 | 🏰 Active Directory | 203 | BloodHound, NetExec, Impacket, Responder, Certipy |
| 13 | 🧬 Malware Analysis | 199 | Sandboxes, unpackers, static/dynamic analysis |
| 14 | 💥 Exploit Framework | 198 | Metasploit, Impacket, Pacu |
| 15 | 🔗 API Security | 167 | Kiterunner, Arjun, GraphQL & Swagger tooling |
| 16 | 🧨 Binary Exploitation / CTF | 148 | pwn tooling, ROP, heap, CTF helpers |
| 17 | 📱 Mobile Security | 130 | MobSF, Frida, objection |
| 18 | 📡 Wireless Attack | 125 | Wifite, Aircrack‑ng, Bettercap |
| 19 | ⏫ Privilege Escalation | 125 | LinPEAS, WinPEAS, GTFOBins, exploit‑suggester |
| 20 | 🔭 Threat Intelligence | 114 | MISP, OpenCTI, MalwareBazaar, IOC & ATT&CK |
| 21 | 🎯 Payload Creation | 105 | msfvenom‑style generators & obfuscators |
| 22 | 🩻 Vulnerability Scanning | 90 | Nuclei, Nikto, WPScan |
| 23 | 🐝 Fuzzing | 75 | Coverage‑guided & protocol fuzzers |
| 24 | 🎣 Phishing | 60 | Campaign frameworks & credential harvesters |
| 25 | 🖼️ Steganography | 55 | Hide/extract data in media |
| 26 | 🎛️ Post‑Exploitation / C2 | 49 | Sliver, Havoc, PowerShell Empire |
| 27 | 🚗 Automotive / CAN | 49 | CAN bus & vehicle security tooling |
| 28 | 🎭 Social Engineering | 46 | SET & pretext tooling |
| 29 | 💣 DDoS / Stress Test | 44 | Load & stress‑testing utilities |
| 30 | 📦 Container / Kubernetes | 37 | Trivy, kube‑hunter, kube‑bench |
| 31 | ☁️ Cloud Security | 32 | Prowler, Pacu |
| 32 | 📻 Radio / SDR / RF | 31 | SDR & RF analysis |
| 33 | ♻️ DevSecOps / SAST‑DAST | 28 | Semgrep, SonarQube, dependency‑check, IaC scanners |
| 34 | ⛓️ Blockchain / Web3 | 26 | Smart‑contract & chain analysis |
| 35 | 💉 SQL Injection | 21 | SQLmap, NoSQLMap |
| 36 | ☎️ VoIP Security | 18 | SIP & VoIP testing |
| 37 | 🩹 XSS Attack | 14 | XSS discovery & exploitation |
| 38 | 🥷 Anonymity / Hiding | 13 | Tor, proxychains, anon tooling |
| 39 | 🚪 Physical / RFID / Badge | 13 | Proxmark, RFIDIOt, mfoc/mfcuk, badge cloning |
| 40 | 🖥️ Remote Admin (RAT) | 11 | Authorized remote‑access frameworks |
| 41 | 🛰️ Satellite / GNSS / Space | 9 | GNSS & satellite research |
| 42 | 🤖 AI / ML Security | 9 | Model & LLM security tooling |
| 43 | 🏭 ICS / SCADA / OT | 8 | Industrial control system testing |
| 44 | 🔁 Update / Uninstall | — | Maintain iw7x and installed tools |

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
