#!/usr/bin/env python3
from pathlib import Path
import json

deltas = json.loads(
    Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\_cl_deltas.json").read_text(
        encoding="utf-8"
    )
)
parents = [d for d in deltas["deltas"] if "subagents" not in d["path"].replace("\\", "/")]
for d in parents[:3] + parents[-2:]:
    p = Path(d["path"])
    print("\n====", d["uuid"], "exists", p.exists(), "size", p.stat().st_size if p.exists() else 0)
    if not p.exists():
        continue
    with open(p, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    print("lines", len(lines))
    for i, line in enumerate(lines[:5]):
        try:
            obj = json.loads(line)
        except Exception as e:
            print("line", i, "parse fail", e, line[:200])
            continue
        print("line", i, "keys", list(obj.keys())[:30])
        print("  role?", obj.get("role"), "type?", obj.get("type"))
        msg = obj.get("message")
        if isinstance(msg, dict):
            print("  message.role", msg.get("role"), "content type", type(msg.get("content")).__name__)
            c = msg.get("content")
            if isinstance(c, str):
                print("  content[:400]", c[:400])
            elif isinstance(c, list) and c:
                print("  content[0] type", type(c[0]).__name__)
                if isinstance(c[0], dict):
                    print("  content[0] keys", list(c[0].keys()))
                    print("  content[0] sample", str(c[0])[:500])
        print("  raw[:350]", line[:350])

# Also check if paths point to wrong nesting (uuid folder mismatch)
print("\n==== path sanity ====")
for d in parents[:5]:
    p = Path(d["path"])
    print(d["uuid"], "->", p.exists(), p)
