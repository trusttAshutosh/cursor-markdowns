# MarkItDown py314 shim (optional)

Stubs `magika` so MarkItDown runs on Windows Python 3.14 without onnxruntime<=1.20.1.

## MCP (Cursor)

Configured in `~/.cursor/mcp.json` as `markitdown`.

- Keep **disabled** in Cursor Settings > MCP until you need a PDF/Office conversion.
- When enabled, agent tool: `convert_to_markdown(uri)` with `file:`, `http:`, `https:`, or `data:` URI.

## CLI

```bash
python ~/.cursor/tools/markitdown-shim/cli.py "/path/to/spec.pdf"
python ~/.cursor/tools/markitdown-shim/cli.py "/path/to/map.xlsx" -o /tmp/out.md
```

## Slash

`/markitdown` - convert an attached or path-given Office/PDF file; do not use for logs/code.

## Restore on a new laptop

1. Copy this folder to `~/.cursor/tools/markitdown-shim/`
2. `pip install --no-deps markitdown==0.1.3 markitdown-mcp`
3. `pip install beautifulsoup4 charset-normalizer defusedxml markdownify requests 'mcp~=1.8.0' pdfminer.six python-docx openpyxl python-pptx`
4. Add to `~/.cursor/mcp.json`:

```json
"markitdown": {
  "command": "C:\Python314\python.exe",
  "args": ["C:\Users\ashutosh.kumar\.cursor\tools\markitdown-shim\run_mcp.py"]
}
```

5. Leave disabled in Cursor Settings > MCP until needed.
