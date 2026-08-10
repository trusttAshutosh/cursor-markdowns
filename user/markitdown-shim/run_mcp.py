"""
MarkItDown MCP launcher for Python 3.14 / Windows.

Official markitdown pins onnxruntime<=1.20.1 on win32 (no cp314 wheels).
This shim stubs magika so extension-based conversion (PDF/DOCX/XLSX/PPTX) still works.
"""
from __future__ import annotations

import sys
import types


def _install_magika_stub() -> None:
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


def main() -> None:
    _install_magika_stub()
    from markitdown_mcp.__main__ import main as mcp_main

    mcp_main()


if __name__ == "__main__":
    main()
