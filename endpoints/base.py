"""Base class that wires the retrieve -> transform -> push pipeline together.

Every endpoint definition subclasses ``EndpointRequestService`` and provides:
    - ``endpoint``: the CFBD API path (e.g. ``"teams"``, ``"plays"``)
    - ``params_iter``: a generator of parameter dicts (for endpoints that need
      to be called multiple times, e.g. once per week)
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from data_pusher_service import PusherService
from data_retriever_service import RetrieverService
from data_transformer_service import TransformService

log = logging.getLogger(__name__)


@dataclass
class EndpointRequestService:
    """Base class for a single CFBD API endpoint pipeline."""

    endpoint: str = ""
    default_params: dict[str, Any] = field(default_factory=dict)

    def params_iter(self) -> Iterator[dict[str, Any]]:
        """Override for endpoints that need multiple paginated calls."""
        yield self.default_params

    def run(self) -> int:
        """Fetch, transform, and write every batch defined by ``params_iter``.

        Returns the total number of rows inserted across all batches.
        """
        total_rows = 0
        for params in self.params_iter():
            log.info("Running %s params=%s", self.endpoint, params)
            response = RetrieverService.fetch(self.endpoint, params)
            df = TransformService.transform(response)
            if df.empty:
                log.info("No rows returned for %s params=%s", self.endpoint, params)
                continue
            table = PusherService.create_table(df, self.endpoint)
            total_rows += PusherService.push(df, table)
        return total_rows


def run_endpoint(service: EndpointRequestService) -> int:
    """Convenience wrapper for ``service.run()`` with top-level error logging."""
    try:
        return service.run()
    except Exception:
        log.exception("Endpoint %s failed", service.endpoint)
        raise
