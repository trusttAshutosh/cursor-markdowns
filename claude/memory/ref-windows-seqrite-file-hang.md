---
name: ref-windows-seqrite-file-hang
description: "ATSLAP-43 file delete/create hangs (Gradle clean/compile, rm -rf) are caused by Seqrite EPS minifilters, not Gradle; how to recognise and diagnose"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f12c0105-52b1-46d6-8d44-41f6cb76b632
  modified: 2026-09-02T09:28:33.503Z
---

On Ashutosh's machine (`ATSLAP-43`) **Seqrite Endpoint Protection 8.4** (drivers `catflt.sys`, `cssdlp.sys`
CoSoSys DLP, `bdsflt.sys` Behavior Detection, installed 2026-03-27) intermittently never completes the
delete-cleanup or create of small files that a JVM writes/removes in bulk. Signature (RCA 2026-09-02,
`docs/RCA_WINDOWS_FILE_HANG_SEQRITE_2026-09-02.md`):

- Gradle hangs in `:<module>:clean` or `compileJava`; `rm -rf build`, `del`, `Remove-Item` on the same
  file all hang; the hung process ends up with 1 thread in `Wait/Unknown` and cannot be killed; daemons
  stay BUSY; shutdown needs the power button.
- The wedged file is usually 0 bytes, reads fine, write/delete opens block or get sharing violation, and
  **no process holds a handle** (Restart Manager / handle enumeration empty) because the thread is stuck
  in the kernel after the handle left the table. Survives reboot.
- `jstack -l <pid>` shows the thread RUNNABLE in `WindowsNativeDispatcher.DeleteFile0` or
  `FileOutputStream.open0`. Defender is off; Windows Search excludes the repos; NTFS/disk healthy.

**Why:** the block is below the filesystem API, so daemon stops, cache/lock cleanup, `clean`, reinstalling
Gradle/Java/Git, or JVM flags cannot help. Previous agents burned hours on those.

**How to apply:** when a build or file op "hangs" here, do not retry or kill; take `jstack` of the daemon,
run `tools/windows-file-hang/HandleProbe.cs` and `Bulk.java` (see its README), run every hang-prone probe
detached with a timeout, and point the user to the RCA fix (Seqrite EPS policy exclusions for the workspace,
`.gradle`, `.jdks`, `java.exe`/`idea64.exe`/`rg.exe`; Safe-Mode delete of wedged files as interim).
Note `novopay-platform-lib` was on `ddp-prod-master` (wrapper 8.10.2) even though the user said `ddp-fea-bkyc`;
`novopay-platform-actor` (Gradle 9.0.0, JDK 25 toolchain) includes lib via `includeBuild`.

Related: [[ref-machine-commands]], [[ref-workspace-tools]], [[user-deepankar]].
