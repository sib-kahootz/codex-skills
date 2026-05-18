---
name: log-interrogator
description: Search and summarize configured log files for user-provided terms, incidents, errors, stack traces, or time windows. Use when Codex needs to investigate logs, inspect recent failures, find matching log lines with surrounding context, detect common error patterns, or configure reusable log file paths for repeated investigations.
---

# Log Interrogator

Use this skill to investigate logs without modifying them. Default to last 24 hours unless the user gives another time window.

## Workflow

1. Check config:
   ```powershell
   python skills\custom\log-interrogator\scripts\log_interrogator.py --show-config
   ```
2. If no log paths are configured, ask the user for log file paths, directory paths, or glob patterns. Store them:
   ```powershell
   python skills\custom\log-interrogator\scripts\log_interrogator.py --set-paths "C:\path\app.log" "C:\logs\*.log"
   ```
3. Search configured logs. Use `--since 24h` by default. Add user terms with repeated values after `--terms`:
   ```powershell
   python skills\custom\log-interrogator\scripts\log_interrogator.py --terms error timeout --since 24h --context 3
   ```
4. For a broad health check or "general overview", run overview mode before targeted searches:
   ```powershell
   python skills\custom\log-interrogator\scripts\log_interrogator.py --overview
   ```
   Overview mode ignores time windows for broad counts, reports newest file writes and parseable log timestamps, and highlights top files, terms, patterns, and parsed messages.
5. Summarize results for the user:
   - matching files and counts
   - strongest timeline clues
   - common error patterns
   - representative surrounding context
   - likely next checks

## Time Windows

Accept relative windows such as `24h`, `2d`, `90m`, or absolute timestamps such as `2026-06-01 09:00`.

Use `--until` only when the user provides an end time:
```powershell
python skills\custom\log-interrogator\scripts\log_interrogator.py --terms "request id 123" --since "2026-06-01 09:00" --until "2026-06-01 10:00"
```

## Rules

- Never edit, truncate, rotate, delete, or move logs.
- Prefer targeted terms from the user; if missing, ask for terms or incident clues.
- If the result set is huge, rerun with narrower terms, a smaller time window, or lower `--max-matches`.
- Treat timestamp parsing as best effort. Mention when matching lines had no parseable timestamp.
- If configured paths include directories, the helper searches common log-like files recursively.

## Helper

Use `scripts/log_interrogator.py` for config and read-only searching. It stores config at `config/logs.json` inside this skill folder.
