"""Tests for ``data_transformer_service.service.TransformService``."""

from __future__ import annotations

import pandas as pd

from data_transformer_service import TransformService


def test_response_to_dataframe_from_list():
    response = [{"id": 1, "name": "Alabama"}, {"id": 2, "name": "Auburn"}]
    df = TransformService.response_to_dataframe(response)
    assert list(df.columns) == ["id", "name"]
    assert len(df) == 2


def test_break_out_dict_columns_flattens_nested():
    df = pd.DataFrame(
        [
            {"game_id": 1, "home": {"team": "Alabama", "score": 24}},
            {"game_id": 2, "home": {"team": "Auburn", "score": 17}},
        ]
    )
    flattened = TransformService.break_out_dict_columns(df)
    assert "home_team" in flattened.columns
    assert "home_score" in flattened.columns
    assert "home" not in flattened.columns
    assert flattened["home_team"].tolist() == ["Alabama", "Auburn"]


def test_flatten_all_handles_recursive_dicts():
    df = pd.DataFrame(
        [
            {
                "game_id": 1,
                "venue": {"name": "Bryant-Denny", "coords": {"lat": 33.2, "lon": -87.5}},
            },
        ]
    )
    flattened = TransformService.flatten_all(df)
    assert "venue_coords_lat" in flattened.columns
    assert flattened["venue_coords_lat"].iloc[0] == 33.2


def test_strip_trailing_zero_suffix():
    df = pd.DataFrame({"id_0": [1, 2], "name_0": ["a", "b"], "keep": [3, 4]})
    cleaned = TransformService.strip_trailing_zero_suffix(df)
    assert set(cleaned.columns) == {"id", "name", "keep"}


def test_transform_end_to_end():
    response = [
        {"game_id": 1, "venue": {"name": "Bryant-Denny"}},
        {"game_id": 2, "venue": {"name": "Jordan-Hare"}},
    ]
    df = TransformService.transform(response)
    assert "venue_name" in df.columns
    assert df["venue_name"].tolist() == ["Bryant-Denny", "Jordan-Hare"]
