"""Orchestrator for the CFBD data pipeline.

Usage:
    python -m request_manager.manager

All endpoints are defined in :mod:`endpoints`. Add a new endpoint by creating a
subclass of ``EndpointRequestService`` and appending an instance of it to the
``ENDPOINTS`` list below.
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Iterable

from endpoints import GameDrivesEndpoint, PlayByPlayEndpoint, TeamsEndpoint
from endpoints.base import EndpointRequestService, run_endpoint

log = logging.getLogger("cfb_data")

ENDPOINTS: list[EndpointRequestService] = [
    TeamsEndpoint(),
    GameDrivesEndpoint(),
    PlayByPlayEndpoint(),
]


def run_all(endpoints: Iterable[EndpointRequestService] = ENDPOINTS) -> dict[str, int]:
    """Run every endpoint in sequence. Returns ``{endpoint: rows_inserted}``."""
    results: dict[str, int] = {}
    for service in endpoints:
        results[service.endpoint] = run_endpoint(service)
    return results


def _configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the CFBD ETL pipeline")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    args = parser.parse_args(argv)

    _configure_logging(args.log_level)
    log.info("Starting CFBD pipeline")
    results = run_all()
    for endpoint, rows in results.items():
        log.info("Endpoint %s inserted %d rows", endpoint, rows)
    log.info("Pipeline complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
