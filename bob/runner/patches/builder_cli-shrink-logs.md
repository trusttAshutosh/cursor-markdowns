# builder_cli.py - shrink-logs wiring

If `bob shrink-logs` is missing after restore, apply these edits to
`bob-the-builder/runner/lib/builder_cli.py`:

## CMD_ALIASES (add)

```python
"shrink-logs": "shrink-logs",
"shrink_logs": "shrink-logs",
"shrinklogs": "shrink-logs",
```

## Help text (add after prune-overhead line)

```python
print("  shrink-logs [file|-] [--ticket ID]   Compress logs for chat; full copy preserved on disk")
```

## Handler function

```python
def cmd_shrink_logs(args: list[str]) -> int:
    _banner("shrink-logs")
    from shrink_logs import run_shrink_logs_cli
    return run_shrink_logs_cli(args)
```

## handlers dict

```python
"shrink-logs": cmd_shrink_logs,
```

## no-next-steps tuple

Add `"shrink-logs"` alongside `"prune-overhead"`, `"chat-hygiene"`, etc.

Copy `bob/runner/lib/shrink_logs.py` and `bob/runner/tests/test_shrink_logs.py` from this backup into the live bob-the-builder tree.
