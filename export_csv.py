import argparse
import csv
import sqlite3
import sys
from datetime import UTC, datetime
from pathlib import Path


def export_csv(db_path: str, output: str) -> None:
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT id, received_at, data FROM raw_data ORDER BY id"
    ).fetchall()
    conn.close()

    fh = open(output, "w", newline="") if output else sys.stdout
    writer = csv.writer(fh)
    writer.writerow(["id", "received_at", "received_at_iso", "data_hex", "data_len"])

    for row_id, ts, data in rows:
        dt = datetime.fromtimestamp(ts, tz=UTC).isoformat()
        writer.writerow([row_id, ts, dt, data.hex(), len(data)])

    if output:
        print(f"Exported {len(rows)} rows to {output}")
    fh.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export raw_data to CSV")
    parser.add_argument(
        "--db",
        default=str(Path(__file__).parent / "data.db"),
        help="Path to SQLite database (default: data.db in project dir)",
    )
    parser.add_argument(
        "-o", "--output",
        default="",
        help="Output CSV file path (default: stdout)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    export_csv(args.db, args.output)


if __name__ == "__main__":
    main()
