# Changelog

All notable changes to **iw7x** are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions track `neoz/__init__.py`.

## [1.7.0] — 2026-07-05

### Added
- **6 new categories**: Cryptography / Encryption, API Security, Privilege
  Escalation, Threat Intelligence, DevSecOps / SAST-DAST, Physical / RFID / Badge.
- New catalog sources: awesome-cryptography, awesome-api-security,
  awesome-python-security, the-book-of-secret-knowledge.
- Authentic terminal preview (`assets/iw7x-preview.svg`) in the README hero.

### Changed
- Catalog grew to **10,506 tools across 44 categories**.
- `crypto` tool group now routes to the dedicated Cryptography category.
- Refreshed counts and category tables in `README.md`, `README.fr.md`, `ARSENAL.md`.

## [1.6.0] — 2026-07-05

### Added
- **14 new tool sources** wired into the auto-updater (biggest: cipher387's
  OSINT tool collection, awesome-privacy, privilege-escalation, cloud-security,
  anti-forensic, command-and-control, reversing, web-hacking, bluetooth, mobile,
  IoT, Kubernetes).

### Changed
- Catalog grew from **8,104 → 10,068 tools** across 38 categories.

## [1.5.0] — 2026-07-05

### Added
- World-class GitHub presentation: bilingual README (EN/FR), badges, arsenal
  tables, `ARSENAL.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  MIT `LICENSE`, issue/PR templates and a CI workflow.
- Data-driven engine: one catalog (`catalog.json`) drives the whole TUI + CLI.
- Auto-updater scanning BlackArch, Kali and dozens of awesome-lists.
- Interactive `rich` TUI with gradient banner, search, tag filters and a task advisor.
- Shell CLI: `iw7x <tool>` installs (if needed) and runs any tool.

[1.7.0]: https://github.com/isneoz1/iw7x-cyber-security/releases
[1.6.0]: https://github.com/isneoz1/iw7x-cyber-security/releases
[1.5.0]: https://github.com/isneoz1/iw7x-cyber-security/releases
