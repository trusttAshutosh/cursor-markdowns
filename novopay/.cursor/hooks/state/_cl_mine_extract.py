import json
import re
from pathlib import Path

deltas_path = Path(r"C:/Users/ashutosh.kumar/Desktop/novopay/.cursor/hooks/state/_cl_deltas.json")
with open(deltas_path, encoding="utf-8") as f:
    payload = json.load(f)


def is_cl_meta(path: str) -> bool:
    return "eb569f50-4460-4cec-87cd-f3785d414fc5" in path.replace("\\", "/")


def extract_text(content) -> str:
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                if c.get("type") == "text":
                    parts.append(c.get("text", ""))
                elif "text" in c:
                    parts.append(str(c["text"]))
            else:
                parts.append(str(c))
        return "\n".join(parts)
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return content.get("text") or json.dumps(content)[:2000]
    return str(content) if content else ""


user_extracts = []
for d in payload["deltas"]:
    path = Path(d["path"])
    if is_cl_meta(str(path)):
        continue
    if not path.exists():
        continue
    texts = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = obj.get("role") or ""
            msg = obj.get("message") or obj.get("content") or obj
            if isinstance(msg, dict):
                role = msg.get("role", role)
                content = msg.get("content")
            else:
                content = msg if role else None
                if content is None and obj.get("type") in ("user", "human", "user_message"):
                    content = obj.get("content") or obj.get("text")
                    role = "user"
            if role not in ("user", "human") and obj.get("type") not in (
                "user",
                "human",
                "user_message",
            ):
                continue
            text = extract_text(content).strip()
            if not text:
                continue
            if "Run the full continual-learning" in text or "agents-memory-updater" in text:
                continue
            m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.DOTALL)
            if m:
                text = m.group(1).strip()
            if len(text) > 2500:
                text = text[:2500] + "...[trunc]"
            texts.append(text)
    if texts:
        user_extracts.append(
            {
                "uuid": d["uuid"],
                "reason": d["reason"],
                "path": d["path"],
                "is_subagent": "subagents" in d["path"].replace("\\", "/"),
                "user_msgs": texts[:40],
                "user_msg_count": len(texts),
            }
        )

parents = [u for u in user_extracts if not u["is_subagent"]]
subs = [u for u in user_extracts if u["is_subagent"]]
print(f"parent_chats_with_user={len(parents)} subagents_with_user={len(subs)}")

out_dir = Path(r"C:/Users/ashutosh.kumar/Desktop/novopay/.cursor/hooks/state/_cl_mine")
out_dir.mkdir(exist_ok=True)

summary_lines = []
for u in parents:
    summary_lines.append("=" * 80)
    summary_lines.append(f"UUID {u['uuid']} ({u['reason']}) msgs={u['user_msg_count']}")
    summary_lines.append(u["path"])
    for i, t in enumerate(u["user_msgs"], 1):
        summary_lines.append(f"--- USER #{i} ---")
        summary_lines.append(t)
        summary_lines.append("")

for u in subs:
    joined = "\n".join(u["user_msgs"]).lower()
    keys = ("prefer", "always", "never", "do not", "don't", "remember", "from now", "rule", "correction")
    if any(k in joined for k in keys):
        summary_lines.append("=" * 80)
        summary_lines.append(f"SUBAGENT {u['uuid']} ({u['reason']})")
        for i, t in enumerate(u["user_msgs"][:5], 1):
            summary_lines.append(f"--- USER #{i} ---")
            summary_lines.append(t[:1500])

out_file = out_dir / "user_messages.txt"
out_file.write_text("\n".join(summary_lines), encoding="utf-8")
print(f"wrote {out_file} chars={out_file.stat().st_size}")
print("parent uuids:")
for p in parents:
    print(f"  {p['uuid']} msgs={p['user_msg_count']}")
