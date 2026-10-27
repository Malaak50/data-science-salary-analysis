"""Tests du module prediction."""

import pandas as pd
import pytest

from salary_prediction.config import FEATURES
from salary_prediction.prediction import (
    PredictionError,
    load_metadata,
    load_pipeline,
    predict_salary,
)


def test_load_pipeline_returns_pipeline():
    pipeline = load_pipeline()
    assert "preprocessor" in pipeline.named_steps
    assert "model" in pipeline.named_steps


def test_load_metadata_returns_dict():
    metadata = load_metadata()
    assert isinstance(metadata, dict)
    assert "metriques" in metadata
    assert "R2_test" in metadata["metriques"]


def test_load_pipeline_missing_file_raises(tmp_path):
    missing = tmp_path / "nonexistent.joblib"
    with pytest.raises(FileNotFoundError):
        load_pipeline(path=missing)


def test_predict_salary_returns_float(sample_features):
    salary = predict_salary(sample_features)
    assert isinstance(salary, float)
    assert salary > 0


def test_predict_salary_missing_feature_raises(sample_features):
    incomplete = {k: v for k, v in sample_features.items() if k != "work_year"}
    with pytest.raises(PredictionError, match="manquantes"):
        predict_salary(incomplete)


def test_predict_salary_extra_feature_raises(sample_features):
    extra = {**sample_features, "extra_feature": "value"}
    with pytest.raises(PredictionError, match="inattendues"):
        predict_salary(extra)


def test_predict_salary_unknown_category_does_not_crash(sample_features):
    """handle_unknown="ignore" doit éviter le crash."""
    unknown = {**sample_features, "job_category": "Unknown_Job"}
    salary = predict_salary(unknown)
    assert isinstance(salary, float)
    assert salary > 0