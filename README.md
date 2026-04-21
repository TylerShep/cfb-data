# cfb-data

> Dynamic ETL pipeline that pulls data from the [CollegeFootballData.com](https://collegefootballdata.com) REST API and loads it into PostgreSQL.

**Version:** 0.2.0
**Author:** [Tyler Shepherd](https://github.com/TylerShep)

---

## What it does

For each configured endpoint (teams, drives, plays, …) the pipeline:

1. **Retrieves** JSON from `api.collegefootballdata.com/{endpoint}` with bearer-token auth.
2. **Transforms** the nested response into a flat pandas DataFrame (recursively expanding `dict`-valued columns).
3. **Pushes** the DataFrame into PostgreSQL, auto-creating the destination table on first run.

## Architecture

```
┌────────────────────┐   ┌──────────────────────┐   ┌─────────────────────┐
│  CFBD REST API     │──▶│  RetrieverService    │──▶│                     │
└────────────────────┘   │  (data_retriever_    │   │  TransformService   │
                         │   service)           │   │  (data_transformer_ │
                         └──────────────────────┘   │   service)          │
                                                    └──────────┬──────────┘
                                                               │
                                                               ▼
┌────────────────────┐   ┌──────────────────────┐   ┌─────────────────────┐
│  PostgreSQL        │◀──│  PusherService       │◀──│  pandas DataFrame   │
└────────────────────┘   │  (data_pusher_       │   └─────────────────────┘
                         │   service)           │
                         └──────────────────────┘
                                   ▲
                                   │
                         ┌──────────────────────┐
                         │  EndpointRequest     │
                         │  Service             │
                         │  (endpoints/*)       │
                         └──────────────────────┘
                                   ▲
                                   │
                         ┌──────────────────────┐
                         │  request_manager     │
                         │  (orchestrator)      │
                         └──────────────────────┘
```

## Project layout

```
cfb-data/
├── data_retriever_service/     # HTTP client for CFBD
├── data_transformer_service/   # JSON -> flat DataFrame
├── data_pusher_service/        # DataFrame -> PostgreSQL
├── endpoints/                  # One file per API endpoint
│   ├── base.py                 # EndpointRequestService base class
│   ├── teams.py
│   ├── game_drives.py
│   └── play_by_play.py
├── request_manager/            # Orchestration / CLI entry point
├── tests/                      # pytest unit tests
├── pyproject.toml              # Packaging + ruff config
├── requirements.txt            # Runtime deps
└── requirements-dev.txt        # + dev deps (pytest, ruff, responses)
```

## Getting started

### 1. Prerequisites

- Python 3.10+
- PostgreSQL 14+ (local or remote)
- A free CFBD API key: https://collegefootballdata.com/key

### 2. Install

```bash
git clone https://github.com/TylerShep/cfb-data.git
cd cfb-data
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 3. Configure

```bash
cp .env.example .env
# then edit .env with your CFBD key + Postgres creds
```

The pipeline reads the following environment variables:

| Variable | Purpose |
|----------|---------|
| `CFBD_DATA_API_KEY` | Bearer token for the CFBD API |
| `DB_HOST` | Postgres host |
| `DB_PORT` | Postgres port (default `5432`) |
| `DB_NAME` | Target database name |
| `DB_USER` | Postgres user |
| `DB_PASSWORD` | Postgres password |

### 4. Run

```bash
# Run every configured endpoint:
python -m request_manager.manager

# Or (once installed via pip):
cfb-data --log-level DEBUG
```

## Adding a new endpoint

Create a new file in `endpoints/` subclassing `EndpointRequestService`:

```python
from dataclasses import dataclass, field
from typing import Any

from endpoints.base import EndpointRequestService


@dataclass
class GamesEndpoint(EndpointRequestService):
    endpoint: str = "games"
    default_params: dict[str, Any] = field(
        default_factory=lambda: {"year": 2023, "seasonType": "regular"}
    )
```

Then add an instance to the `ENDPOINTS` list in `request_manager/manager.py`.

For endpoints that need multiple calls (e.g. once per week), override `params_iter()` — see `endpoints/play_by_play.py` for an example.

## Development

```bash
# Lint + format:
ruff check .
ruff format .

# Run tests:
pytest
```

## Changelog

### 0.2.0 (2026-04)

- **Rewrote** retriever/transformer/pusher services to use proper connection management, error handling, and batch inserts.
- **Renamed** the `requests/` package to `endpoints/` to avoid shadowing the third-party `requests` library.
- **Added** a base `EndpointRequestService` class with a common retrieve → transform → push flow.
- **Added** `pyproject.toml`, a real `requirements.txt` (with pins, minus stdlib entries), a `--log-level` CLI, and an `.env.example`.
- **Removed** committed `.idea/` IntelliJ metadata.
- **Fixed** several runtime bugs: missing `numpy` import, `getConnection` vs `getPostgresConnection` typo, bound-method call on class, empty `games.py`.

### 0.1.0 (2024-03)

Initial release (classroom project scaffolding).

## Helpful resources

- CFBD's official Python client: https://github.com/CFBD/cfbd-python
- API docs (endpoints + schema): https://api.collegefootballdata.com/api/docs/?url=/api-docs.json
- Raw data exporter: https://collegefootballdata.com/exporter
