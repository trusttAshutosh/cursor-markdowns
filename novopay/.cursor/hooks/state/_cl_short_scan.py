#!/usr/bin/env python3
"""Deeper scan: extract short user_query texts that look like prefs/corrections."""
import json
import re
import sys
from pathlib import Path

MINE = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\_cl_mine_out.json")
AGENTS = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\AGENTS.md").read_text(encoding="utf-8").lower()
OUT = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\_cl_short_queries.txt")

SKIP = re.compile(
    r"(?i)^(resume|ok|yes|no|thanks|continue|go ahead|check again|"
    r"run the `continual-learning`|briefly inform the user)"
)


def extract_query(msg: str) -> str:
    m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", msg, re.S | re.I)
    if m:
        return m.group(1).strip()
    # strip image/skill wrappers
    msg = re.sub(r"<image_files>.*?</image_files>", "", msg, flags=re.S)
    msg = re.sub(r"<manually_attached_skills>.*?</manually_attached_skills>", "", msg, flags=re.S)
    msg = re.sub(r"<timestamp>.*?</timestamp>", "", msg, flags=re.S)
    return msg.strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    data = json.loads(MINE.read_text(encoding="utf-8"))
    lines = []
    for p in data["parents"]:
        for i, msg in enumerate(p["user_msgs"]):
            q = extract_query(msg)
            q = re.sub(r"\s+", " ", q).strip()
            if len(q) < 15 or len(q) > 600:
                continue
            if SKIP.search(q):
                continue
            if q.lower().startswith("build failed"):
                continue
            # skip pure URLs / file paths only
            if re.fullmatch(r"https?://\S+", q) or re.fullmatch(r"[A-Za-z]:\\.*", q):
                continue
            already = any(
                phrase in AGENTS
                for phrase in [
                    "digilocker",
                    "mobile_match_flag",
                    "filler1",
                    "quote_identifiers",
                    "continual learning",
                    "one-liner",
                    "don't commit",
                    "do not commit",
                ]
                if phrase in q.lower()
            )
            lines.append(f"[{p['uuid'][:8]} U{i}] len={len(q)}\n{q}\n")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"short queries: {len(lines)}")
    print(f"wrote {OUT}")
    for line in lines:
        print(line[:400])
        print("---")


if __name__ == "__main__":
    main()
