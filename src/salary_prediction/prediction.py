"""Fonctions de génération de prédictions.

Contient :
- load_pipeline : charge le pipeline sauvegardé (joblib).
- load_metadata : charge les métadonnées (JSON).
- predict_salary : prédit un salaire à partir d'un dictionnaire de features.
- predict_batch : prédit des salaires à partir d'un DataFrame.

Ces fonctions sont conçues pour être appelées par l'application Streamlit
(phase 8) et par les tests (phase 9). Elles ne font AUCUN entraînement.
"""

import json
from pathlib import Path
from typing import Any

import numpy as np          # ← ajouter si absent
import pandas as pd

try:
    import joblib
except ImportError:
    joblib = None

from salary_prediction.config import (
    FEATURES,
    METADATA_PATH,
    PIPELINE_PATH,
    TARGET,
)

from salary_prediction.config import (
    FEATURES,
    METADATA_PATH,
    PIPELINE_PATH,
    TARGET,
)


class PredictionError(Exception):
    """Erreur levée lors de la génération de prédictions."""


def load_pipeline(path: Path = PIPELINE_PATH):
    """Charge le pipeline sauvegardé.

    Parameters
    ----------
    path : Path, optional
        Chemin vers le fichier .joblib. Par défaut PIPELINE_PATH.

    Returns
    -------
    Pipeline
        Pipeline Scikit-Learn entraîné.

    Raises
    ------
    FileNotFoundError
        Si le fichier n'existe pas.
    PredictionError
        Si joblib n'est pas installé ou si le chargement échoue.
    """
    if joblib is None:
        raise PredictionError(
            "joblib n'est pas installé. Exécute `pip install joblib`."
        )
    if not path.exists():
        raise FileNotFoundError(
            f"Pipeline introuvable : {path}. "
            f"Exécute l'étape 44 (sauvegarde du pipeline) d'abord."
        )
    try:
        return joblib.load(path)
    except Exception as exc:
        raise PredictionError(f"Impossible de charger le pipeline : {exc}") from exc


def load_metadata(path: Path = METADATA_PATH) -> dict[str, Any]:
    """Charge les métadonnées du modèle.

    Parameters
    ----------
    path : Path, optional
        Chemin vers le fichier JSON. Par défaut METADATA_PATH.

    Returns
    -------
    dict
        Métadonnées du modèle.

    Raises
    ------
    FileNotFoundError
        Si le fichier n'existe pas.
    """
    if not path.exists():
        raise FileNotFoundError(f"Métadonnées introuvables : {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _validate_input(input_dict: dict[str, Any]) -> None:
    """Vérifie que le dictionnaire contient toutes les features attendues."""
    missing = set(FEATURES) - set(input_dict.keys())
    if missing:
        raise PredictionError(
            f"Features manquantes : {sorted(missing)}. "
            f"Attendu : {FEATURES}"
        )
    extra = set(input_dict.keys()) - set(FEATURES)
    if extra:
        # On tolère les extras (ex. TARGET, salary, etc.) mais on les signale
        # dans le message d'erreur pour éviter les confusions.
        raise PredictionError(
            f"Features inattendues : {sorted(extra)}. "
            f"Attendu : {FEATURES}"
        )


def predict_salary(
    input_dict: dict[str, Any],
    pipeline=None,
) -> float:
    """Prédit un salaire en USD à partir d'un dictionnaire de features.

    Parameters
    ----------
    input_dict : dict
        Dictionnaire avec les 8 features attendues.
        Exemple : {
            "work_year": 2025,
            "experience_level": "SE",
            "employment_type": "FT",
            "job_category": "Data Scientist",
            "remote_ratio": 100,
            "company_size": "M",
            "residence_continent": "North America",
            "company_continent": "North America",
        }
    pipeline : Pipeline, optional
        Pipeline déjà chargé (pour éviter de recharger le fichier à chaque
        appel). Si None, le pipeline est chargé depuis PIPELINE_PATH.

    Returns
    -------
    float
        Salaire prédit en USD.

    Raises
    ------
    PredictionError
        Si une feature est manquante ou en trop, ou si la prédiction échoue.
    """
    _validate_input(input_dict)

    if pipeline is None:
        pipeline = load_pipeline()

    try:
        X = pd.DataFrame([input_dict])
        prediction = pipeline.predict(X)[0]
    except Exception as exc:
        raise PredictionError(f"Échec de la prédiction : {exc}") from exc

    return float(prediction)


def predict_batch(
    df: pd.DataFrame,
    pipeline=None,
) -> pd.DataFrame:
    """Prédit des salaires pour un DataFrame de features.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame avec les 8 features attendues (au moins).
    pipeline : Pipeline, optional
        Pipeline déjà chargé. Si None, chargé depuis PIPELINE_PATH.

    Returns
    -------
    pd.DataFrame
        Copie du DataFrame avec une colonne supplémentaire
        'salary_predicted_usd'.
    """
    if pipeline is None:
        pipeline = load_pipeline()

    missing = set(FEATURES) - set(df.columns)
    if missing:
        raise PredictionError(f"Features manquantes : {sorted(missing)}")

    try:
        predictions = pipeline.predict(df[FEATURES])
    except Exception as exc:
        raise PredictionError(f"Échec de la prédiction par lot : {exc}") from exc

    result = df.copy()
    result["salary_predicted_usd"] = predictions
    return result
def test_pipeline_roundtrip(
    X_test: pd.DataFrame,
    pipeline_path: Path = PIPELINE_PATH,
    tolerance: float = 1e-6,
) -> dict[str, Any]:
    """Vérifie que le pipeline rechargé produit les mêmes prédictions.

    Parameters
    ----------
    X_test : pd.DataFrame
        Données de test (features uniquement).
    pipeline_path : Path, optional
        Chemin du pipeline sauvegardé.
    tolerance : float, optional
        Tolérance pour la comparaison des prédictions.

    Returns
    -------
    dict
        Résultat du test : {"succes": bool, "message": str,
        "max_diff": float, "n_predictions": int}.
    """
    # 1. Recharger le pipeline depuis le fichier
    pipeline_reloaded = load_pipeline(pipeline_path)

    # 2. Faire une prédiction sur X_test
    y_pred_reloaded = pipeline_reloaded.predict(X_test[FEATURES])

    # 3. Recharger le pipeline une seconde fois (indépendance)
    pipeline_reloaded_2 = load_pipeline(pipeline_path)
    y_pred_reloaded_2 = pipeline_reloaded_2.predict(X_test[FEATURES])

    # 4. Comparer les deux prédictions
    max_diff = float(np.max(np.abs(y_pred_reloaded - y_pred_reloaded_2)))

    succes = max_diff < tolerance
    message = (
        f"✔ Roundtrip OK : {len(y_pred_reloaded)} prédictions, "
        f"écart max = {max_diff:.2e}"
        if succes
        else f"✘ ÉCHEC : écart max = {max_diff:.2e} > tolérance {tolerance:.2e}"
    )

    return {
        "succes": succes,
        "message": message,
        "max_diff": max_diff,
        "n_predictions": len(y_pred_reloaded),
    }