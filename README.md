<div align="center">

<h1>⚡ iw7x</h1>

### Every cybersecurity tool in the world — in one Kali Linux terminal.

**iw7x** brings **12,669** offensive & defensive security tools — from Nmap to BloodHound, Metasploit to Volatility — into a single command‑line arsenal that **installs, updates and launches** any of them for you. Built for Kali Linux. Free forever.

<br/>

[![Stars](https://img.shields.io/github/stars/isneoz1/iw7x-cyber-security?style=for-the-badge&color=FF47B3&labelColor=1a1a2e&logo=github)](https://github.com/isneoz1/iw7x-cyber-security/stargazers)
[![Forks](https://img.shields.io/github/forks/isneoz1/iw7x-cyber-security?style=for-the-badge&color=9652FF&labelColor=1a1a2e&logo=github)](https://github.com/isneoz1/iw7x-cyber-security/network/members)
[![License](https://img.shields.io/badge/License-MIT-4AE3A8?style=for-the-badge&labelColor=1a1a2e)](LICENSE)

[![Tools](https://img.shields.io/badge/Tools-12%2C669-FF47B3?style=for-the-badge&labelColor=1a1a2e)](catalog.json)
[![Categories](https://img.shields.io/badge/Categories-50-9652FF?style=for-the-badge&labelColor=1a1a2e)](#the-arsenal--50-categories-12669-tools)
[![Python](https://img.shields.io/badge/Python-3.10%2B-48DCFF?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e)](https://www.python.org/)
[![Kali](https://img.shields.io/badge/Kali%20Linux-Ready-4AE3A8?style=for-the-badge&logo=kalilinux&logoColor=white&labelColor=1a1a2e)](https://www.kali.org/)
[![Website](https://img.shields.io/badge/Live_Site-Visit-48DCFF?style=for-the-badge&labelColor=1a1a2e)](https://isneoz1.github.io/iw7x-cyber-security/)

**[English](README.md) · [Français](README.fr.md)** &nbsp;·&nbsp; **[Live website →](https://isneoz1.github.io/iw7x-cyber-security/)**

<br/>

<img src="assets/iw7x-preview.svg" alt="iw7x — cybersecurity arsenal: 12,669 tools across 50 categories, built for Kali Linux, by NeoZ" width="840">

</div>

> ⚠️ **For authorized security testing and education only.** Read [Legal & Ethical Use](#legal--ethical-use) before you begin. If you don't have written permission to test a system, stop.

---

## A word from NeoZ

I'm NeoZ, and I built iw7x for one reason: I was tired of losing whole evenings to setup instead of hacking.

Every engagement, every CTF, every lab started the same way — open ten browser tabs, clone a repo, chase a broken dependency, read a README to remember the one install flag, give up, try another tool. The actual security work kept getting buried under plumbing.

So I made the thing I wished existed: **one terminal that already knows every tool, installs it the right way for Kali, and launches it for you.** You think "I need to enumerate this Active Directory" — you type `iw7x` and it's running. That's the whole idea.

This is a passion project. I keep it free, open source, and growing. If it saves you even one of those wasted evenings, **star it** so the next person finds it too. That's all I ask. — *NeoZ*

---

## Why you'll actually use it

| | |
|---|---|
| **The whole ecosystem** | **12,669 tools** across **50 categories** — OSINT, web, wireless, exploitation, forensics, reversing, crypto, cloud, Active Directory, mobile, IoT, CTF, honeypots, threat hunting, blue team and far more. |
| **It installs & runs for you** | Pick a tool → iw7x runs the right `apt` / `pipx` / `go` / `git` and launches it. No more copy‑pasting setup from a dozen READMEs. |
| **Built for Kali** | It detects your distro and even rewrites `pacman` ↔ `apt`, so BlackArch‑sourced tools install cleanly on Kali. |
| **Never stops growing** | A built‑in scanner pulls fresh tools from **BlackArch, Kali & 75+ awesome‑lists** — and keeps collecting **in the background while you work**, so new tools appear automatically without ever restarting. |
| **Find anything fast** | Full‑text search, tag filters (`osint`, `c2`, `web`…) and an **advisor** that recommends tools for the task you describe. |
| **Never dumps a traceback** | Bad name, missing binary, offline? You get a clear message — never a stack trace. |

---

## Step 1 — Get Kali Linux

iw7x runs its tools on **[Kali Linux](https://www.kali.org/)**. If you already have Kali, skip to [Step 2](#step-2--install-iw7x). If not, pick whichever method fits you — all are free and official.

<details open>
<summary><b>🖥️ Option A — Virtual Machine (easiest, recommended)</b></summary>

Run Kali safely inside your current OS (Windows/macOS/Linux). Nothing to dual‑boot.

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (free) — or VMware.
2. Download the prebuilt **Kali VirtualBox image**: <https://www.kali.org/get-kali/#kali-virtual-machines>
3. In VirtualBox: **File → Import Appliance →** select the downloaded file → **Import**.
4. Start the VM. Login is `kali` / `kali`.
5. Update once: `sudo apt update && sudo apt -y full-upgrade`

</details>

<details>
<summary><b>🪟 Option B — Windows without a VM (WSL2)</b></summary>

Run Kali as a Windows app. Open **PowerShell as Administrator**:

```powershell
wsl --install
wsl --install -d kali-linux
```

Reboot if asked, launch **Kali Linux** from the Start menu, create your user, then:

```bash
sudo apt update && sudo apt -y full-upgrade
```

> For GUI tools inside WSL, install the Win‑KeX package: `sudo apt install -y kali-win-kex`.

</details>

<details>
<summary><b>💾 Option C — Bare metal / dual boot (best performance)</b></summary>

1. Download the **Kali Installer ISO**: <https://www.kali.org/get-kali/#kali-installer-images>
2. Flash it to an 8 GB+ USB stick with [balenaEtcher](https://etcher.balena.io/) (any OS) or [Rufus](https://rufus.ie/) (Windows).
3. Boot your PC from the USB (usually `F12` / `Esc` / `Del` at startup to pick the boot device).
4. Choose **Graphical Install** and follow the steps. You can install alongside your current OS.

</details>

<details>
<summary><b>🔌 Option D — Live USB (try it, install nothing)</b></summary>

Want to test first? Flash the **Kali Live** image (same tools as above), boot from the USB and choose **Live**. Everything runs from RAM — nothing touches your disk.

</details>

> On a Mac with Apple Silicon? Use the **Apple Silicon / ARM64** VM image from the same download page.

---

## Step 2 — Install iw7x

On your Kali machine:

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
<summary><b>⚡ One‑liner</b></summary>

```bash
git clone https://github.com/isneoz1/iw7x-cyber-security.git && cd iw7x-cyber-security && chmod +x install.sh && ./install.sh && python3 neoz.py
```
</details>

---

## See it in action

**Install and run any tool by name** — iw7x handles the install, then opens it:

```console
$ python3 neoz.py nmap
[iw7x] Installing Nmap ...
[iw7x] Launching Nmap ...
Nmap 7.94 ( https://nmap.org )
Usage: nmap [Scan Type(s)] [Options] {target specification}
```

**Not sure which tool? Ask the advisor** — press `R` in the menu and describe the job:

```text
What do you want to do?
  1  Scan a network            5  Pentest Active Directory
  2  Find subdomains           6  Crack passwords
  3  OSINT a target            7  Capture a Wi‑Fi handshake
  4  Pentest a web app         8  Post‑exploitation / C2
> 5
Recommended for: Pentest Active Directory
  NetExec · BloodHound.py · Impacket · Certipy · Kerbrute · Responder · mitm6 …
```

**Real workflows, one line each:**

```bash
python3 neoz.py sherlock              # hunt a username across 400+ sites
python3 neoz.py nuclei                # template-based vuln scanning
python3 neoz.py bloodhound            # map Active Directory attack paths
python3 neoz.py hashcat               # crack hashes on your GPU
python3 neoz.py search "wifi"         # every wireless tool, instantly
python3 neoz.py list active_directory # browse a whole category
```

**Install a whole kit for the job in one command** — task bundles:

```bash
python3 neoz.py bundles               # list every kit
python3 neoz.py bundle web            # Web app pentest kit (nmap, nuclei, ffuf, sqlmap…)
python3 neoz.py bundle ad             # Active Directory kit (NetExec, BloodHound, Impacket…)
python3 neoz.py bundle osint          # OSINT recon kit
# 15 kits — also: wireless, pwn, forensics, cloud, passwords, c2, mobile, recon, bugbounty, malware, container, stego
```

**Prefer the menu?** Launch `python3 neoz.py` and drive it with your keyboard:

| Key | Action |
|:---:|--------|
| `1–N` | Open a category |
| `/query` | Search every tool by name / keyword |
| `T` | Filter by tag (`osint`, `web`, `c2`, `wireless`…) |
| `R` | Advisor — describe the task, get the tools |
| `U` | Update — pull every new tool online |
| `?` · `Q` | Help · Quit |

---

## The Arsenal — 50 categories, 12,669 tools

Every domain of offensive and defensive security, in one place — and growing with every `--update`.

| Category | Tools | Category | Tools |
|---|:--:|---|:--:|
| 🕵️ OSINT / Recon | 2348 | 🎣 Phishing | 59 |
| 🧰 Other Tools / OSINT | 1702 | 🚪 Physical / RFID / Badge | 57 |
| 🌐 Web Attack | 1667 | 🖼️ Steganography | 54 |
| 🔍 Information Gathering | 1298 | 🚗 Automotive / CAN | 49 |
| 🔬 Forensics / DFIR | 684 | 🎛️ Post‑Exploitation / C2 | 47 |
| 🧠 Reverse Engineering | 497 | 🎭 Social Engineering | 45 |
| 📶 Sniffing & Network MITM | 364 | 💣 DDoS / Stress Test | 44 |
| 🔐 Cryptography / Encryption | 233 | 📻 Radio / SDR / RF | 42 |
| 🍯 Honeypots / Deception | 232 | ⛓️ Blockchain / Web3 | 41 |
| 🔑 Wordlist / Password | 231 | 📦 Container / Kubernetes | 38 |
| 🔌 IoT / Firmware / Hardware | 229 | ☎️ VoIP Security | 34 |
| 🏰 Active Directory | 203 | ☁️ Cloud Security | 32 |
| 🧬 Malware Analysis | 202 | 🐺 Threat Hunting | 30 |
| 💥 Exploit Framework | 198 | 📤 Data Exfiltration | 26 |
| 🛡️ Blue Team / Defense | 186 | ♻️ DevSecOps / SAST‑DAST | 25 |
| 🔗 API Security | 167 | 💉 SQL Injection | 21 |
| 📱 Mobile Security | 130 | 🧱 Supply Chain / SBOM | 17 |
| 📡 Wireless Attack | 128 | 🧪 Malware Sandbox / Detonation | 15 |
| ⏫ Privilege Escalation | 125 | 🩹 XSS Attack | 14 |
| 🧨 Binary Exploitation / CTF | 118 | 🥷 Anonymity / Hiding | 13 |
| 🎯 Payload Creation | 107 | 🖥️ Remote Admin (RAT) | 11 |
| 🔭 Threat Intelligence | 94 | 🛰️ Satellite / GNSS / Space | 9 |
| 🩻 Vulnerability Scanning | 90 | 🤖 AI / ML Security | 9 |
| 🚩 CTF / Wargames | 82 | 🏭 ICS / SCADA / OT | 8 |
| 🐝 Fuzzing | 75 | 🎮 Game Hacking | 7 |

<details>
<summary><b>A taste of what's inside</b></summary>

`Nmap` · `Masscan` · `theHarvester` · `Amass` · `SpiderFoot` · `Sherlock` · `Nuclei` · `Burp Suite` · `OWASP ZAP` · `SQLmap` · `ffuf` · `Gobuster` · `Aircrack‑ng` · `Bettercap` · `Wifite` · `Hashcat` · `John the Ripper` · `Hydra` · `Metasploit` · `Sliver` · `Havoc` · `Empire` · `BloodHound` · `Impacket` · `NetExec` · `Responder` · `Certipy` · `Ghidra` · `radare2` · `Frida` · `jadx` · `Volatility` · `Autopsy` · `binwalk` · `YARA` · `Prowler` · `Pacu` · `MobSF` · `Wireshark` · `evilginx` · `Cowrie` · `CTFd` · … and thousands more.

</details>

---

## It keeps growing on its own

iw7x isn't a frozen list. Run `--update` (or press `U`) and it scans **BlackArch**, **Kali** and 70+ community **awesome‑lists**, deduplicates, and adds every new tool it finds — install commands ready to go.

```bash
python3 neoz.py --update          # one‑off full scan
python3 neoz.py --watch 60        # keep scanning every hour
```

The goal is simple: **every security tool on Earth, always current, in one place.**

---

## Contributing

iw7x grows because of people like you. Adding a tool is the easiest open‑source contribution you'll ever make — one JSON object:

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

Drop it into `catalog.json`, open a PR — done. See **[CONTRIBUTING.md](CONTRIBUTING.md)**, or just [request a tool](https://github.com/isneoz1/iw7x-cyber-security/issues/new/choose) and I'll add it.

---

## Legal & Ethical Use

iw7x is a **penetration‑testing and security‑education** framework, intended **only** for:

- Systems you **own** or have **explicit written authorization** to test
- Learning, CTFs, labs and authorized red‑team engagements
- Defensive research and blue‑team work

**Unauthorized access to computer systems is illegal.** You alone are responsible for your actions and for complying with all applicable laws. The authors accept **no liability** for misuse. No permission? Stop.

---

## License

Released under the [MIT License](LICENSE). Individual tools distributed via the catalog keep **their own** respective licenses.

---

<div align="center">

### If iw7x saves you time, star it ⭐

That one click is how the next hacker discovers it.

**⭐ Star · 🔀 Fork · 🐛 Report an issue · 🧩 Add a tool · 📣 Share it**

<br/>

[![Star History Chart](https://api.star-history.com/svg?repos=isneoz1/iw7x-cyber-security&type=Date)](https://star-history.com/#isneoz1/iw7x-cyber-security&Date)

<br/>

**Made with real passion by [NeoZ](https://github.com/isneoz1).**

<sub>The quieter you become, the more you can hear.</sub>

</div>
