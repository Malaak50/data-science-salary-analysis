"""Fonctions d'évaluation des modèles.

Contient :
- compute_metrics : calcule MAE, MSE, RMSE, R².
- evaluate_pipeline : entraîne et évalue un pipeline sur train et test.
- compare_models : compare plusieurs modèles dans un DataFrame.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

from salary_prediction.config import TARGET
from salary_prediction.training import ModelName, train_model


def compute_metrics(
    y_true: pd.Series | np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, float]:
    """Calcule MAE, MSE, RMSE, R².

    Parameters
    ----------
    y_true : pd.Series | np.ndarray
        Valeurs réelles.
    y_pred : np.ndarray
        Valeurs prédites.

    Returns
    -------
    dict
        Dictionnaire avec les clés mae, mse, rmse, r2.
    """
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": float(mean_squared_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def evaluate_pipeline(
    pipeline: Pipeline,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float]:
    """Évalue un pipeline entraîné sur train et test.

    Parameters
    ----------
    pipeline : Pipeline
        Pipeline déjà entraîné.
    X_train, y_train : pd.DataFrame, pd.Series
        Données d'entraînement (pour les métriques train).
    X_test, y_test : pd.DataFrame, pd.Series
        Données de test.

    Returns
    -------
    dict
        Métriques train et test (MAE, MSE, RMSE, R²).
    """
    y_train_pred = pipeline.predict(X_train)
    y_test_pred = pipeline.predict(X_test)

    metrics_train = compute_metrics(y_train, y_train_pred)
    metrics_test = compute_metrics(y_test, y_test_pred)

    return {
        "mae_train": metrics_train["mae"],
        "mae_test": metrics_test["mae"],
        "mse_train": metrics_train["mse"],
        "mse_test": metrics_test["mse"],
        "rmse_train": metrics_train["rmse"],
        "rmse_test": metrics_test["rmse"],
        "r2_train": metrics_train["r2"],
        "r2_test": metrics_test["r2"],
    }


def compare_models(
    results: dict[str, dict[str, float]],
) -> pd.DataFrame:
    """Compare plusieurs modèles dans un DataFrame trié par R² test.

    Parameters
    ----------
    results : dict
        Dictionnaire {nom_modele: métriques}.

    Returns
    -------
    pd.DataFrame
        DataFrame avec une ligne par modèle, trié par R² test décroissant.
    """
    rows = []
    for name, metrics in results.items():
        rows.append({
            "modèle": name,
            "MAE test (USD)": metrics["mae_test"],
            "RMSE test (USD)": metrics["rmse_test"],
            "R² test": metrics["r2_test"],
            "R² train": metrics["r2_train"],
            "Écart R²": metrics["r2_train"] - metrics["r2_test"],
        })

    df = pd.DataFrame(rows).sort_values("R² test", ascending=False)
    return df.reset_index(drop=True)