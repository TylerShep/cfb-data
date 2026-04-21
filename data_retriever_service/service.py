"""HTTP retriever for the CollegeFootballData.com REST API.

Reads the bearer token from the ``CFBD_DATA_API_KEY`` environment variable and
exposes a single ``fetch`` classmethod that returns parsed JSON.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import requests

log = logging.getLogger(__name__)

CFBD_BASE_URL = "https://api.collegefootballdata.com"


class RetrieverError(RuntimeError):
    """Raised when the CFBD API returns a non-2xx response."""


class RetrieverService:
    """Thin wrapper around the CollegeFootballData.com HTTP API."""

    @staticmethod
    def _get_api_key() -> str:
        api_key = os.environ.get("CFBD_DATA_API_KEY")
        if not api_key:
            raise RetrieverError(
                "CFBD_DATA_API_KEY environment variable is not set. "
                "Get a free key at https://collegefootballdata.com/key."
            )
        return api_key

    @classmethod
    def fetch(
        cls,
        endpoint: str,
        params: dict[str, Any] | None = None,
        timeout: int = 30,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Issue a GET request to ``{CFBD_BASE_URL}/{endpoint}`` and return JSON.

        Raises ``RetrieverError`` for non-2xx responses.
        """
        url = f"{CFBD_BASE_URL}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {cls._get_api_key()}"}

        log.info("GET %s params=%s", url, params)
        response = requests.get(url, headers=headers, params=params or {}, timeout=timeout)

        if not response.ok:
            raise RetrieverError(
                f"CFBD API returned {response.status_code} for {url}: {response.text[:200]}"
            )

        return response.json()
