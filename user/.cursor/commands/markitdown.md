---
description: "Optional - convert PDF/Word/Excel/PPT to Markdown via MarkItDown"
---

# MarkItDown (opt-in)

Convert a local PDF / DOCX / XLSX / PPTX (or URL) to Markdown for this chat.

1. If MCP server `markitdown` is disabled in Cursor Settings > MCP, ask user to enable it, or run CLI:
   `python C:/Users/ashutosh.kumar/.cursor/tools/markitdown-shim/cli.py "<path>"`
2. Prefer MCP tool `convert_to_markdown` with a `file:///...` URI when the server is enabled.
3. Summarize from the Markdown - do not dump huge converted text unless asked.
4. Do **not** use for applogs, code, Jira/Confluence (Atlassian MCP), or RCA log greps.
