#!/usr/bin/env python3
"""Mine continual-learning delta transcripts for high-signal memory candidates."""
import json
import re
import sys
from pathlib import Path

STATE = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state")
DELTAS = STATE / "_cl_deltas.json"
OUT = STATE / "_cl_mine_out.json"
OUT_TXT = STATE / "_cl_mine_out.txt"


def content_to_text(content, max_chars=12000):
    if content is None:
        return ""
    if isinstance(content, str):
        return content[:max_chars]
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                if c.get("type") == "text" or "text" in c:
                    parts.append(c.get("text") or "")
                elif c.get("type") == "tool_result":
                    continue
                else:
                    # skip images etc
                    continue
            elif isinstance(c, str):
                parts.append(c)
        return "\n".join(parts)[:max_chars]
    if isinstance(content, dict):
        return (content.get("text") or str(content))[:max_chars]
    return str(content)[:max_chars]


def extract_user_texts(path, max_chars=12000):
    texts = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue

                role = obj.get("role")
                msg = obj.get("message")
                if isinstance(msg, dict) and msg.get("role"):
                    role = msg.get("role")

                if role not in ("user", "human"):
                    continue

                content = None
                if isinstance(msg, dict) and "content" in msg:
                    content = msg.get("content")
                elif "content" in obj:
                    content = obj.get("content")

                text = content_to_text(content, max_chars)
                if text.strip():
                    texts.append(text)
    except Exception as e:
        return [f"ERROR: {e}"]
    return texts


def main():
    deltas = json.loads(DELTAS.read_text(encoding="utf-8"))
    parents = []
    subagents = []
    for d in deltas["deltas"]:
        p = d["path"].replace("\\", "/")
        if "/subagents/" in p:
            subagents.append(d)
        else:
            parents.append(d)

    results = {
        "meta": {
            "delta_count": len(deltas["deltas"]),
            "removed_count": len(deltas.get("removed", [])),
            "parents": len(parents),
            "subagents": len(subagents),
        },
        "parents": [],
    }

    lines_out = []
    for d in parents:
        texts = extract_user_texts(d["path"])
        compact = []
        for t in texts:
            t2 = re.sub(r"\s+", " ", t).strip()
            compact.append(t2[:2500])
        entry = {
            "uuid": d["uuid"],
            "reason": d["reason"],
            "path": d["path"],
            "user_msg_count": len(texts),
            "user_msgs": compact,
        }
        results["parents"].append(entry)
        lines_out.append(f"\n=== {d['uuid']} ({d['reason']}) msgs={len(texts)} ===")
        for i, m in enumerate(compact[:25]):
            lines_out.append(f"U{i}: {m[:1200]}")
            lines_out.append("---")

    # Also mine non-trivial subagents briefly for user corrections embedded in prompts
    sub_hits = []
    for d in subagents:
        texts = extract_user_texts(d["path"], max_chars=4000)
        # only keep if looks like user correction / preference language
        joined = " ".join(texts).lower()
        keywords = (
            "always",
            "never",
            "prefer",
            "don't",
            "do not",
            "must",
            "rule",
            "remember",
            "from now",
            "agents.md",
            "preference",
        )
        if any(k in joined for k in keywords) and len(joined) > 80:
            sub_hits.append(
                {
                    "uuid": d["uuid"],
                    "path": d["path"],
                    "snippet": re.sub(r"\s+", " ", texts[0]).strip()[:800] if texts else "",
                }
            )
    results["subagent_keyword_hits"] = sub_hits

    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    OUT_TXT.write_text("\n".join(lines_out), encoding="utf-8")
    # print ascii-safe summary to console
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(results["meta"], indent=2))
    print(f"wrote {OUT}")
    print(f"wrote {OUT_TXT}")
    print(f"parents with msgs: {sum(1 for p in results['parents'] if p['user_msg_count'])}")
    print(f"subagent keyword hits: {len(sub_hits)}")
    for p in results["parents"]:
        if p["user_msg_count"]:
            print(f"  {p['uuid']}: {p['user_msg_count']} msgs")


if __name__ == "__main__":
    main()
