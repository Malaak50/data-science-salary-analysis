"""Tests du module data_loader."""

import pandas as pd
import pytest

from salary_prediction.config import TARGET
from salary_prediction.data_loader import (
    load_processed_data,
    load_raw_data,
    validate_dataframe,
)


def test_load_processed_data_returns_dataframe():
    df = load_processed_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_processed_data_has_target():
    df = load_processed_data()
    assert TARGET in df.columns


def test_load_processed_data_has_continents():
    df = load_processed_data()
    assert "residence_continent" in df.columns
    assert "company_continent" in df.columns


def test_load_raw_data_raises_if_missing(tmp_path):
    missing_path = tmp_path / "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        load_raw_data(path=missing_path)


def test_validate_dataframe_raises_on_empty():
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="vide"):
        validate_dataframe(empty_df)


def test_validate_dataframe_raises_on_missing_target():
    df = pd.DataFrame({"col1": [1, 2, 3]})
    with pytest.raises(ValueError, match="cible"):
        validate_dataframe(df)


def test_validate_dataframe_raises_on_negative_salary():
    df = pd.DataFrame({TARGET: [1000, -500, 2000]})
    with pytest.raises(ValueError, match="<= 0"):
        validate_dataframe(df)