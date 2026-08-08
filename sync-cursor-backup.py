#!/usr/bin/env python3
"""Mirror all Novopay-related agent config into cursor-markdowns (laptop migrate backup)."""
from __future__ import annotations

import os
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOVOPAY = Path(r"C:/Users/ashutosh.kumar/Desktop/novopay")
USER_CURSOR = Path(r"C:/Users/ashutosh.kumar/.cursor")

# Global ~/.cursor: backup config, skip IDE runtime/cache
USER_EXCLUDE_DIRS = {
    "extensions",
    "projects",
    "ai-tracking",
    "debug-logs",
    "snapshots",
}

USER_EXCLUDE_FILES = {
    "ide_state.json",
}

# Hook throttle timestamps (runtime, not config)
HOOK_STATE_SKIP = {"posttool-nudge-ts"}


def _writable(path: Path) -> None:
    if path.exists():
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IWRITE)


def _rmtree(path: Path) -> None:
    if not path.exists():
        return

    def onexc(func, p, exc_info):
        if not path.exists():
            return
        try:
            Path(p).chmod(stat.S_IWRITE)
            func(p)
        except OSError:
            pass

    shutil.rmtree(path, onexc=onexc)


def copy_tree(src: Path, dst: Path) -> int:
    """Copy src -> dst; resolve symlinks to content. Returns file count."""
    if not src.exists():
        return 0
    count = 0
    _rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(src, followlinks=True):
        rel = Path(root).relative_to(src)
        if rel.parts and rel.parts[0] in USER_EXCLUDE_DIRS:
            dirs.clear()
            continue
        dirs[:] = [d for d in dirs if d != ".git"]
        out_dir = dst / rel
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in files:
            if name in USER_EXCLUDE_FILES:
                continue
            if "hooks/state" in str(rel).replace("\\", "/") and name in HOOK_STATE_SKIP:
                continue
            s = Path(root) / name
            t = out_dir / name
            if s.is_symlink():
                target = s.resolve()
                if target.is_dir():
                    count += copy_tree(target, t)
                elif target.is_file():
                    if t.exists():
                        _writable(t)
                    shutil.copy2(target, t)
                    count += 1
            elif s.is_file():
                if t.exists():
                    _writable(t)
                shutil.copy2(s, t)
                count += 1
    return count


def copy_file(src: Path, dst: Path) -> bool:
    if not src.exists() or not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        _writable(dst)
    shutil.copy2(src, dst)
    return True


def sync_pair(label: str, src: Path, dst: Path, results: list[tuple[str, int, str]]) -> None:
    if not src.exists():
        results.append((label, 0, "missing source"))
        return
    n = copy_tree(src, dst)
    if n == 0 and src.is_dir():
        placeholder = dst / "README.md"
        placeholder.parent.mkdir(parents=True, exist_ok=True)
        placeholder.write_text(
            f"# Empty .cursor tree\n\nSource `{src}` exists but has no files (dirs only).\n",
            encoding="utf-8",
        )
        n = 1
    results.append((label, n, str(dst.relative_to(ROOT))))


def main() -> int:
    results: list[tuple[str, int, str]] = []

    # Global user .cursor (full config tree)
    sync_pair("user", USER_CURSOR, ROOT / "user" / ".cursor", results)

    # Novopay workspace + service repos + bob
    mappings = [
        ("novopay-workspace", NOVOPAY / ".cursor", ROOT / "novopay" / ".cursor"),
        ("cc", NOVOPAY / "novopay-platform-creditcard-management" / ".cursor", ROOT / "cc" / ".cursor"),
        ("bob", NOVOPAY / "bob-the-builder" / ".cursor", ROOT / "bob" / ".cursor"),
        (
            "bob-skills",
            NOVOPAY / "bob-the-builder" / "skills",
            ROOT / "bob" / "skills",
        ),
        (
            "bob-template-host-cc",
            NOVOPAY / "bob-the-builder/templates/onboarding/host-cc/.cursor",
            ROOT / "bob-templates" / "host-cc" / ".cursor",
        ),
        (
            "bob-template-novopay",
            NOVOPAY / "bob-the-builder/templates/onboarding/novopay/.cursor",
            ROOT / "bob-templates" / "novopay" / ".cursor",
        ),
        ("actor", NOVOPAY / "novopay-platform-actor" / ".cursor", ROOT / "actor" / ".cursor"),
        ("gateway", NOVOPAY / "novopay-platform-api-gateway" / ".cursor", ROOT / "gateway" / ".cursor"),
        (
            "agent-webapp",
            NOVOPAY / "novopay-platform-agent-webapp" / ".cursor",
            ROOT / "agent-webapp" / ".cursor",
        ),
    ]
    for label, src, dst in mappings:
        sync_pair(label, src, dst, results)

    # Bob onboarding cursor (hooks at templates/onboarding/cursor/)
    onboarding = NOVOPAY / "bob-the-builder/templates/onboarding/cursor"
    if onboarding.exists():
        sync_pair("bob-onboarding-cursor", onboarding, ROOT / "bob-templates" / "onboarding-cursor", results)

    # CC keeps its own skills on disk (not always a junction). Keep `cc/.cursor/skills`
    # intact from the CC mapping above, and also merge those skills into the novopay
    # backup skills tree so a laptop restore of canonical `novopay/.cursor/skills/`
    # still has CC test/plan skills.
    cc_skills_live = NOVOPAY / "novopay-platform-creditcard-management" / ".cursor" / "skills"
    novopay_skills_backup = ROOT / "novopay" / ".cursor" / "skills"
    if cc_skills_live.exists():
        merged = 0
        for skill_dir in cc_skills_live.iterdir():
            if not skill_dir.is_dir():
                continue
            merged += copy_tree(skill_dir, novopay_skills_backup / skill_dir.name)
        if merged:
            results.append(
                ("cc-skills-into-novopay", merged, "novopay\\.cursor\\skills (merged from CC)")
            )

    # Related non-.cursor docs / agent entrypoints (laptop migrate essentials)
    extras: list[tuple[str, Path, Path]] = [
        ("novopay-AGENTS", NOVOPAY / "AGENTS.md", ROOT / "novopay" / "AGENTS.md"),
        ("novopay-README", NOVOPAY / "README.md", ROOT / "novopay" / "README.md"),
        ("novopay-package", NOVOPAY / "package.json", ROOT / "novopay" / "package.json"),
        ("novopay-Makefile", NOVOPAY / "Makefile", ROOT / "novopay" / "Makefile"),
        (
            "novopay-validate-script",
            NOVOPAY / "scripts" / "validate-change.py",
            ROOT / "novopay" / "scripts" / "validate-change.py",
        ),
        (
            "novopay-workspace-file",
            NOVOPAY / "novopay.code-workspace",
            ROOT / "novopay" / "novopay.code-workspace",
        ),
        (
            "bob-boot-remediation",
            NOVOPAY / "bob-the-builder/runner/config/boot-remediation.yaml",
            ROOT / "novopay" / "bob-boot-remediation.yaml",
        ),
        (
            "bob-CURSOR_PLUGINS",
            NOVOPAY / "bob-the-builder/docs/CURSOR_PLUGINS.md",
            ROOT / "bob" / "CURSOR_PLUGINS.md",
        ),
        (
            "bob-README",
            NOVOPAY / "bob-the-builder/README.md",
            ROOT / "bob" / "README.md",
        ),
        (
            "bob-KT",
            NOVOPAY / "bob-the-builder/docs/KT_CURSOR_AND_BOB.md",
            ROOT / "bob" / "docs" / "KT_CURSOR_AND_BOB.md",
        ),
        (
            "bob-GUIDE",
            NOVOPAY / "bob-the-builder/docs/BOB_GUIDE.md",
            ROOT / "bob" / "docs" / "BOB_GUIDE.md",
        ),
        (
            "bob-MCP_TOOL_BRIDGE",
            NOVOPAY / "bob-the-builder/docs/MCP_TOOL_BRIDGE.md",
            ROOT / "bob" / "docs" / "MCP_TOOL_BRIDGE.md",
        ),
        (
            "bob-docs-README",
            NOVOPAY / "bob-the-builder/docs/README.md",
            ROOT / "bob" / "docs" / "README.md",
        ),
        (
            "bob-ONBOARDING_DEVELOPER",
            NOVOPAY / "bob-the-builder/docs/ONBOARDING_DEVELOPER.md",
            ROOT / "bob" / "docs" / "ONBOARDING_DEVELOPER.md",
        ),
        (
            "bob-CHEATSHEET",
            NOVOPAY / "bob-the-builder/docs/BOB_CHEATSHEET.md",
            ROOT / "bob" / "docs" / "BOB_CHEATSHEET.md",
        ),
        (
            "bob-mcp-servers",
            NOVOPAY / "bob-the-builder/runner/config/mcp-servers.yaml",
            ROOT / "bob" / "config" / "mcp-servers.yaml",
        ),
        (
            "bob-tool-bridge",
            NOVOPAY / "bob-the-builder/runner/config/tool-bridge.yaml",
            ROOT / "bob" / "config" / "tool-bridge.yaml",
        ),
        (
            "workflow-mirror",
            NOVOPAY / ".cursor" / "WORKFLOWS.md",
            ROOT / "WORKFLOW.md",
        ),
        (
            "bob-shrink-logs",
            NOVOPAY / "bob-the-builder/runner/lib/shrink_logs.py",
            ROOT / "bob" / "runner" / "lib" / "shrink_logs.py",
        ),
        (
            "bob-shrink-logs-test",
            NOVOPAY / "bob-the-builder/runner/tests/test_shrink_logs.py",
            ROOT / "bob" / "runner" / "tests" / "test_shrink_logs.py",
        ),
    ]
    extra_count = 0
    for label, src, dst in extras:
        if copy_file(src, dst):
            extra_count += 1
            results.append((label, 1, str(dst.relative_to(ROOT))))
        else:
            results.append((label, 0, "missing source"))

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [f"# Last sync: {stamp}", "", "| Source | Files | Backup path |", "|--------|-------|-------------|"]
    for label, n, path in results:
        lines.append(f"| {label} | {n} | `{path}` |")
    (ROOT / "SYNC_MANIFEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    total = sum(n for _, n, _ in results)
    print(f"Synced {total} files across {len(results)} trees -> {ROOT}")
    print(f"  (including {extra_count} workspace entrypoint extras)")
    for label, n, path in results:
        print(f"  {label}: {n} files -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
