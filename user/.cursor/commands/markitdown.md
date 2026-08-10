---
description: "Convert PDF/Word/Excel/PPT to Markdown via MarkItDown (auto on attachments when MCP on)"
---

# MarkItDown

Convert PDF / DOCX / XLSX / PPTX to Markdown before answering.

## Auto (when MCP `markitdown` is enabled)

If the user attached or linked a PDF/Office file in this message, **convert first** via `convert_to_markdown`, then answer from Markdown - do not read the raw attachment.

## Manual

1. MCP enabled: `convert_to_markdown` with `file:///...` or direct `https://.../file.pdf` URL.
2. MCP disabled: `python C:/Users/ashutosh.kumar/.cursor/tools/markitdown-shim/cli.py "<abs-path>"`
3. Summarize from Markdown - do not dump huge converted text unless asked.

Do **not** use for applogs, code, Jira/Confluence, or RCA log greps.
