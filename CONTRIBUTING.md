# Contributing to iw7x

First off — **thank you.** iw7x aims to be the single most complete cybersecurity arsenal on Earth, and it only gets there because people like you add the tools they love. Every contribution, big or small, matters.

There are three easy ways to help:

1. ⭐ **Star the repo** — it's free and it genuinely helps others discover the project.
2. 🧩 **Add a tool** — the most valuable contribution (see below).
3. 🐛 **Report a bug or request a tool** — [open an issue](https://github.com/isneoz1/iw7x-cyber-security/issues/new/choose).

---

## 🧩 Adding a tool (the 5‑minute PR)

Every tool in iw7x is a single JSON object in [`catalog.json`](catalog.json). No Python required.

### 1. Find the right category

Open `catalog.json` and locate the category (`id`) that fits — e.g. `information_gathering`, `web_attack`, `active_directory`, `osint`, `forensics`, `reverse_engineering`, `wireless_attack`, `post_exploitation`, …

### 2. Add your tool object

```json
{
  "title": "Subfinder",
  "description": "Fast passive subdomain enumeration.",
  "install": ["go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"],
  "run": ["subfinder -d example.com"],
  "url": "https://github.com/projectdiscovery/subfinder",
  "tags": ["osint", "recon"],
  "os": ["linux", "macos"],
  "requires_root": false
}
```

| Field | Required | Notes |
|-------|:--:|-------|
| `title` | ✅ | Display name, unique within the catalog. |
| `description` | ✅ | One clear sentence. What does it do? |
| `install` | ✅ | List of shell commands (`apt`, `pipx`, `go install`, `git clone`…). |
| `run` | ⬜ | Example run command(s). |
| `url` | ✅ | Official project page / repo. |
| `tags` | ⬜ | Lowercase tags: `osint`, `web`, `c2`, `wireless`, `credentials`… |
| `os` | ⬜ | Defaults to `["linux", "macos"]`. |
| `requires_root` | ⬜ | `true` if it needs root. |

### 3. Validate & open a PR

```bash
python3 -c "import json; json.load(open('catalog.json', encoding='utf-8')); print('catalog OK')"
python3 neoz.py search "Subfinder"    # confirm it shows up
```

Then open a pull request. That's it. 🎉

> Prefer not to touch JSON? Just [request the tool](https://github.com/isneoz1/iw7x-cyber-security/issues/new/choose) and a maintainer will add it.

---

## 🛠️ Code contributions

The engine is intentionally small and data‑driven. Structure:

```
neoz/
├── app.py        # interactive menu flow
├── cli.py        # shell command dispatch
├── models.py     # Tool / Category dataclasses + search/tags
├── system.py     # install / run / OS detection
├── ui.py         # rich rendering (banner, menus)
├── updater.py    # online catalog scanner
└── i18n.py       # UI strings
```

### Setup

```bash
git clone https://github.com/isneoz1/iw7x-cyber-security.git
cd iw7x-cyber-security
python3 -m pip install -r requirements.txt
python3 neoz.py
```

### Guidelines

- **Python 3.10+**, type hints on function signatures, PEP 8.
- Keep files focused and small; prefer many small modules over large ones.
- The catalog is the source of truth — **don't hand‑write tool logic**, add JSON.
- Handle errors gracefully: the CLI must never show a raw traceback to a user.
- Run a quick smoke test before pushing:
  ```bash
  python3 -c "import neoz.cli, neoz.models, neoz.system, neoz.ui"
  python3 neoz.py --help
  ```

### Commit style

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.

---

## 💬 Community

- **Ideas / feature votes:** [Discussions](https://github.com/isneoz1/iw7x-cyber-security/discussions)
- **Bugs & tool requests:** [Issues](https://github.com/isneoz1/iw7x-cyber-security/issues)
- Be kind. See our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## ⚖️ Ethics reminder

By contributing you agree that iw7x is for **authorized security testing and education only**. Don't submit malware, tools whose *only* purpose is unlawful harm, or anything designed purely to evade detection for malicious ends.

Thanks for making iw7x better for the whole security community. 💜
