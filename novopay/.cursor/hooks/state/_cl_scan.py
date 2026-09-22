import json
from pathlib import Path
from collections import Counter

INDEX = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\continual-learning-index.json")
TRANSCRIPTS = Path(r"C:\Users\ashutosh.kumar\.cursor\projects\c-Users-ashutosh-kumar-Desktop-novopay\agent-transcripts")
OUT = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\_cl_to_process.json")

with INDEX.open(encoding="utf-8") as f:
    idx = json.load(f)

processed = idx.get("processedTranscripts", {})
files = list(TRANSCRIPTS.rglob("*.jsonl"))
print(f"total_transcripts_in_dir={len(files)}")
print(f"index_entries={len(processed)}")

by_id = dict(processed)

to_process = []
for fp in files:
    st = fp.stat()
    mtime = st.st_mtime
    stem = fp.stem
    abs_path = str(fp.resolve())

    in_index = stem in by_id
    indexed_mtime = by_id[stem].get("mtime") if in_index else None

    if not in_index:
        for tid, meta in processed.items():
            ip = meta.get("path", "").replace("\\", "/").lower()
            if Path(ip).name == stem + ".jsonl" or Path(ip).stem == stem:
                in_index = True
                indexed_mtime = meta.get("mtime")
                break

    needs = False
    reason = ""
    if not in_index:
        needs = True
        reason = "not_in_index"
    elif indexed_mtime is None or mtime > float(indexed_mtime) + 0.001:
        needs = True
        reason = "newer_mtime"

    if needs:
        to_process.append(
            {
                "path": abs_path,
                "id": stem,
                "mtime": mtime,
                "size": st.st_size,
                "reason": reason,
                "is_subagent": "subagents" in str(fp),
            }
        )

to_process.sort(key=lambda x: x["mtime"], reverse=True)
print(f"to_process={len(to_process)}")
print(f"parent_chats={sum(1 for x in to_process if not x['is_subagent'])}")
print(f"subagents={sum(1 for x in to_process if x['is_subagent'])}")
print("--- all parent chats to process ---")
for x in to_process:
    if not x["is_subagent"]:
        print(f"{x['reason']:12} size={x['size']:8} mtime={x['mtime']:.0f} {x['id']}")
print("--- subagents by reason ---")
print(dict(Counter(x["reason"] for x in to_process if x["is_subagent"])))

with OUT.open("w", encoding="utf-8") as f:
    json.dump(to_process, f, indent=2)
print(f"wrote {OUT}")
