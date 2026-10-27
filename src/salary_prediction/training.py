"""Fonctions d'entraînement des modèles.

Contient :
- build_pipeline : construit un Pipeline (preprocessor + modèle).
- split_train_test : réalise un split stratifié groupé.
- train_model : entraîne un pipeline sur X_train, y_train.

Les modèles disponibles sont définis dans MODEL_FACTORIES pour permettre
l'ajout facile de nouveaux modèles.
"""

from typing import Literal

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.pipeline import Pipeline

from salary_prediction.config import (
    CATEGORICAL_FEATURES,
    FINAL_MODEL_PARAMS,
    NUMERIC_FEATURES,
    RANDOM_STATE,
    TARGET,
    TEST_SIZE,
)
from salary_prediction.preprocessing import build_preprocessor

ModelName = Literal["baseline", "lr", "rf", "gb"]

# Factories de modèles (permet d'ajouter facilement de nouveaux modèles)
MODEL_FACTORIES = {
    "baseline": lambda: DummyRegressor(strategy="median"),
    "lr": lambda: LinearRegression(),
    "rf": lambda: RandomForestRegressor(
        n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1
    ),
    "gb": lambda: GradientBoostingRegressor(
        n_estimators=FINAL_MODEL_PARAMS["n_estimators"],
        learning_rate=FINAL_MODEL_PARAMS["learning_rate"],
        max_depth=FINAL_MODEL_PARAMS["max_depth"],
        random_state=RANDOM_STATE,
    ),
}


def build_pipeline(model_name: ModelName) -> Pipeline:
    """Construit un Pipeline (preprocessor + modèle).

    Parameters
    ----------
    model_name : {"baseline", "lr", "rf", "gb"}
        Identifiant du modèle.

    Returns
    -------
    Pipeline
        Pipeline non entraîné, prêt à être fit.

    Raises
    ------
    ValueError
        Si model_name n'est pas reconnu.
    """
    if model_name not in MODEL_FACTORIES:
        raise ValueError(
            f"Modèle inconnu : '{model_name}'. "
            f"Disponibles : {list(MODEL_FACTORIES.keys())}"
        )
    return Pipeline([
        ("preprocessor", build_preprocessor()),
        ("model", MODEL_FACTORIES[model_name]()),
    ])


def split_train_test(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
    n_splits: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
    """Réalise un split train/test stratifié groupé.

    Le split est groupé sur la combinaison des 8 features pour éviter la
    fuite de données par duplication (voir étape 33 du projet).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contenant au moins TARGET et les features.
    test_size : float, optional
        Proportion du test. Par défaut TEST_SIZE (0.20).
    random_state : int, optional
        Graine aléatoire. Par défaut RANDOM_STATE (42).
    n_splits : int, optional
        Nombre de folds pour la stratification. Par défaut 5.

    Returns
    -------
    tuple
        (train_df, test_df, train_idx, test_idx)
    """
    # Construire les groupes (combinaison des features)
    group_cols = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    df = df.copy()
    df["_group_id"] = df[group_cols].astype(str).agg("|".join, axis=1)

    # Stratification sur experience_level (catégorie bien équilibrée)
    sgkf = StratifiedGroupKFold(
        n_splits=n_splits, shuffle=True, random_state=random_state
    )
    train_idx, test_idx = next(
        sgkf.split(df, y=df["experience_level"], groups=df["_group_id"])
    )

    train_df = df.iloc[train_idx].copy()
    test_df = df.iloc[test_idx].copy()

    return train_df, test_df, train_idx, test_idx


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: ModelName = "gb",
) -> Pipeline:
    """Entraîne un pipeline sur X_train, y_train.

    Parameters
    ----------
    X_train : pd.DataFrame
        Features d'entraînement.
    y_train : pd.Series
        Cible d'entraînement.
    model_name : ModelName, optional
        Identifiant du modèle. Par défaut "gb".

    Returns
    -------
    Pipeline
        Pipeline entraîné.
    """
    pipeline = build_pipeline(model_name)
    pipeline.fit(X_train, y_train)
    return pipeline