#!/usr/bin/env python3
"""Extract high-signal preference/fact candidates from mined user messages."""
import json
import re
import sys
from pathlib import Path

STATE = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state")
MINE = STATE / "_cl_mine_out.json"
AGENTS = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\AGENTS.md")
OUT = STATE / "_cl_candidates.txt"

# Patterns that often indicate durable prefs / corrections
SIGNAL = re.compile(
    r"(?i)("
    r"always|never|from now|prefer|don't|do not|must not|must |"
    r"remember|rule:|going forward|stop doing|instead of|"
    r"agents\.md|workspace fact|preference|correction|"
    r"do not invent|one.?liner|fully qualified|ascii hyphen|"
    r"without asking|explicit|gate|bob validate|continual.?learning|"
    r"commit only|never push|never comment on jira|"
    r"backward compat|common.?scripts|flyway|"
    r"paste.?ready|one ticket|shrink.?logs|"
    r"codeant|sonar|quote_identifiers|"
    r"caveman|markitdown|unit test|"
    r"do not auto|ignore.*continual|"
    r"when asked|unless.*ask|"
    r"TL;DR|bottom line|summary"
    r")"
)

NOISE = re.compile(
    r"(?i)("
    r"HDP-\d+|ticket|PR #\d+|curl |gradlew |SELECT |"
    r"<user_info>|<git_status>|agent-transcripts|"
    r"Run the continual-learning|memory update flow|"
    r"You are an AI coding assistant"
    r")"
)


def strip_system_wrappers(text: str) -> str:
    # Remove common injected context blocks that dwarf the real ask
    for marker in (
        "<user_info>",
        "<git_status>",
        "<agent_transcripts>",
        "<rules>",
        "<communication>",
        "You are an AI coding assistant",
    ):
        if marker in text:
            # keep after last user_query if present
            break
    m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.S | re.I)
    if m:
        return m.group(1).strip()
    # sometimes query is after a long preamble
    if "user_query" in text.lower():
        parts = re.split(r"</?user_query>", text, flags=re.I)
        if len(parts) >= 2:
            return parts[1].strip()
    return text


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    data = json.loads(MINE.read_text(encoding="utf-8"))
    agents = AGENTS.read_text(encoding="utf-8")
    agents_l = agents.lower()

    candidates = []
    for p in data["parents"]:
        for i, msg in enumerate(p["user_msgs"]):
            q = strip_system_wrappers(msg)
            if len(q) < 40:
                continue
            if not SIGNAL.search(q):
                continue
            # skip pure task dumps that are mostly noise unless short correction
            noise_ratio = len(NOISE.findall(q))
            if noise_ratio > 8 and len(q) > 1500:
                continue
            # already in AGENTS?
            # take a few distinctive 6-word phrases
            words = re.findall(r"[A-Za-z0-9'.-]{3,}", q.lower())
            already = False
            for j in range(0, min(len(words) - 5, 40), 3):
                phrase = " ".join(words[j : j + 6])
                if len(phrase) > 25 and phrase in agents_l:
                    already = True
                    break
            candidates.append(
                {
                    "uuid": p["uuid"],
                    "idx": i,
                    "already_partial": already,
                    "text": q[:1800],
                }
            )

    OUT.write_text(
        "\n\n".join(
            f"[{c['uuid']} U{c['idx']}] already~{c['already_partial']}\n{c['text']}"
            for c in candidates
        ),
        encoding="utf-8",
    )
    print(f"candidates: {len(candidates)}")
    print(f"wrote {OUT}")
    # print shorter list for review
    for c in candidates:
        one = re.sub(r"\s+", " ", c["text"]).strip()
        print(f"\n[{c['uuid'][:8]} U{c['idx']}] already~{c['already_partial']}")
        print(one[:500])


if __name__ == "__main__":
    main()
