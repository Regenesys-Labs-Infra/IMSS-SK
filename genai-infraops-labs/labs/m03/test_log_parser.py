import csv
from pathlib import Path

from log_parser import count_requests, parse_access_log_line, write_csv


def test_parse_access_log_line_extracts_fields() -> None:
    line = (
        '10.40.3.161 - - [09/Nov/2026:08:00:00 +0530] '
        '"GET /login HTTP/1.1" 503 6261 "-" "Mozilla/5.0"'
    )

    entry = parse_access_log_line(line)

    assert entry is not None
    assert entry.ip == "10.40.3.161"
    assert entry.method == "GET"
    assert entry.path == "/login"
    assert entry.status == 503


def test_count_requests_groups_in_utc_and_counts_malformed_lines(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "access.log"
    input_path.write_text(
        "\n".join(
            [
                '10.40.3.161 - - [09/Nov/2026:08:00:00 +0530] '
                '"GET /login HTTP/1.1" 503 6261 "-" "Mozilla/5.0"',
                '10.40.3.162 - - [09/Nov/2026:02:30:00 +0000] '
                '"GET /home HTTP/1.1" 503 415 "-" "Mozilla/5.0"',
                '10.40.3.163 - - [09/Nov/2026:03:00:00 +0000] '
                '"GET /home HTTP/1.1" 200 415 "-" "Mozilla/5.0"',
                "malformed line",
                'invalid-ip - - [09/Nov/2026:03:00:00 +0000] '
                '"GET /home HTTP/1.1" 200 415 "-" "Mozilla/5.0"',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    counts, malformed_lines = count_requests(input_path)

    assert counts == {
        ("2026-11-09T02:00Z", 503): 2,
        ("2026-11-09T03:00Z", 200): 1,
    }
    assert malformed_lines == 2


def test_write_csv_has_expected_columns_and_order(tmp_path: Path) -> None:
    output_path = tmp_path / "summary" / "counts.csv"
    counts = {
        ("2026-11-09T03:00Z", 200): 1,
        ("2026-11-09T02:00Z", 503): 2,
    }

    write_csv(output_path, counts)

    with output_path.open("r", encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    assert rows == [
        ["hour", "status", "count"],
        ["2026-11-09T02:00Z", "503", "2"],
        ["2026-11-09T03:00Z", "200", "1"],
    ]
