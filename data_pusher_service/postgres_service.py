"""Postgres writer for CFBD-sourced DataFrames.

Reads connection parameters from environment variables:
    DB_HOST, DB_PORT (default 5432), DB_NAME, DB_USER, DB_PASSWORD
"""

from __future__ import annotations

import datetime as dt
import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager

import numpy as np
import pandas as pd
import psycopg2
from psycopg2 import extensions, extras

log = logging.getLogger(__name__)

PG_TYPE_MAPPING: dict[str, str] = {
    "int64": "bigint",
    "Int64": "bigint",
    "int32": "integer",
    "float64": "numeric",
    "bool": "boolean",
    "datetime64[ns]": "timestamp",
    "object": "text",
}


class PusherService:
    """Thin Postgres wrapper that creates tables from DataFrames and bulk-inserts rows."""

    @staticmethod
    @contextmanager
    def connection() -> Iterator[extensions.connection]:
        """Yield a Postgres connection, committing on success and closing on exit."""
        conn = psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=int(os.environ.get("DB_PORT", "5432")),
        )
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _table_name_for_endpoint(endpoint: str) -> str:
        safe = endpoint.strip("/").replace("/", "_").replace("-", "_")
        return f"d_{safe}"

    @classmethod
    def create_table(cls, df: pd.DataFrame, endpoint: str) -> str:
        """Create a destination table for ``df`` if it doesn't exist. Returns the table name."""
        table_name = cls._table_name_for_endpoint(endpoint)
        columns_ddl = ", ".join(
            f'"{col}" {PG_TYPE_MAPPING.get(str(df[col].dtype), "text")}' for col in df.columns
        )
        ddl = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_ddl}, updated_on timestamp);'

        with cls.connection() as conn, conn.cursor() as cur:
            cur.execute(ddl)

        log.info("Ensured table %s exists", table_name)
        return table_name

    @classmethod
    def push(cls, df: pd.DataFrame, table_name: str, batch_size: int = 500) -> int:
        """Bulk-insert every row of ``df`` into ``table_name``. Returns row count."""
        if df.empty:
            log.info("Skipping push: DataFrame is empty")
            return 0

        df_clean = df.replace({np.nan: None})
        columns = list(df_clean.columns)
        columns_sql = ", ".join(f'"{c}"' for c in columns) + ", updated_on"
        placeholders = "(" + ", ".join(["%s"] * (len(columns) + 1)) + ")"
        insert_sql = f'INSERT INTO "{table_name}" ({columns_sql}) VALUES %s'

        now = dt.datetime.now()
        rows = [tuple(row[c] for c in columns) + (now,) for _, row in df_clean.iterrows()]

        with cls.connection() as conn, conn.cursor() as cur:
            extras.execute_values(
                cur, insert_sql, rows, template=placeholders, page_size=batch_size
            )

        log.info("Inserted %d rows into %s", len(rows), table_name)
        return len(rows)
