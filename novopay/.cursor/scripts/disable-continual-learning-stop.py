#!/usr/bin/env python3
"""Disable Continual Learning plugin stop hook (opt-in memory mining only).

Cursor plugin updates can restore hooks/hooks.json and re-enable auto-run after
each agent turn. Re-run this script after updating the Continual Learning plugin:

  python .cursor/scripts/disable-continual-learning-stop.py
"""
from __future__ import annotations

import json
from pathlib import Path

DISABLED_HOOKS = {"version": 1, "hooks": {}}
CACHE_ROOT = Path.home() / ".cursor" / "plugins" / "cache" / "cursor-public" / "continual-learning"


def main() -> int:
    if not CACHE_ROOT.is_dir():
        print(f"No continual-learning plugin cache at {CACHE_ROOT}")
        return 0

    updated = 0
    for version_dir in sorted(CACHE_ROOT.iterdir()):
        hooks_path = version_dir / "hooks" / "hooks.json"
        if not hooks_path.is_file():
            continue
        try:
            current = json.loads(hooks_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            current = None
        if current == DISABLED_HOOKS:
            print(f"Already disabled: {hooks_path}")
            continue
        hooks_path.write_text(json.dumps(DISABLED_HOOKS, indent=2) + "\n", encoding="utf-8")
        print(f"Disabled stop hook: {hooks_path}")
        updated += 1

    if updated:
        print("\nReload Cursor (or start a new chat) so the change takes effect.")
    else:
        print("\nNo changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
