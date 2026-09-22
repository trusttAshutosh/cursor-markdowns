import json
import re
from pathlib import Path

paths = [
    r"C:\Users\ashutosh.kumar\.cursor\projects\c-Users-ashutosh-kumar-Desktop-novopay\agent-transcripts\ff96e707-1f7d-46da-a220-44d919fad31f\ff96e707-1f7d-46da-a220-44d919fad31f.jsonl",
    r"C:\Users\ashutosh.kumar\.cursor\projects\c-Users-ashutosh-kumar-Desktop-novopay\agent-transcripts\c246405c-1abf-4cfc-a2f7-1a1aaeb2aa6b\c246405c-1abf-4cfc-a2f7-1a1aaeb2aa6b.jsonl",
    r"C:\Users\ashutosh.kumar\.cursor\projects\c-Users-ashutosh-kumar-Desktop-novopay\agent-transcripts\a717ff40-a52c-4387-8eae-3b1071682f40\a717ff40-a52c-4387-8eae-3b1071682f40.jsonl",
    r"C:\Users\ashutosh.kumar\.cursor\projects\c-Users-ashutosh-kumar-Desktop-novopay\agent-transcripts\56dc9aea-af5a-43df-a073-0f1c4ddbde0e\56dc9aea-af5a-43df-a073-0f1c4ddbde0e.jsonl",
    r"C:\Users\ashutosh.kumar\.cursor\projects\c-Users-ashutosh-kumar-Desktop-novopay\agent-transcripts\6d631b7d-e04b-430a-9228-2b994db9a3b7\6d631b7d-e04b-430a-9228-2b994db9a3b7.jsonl",
]

OUT = Path(r"C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\hooks\state\_cl_assistant_snippets.md")
chunks = []

for p in paths:
    path = Path(p)
    if not path.exists():
        continue
    chunks.append(f"\n# {path.stem}\n")
    asst = []
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            msg = obj.get("message") or {}
            role = msg.get("role") or obj.get("role") or ""
            if role != "assistant":
                continue
            content = msg.get("content")
            text = ""
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                parts = []
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        parts.append(c.get("text", ""))
                text = "\n".join(parts)
            if not text:
                continue
            # keep TL;DR / Summary / Bottom line / preference-like lines
            keep = []
            for para in re.split(r"\n{2,}", text):
                low = para.lower()
                if any(
                    k in low
                    for k in (
                        "tl;dr",
                        "summary",
                        "bottom line",
                        "preference",
                        "always",
                        "never",
                        "do not",
                        "masterdata",
                        "configuration",
                        "mobile match",
                        "phone_match",
                        "filler1",
                        "prop_key",
                        "hdfc.soa",
                        "pan",
                        "encrypt",
                        "simulator",
                        "digilocker",
                        "address",
                        "bank",
                    )
                ):
                    keep.append(para[:1500])
            if keep:
                asst.append("\n---\n".join(keep[:8]))
    # last few assistant high-signal chunks
    for i, a in enumerate(asst[-6:], 1):
        chunks.append(f"\n## asst snippet {i}\n{a}\n")

OUT.write_text("\n".join(chunks), encoding="utf-8")
print(f"wrote {OUT} size={OUT.stat().st_size}")
