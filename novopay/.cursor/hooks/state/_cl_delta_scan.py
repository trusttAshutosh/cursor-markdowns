import json
import os
import glob
from pathlib import Path
from collections import Counter

index_path = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\continual-learning-index.json")
with open(index_path, encoding="utf-8") as f:
    idx = json.load(f)

processed = idx.get("processedTranscripts", {})
print("indexed", len(processed))
print("lastUpdated", idx.get("lastUpdated"))

roots = glob.glob(r"C:\Users\ashutosh.kumar\.cursor\projects\c-Users-ashutosh-kumar-Desktop-novopay*\agent-transcripts")
files = []
for root in roots:
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".jsonl"):
                files.append(Path(dirpath) / fn)

print("on_disk", len(files))


def tid_from_path(p: Path):
    return p.stem


def norm(p):
    return str(p).replace("\\", "/")


delta = []
missing_from_disk = []
for tid, meta in processed.items():
    p = Path(meta["path"])
    if not p.exists():
        missing_from_disk.append(tid)

for p in files:
    tid = tid_from_path(p)
    mtime = p.stat().st_mtime
    meta = processed.get(tid)
    if meta is None:
        delta.append((tid, str(p), mtime, "NEW"))
    else:
        indexed_mtime = meta.get("mtime", 0)
        if mtime > indexed_mtime + 0.001:
            delta.append((tid, str(p), mtime, "NEWER"))

parents = [d for d in delta if "/subagents/" not in norm(d[1])]
subs = [d for d in delta if "/subagents/" in norm(d[1])]

print("delta_total", len(delta), "parents", len(parents), "subs", len(subs))
print("missing_from_disk", len(missing_from_disk))

parents.sort(key=lambda x: x[2], reverse=True)
print("\n=== PARENT DELTAS (newest first, up to 50) ===")
for row in parents[:50]:
    print(f"{row[3]:6} {row[2]:.0f} {row[0]}")
    print(f"       {row[1]}")

c = Counter()
for tid, path, mt, why in subs:
    parts = Path(path).parts
    try:
        i = list(parts).index("subagents")
        c[parts[i - 1]] += 1
    except ValueError:
        c["?"] += 1
print("\nsub deltas by parent", dict(c.most_common(15)))

out = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\_cl_delta_tmp.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(
        {
            "parents": [{"id": a, "path": b, "mtime": c, "why": d} for a, b, c, d in parents],
            "subs": [{"id": a, "path": b, "mtime": c, "why": d} for a, b, c, d in subs],
            "missing": missing_from_disk,
            "all_files": [
                {"id": tid_from_path(p), "path": str(p), "mtime": p.stat().st_mtime} for p in files
            ],
        },
        f,
    )
print("wrote", out, "parents", len(parents))
