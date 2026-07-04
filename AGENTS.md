# asu-wind-collector

## Run & dev

```bash
uv run server.py               # default port 21345
uv run server.py --port 9999
uv run export_csv.py            # prints CSV to stdout
uv run export_csv.py -o out.csv
```

No deps needed — stdlib only. Dev dep `watchfiles` installed via `uv sync`.

## Project structure

- `server.py` — single entrypoint, sync `main()` wrapper around `async def main_async()`
- `database.py` — SQLite with WAL mode, creates `data.db` in project root (gitignored)
- `export_csv.py` — reads `data.db`, writes CSV with iso timestamps and hex data
- `dev.sh` — `watchfiles` wrapper, auto-restarts on file changes (may race on port, `reuse_address=True` set)

## Schema

```sql
raw_data (id INTEGER PK, received_at INTEGER unix_ts, data BLOB)
```

## Repo & deploy

- `git@github.com:belsabbagh/asu-wind-tcp-collector.git`
- Remote target: `belal@192.168.1.92` pass `0000`, `~/projects/asu-wind-collector`
- No tests, no CI, no lint config
