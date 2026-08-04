#!/usr/bin/env python3
"""Scoped validation for a single Novopay service/module.

Agents should prefer this over a full monorepo rebuild.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run(cmd: list[str], cwd: Path) -> int:
    print(f"+ [{' '.join(cmd)}] (cwd={cwd})")
    completed = subprocess.run(cmd, cwd=str(cwd), check=False)
    return int(completed.returncode)


def _gradle_cmd(service: Path) -> list[str]:
    if os.name == "nt":
        bat = service / "gradlew.bat"
        if bat.exists():
            return [str(bat)]
    gradlew = service / "gradlew"
    if gradlew.exists():
        return [str(gradlew)]
    raise SystemExit(f"No gradlew in {service}")


def _has_npm_script(service: Path, name: str) -> bool:
    package_json = service / "package.json"
    if not package_json.exists():
        return False
    try:
        import json

        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    scripts = data.get("scripts") or {}
    return name in scripts


def validate_service(service: Path, *, run_tests: bool) -> int:
    if (service / "gradlew").exists() or (service / "gradlew.bat").exists():
        cmd = _gradle_cmd(service)
        task = "test" if run_tests else "compileJava"
        # Many modules use compileJava; fall back to build if needed by caller.
        return _run([*cmd, task, "-q"], service)

    if (service / "package.json").exists():
        if run_tests and _has_npm_script(service, "test"):
            return _run(["npm", "test", "--", "--watchAll=false"], service)
        if _has_npm_script(service, "build"):
            return _run(["npm", "run", "build"], service)
        raise SystemExit(f"No npm test/build script in {service}")

    raise SystemExit(
        f"Unsupported service layout at {service}. "
        "Expected gradlew or package.json. See README.md."
    )


def lint_service(service: Path) -> int:
    if _has_npm_script(service, "lint"):
        return _run(["npm", "run", "lint"], service)
    if (service / ".eslintrc.json").exists() or (service / ".eslintrc.js").exists():
        return _run(["npx", "eslint", "."], service)
    if (service / "gradlew").exists() or (service / "gradlew.bat").exists():
        # No unified Java lint at root; compile is the cheap signal.
        return validate_service(service, run_tests=False)
    raise SystemExit(f"No lint tooling found under {service}")


def format_service(service: Path) -> int:
    if _has_npm_script(service, "format"):
        return _run(["npm", "run", "format"], service)
    if (service / ".prettierrc").exists() or (service / ".prettierrc.js").exists():
        return _run(["npx", "prettier", "--write", "."], service)
    raise SystemExit(f"No format tooling found under {service}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate/lint one Novopay service without a full monorepo loop."
    )
    parser.add_argument(
        "service",
        nargs="?",
        help="Service directory relative to workspace root "
        "(e.g. novopay-platform-api-gateway)",
    )
    parser.add_argument("--lint", action="store_true", help="Run lint/format-check path")
    parser.add_argument("--format", action="store_true", help="Run formatter when available")
    parser.add_argument("--test", action="store_true", help="Run unit tests when supported")
    args = parser.parse_args()

    if not args.service:
        parser.print_help()
        print(
            "\nExample: python scripts/validate-change.py novopay-platform-api-gateway",
            file=sys.stderr,
        )
        return 2

    service = (ROOT / args.service).resolve()
    if not service.exists() or not service.is_dir():
        raise SystemExit(f"Service directory not found: {service}")
    try:
        service.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit(f"Service must be inside workspace root: {ROOT}") from exc

    if args.format:
        return format_service(service)
    if args.lint:
        return lint_service(service)
    return validate_service(service, run_tests=args.test)


if __name__ == "__main__":
    sys.exit(main())
