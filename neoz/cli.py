"""Terminal CLI for iw7x — use any tool straight from the shell.

    iw7x                     launch the interactive menu
    iw7x <tool>              install (if needed) and run a tool by name
    iw7x run <tool>          run a tool (install first if missing)
    iw7x install <tool>      install a tool
    iw7x uninstall <tool>    remove a tool
    iw7x search <query>      list matching tools
    iw7x list [category]     list categories, or tools in a category
    iw7x bundle <name>       install a whole kit for a job (web, ad, osint, …)
    iw7x bundles             list every task bundle
    iw7x --update            fetch every tool from online sources, then exit
    iw7x --watch [minutes]   live auto-scan: keep adding new tools
    iw7x --no-update         launch without the startup scan
    iw7x --help              show this help

Everything is wrapped so a bad tool name, missing binary or offline state
produces a clear message — never a traceback.
"""

from __future__ import annotations

import os
import sys


# ── Tool resolution ─────────────────────────────────────────────────────────────

def _maybe_autoscan() -> None:
    """On first terminal use, fetch the full catalog so every tool is available.
    Runs at most once (skips when already populated, offline, or disabled)."""
    try:
        import os as _os
        from . import config
        from .models import load_catalog, tag_index
        if _os.environ.get("IW7X_NO_UPDATE") == "1" or not config.get("auto_update", True):
            return
        if load_catalog().tool_count >= 2000:
            return   # already scanned/populated
        from . import updater
        if not updater.online():
            return
        _print("First run — fetching the full tool catalog (BlackArch, Kali, awesome)...")
        added, total, _ = updater.update_catalog()
        load_catalog.cache_clear()
        tag_index.cache_clear()
        if added:
            _print(f"Catalog ready: {total} tools available.")
    except Exception:
        pass   # never block a CLI command on the scan


def _all_tools():
    from .models import all_tools
    return all_tools()


def _resolve(name: str):
    """Return (tool, category) for an exact/unique match, or (None, suggestions)."""
    q = name.strip().lower()
    if not q:
        return None, []
    pairs = _all_tools()
    exact = [(t, c) for t, c in pairs if t.title.strip().lower() == q]
    if exact:
        return exact[0], []
    starts = [(t, c) for t, c in pairs if t.title.lower().startswith(q)]
    if len(starts) == 1:
        return starts[0], []
    contains = [(t, c) for t, c in pairs if q in t.title.lower()]
    if len(contains) == 1:
        return contains[0], []
    return None, (starts or contains)[:20]


# ── Actions ─────────────────────────────────────────────────────────────────────

def _print(msg: str) -> None:
    print(f"[iw7x] {msg}")


def _suggest(name: str, suggestions) -> None:
    if suggestions:
        _print(f"No exact match for '{name}'. Did you mean:")
        for t, c in suggestions:
            print(f"    - {t.title}   ({c.title})")
    else:
        _print(f"No tool found matching '{name}'.")
        _print("Tip: run 'iw7x --update' to fetch the full catalog, then retry.")


def _require_kali() -> bool:
    from . import system
    if not system.CURRENT.is_kali:
        _print("iw7x runs tools on Kali Linux only. Boot Kali (or WSL Kali) to use them.")
        return False
    return True


def _launch_tool(tool) -> None:
    """Launch the tool; if no binary is found, show how to run it."""
    from . import system
    _print(f"Launching {tool.title} ...")
    launched = system.launch(tool)
    if not launched:
        cands = system.binary_candidates(tool)
        _print("Installed. Launch it with:  " + (", ".join(cands[:3]) or tool.title))
        if tool.url:
            _print(f"Project page: {tool.url}")


def cli_install(name: str) -> None:
    from . import system
    if not _require_kali():
        return
    tool, sugg = _resolve(name)
    if not tool:
        _suggest(name, sugg)
        return
    t, _ = tool
    if not t.install:
        _print(f"'{t.title}' has no automatic install. See: {t.url or 'n/a'}")
        return
    _print(f"Installing {t.title} ...")
    system.run_commands(list(t.install))
    _launch_tool(t)   # auto-launch straight after install


def cli_run(name: str) -> None:
    from . import system
    if not _require_kali():
        return
    tool, sugg = _resolve(name)
    if not tool:
        _suggest(name, sugg)
        return
    t, _ = tool
    if not system.is_installed(t) and t.install:
        _print(f"{t.title} not installed — installing first ...")
        system.run_commands(list(t.install))
    _launch_tool(t)


def cli_uninstall(name: str) -> None:
    from . import system
    if not _require_kali():
        return
    tool, sugg = _resolve(name)
    if not tool:
        _suggest(name, sugg)
        return
    t, _ = tool
    for cmd in (t.uninstall or []):
        system.run_shell(cmd)
    for cmd in t.install:
        if "pacman -S" in cmd:
            system.run_shell(cmd.replace("pacman -S", "pacman -Rns --noconfirm"))
        elif "apt install" in cmd:
            system.run_shell(cmd.replace("apt install -y", "apt remove -y").replace("apt install", "apt remove"))
        elif "pipx install" in cmd:
            system.run_shell(cmd.replace("pipx install", "pipx uninstall"))
    _print(f"Removed {t.title} (best effort).")


def cli_search(query: str) -> None:
    from .models import search
    query = query.strip()
    if not query:
        _print("Usage: iw7x search <query>")
        return
    results = search(query)
    if not results:
        _print(f"No tool matches '{query}'.")
        return
    _print(f"{len(results)} match(es) for '{query}':")
    for t, c in results[:60]:
        print(f"    {t.title:<32} {c.title:<22} {t.short_description()[:50]}")
    if len(results) > 60:
        print(f"    … and {len(results) - 60} more")


def cli_list(args: list[str]) -> None:
    from .models import load_catalog
    cats = load_catalog().categories
    if not args:
        _print("Categories:")
        for i, c in enumerate(cats, 1):
            print(f"    {i:>2}  {c.title:<26} ({len(c.tools)} tools)")
        _print("Use: iw7x list <category name>")
        return
    q = " ".join(args).lower()
    cat = next((c for c in cats if q in c.title.lower()), None)
    if not cat:
        _print(f"No category matching '{q}'.")
        return
    _print(f"{cat.title} — {len(cat.tools)} tools:")
    for t in cat.tools:
        print(f"    {t.title:<32} {t.short_description()[:56]}")


def cli_update() -> None:
    from .updater import update_catalog
    _print("Scanning online sources (BlackArch, Kali, awesome-lists) for all tools...")
    _, _, msg = update_catalog()
    _print(msg)


def cli_watch(rest: list[str]) -> None:
    from .updater import watch
    minutes = 60.0
    for a in rest:
        if a.replace(".", "", 1).isdigit():
            minutes = float(a)
    try:
        watch(minutes)
    except KeyboardInterrupt:
        _print("Auto-scan stopped.")


def cli_bundles() -> None:
    from . import bundles
    _print("Task bundles — install a whole kit for a job in one command:")
    for name, b in bundles.ALL.items():
        print(f"    {name:<11} {b['title']:<28} ({len(b['tools'])} tools)")
    _print("Use: iw7x bundle <name>   (e.g. iw7x bundle web)")


def cli_bundle(args: list[str]) -> None:
    from . import system, bundles
    if not args:
        cli_bundles()
        return
    name = args[0].strip().lower()
    b = bundles.get(name)
    if not b:
        _print(f"No bundle named '{name}'.")
        cli_bundles()
        return
    if not _require_kali():
        return
    _print(f"Installing bundle '{b['title']}' — {len(b['tools'])} tools. This can take a while ...")
    installed = skipped = 0
    for want in b["tools"]:
        tool, _sugg = _resolve(want)
        if not tool:
            _print(f"  skip (not found): {want}")
            skipped += 1
            continue
        t, _ = tool
        if not t.install:
            _print(f"  skip (no auto-install): {t.title}")
            skipped += 1
            continue
        _print(f"  → {t.title}")
        try:
            system.run_commands(list(t.install))
            installed += 1
        except Exception as exc:
            _print(f"    failed: {exc}")
            skipped += 1
    _print(f"Bundle '{name}' done — {installed} installed, {skipped} skipped.")


def print_usage() -> None:
    print(__doc__.strip())


# ── Entry point ─────────────────────────────────────────────────────────────────

def _launch_menu() -> None:
    from .app import run
    try:
        run()
    except KeyboardInterrupt:
        print("\n[iw7x] Bye.")


def run_entry(argv: list[str]) -> None:
    """Single entry used by iw7x.py and neoz.py. Never raises."""
    try:
        args = argv[1:]
        if not args:
            _launch_menu()
            return
        cmd = args[0].lower()
        if cmd in ("-h", "--help", "help"):
            print_usage()
        elif cmd == "--update":
            cli_update()
        elif cmd == "--watch":
            cli_watch(args[1:])
        elif cmd == "--no-update":
            os.environ["IW7X_NO_UPDATE"] = "1"
            _launch_menu()
        elif cmd in ("search", "find"):
            _maybe_autoscan()
            cli_search(" ".join(args[1:]))
        elif cmd in ("list", "ls", "categories"):
            _maybe_autoscan()
            cli_list(args[1:])
        elif cmd == "install":
            _maybe_autoscan()
            cli_install(" ".join(args[1:]))
        elif cmd in ("bundle", "kit"):
            _maybe_autoscan()
            cli_bundle(args[1:])
        elif cmd in ("bundles", "kits"):
            cli_bundles()
        elif cmd == "uninstall":
            cli_uninstall(" ".join(args[1:]))
        elif cmd in ("run", "launch", "start", "use"):
            _maybe_autoscan()
            cli_run(" ".join(args[1:]))
        else:
            # Bare tool name: install (if needed) and run it.
            _maybe_autoscan()
            cli_run(" ".join(args))
    except KeyboardInterrupt:
        print("\n[iw7x] Interrupted.")
    except Exception as exc:
        print(f"[iw7x] Error: {exc}")
