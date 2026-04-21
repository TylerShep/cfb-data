"""Tests for ``data_retriever_service.service.RetrieverService``."""

from __future__ import annotations

import pytest
import responses

from data_retriever_service.service import CFBD_BASE_URL, RetrieverError, RetrieverService


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("CFBD_DATA_API_KEY", raising=False)
    with pytest.raises(RetrieverError, match="CFBD_DATA_API_KEY"):
        RetrieverService.fetch("teams")


@responses.activate
def test_fetch_returns_json(monkeypatch):
    monkeypatch.setenv("CFBD_DATA_API_KEY", "test-key")
    responses.add(
        responses.GET,
        f"{CFBD_BASE_URL}/teams",
        json=[{"id": 1, "school": "Alabama"}],
        status=200,
    )
    result = RetrieverService.fetch("teams")
    assert result == [{"id": 1, "school": "Alabama"}]


@responses.activate
def test_fetch_raises_on_non_2xx(monkeypatch):
    monkeypatch.setenv("CFBD_DATA_API_KEY", "test-key")
    responses.add(
        responses.GET,
        f"{CFBD_BASE_URL}/teams",
        json={"error": "unauthorized"},
        status=401,
    )
    with pytest.raises(RetrieverError, match="401"):
        RetrieverService.fetch("teams")


@responses.activate
def test_fetch_passes_params_and_auth(monkeypatch):
    monkeypatch.setenv("CFBD_DATA_API_KEY", "test-key")
    responses.add(
        responses.GET,
        f"{CFBD_BASE_URL}/games",
        json=[],
        status=200,
    )
    RetrieverService.fetch("games", {"year": 2023})
    assert len(responses.calls) == 1
    call = responses.calls[0]
    assert "year=2023" in call.request.url
    assert call.request.headers["Authorization"] == "Bearer test-key"
