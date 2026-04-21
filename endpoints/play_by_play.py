from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from endpoints.base import EndpointRequestService

REGULAR_SEASON_WEEKS = range(1, 16)


@dataclass
class PlayByPlayEndpoint(EndpointRequestService):
    """Fetch play-by-play for every week of a season.

    Attributes:
        year: Season year to pull.
        season_type: CFBD season type (``"regular"``, ``"postseason"``, ``"both"``).
        classification: Division (``"fbs"``, ``"fcs"``, etc.).
        weeks: Iterable of week numbers to pull (defaults to regular season 1-15).
    """

    endpoint: str = "plays"
    year: int = 2023
    season_type: str = "both"
    classification: str = "fbs"
    weeks: tuple[int, ...] = tuple(REGULAR_SEASON_WEEKS)
    default_params: dict[str, Any] = field(default_factory=dict)

    def params_iter(self) -> Iterator[dict[str, Any]]:
        for week in self.weeks:
            yield {
                "year": self.year,
                "seasonType": self.season_type,
                "classification": self.classification,
                "week": week,
            }
