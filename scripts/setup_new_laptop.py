#!/usr/bin/env python3
"""New-laptop restore: clone Novopay repos + apply Cursor/AI config from this backup.

Invoked by SETUP-NEW-LAPTOP-NOVOPAY.bat after cursor-markdowns is cloned to Desktop.
"""
from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path


def _desktop() -> Path:
    user = Path(os.path.expanduser("~"))
    for candidate in (user / "Desktop", user / "OneDrive" / "Desktop"):
        if candidate.is_dir():
            return candidate
    return user / "Desktop"


def _run(cmd: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
    print(f"+ {' '.join(cmd)}")
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=check,
    )


def _writable(path: Path) -> None:
    if path.exists():
        path.chmod(path.stat().st_mode | stat.S_IWRITE)


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        _writable(dst)
    shutil.copy2(src, dst)


def _copy_tree_merge(src: Path, dst: Path) -> int:
    """Copy files from src into dst (create dirs; overwrite files)."""
    if not src.exists():
        return 0
    count = 0
    for root, _dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        out = dst / rel
        out.mkdir(parents=True, exist_ok=True)
        for name in files:
            s = Path(root) / name
            t = out / name
            if s.is_file():
                _copy_file(s, t)
                count += 1
    return count


def load_repos(tsv: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in tsv.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            raise SystemExit(f"Bad repos line (need folder, url, branch): {line}")
        rows.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))
    return rows


def remote_has_branch(url: str, branch: str) -> bool:
    r = _run(["git", "ls-remote", "--heads", url, branch])
    if r.returncode != 0:
        return False
    needle = f"refs/heads/{branch}"
    return any(needle in line for line in r.stdout.splitlines())


def clone_repo(novopay: Path, folder: str, url: str, branch: str) -> str:
    target = novopay / folder
    if target.exists() and (target / ".git").exists():
        print(f"  skip clone (exists): {folder}")
        # still try to fetch preferred branch tip lightly
        _run(["git", "-C", str(target), "fetch", "--depth", "1", "origin", branch])
        return "exists"

    if target.exists() and any(target.iterdir()):
        print(f"  skip clone (non-empty non-git): {folder}")
        return "skipped-non-git"

    use_branch = branch if remote_has_branch(url, branch) else ""
    if use_branch:
        r = _run(["git", "clone", "--branch", use_branch, "--single-branch", url, str(target)])
    else:
        print(f"  preferred branch '{branch}' not on origin; cloning default for {folder}")
        r = _run(["git", "clone", url, str(target)])

    if r.returncode != 0:
        print(r.stderr or r.stdout)
        return "failed"
    print(f"  cloned: {folder}" + (f" @{use_branch}" if use_branch else ""))
    return "cloned"


def restore_user_cursor(backup: Path) -> None:
    user_cursor = Path.home() / ".cursor"
    src = backup / "user" / ".cursor"
    if not src.exists():
        print("WARN: backup user/.cursor missing; skip user restore")
        return

    user_cursor.mkdir(parents=True, exist_ok=True)

    # Safe selective restore (do not wipe extensions/projects/caches)
    for rel in (
        "rules",
        "hooks",
        "hooks.json",
        "skills-cursor",
        "agents",
    ):
        s = src / rel
        d = user_cursor / rel
        if s.is_dir():
            n = _copy_tree_merge(s, d)
            print(f"  restored ~/.cursor/{rel} ({n} files)")
        elif s.is_file():
            _copy_file(s, d)
            print(f"  restored ~/.cursor/{rel}")

    # mcp.json: only copy if user has none yet (avoid clobbering secrets)
    mcp_src = src / "mcp.json"
    mcp_dst = user_cursor / "mcp.json"
    if mcp_src.exists() and not mcp_dst.exists():
        _copy_file(mcp_src, mcp_dst)
        print("  restored ~/.cursor/mcp.json (was missing)")
    elif mcp_dst.exists():
        print("  kept existing ~/.cursor/mcp.json (not overwritten)")


def restore_novopay_workspace(backup: Path, novopay: Path) -> None:
    src_root = backup / "novopay"
    novopay.mkdir(parents=True, exist_ok=True)

    # Workspace entrypoints
    for name in (
        "AGENTS.md",
        "README.md",
        "package.json",
        "Makefile",
        "novopay.code-workspace",
        "bob-boot-remediation.yaml",
    ):
        s = src_root / name
        if s.exists():
            _copy_file(s, novopay / name)
            print(f"  workspace file: {name}")

    scripts = src_root / "scripts" / "validate-change.py"
    if scripts.exists():
        _copy_file(scripts, novopay / "scripts" / "validate-change.py")
        print("  workspace file: scripts/validate-change.py")

    # Full .cursor tree for workspace
    cursor_src = src_root / ".cursor"
    if cursor_src.exists():
        n = _copy_tree_merge(cursor_src, novopay / ".cursor")
        print(f"  restored novopay/.cursor ({n} files)")

    # Service overlays
    overlays = [
        (backup / "cc" / ".cursor", novopay / "novopay-platform-creditcard-management" / ".cursor"),
        (backup / "agent-webapp" / ".cursor", novopay / "novopay-platform-agent-webapp" / ".cursor"),
        (backup / "bob" / ".cursor", novopay / "bob-the-builder" / ".cursor"),
        (backup / "actor" / ".cursor", novopay / "novopay-platform-actor" / ".cursor"),
        (backup / "gateway" / ".cursor", novopay / "novopay-platform-api-gateway" / ".cursor"),
    ]
    for src, dst in overlays:
        if src.exists() and dst.parent.exists():
            n = _copy_tree_merge(src, dst)
            print(f"  overlay {dst.relative_to(novopay)} ({n} files)")

    # Bob skills + boot remediation into bob-the-builder
    bob = novopay / "bob-the-builder"
    if bob.exists():
        skills = backup / "bob" / "skills"
        if skills.exists():
            n = _copy_tree_merge(skills, bob / "skills")
            print(f"  bob skills ({n} files)")
        boot = src_root / "bob-boot-remediation.yaml"
        if boot.exists():
            _copy_file(boot, bob / "runner" / "config" / "boot-remediation.yaml")
            print("  bob boot-remediation.yaml")
        # MCP configs
        for name in ("mcp-servers.yaml", "tool-bridge.yaml"):
            s = backup / "bob" / "config" / name
            if s.exists():
                _copy_file(s, bob / "runner" / "config" / name)
                print(f"  bob config {name}")


def print_next_steps(novopay: Path) -> None:
    print()
    print("=" * 64)
    print("DONE - next steps on this laptop")
    print("=" * 64)
    print(f"1. Open workspace: {novopay / 'novopay.code-workspace'}")
    print("2. In Cursor > Extensions, install plugins listed in:")
    print(f"   {novopay / '.cursor' / 'CURSOR_PLUGINS.md'}")
    print("   (or run: python bob.py plugins   from Desktop\\novopay)")
    print("3. Smoke:  python bob.py --help")
    print("4. Smoke:  npm run validate -- novopay-platform-api-gateway")
    print("5. Auth GitHub for khoslalabs / trusttAshutosh if any clone failed.")
    print("=" * 64)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backup-root",
        type=Path,
        default=None,
        help="cursor-markdowns repo root (default: this script's parent)",
    )
    parser.add_argument(
        "--novopay-root",
        type=Path,
        default=None,
        help="Target Desktop/novopay (default: <Desktop>/novopay)",
    )
    parser.add_argument(
        "--skip-clone",
        action="store_true",
        help="Only restore Cursor/AI files; do not clone repos",
    )
    parser.add_argument(
        "--skip-cursor",
        action="store_true",
        help="Only clone repos; do not restore Cursor/AI files",
    )
    args = parser.parse_args()

    backup = (args.backup_root or Path(__file__).resolve().parent.parent).resolve()
    novopay = (args.novopay_root or (_desktop() / "novopay")).resolve()
    repos_tsv = backup / "novopay-repos.tsv"

    print(f"Backup root : {backup}")
    print(f"Novopay root: {novopay}")
    print()

    if not (backup / "novopay" / "AGENTS.md").exists():
        print("ERROR: This does not look like cursor-markdowns (missing novopay/AGENTS.md).")
        print("Clone https://github.com/trusttAshutosh/cursor-markdowns.git to Desktop first.")
        return 2

    # Preconditions
    for tool in ("git", "python"):
        if shutil.which(tool) is None and tool == "git":
            print("ERROR: git not found on PATH")
            return 2

    novopay.mkdir(parents=True, exist_ok=True)

    results = {"cloned": 0, "exists": 0, "failed": 0, "skipped-non-git": 0}
    if not args.skip_clone:
        if not repos_tsv.exists():
            print(f"ERROR: missing {repos_tsv}")
            return 2
        print("=== Cloning repos into Desktop\\novopay ===")
        for folder, url, branch in load_repos(repos_tsv):
            status = clone_repo(novopay, folder, url, branch)
            results[status] = results.get(status, 0) + 1
        print(
            f"Clone summary: cloned={results.get('cloned',0)} "
            f"exists={results.get('exists',0)} failed={results.get('failed',0)} "
            f"skipped={results.get('skipped-non-git',0)}"
        )
        print()

    if not args.skip_cursor:
        print("=== Restoring Cursor / AI config from backup ===")
        restore_user_cursor(backup)
        restore_novopay_workspace(backup, novopay)
        print()

    print_next_steps(novopay)
    return 1 if results.get("failed", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
