"""Tests for bob shrink-logs."""
from __future__ import annotations

import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "lib"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

from shrink_logs import (  # noqa: E402
    looks_like_log_blob,
    shrink_lines,
    shrink_text,
)


def _sample_log() -> str:
    noise = "\n".join(f"2026-08-08 10:00:00.000 INFO  heartbeat ok #{i}" for i in range(200))
    error_block = """
2026-08-08 10:05:01.123 ERROR in.novopay.creditcard FooProcessor STAN=abc-123 client_reference=CRN-9
NovopayFatalException: 4000181 - Bank timeout
\tat in.novopay.creditcard.FooProcessor.process(FooProcessor.java:42)
\tat in.novopay.platform.AbstractProcessor.run(AbstractProcessor.java:10)
Caused by: java.net.SocketTimeoutException: Read timed out
""".strip()
    tail_noise = "\n".join(f"2026-08-08 10:06:00.000 INFO  idle #{i}" for i in range(100))
    return noise + "\n" + error_block + "\n" + tail_noise


def test_shrink_keeps_errors_and_reduces_size() -> None:
    lines = _sample_log().splitlines()
    digest, high_count, blocks = shrink_lines(lines)
    text = "\n".join(digest)
    assert high_count >= 1
    assert "4000181" in text
    assert "STAN=abc-123" in text
    assert "SocketTimeoutException" in text
    assert len(digest) < len(lines) / 2


def test_shrink_text_writes_full_and_digest(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("shrink_logs.infer_workspace_root", lambda: tmp_path)
    raw = _sample_log()
    result = shrink_text(raw, source="test.log", out_dir=tmp_path / "out")
    assert result.full_path.is_file()
    assert result.digest_path.is_file()
    assert result.original_lines == len(raw.splitlines())
    assert result.digest_lines < result.original_lines
    assert result.reduction_pct > 50.0
    full = result.full_path.read_text(encoding="utf-8")
    assert full == raw + "\n"
    latest = tmp_path / ".cursor" / "evidence" / "logs" / "latest.json"
    assert latest.is_file()
    from shrink_logs import resolve_latest_full_log  # noqa: E402

    assert resolve_latest_full_log() == result.full_path


def test_shrink_keeps_journey_success_before_error() -> None:
    lines = [
        "2026-08-08 10:00:00 INFO  heartbeat",
        "2026-08-08 10:01:00 INFO  InitiateKycProcessor BEGIN STAN=abc",
        "2026-08-08 10:01:01 INFO  request-out bank kyc initiate completed successfully",
        "2026-08-08 10:01:02 INFO  response-in status=SUCCESS",
    ] + [f"2026-08-08 10:02:00 INFO  noise filler {i}" for i in range(80)] + [
        "2026-08-08 10:05:00 ERROR ApplyKycProcessor NovopayFatalException 4000181",
    ]
    digest, _, _ = shrink_lines(lines)
    text = "\n".join(digest)
    assert "InitiateKycProcessor" in text
    assert "request-out" in text or "response-in" in text
    assert "4000181" in text
