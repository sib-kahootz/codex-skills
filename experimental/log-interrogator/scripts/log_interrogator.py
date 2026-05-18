#!/usr/bin/env python3
"""Read-only log search helper for the log-interrogator skill."""

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = SKILL_DIR / "config" / "logs.json"
LOG_EXTENSIONS = {".log", ".txt", ".out", ".err", ".trace"}
TIMESTAMP_PATTERNS = [
    re.compile(r"(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[,.]\d{1,6})?)"),
    re.compile(r"(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2})"),
    re.compile(r"(?P<ts>\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})"),
    re.compile(r"(?P<ts>\d{2}/\d{2}/\d{4}[ T]\d{2}:\d{2}:\d{2})"),
]
ERROR_PATTERNS = {
    "exception": re.compile(r"\b(exception|traceback|stack trace)\b", re.I),
    "timeout": re.compile(r"\b(timed?\s*out|timeout|deadline exceeded)\b", re.I),
    "http_5xx": re.compile(r"\b(50[0-9]|HTTP/\S+\"?\s+50[0-9])\b", re.I),
    "http_4xx": re.compile(r"\b(40[0-9]|HTTP/\S+\"?\s+40[0-9])\b", re.I),
    "database": re.compile(r"\b(sql|database|deadlock|connection pool|jdbc|odbc)\b", re.I),
    "auth": re.compile(r"\b(auth|permission denied|forbidden|unauthori[sz]ed)\b", re.I),
    "memory": re.compile(r"\b(out of memory|oom|heap|gc overhead)\b", re.I),
    "disk": re.compile(r"\b(no space left|disk|filesystem|quota)\b", re.I),
}
DEFAULT_OVERVIEW_TERMS = ["error", "warn", "exception", "timeout", "failed", "fatal", "severe"]


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {"paths": []}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_paths(paths: list[str]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"paths": paths}, indent=2) + "\n", encoding="utf-8")


def parse_time(value: str | None, default_delta: timedelta | None = None) -> datetime | None:
    if value is None:
        return datetime.now() - default_delta if default_delta else None
    lowered = value.strip().lower()
    match = re.fullmatch(r"(\d+)\s*([mhd])", lowered)
    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        delta = {"m": timedelta(minutes=amount), "h": timedelta(hours=amount), "d": timedelta(days=amount)}[unit]
        return datetime.now() - delta
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise SystemExit(f"Unsupported time value: {value!r}")


def parse_line_time(line: str) -> datetime | None:
    lucee_match = re.search(r'"(?P<date>\d{2}/\d{2}/\d{4})","(?P<time>\d{2}:\d{2}:\d{2})"', line)
    if lucee_match:
        try:
            return datetime.strptime(f"{lucee_match.group('date')} {lucee_match.group('time')}", "%m/%d/%Y %H:%M:%S")
        except ValueError:
            pass
    for pattern in TIMESTAMP_PATTERNS:
        match = pattern.search(line)
        if not match:
            continue
        raw = match.group("ts").replace(",", ".")
        for fmt in (
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M",
            "%d/%b/%Y:%H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%YT%H:%M:%S",
        ):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                pass
    return None


def extract_log_message(line: str) -> str | None:
    lucee_match = re.match(r'^"(?:ERROR|WARN|INFO|DEBUG|TRACE)","[^"]+","[^"]+","[^"]+","[^"]*","(?P<message>.*)', line, re.I)
    if lucee_match:
        return lucee_match.group("message").split(";", 1)[0].strip().rstrip('"')
    return None


def expand_paths(configured: list[str]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for item in configured:
        matches = [Path(p) for p in glob.glob(item, recursive=True)] or [Path(item)]
        for path in matches:
            if path.is_dir():
                candidates = (p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in LOG_EXTENSIONS)
            else:
                candidates = [path] if path.is_file() else []
            for candidate in candidates:
                resolved = candidate.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    files.append(resolved)
    return files


def line_matches(line: str, terms: list[str], case_sensitive: bool) -> bool:
    haystack = line if case_sensitive else line.lower()
    needles = terms if case_sensitive else [term.lower() for term in terms]
    return all(term in haystack for term in needles)


def search(args: argparse.Namespace) -> int:
    config = load_config()
    configured_paths = config.get("paths", [])
    if not configured_paths:
        print("NO_CONFIG: ask user for log file paths, directory paths, or glob patterns, then run --set-paths.")
        return 2

    terms = args.terms or []
    if not terms:
        print("NO_TERMS: ask user for search terms, request ids, error text, usernames, or incident clues.")
        return 2

    since = parse_time(args.since, timedelta(hours=24))
    until = parse_time(args.until)
    files = expand_paths(configured_paths)
    if not files:
        print("NO_FILES: configured paths did not resolve to readable log files.")
        return 1

    by_file: Counter[str] = Counter()
    pattern_counts: Counter[str] = Counter()
    no_timestamp = 0
    matches: list[dict] = []

    for file_path in files:
        previous = deque(maxlen=args.context)
        pending_after = 0
        after_lines: list[tuple[int, str]] = []
        try:
            with file_path.open("r", encoding=args.encoding, errors="replace") as handle:
                for line_no, line in enumerate(handle, 1):
                    clean = line.rstrip("\n")
                    if pending_after > 0:
                        after_lines.append((line_no, clean))
                        pending_after -= 1
                        if matches:
                            matches[-1]["after"] = list(after_lines)
                    matched = line_matches(clean, terms, args.case_sensitive)
                    line_time = parse_line_time(clean)
                    in_window = (line_time is None or line_time >= since) and (until is None or line_time <= until)
                    if matched and in_window:
                        if line_time is None:
                            no_timestamp += 1
                        by_file[str(file_path)] += 1
                        for name, pattern in ERROR_PATTERNS.items():
                            if pattern.search(clean):
                                pattern_counts[name] += 1
                        matches.append(
                            {
                                "file": str(file_path),
                                "line": line_no,
                                "timestamp": line_time.isoformat(sep=" ") if line_time else None,
                                "before": list(previous),
                                "match": clean,
                                "after": [],
                            }
                        )
                        pending_after = args.context
                        after_lines = []
                        if len(matches) >= args.max_matches:
                            raise StopIteration
                    previous.append((line_no, clean))
        except StopIteration:
            break
        except OSError as exc:
            print(f"READ_ERROR: {file_path}: {exc}")

    print(f"Configured paths: {len(configured_paths)}")
    print(f"Resolved files: {len(files)}")
    print(f"Window: since {since.isoformat(sep=' ')}" + (f" until {until.isoformat(sep=' ')}" if until else ""))
    print(f"Terms: {', '.join(terms)}")
    print(f"Matches: {len(matches)}")
    if no_timestamp:
        print(f"Matches without parseable timestamp: {no_timestamp}")

    if by_file:
        print("\nMatches by file:")
        for file_name, count in by_file.most_common():
            print(f"- {count} {file_name}")

    if pattern_counts:
        print("\nCommon error patterns:")
        for name, count in pattern_counts.most_common():
            print(f"- {name}: {count}")

    print("\nContext:")
    for entry in matches[: args.max_matches]:
        print(f"\n--- {entry['file']}:{entry['line']} time={entry['timestamp'] or 'unparsed'}")
        for line_no, text in entry["before"]:
            print(f"  {line_no}: {text}")
        print(f"> {entry['line']}: {entry['match']}")
        for line_no, text in entry["after"]:
            print(f"  {line_no}: {text}")

    if len(matches) >= args.max_matches:
        print(f"\nTRUNCATED: hit --max-matches {args.max_matches}. Narrow terms or time window.")
    return 0


def overview(args: argparse.Namespace) -> int:
    config = load_config()
    configured_paths = config.get("paths", [])
    if not configured_paths:
        print("NO_CONFIG: ask user for log file paths, directory paths, or glob patterns, then run --set-paths.")
        return 2

    files = expand_paths(configured_paths)
    if not files:
        print("NO_FILES: configured paths did not resolve to readable log files.")
        return 1

    terms = args.terms or DEFAULT_OVERVIEW_TERMS
    lowered_terms = [term.lower() for term in terms]
    by_file: Counter[str] = Counter()
    by_term: Counter[str] = Counter()
    pattern_counts: Counter[str] = Counter()
    message_counts: Counter[str] = Counter()
    newest_line_time: datetime | None = None
    parseable_timestamps = 0
    unreadable = 0

    for file_path in files:
        try:
            with file_path.open("r", encoding=args.encoding, errors="replace") as handle:
                for line in handle:
                    clean = line.rstrip("\n")
                    line_time = parse_line_time(clean)
                    if line_time:
                        parseable_timestamps += 1
                        if newest_line_time is None or line_time > newest_line_time:
                            newest_line_time = line_time

                    haystack = clean.lower()
                    matched_terms = [term for term in lowered_terms if term in haystack]
                    if not matched_terms:
                        continue

                    by_file[str(file_path)] += 1
                    by_term.update(matched_terms)
                    for name, pattern in ERROR_PATTERNS.items():
                        if pattern.search(clean):
                            pattern_counts[name] += 1
                    message = extract_log_message(clean)
                    if message:
                        message_counts[message[:240]] += 1
        except OSError as exc:
            unreadable += 1
            print(f"READ_ERROR: {file_path}: {exc}")

    newest_file = max(files, key=lambda path: path.stat().st_mtime)
    newest_file_time = datetime.fromtimestamp(newest_file.stat().st_mtime)

    print(f"Configured paths: {len(configured_paths)}")
    print(f"Resolved files: {len(files)}")
    print(f"Newest file write: {newest_file_time.isoformat(sep=' ')} {newest_file}")
    print(f"Newest parseable log timestamp: {newest_line_time.isoformat(sep=' ') if newest_line_time else 'none'}")
    print(f"Parseable timestamped lines: {parseable_timestamps}")
    if unreadable:
        print(f"Unreadable files: {unreadable}")

    print("\nRecent files:")
    for file_path in sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)[: args.overview_files]:
        stat = file_path.stat()
        print(f"- {datetime.fromtimestamp(stat.st_mtime).isoformat(sep=' ')} {stat.st_size} {file_path}")

    print("\nOverview terms:")
    print(f"- {', '.join(terms)}")

    if by_file:
        print("\nBroad matches by file:")
        for file_name, count in by_file.most_common(args.overview_files):
            print(f"- {count} {file_name}")
    else:
        print("\nBroad matches by file: none")

    if by_term:
        print("\nBroad matches by term:")
        for term, count in by_term.most_common():
            print(f"- {term}: {count}")

    if pattern_counts:
        print("\nCommon error patterns:")
        for name, count in pattern_counts.most_common():
            print(f"- {name}: {count}")

    if message_counts:
        print("\nTop parsed messages:")
        for message, count in message_counts.most_common(args.overview_messages):
            print(f"- {count} {message}")

    return 0


def setup_interactive() -> int:
    print("Enter log file paths, directory paths, or glob patterns. Blank line ends.")
    paths: list[str] = []
    while True:
        value = input("> ").strip()
        if not value:
            break
        paths.append(value)
    if not paths:
        print("No paths saved.")
        return 1
    save_paths(paths)
    print(f"Saved {len(paths)} path(s) to {CONFIG_PATH}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only configured log search.")
    parser.add_argument("--show-config", action="store_true")
    parser.add_argument("--overview", action="store_true")
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--set-paths", nargs="+")
    parser.add_argument("--terms", nargs="+")
    parser.add_argument("--since", default="24h")
    parser.add_argument("--until")
    parser.add_argument("--context", type=int, default=3)
    parser.add_argument("--max-matches", type=int, default=100)
    parser.add_argument("--overview-files", type=int, default=20)
    parser.add_argument("--overview-messages", type=int, default=12)
    parser.add_argument("--case-sensitive", action="store_true")
    parser.add_argument("--encoding", default="utf-8")
    args = parser.parse_args()

    if args.setup:
        return setup_interactive()
    if args.set_paths is not None:
        save_paths(args.set_paths)
        print(f"Saved {len(args.set_paths)} path(s) to {CONFIG_PATH}")
        return 0
    if args.show_config:
        config = load_config()
        print(json.dumps({"config": str(CONFIG_PATH), **config}, indent=2))
        return 0 if config.get("paths") else 2
    if args.overview:
        return overview(args)
    return search(args)


if __name__ == "__main__":
    raise SystemExit(main())
