<div align="center">

<h1>⚡ iw7x</h1>

### Tous les outils de cybersécurité du monde. Un terminal. Une commande.

**iw7x** réunit **plus de 10 000** outils de sécurité offensive et défensive — de Nmap à BloodHound, de Metasploit à Volatility — dans un seul arsenal en ligne de commande, qui installe, met à jour et lance n'importe quel outil à votre place.

<br/>

[![Étoiles](https://img.shields.io/github/stars/isneoz1/iw7x-cyber-security?style=for-the-badge&color=FF47B3&labelColor=1a1a2e&logo=github)](https://github.com/isneoz1/iw7x-cyber-security/stargazers)
[![Forks](https://img.shields.io/github/forks/isneoz1/iw7x-cyber-security?style=for-the-badge&color=9652FF&labelColor=1a1a2e&logo=github)](https://github.com/isneoz1/iw7x-cyber-security/network/members)
[![Issues](https://img.shields.io/github/issues/isneoz1/iw7x-cyber-security?style=for-the-badge&color=48DCFF&labelColor=1a1a2e&logo=github)](https://github.com/isneoz1/iw7x-cyber-security/issues)
[![Licence](https://img.shields.io/badge/Licence-MIT-4AE3A8?style=for-the-badge&labelColor=1a1a2e)](LICENSE)

[![Outils](https://img.shields.io/badge/Outils-10%2C000%2B-FF47B3?style=for-the-badge&labelColor=1a1a2e)](catalog.json)
[![Catégories](https://img.shields.io/badge/Cat%C3%A9gories-44-9652FF?style=for-the-badge&labelColor=1a1a2e)](#-larsenal)
[![Python](https://img.shields.io/badge/Python-3.10%2B-48DCFF?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e)](https://www.python.org/)
[![Kali](https://img.shields.io/badge/Kali%20Linux-Pr%C3%AAt-4AE3A8?style=for-the-badge&logo=kalilinux&logoColor=white&labelColor=1a1a2e)](https://www.kali.org/)

**🌍 [English](README.md) · [Français](README.fr.md)**

<br/>

<img src="assets/iw7x-preview.svg" alt="iw7x — arsenal cybersécurité : 10 506 outils dans 44 catégories, par NeoZ" width="820">

</div>

> ⚠️ **Réservé aux tests de sécurité autorisés et à l'éducation.** Lisez la section [Cadre légal & éthique](#-cadre-légal--éthique) avant de commencer.

---

## ✨ Pourquoi iw7x ?

Les professionnels de la sécurité perdent des heures à chercher le bon outil, cloner des dépôts, réparer des dépendances et retrouver les commandes d'installation. **iw7x remplace tout ça par un seul programme.**

| | |
|---|---|
| 🗂️ **Tout l'écosystème** | **10 000+ outils** répartis en **44 catégories** — OSINT, web, wireless, exploitation, forensic, reverse, crypto, cloud, AD, mobile, IoT, threat‑intel, blue team, et plus. |
| ⚙️ **Installe & lance pour vous** | Choisissez un outil → iw7x l'installe (apt / pipx / go / git) et le lance. Fini le copier‑coller de commandes. |
| 🔄 **Toujours à jour** | Un scanner intégré récupère les nouveaux outils depuis **BlackArch, Kali & awesome‑lists** — votre arsenal grandit tout seul. |
| 🔎 **Trouvez tout, tout de suite** | Recherche plein‑texte, filtres par tag (`osint`, `c2`, `web`…) et un **conseiller** qui recommande des outils selon votre objectif. |
| 🎨 **Un terminal qu'on aime** | Une superbe interface [rich](https://github.com/Textualize/rich) avec en‑tête système en direct, dégradés et menus épurés. |
| 🧩 **Data‑driven & hackable** | Chaque outil est une entrée JSON — aucune classe spaghetti. Ajouter un outil = une PR de 6 lignes. |
| 🚫 **Ne plante jamais** | Mauvais nom, binaire manquant, hors ligne ? Un message clair, jamais un traceback. |

---

## 🚀 Démarrage rapide

> **OS recommandé :** [Kali Linux](https://www.kali.org/) (ou Kali sur WSL2). iw7x exécute les outils sur Kali ; le menu, la recherche et le catalogue fonctionnent partout.

```bash
# 1. Cloner
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security

# 2. Installer les dépendances (git, python, pipx, go…)
chmod +x install.sh && ./install.sh

# 3. Lancer l'arsenal
python3 neoz.py
```

C'est tout. Au premier lancement, iw7x récupère le catalogue complet : chaque outil est à une touche de distance.

<details>
<summary><b>⚡ Installation en une ligne</b></summary>

```bash
git clone https://github.com/isneoz1/iw7x-cyber-security.git && cd iw7x-cyber-security && ./install.sh && python3 neoz.py
```
</details>

---

## 🎮 Utilisation

### Menu interactif

```bash
python3 neoz.py            # ou : python3 iw7x.py
```

Dans le menu :

| Touche | Action |
|--------|--------|
| `1–N` | Ouvrir une catégorie |
| `/requête` | Chercher un outil par nom / mot‑clé |
| `T` | Filtrer par tag (`osint`, `web`, `c2`, `wireless`…) |
| `R` | **Conseiller** — « Que voulez‑vous faire ? » → outils recommandés |
| `U` | Mise à jour : récupérer les nouveaux outils en ligne |
| `?` | Aide · `Q` Quitter |

### Depuis le shell (sans menu)

```bash
python3 neoz.py nmap              # installe (si besoin) et lance un outil
python3 neoz.py search "sql inj"  # liste les outils correspondants
python3 neoz.py list              # liste les 44 catégories
python3 neoz.py list osint        # liste les outils d'une catégorie
python3 neoz.py install bloodhound
python3 neoz.py --update          # récupère tous les outils en ligne
python3 neoz.py --watch 30        # auto‑scan toutes les 30 min
python3 neoz.py --help            # aide complète
```

---

## 🗂️ L'Arsenal

**44 catégories · 10 506 outils** — et ça grandit tout seul à chaque `--update`.

| Catégorie | Outils | Catégorie | Outils |
|---|:--:|---|:--:|
| 🧰 Autres outils / OSINT | 1512 | 🐝 Fuzzing | 75 |
| 🌐 Web Attack | 1511 | 🎣 Phishing | 60 |
| 🔍 Information Gathering | 1310 | 🖼️ Stéganographie | 55 |
| 🕵️ OSINT / Recon | 1282 | 🎛️ Post‑Exploitation / C2 | 49 |
| 🔬 Forensic / DFIR | 689 | 🚗 Automobile / CAN | 49 |
| 🧠 Reverse Engineering | 504 | 🎭 Ingénierie sociale | 46 |
| 🛡️ Blue Team / Défense | 408 | 💣 DDoS / Stress Test | 44 |
| 📶 Sniffing & MITM réseau | 369 | 📦 Container / Kubernetes | 37 |
| 🔌 IoT / Firmware / Hardware | 229 | ☁️ Sécurité Cloud | 32 |
| 🔐 Cryptographie / Chiffrement | 225 | 📻 Radio / SDR / RF | 31 |
| 🔑 Wordlists / Mots de passe | 213 | ♻️ DevSecOps / SAST‑DAST | 28 |
| 🏰 Active Directory | 203 | ⛓️ Blockchain / Web3 | 26 |
| 🧬 Analyse de malware | 199 | 💉 Injection SQL | 21 |
| 💥 Frameworks d'exploit | 198 | ☎️ Sécurité VoIP | 18 |
| 🔗 Sécurité API | 167 | 🩹 Attaques XSS | 14 |
| 🧨 Binary Exploitation / CTF | 148 | 🥷 Anonymat / Dissimulation | 13 |
| 📱 Sécurité mobile | 130 | 🚪 Sécurité physique / RFID | 13 |
| 📡 Attaques Wireless | 125 | 🖥️ Remote Admin (RAT) | 11 |
| ⏫ Élévation de privilèges | 125 | 🛰️ Satellite / GNSS / Spatial | 9 |
| 🔭 Renseignement / Threat Intel | 114 | 🤖 Sécurité IA / ML | 9 |
| 🎯 Création de payloads | 105 | 🏭 ICS / SCADA / OT | 8 |
| 🩻 Scan de vulnérabilités | 90 | 🔁 Mise à jour / Désinstall. | — |

---

## 🔄 Un catalogue qui s'agrandit tout seul

iw7x n'est pas une liste figée. Lancez `--update` (ou appuyez sur `U`) : il scanne **BlackArch**, **Kali** et les **awesome‑lists** de la communauté, déduplique, et ajoute chaque nouvel outil trouvé — commandes d'installation prêtes. L'objectif est simple : **tous les outils de sécurité de la planète, toujours à jour, au même endroit.**

---

## 🤝 Contribuer

**iw7x grandit grâce à des gens comme vous.** Ajouter un outil est la contribution open‑source la plus simple qui soit — un seul objet JSON :

```json
{
  "title": "Subfinder",
  "description": "Énumération passive et rapide de sous-domaines.",
  "install": ["go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"],
  "run": ["subfinder -d example.com"],
  "url": "https://github.com/projectdiscovery/subfinder",
  "tags": ["osint", "recon"]
}
```

Ajoutez‑le à `catalog.json`, ouvrez une PR — c'est fait. Voir **[CONTRIBUTING.md](CONTRIBUTING.md)**, ou [demandez simplement un outil](https://github.com/isneoz1/iw7x-cyber-security/issues/new/choose) et on l'ajoute.

⭐ **Mettez une étoile** pour aider d'autres hackers à découvrir le projet — c'est le geste le plus utile pour le faire grandir.

---

## ⚖️ Cadre légal & éthique

iw7x est un framework de **test d'intrusion** et **d'éducation à la sécurité**, destiné **exclusivement** à :

- 🎯 Les systèmes que vous **possédez** ou pour lesquels vous avez une **autorisation écrite explicite**
- 🎓 L'apprentissage, les CTF, les labs et les engagements red‑team autorisés
- 🛡️ La recherche défensive et le travail blue‑team

**L'accès non autorisé à des systèmes informatiques est illégal.** Vous êtes seul responsable de vos actes et du respect des lois applicables. Les auteurs et contributeurs déclinent **toute responsabilité** en cas de mauvais usage ou de dommage. Si vous n'avez pas l'autorisation — **arrêtez‑vous.**

---

## 📜 Licence

Distribué sous [licence MIT](LICENSE). Les outils fournis via le catalogue restent sous **leurs propres** licences respectives.

---

<div align="center">

**Créé avec 💜 par [NeoZ](https://github.com/isneoz1)** — *l'attaque éclaire la défense.*

<sub>Plus vous devenez silencieux, plus vous entendez.</sub>

</div>
