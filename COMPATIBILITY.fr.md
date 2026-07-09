<div align="center">

# iw7x — Guide de compatibilité

**Faites tourner iw7x sur n'importe quel appareil au monde.** &nbsp;·&nbsp; **[English](COMPATIBILITY.md) · [Français](COMPATIBILITY.fr.md)**

</div>

iw7x est un petit programme Python : son **menu, sa recherche et la navigation tournent partout où Python tourne** — Windows, macOS, Linux, et même un téléphone. Pour **installer et lancer** les outils de sécurité eux‑mêmes, il faut un **environnement Linux (Kali)**, car c'est là que vivent les outils. Ce guide montre le chemin le plus simple vers ça, sur chaque type d'appareil.

> **La réponse universelle, c'est Docker.** Si votre appareil fait tourner Docker, il fait tourner iw7x *en entier* — voir [Docker](#docker--la-méthode-universelle). Tout le reste ci‑dessous, c'est pour une installation native.

---

## Matrice de compatibilité

| Appareil / OS | Naviguer & chercher | Installer & lancer | Méthode complète la plus simple |
|---|:---:|:---:|---|
| **Kali Linux** (toute archi) | ✅ | ✅ | Natif — lancez‑le, c'est tout |
| **Windows 10 / 11** | ✅ (Python natif) | ✅ | **WSL2 + Kali**, Docker, ou une VM |
| **macOS** (Apple Silicon / Intel) | ✅ (Python natif) | ✅ | **Docker**, ou une VM Kali (UTM/VirtualBox/VMware) |
| **Ubuntu / Debian / Mint** | ✅ | ✅ | Natif (apt) — la plupart s'installent directement |
| **Arch / BlackArch / Manjaro** | ✅ | ✅ | Natif — `pacman` s'adapte tout seul |
| **Fedora / RHEL / openSUSE** | ✅ | ✅ (la plupart) | Natif, ou Docker pour la parité |
| **Android** (tél. / tablette) | ✅ (Termux) | ✅ | **Kali NetHunter**, ou Termux |
| **Raspberry Pi / carte ARM** | ✅ | ✅ | Image Kali ARM, ou Docker (arm64) |
| **Chromebook** | ✅ | ✅ | Conteneur Linux (Crostini), ou Docker |
| **Cloud / VPS** | ✅ | ✅ | N'importe quel droplet Debian/Kali + SSH |
| **iOS / iPadOS** | ✅ (a‑Shell/iSH, limité) | ⚠️ | Via SSH vers une machine Kali distante |

✅ = fonctionne · ⚠️ = limité (navigation seule ; lancez les outils sur un Linux distant)

---

## Prérequis (toutes plateformes)

- **Python 3.10+** (`python3 --version`)
- **git** (pour les outils installés depuis les sources)
- Une **connexion internet** au premier lancement (pour récupérer le catalogue complet)
- Pour installer/lancer les outils : un userland **Linux** (natif, WSL2, VM, Docker, Termux ou distant)

Installer puis lancer, dans n'importe quel shell Linux/WSL/macOS :

```bash
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security
chmod +x install.sh && ./install.sh
python3 neoz.py
```

---

## Docker — la méthode universelle

Fonctionne à l'identique sur **Windows, macOS, Linux, ARM/Apple Silicon, Raspberry Pi et le cloud**. L'image est basée sur Kali : l'installation des outils marche quel que soit l'hôte.

```bash
# 1. Récupérer le code
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security

# 2. Construire une fois
docker build -t iw7x .

# 3. Lancer l'arsenal interactif
docker run -it --rm iw7x

# …ou installer & lancer un outil directement
docker run -it --rm iw7x nmap
```

Avec Compose : `docker compose run --rm iw7x` (un volume nommé conserve vos outils installés entre les sessions).

> Installer Docker : **Docker Desktop** sur Windows/macOS, ou `curl -fsSL https://get.docker.com | sh` sur Linux.

---

## Windows

**Option A — WSL2 + Kali (recommandé, vitesse native).** Dans un PowerShell **Administrateur** :

```powershell
wsl --install
wsl --install -d kali-linux
```

Redémarrez si demandé, ouvrez **Kali** depuis le menu Démarrer, créez votre utilisateur, puis :

```bash
sudo apt update && sudo apt -y full-upgrade
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security && chmod +x install.sh && ./install.sh && python3 neoz.py
```

**Option B — Docker Desktop.** Voir [Docker](#docker--la-méthode-universelle).

**Option C — Machine virtuelle.** Importez l'image officielle Kali VirtualBox/VMware : <https://www.kali.org/get-kali/#kali-virtual-machines>.

**Option D — Python natif (navigation seule).** Installez Python depuis python.org, puis `python neoz.py` — vous pouvez parcourir et chercher les 30 000+ outils ; l'installation/lancement nécessite A–C.

---

## macOS (Apple Silicon & Intel)

**Option A — Docker Desktop (recommandé).** Voir [Docker](#docker--la-méthode-universelle). L'image Kali tourne nativement sur Apple Silicon (arm64) et Intel (amd64).

**Option B — VM Kali.** Utilisez **UTM** (gratuit, idéal Apple Silicon) ou VirtualBox/VMware avec l'image Kali ARM64 ou Intel depuis les [téléchargements Kali](https://www.kali.org/get-kali/#kali-virtual-machines).

**Option C — Natif (navigation seule).** macOS fournit Python 3 ; `python3 neoz.py` parcourt le catalogue. Homebrew installe *certains* outils, mais pour la parité complète utilisez Docker ou une VM.

---

## Linux

**Kali** — le terrain de jeu naturel. Clonez, `./install.sh`, `python3 neoz.py`. Tout fonctionne.

**Ubuntu / Debian / Mint** — la plupart des outils s'installent directement (`apt`/`pipx`/`go`) :

```bash
sudo apt update && sudo apt install -y git python3 python3-pip pipx golang-go
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security && ./install.sh && python3 neoz.py
```

**Arch / BlackArch / Manjaro** — iw7x réécrit `pacman` ↔ `apt` dans les deux sens, donc les outils issus de BlackArch s'installent proprement.

**Fedora / RHEL / openSUSE** — l'app Python et la plupart des outils `pipx`/`go`/`git` fonctionnent ; pour les quelques‑uns qui supposent un empaquetage Debian, utilisez Docker pour la parité complète.

> iw7x détecte votre distribution et adapte automatiquement les commandes du gestionnaire de paquets (`system.adapt_command`) : un seul catalogue marche sur toutes les distros.

---

## Android (téléphone & tablette)

**Option A — Kali NetHunter (puissance complète).** Installez NetHunter (rooté ou le chroot NetHunter sans root) depuis <https://www.kali.org/get-kali/#kali-mobile>, ouvrez le shell Kali, puis clonez et lancez iw7x exactement comme sur un Kali de bureau.

**Option B — Termux.** Installez [Termux](https://f-droid.org/en/packages/com.termux/) (depuis F‑Droid), puis :

```bash
pkg update && pkg install -y git python
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security && python neoz.py
```

La navigation/recherche marchent très bien ; beaucoup d'outils Python et Go s'installent aussi. Pour ceux qui exigent l'empaquetage Kali complet, utilisez NetHunter ou une machine distante.

---

## Raspberry Pi & cartes ARM

Flashez l'**image Kali ARM** de votre carte depuis <https://www.kali.org/get-kali/#kali-arm>, démarrez, puis clonez et lancez iw7x. Sur tout Pi/SBC qui fait tourner Docker, l'image arm64 (voir [Docker](#docker--la-méthode-universelle)) est la voie la plus rapide.

---

## Cloud / VPS

Créez un droplet Debian ou Kali (DigitalOcean, Hetzner, AWS, Azure…), connectez‑vous en SSH, et lancez l'[installation standard](#prérequis-toutes-plateformes). Idéal pour les longs scans et un usage permanent, accessible depuis n'importe quel appareil — y compris iOS/iPadOS en SSH.

---

## iOS / iPadOS

Le sandbox d'Apple empêche d'installer localement des outils de sécurité Linux. Utilisez une app terminal (**a‑Shell**, **iSH**, **Blink**) pour vous **connecter en SSH à une machine Kali, un VPS ou un ordinateur** qui fait tourner iw7x — vous obtenez l'expérience complète à distance depuis votre iPhone/iPad.

---

## Dépannage

| Symptôme | Solution |
|---|---|
| `python : commande introuvable` | Utilisez `python3` (et `pip3`). Sur Windows natif, installez Python depuis python.org en cochant *Add to PATH*. |
| `externally-managed-environment` (pip) | Debian/Kali récents : `pip3 install --break-system-packages -r requirements.txt`, ou utilisez `pipx`. L'image Docker gère déjà ça. |
| « Cette action nécessite Kali Linux » à l'installation | Vous naviguez sur un hôte non‑Kali. Installez/lancez depuis WSL2, une VM, Docker ou un Kali distant. |
| Un outil refuse de s'installer sur ma distro | Utilisez Docker pour la parité Kali, ou ouvrez le GitHub de l'outil (affiché dans son écran) et clonez manuellement. |
| Les couleurs/traits s'affichent mal | Utilisez un terminal UTF‑8 truecolor (Windows Terminal, iTerm2, la plupart des terminaux Linux). |
| Le premier lancement est lent | Il récupère le catalogue complet une fois ; les lancements suivants sont instantanés. Ignorez avec `IW7X_NO_UPDATE=1`. |

---

## FAQ

**Ça marche sans Kali ?** Oui — navigation/recherche partout. Installer/lancer les outils nécessite un userland Linux (Kali), fourni par Docker/WSL2/VM/Termux/cloud.

**Windows/macOS sont‑ils pleinement supportés ?** L'app tourne nativement pour la navigation. Pour installer+lancer, Docker (tous OS) ou WSL2 (Windows) donnent la puissance complète sans surcoût de VM.

**ARM / Apple Silicon / Raspberry Pi ?** Oui — l'image Kali de base et les builds Kali ARM sont multi‑architectures.

**Faut‑il être root ?** Seulement certains outils (iw7x vous le dit). Docker et Kali tournent en root par défaut ; ailleurs, utilisez `sudo` quand c'est demandé.

---

<div align="center">

**[⬅ Retour au README](README.fr.md)** &nbsp;·&nbsp; **[▶ Voir la démo](https://claude.ai/code/artifact/5210489a-74c0-4eb2-a04f-f33aa3080b3b)** &nbsp;·&nbsp; [github.com/isneoz1/iw7x-cyber-security](https://github.com/isneoz1/iw7x-cyber-security)

</div>
