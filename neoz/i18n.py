"""Text layer (English) for iw7x — by NeoZ.

English-only interface. ``t(key, **kwargs)`` returns the matching string;
missing keys fall back to the raw key so the UI never breaks. ``kwargs`` feeds
placeholders via ``str.format``.
"""

from __future__ import annotations

PRODUCT = "iw7x"
AUTHOR = "NeoZ"

_EN: dict[str, str] = {
    # navigation / common
    "back": "Back",
    "back_main": "Back to main menu",
    "main_menu": "Main Menu",
    "select": "Select",
    "no": "No.",
    "action": "Action",
    "tool": "Tool",
    "category": "Category",
    "description": "Description",
    "reason": "Reason",
    "no_reason": "No reason given",
    "press_enter": "Press Enter to continue",
    "press_return": "Press Enter to go back",
    "invalid": "Invalid choice.",
    "enter_number": "Enter a number, ? for help, or q to quit.",

    # tool actions
    "install": "Install",
    "run": "Run",
    "update": "Update",
    "uninstall": "Uninstall",
    "open_folder": "Open Folder",
    "open_project": "Open Project Page",
    "options": "Options",
    "uninstalled_ok": "Uninstalled.",
    "no_uninstall": "No uninstall method for this tool.",

    # execution
    "installed_ok": "Successfully installed!",
    "install_failed": "Installation reported an error.",
    "not_installed": "Tool is not installed yet — install it first.",
    "updated_ok": "Update complete!",
    "no_update": "No automatic update method for this tool.",
    "running": "Running",
    "opening_folder": "Opening folder: {dir}",
    "type_exit": "Type 'exit' to return to iw7x.",
    "dir_not_found": "Tool folder not found on disk.",
    "clone_hint": "You can clone it manually:",
    "confirm_run": "This will execute shell commands. Continue?",
    "win_run_warning": "These tools target Linux/macOS. Running on Windows will likely fail.",
    "kali_only": "iw7x runs tools on Kali Linux only. Boot Kali (or WSL Kali) to use them.",
    "launching": "Launching {name} ...",
    "launch_hint": "Installed. Launch it with:  {bin}",

    # category
    "available_tools": "Available Tools",
    "page_of": "Page {p}/{tp}  ·  {total} tools",
    "next_page": "Next page",
    "prev_page": "Previous page",
    "install_all": "Install all ({n} not installed)",
    "archived": "Archived tools ({n})",
    "hidden_os": "({n} tools hidden — not supported on {os})",
    "installing": "Installing {n} tools...",
    "failed_tool": "Failed: {name}",
    "archived_title": "Archived Tools — {title}",
    "no_archived": "No archived tools here.",

    # kali status (shown in the header)
    "kali_banner": "BUILT FOR KALI LINUX",
    "kali_detected": "KALI LINUX DETECTED — READY TO INSTALL & LAUNCH",
    "kali_wsl": "KALI ON WSL DETECTED — READY TO INSTALL & LAUNCH",
    "kali_other_linux": "{distro} DETECTED — apt/pacman auto-adapted, best on Kali",
    "kali_browse_only": "NOT ON KALI — BROWSE ONLY (boot Kali to install & run)",

    # main menu
    "choose_category": "Choose a Category",
    "authorized_only": "For authorized security testing only · Built for Kali Linux",
    "goodbye": "  See you soon — stay ethical  ",
    "h_search": "search",
    "h_tags": "tags",
    "h_recommend": "advisor",
    "h_update": "update",
    "h_help": "help",
    "h_quit": "quit",
    "updating": "Fetching the full tool catalog from online sources (BlackArch)…",
    "update_added": "Added {n} new tools — {total} total.",
    "update_none": "Catalog already up to date.",
    "update_offline": "Update sources unreachable (offline?).",
    "help_do_update_all": "auto-update: fetch every tool online",
    "invalid_main": "Invalid input — a number, /query to search, or q to quit.",
    "choose_range": "Choose 1–{n}, ? for help, or q to quit.",

    # header
    "hdr_os": "os",
    "hdr_kernel": "kernel",
    "hdr_user": "user",
    "hdr_ip": "ip",
    "hdr_tools": "arsenal",
    "hdr_session": "session",
    "hdr_python": "python",
    "hdr_arch": "arch",
    "hdr_status": "status",
    "ready": "READY",
    "arsenal_line": "{cats} categories · {tools} tools",

    # search
    "search_prompt": "Search",
    "results_for": "Results for '{q}'",
    "no_results": "No tool matches '{q}'.",

    # tags
    "tags_title": "Available Tags",
    "enter_tag": "Enter a tag",
    "tag_missing": "Tag '{tag}' not found.",
    "tagged_with": "Tools tagged '{tag}'",

    # advisor
    "advisor_title": "What do you want to do?",
    "task": "Task",
    "advisor_for": "Recommended for: {task}",
    "advisor_none": "No tool found for this task.",

    # help
    "help_title": " iw7x — Quick Help ",
    "help_main": "Main menu",
    "help_open_cat": "open a category",
    "help_do_search": "search tools by name / keyword",
    "help_do_tags": "filter by tag (osint, web, c2, ...)",
    "help_do_advisor": "recommend tools for a task",
    "help_do_help": "show this help",
    "help_do_quit": "quit iw7x",
    "help_cat": "Inside a category",
    "help_pick_tool": "pick a tool",
    "help_install_all": "install every tool in the category",
    "help_show_archived": "show archived tools",
    "help_back_main": "back to main menu",
    "help_tool": "Inside a tool",
    "help_do_install": "install",
    "help_do_run": "run",
    "help_do_update": "update",
    "help_back_cat": "back to category",
}


def t(key: str, **kwargs) -> str:
    text = _EN.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text
