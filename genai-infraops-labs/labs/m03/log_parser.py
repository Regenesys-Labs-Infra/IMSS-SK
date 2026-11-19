"""Summarize nginx access-log requests by UTC hour and HTTP status."""

import argparse
import csv
import ipaddress
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, NamedTuple, Optional, Sequence, Tuple


LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>\S+)"\s+'
    r'(?P<status>\d{3})(?:\s|$)'
)
LOG_TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


class AccessLogEntry(NamedTuple):
    """Fields used from one combined-format nginx access-log entry."""

    ip: str
    timestamp: datetime
    method: str
    path: str
    status: int


def parse_access_log_line(line: str) -> Optional[AccessLogEntry]:
    """Parse one combined-format log line, returning None when malformed."""
    match = LOG_PATTERN.match(line.rstrip("\r\n"))
    if match is None:
        return None

    try:
        ipaddress.ip_address(match.group("ip"))
        timestamp = datetime.strptime(match.group("time"), LOG_TIME_FORMAT)
        status = int(match.group("status"))
    except ValueError:
        return None

    if not 100 <= status <= 599:
        return None

    return AccessLogEntry(
        ip=match.group("ip"),
        timestamp=timestamp,
        method=match.group("method"),
        path=match.group("path"),
        status=status,
    )


def count_requests(
    input_path: Path,
) -> Tuple[Dict[Tuple[str, int], int], int]:
    """Count requests by UTC hour and status, returning counts and bad-line count."""
    counts: Dict[Tuple[str, int], int] = {}
    malformed_lines = 0

    with input_path.open("r", encoding="utf-8") as log_file:
        for line in log_file:
            entry = parse_access_log_line(line)
            if entry is None:
                malformed_lines += 1
                continue

            hour = entry.timestamp.astimezone(timezone.utc).strftime(
                "%Y-%m-%dT%H:00Z"
            )
            key = (hour, entry.status)
            counts[key] = counts.get(key, 0) + 1

    return counts, malformed_lines


def write_csv(
    output_path: Path,
    counts: Dict[Tuple[str, int], int],
) -> None:
    """Write counts to a CSV with hour, status, and count columns."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(("hour", "status", "count"))
        for (hour, status), count in sorted(counts.items()):
            writer.writerow((hour, status, count))


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Parse command-line arguments and write the hourly request summary."""
    parser = argparse.ArgumentParser(
        description="Count nginx access-log requests by UTC hour and status code."
    )
    parser.add_argument("--input", required=True, type=Path, help="nginx access log")
    parser.add_argument("--output", required=True, type=Path, help="output CSV path")
    args = parser.parse_args(argv)

    if args.input.resolve() == args.output.resolve():
        parser.error("--input and --output must refer to different files")

    try:
        counts, malformed_lines = count_requests(args.input)
        write_csv(args.output, counts)
    except (OSError, UnicodeError) as exc:
        parser.error(str(exc))

    print(f"Skipped malformed lines: {malformed_lines}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
