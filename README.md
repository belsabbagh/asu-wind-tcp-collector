# ASU Wind TCP Collector

TCP server that collects raw data from embedded systems and logs it to SQLite.

## Usage

```bash
uv run server.py                    # default port 21345
uv run server.py --port 9999        # custom port
```

Send data:

```bash
echo "some raw data" | nc localhost 21345
```

## Export to CSV

```bash
uv run export_csv.py                        # print to stdout
uv run export_csv.py -o data.csv            # write to file
uv run export_csv.py --db /path/to/data.db  # custom db path
```

## Live Reload (dev)

```bash
./dev.sh
```

Watches for file changes and restarts automatically.

## Schema

| Column      | Type    | Description            |
|-------------|---------|------------------------|
| id          | INTEGER | Auto-incrementing PK   |
| received_at | INTEGER | Unix timestamp         |
| data        | BLOB    | Raw bytes from device  |
