# Security Policy

## Reporting a vulnerability

iw7x is a security tool, so we take the security of the framework itself seriously.

If you find a vulnerability **in iw7x's own code** (not in a bundled third‑party tool):

1. **Do not** open a public issue.
2. Report it privately via [GitHub Security Advisories](https://github.com/isneoz1/iw7x-cyber-security/security/advisories/new), or open a minimal issue asking a maintainer to contact you.
3. Include: affected version, reproduction steps, and impact.

We aim to acknowledge reports within **72 hours** and to ship a fix as fast as reasonably possible. Credit is given to reporters unless you prefer to remain anonymous.

## Scope

| In scope | Out of scope |
|---|---|
| Bugs in the iw7x engine (`neoz/*`, `catalog.json` handling, installer) | Vulnerabilities in the third‑party tools iw7x installs — report those upstream |
| Command injection / unsafe execution in iw7x itself | Findings that require the user to run explicitly malicious catalog entries |
| Supply‑chain issues in iw7x dependencies | General questions (use Discussions) |

## Responsible use

iw7x installs and runs offensive security tools. It is intended **only** for authorized testing and education. Using it against systems you do not own or have written permission to test is illegal and unsupported. See the disclaimer in the [README](README.md#-legal--ethical-use).
