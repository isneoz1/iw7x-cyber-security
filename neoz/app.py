"""Flow control for the NeoZ Toolkit — the interactive menu loops.

Presentation lives in ``ui.py``; execution lives in ``system.py``. This module
only decides *what happens next* based on user input.
"""

from __future__ import annotations

import webbrowser

from rich import box
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from . import config, system, ui
from .i18n import t
from .models import (
    ADVISOR, Catalog, Category, Tool,
    load_catalog, search, tag_index,
)

console = ui.console

# Tools shown per page inside a category (press 90 for the next page).
_PAGE_SIZE = 40


def _pause(msg_key: str = "press_enter") -> None:
    Prompt.ask(f"[dim]{t(msg_key)}[/dim]", default="")


def _ask(prompt: str = "[brand]╰─>[/brand]") -> str:
    return Prompt.ask(prompt, default="").strip()


# ── Tool screen ────────────────────────────────────────────────────────────────

def _confirm_shell() -> bool:
    """Guard shell execution — iw7x runs tools on Kali Linux only."""
    if not system.CURRENT.is_kali:
        console.print(f"[warn]{t('kali_only')}[/warn]")
        return False
    return Confirm.ask(f"[warn]{t('confirm_run')}[/warn]", default=True)


def _launch(tool: Tool) -> None:
    """Launch the tool and, if no binary is found, tell the user how."""
    console.print(f"[brand]{t('launching', name=tool.title)}[/brand]")
    launched = system.launch(tool)
    if not launched:
        cands = system.binary_candidates(tool)
        console.print(f"[dim]{t('launch_hint', bin=', '.join(cands[:3]) or tool.title)}[/dim]")


def _do_install(tool: Tool, autorun: bool = True) -> None:
    if not tool.install:
        console.print(f"[warn]{t('no_update')}[/warn]")
        return
    if not _confirm_shell():
        return
    for cmd in tool.install:
        console.print(f"[warn]→ {cmd}[/warn]")
    ok = system.run_commands(list(tool.install))
    console.print(f"[ok]✔ {t('installed_ok')}[/ok]" if ok
                  else f"[err]{t('install_failed')}[/err]")
    if ok and autorun:
        _launch(tool)   # auto-launch straight after install


def _do_run(tool: Tool) -> None:
    if not _confirm_shell():
        return
    _launch(tool)


def _do_update(tool: Tool) -> None:
    if not system.is_installed(tool):
        console.print(f"[warn]{t('not_installed')}[/warn]")
        return
    console.print(f"[ok]✔ {t('updated_ok')}[/ok]" if system.smart_update(tool)
                  else f"[dim]{t('no_update')}[/dim]")


def _do_uninstall(tool: Tool) -> None:
    if not tool.uninstall and not tool.install:
        console.print(f"[warn]{t('no_uninstall')}[/warn]")
        return
    if not _confirm_shell():
        return
    if tool.uninstall:
        system.run_commands(list(tool.uninstall))
    else:
        # Derive an uninstall command from how the tool was installed.
        for cmd in tool.install:
            if "pacman -S" in cmd:
                system.run_shell(cmd.replace("pacman -S", "pacman -Rns --noconfirm"))
            elif "apt install" in cmd:
                system.run_shell(cmd.replace("apt install -y", "apt remove -y")
                                    .replace("apt install", "apt remove"))
            elif "pipx install" in cmd:
                system.run_shell(cmd.replace("pipx install", "pipx uninstall"))
            elif "pip install" in cmd:
                system.run_shell(cmd.replace("pip install --user", "pip uninstall -y")
                                    .replace("pip install", "pip uninstall -y"))
            elif "git clone" in cmd:
                directory = system.tool_dir(tool)
                if directory:
                    system.run_shell(f'rm -rf "{directory}"')
    console.print(f"[ok]{t('uninstalled_ok')}[/ok]")


def _do_open_folder(tool: Tool) -> None:
    directory = system.tool_dir(tool)
    if directory:
        console.print(f"[ok]{t('opening_folder', dir=directory)}[/ok]")
        console.print(f"[dim]{t('type_exit')}[/dim]")
        system.open_in_shell(directory)
    else:
        console.print(f"[warn]{t('dir_not_found')}[/warn]")
        if tool.url:
            console.print(f"[dim]{t('clone_hint')}[/dim]")
            console.print(f"[cyan]  git clone {tool.url}.git[/cyan]")


def tool_screen(tool: Tool, parent_title: str) -> None:
    # Build the action list dynamically (respect installable/runnable flags).
    actions: list[tuple[str, callable]] = []
    if tool.installable and tool.install:
        actions.append((t("install"), lambda: _do_install(tool)))
    actions.append((t("run"), lambda: _do_run(tool)))
    actions.append((t("update"), lambda: _do_update(tool)))
    if tool.installable and (tool.install or tool.uninstall):
        actions.append((t("uninstall"), lambda: _do_uninstall(tool)))
    actions.append((t("open_folder"), lambda: _do_open_folder(tool)))

    while True:
        ui.clear()
        desc = f"[cyan]{tool.description}[/cyan]"
        if tool.url:
            desc += f"\n[url]{tool.url}[/url]"
        if tool.archived:
            desc += f"\n[arch]! {tool.archived_reason}[/arch]"
        console.print(Panel(
            desc, title=f"[accent]{tool.title}[/accent]",
            border_style="magenta", box=box.DOUBLE,
        ))

        table = Table(title=t("options"), box=box.SIMPLE_HEAVY)
        table.add_column(t("no"), style="brand", justify="center")
        table.add_column(t("action"), style="warn")
        for i, (label, _) in enumerate(actions, start=1):
            table.add_row(str(i), label)
        if tool.url:
            table.add_row("98", t("open_project"))
        table.add_row("99", f"« {parent_title}")
        console.print(table)

        raw = _ask().lower()
        if raw in ("", "99", "q"):
            if raw == "q":
                raise SystemExit(0)
            return
        if raw in ("?", "help"):
            ui.render_help(); _pause(); continue
        if raw == "98" and tool.url:
            webbrowser.open_new_tab(tool.url); continue
        if not raw.isdigit():
            console.print(f"[err]{t('enter_number')}[/err]"); _pause(); continue
        idx = int(raw)
        if 1 <= idx <= len(actions):
            try:
                actions[idx - 1][1]()
            except Exception:
                console.print_exception(show_locals=False)
            _pause()
        else:
            console.print(f"[err]{t('invalid')}[/err]"); _pause()


# ── Category screen ────────────────────────────────────────────────────────────

def _visible_tools(cat: Category) -> tuple[list[Tool], list[Tool], list[Tool]]:
    active, archived, incompatible = [], [], []
    for tool in cat.tools:
        if tool.archived:
            archived.append(tool)
        elif system.CURRENT.system in tool.os or system.CURRENT.system == "windows":
            active.append(tool)   # allow browsing on Windows
        else:
            incompatible.append(tool)
    return active, archived, incompatible


def _archived_screen(cat: Category, archived: list[Tool]) -> None:
    while True:
        ui.clear()
        console.rule(f"[arch]{t('archived_title', title=cat.title)}[/arch]", style="yellow")
        table = Table(box=box.MINIMAL_DOUBLE_HEAD, show_lines=True)
        table.add_column(t("no"), justify="center", style="warn")
        table.add_column(t("tool"), style="arch")
        table.add_column(t("reason"), style="dim white")
        for i, tool in enumerate(archived, start=1):
            table.add_row(str(i), tool.title, tool.archived_reason or t("no_reason"))
        table.add_row("99", t("back"), "")
        console.print(table)
        raw = _ask(f"[warn][?] {t('select')}[/warn]")
        if raw in ("", "99"):
            return
        if raw.isdigit() and 1 <= int(raw) <= len(archived):
            tool_screen(archived[int(raw) - 1], cat.title)


def _install_all(active: list[Tool]) -> None:
    pending = [tl for tl in active if not system.is_installed(tl) and tl.install]
    if not pending:
        return
    console.print(Panel(f"[bold]{t('installing', n=len(pending))}[/bold]",
                        border_style="green", box=box.ROUNDED))
    if not _confirm_shell():
        return
    for i, tool in enumerate(pending, start=1):
        console.print(f"\n[brand]({i}/{len(pending)})[/brand] {tool.title}")
        try:
            system.run_commands(list(tool.install))
        except Exception:
            console.print(f"[err]{t('failed_tool', name=tool.title)}[/err]")
    _pause()


def category_screen(cat: Category) -> None:
    page = 0
    while True:
        ui.clear()
        console.rule(f"[brand]{cat.title.upper()}[/brand]", style="dim cyan")
        active, archived, incompatible = _visible_tools(cat)

        total = len(active)
        total_pages = max(1, -(-total // _PAGE_SIZE))   # ceil division
        page %= total_pages
        start = page * _PAGE_SIZE
        page_tools = active[start:start + _PAGE_SIZE]

        title = t("available_tools")
        if total_pages > 1:
            title = t("page_of", p=page + 1, tp=total_pages, total=total)
        table = Table(title=title, box=box.SIMPLE_HEAD, show_lines=False)
        table.add_column(t("no"), justify="right", style="accent", width=5)
        table.add_column(t("tool"), style="brand", min_width=24)
        table.add_column(t("description"), style="white", overflow="fold")
        for offset, tool in enumerate(page_tools):
            idx = start + offset + 1   # global 1-based index (stable across pages)
            table.add_row(str(idx), ui.tool_cell(tool), tool.short_description())

        pending = [tl for tl in active if not system.is_installed(tl) and tl.install]
        if total_pages > 1:
            table.add_row("89", f"[accent]« {t('prev_page')}[/accent]", "")
            table.add_row("90", f"[accent]{t('next_page')} »[/accent]", "")
        if pending:
            table.add_row("97", f"[ok]{t('install_all', n=len(pending))}[/ok]", "")
        if archived:
            table.add_row("98", f"[arch]{t('archived', n=len(archived))}[/arch]", "")
        table.add_row("99", f"[dim]{t('back_main')}[/dim]", "")
        console.print(table)
        if incompatible:
            console.print(f"[dim]{t('hidden_os', n=len(incompatible), os=system.CURRENT.system)}[/dim]")

        raw = _ask().lower()
        if raw in ("", ):
            continue
        if raw == "q":
            raise SystemExit(0)
        if raw in ("?", "help"):
            ui.render_help(); _pause(); continue
        if raw == "99":
            return
        if raw == "90" and total_pages > 1:
            page += 1; continue
        if raw == "89" and total_pages > 1:
            page -= 1; continue
        if raw == "97" and pending:
            _install_all(active); continue
        if raw == "98" and archived:
            _archived_screen(cat, archived); continue
        if raw.isdigit() and 1 <= int(raw) <= len(active):
            tool_screen(active[int(raw) - 1], cat.title)
        else:
            console.print(f"[err]{t('invalid')}[/err]"); _pause()


# ── Search / tags / advisor ────────────────────────────────────────────────────

def _open_from_results(results: list[tuple[Tool, Category]]) -> None:
    raw = _ask("[brand]>[/brand]").lower()
    if raw in ("", "99"):
        return
    if raw.isdigit() and 1 <= int(raw) <= len(results):
        tool, cat = results[int(raw) - 1]
        tool_screen(tool, cat.title)


def search_screen(query: str | None = None) -> None:
    if query is None:
        query = _ask(f"[brand]/ {t('search_prompt')}[/brand]")
    if not query:
        return
    results = search(query)
    if not results:
        console.print(f"[dim]{t('no_results', q=query)}[/dim]"); _pause(); return
    ui.render_results(t("results_for", q=query), results)
    _open_from_results(results)


def tags_screen() -> None:
    index = tag_index()
    tags = sorted(index)
    console.print(Panel(
        "   ".join(f"[brand]{tg}[/brand]([dim]{len(index[tg])}[/dim])" for tg in tags),
        title=f"[accent] {t('tags_title')} [/accent]",
        border_style="magenta", box=box.ROUNDED, padding=(0, 2),
    ))
    tag = _ask(f"[brand]{t('enter_tag')}[/brand]").lower()
    if not tag:
        return
    if tag not in index:
        console.print(f"[dim]{t('tag_missing', tag=tag)}[/dim]"); _pause(); return
    ui.render_results(t("tagged_with", tag=tag), index[tag])
    _open_from_results(index[tag])


def advisor_screen() -> None:
    tasks = list(ADVISOR)
    table = Table(title=t("advisor_title"), box=box.SIMPLE_HEAD)
    table.add_column(t("no"), justify="center", style="brand", width=5)
    table.add_column(t("task"), style="warn")
    for i, task in enumerate(tasks, start=1):
        table.add_row(str(i), task)
    table.add_row("99", t("back_main"))
    console.print(table)

    raw = _ask("[brand]>[/brand]")
    if not raw.isdigit():
        return
    idx = int(raw)
    if not (1 <= idx <= len(tasks)):
        return
    task = tasks[idx - 1]
    index = tag_index()
    seen, results = set(), []
    for tag in ADVISOR[task]:
        for tool, cat in index.get(tag, []):
            if id(tool) not in seen:
                seen.add(id(tool))
                results.append((tool, cat))
    if not results:
        console.print(f"[dim]{t('advisor_none')}[/dim]"); _pause(); return
    console.print(Panel(f"[bold]{t('advisor_for', task=task)}[/bold]",
                        border_style="green", box=box.ROUNDED))
    ui.render_results(t("advisor_for", task=task), results)
    _open_from_results(results)


# ── Auto-update ────────────────────────────────────────────────────────────────

def _counter_text(n: int) -> "Text":
    from rich.text import Text
    return Text.assemble(
        ("  integrating tools in real time      ", "brand"),
        (f"{n:,}", "ok"),
        ("  tools", "dim"),
    )


def update_screen() -> Catalog | None:
    """Fetch the full online tool catalog and merge it, showing the tool count
    climb live. Returns the reloaded catalog on success, else None. Never raises."""
    from rich.live import Live
    from . import updater
    from .models import load_catalog, tag_index

    if not updater.online():
        console.print(f"[warn]{t('update_offline')}[/warn]")
        _pause()
        return None

    console.print(Panel(f"[warn]{t('updating')}[/warn]",
                        border_style="yellow", box=box.ROUNDED))
    start_total = load_catalog().tool_count
    try:
        with Live(_counter_text(start_total), console=console,
                  refresh_per_second=30, transient=True) as live:
            added, total, msg = updater.update_catalog(
                progress=lambda n: live.update(_counter_text(n)))
    except Exception as exc:
        console.print(f"[err]{exc}[/err]")
        _pause()
        return None

    if added:
        console.print(f"[ok]{t('update_added', n=added, total=total)}[/ok]")
    elif "unreachable" in msg or "offline" in msg:
        console.print(f"[warn]{t('update_offline')}[/warn]")
    else:
        console.print(f"[dim]{t('update_none')}[/dim]")
    _pause()
    load_catalog.cache_clear()
    tag_index.cache_clear()
    return load_catalog()


# ── Main loop ──────────────────────────────────────────────────────────────────

def bundles_screen() -> None:
    """Pick a task bundle and install the whole kit in one go."""
    from rich import box
    from rich.table import Table
    from . import bundles as _b
    from .cli import cli_bundle
    ui.clear()
    names = list(_b.ALL.items())
    table = Table(title="Task bundles — install a whole kit for a job", box=box.SIMPLE_HEAD)
    table.add_column("No.", justify="right", style="accent", width=5)
    table.add_column("Bundle", style="brand", min_width=26)
    table.add_column("Tools", justify="right", style="dim cyan")
    for i, (name, b) in enumerate(names, 1):
        table.add_row(str(i), f"{b['title']}  [dim]({name})[/dim]", str(len(b["tools"])))
    table.add_row("99", "[dim]Back to main menu[/dim]", "")
    console.print(table)
    choice = _ask("[accent]Bundle number[/accent]")
    if not choice or not choice.strip().isdigit():
        return
    n = int(choice.strip())
    if n == 99 or not (1 <= n <= len(names)):
        return
    name = names[n - 1][0]
    console.print(f"[dim]Installing the '{name}' kit — this can take a while...[/dim]")
    cli_bundle([name])   # reuses the tested installer (Kali-guarded, error-wrapped)
    _pause()


def _dispatch(raw: str, catalog: Catalog) -> bool:
    """Return False to quit, True to keep looping."""
    low = raw.lower()
    if low in ("?", "help"):
        ui.render_help(); _pause(); return True
    if low in ("b", "bundle", "bundles", "kit", "kits"):
        bundles_screen(); return True
    if raw.startswith("/"):
        search_screen(raw[1:].strip() or None); return True
    if low in ("s", "search"):
        search_screen(); return True
    if low in ("t", "tag", "tags"):
        tags_screen(); return True
    if low in ("r", "rec", "recommend", "advisor"):
        advisor_screen(); return True
    if low in ("q", "quit", "exit"):
        ui.goodbye(); return False
    if low.isdigit():
        idx = int(low)
        if 1 <= idx <= len(catalog.categories):
            category_screen(catalog.categories[idx - 1])
        else:
            console.print(f"[err]{t('choose_range', n=len(catalog.categories))}[/err]"); _pause()
        return True
    console.print(f"[err]{t('invalid_main')}[/err]"); _pause()
    return True


def _auto_scan_on_launch() -> None:
    """Silently fetch new tools from online sources at startup (if enabled and
    online). Fully error-wrapped so it can never block or crash the launch."""
    import os
    if os.environ.get("IW7X_NO_UPDATE") == "1" or not config.get("auto_update", True):
        return
    try:
        from rich.live import Live
        from . import updater
        from .models import load_catalog as _lc, tag_index as _ti
        if not updater.online():
            return
        console.print(f"[dim]{t('updating')}[/dim]")
        start = _lc().tool_count
        with Live(_counter_text(start), console=console,
                  refresh_per_second=30, transient=True) as live:
            added, total, _ = updater.update_catalog(
                progress=lambda n: live.update(_counter_text(n)))
        _lc.cache_clear(); _ti.cache_clear()
        if added:
            console.print(f"[ok]{t('update_added', n=added, total=total)}[/ok]")
    except Exception:
        pass   # never let auto-scan break startup


def _start_background_collector() -> None:
    """Keep collecting new tools in the background while the menu is open, so the
    arsenal never stops growing during a session. Disabled by IW7X_NO_UPDATE or the
    auto_update config. Never blocks or crashes the UI (daemon thread)."""
    import os
    if os.environ.get("IW7X_NO_UPDATE") == "1" or not config.get("auto_update", True):
        return
    try:
        from . import updater
        updater.start_background_watch(interval_minutes=float(config.get("bg_scan_minutes", 20)))
    except Exception:
        pass


def run() -> None:
    config.get_tools_dir()
    _auto_scan_on_launch()
    _start_background_collector()
    while True:
        try:
            catalog = load_catalog()   # re-read each loop so background-collected tools appear live
            ui.render_main_menu(catalog)
            raw = _ask("[accent]╰─>[/accent]")
            if not raw:
                continue
            if raw.lower() in ("u", "update", "upgrade"):
                refreshed = update_screen()
                if refreshed is not None:
                    catalog = refreshed
                continue
            if not _dispatch(raw, catalog):
                break
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[err]{t('h_quit')}[/err]")
            break
        except SystemExit:
            ui.goodbye()
            break
