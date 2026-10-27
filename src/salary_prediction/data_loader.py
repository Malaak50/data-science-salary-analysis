"""Fonctions de chargement des données.

Contient :
- load_raw_data : charge le CSV brut, avec vérifications de schéma.
- load_processed_data : charge le CSV traité, avec vérifications de schéma.
"""

from pathlib import Path

import pandas as pd

from salary_prediction.config import (
    EXPECTED_CATEGORIES,
    MAX_MISSING_RATIO,
    PROCESSED_CSV_PATH,
    RAW_CSV_PATH,
    TARGET,
)


def load_raw_data(path: Path = RAW_CSV_PATH) -> pd.DataFrame:
    """Charge le CSV brut et vérifie le schéma de base.

    Parameters
    ----------
    path : Path, optional
        Chemin vers le CSV brut. Par défaut RAW_CSV_PATH.

    Returns
    -------
    pd.DataFrame
        DataFrame brut.

    Raises
    ------
    FileNotFoundError
        Si le fichier n'existe pas.
    ValueError
        Si le schéma est incohérent (colonnes manquantes, cible absente,
        valeurs manquantes au-delà du seuil).
    """
    if not path.exists():
        raise FileNotFoundError(f"Fichier brut introuvable : {path}")

    df = pd.read_csv(path, encoding="utf-8")

    # Vérifications de schéma
    if TARGET not in df.columns:
        raise ValueError(f"Colonne cible '{TARGET}' absente du CSV brut")

    missing_ratio = df.isna().sum().sum() / (len(df) * len(df.columns))
    if missing_ratio > MAX_MISSING_RATIO:
        raise ValueError(
            f"Trop de valeurs manquantes dans le CSV brut : "
            f"{missing_ratio:.2%} > {MAX_MISSING_RATIO:.2%}"
        )

    return df


def load_processed_data(path: Path = PROCESSED_CSV_PATH) -> pd.DataFrame:
    """Charge le CSV traité et vérifie le schéma attendu.

    Le CSV traité doit contenir toutes les colonnes d'origine + les 2 colonnes
    de continent (residence_continent, company_continent).

    Parameters
    ----------
    path : Path, optional
        Chemin vers le CSV traité. Par défaut PROCESSED_CSV_PATH.

    Returns
    -------
    pd.DataFrame
        DataFrame traité.

    Raises
    ------
    FileNotFoundError
        Si le fichier n'existe pas.
    ValueError
        Si des colonnes attendues sont manquantes.
    """
    if not path.exists():
        raise FileNotFoundError(f"Fichier traité introuvable : {path}")

    df = pd.read_csv(path, encoding="utf-8")

    # Vérifications de schéma
    required_cols = [TARGET, "residence_continent", "company_continent"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Colonne attendue absente : {col}")

    # Vérification des catégories attendues
    for col, expected in EXPECTED_CATEGORIES.items():
        if col in df.columns:
            actual = set(df[col].unique())
            if not actual.issubset(expected):
                raise ValueError(
                    f"Valeurs inattendues dans '{col}' : {actual - expected}"
                )

    return df


def validate_dataframe(df: pd.DataFrame) -> None:
    """Vérifie qu'un DataFrame respecte le schéma attendu.

    Lève une ValueError si une vérification échoue.
    """
    if df.empty:
        raise ValueError("Le DataFrame est vide")

    if TARGET not in df.columns:
        raise ValueError(f"Colonne cible '{TARGET}' absente")

    if (df[TARGET] <= 0).any():
        raise ValueError(f"Valeurs de '{TARGET}' <= 0 détectées")

    if df[TARGET].isna().any():
        raise ValueError(f"Valeurs manquantes dans '{TARGET}'")

    for col, expected in EXPECTED_CATEGORIES.items():
        if col in df.columns:
            actual = set(df[col].unique())
            unexpected = actual - expected
            if unexpected:
                raise ValueError(f"Valeurs inattendues dans '{col}' : {unexpected}")