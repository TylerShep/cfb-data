from __future__ import annotations

from dataclasses import dataclass

from endpoints.base import EndpointRequestService


@dataclass
class TeamsEndpoint(EndpointRequestService):
    endpoint: str = "teams"
