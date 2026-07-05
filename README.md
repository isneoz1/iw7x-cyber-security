<div align="center">

<h1>⚡ iw7x</h1>

### Every cybersecurity tool in the world. One terminal. One command.

**iw7x** unifies **8,000+** offensive & defensive security tools — from Nmap to BloodHound, Metasploit to Volatility — into a single, beautiful command‑line arsenal that installs, updates and launches anything for you.

<br/>

[![Stars](https://img.shields.io/github/stars/isneoz1/iw7x-cyber-security?style=for-the-badge&color=FF47B3&labelColor=1a1a2e&logo=github)](https://github.com/isneoz1/iw7x-cyber-security/stargazers)
[![Forks](https://img.shields.io/github/forks/isneoz1/iw7x-cyber-security?style=for-the-badge&color=9652FF&labelColor=1a1a2e&logo=github)](https://github.com/isneoz1/iw7x-cyber-security/network/members)
[![Issues](https://img.shields.io/github/issues/isneoz1/iw7x-cyber-security?style=for-the-badge&color=48DCFF&labelColor=1a1a2e&logo=github)](https://github.com/isneoz1/iw7x-cyber-security/issues)
[![License](https://img.shields.io/badge/License-MIT-4AE3A8?style=for-the-badge&labelColor=1a1a2e)](LICENSE)

[![Tools](https://img.shields.io/badge/Tools-8%2C000%2B-FF47B3?style=for-the-badge&labelColor=1a1a2e)](catalog.json)
[![Categories](https://img.shields.io/badge/Categories-38-9652FF?style=for-the-badge&labelColor=1a1a2e)](#-the-arsenal)
[![Python](https://img.shields.io/badge/Python-3.10%2B-48DCFF?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e)](https://www.python.org/)
[![Kali](https://img.shields.io/badge/Kali%20Linux-Ready-4AE3A8?style=for-the-badge&logo=kalilinux&logoColor=white&labelColor=1a1a2e)](https://www.kali.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-FFD15C?style=for-the-badge&labelColor=1a1a2e)](CONTRIBUTING.md)

**🌍 [English](README.md) · [Français](README.fr.md)**

</div>

```text
     ██╗ ██╗    ██╗ ███████╗ ██╗  ██╗
     ██║ ██║    ██║ ╚════██║ ╚██╗██╔╝
     ██║ ██║ █╗ ██║     ██╔╝  ╚███╔╝
     ██║ ██║███╗██║    ██╔╝   ██╔██╗
     ██║ ╚███╔███╔╝    ██║   ██╔╝ ██╗
     ╚═╝  ╚══╝╚══╝     ╚═╝   ╚═╝  ╚═╝
      C Y B E R S E C U R I T Y   A R S E N A L
        8104 TOOLS · 38 CATEGORIES · BY NeoZ
```

> ⚠️ **For authorized security testing and education only.** See the [Legal & Ethical Use](#-legal--ethical-use) section before you begin.

---

## ✨ Why iw7x?

Security professionals waste hours hunting for the right tool, cloning repos, fixing dependencies and remembering install commands. **iw7x replaces all of that with one program.**

| | |
|---|---|
| 🗂️ **The whole ecosystem** | **8,000+ tools** across **38 categories** — OSINT, web, wireless, exploitation, forensics, reversing, cloud, AD, mobile, IoT, blue team & more. |
| ⚙️ **Install & run for you** | Pick a tool → iw7x installs it (apt / pipx / go / git) and launches it. No more copy‑pasting install snippets. |
| 🔄 **Always up to date** | A built‑in scanner pulls fresh tools from **BlackArch, Kali & awesome‑lists** so your arsenal keeps growing on its own. |
| 🔎 **Find anything instantly** | Full‑text search, tag filters (`osint`, `c2`, `web`…) and a task **advisor** that recommends tools for what you're trying to do. |
| 🎨 **A terminal you enjoy** | A gorgeous [rich](https://github.com/Textualize/rich)‑powered TUI with live system header, gradients and clean menus. |
| 🧩 **Data‑driven & hackable** | Every tool is one JSON entry — no spaghetti classes. Adding a tool is a 6‑line pull request. |
| 🚫 **Never crashes on you** | Bad tool name, missing binary or offline? You get a clear message, never a traceback. |

---

## 🚀 Quick Start

> **Recommended OS:** [Kali Linux](https://www.kali.org/) (or Kali on WSL2). iw7x runs tools on Kali; the menu, search and catalog work everywhere.

```bash
# 1. Clone
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security

# 2. Install dependencies (git, python, pipx, go…)
chmod +x install.sh && ./install.sh

# 3. Launch the arsenal
python3 neoz.py
```

That's it. On first run iw7x fetches the full catalog so every tool is one keystroke away.

<details>
<summary><b>⚡ One‑liner install</b></summary>

```bash
git clone https://github.com/isneoz1/iw7x-cyber-security.git && cd iw7x-cyber-security && ./install.sh && python3 neoz.py
```
</details>

<details>
<summary><b>🐳 Run with Docker</b></summary>

```bash
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security
python3 -m pip install -r requirements.txt   # just needs `rich`
python3 neoz.py
```
</details>

---

## 🎮 Usage

### Interactive menu

```bash
python3 neoz.py            # or: python3 iw7x.py
```

Inside the menu:

| Key | Action |
|-----|--------|
| `1–N` | Open a category |
| `/query` | Search every tool by name / keyword |
| `T` | Filter by tag (`osint`, `web`, `c2`, `wireless`…) |
| `R` | **Advisor** — "What do you want to do?" → recommended tools |
| `U` | Update: fetch every new tool online |
| `?` | Help · `Q` Quit |

### From the shell (no menu needed)

```bash
python3 neoz.py nmap              # install (if needed) and run a tool by name
python3 neoz.py search "sql inj"  # list matching tools
python3 neoz.py list              # list all 38 categories
python3 neoz.py list osint        # list tools in a category
python3 neoz.py install bloodhound
python3 neoz.py --update          # pull every tool from online sources
python3 neoz.py --watch 30        # live auto‑scan every 30 min
python3 neoz.py --help            # full CLI help
```

---

## 🗂️ The Arsenal

**38 categories · 8,104 curated tools** — and growing automatically.

| Category | Tools | Category | Tools |
|---|:--:|---|:--:|
| 🔍 Information Gathering | 1342 | 🧬 Malware Analysis | 201 |
| 🌐 Web Attack | 1288 | 💥 Exploit Framework | 200 |
| 🕵️ OSINT & Recon | 407 | 🔑 Wordlist / Password | 198 |
| 🛡️ Blue Team / Defense | 474 | 🧨 Binary Exploitation / CTF | 149 |
| 🔬 Forensics / DFIR | 666 | 📡 Wireless Attack | 123 |
| 🧠 Reverse Engineering | 475 | 🩻 Vulnerability Scanning | 93 |
| 📶 Sniffing & Network MITM | 369 | 📱 Mobile Security | 85 |
| 🔌 IoT / Firmware / Hardware | 226 | 🎯 Payload Creation | 84 |
| 🏰 Active Directory | 214 | 🐝 Fuzzing | 75 |
| 🧰 Other Tools / OSINT | 899 | 🎛️ Post‑Exploitation / C2 | 68 |
| 🎣 Phishing | 61 | 🚗 Automotive / CAN | 50 |
| 💣 DDoS / Stress Test | 44 | 🖼️ Steganography | 44 |
| 📦 Container / Kubernetes | 38 | ☁️ Cloud Security | 36 |
| 🎭 Social Engineering | 33 | 📻 Radio / SDR / RF | 31 |
| ⛓️ Blockchain / Web3 | 26 | 💉 SQL Injection | 21 |
| ☎️ VoIP Security | 18 | 🩹 XSS Attack | 14 |
| 🥷 Anonymity / Hiding | 13 | 🖥️ Remote Admin (RAT) | 11 |
| 🤖 AI / ML Security | 9 | 🛰️ Satellite / GNSS / Space | 9 |
| 🏭 ICS / SCADA / OT | 8 | 🔁 Update / Uninstall | — |

<details>
<summary><b>A taste of what's inside</b></summary>

`Nmap` · `Masscan` · `theHarvester` · `Amass` · `SpiderFoot` · `Sherlock` · `Nuclei` · `Burp Suite` · `OWASP ZAP` · `SQLmap` · `ffuf` · `Gobuster` · `Aircrack‑ng` · `Bettercap` · `Wifite` · `Hashcat` · `John the Ripper` · `Hydra` · `Metasploit` · `Sliver` · `Havoc` · `Empire` · `BloodHound` · `Impacket` · `NetExec` · `Responder` · `Certipy` · `Ghidra` · `radare2` · `Frida` · `jadx` · `Volatility` · `Autopsy` · `binwalk` · `YARA` · `Prowler` · `Pacu` · `MobSF` · `Wireshark` · `evilginx` · … and thousands more.

</details>

---

## 🔄 Self‑growing catalog

iw7x isn't a static list. Run `--update` (or press `U`) and it scans **BlackArch**, **Kali** and community **awesome‑lists**, deduplicates, and adds every new tool it finds — with install commands ready to go. The goal is simple: **every security tool on Earth, always current, in one place.**

```bash
python3 neoz.py --update          # one‑off full scan
python3 neoz.py --watch 60        # keep scanning every hour
```

---

## 🤝 Contributing

**iw7x grows because of people like you.** Adding a tool is the easiest open‑source contribution you'll ever make — it's just one JSON object:

```json
{
  "title": "Subfinder",
  "description": "Fast passive subdomain enumeration.",
  "install": ["go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"],
  "run": ["subfinder -d example.com"],
  "url": "https://github.com/projectdiscovery/subfinder",
  "tags": ["osint", "recon"]
}
```

Add it to `catalog.json`, open a PR — done. See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full guide, or just [request a tool](https://github.com/isneoz1/iw7x-cyber-security/issues/new/choose) and we'll add it.

⭐ **Star the repo** to help other hackers discover it — that's the single biggest thing you can do to grow the project.

---

## 🛣️ Roadmap

- [ ] Web dashboard companion
- [ ] Per‑tool cheat‑sheets inside the TUI
- [ ] Profiles ("Web pentest", "AD pentest", "OSINT") that install a curated bundle
- [ ] Community tool ratings
- [ ] Plugin API for private tool catalogs
- [ ] More languages (🇪🇸 🇩🇪 🇵🇹 🇸🇦 🇨🇳)

Vote on features in the [Discussions](https://github.com/isneoz1/iw7x-cyber-security/discussions).

---

## ⚖️ Legal & Ethical Use

iw7x is a **penetration‑testing and security‑education** framework intended **exclusively** for:

- 🎯 Systems you **own** or have **explicit written authorization** to test
- 🎓 Learning, CTFs, labs and authorized red‑team engagements
- 🛡️ Defensive research and blue‑team work

**Unauthorized access to computer systems is illegal.** You are solely responsible for your actions and for complying with all applicable laws. The authors and contributors accept **no liability** for misuse or damage caused by this software. If you don't have permission — **stop.**

---

## 📜 License

Released under the [MIT License](LICENSE). Individual tools distributed via the catalog remain under **their own** respective licenses.

---

## 💛 Support the project

If iw7x saves you time, please:

⭐ **Star** it · 🔀 **Fork** it · 🐛 **Report** issues · 🧩 **Add a tool** · 📣 **Share** it with your team

---

<div align="center">

### ⭐ Star history

[![Star History Chart](https://api.star-history.com/svg?repos=isneoz1/iw7x-cyber-security&type=Date)](https://star-history.com/#isneoz1/iw7x-cyber-security&Date)

<br/>

**Built with 💜 by [NeoZ](https://github.com/isneoz1)** — *offense informs defense.*

<sub>The quieter you become, the more you can hear.</sub>

</div>
