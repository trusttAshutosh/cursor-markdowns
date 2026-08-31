---
name: ref-machine-commands
description: "Windows machine command constraints — PowerShell blocked patterns and working substitutes (git, gradle)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-25T09:55:06.084Z
---

Deepankar's Windows machine has setup/permission constraints. Do **not** retry broken commands — use the
substitutes below. Core rule is also in CLAUDE.md.

**Hard rule:** after any PowerShell failure (permission, execution policy, `cannot spawn`, GCM, empty
exit 128), stop using PowerShell for that job and switch to **Git Bash** (`C:\Program Files\Git\bin\bash.exe`)
+ plain `git`, or hand the user copy-paste commands. No second PowerShell attempt for the same git job.

### Blocked → substitute

| Blocked pattern | Reason | Use instead |
|---|---|---|
| `powershell -NoProfile -File C:\Users\ashutosh.kumar\Desktop\novopay\tools\*.ps1` | permission / execution policy / machine load | per-repo `git` / Git Bash; user runs script locally |
| Re-running PowerShell for **git** after one permission/spawn/GCM failure | burns turns | Git Bash + `git`, or user copy-paste |
| `git` when `mingw64\bin\git.exe` missing / `BUG (fork bomb)` | broken Git for Windows | Admin reboot + `winget install --id Git.Git -e`; verify `mingw64\bin\git.exe`. (Last fix → 2.55.0.windows.3) |
| `cannot spawn .git/hooks/pre-commit` (`#!/bin/sh` stubs) | shebang hooks fail from some agent shells | Git Bash commit; or `.cmd` → `bash.exe` + `git-hooks/*.sh` |
| `git push` exit 128 at `credential-manager get` | GCM interactive auth blocked in agent | user pushes `git push origin <branch>` as **deepankar-np** |
| `git commit` via PowerShell with a `--trailer "Co-authored-by: X <…>"` | PS parses `<…>` as redirection → empty message | write msg file + `bash.exe script.sh` with `git commit -F file` |
| `npx md-to-pdf` | Chromium download, slow | markdowntoword.io Markdown→PDF (user converts) |
| `C:\Python314\python.exe` / Store `python` alias | not installed / Store stub | parse with PowerShell/Grep, or install real Python |

### Gradle "Unable to establish loopback connection" (this machine — Ashutosh's)

Every Gradle build (and any `Selector.open()` in any JVM) fails with
`java.io.IOException: Unable to establish loopback connection`, root cause
`SocketException: Invalid argument: connect` in `sun.nio.ch.UnixDomainSockets.connect0`.
The JDK builds selector wake-up pipes on an AF_UNIX socket in `%TEMP%`
(`C:\Users\ASHUTO~1.KUM\...` — the 8.3 short-name path breaks it). It is **not** the
firewall/FortiClient blocking TCP — raw loopback TCP and NIO connects work fine.

**Fix (verified 2026-08-25):** point the unix-socket dir somewhere clean, for every Gradle JVM:

```
set JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Users/ashutosh.kumar/tmpnio
.\gradlew.bat compileJava --no-daemon
```

(`C:\Users\ashutosh.kumar\tmpnio` must exist. cmd also needs the `.\` prefix on
`gradlew.bat` — bare `gradlew.bat` is "not recognized": cwd exe search is disabled.)

### Working patterns

| Task | Command |
|---|---|
| Read-only git | `git -C "C:\Users\ashutosh.kumar\Desktop\novopay\<repo>" status\|log\|diff\|fetch` |
| Commit / push / hooks-sensitive git | `"C:\Program Files\Git\bin\bash.exe"` → `cd /c/novopay/<repo>` → `git …` |
| Compile one microservice | `.\gradlew.bat compileJava --no-daemon` (+ JAVA_TOOL_OPTIONS fix above) |
| Install branch-guard hooks | `.\gradlew.bat installGitHooks --no-daemon` |
| Search code | dedicated Grep/Read tools, not huge PS `rg` |

Related: [[pref-working-style]], [[pref-git-workflow]], [[ref-workspace-tools]].
