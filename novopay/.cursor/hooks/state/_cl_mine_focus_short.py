# -*- coding: utf-8 -*-
from pathlib import Path
import re

text = Path(r"C:/Users/ashutosh.kumar/Desktop/novopay/.cursor/hooks/state/_cl_mine/user_messages.txt").read_text(encoding="utf-8")

focus = [
    "75c6955f-f80a-41b3-ac7e-da41fc1ca13a",
    "65ca16a6-7039-49df-8170-1f4ed6e4d808",
    "d05af2a1-2758-48d0-9c7b-84651779d42b",
    "1dc4360a-3148-4573-8e30-fb795b51432c",
    "a3a4fcc9-5996-4dc6-9b2a-bc133a45a70b",
    "f448f228-62f8-450c-8970-1f549c64eaec",
    "ff96e707-1f7d-46da-a220-44d919fad31f",
    "a717ff40-a52c-4387-8eae-3b1071682f40",
    "3dcaf39a-5bac-4f41-9bc1-ae1dbaec78c7",
    "0198bc4e-6206-43ab-8c9d-cb15fec5cea8",
    "841c07b1-9cbd-4e67-931e-f1884b937327",
    "c246405c-1abf-4cfc-a2f7-1a1aaeb2aa6b",
    "c78e4b6c-5bbe-4ccb-8055-889d65c1a610",
    "413d480a-6abd-4235-ad45-6b356c53bd88",
    "6d631b7d-e04b-430a-9228-2b994db9a3b7",
    "56dc9aea-af5a-43df-a073-0f1c4ddbde0e",
]

out_lines = []
for uuid in focus:
    m = re.search(rf"UUID {uuid} \((\w+)\) msgs=(\d+)\n([^\n]+)\n(.*?)(?=\n={80}\nUUID |\Z)", text, re.DOTALL)
    if not m:
        out_lines.append(f"MISSING {uuid}")
        continue
    reason, msgs, path, body = m.groups()
    out_lines.append("=" * 70)
    out_lines.append(f"{uuid} reason={reason} msgs={msgs}")
    for um in re.finditer(r"--- USER #(\d+) ---\n(.*?)(?=\n--- USER #|\Z)", body, re.DOTALL):
        n = um.group(1)
        content = um.group(2).strip()
        if "Briefly inform the user about the task result" in content:
            continue
        # Drop huge binary-ish pastes: keep first 600 chars
        first = content[:600].replace("\r", "")
        # classify
        kind = "ask"
        if content.startswith("BUILD FAILED") or "gradlew" in content[:200]:
            kind = "build_paste"
        elif "Antipatterns" in content[:200]:
            kind = "codeant"
        elif len(content) > 3000:
            kind = "long_paste"
        out_lines.append(f"\n#{n} [{kind}] len={len(content)}")
        out_lines.append(first)
        if len(content) > 600:
            out_lines.append("...[trunc]")

out = Path(r"C:/Users/ashutosh.kumar/Desktop/novopay/.cursor/hooks/state/_cl_mine/focus_short.txt")
out.write_text("\n".join(out_lines), encoding="utf-8")
print(f"wrote {out} size={out.stat().st_size}")
