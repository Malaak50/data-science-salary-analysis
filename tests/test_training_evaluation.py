"""Tests des modules training et evaluation."""

import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from salary_prediction.config import FEATURES, TARGET
from salary_prediction.evaluation import compare_models, compute_metrics
from salary_prediction.training import MODEL_FACTORIES, build_pipeline, train_model


def test_build_pipeline_returns_pipeline():
    pipeline = build_pipeline("gb")
    assert isinstance(pipeline, Pipeline)
    assert "preprocessor" in pipeline.named_steps
    assert "model" in pipeline.named_steps


def test_build_pipeline_invalid_model_raises():
    with pytest.raises(ValueError, match="Modèle inconnu"):
        build_pipeline("invalid_model")


@pytest.mark.parametrize("model_name", list(MODEL_FACTORIES.keys()))
def test_all_models_build(model_name):
    pipeline = build_pipeline(model_name)
    assert isinstance(pipeline, Pipeline)


def test_compute_metrics_returns_expected_keys():
    y_true = np.array([100.0, 200.0, 300.0, 400.0])
    y_pred = np.array([110.0, 190.0, 310.0, 390.0])
    metrics = compute_metrics(y_true, y_pred)
    assert set(metrics.keys()) == {"mae", "mse", "rmse", "r2"}
    assert metrics["mae"] == 10.0
    assert metrics["rmse"] == 10.0


def test_train_model_returns_trained_pipeline(small_df):
    df = small_df.copy()
    df["job_category"] = "Data Scientist"
    X = df[FEATURES]
    y = df[TARGET]
    pipeline = train_model(X, y, model_name="lr")
    # Un pipeline entraîné a un attribut coef_ sur le modèle
    assert hasattr(pipeline.named_steps["model"], "coef_")


def test_compare_models_returns_sorted_dataframe():
    results = {
        "model_a": {"mae_test": 100, "rmse_test": 150, "r2_test": 0.5,
                     "r2_train": 0.55, "mse_test": 22500, "mse_train": 25000,
                     "mae_train": 95, "rmse_train": 145},
        "model_b": {"mae_test": 120, "rmse_test": 170, "r2_test": 0.3,
                     "r2_train": 0.35, "mse_test": 28900, "mse_train": 30000,
                     "mae_train": 115, "rmse_train": 165},
    }
    df = compare_models(results)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["modèle"] == "model_a"  # R² plus élevé
    assert len(df) == 2