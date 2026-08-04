#!/usr/bin/env python3
"""Save a where-did-time-go workflog under Desktop/worklogs/YYYY-MM/YYYY-MM-DD/."""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_ROOT = Path.home() / "Desktop" / "worklogs"
# Asia/Kolkata without requiring the tzdata package on Windows
IST = timezone(timedelta(hours=5, minutes=30), name="IST")

# Legacy 24h: 153700.md or 153700_01.md
LEGACY_24H = re.compile(r"^(\d{2})(\d{2})(\d{2})(?:_(\d+))?\.md$", re.I)
# Legacy 12h with seconds: 09-02-15_PM.md
NAME_12H_SEC = re.compile(
    r"^(\d{2})-(\d{2})-(\d{2})_(AM|PM)(?:_(\d+))?\.md$", re.I
)
# Current 12h without seconds: 09-02_PM.md
NAME_12H = re.compile(r"^(\d{2})-(\d{2})_(AM|PM)(?:_(\d+))?\.md$", re.I)


def day_dir(root: Path, work_day) -> Path:
    return root / work_day.strftime("%Y-%m") / work_day.isoformat()


def format_12h_name(dt: datetime, collision: int = 0) -> str:
    """Return hh-mm_AM.md / hh-mm_PM.md (12-hour, no seconds)."""
    h24 = dt.hour
    ampm = "AM" if h24 < 12 else "PM"
    h12 = h24 % 12
    if h12 == 0:
        h12 = 12
    base = f"{h12:02d}-{dt.minute:02d}_{ampm}"
    if collision:
        return f"{base}_{collision:02d}.md"
    return f"{base}.md"


def _h12_to_24(hh: int, ap: str) -> int:
    ap = ap.upper()
    if hh == 12:
        return 12 if ap == "PM" else 0
    return hh + (12 if ap == "PM" else 0)


def parse_run_sort_key(path: Path) -> tuple:
    """Chronological sort key for a workflog filename (not lexicographic)."""
    name = path.name
    m = NAME_12H.match(name)
    if m:
        hh, mm, ap, coll = m.groups()
        return (_h12_to_24(int(hh), ap), int(mm), 0, int(coll or 0), name)
    m = NAME_12H_SEC.match(name)
    if m:
        hh, mm, ss, ap, coll = m.groups()
        return (_h12_to_24(int(hh), ap), int(mm), int(ss), int(coll or 0), name)
    m = LEGACY_24H.match(name)
    if m:
        hh, mm, ss, coll = m.groups()
        return (int(hh), int(mm), int(ss), int(coll or 0), name)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        sm = re.search(r"^saved_at:\s*(\S+)", text, re.M)
        if sm:
            dt = datetime.fromisoformat(sm.group(1).strip())
            return (dt.hour, dt.minute, dt.second, 0, name)
    except Exception:
        pass
    return (99, 99, 99, 99, name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--work-day",
        required=True,
        help="Calendar day being summarized (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"Worklogs root (default: {DEFAULT_ROOT})",
    )
    parser.add_argument(
        "--person",
        default="",
        help="Optional person name for YAML front matter",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Read markdown from file instead of stdin",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read markdown body from stdin (default if --input omitted)",
    )
    args = parser.parse_args()

    try:
        work_day = datetime.strptime(args.work_day, "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid --work-day: {args.work_day}", file=sys.stderr)
        return 2

    if args.input:
        body = args.input.read_text(encoding="utf-8")
    else:
        body = sys.stdin.read()
    body = body.strip() + "\n"
    if not body.strip():
        print("Empty workflog body", file=sys.stderr)
        return 2

    now = datetime.now(IST)
    out_dir = day_dir(args.root, work_day)
    out_dir.mkdir(parents=True, exist_ok=True)
    collision = 0
    out = out_dir / format_12h_name(now, collision)
    while out.exists():
        collision += 1
        out = out_dir / format_12h_name(now, collision)

    front = [
        "---",
        f"person: {args.person}" if args.person else "person:",
        f"work_day: {work_day.isoformat()}",
        f"saved_at: {now.isoformat(timespec='seconds')}",
        "skill: where-did-time-go",
        "---",
        "",
    ]
    if body.lstrip().startswith("---"):
        content = body
    else:
        content = "\n".join(front) + body

    out.write_text(content, encoding="utf-8")
    print(out.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
