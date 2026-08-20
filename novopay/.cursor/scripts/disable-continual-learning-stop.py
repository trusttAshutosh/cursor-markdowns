#!/usr/bin/env python3
"""Disable Continual Learning plugin stop hook (opt-in memory mining only).

Cursor plugin updates restore hooks/hooks.json and re-enable auto-run after
each agent turn. Re-run this script after updating the Continual Learning plugin:

  python .cursor/scripts/disable-continual-learning-stop.py
"""
from __future__ import annotations

import json
from pathlib import Path

DISABLED_HOOKS = {"version": 1, "hooks": {}}
NOOP_STOP_TS = (
    "// Continual Learning stop hook disabled (opt-in memory mining only).\n"
    "console.log(JSON.stringify({}));\n"
)
CACHE_ROOT = Path.home() / ".cursor" / "plugins" / "cache" / "cursor-public" / "continual-learning"


def main() -> int:
    if not CACHE_ROOT.is_dir():
        print(f"No continual-learning plugin cache at {CACHE_ROOT}")
        return 0

    updated = 0
    for version_dir in sorted(CACHE_ROOT.iterdir()):
        hooks_dir = version_dir / "hooks"
        if not hooks_dir.is_dir():
            continue

        hooks_path = hooks_dir / "hooks.json"
        if hooks_path.is_file():
            try:
                current = json.loads(hooks_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                current = None
            if current != DISABLED_HOOKS:
                hooks_path.write_text(json.dumps(DISABLED_HOOKS, indent=2) + "\n", encoding="utf-8")
                print(f"Disabled stop hook: {hooks_path}")
                updated += 1
            else:
                print(f"Already disabled: {hooks_path}")

        stop_path = hooks_dir / "continual-learning-stop.ts"
        if stop_path.is_file():
            existing = stop_path.read_text(encoding="utf-8")
            if existing != NOOP_STOP_TS:
                stop_path.write_text(NOOP_STOP_TS, encoding="utf-8")
                print(f"No-op stop script: {stop_path}")
                updated += 1
            else:
                print(f"Already no-op: {stop_path}")

    if updated:
        print("\nReload Cursor (or start a new chat) so the change takes effect.")
    else:
        print("\nNo changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
