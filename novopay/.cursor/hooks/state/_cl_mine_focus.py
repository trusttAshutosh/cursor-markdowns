# -*- coding: utf-8 -*-
from pathlib import Path
import re
import json

text = Path(r"C:/Users/ashutosh.kumar/Desktop/novopay/.cursor/hooks/state/_cl_mine/user_messages.txt").read_text(encoding="utf-8")

# Focus on recent parent chats (Sep 17-18 era) - exclude ancient touch-only updates
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
    m = re.search(
        rf"UUID {uuid}.*?(?=\n={80}\nUUID |\Z)",
        text,
        re.DOTALL,
    )
    if not m:
        out_lines.append(f"MISSING {uuid}")
        continue
    block = m.group(0)
    # strip agent system reminders
    cleaned_msgs = []
    for um in re.finditer(r"--- USER #(\d+) ---\n(.*?)(?=\n--- USER #|\Z)", block, re.DOTALL):
        content = um.group(2).strip()
        if "Briefly inform the user about the task result" in content:
            continue
        if content.startswith("The \"Antipatterns\" quality gate"):
            cleaned_msgs.append(f"#{um.group(1)} [CODEANT_GATE] " + content[:500])
            continue
        if "BUILD FAILED" in content and "generateFlywayScriptAuthors" in content:
            cleaned_msgs.append(f"#{um.group(1)} [BUILD_FAIL_PASTE] " + content[:400])
            continue
        cleaned_msgs.append(f"#{um.group(1)} ({len(content)} chars)\n{content[:2000]}")
    out_lines.append("=" * 70)
    out_lines.append(uuid)
    out_lines.extend(cleaned_msgs if cleaned_msgs else ["(no usable user msgs)"])

out = Path(r"C:/Users/ashutosh.kumar/Desktop/novopay/.cursor/hooks/state/_cl_mine/focus.txt")
out.write_text("\n\n".join(out_lines), encoding="utf-8")
print(f"wrote {out} size={out.stat().st_size}")
