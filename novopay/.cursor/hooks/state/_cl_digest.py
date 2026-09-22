import json
import re
from pathlib import Path

OUT_LIST = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\_cl_to_process.json")
DIGEST = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\_cl_digest.md")

with OUT_LIST.open(encoding="utf-8") as f:
    items = json.load(f)

parents = [x for x in items if not x["is_subagent"]]
lines = []

for item in parents:
    path = Path(item["path"])
    lines.append(f"\n## {item['id']} ({item['reason']}, size={item['size']})\n")
    if not path.exists():
        lines.append("(missing)\n")
        continue
    user_turns = []
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = obj.get("role") or obj.get("type") or ""
            # common shapes
            if role not in ("user", "human"):
                # cursor jsonl often uses type
                t = obj.get("type", "")
                if t not in ("user", "user_message", "human"):
                    # check message.role
                    msg = obj.get("message") or obj.get("data") or {}
                    if isinstance(msg, dict):
                        if msg.get("role") not in ("user", "human"):
                            continue
                        content = msg.get("content")
                    else:
                        continue
                else:
                    content = obj.get("content") or obj.get("text") or obj.get("message")
            else:
                content = obj.get("content") or obj.get("text") or obj.get("message")

            text = ""
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                parts = []
                for p in content:
                    if isinstance(p, str):
                        parts.append(p)
                    elif isinstance(p, dict):
                        if p.get("type") in ("text", "input_text"):
                            parts.append(p.get("text", ""))
                        elif "text" in p:
                            parts.append(str(p.get("text", "")))
                text = "\n".join(parts)
            elif isinstance(content, dict):
                text = content.get("text") or json.dumps(content)[:2000]
            else:
                continue

            text = text.strip()
            if not text:
                continue
            # strip system noise / tool dumps
            if text.startswith("<") and "user_query" in text:
                m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.S)
                if m:
                    text = m.group(1).strip()
            # skip very large pastes
            if len(text) > 4000:
                text = text[:4000] + "\n...[truncated]..."
            user_turns.append(text)

    lines.append(f"user_turns={len(user_turns)}\n")
    for i, t in enumerate(user_turns, 1):
        lines.append(f"\n### turn {i}\n")
        lines.append(t)
        lines.append("\n")

DIGEST.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {DIGEST} chars={DIGEST.stat().st_size}")
print(f"parents={len(parents)}")
