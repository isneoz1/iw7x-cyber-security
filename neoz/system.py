"""OS detection, package managers, and command execution for the NeoZ Toolkit.

All shell execution funnels through this module so behaviour (privilege
escalation, dry-run on unsupported OS, install detection) stays in one place.
"""

from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class OSInfo:
    system: str                 # "linux" | "macos" | "windows" | "unknown"
    distro_id: str = ""
    distro_like: str = ""
    version: str = ""
    pkg_manager: str = ""
    is_root: bool = False
    is_wsl: bool = False
    arch: str = ""
    home: Path = field(default_factory=Path.home)

    @property
    def is_supported(self) -> bool:
        """True when tools can actually run (POSIX shells)."""
        return self.system in ("linux", "macos")

    @property
    def is_kali(self) -> bool:
        """True only on Kali Linux (iw7x is built for Kali)."""
        return self.distro_id == "kali" or "kali" in self.distro_like


def _read_os_release() -> dict[str, str]:
    data: dict[str, str] = {}
    for path in ("/etc/os-release", "/usr/lib/os-release"):
        try:
            for line in Path(path).read_text(encoding="utf-8").splitlines():
                key, _, val = line.partition("=")
                data[key.strip()] = val.strip().strip('"')
            break
        except (FileNotFoundError, PermissionError):
            continue
    return data


def detect() -> OSInfo:
    raw = platform.system().lower()
    system = "macos" if raw == "darwin" else raw

    is_root = bool(hasattr(os, "geteuid") and os.geteuid() == 0)
    distro_id = distro_like = version = ""
    is_wsl = False

    if system == "linux":
        rel = _read_os_release()
        distro_id = rel.get("ID", "").lower()
        distro_like = rel.get("ID_LIKE", "").lower()
        version = rel.get("VERSION_ID", "")
        try:
            is_wsl = "microsoft" in Path("/proc/version").read_text(encoding="utf-8").lower()
        except (FileNotFoundError, PermissionError):
            pass

    pkg_manager = ""
    for mgr in ("apt-get", "pacman", "dnf", "zypper", "apk", "brew", "pkg"):
        if shutil.which(mgr):
            pkg_manager = mgr
            break

    return OSInfo(
        system=system,
        distro_id=distro_id,
        distro_like=distro_like,
        version=version,
        pkg_manager=pkg_manager,
        is_root=is_root,
        is_wsl=is_wsl,
        arch=platform.machine(),
    )


CURRENT = detect()

# Prefer doas when present, else sudo.
PRIV_CMD = "doas" if shutil.which("doas") else "sudo"

# Directories where pipx / go / cargo / gem drop executables but which are not
# always on the current shell's PATH (common right after a fresh install).
_EXTRA_BIN_DIRS = [
    CURRENT.home / ".local" / "bin",     # pipx, pip --user
    CURRENT.home / "go" / "bin",         # go install
    CURRENT.home / ".cargo" / "bin",     # cargo install
    CURRENT.home / ".gem" / "bin",       # gem install --user
    Path("/usr/local/go/bin"),
    Path("/usr/local/bin"),
    Path("/snap/bin"),
]


def which(binary: str) -> str | None:
    """Like ``shutil.which`` but also searches the pipx/go/cargo/gem bin dirs
    that a freshly installed tool may live in before PATH is refreshed."""
    if not binary:
        return None
    found = shutil.which(binary)
    if found:
        return found
    for d in _EXTRA_BIN_DIRS:
        for cand in (d / binary, d / f"{binary}.py"):
            try:
                if cand.is_file():
                    return str(cand)
            except OSError:
                continue
    return None


# ── Install-state & directory detection ────────────────────────────────────────

def _clone_dir(install_cmds: list[str]) -> str | None:
    """Return the directory a `git clone` command would create, if any."""
    for cmd in install_cmds:
        if "git clone" not in cmd:
            continue
        parts = cmd.split()
        urls = [p for p in parts if p.startswith("http")]
        if not urls:
            continue
        name = urls[0].rstrip("/").rsplit("/", 1)[-1].replace(".git", "")
        idx = parts.index(urls[0])
        if idx + 1 < len(parts) and not parts[idx + 1].startswith("-"):
            name = parts[idx + 1]           # explicit target dir
        return name
    return None


def is_installed(tool) -> bool:
    """Best-effort: binary on PATH, or the clone directory exists."""
    for cmd in tool.run:
        c = cmd.split("&&")[-1].strip() if "&&" in cmd else cmd
        c = c.split(";")[-1].strip()
        if c.startswith("sudo "):
            c = c[5:].strip()
        binary = c.split()[0] if c else ""
        if binary and binary not in (".", "cd", "echo", "python3", "python", "sudo"):
            if which(binary):
                return True
    name = _clone_dir(list(tool.install))
    if name and Path(name).is_dir():
        return True
    return False


def tool_dir(tool) -> str | None:
    """Locate a tool's working directory on disk."""
    name = _clone_dir(list(tool.install))
    if name and Path(name).is_dir():
        return str(Path(name).resolve())
    for cmd in tool.run:
        head = cmd.split("&&")[0].split(";")[0].strip()
        if head.startswith("cd "):
            d = head[3:].strip()
            if Path(d).is_dir():
                return str(Path(d).resolve())
    return None


# ── Execution ──────────────────────────────────────────────────────────────────

def adapt_command(cmd: str) -> str:
    """
    Make package-manager install/remove commands match the current distro so the
    whole catalog works on Kali/Debian (apt) even for BlackArch-sourced entries
    that ship a ``pacman`` command — and vice-versa on Arch/BlackArch.

    Only rewrites the specific pacman/apt install|remove patterns; everything
    else is returned untouched.
    """
    mgr = CURRENT.pkg_manager
    if mgr in ("apt-get", "apt"):
        # Running on Debian/Kali/Parrot/Ubuntu → convert pacman → apt.
        cmd = re.sub(r"(sudo\s+)?pacman\s+-S(?:yu|y)?\s+--noconfirm\s+",
                     "sudo apt install -y ", cmd)
        cmd = re.sub(r"(sudo\s+)?pacman\s+-S(?:yu|y)?\s+", "sudo apt install -y ", cmd)
        cmd = re.sub(r"(sudo\s+)?pacman\s+-R(?:ns|s|n)?\s+--noconfirm\s+",
                     "sudo apt remove -y ", cmd)
        cmd = re.sub(r"(sudo\s+)?pacman\s+-R(?:ns|s|n)?\s+", "sudo apt remove -y ", cmd)
    elif mgr == "pacman":
        # Running on Arch/BlackArch → convert apt → pacman.
        cmd = re.sub(r"(sudo\s+)?apt(?:-get)?\s+install\s+-y\s+",
                     "sudo pacman -S --noconfirm ", cmd)
        cmd = re.sub(r"(sudo\s+)?apt(?:-get)?\s+install\s+", "sudo pacman -S --noconfirm ", cmd)
        cmd = re.sub(r"(sudo\s+)?apt(?:-get)?\s+remove\s+-y\s+",
                     "sudo pacman -Rns --noconfirm ", cmd)
    return cmd


def run_shell(cmd: str) -> int:
    """Run a single shell command (adapted to the current distro), returning its
    exit code."""
    return os.system(adapt_command(cmd))


def run_commands(cmds: list[str]) -> bool:
    """Run a sequence of commands; return True if all succeeded (best-effort)."""
    ok = True
    for cmd in cmds:
        if run_shell(cmd) not in (0, None):
            ok = False
    return ok


def binary_candidates(tool) -> list[str]:
    """Best-effort list of binary names that might launch this tool."""
    cands: list[str] = []
    for cmd in tool.run:
        head = cmd.split("&&")[-1].split(";")[-1].strip()
        if head.startswith("sudo "):
            head = head[5:].strip()
        binary = head.split()[0] if head else ""
        if binary and binary not in (".", "cd", "sudo", "python3", "python", "bash", "sh"):
            cands.append(binary)
    for cmd in tool.install:
        if "apt install" in cmd or "pacman -S" in cmd or "pipx install" in cmd:
            token = cmd.split()[-1]
            if token and not token.startswith("-"):
                cands.append(token)
    if tool.title:
        cands.append(tool.title.split()[0].lower())
    out: list[str] = []
    for c in cands:
        if c and c not in out:
            out.append(c)
    return out


def launch(tool) -> str | None:
    """Launch an installed tool. Runs its ``run`` commands, else the first binary
    candidate found on PATH (including pipx/go/cargo/gem bin dirs). Returns what
    was launched, or None if nothing found."""
    if tool.run:
        for cmd in tool.run:
            run_shell(cmd)
        return tool.run[0]
    binary = next((b for b in binary_candidates(tool) if which(b)), None)
    if binary:
        run_shell(which(binary) or binary)
        return binary
    return None


def smart_update(tool) -> bool:
    """Detect the install method and run the matching update command."""
    updated = False
    for cmd in tool.install:
        if "git clone" in cmd:
            name = _clone_dir([cmd])
            if name and Path(name).is_dir():
                run_shell(f"git -C {name} pull")
                updated = True
        elif "pip install" in cmd:
            run_shell(cmd.replace("pip install", "pip install --upgrade"))
            updated = True
        elif "go install" in cmd:
            run_shell(cmd)
            updated = True
        elif "gem install" in cmd:
            run_shell(cmd.replace("gem install", "gem update"))
            updated = True
    return updated


def open_in_shell(directory: str) -> None:
    """Drop the user into an interactive shell inside a directory."""
    if CURRENT.system == "windows":
        subprocess.run(["cmd", "/K", f'cd /d "{directory}"'])
    else:
        os.system(f'cd "{directory}" && ${{SHELL:-/bin/sh}}')
