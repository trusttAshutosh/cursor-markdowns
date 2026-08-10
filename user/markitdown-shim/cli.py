"""
CLI: convert a local file to Markdown via MarkItDown (magika-stubbed on py314).

Usage:
  python cli.py path/to/file.pdf
  python cli.py path/to/file.docx -o out.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _install_magika_stub() -> None:
    import types

    if "magika" in sys.modules:
        return

    mod = types.ModuleType("magika")

    class _Output:
        label = "unknown"
        mime_type = None
        extensions: list[str] = []
        is_text = False

    class _Prediction:
        output = _Output()

    class _Result:
        status = "unavailable"
        prediction = _Prediction()

    class Magika:
        def identify_stream(self, *_args, **_kwargs):
            return _Result()

        def identify_bytes(self, *_args, **_kwargs):
            return _Result()

        def identify_path(self, *_args, **_kwargs):
            return _Result()

    mod.Magika = Magika
    sys.modules["magika"] = mod


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert file to Markdown (MarkItDown)")
    parser.add_argument("path", help="Local file path (pdf/docx/xlsx/pptx/html/...)")
    parser.add_argument("-o", "--output", help="Write markdown to this file")
    args = parser.parse_args()

    src = Path(args.path).expanduser().resolve()
    if not src.is_file():
        print(f"File not found: {src}", file=sys.stderr)
        return 1

    _install_magika_stub()
    from markitdown import MarkItDown

    result = MarkItDown().convert(str(src))
    text = result.markdown or ""

    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out} ({len(text)} chars)")
    else:
        sys.stdout.write(text)
        if text and not text.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
