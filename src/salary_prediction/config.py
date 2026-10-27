"""Configuration centrale du projet.

Centralise toutes les constantes : chemins, noms de features, hyperparamètres,
seuils. Toute modification de configuration doit passer par ce fichier.
"""

from pathlib import Path

# === Racine du projet ===
# config.py est dans src/salary_prediction/ -> remonter 3 niveaux pour la racine
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# === Répertoires ===
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
IMAGES_DIR = PROJECT_ROOT / "images"
REPORTS_DIR = PROJECT_ROOT / "reports"
DOCS_DIR = PROJECT_ROOT / "docs"

# Création des répertoires s'ils n'existent pas (idempotent)
for _dir in [DATA_PROCESSED_DIR, MODELS_DIR, IMAGES_DIR, REPORTS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# === Fichiers de données ===
RAW_CSV_PATH = DATA_RAW_DIR / "DataScience_salaries_2025.csv"
PROCESSED_CSV_PATH = DATA_PROCESSED_DIR / "salaries_clean.csv"
PIPELINE_PATH = MODELS_DIR / "salary_prediction_pipeline.joblib"
METADATA_PATH = MODELS_DIR / "metadata.json"

# === Variable cible ===
TARGET = "salary_in_usd"

# === Features ===
NUMERIC_FEATURES = ["work_year"]

CATEGORICAL_FEATURES = [
    "experience_level",
    "employment_type",
    "job_category",
    "remote_ratio",
    "company_size",
    "residence_continent",
    "company_continent",
]

# Liste complète des features (ordre non significatif)
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# === Colonnes exclues (fuite de données) ===
LEAKAGE_COLS = ["salary", "salary_currency"]

# === Colonnes géographiques à forte cardinalité (remplacées par continents) ===
HIGH_CARDINALITY_GEO = ["employee_residence", "company_location"]

# === Colonnes non-features (identifiants, intitulés bruts, colonnes techniques) ===
# Note : job_title est remplacé par job_category
NON_FEATURE_COLS = LEAKAGE_COLS + HIGH_CARDINALITY_GEO + ["job_title"]

# === Valeurs attendues des variables catégorielles (pour assertions) ===
EXPECTED_CATEGORIES = {
    "experience_level": {"EN", "MI", "SE", "EX"},
    "employment_type": {"FT", "PT", "CT", "FL"},
    "company_size": {"S", "M", "L"},
    "remote_ratio": {0, 50, 100},
}

# === Hyperparamètres ===
RANDOM_STATE = 42
TEST_SIZE = 0.20
CV_N_SPLITS = 5  # pour StratifiedGroupKFold (étape 33)

# === Hyperparamètres du modèle final (GB par défaut, étape 44) ===
FINAL_MODEL_PARAMS = {
    "n_estimators": 100,
    "learning_rate": 0.1,
    "max_depth": 3,
}

# === Métriques de référence (étape 44) ===
REFERENCE_METRICS = {
    "model_name": "Gradient Boosting (défaut, non optimisé)",
    "R2_test": 0.2025,
    "MAE_test_usd": 47964.0,
    "RMSE_test_usd": 64788.0,
    "R2_train": 0.2431,
    "MAE_train_usd": 47344.0,
    "RMSE_train_usd": 64589.0,
}

# === Seuils d'alerte ===
MAX_MISSING_RATIO = 0.0       # tolérance de valeurs manquantes (0 = aucune)
MAX_DUPLICATE_RATIO = 0.60    # au-delà, le dataset est suspect (52,5 % observé)
MIN_GROUP_SIZE = 30           # seuil pour interpréter une médiane par groupe

# === Versions minimales des dépendances ===
MIN_VERSIONS = {
    "python": "3.12",
    "numpy": "2.0",
    "pandas": "3.0",
    "scikit_learn": "1.4",
    "streamlit": "1.30",
}