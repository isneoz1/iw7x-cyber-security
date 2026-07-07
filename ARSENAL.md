# 🗂️ The iw7x Arsenal

A reference of what ships in [`catalog.json`](catalog.json). Every entry installs and launches straight from the menu or the shell.

> **52 categories · 14,476 tools** in the shipped catalog — and the built‑in scanner (`python3 neoz.py --update`) keeps adding more from BlackArch, Kali and dozens of awesome‑lists, in the background while you work.

Find any tool instantly:

```bash
python3 neoz.py search "kerberos"     # search everything
python3 neoz.py list                  # all categories
python3 neoz.py list "active directory"   # tools in a category
python3 neoz.py bundle web            # install a whole task kit at once
python3 neoz.py bloodhound            # install (if needed) + run
```

---

## Categories & featured tools

| # | Category | Tools | A few of what's inside |
|--:|----------|:-----:|------------------------|
| 1 | 🕵️ OSINT / Recon | 2321 | theHarvester, Amass, SpiderFoot, Subfinder, Sherlock |
| 2 | 🧰 Other Tools / OSINT | 1985 | Utility & niche tooling across domains |
| 3 | 🌐 Web Attack | 1765 | Burp Suite, ffuf, sqlmap, dalfox, Nuclei |
| 4 | 🔍 Information Gathering | 1273 | Nmap, Masscan, naabu, asnmap, RustScan |
| 5 | 🗄️ Self-Hosted & Infrastructure | 953 | Self-hostable apps & infrastructure |
| 6 | ⌨️ CLI Apps & Utilities | 718 | Terminal applications & shell tools |
| 7 | 🔬 Forensics / DFIR | 686 | Autopsy, Volatility 3, Wireshark, binwalk |
| 8 | 🧠 Reverse Engineering | 504 | Ghidra, radare2, Rizin, Frida, jadx |
| 9 | 📶 Sniffing & Network MITM | 415 | Bettercap, Responder, tcpdump, Ettercap |
| 10 | 🧬 Malware Analysis | 342 | YARA, capa, FLOSS, sandboxes |
| 11 | 🍯 Honeypots / Deception | 241 | Cowrie, OpenCanary, Conpot |
| 12 | 🔐 Cryptography / Encryption | 237 | OpenSSL, GnuPG, RsaCtfTool, Ciphey |
| 13 | 🔑 Wordlist / Password | 229 | Hashcat, John the Ripper, Hydra, crunch |
| 14 | 🔌 IoT / Firmware / Hardware | 227 | Firmware & hardware hacking |
| 15 | 🛡️ Blue Team / Defense | 208 | YARA, Sigma, Suricata, Zeek |
| 16 | 📱 Mobile Security | 206 | MobSF, Frida, objection, jadx |
| 17 | 🏰 Active Directory | 205 | NetExec, BloodHound, Impacket, Certipy |
| 18 | 💥 Exploit Framework | 202 | Metasploit, Impacket, Pacu |
| 19 | 🔗 API Security | 180 | Kiterunner, Arjun, GraphQL tooling |
| 20 | 📡 Wireless Attack | 126 | Aircrack-ng, Wifite, Bettercap |
| 21 | ⏫ Privilege Escalation | 122 | LinPEAS, GTFOBins, traitor |
| 22 | 🧨 Binary Exploitation / CTF | 117 | pwntools, GEF, Ropper, one_gadget |
| 23 | 🎯 Payload Creation | 116 | msfvenom, Donut, ScareCrow |
| 24 | 🔭 Threat Intelligence | 91 | MISP, OpenCTI, MalwareBazaar |
| 25 | 🩻 Vulnerability Scanning | 89 | Nuclei, Nikto, WPScan, OpenVAS |
| 26 | 🚩 CTF / Wargames | 79 | pwntools, RsaCtfTool, CTF helpers |
| 27 | 🐝 Fuzzing | 75 | ffuf, AFL++, honggfuzz, boofuzz |
| 28 | 🎣 Phishing | 59 | Gophish, Evilginx2, Zphisher |
| 29 | 🚪 Physical / RFID / Badge | 57 | Proxmark, mfoc, lockpicking |
| 30 | 🚗 Automotive / CAN | 55 | can-utils, CAN bus tooling |
| 31 | 🖼️ Steganography | 53 | steghide, zsteg, StegSeek |
| 32 | 🎛️ Post-Exploitation / C2 | 47 | Sliver, Havoc, chisel, ligolo-ng |
| 33 | 🎭 Social Engineering | 46 | SET, King Phisher |
| 34 | 📦 Container / Kubernetes | 45 | Trivy, kube-hunter, kubescape |
| 35 | 💣 DDoS / Stress Test | 43 | GoldenEye, hping3, slowhttptest |
| 36 | ⛓️ Blockchain / Web3 | 41 | Slither, Mythril |
| 37 | 📻 Radio / SDR / RF | 41 | rtl_433, URH, multimon-ng |
| 38 | ☁️ Cloud Security | 33 | Prowler, ScoutSuite, Pacu, CloudFox |
| 39 | ☎️ VoIP Security | 31 | SIPVicious, sngrep, SIPp |
| 40 | 🐺 Threat Hunting | 27 | Sigma, hunting tooling |
| 41 | 📤 Data Exfiltration | 26 | dnscat2, iodine, ptunnel-ng |
| 42 | ♻️ DevSecOps / SAST-DAST | 25 | Semgrep, Trivy, Gitleaks |
| 43 | 💉 SQL Injection | 21 | SQLmap, Ghauri, NoSQLMap |
| 44 | 🧱 Supply Chain / SBOM | 17 | Syft, Grype, osv-scanner |
| 45 | 🧪 Malware Sandbox / Detonation | 15 | firejail, bubblewrap |
| 46 | 🩹 XSS Attack | 14 | XSStrike, dalfox, kxss |
| 47 | 🥷 Anonymity / Hiding | 13 | Tor, proxychains, macchanger |
| 48 | 🤖 AI / ML Security | 12 | garak, PyRIT, ART, TextAttack |
| 49 | 🖥️ Remote Admin (RAT) | 11 | Authorized remote-access frameworks |
| 50 | 🏭 ICS / SCADA / OT | 11 | Conpot, pymodbus, s7scan |
| 51 | 🛰️ Satellite / GNSS / Space | 11 | GNSS-SDR, gpredict, gr-gsm |
| 52 | 🎮 Game Hacking | 8 | PINCE, Il2CppDumper, BepInEx |
| 53 | 🔁 Update / Uninstall | — | Maintain iw7x and installed tools |

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
