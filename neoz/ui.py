"""Rendering layer for iw7x — banner, header, menus, help.

Presentation only: these functions build/print rich renderables. Flow control
and input live in ``app.py``.
"""

from __future__ import annotations

import os
import random
from itertools import zip_longest

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from .i18n import PRODUCT, AUTHOR, t
from .models import Catalog, Category, Tool
from .system import CURRENT, is_installed

# Truecolor palette borrowed from test.py.
_ROUGE = "#FF4C60"; _VERT = "#4AE3A8"; _JAUNE = "#FFD15C"; _BLEU = "#60A8FF"
_MAGENTA = "#CE60FF"; _CYAN = "#48DCFF"; _BLANC = "#F0F2FF"; _GRIS = "#787C96"
_VIOLET = "#9652FF"; _PINK = "#FF47B3"; _BORDER = "#5B4B9E"

# Hero gradient (test.py PALETTE): pink -> violet -> cyan.
_GRAD = [(255, 71, 179), (150, 82, 255), (72, 220, 255)]

THEME = Theme({
    "brand":  f"bold {_CYAN}",
    "accent": f"bold {_VIOLET}",
    "ok":     f"bold {_VERT}",
    "err":    f"bold {_ROUGE}",
    "warn":   f"bold {_JAUNE}",
    "muted":  _GRIS,
    "url":    f"underline {_BLEU}",
    "arch":   f"dim {_JAUNE}",
    "soft":   _BORDER,
    "name":   "#8FE9FF",          # category / tool names — soft cyan
    # Override the base color names so every literal [cyan] / border_style="cyan"
    # etc. picks up the test.py palette without touching the layout.
    "cyan":    _CYAN,
    "magenta": _MAGENTA,
    "green":   _VERT,
    "red":     _ROUGE,
    "yellow":  _JAUNE,
    "white":   _BLANC,
    "blue":    _BLEU,
})

console = Console(theme=THEME)

# "IW7X" banner (ANSI-shadow style, no emoji).
_BANNER = [
    "██╗ ██╗    ██╗ ███████╗ ██╗  ██╗",
    "██║ ██║    ██║ ╚════██║ ╚██╗██╔╝",
    "██║ ██║ █╗ ██║     ██╔╝  ╚███╔╝ ",
    "██║ ██║███╗██║    ██╔╝   ██╔██╗ ",
    "██║ ╚███╔███╔╝    ██║   ██╔╝ ██╗",
    "╚═╝  ╚══╝╚══╝     ╚═╝   ╚═╝  ╚═╝",
]

_QUOTES = [
    "The quieter you become, the more you can hear.",
    "Offense informs defense.",
    "Enumerate before you exploit.",
    "Security is a process, not a product.",
    "Know your system before others do.",
    "A defined scope is your playground.",
]


def clear() -> None:
    os.system("cls" if CURRENT.system == "windows" else "clear")


def _spaced(text: str) -> str:
    """Letter-space a phrase for an editorial wordmark: 'ABC DE' -> 'A B C  D E'."""
    return "  ".join(" ".join(word) for word in text.split(" "))


def _grad_rgb(pos: float) -> str:
    """Interpolate the hero gradient at pos in [0,1] -> '#rrggbb'."""
    pos = 0.0 if pos < 0 else 1.0 if pos > 1 else pos
    seg = pos * (len(_GRAD) - 1)
    i = int(seg)
    f = seg - i
    a = _GRAD[i]
    b = _GRAD[min(i + 1, len(_GRAD) - 1)]
    r, g, bl = (int(a[k] + (b[k] - a[k]) * f) for k in range(3))
    return f"#{r:02x}{g:02x}{bl:02x}"


def _gradient_banner() -> Text:
    """Horizontal pink->violet->cyan gradient across the wordmark."""
    width = max((len(line) for line in _BANNER), default=1)
    txt = Text()
    for li, line in enumerate(_BANNER):
        for ci, ch in enumerate(line):
            txt.append(ch, style=f"bold {_grad_rgb(ci / max(1, width - 1))}")
        if li < len(_BANNER) - 1:
            txt.append("\n")
    return txt


def _gradient_text(text: str, bold: bool = False) -> Text:
    """Left-to-right gradient over a single line of text (spaces kept blank)."""
    txt = Text()
    n = max(1, len(text) - 1)
    for i, ch in enumerate(text):
        if ch == " ":
            txt.append(" ")
        else:
            txt.append(ch, style=("bold " if bold else "") + _grad_rgb(i / n))
    return txt


def tool_cell(tool: Tool) -> Text:
    """Tool name styled by install state — installed = green, else plain white.
    Pure typography: colour carries the state, no glyphs."""
    return Text(tool.title, style="ok" if is_installed(tool) else "white")


# ── Header — pure typography, no glyphs ────────────────────────────────────────

def _kali_status_line() -> "Text":
    """A live 'Kali readiness' line: green when tools can install/launch here,
    yellow on other Linux (apt/pacman auto-adapted), red when browse-only."""
    dragon = "#8ED0FF"
    if CURRENT.is_kali and CURRENT.is_wsl:
        return Text.assemble(("🐉 ", ""), (t("kali_wsl"), f"bold {_VERT}"))
    if CURRENT.is_kali:
        return Text.assemble(("🐉 ", ""), (t("kali_detected"), f"bold {_VERT}"))
    if CURRENT.system == "linux":
        distro = (CURRENT.distro_id or "linux").capitalize()
        return Text.assemble(("🐉 ", ""),
                             (t("kali_other_linux", distro=distro), f"bold {_JAUNE}"))
    return Text.assemble(("🐉 ", ""), (t("kali_browse_only"), f"bold {_ROUGE}"))


def render_header(catalog: Catalog) -> None:
    quote = random.choice(_QUOTES)

    body = Table.grid(expand=True)
    body.add_column(justify="center")
    body.add_row(_gradient_banner())
    body.add_row(Text(""))
    body.add_row(_gradient_text(_spaced("CYBERSECURITY ARSENAL")))
    body.add_row(Text.assemble(
        (f"{catalog.tool_count}", f"bold {_CYAN}"), ("  TOOLS", "dim"),
        ("        ", ""),
        (f"{len(catalog.categories)}", f"bold {_CYAN}"), ("  CATEGORIES", "dim"),
        ("        ", ""),
        ("BY ", "dim"), (AUTHOR.upper(), f"bold {_PINK}"),
    ))
    body.add_row(Text(""))
    body.add_row(_kali_status_line())
    body.add_row(Text(quote, style="italic dim"))

    console.print(Panel(
        Align.center(body),
        title=Text.assemble(("  ", ""), _gradient_text(_spaced(PRODUCT.upper()), bold=True),
                            (f"   v{catalog.version}  ", "dim")),
        subtitle=f"[dim]{t('authorized_only').upper()}[/dim]",
        subtitle_align="center",
        border_style=_BORDER,
        box=box.HEAVY,
        padding=(1, 2),
    ))


# ── Main menu — clean two-tone grid, no icons ──────────────────────────────────

def render_main_menu(catalog: Catalog) -> None:
    clear()
    render_header(catalog)

    cats = catalog.categories
    mid = (len(cats) + 1) // 2
    left = list(enumerate(cats[:mid], start=1))
    right = list(enumerate(cats[mid:], start=mid + 1))

    def _num(n: int) -> Text:
        return Text(f"{n:02d}", style=f"bold {_VIOLET}")

    def _name(title: str) -> Text:
        return Text(title.upper(), style="name")

    grid = Table.grid(padding=(0, 3), expand=True)
    grid.add_column(justify="right", width=3)
    grid.add_column(ratio=1, no_wrap=True)
    grid.add_column(width=6)
    grid.add_column(justify="right", width=3)
    grid.add_column(ratio=1, no_wrap=True)

    for (li, lc), r in zip_longest(left, right, fillvalue=None):
        if r:
            ri, rc = r
            grid.add_row(_num(li), _name(lc.title), "", _num(ri), _name(rc.title))
        else:
            grid.add_row(_num(li), _name(lc.title), "", Text(""), Text(""))

    console.print(Panel(
        grid,
        title=_gradient_text(_spaced(t("choose_category").upper()), bold=True),
        border_style=_BORDER,
        box=box.ROUNDED,
        padding=(1, 3),
    ))

    def _cmd(key: str, label: str) -> str:
        return f"[bold {_VIOLET}]{key}[/]  [dim]{label.upper()}[/dim]"

    console.print(Rule(style=_BORDER))
    console.print("     ".join([
        _cmd("/", t("h_search")), _cmd("T", t("h_tags")), _cmd("R", t("h_recommend")),
        _cmd("U", t("h_update")), _cmd("?", t("h_help")), _cmd("Q", t("h_quit")),
    ]))


# ── Reusable results table ─────────────────────────────────────────────────────

def render_results(title: str, results: list[tuple[Tool, Category]]) -> None:
    table = Table(title=title, box=box.SIMPLE_HEAD, show_lines=False)
    table.add_column(t("no"), justify="right", style="accent", width=5)
    table.add_column(t("tool"), style="brand", min_width=22)
    table.add_column(t("category"), style="dim cyan", min_width=15)
    table.add_column(t("description"), style="white", overflow="fold")

    for i, (tool, cat) in enumerate(results, start=1):
        table.add_row(str(i), tool_cell(tool), cat.title, tool.short_description())
    table.add_row("99", Text(t("back_main"), style="dim"), "", "")
    console.print(table)


# ── Aide ───────────────────────────────────────────────────────────────────────

def render_help() -> None:
    console.print(Panel(
        Text.assemble(
            (f"  {t('help_main')}\n", "bold white"),
            ("  ────────────────────────────────────────\n", "dim"),
            ("  1–N    ", "brand"), (t("help_open_cat") + "\n", "white"),
            ("  /…     ", "brand"), (t("help_do_search") + "\n", "white"),
            ("  t      ", "brand"), (t("help_do_tags") + "\n", "white"),
            ("  r      ", "brand"), (t("help_do_advisor") + "\n", "white"),
            ("  u      ", "brand"), (t("help_do_update_all") + "\n", "white"),
            ("  ?      ", "brand"), (t("help_do_help") + "\n", "white"),
            ("  q      ", "brand"), (t("help_do_quit") + "\n\n", "white"),
            (f"  {t('help_cat')}\n", "bold white"),
            ("  ────────────────────────────────────────\n", "dim"),
            ("  1–N    ", "brand"), (t("help_pick_tool") + "\n", "white"),
            ("  97     ", "brand"), (t("help_install_all") + "\n", "white"),
            ("  98     ", "brand"), (t("help_show_archived") + "\n", "white"),
            ("  99     ", "brand"), (t("help_back_main") + "\n\n", "white"),
            (f"  {t('help_tool')}\n", "bold white"),
            ("  ────────────────────────────────────────\n", "dim"),
            ("  1      ", "brand"), (t("help_do_install") + "\n", "white"),
            ("  2      ", "brand"), (t("help_do_run") + "\n", "white"),
            ("  99     ", "brand"), (t("help_back_cat") + "\n", "white"),
        ),
        title=f"[accent]{t('help_title')}[/accent]",
        border_style="magenta",
        box=box.ROUNDED,
        padding=(0, 2),
    ))


def goodbye() -> None:
    console.print(Panel(
        f"[bold white on cyan]{t('goodbye')}[/bold white on cyan]",
        box=box.HEAVY, border_style="cyan",
    ))
