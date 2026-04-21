"""Transformations from raw CFBD JSON into tidy pandas DataFrames.

The CFBD API returns nested dict structures in fields like ``home`` / ``away`` /
``offense``. ``TransformService`` flattens those into columnar form suitable
for insertion into a relational database.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


class TransformService:
    """Flatten nested CFBD API responses into pandas DataFrames."""

    @staticmethod
    def response_to_dataframe(response: list[dict[str, Any]] | dict[str, Any]) -> pd.DataFrame:
        """Normalize the CFBD API response into a DataFrame."""
        if isinstance(response, list):
            return pd.DataFrame(response)
        return pd.json_normalize(response)

    @staticmethod
    def _has_dict_columns(df: pd.DataFrame) -> bool:
        return any(df[col].apply(lambda x: isinstance(x, dict)).any() for col in df.columns)

    @staticmethod
    def break_out_dict_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Expand any column whose first value is a dict into ``col_key`` columns."""
        dict_columns = [
            col for col in df.columns if df[col].apply(lambda x: isinstance(x, dict)).any()
        ]
        for col in dict_columns:
            expanded = (
                df[col]
                .apply(lambda x: pd.Series(x) if isinstance(x, dict) else pd.Series(dtype=object))
                .add_prefix(f"{col}_")
            )
            df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
        return df

    @classmethod
    def flatten_all(cls, df: pd.DataFrame, max_passes: int = 10) -> pd.DataFrame:
        """Recursively break out dict columns until none remain (or ``max_passes`` hit)."""
        for _ in range(max_passes):
            if not cls._has_dict_columns(df):
                break
            df = cls.break_out_dict_columns(df)
        return df

    @staticmethod
    def strip_trailing_zero_suffix(df: pd.DataFrame) -> pd.DataFrame:
        """Remove a trailing ``_0`` on any column name (artifact of flattening)."""
        df = df.rename(columns={c: c[:-2] for c in df.columns if c.endswith("_0")})
        return df

    @classmethod
    def transform(cls, response: list[dict[str, Any]] | dict[str, Any]) -> pd.DataFrame:
        """End-to-end: JSON response -> tidy DataFrame."""
        df = cls.response_to_dataframe(response)
        df = cls.flatten_all(df)
        df = cls.strip_trailing_zero_suffix(df)
        return df
