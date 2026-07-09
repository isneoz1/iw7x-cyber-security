<div align="center">

# iw7x — Compatibility Guide

**Run iw7x on any device in the world.** &nbsp;·&nbsp; **[English](COMPATIBILITY.md) · [Français](COMPATIBILITY.fr.md)**

</div>

iw7x is a small Python program, so its **menu, search and browsing run anywhere Python runs** — Windows, macOS, Linux, even a phone. To **install and launch** the security tools themselves you need a **Linux (Kali) environment**, because that's where the tools live. This guide shows the easiest path to that on every kind of device.

> **The universal answer is Docker.** If your device runs Docker, it runs the *full* iw7x — see [Docker](#docker--the-universal-method). Everything else below is for when you'd rather run it natively.

---

## Compatibility matrix

| Device / OS | Browse & search | Install & run tools | Easiest full-power method |
|---|:---:|:---:|---|
| **Kali Linux** (any arch) | ✅ | ✅ | Native — just run it |
| **Windows 10 / 11** | ✅ (native Python) | ✅ | **WSL2 + Kali**, Docker, or a VM |
| **macOS** (Apple Silicon / Intel) | ✅ (native Python) | ✅ | **Docker**, or a Kali VM (UTM/VirtualBox/VMware) |
| **Ubuntu / Debian / Mint** | ✅ | ✅ | Native (apt) — most tools install directly |
| **Arch / BlackArch / Manjaro** | ✅ | ✅ | Native — `pacman` auto-adapts |
| **Fedora / RHEL / openSUSE** | ✅ | ✅ (most) | Native, or Docker for parity |
| **Android** (phone / tablet) | ✅ (Termux) | ✅ | **Kali NetHunter**, or Termux |
| **Raspberry Pi / ARM SBC** | ✅ | ✅ | Kali ARM image, or Docker (arm64) |
| **Chromebook** | ✅ | ✅ | Linux (Crostini) container, or Docker |
| **Cloud / VPS** | ✅ | ✅ | Any Debian/Kali droplet + SSH |
| **iOS / iPadOS** | ✅ (a-Shell/iSH, limited) | ⚠️ | Use a remote Kali box over SSH |

✅ = works · ⚠️ = limited (browse only; run tools on a remote Linux box)

---

## Requirements (all platforms)

- **Python 3.10+** (`python3 --version`)
- **git** (for tools installed from source)
- An **internet connection** on first launch (to fetch the full catalog)
- To install/run tools: a **Linux** userland (native, WSL2, VM, Docker, Termux, or remote)

Install then launch, on any Linux/WSL/macOS shell:

```bash
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security
chmod +x install.sh && ./install.sh
python3 neoz.py
```

---

## Docker — the universal method

Works identically on **Windows, macOS, Linux, ARM/Apple Silicon, Raspberry Pi and the cloud**. The image is Kali-based, so tool installation works no matter what the host is.

```bash
# 1. Get the code
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security

# 2. Build once
docker build -t iw7x .

# 3. Run the interactive arsenal
docker run -it --rm iw7x

# …or install & launch a single tool directly
docker run -it --rm iw7x nmap
```

Prefer Compose? `docker compose run --rm iw7x` (a named volume keeps your installed tools between runs).

> Install Docker: **Docker Desktop** on Windows/macOS, or `curl -fsSL https://get.docker.com | sh` on Linux.

---

## Windows

**Option A — WSL2 + Kali (recommended, native speed).** In an **Administrator** PowerShell:

```powershell
wsl --install
wsl --install -d kali-linux
```

Reboot if asked, open **Kali** from the Start menu, create your user, then:

```bash
sudo apt update && sudo apt -y full-upgrade
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security && chmod +x install.sh && ./install.sh && python3 neoz.py
```

**Option B — Docker Desktop.** See [Docker](#docker--the-universal-method).

**Option C — Virtual Machine.** Import the official Kali VirtualBox/VMware image from <https://www.kali.org/get-kali/#kali-virtual-machines>.

**Option D — Native Python (browse only).** Install Python from python.org, then `python neoz.py` — you can browse and search all 30,000+ tools; install/launch needs one of A–C.

---

## macOS (Apple Silicon & Intel)

**Option A — Docker Desktop (recommended).** See [Docker](#docker--the-universal-method). The Kali image runs natively on Apple Silicon (arm64) and Intel (amd64).

**Option B — Kali VM.** Use **UTM** (free, best for Apple Silicon) or VirtualBox/VMware with the ARM64 or Intel Kali image from the [Kali downloads](https://www.kali.org/get-kali/#kali-virtual-machines).

**Option C — Native (browse only).** macOS ships Python 3; `python3 neoz.py` browses the catalog. Homebrew can install *some* tools, but for full parity use Docker or a VM.

---

## Linux

**Kali** — the home turf. Clone, `./install.sh`, `python3 neoz.py`. Everything just works.

**Ubuntu / Debian / Mint** — most tools install directly (they're `apt`/`pipx`/`go` based):

```bash
sudo apt update && sudo apt install -y git python3 python3-pip pipx golang-go
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security && ./install.sh && python3 neoz.py
```

**Arch / BlackArch / Manjaro** — iw7x auto-rewrites `pacman` ↔ `apt` both ways, so BlackArch-sourced tools install cleanly.

**Fedora / RHEL / openSUSE** — the Python app and most `pipx`/`go`/`git` tools work; for the handful that assume Debian packaging, use Docker for full parity.

> iw7x detects your distro and adapts package-manager commands automatically (`system.adapt_command`), so a single catalog works across distros.

---

## Android (phone & tablet)

**Option A — Kali NetHunter (full power).** Install NetHunter (rooted or the non-root NetHunter chroot) from <https://www.kali.org/get-kali/#kali-mobile>, open the Kali shell, then clone and run iw7x exactly like on desktop Kali.

**Option B — Termux.** Install [Termux](https://f-droid.org/en/packages/com.termux/) (from F-Droid), then:

```bash
pkg update && pkg install -y git python
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security && python neoz.py
```

Browsing/search work great; many pure-Python and Go tools install too. For tools that need full Kali packaging, use NetHunter or a remote box.

---

## Raspberry Pi & ARM boards

Flash the **Kali ARM image** for your board from <https://www.kali.org/get-kali/#kali-arm>, boot, then clone and run iw7x. On any Pi/SBC that runs Docker, the arm64 image (see [Docker](#docker--the-universal-method)) is the quickest route.

---

## Cloud / VPS

Spin up a Debian or Kali droplet (DigitalOcean, Hetzner, AWS, Azure…), SSH in, and run the [standard install](#requirements-all-platforms). This is ideal for long scans and always-on use, and reachable from any device — including iOS/iPadOS over SSH.

---

## iOS / iPadOS

Apple sandboxing prevents installing Linux security tools locally. Use a terminal app (**a-Shell**, **iSH**, **Blink**) to **SSH into a Kali box, a VPS, or a home machine** running iw7x — you get the full experience remotely from your iPhone/iPad.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `python: command not found` | Use `python3` (and `pip3`). On Windows native, install Python from python.org and tick *Add to PATH*. |
| `externally-managed-environment` (pip) | Newer Debian/Kali: `pip3 install --break-system-packages -r requirements.txt`, or use `pipx`. The Docker image already handles this. |
| "This action needs Kali Linux" when installing | You're browsing on a non-Kali host. Install/run from WSL2, a VM, Docker, or a remote Kali box. |
| A tool won't install on my distro | Use Docker for full Kali parity, or open the tool's GitHub (shown in its screen) and clone manually. |
| Colors/box-drawing look wrong | Use a UTF-8, truecolor terminal (Windows Terminal, iTerm2, most Linux terminals). |
| First launch is slow | It's fetching the full catalog once; subsequent launches are instant. Skip with `IW7X_NO_UPDATE=1`. |

---

## FAQ

**Does it run without Kali?** Yes — browsing/search run anywhere. Installing/launching tools needs a Linux (Kali) userland, which Docker/WSL2/VM/Termux/cloud all provide.

**Is Windows/macOS fully supported?** The app runs natively for browsing. For install+launch, Docker (all OSes) or WSL2 (Windows) give full power with no VM overhead.

**ARM / Apple Silicon / Raspberry Pi?** Yes — the Kali base image and Kali ARM builds are multi-arch.

**Do I need root?** Only some tools do (iw7x tells you). Docker and Kali run as root by default; on other setups use `sudo` when prompted.

---

<div align="center">

**[⬅ Back to the README](README.md)** &nbsp;·&nbsp; **[▶ Watch the demo](https://claude.ai/code/artifact/5210489a-74c0-4eb2-a04f-f33aa3080b3b)** &nbsp;·&nbsp; [github.com/isneoz1/iw7x-cyber-security](https://github.com/isneoz1/iw7x-cyber-security)

</div>
