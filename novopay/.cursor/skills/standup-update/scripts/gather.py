"""Collect one day's work evidence for a standup: git commits across workspace repos + Cursor chats.

Usage:
    python gather.py                 # last workday (Mon -> Fri)
    python gather.py --date 2026-09-28
    python gather.py --date friday
"""

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

WORKSPACE = Path.home() / "Desktop" / "novopay"
TRANSCRIPTS = (
    Path.home() / ".cursor" / "projects" / "c-Users-ashutosh-kumar-Desktop-novopay" / "agent-transcripts"
)
AUTHOR = "shutosh"
REPO_GLOBS = ("bob-the-builder", "novopay-platform-*", "trustt-platform-*")
NOISE_PROMPTS = re.compile(
    r"^(Run the `continual-learning`|what did i do|short upadte|short update|is there a skill)", re.I
)
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def resolve_date(value: str | None) -> dt.date:
    today = dt.date.today()
    if not value or value == "yesterday":
        back = 3 if today.weekday() == 0 else 2 if today.weekday() == 6 else 1
        return today - dt.timedelta(days=back)
    if value.lower() in WEEKDAYS:
        delta = (today.weekday() - WEEKDAYS.index(value.lower())) % 7 or 7
        return today - dt.timedelta(days=delta)
    return dt.date.fromisoformat(value)


def repos() -> list[Path]:
    found = [WORKSPACE] if (WORKSPACE / ".git").exists() else []
    for pattern in REPO_GLOBS:
        found += sorted(p for p in WORKSPACE.glob(pattern) if (p / ".git").exists())
    return found


def commits(day: dt.date) -> dict[str, list[str]]:
    since, until = day.isoformat(), (day + dt.timedelta(days=1)).isoformat()
    out: dict[str, list[str]] = {}
    for repo in repos():
        result = subprocess.run(
            ["git", "-C", str(repo), "log", "--all", f"--since={since} 00:00", f"--until={until} 00:00",
             f"--author={AUTHOR}", "--pretty=%ad %s", "--date=format:%H:%M"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
        )
        subjects = list(dict.fromkeys(line for line in result.stdout.splitlines() if line.strip()))
        if subjects:
            out[repo.name] = subjects
    return out


def message_text(record: dict) -> str:
    content = record.get("message", {}).get("content", record.get("content"))
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content if isinstance(part, dict) and part.get("type", "text") == "text")
    return ""


def chat_summary(path: Path) -> dict | None:
    prompts: list[str] = []
    last_answer = ""
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = message_text(record).strip()
        if not text:
            continue
        if record.get("role") == "user":
            match = re.search(r"<user_query>(.*?)</user_query>", text, re.S)
            query = " ".join((match.group(1) if match else text).split())
            if query and not NOISE_PROMPTS.match(query) and len(prompts) < 3:
                prompts.append(query[:220])
        elif record.get("role") == "assistant":
            last_answer = text
    if not prompts:
        return None
    return {"id": path.stem, "prompts": prompts, "outcome": " ".join(last_answer.split())[:700]}


def chats(day: dt.date) -> list[dict]:
    if not TRANSCRIPTS.exists():
        return []
    picked = []
    for path in TRANSCRIPTS.glob("*/*.jsonl"):
        modified = dt.datetime.fromtimestamp(path.stat().st_mtime)
        if modified.date() == day:
            summary = chat_summary(path)
            if summary:
                summary["last_active"] = modified.strftime("%H:%M")
                picked.append(summary)
    return sorted(picked, key=lambda s: s["last_active"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="YYYY-MM-DD, weekday name, or 'yesterday' (default: last workday)")
    day = resolve_date(parser.parse_args().date)

    print(f"# Work evidence for {day.isoformat()} ({WEEKDAYS[day.weekday()].title()})\n")
    print("## Commits")
    found = commits(day)
    if not found:
        print("- none")
    for repo, subjects in found.items():
        print(f"### {repo}")
        for subject in subjects:
            print(f"- {subject}")
    print("\n## Chats (by last activity)")
    for chat in chats(day) or [{"id": "-", "last_active": "", "prompts": ["none"], "outcome": ""}]:
        print(f"### {chat['last_active']} {chat['id']}")
        for prompt in chat["prompts"]:
            print(f"- asked: {prompt}")
        if chat["outcome"]:
            print(f"- outcome: {chat['outcome']}")


if __name__ == "__main__":
    main()
