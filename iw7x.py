#!/usr/bin/env python3
"""iw7x entry point (same as neoz.py). Created by NeoZ.
For authorized security testing and education only.

    iw7x                     launch the interactive menu
    iw7x <tool>              install (if needed) and run a tool by name
    iw7x run|install <tool>  run / install a specific tool
    iw7x search <query>      list matching tools
    iw7x list [category]     list categories or their tools
    iw7x --update            fetch every tool from online sources
    iw7x --watch [minutes]   live auto-scan (keep adding new tools)
    iw7x --help              full help
"""

import sys

if sys.version_info < (3, 10):
    sys.exit("[iw7x] Python 3.10+ required.")

from neoz.cli import run_entry  # noqa: E402

if __name__ == "__main__":
    run_entry(sys.argv)
