from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from endpoints.base import EndpointRequestService


@dataclass
class GameDrivesEndpoint(EndpointRequestService):
    endpoint: str = "drives"
    default_params: dict[str, Any] = field(
        default_factory=lambda: {
            "year": 2023,
            "seasonType": "both",
            "classification": "fbs",
        }
    )
