#!/usr/bin/env python3
"""Render an AUTHENTIC preview of the real iw7x header to an SVG.

This is not a mockup: it calls the same ``ui.render_header`` the program uses,
captured with ``rich``'s SVG exporter, so the README hero always matches the
actual terminal. The current OS is faked to Kali so the banner shows the green
"KALI LINUX DETECTED — READY" line as users see it on Kali.

Run:  python scripts/make_preview.py   ->  assets/iw7x-preview.svg
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console  # noqa: E402

from neoz import ui, system  # noqa: E402
from neoz.models import load_catalog  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "assets" / "iw7x-preview.svg"


def main() -> None:
    # Pretend we're on Kali so the readiness line renders green.
    kali = system.OSInfo(system="linux", distro_id="kali", distro_like="debian",
                         version="2026.1", pkg_manager="apt-get", is_root=True,
                         is_wsl=False, arch="x86_64")
    ui.CURRENT = kali

    rec = Console(record=True, file=io.StringIO(), width=92, theme=ui.THEME)
    ui.console = rec
    ui.render_header(load_catalog())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    rec.save_svg(str(OUT), title="kali@kali: ~ $ python3 neoz.py")
    print(f"wrote {OUT}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
