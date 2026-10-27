"""Fonctions de prétraitement des données.

Contient :
- create_job_category : regroupe job_title en 10 catégories métier.
- add_continents : ajoute residence_continent et company_continent.
- build_preprocessor : construit le ColumnTransformer (StandardScaler +
  OneHotEncoder) prêt à être utilisé dans un Pipeline.
"""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from salary_prediction.config import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
)
from salary_prediction.country_mapping import COUNTRY_TO_CONTINENT


def create_job_category(title: str) -> str:
    """Regroupe un intitulé de poste en une catégorie métier.

    Parameters
    ----------
    title : str
        Intitulé de poste brut (ex. "Data Scientist").

    Returns
    -------
    str
        Catégorie métier parmi : Data Scientist, Software Engineer,
        Data Engineer, Data Analyst, ML Engineer, Manager, Architect,
        Engineer, Researcher, Other.
    """
    t = title.lower()

    # Ordre important : du plus spécifique au plus général
    if "data scientist" in t or "scientist" in t or "science" in t:
        return "Data Scientist"
    if "software engineer" in t or "developer" in t or "programmer" in t:
        return "Software Engineer"
    if "data engineer" in t or "big data" in t or "analytics engineer" in t:
        return "Data Engineer"
    if "data analyst" in t or "analyst" in t or "analytics" in t:
        return "Data Analyst"
    if "machine learning" in t or "ml" in t or "ai " in t or "artificial intelligence" in t:
        return "ML Engineer"
    if "manager" in t or "director" in t or "head" in t or "lead" in t:
        return "Manager"
    if "architect" in t:
        return "Architect"
    if "engineer" in t:
        return "Engineer"
    if "researcher" in t or "research" in t:
        return "Researcher"
    return "Other"


def add_job_category(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la colonne job_category au DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contenant la colonne job_title.

    Returns
    -------
    pd.DataFrame
        Copie du DataFrame avec job_category ajoutée.
    """
    if "job_title" not in df.columns:
        raise ValueError("Colonne 'job_title' absente du DataFrame")

    df = df.copy()
    df["job_category"] = df["job_title"].apply(create_job_category)
    return df


def add_continents(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les colonnes residence_continent et company_continent.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contenant employee_residence et company_location.

    Returns
    -------
    pd.DataFrame
        Copie du DataFrame avec les 2 colonnes de continent ajoutées.

    Raises
    ------
    ValueError
        Si des codes pays ne sont pas mappés dans COUNTRY_TO_CONTINENT.
    """
    required = ["employee_residence", "company_location"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Colonne '{col}' absente du DataFrame")

    df = df.copy()

    # Résidence
    df["residence_continent"] = df["employee_residence"].map(COUNTRY_TO_CONTINENT)
    df["company_continent"] = df["company_location"].map(COUNTRY_TO_CONTINENT)

    # Vérification : aucun NaN après mapping
    unmapped_res = set(df.loc[df["residence_continent"].isna(), "employee_residence"].unique())
    unmapped_com = set(df.loc[df["company_continent"].isna(), "company_location"].unique())
    unmapped = unmapped_res | unmapped_com
    if unmapped:
        raise ValueError(f"Codes pays non mappés : {sorted(unmapped)}")

    return df


def build_preprocessor() -> ColumnTransformer:
    """Construit le ColumnTransformer (StandardScaler + OneHotEncoder).

    Returns
    -------
    ColumnTransformer
        Préprocesseur prêt à être utilisé dans un Pipeline.

    Notes
    -----
    - StandardScaler sur NUMERIC_FEATURES.
    - OneHotEncoder(handle_unknown="ignore", sparse_output=False) sur
      CATEGORICAL_FEATURES.
    - Aucune colonne ne doit être oubliée (remainder="drop" par sécurité).
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )