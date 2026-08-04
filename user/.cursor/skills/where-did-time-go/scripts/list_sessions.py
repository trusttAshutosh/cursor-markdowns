#!/usr/bin/env python3
"""List Cursor agent transcripts active in a date range (mtime or embedded timestamps)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

TIMESTAMP_RE = re.compile(
    r"<timestamp>\s*([^<]+?)\s*</timestamp>", re.IGNORECASE
)
USER_QUERY_RE = re.compile(
    r"<user_query>\s*(.*?)\s*</user_query>", re.DOTALL | re.IGNORECASE
)
JIRA_RE = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")


def parse_day(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d")


def home_projects() -> Path:
    return Path.home() / ".cursor" / "projects"


def extract_user_queries(text: str, limit: int = 3) -> list[str]:
    out: list[str] = []
    for m in USER_QUERY_RE.finditer(text):
        q = " ".join(m.group(1).split())
        if q:
            out.append(q[:160])
        if len(out) >= limit:
            break
    if out:
        return out
    for line in text.splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("role") != "user":
            continue
        msg = obj.get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    t = part.get("text") or ""
                    m = USER_QUERY_RE.search(t)
                    q = " ".join((m.group(1) if m else t).split())
                    if q:
                        out.append(q[:160])
                        break
        if len(out) >= limit:
            break
    return out


def embedded_datetimes(text: str) -> list[datetime]:
    found: list[datetime] = []
    for m in TIMESTAMP_RE.finditer(text):
        raw = m.group(1).strip()
        cleaned = re.sub(r"\s*\([^)]*\)\s*$", "", raw)
        for fmt in (
            "%A, %b %d, %Y, %I:%M %p",
            "%A, %B %d, %Y, %I:%M %p",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
        ):
            try:
                found.append(datetime.strptime(cleaned, fmt))
                break
            except ValueError:
                continue
    return found


def read_head_tail(path: Path, head_bytes: int = 65536, tail_bytes: int = 65536) -> str:
    try:
        size = path.stat().st_size
        with path.open("rb") as f:
            head = f.read(head_bytes)
            if size > head_bytes + tail_bytes:
                f.seek(max(0, size - tail_bytes))
                tail = f.read(tail_bytes)
            else:
                tail = b""
        return (head + b"\n" + tail).decode("utf-8", errors="replace")
    except OSError:
        return ""


def duration_note(stamps: list[datetime]) -> str:
    if len(stamps) >= 2:
        mins = int((max(stamps) - min(stamps)).total_seconds() // 60)
        if mins >= 60:
            return f"~{mins // 60}h{mins % 60:02d}m"
        return f"~{mins}m"
    if stamps:
        return "duration unknown"
    return "duration unknown (mtime only)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", required=True, help="YYYY-MM-DD inclusive")
    parser.add_argument(
        "--until",
        help="YYYY-MM-DD exclusive end (default: since+1 day)",
    )
    parser.add_argument(
        "--root",
        default=str(home_projects()),
        help="Cursor projects root",
    )
    parser.add_argument(
        "--scan-stamps",
        action="store_true",
        help="Also open non-mtime-matching files for embedded timestamps (slow)",
    )
    args = parser.parse_args()

    start = parse_day(args.since)
    end = parse_day(args.until) if args.until else start + timedelta(days=1)
    start_ts = start.timestamp()
    end_ts = end.timestamp()

    root = Path(args.root)
    if not root.is_dir():
        print(f"No projects root: {root}", file=sys.stderr)
        return 1

    rows: list[dict] = []
    for jsonl in root.glob("*/agent-transcripts/**/*.jsonl"):
        try:
            st = jsonl.stat()
        except OSError:
            continue
        mtime_in = start_ts <= st.st_mtime < end_ts
        if not mtime_in and not args.scan_stamps:
            continue

        sample = read_head_tail(jsonl)
        stamps = embedded_datetimes(sample)
        stamp_in = any(start <= s < end for s in stamps)

        if not mtime_in and not stamp_in:
            continue

        # Prefer fuller read only for matched sessions (still capped)
        text = sample
        if st.st_size <= 256_000:
            try:
                text = jsonl.read_text(encoding="utf-8", errors="replace")
                stamps = embedded_datetimes(text) or stamps
            except OSError:
                pass

        uuid = jsonl.stem
        parts = jsonl.parts
        project = parts[parts.index("projects") + 1] if "projects" in parts else "?"
        queries = extract_user_queries(text)
        jira = sorted(set(JIRA_RE.findall(text)))[:8]
        rows.append(
            {
                "uuid": uuid,
                "project": project,
                "path": str(jsonl),
                "match": "timestamp" if stamp_in else "mtime",
                "duration": duration_note(stamps),
                "jira": jira,
                "user_queries": queries,
            }
        )

    rows.sort(key=lambda r: r["path"])
    print(
        json.dumps(
            {
                "since": args.since,
                "until": end.strftime("%Y-%m-%d"),
                "sessions": rows,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
