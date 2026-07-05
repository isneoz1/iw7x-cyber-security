#!/usr/bin/env python3
"""
iw7x — cybersecurity arsenal (English). Created by NeoZ.
For authorized security testing and education only.

Launch:
    python3 neoz.py            (or: python3 iw7x.py)
    python3 neoz.py <tool>     install (if needed) and run a tool
    python3 neoz.py --help     full CLI help
"""

import sys

if sys.version_info < (3, 10):
    sys.exit(
        f"[iw7x] Python 3.10+ required — you have "
        f"{sys.version_info.major}.{sys.version_info.minor}."
    )

from neoz.cli import run_entry  # noqa: E402


def main() -> None:
    run_entry(sys.argv)


if __name__ == "__main__":
    main()
