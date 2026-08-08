#!/usr/bin/env python3
"""Generate today's where-did-time-go workflog from local Cursor transcripts.

Unattended daily runner for Task Scheduler. Heuristic (not full agent quality):
builds chronological blocks from embedded timestamps + user queries, then saves
under Desktop/worklogs/YYYY-MM/YYYY-MM-DD/hh-mm_AM.md (or _PM).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

IST = timezone(timedelta(hours=5, minutes=30), name="IST")
DEFAULT_ROOT = Path.home() / "Desktop" / "worklogs"
PROJECTS = Path.home() / ".cursor" / "projects"
LOG_DIR = Path.home() / "Desktop" / "worklogs" / "_runner_logs"

TS_RE = re.compile(r"<timestamp>([^<]+)</timestamp>", re.I)
UQ_RE = re.compile(r"<user_query>\s*(.*?)\s*</user_query>", re.S | re.I)
JIRA_RE = re.compile(r"\b([A-Z]{2,10}-\d+)\b")
FAKE_JIRA = {
    "PROJ-123", "CR-501", "CR-502", "ST-3", "STAGE-1", "CR-1", "PRN-1",
    "REF-0", "REF-2", "ST-1", "ST-4", "REF-001", "TEST-001", "UTF-8",
    "XX-1971", "AAN-601", "STAGE-2",
}
MONTHS = {
    n: i
    for i, n in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        1,
    )
}


def parse_ts(raw: str) -> datetime | None:
    s = raw.strip()
    m = re.match(
        r".+?,\s+(\w+)\s+(\d+),\s+(\d+),\s+(\d+):(\d+)\s+(AM|PM)\s+\(UTC([+-]\d+):(\d+)\)",
        s,
    )
    if m:
        mon, day, year, hh, mm, ap, oh, om = m.groups()
        h = int(hh) % 12
        if ap == "PM":
            h += 12
        if ap == "AM" and int(hh) == 12:
            h = 0
        oh_i, om_i = int(oh), int(om)
        off = timezone(timedelta(hours=oh_i, minutes=om_i if oh_i >= 0 else -om_i))
        mon_i = MONTHS.get(mon[:3])
        if not mon_i:
            return None
        return datetime(int(year), mon_i, int(day), h, int(mm), tzinfo=off).astimezone(IST)
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(IST)
    except Exception:
        return None


def extract_text(obj: dict) -> str:
    msg = obj.get("message")
    if not isinstance(msg, dict):
        return ""
    c = msg.get("content")
    if isinstance(c, list):
        return "\n".join(
            x.get("text") or ""
            for x in c
            if isinstance(x, dict) and x.get("type") == "text"
        )
    return c if isinstance(c, str) else ""


def format_12h_name(dt: datetime, collision: int = 0) -> str:
    h24 = dt.hour
    ampm = "AM" if h24 < 12 else "PM"
    h12 = h24 % 12 or 12
    base = f"{h12:02d}-{dt.minute:02d}_{ampm}"
    if collision:
        return f"{base}_{collision:02d}.md"
    return f"{base}.md"


def fmt_dur(mins: int | None) -> str:
    if mins is None:
        return "unknown"
    if mins < 60:
        return f"~{mins}m"
    h, m = divmod(mins, 60)
    return f"~{h}h {m}m" if m else f"~{h}h"


def topic_from_queries(queries: list[str]) -> str:
    if not queries:
        return "Cursor chat activity"
    q = queries[0]
    q = re.sub(r"\s+", " ", q).strip()
    # Drop skill-attachment noise
    if "Session start" in q and "timestamp" in q.lower():
        if len(queries) > 1:
            q = queries[1]
        else:
            return "where-did-time-go / workflog"
    if q.startswith("/"):
        return q.split()[0][:80]
    return (q[:90] + ("…" if len(q) > 90 else ""))


# Heuristic Work tags for auto-runner (agent polish can override).
OPS_HINTS = re.compile(
    r"(?i)\b("
    r"flyway|checksum|jenkins|deploy|merge.?conflict|/fix-merge-conflicts|"
    r"branch sync|checkout to|take latest pull|ddp-bkup|platform_master|"
    r"validate failure|repair/validate|env drift|actuator"
    r")\b"
)
META_HINTS = re.compile(
    r"(?i)\b("
    r"where-did-time-go|workflog|atlassian plugin|agent compatibility|"
    r"how many cursor agents|which all agents|work-capture|what-did-i-get-done|"
    r"cursor agents active|skill so that"
    r")\b"
)


def classify_work(topic: str, queries: list[str] | None = None) -> str:
    """Return build: / ops: / meta: prefix for a Work cell."""
    blob = " ".join([topic or ""] + (queries or [])[:5])
    if META_HINTS.search(blob) or topic.startswith("/where-did-time-go"):
        return "meta"
    if OPS_HINTS.search(blob) or topic.startswith("/fix-merge-conflicts"):
        return "ops"
    return "build"


def tagged_work(topic: str, queries: list[str] | None = None) -> str:
    tag = classify_work(topic, queries)
    phrase = topic.strip()
    if phrase.lower().startswith(("build:", "ops:", "meta:")):
        return phrase
    return f"{tag}: {phrase}"


def tickets_from_queries(queries: list[str]) -> str:
    found: list[str] = []
    for q in queries:
        for j in JIRA_RE.findall(q):
            if j not in FAKE_JIRA and j not in found:
                found.append(j)
    return ", ".join(found)


def collect_day_sessions(work_day: date) -> list[dict]:
    day_s = work_day.isoformat()
    next_day = (work_day + timedelta(days=1)).isoformat()
    mon = work_day.strftime("%b")  # Aug
    day_label = f"{mon} {work_day.day}, {work_day.year}"  # Aug 4, 2026
    by_uuid: dict[str, Path] = {}
    for p in PROJECTS.glob("**/agent-transcripts/*/*.jsonl"):
        if "subagents" in str(p):
            continue
        mtime = datetime.fromtimestamp(p.stat().st_mtime, IST)
        include = mtime.strftime("%Y-%m-%d") == day_s
        if not include:
            try:
                head = p.read_text(encoding="utf-8", errors="replace")[:300_000]
            except Exception:
                continue
            if day_s not in head and day_label not in head:
                continue
        uuid = p.stem
        if uuid in by_uuid and "empty-window" in str(p):
            continue
        if uuid in by_uuid and "empty-window" in str(by_uuid[uuid]):
            by_uuid[uuid] = p
            continue
        by_uuid[uuid] = p

    sessions: list[dict] = []
    for uuid, path in by_uuid.items():
        day_ts: list[datetime] = []
        day_queries: list[tuple[datetime, str]] = []
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            text = extract_text(obj)
            tss = [parse_ts(m.group(1)) for m in TS_RE.finditer(text or "")]
            tss = [t for t in tss if t and t.strftime("%Y-%m-%d") == day_s]
            day_ts.extend(tss)
            if obj.get("role") == "user":
                uqs = [re.sub(r"\s+", " ", m.group(1)).strip() for m in UQ_RE.finditer(text or "")]
                if uqs and tss:
                    for q in uqs:
                        if q:
                            day_queries.append((tss[0], q))
        if not day_ts:
            continue
        day_ts.sort()
        start, end = day_ts[0], day_ts[-1]
        mins = int((end - start).total_seconds() // 60)
        if mins == 0 and len(day_ts) == 1:
            mins = None
        queries = [q for _, q in sorted(day_queries, key=lambda x: x[0])]
        # Drop pure meta where-did-time-go skill dumps as sole activity
        if len(queries) == 1 and "Session start" in queries[0] and "timestamp" in queries[0].lower():
            continue
        sessions.append(
            {
                "uuid": uuid,
                "start": start,
                "end": end,
                "mins": mins,
                "queries": queries,
                "title": topic_from_queries(queries),
                "tickets": tickets_from_queries(queries),
            }
        )
    sessions.sort(key=lambda s: (s["start"], s["end"]))
    return sessions


def split_long_session(session: dict) -> list[dict]:
    """Split one session when query gaps exceed 90 minutes."""
    queries = session["queries"]
    # We only have query texts, not per-query times in this simplified path
    # Keep as one block; agent skill does smarter splits when run interactively.
    return [session]


def build_markdown(person: str, work_day: date, sessions: list[dict]) -> str:
    lines = [
        f"## Workflog — {work_day.isoformat()}",
        f"**Person:** {person}",
        "",
        "| # | Time | Duration | Work | Ticket | Chat |",
        "|---|------|----------|------|--------|------|",
    ]
    total_mins = 0
    mix = {"build": 0, "ops": 0, "meta": 0}
    for i, s in enumerate(sessions, 1):
        t0 = s["start"].strftime("%H:%M")
        t1 = s["end"].strftime("%H:%M")
        dur = fmt_dur(s["mins"])
        work = tagged_work(s["title"].replace("|", "/"), s.get("queries")).replace("|", "/")
        tag = work.split(":", 1)[0].lower()
        if isinstance(s["mins"], int):
            total_mins += s["mins"]
            if tag in mix:
                mix[tag] += s["mins"]
        ticket = s["tickets"]
        chat_title = s["title"][:40].replace("|", "/")
        chat = f"[{chat_title}]({s['uuid']})"
        lines.append(f"| {i} | {t0}–{t1} | {dur} | {work} | {ticket} | {chat} |")

    if not sessions:
        lines.append("| 1 | — | unknown | meta: No Cursor chat activity found | | |")

    lines.append("")
    if total_mins:
        lines.append(
            f"**Total duration:** {fmt_dur(total_mins)} "
            "*(estimates from chat timestamps; auto-generated daily run)*"
        )
    else:
        lines.append(
            "**Total duration:** unknown *(auto-generated daily run; sparse timestamps)*"
        )
    lines.append(
        f"**Mix:** build {fmt_dur(mix['build'])} · ops {fmt_dur(mix['ops'])} · "
        f"meta {fmt_dur(mix['meta'])}"
    )
    if sessions:
        wall0 = sessions[0]["start"].strftime("%H:%M")
        wall1 = sessions[-1]["end"].strftime("%H:%M")
        span = int((sessions[-1]["end"] - sessions[0]["start"]).total_seconds() // 60)
        lines.append(f"**Wall clock:** {wall0}–{wall1} ({fmt_dur(span)} span)")
    lines.append("")
    lines.append(
        f"*Source: local auto-runner (`generate_daily_workflog.py`). "
        f"Re-run `/where-did-time-go` in Cursor to refine.*"
    )
    lines.append("")
    return "\n".join(lines)


def save_workflog(person: str, work_day: date, body: str, root: Path) -> Path:
    now = datetime.now(IST)
    out_dir = root / work_day.strftime("%Y-%m") / work_day.isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    collision = 0
    out = out_dir / format_12h_name(now, collision)
    while out.exists():
        collision += 1
        out = out_dir / format_12h_name(now, collision)
    front = (
        "---\n"
        f"person: {person}\n"
        f"work_day: {work_day.isoformat()}\n"
        f"saved_at: {now.isoformat(timespec='seconds')}\n"
        "skill: where-did-time-go\n"
        "source: daily-auto-runner\n"
        "---\n\n"
    )
    out.write_text(front + body.lstrip(), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--work-day",
        default="",
        help="YYYY-MM-DD (default: today in IST). Use yesterday if run just after midnight.",
    )
    parser.add_argument("--person", default="Ashutosh")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--prefer-yesterday-after-hour",
        type=int,
        default=0,
        help="If local hour < this (0-23), summarize yesterday instead (useful for 00:00 runs).",
    )
    args = parser.parse_args()

    now = datetime.now(IST)
    if args.work_day:
        work_day = datetime.strptime(args.work_day, "%Y-%m-%d").date()
    else:
        work_day = now.date()
        # Scheduled at 23:59 → same calendar day. If somehow after midnight, use yesterday.
        if now.hour < args.prefer_yesterday_after_hour:
            work_day = (now - timedelta(days=1)).date()
        # If run in first few minutes after midnight (missed 23:59), still prefer yesterday
        if now.hour == 0 and now.minute <= 5 and not args.work_day:
            work_day = (now - timedelta(days=1)).date()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{now.strftime('%Y-%m-%d')}_{now.strftime('%H%M%S')}.log"

    def log(msg: str) -> None:
        line = f"{datetime.now(IST).isoformat(timespec='seconds')} {msg}"
        print(line, flush=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    log(f"START work_day={work_day} person={args.person}")
    sessions = collect_day_sessions(work_day)
    log(f"sessions={len(sessions)}")
    body = build_markdown(args.person, work_day, sessions)
    out = save_workflog(args.person, work_day, body, args.root)
    log(f"SAVED {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
