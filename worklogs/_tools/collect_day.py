#!/usr/bin/env python3
"""Collect one day's work evidence from Cursor chats, Claude Code sessions and git commits.

Shared by Claude Code (/where-did-time-go, /standup) and Cursor skills, so both tools
see the same merged timeline. Prints markdown; all times are IST (UTC+5:30).

Usage:
    python collect_day.py                     # today
    python collect_day.py --date 2026-09-28
    python collect_day.py --date yesterday    # or: last-workday, friday, ...
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

IST = dt.timezone(dt.timedelta(hours=5, minutes=30), name="IST")
HOME = Path.home()
CURSOR_PROJECTS = HOME / ".cursor" / "projects"
CLAUDE_PROJECTS = HOME / ".claude" / "projects"
WORKSPACE = HOME / "Desktop" / "novopay"
REPO_GLOBS = ("bob-the-builder", "novopay-platform-*", "trustt-platform-*")
# Reflog actions that mean "this machine wrote the commit" (see made_here).
LOCAL_ACTIONS = ("commit", "cherry-pick", "rebase", "merge", "pull --rebase")

IDLE_SPLIT = dt.timedelta(minutes=45)
BLOCK_CAP = dt.timedelta(hours=3)
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

META_PROMPT = re.compile(
    r"^\s*(/?where[- ]did[- ]time[- ]go|/?standup|what did i (do|get done)|what new to tell|"
    r"(short )?(standup )?upd?ate? for standup|short upa?date|standup update|daily workflog|"
    r"run the `?continual-learning|is there a skill)",
    re.I,
)
STANDUP_ASK = re.compile(r"\bstand-?up\b", re.I)  # short asks only; long pastes may just mention it
# Prompts the tools inject on the user's behalf (Cursor subagent/task plumbing).
TOOL_PROMPT = re.compile(r"^\s*(Available subagent_types|Briefly inform the user about the task result)", re.I)
INJECTED = re.compile(
    r"<(system-reminder|local-command-stdout|local-command-stderr|command-message|user-prompt-submit-hook)"
    r"\b[^>]*>.*?</\1>",
    re.S,
)
PASTED = re.compile(r"<pasted_content\b[^>]*>.*?</pasted_content[^>]*>", re.S)
COMMAND_NAME = re.compile(r"<command-name>\s*(.*?)\s*</command-name>", re.S)
TAG = re.compile(r"</?[a-z_-]+(?:\s[^>]*)?>")
CURSOR_STAMP = re.compile(r"<timestamp>\s*([^<]+?)\s*</timestamp>", re.I)
CURSOR_QUERY = re.compile(r"<user_query>\s*(.*?)\s*</user_query>", re.S | re.I)
TICKET = re.compile(r"\b(?:HDP|AAN|CC|BKYC|DDP|NP|TP)-\d{2,6}\b")


@dataclass
class Event:
    at: dt.datetime
    role: str  # "user" | "assistant"
    text: str


@dataclass
class Session:
    source: str  # "Cursor" | "Claude"
    sid: str
    title: str
    workspace: str
    events: list[Event] = field(default_factory=list)


# ---------------------------------------------------------------- day resolution

def resolve_day(value: str | None) -> dt.date:
    today = dt.datetime.now(IST).date()
    value = (value or "today").strip().lower()
    if value == "today":
        return today
    if value == "yesterday":
        return today - dt.timedelta(days=1)
    if value == "last-workday":
        back = {0: 3, 6: 2}.get(today.weekday(), 1)  # Mon -> Fri, Sun -> Fri
        return today - dt.timedelta(days=back)
    if value in WEEKDAYS:
        delta = (today.weekday() - WEEKDAYS.index(value)) % 7 or 7
        return today - dt.timedelta(days=delta)
    return dt.date.fromisoformat(value)


# ---------------------------------------------------------------- text helpers

def content_text(content) -> tuple[str, bool]:
    """Return (text, has_tool_result) for a message content field."""
    if isinstance(content, str):
        return content, False
    if not isinstance(content, list):
        return "", False
    texts, tool_result = [], False
    for part in content:
        if not isinstance(part, dict):
            continue
        if part.get("type") == "text":
            texts.append(part.get("text") or "")
        elif part.get("type") == "tool_result":
            tool_result = True
        elif part.get("type") == "image":
            texts.append("[image]")
    return "\n".join(texts), tool_result


def clean_prompt(text: str) -> str:
    command = COMMAND_NAME.search(text)
    text = PASTED.sub(" [pasted notes] ", text)
    text = INJECTED.sub(" ", text)
    text = COMMAND_NAME.sub(" ", text)
    text = TAG.sub(" ", text)
    text = " ".join(text.split())
    if command:
        text = f"{command.group(1)} {text}".strip()
    return text


def one_line(text: str, limit: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def modified_since(path: Path, start: dt.datetime) -> bool:
    try:
        return path.stat().st_mtime >= start.timestamp()
    except OSError:
        return False


def read_jsonl(path: Path):
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


# ---------------------------------------------------------------- Cursor

def parse_cursor_stamp(raw: str) -> dt.datetime | None:
    cleaned = re.sub(r"\s*\([^)]*\)\s*$", "", raw.strip())
    for fmt in ("%A, %b %d, %Y, %I:%M %p", "%A, %B %d, %Y, %I:%M %p", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return dt.datetime.strptime(cleaned, fmt).replace(tzinfo=IST)
        except ValueError:
            continue
    return None


def cursor_sessions(start: dt.datetime) -> list[Session]:
    sessions = []
    for path in CURSOR_PROJECTS.glob("*/agent-transcripts/*/*.jsonl"):
        if not modified_since(path, start):
            continue
        workspace = path.parts[-4].removeprefix(f"c-Users-{HOME.name.replace('.', '-')}-")
        session = Session("Cursor", path.stem, "", workspace)
        last_stamp: dt.datetime | None = None
        for record in read_jsonl(path):
            text, _ = content_text((record.get("message") or {}).get("content"))
            if record.get("role") == "user":
                stamp = CURSOR_STAMP.search(text)
                parsed = parse_cursor_stamp(stamp.group(1)) if stamp else None
                last_stamp = parsed or last_stamp
                query = CURSOR_QUERY.search(text)
                prompt = clean_prompt(query.group(1) if query else text)
                if last_stamp and prompt and not TOOL_PROMPT.match(prompt):
                    session.events.append(Event(last_stamp, "user", prompt))
            elif record.get("role") == "assistant" and last_stamp and text.strip():
                session.events.append(Event(last_stamp, "assistant", text))
        first_prompt = next((e.text for e in session.events if e.role == "user"), "")
        session.title = one_line(first_prompt, 60)
        sessions.append(session)
    return sessions


# ---------------------------------------------------------------- Claude Code

def claude_is_prompt(record: dict, text: str, tool_result: bool) -> bool:
    if record.get("isMeta") or record.get("isSidechain") or tool_result:
        return False
    origin = (record.get("origin") or {}).get("kind")
    if origin:
        return origin == "human"
    return bool(text.strip()) and not text.startswith("[Request interrupted")


def ran_here(cwd: str) -> bool:
    """True for a session whose working directory is on this Windows machine.

    The Claude account is shared; sessions run elsewhere (cloud / other users) would carry
    a Linux or foreign path, so they are skipped even if they ever sync into this folder.
    """
    home = os.path.normcase(str(HOME)) + os.sep
    return os.path.normcase(cwd).startswith(home)


def claude_sessions(start: dt.datetime) -> list[Session]:
    sessions = []
    for path in CLAUDE_PROJECTS.glob("*/*.jsonl"):
        if not modified_since(path, start):
            continue
        session = Session("Claude", path.stem, "", "")
        cwd = next((r["cwd"] for r in read_jsonl(path) if r.get("cwd")), "")
        if cwd and not ran_here(cwd):
            continue
        for record in read_jsonl(path):
            kind = record.get("type")
            if kind == "custom-title":
                session.title = record.get("customTitle") or session.title
            elif kind == "summary" and not session.title:
                session.title = record.get("summary") or ""
            if kind not in ("user", "assistant") or not record.get("timestamp"):
                continue
            if record.get("cwd") and not session.workspace:
                session.workspace = Path(record["cwd"]).name
            at = dt.datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00")).astimezone(IST)
            text, tool_result = content_text((record.get("message") or {}).get("content"))
            if kind == "user":
                if claude_is_prompt(record, text, tool_result):
                    prompt = clean_prompt(text)
                    if prompt:
                        session.events.append(Event(at, "user", prompt))
            elif not record.get("isSidechain"):
                session.events.append(Event(at, "assistant", text))
        if not session.title:
            session.title = one_line(next((e.text for e in session.events if e.role == "user"), ""), 60)
        sessions.append(session)
    return sessions


# ---------------------------------------------------------------- blocks

@dataclass
class Block:
    session: Session
    events: list[Event]

    @property
    def start(self) -> dt.datetime:
        return self.events[0].at

    @property
    def end(self) -> dt.datetime:
        return self.events[-1].at

    @property
    def prompts(self) -> list[Event]:
        return [e for e in self.events if e.role == "user"]


def drop_meta(events: list[Event]) -> tuple[list[Event], int]:
    """Remove meta prompts and the assistant turns answering them."""
    kept, skipping, dropped = [], False, 0
    for event in events:
        if event.role == "user":
            skipping = bool(META_PROMPT.match(event.text)
                            or (len(event.text) <= 200 and STANDUP_ASK.search(event.text)))
            dropped += skipping
        if not skipping:
            kept.append(event)
    return kept, dropped


def split_blocks(session: Session, day_start: dt.datetime, day_end: dt.datetime) -> tuple[list[Block], int]:
    events = sorted((e for e in session.events if day_start <= e.at < day_end), key=lambda e: e.at)
    events, dropped = drop_meta(events)
    blocks: list[Block] = []
    for event in events:
        current = blocks[-1] if blocks else None
        if current and event.at - current.end <= IDLE_SPLIT and event.at - current.start <= BLOCK_CAP:
            current.events.append(event)
        else:
            blocks.append(Block(session, [event]))
    return [b for b in blocks if b.prompts], dropped


# ---------------------------------------------------------------- git

def repos() -> list[Path]:
    """Workspace repos, skipping worktrees whose main clone is already listed."""
    candidates = [WORKSPACE] if (WORKSPACE / ".git").exists() else []
    for pattern in REPO_GLOBS:
        candidates += sorted(p for p in WORKSPACE.glob(pattern) if (p / ".git").exists())
    found, common_dirs = [], set()
    for repo in candidates:
        result = subprocess.run(["git", "-C", str(repo), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                capture_output=True, text=True, check=False)
        common = result.stdout.strip() or str(repo)
        if common not in common_dirs:
            common_dirs.add(common)
            found.append(repo)
    return found


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False).stdout


def my_email() -> str:
    return git(WORKSPACE, "config", "user.email").strip().lower()


def made_here(repo: Path, since: dt.datetime) -> set[str]:
    """Hashes of commits created on this machine since `since`.

    Reflogs are never pushed or fetched, so a commit / amend / cherry-pick / rebase / merge
    entry in them means the commit was written here - not pulled from a colleague or GitHub.
    Reads the reflog files directly (`git log -g --all` takes ~30 s on these repos).
    Line format: `<old> <new> <name> <<email>> <unix-ts> <tz>\\t<action>: <subject>`.
    """
    common = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())
    logs = [p for p in (common / "logs").rglob("*") if p.is_file()]
    logs += list((common / "worktrees").glob("*/logs/HEAD"))
    made, cutoff = set(), since.timestamp()
    for path in logs:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            head, _, action = line.partition("\t")
            fields = head.split()
            if len(fields) < 5 or not fields[-2].isdigit() or int(fields[-2]) < cutoff:
                continue
            local = action.startswith(LOCAL_ACTIONS) or (action.startswith("pull") and "Merge made" in action)
            if local and "Fast-forward" not in action:
                made.add(fields[1])
    return made


def commits(day_start: dt.datetime, day_end: dt.datetime) -> list[tuple[dt.datetime, str, str, int]]:
    """(time, repo, subject, copies) for commits you authored AND committed on this machine.

    Excludes your commits that someone else cherry-picked, merged or rebased (committer is
    them / GitHub) and anything not in the local reflog. Same subject on several branches
    is collapsed.
    """
    email = my_email()
    since = day_start - dt.timedelta(days=1)
    seen: dict[tuple[str, str], list] = {}
    for repo in repos():
        made = made_here(repo, since)
        log = git(repo, "log", "--all", f"--author={email}", f"--since={since.date().isoformat()}",
                  "--pretty=%H%x09%ae%x09%ce%x09%aI%x09%s")
        for line in log.splitlines():
            sha, author, committer, stamp, subject = (line.split("\t", 4) + [""] * 5)[:5]
            if author.lower() != email or committer.lower() != email or sha not in made:
                continue
            try:
                at = dt.datetime.fromisoformat(stamp).astimezone(IST)
            except ValueError:
                continue
            if not day_start <= at < day_end:
                continue
            key = (repo.name, subject.strip())
            if key in seen:
                seen[key][0] = min(seen[key][0], at)
                seen[key][3] += 1
            else:
                seen[key] = [at, repo.name, subject.strip(), 1]
    return sorted(tuple(v) for v in seen.values())


# ---------------------------------------------------------------- output

def minutes(delta: dt.timedelta) -> int:
    return int(delta.total_seconds() // 60)


def last_answer(block: Block) -> str:
    return next((e.text for e in reversed(block.events) if e.role == "assistant" and e.text.strip()), "")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--date", help="YYYY-MM-DD | today | yesterday | last-workday | weekday name (default: today)")
    parser.add_argument("--max-prompts", type=int, default=8, help="prompts listed per block (default 8)")
    args = parser.parse_args()

    day = resolve_day(args.date)
    day_start = dt.datetime.combine(day, dt.time.min, IST)
    day_end = day_start + dt.timedelta(days=1)

    blocks: list[Block] = []
    meta_dropped = 0
    sessions = cursor_sessions(day_start) + claude_sessions(day_start)
    for session in sessions:
        found, dropped = split_blocks(session, day_start, day_end)
        blocks += found
        meta_dropped += dropped
    blocks.sort(key=lambda b: (b.start, b.end))
    found_commits = commits(day_start, day_end)

    used = {(b.session.source, b.session.sid) for b in blocks}
    counts = {src: sum(1 for s, _ in used if s == src) for src in ("Cursor", "Claude")}
    print(f"# Work evidence - {day.isoformat()} ({WEEKDAYS[day.weekday()].title()}) - times IST")
    print(f"Sessions: Cursor {counts['Cursor']} · Claude {counts['Claude']} · "
          f"blocks {len(blocks)} · commits {len(found_commits)} · meta prompts ignored {meta_dropped}")
    print("Blocks are auto-split per session (idle > 45m, cap 3h). Merge same-topic cross-tool overlaps yourself.\n")

    print("## Activity blocks (by start time)")
    if not blocks:
        print("- none")
    for n, block in enumerate(blocks, 1):
        span = minutes(block.end - block.start)
        duration = f"~{span}m" if span else "single stamp"
        tickets = sorted(set(TICKET.findall(block.session.title + " " + " ".join(p.text for p in block.prompts))))
        print(f"\n### B{n} {block.start:%H:%M}-{block.end:%H:%M} ({duration}) · {block.session.source}: "
              f"[{block.session.title or 'untitled'}]({block.session.sid})")
        print(f"- workspace: {block.session.workspace or '?'}" + (f" · tickets: {', '.join(tickets)}" if tickets else ""))
        prompts = block.prompts
        for event in prompts[: args.max_prompts]:
            print(f"- {event.at:%H:%M} asked: {one_line(event.text, 240)}")
        if len(prompts) > args.max_prompts:
            print(f"- … {len(prompts) - args.max_prompts} more prompts until {prompts[-1].at:%H:%M}: "
                  f"{one_line(prompts[-1].text, 160)}")
        answer = last_answer(block)
        if answer:
            print(f"- outcome: {one_line(answer, 500)}")

    print("\n## Commits (yours, made on this machine; same subject on several branches collapsed)")
    if not found_commits:
        print("- none")
    for at, repo, subject, copies in found_commits:
        print(f"- {at:%H:%M} {repo}: {subject}" + (f" (x{copies} branches)" if copies > 1 else ""))


if __name__ == "__main__":
    main()
