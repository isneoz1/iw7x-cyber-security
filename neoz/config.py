"""User configuration and paths for the NeoZ Toolkit.

Everything is user-scoped under ``~/.neoz`` so it works for any user (root,
regular, macOS) without hardcoded home paths.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

APP_NAME = "iw7x"

CONFIG_DIR = Path.home() / f".{APP_NAME}"
CONFIG_FILE = CONFIG_DIR / "config.json"
TOOLS_DIR = CONFIG_DIR / "tools"

DEFAULTS: dict[str, Any] = {
    "tools_dir": str(TOOLS_DIR),
    "version": "1.5.0",
    "auto_update": True,   # scan online sources for new tools on every launch
}


def load() -> dict[str, Any]:
    """Load config, merged over defaults; never raises."""
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return {**DEFAULTS, **data}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULTS)


def save(cfg: dict[str, Any]) -> None:
    """Persist config, creating the directory if needed; never raises."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(
            json.dumps(cfg, indent=2, sort_keys=True, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError:
        pass


def get_tools_dir() -> Path:
    """Return (and create) the directory where cloned tools are stored."""
    cfg = load()
    path = Path(cfg.get("tools_dir", str(TOOLS_DIR))).expanduser()
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    return path


def get(key: str, default: Any = None) -> Any:
    return load().get(key, default)


def set_value(key: str, value: Any) -> None:
    cfg = load()
    cfg[key] = value
    save(cfg)
