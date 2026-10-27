"""Tests du module preprocessing."""

import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer

from salary_prediction.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES
from salary_prediction.preprocessing import (
    add_continents,
    add_job_category,
    build_preprocessor,
    create_job_category,
)


@pytest.mark.parametrize("title,expected", [
    ("Data Scientist", "Data Scientist"),
    ("Senior Data Scientist", "Data Scientist"),
    ("data scientist", "Data Scientist"),
    ("Data Engineer", "Data Engineer"),
    ("Data Analyst", "Data Analyst"),
    ("Software Engineer", "Software Engineer"),
    ("Machine Learning Engineer", "ML Engineer"),
    ("Manager", "Manager"),
    ("Data Architect", "Architect"),
    ("Research Scientist", "Data Scientist"),
    ("Unknown Title", "Other"),
])
def test_create_job_category(title, expected):
    assert create_job_category(title) == expected


def test_create_job_category_empty_string():
    assert create_job_category("") == "Other"


def test_create_job_category_case_insensitive():
    assert create_job_category("DATA SCIENTIST") == "Data Scientist"
    assert create_job_category("data scientist") == "Data Scientist"


def test_add_job_category_adds_column(sample_features):
    df = pd.DataFrame([sample_features])
    df["job_title"] = "Data Scientist"
    result = add_job_category(df)
    assert "job_category" in result.columns
    assert result["job_category"].iloc[0] == "Data Scientist"


def test_add_job_category_raises_without_job_title():
    df = pd.DataFrame({"other_col": [1]})
    with pytest.raises(ValueError, match="job_title"):
        add_job_category(df)


def test_build_preprocessor_returns_column_transformer():
    pre = build_preprocessor()
    assert isinstance(pre, ColumnTransformer)
    assert len(pre.transformers) == 2


def test_build_preprocessor_uses_expected_features():
    pre = build_preprocessor()
    # ColumnTransformer.transformers est une liste de tuples (name, transformer, columns)
    transformer_names = [t[0] for t in pre.transformers]
    assert "num" in transformer_names
    assert "cat" in transformer_names

    # Vérifier que les colonnes couvertes sont bien celles attendues
    num_cols = [t[2] for t in pre.transformers if t[0] == "num"][0]
    cat_cols = [t[2] for t in pre.transformers if t[0] == "cat"][0]
    assert num_cols == NUMERIC_FEATURES
    assert cat_cols == CATEGORICAL_FEATURES

    # Vérifier que toutes les features sont couvertes
    all_covered = set(num_cols) | set(cat_cols)
    expected = set(NUMERIC_FEATURES) | set(CATEGORICAL_FEATURES)
    assert all_covered == expected