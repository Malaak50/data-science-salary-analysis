"""Fixtures partagées pour les tests pytest."""

import pandas as pd
import pytest

from salary_prediction.config import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
)
from salary_prediction.data_loader import load_processed_data
from salary_prediction.preprocessing import add_job_category


@pytest.fixture(scope="session")
def df_processed():
    """DataFrame traité complet (151 445 lignes, 13 colonnes)."""
    return load_processed_data()


@pytest.fixture(scope="session")
def df_with_job_category(df_processed):
    """DataFrame avec job_category ajoutée (14 colonnes)."""
    return add_job_category(df_processed)


@pytest.fixture(scope="session")
def sample_features():
    """Dictionnaire de features valides pour une prédiction."""
    return {
        "work_year": 2025,
        "experience_level": "SE",
        "employment_type": "FT",
        "job_category": "Data Scientist",
        "remote_ratio": 0,
        "company_size": "M",
        "residence_continent": "North America",
        "company_continent": "North America",
    }


@pytest.fixture(scope="session")
def small_df():
    """Petit DataFrame (10 lignes) pour les tests rapides."""
    return pd.DataFrame({
        "work_year": [2024, 2024, 2024, 2024, 2024,
                      2025, 2025, 2025, 2025, 2025],
        "experience_level": ["EN", "MI", "SE", "EX", "SE",
                             "EN", "MI", "SE", "EX", "SE"],
        "employment_type": ["FT"] * 10,
        "job_title": ["Data Scientist", "Data Analyst", "Data Engineer",
                      "Manager", "Software Engineer",
                      "Data Scientist", "Data Analyst", "Data Engineer",
                      "Manager", "Software Engineer"],
        "salary": [50000, 80000, 120000, 200000, 150000,
                   55000, 85000, 125000, 210000, 155000],
        "salary_currency": ["USD"] * 10,
        TARGET: [50000, 80000, 120000, 200000, 150000,
                 55000, 85000, 125000, 210000, 155000],
        "employee_residence": ["US"] * 10,
        "remote_ratio": [0, 50, 100, 0, 50, 0, 50, 100, 0, 50],
        "company_location": ["US"] * 10,
        "company_size": ["M", "S", "L", "M", "M",
                         "M", "S", "L", "M", "M"],
        "residence_continent": ["North America"] * 10,
        "company_continent": ["North America"] * 10,
    })