---
name: ref-machine-commands
description: "Windows machine command constraints — PowerShell blocked patterns and working substitutes (git, gradle)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-09-06T03:05:00.000Z
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
The JDK builds selector wake-up pipes on an AF_UNIX socket in `%TEMP%`. AF_UNIX `connect`
fails with EINVAL for **any** socket file under `C:\Users\ashutosh.kumar\AppData\Local\Temp`
(verified 2026-09-06: long-form path fails too, so it is the folder, not the 8.3 short name;
`C:\Temp` works). Something filters that folder. It is **not** the firewall/FortiClient blocking
TCP — raw loopback TCP, NIO connects and `Pipe.open()` all work. Leftover `afunix-*.sock` files in
that Temp folder cannot be deleted (error 1920, even via `fsutil reparsepoint delete`) — ignore them.

**Fix (verified 2026-08-25):** point the unix-socket dir somewhere clean, for every Gradle JVM:

```
set JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Users/ashutosh.kumar/tmpnio
.\gradlew.bat compileJava --no-daemon
```

(`C:\Users\ashutosh.kumar\tmpnio` must exist. cmd also needs the `.\` prefix on
`gradlew.bat` — bare `gradlew.bat` is "not recognized": cwd exe search is disabled.)
Even `./gradlew help` fails without it (the client cannot reach its own single-use daemon), so
export it in Git Bash too: `export JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Users/ashutosh.kumar/tmpnio`.
Sandbox on/off makes no difference — do not waste a retry on `dangerouslyDisableSandbox`.

**Gradle-free fallback (verified 2026-09-03, task-allocation):** the repo's JDK 25 toolchain lives at
`~/.gradle/jdks/eclipse_adoptium-25-amd64-windows.2/bin` (`~/.jdks` only has 8/21 and cannot read the
v69 class files in `build/classes`). Compile `src/main/java` with that `javac -proc:none` against every
jar in `~/.gradle/caches/modules-2/files-2.1` + `~/.m2/repository/in/novopay` (one version per artifact,
pass `-cp` via an `@argfile` with `-cp` and the path on separate lines, no quotes) plus
`-sourcepath` on `novopay-platform-lib/infra-transaction-internal-interface/src/main/java;…/infra-batch/src/main/java`
(CsvRecordReader / batch base classes are composite-build only). Run tests with a 15-line
`LauncherFactory` + `SummaryGeneratingListener` main class. Wider lib sourcepaths drag in protobuf
generated code that does not compile — keep it to those two modules.

### Gateway Java-21 feature branch vs Java-25 lib (compile-only recipe, verified 2026-09-06)

`novopay-platform-api-gateway` feature branches off `ddp-prod` pin `sourceCompatibility 21`, but the
included `../novopay-platform-lib` checkout (`ddp-fea-bkyc`, `ddp-bkup-qa`) is toolchain 25, so
`compileJava` dies at dependency resolution ("looking for a library compatible with JVM runtime
version 21 ... only compatible with 25"). `ddp-bkup-qa` gateway is already Java 25, so QA compiles it
that way. Local check without touching either repo: a Gradle init script that lifts the toolchain and
the resolution attribute (a toolchain alone is not enough — explicit `targetCompatibility` wins):

```groovy
import org.gradle.api.attributes.java.TargetJvmVersion
allprojects {
    plugins.withId('java') { java { toolchain { languageVersion = JavaLanguageVersion.of(25) } } }
    afterEvaluate {
        if (project.name == 'novopay-platform-api-gateway') {
            configurations.configureEach { c ->
                if (c.canBeResolved) c.attributes.attribute(TargetJvmVersion.TARGET_JVM_VERSION_ATTRIBUTE, 25)
            }
        }
    }
}
```

`./gradlew compileJava --no-daemon -q -I toolchain25.init.gradle` (+ `JAVA_TOOL_OPTIONS` fix above).
JDK 25 is already provisioned at `~/.gradle/jdks/eclipse_adoptium-25-amd64-windows.2`.

### Working patterns

| Task | Command |
|---|---|
| Read-only git | `git -C "C:\Users\ashutosh.kumar\Desktop\novopay\<repo>" status\|log\|diff\|fetch` |
| Commit / push / hooks-sensitive git | `"C:\Program Files\Git\bin\bash.exe"` → `cd /c/novopay/<repo>` → `git …` |
| Compile one microservice | `.\gradlew.bat compileJava --no-daemon` (+ JAVA_TOOL_OPTIONS fix above) |
| Install branch-guard hooks | `.\gradlew.bat installGitHooks --no-daemon` |
| Search code | dedicated Grep/Read tools, not huge PS `rg` |

Related: [[pref-working-style]], [[pref-git-workflow]], [[ref-workspace-tools]].
