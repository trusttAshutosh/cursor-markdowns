"""Shrink large log files for Cursor/Bob - preserve full copy, emit token-safe digest."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from host_repo import infer_workspace_root

# Novopay / Spring / JVM high-signal patterns (case-insensitive).
HIGH_SIGNAL = re.compile(
    r"(?i)"
    r"(?:\berror\b|\bwarn(?:ing)?\b|\bfatal\b|\bfail(?:ed|ure)?\b|"
    r"exception|throwable|novopayfatal|novopaynonfatal|"
    r"caused by|\bat in\.|\bat java\.|\bat org\.|\bat com\.|"
    r"stacktrace|4000\d{3}|response[_ ]code|error[_ ]code|"
    r"\bstan\b|client[_ ]?reference|clientreferencecode|"
    r"\bbegin\b|\bend\b|rejected|timeout|refused|denied|rollback|"
    r"NovopayFatalException|NovopayNonFatalException)"
)

# Journey / success markers - keep so "X succeeded then Y failed" stays visible.
JOURNEY_SIGNAL = re.compile(
    r"(?i)"
    r"(?:request[- ]out|response[- ]in|"
    r"executeservice|doservicecall|"
    r"transactionaudit|selected_api_channel|"
    r"processor\b|abstractcreditcardmanager|abstractprocessor|"
    r"\bsuccess\b|completed|status[=:]\s*success|"
    r"response received|bank response|"
    r"initiatekyc|applykyc|getkyc|submitloan|"
    r"createorupdate|fetch.*processor)"
)

STACK_CONT = re.compile(
    r"(?i)^(\s+at\s+|\s*\.\.\.\s+\d+\s+more|\s*Caused by:|^\s*Suppressed:)"
)

TIMESTAMP_PREFIX = re.compile(
    r"^(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d{3})?(?:\s+\S+)?\s+)"
)

DEFAULT_CONTEXT = 5
DEFAULT_HEAD_TAIL = 5
DEFAULT_MIN_REPEAT = 4
SHRINK_THRESHOLD_LINES = 40
GAP_BRIDGE_THRESHOLD = 30
LATEST_SHRINK_REL = Path(".cursor/evidence/logs/latest.json")


@dataclass
class ShrinkResult:
    source: str
    original_lines: int
    digest_lines: int
    full_path: Path
    digest_path: Path
    reduction_pct: float
    high_signal_count: int
    collapsed_repeat_blocks: int = 0

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "original_lines": self.original_lines,
            "digest_lines": self.digest_lines,
            "reduction_pct": round(self.reduction_pct, 1),
            "high_signal_count": self.high_signal_count,
            "collapsed_repeat_blocks": self.collapsed_repeat_blocks,
            "full_path": str(self.full_path),
            "digest_path": str(self.digest_path),
        }


def _normalize_for_repeat(line: str) -> str:
    return TIMESTAMP_PREFIX.sub("", line.rstrip())


def _is_high_signal(line: str) -> bool:
    return bool(HIGH_SIGNAL.search(line))


def _is_journey_signal(line: str) -> bool:
    return bool(JOURNEY_SIGNAL.search(line))


def _is_keep_line(line: str) -> bool:
    return _is_high_signal(line) or _is_journey_signal(line)


def _add_gap_bridges(lines: list[str], keep: set[int]) -> None:
    """When two kept regions are far apart, sample 1-2 lines from the gap."""
    if not keep:
        return
    ordered = sorted(keep)
    for a, b in zip(ordered, ordered[1:]):
        gap = b - a - 1
        if gap < GAP_BRIDGE_THRESHOLD:
            continue
        keep.add(a + gap // 3)
        keep.add(a + (2 * gap) // 3)


def _collect_keep_indices(lines: list[str], context: int) -> set[int]:
    keep: set[int] = set()
    n = len(lines)
    for i, line in enumerate(lines):
        if _is_keep_line(line):
            start = max(0, i - context)
            end = min(n, i + context + 1)
            keep.update(range(start, end))
            # Extend through stack-trace continuation lines.
            j = i + 1
            while j < n and STACK_CONT.match(lines[j]):
                keep.add(j)
                j += 1
    _add_gap_bridges(lines, keep)
    if n:
        keep.update(range(min(DEFAULT_HEAD_TAIL, n)))
        keep.update(range(max(0, n - DEFAULT_HEAD_TAIL), n))
    return keep


def _collapse_repeats(lines: list[str], min_repeat: int) -> tuple[list[str], int]:
    """Collapse runs of identical normalized lines outside explicit keep set."""
    if not lines:
        return [], 0
    out: list[str] = []
    blocks = 0
    i = 0
    n = len(lines)
    while i < n:
        norm = _normalize_for_repeat(lines[i])
        j = i + 1
        while j < n and _normalize_for_repeat(lines[j]) == norm:
            j += 1
        run_len = j - i
        if run_len >= min_repeat and not _is_keep_line(lines[i]):
            out.append(f"[... repeated {run_len}x: {lines[i].rstrip()}]")
            blocks += 1
            i = j
        else:
            out.extend(line.rstrip() for line in lines[i:j])
            i = j
    return out, blocks


def shrink_lines(
    lines: list[str],
    *,
    context: int = DEFAULT_CONTEXT,
    min_repeat: int = DEFAULT_MIN_REPEAT,
) -> tuple[list[str], int, int]:
    """Return digest lines, high_signal_count, collapsed_blocks."""
    if not lines:
        return [], 0, 0

    keep = _collect_keep_indices(lines, context)
    high_count = sum(1 for i, ln in enumerate(lines) if i in keep and _is_high_signal(ln))

    # Pass 1: keep high-signal windows + head/tail only.
    selected = [lines[i].rstrip() for i in sorted(keep)]

    # Pass 2: collapse long identical runs in the selected subset.
    digest, blocks = _collapse_repeats(selected, min_repeat)
    return digest, high_count, blocks


def _default_out_dir(ticket: str | None = None) -> Path:
    ws = infer_workspace_root()
    base = (ws or Path.cwd()) / ".cursor" / "evidence" / "logs"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = f"-{ticket}" if ticket else ""
    return base / f"{stamp}{suffix}"


def shrink_text(
    text: str,
    *,
    source: str = "-",
    out_dir: Path | None = None,
    ticket: str | None = None,
    context: int = DEFAULT_CONTEXT,
) -> ShrinkResult:
    lines = text.splitlines()
    out = out_dir or _default_out_dir(ticket)
    out.mkdir(parents=True, exist_ok=True)

    full_path = out / "full.log"
    digest_path = out / "digest.log"
    meta_path = out / "meta.json"

    full_path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")

    digest_lines, high_count, blocks = shrink_lines(lines, context=context)
    header = [
        "=== LOG DIGEST (bob shrink-logs) ===",
        f"source: {source}",
        f"original_lines: {len(lines)}",
        f"digest_lines: {len(digest_lines)}",
        f"full_preserved: {full_path}",
        "=== CONTENT ===",
    ]
    body = header + digest_lines
    digest_path.write_text("\n".join(body) + "\n", encoding="utf-8")

    reduction = 0.0
    if len(lines):
        reduction = (1.0 - len(digest_lines) / len(lines)) * 100.0

    result = ShrinkResult(
        source=source,
        original_lines=len(lines),
        digest_lines=len(digest_lines),
        full_path=full_path,
        digest_path=digest_path,
        reduction_pct=reduction,
        high_signal_count=high_count,
        collapsed_repeat_blocks=blocks,
    )
    meta_path.write_text(json.dumps(result.to_dict(), indent=2) + "\n", encoding="utf-8")
    _write_latest_pointer(result, ticket=ticket)
    return result


def _write_latest_pointer(result: ShrinkResult, *, ticket: str | None) -> None:
    ws = infer_workspace_root() or Path.cwd()
    latest = ws / LATEST_SHRINK_REL
    latest.parent.mkdir(parents=True, exist_ok=True)
    payload = result.to_dict()
    payload["created_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if ticket:
        payload["ticket"] = ticket
    latest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def resolve_latest_full_log() -> Path | None:
    ws = infer_workspace_root() or Path.cwd()
    latest = ws / LATEST_SHRINK_REL
    if not latest.is_file():
        return None
    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    full = Path(str(data.get("full_path", "")))
    return full if full.is_file() else None


def looks_like_log_blob(text: str) -> bool:
    """Heuristic: pasted chat content is probably logs."""
    lines = text.splitlines()
    if len(lines) >= SHRINK_THRESHOLD_LINES:
        return True
    sample = "\n".join(lines[:200])
    if HIGH_SIGNAL.search(sample):
        return True
    ts_hits = sum(1 for ln in lines[:100] if TIMESTAMP_PREFIX.match(ln))
    return ts_hits >= 5


def format_summary(result: ShrinkResult) -> str:
    return (
        f"Shrunk {result.original_lines} -> {result.digest_lines} lines "
        f"({result.reduction_pct:.1f}% reduction). "
        f"Digest: {result.digest_path}\n"
        f"Full preserved: {result.full_path}"
    )


def run_shrink_logs_cli(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Shrink logs for Cursor - full copy preserved on disk.")
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        help="Log file path, or '-' / omit for stdin",
    )
    parser.add_argument("--ticket", help="Optional ticket id for output folder name")
    parser.add_argument("--out", type=Path, help="Output directory (default: .cursor/evidence/logs/<ts>/)")
    parser.add_argument("--context", type=int, default=DEFAULT_CONTEXT, help="Context lines around signals")
    parser.add_argument("--json", action="store_true", help="Print JSON summary only")
    parser.add_argument("--quiet", action="store_true", help="Print digest path only")
    ns = parser.parse_args(args)

    src = ns.file
    if src in ("-", ""):
        text = sys.stdin.read()
        source_label = "stdin"
    else:
        path = Path(src)
        if not path.is_file():
            print(f"Not a file: {path}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8", errors="replace")
        source_label = str(path)

    if not text.strip():
        print("Empty input.", file=sys.stderr)
        return 1

    result = shrink_text(
        text,
        source=source_label,
        out_dir=ns.out,
        ticket=ns.ticket,
        context=ns.context,
    )

    if ns.json:
        print(json.dumps(result.to_dict(), indent=2))
    elif ns.quiet:
        print(result.digest_path)
    else:
        print(format_summary(result))
        print(f"\n--- digest preview (first 40 lines) ---")
        digest_body = result.digest_path.read_text(encoding="utf-8").splitlines()
        for ln in digest_body[:40]:
            print(ln)
        if len(digest_body) > 40:
            print(f"... ({len(digest_body) - 40} more lines in digest file)")
    return 0
