# 💰 Data Science Salary Analysis & Salary Prediction

**Analyse et prédiction des salaires dans la Data Science** — Projet portfolio de Data Science / Machine Learning.

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.66-red.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/tests-40%20passed-brightgreen.svg)]()

---

## 📌 Problématique

**Quels sont les facteurs associés aux salaires des professionnels de la Data Science, et peut-on prédire leur salaire annuel à partir de leurs caractéristiques professionnelles ?**

Ce projet répond à cette question en trois temps :
1. **Exploration** des données salariales (2020–2025).
2. **Modélisation** de la relation entre caractéristiques et salaire.
3. **Mise en production** d'une application web interactive (Streamlit).

---

## 🎯 Résultats clés

| Modèle | MAE test | RMSE test | R² test |
|--------|----------|-----------|---------|
| Baseline (médiane) | 54 207 USD | 73 873 USD | −0,037 |
| Régression Linéaire | 48 325 USD | 65 065 USD | 0,196 |
| Random Forest | 47 796 USD | 65 917 USD | 0,174 |
| **Gradient Boosting** ⭐ | **47 964 USD** | **64 788 USD** | **0,203** |

**Le Gradient Boosting est le modèle retenu** (meilleur R² test, meilleure RMSE). Il estime le salaire annuel avec une erreur moyenne de **± 47 964 USD**.

**Facteurs les plus discriminants** (importance des variables) :
1. `job_category` (46 % de l'importance) — le métier.
2. `experience_level` (27 %) — le niveau d'expérience.
3. `residence_continent` (24 %) — la localisation géographique.

---

## 📊 Données

- **Source :** [Kaggle — Data Science Salaries 2020-2025](https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs)
- **Taille :** 151 445 profils, 11 colonnes d'origine.
- **Période :** 2020–2025 (94 % des données en 2024–2025).
- **Licence :** CC0 1.0 (domaine public, source originale ai-jobs.net).
- **Variables :** année, niveau d'expérience, type d'emploi, intitulé du poste, salaire (devise locale et USD), pays de résidence, taux de télétravail, pays de l'employeur, taille d'entreprise.

**Provenance détaillée :** voir [`data/raw/README.md`](data/raw/README.md).

---

## 🗂️ Structure du projet

```
data-science-salary-analysis/
│
├── data/
│   ├── raw/                      # CSV brut (exclu de Git)
│   │   └── README.md             # Provenance et licence
│   └── processed/                # CSV traité (exclu de Git)
│       └── README.md             # Description de l'export
│
├── notebooks/
│   ├── 01_numpy_analysis.ipynb    # Analyse NumPy (phase 3)
│   ├── 02_pandas_analysis.ipynb   # Analyse Pandas (phase 4)
│   ├── 03_visualization.ipynb     # Visualisation (phase 5)
│   └── 04_machine_learning.ipynb  # Modélisation (phase 6)
│
├── src/salary_prediction/         # Package Python (phase 7)
│   ├── __init__.py
│   ├── config.py                  # Constantes centralisées
│   ├── country_mapping.py         # Référentiel pays → continent
│   ├── data_loader.py             # Chargement des données
│   ├── preprocessing.py           # Feature engineering
│   ├── training.py                # Entraînement
│   ├── evaluation.py              # Métriques
│   └── prediction.py              # Prédictions
│
├── tests/                         # Tests automatisés (40 tests)
│   ├── conftest.py
│   ├── test_data_loader.py
│   ├── test_preprocessing.py
│   ├── test_training_evaluation.py
│   └── test_prediction.py
│
├── models/
│   ├── salary_prediction_pipeline.joblib  # Pipeline sauvegardé
│   └── metadata.json              # Métadonnées du modèle
│
├── images/                        # Figures générées (phase 5)
├── reports/                       # Rapports d'analyse
│
├── app.py                         # Application Streamlit (phase 8)
├── requirements.txt               # Dépendances
├── pyproject.toml                 # Package installable
├── .gitignore
├── README.md
└── presentation.pdf               # Présentation (optionnel)
```

---

## 🚀 Installation

### Prérequis

- Python 3.12+
- Git
- Un terminal (PowerShell, CMD, ou bash)

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/Malaak50/data-science-salary-analysis.git
cd data-science-salary-analysis

# 2. Créer et activer l'environnement virtuel
python -m venv .venv
# Windows :
.venv\Scripts\activate
# macOS/Linux :
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
pip install -e .   # installe le package salary_prediction en mode éditable

# 4. Télécharger les données (voir data/raw/README.md pour la licence)
# Placez le CSV dans data/raw/DataScience_salaries_2025.csv

# 5. Régénérer les données traitées (nécessite les notebooks)
# Ou utilisez directement le pipeline sauvegardé dans models/
```

---

## 💻 Utilisation

### Application Streamlit (recommandée)

```bash
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`. Renseignez les 8 champs du formulaire et obtenez une prédiction instantanée.

### Notebooks

```bash
jupyter notebook
```

Les notebooks sont numérotés dans l'ordre logique du projet :
1. `01_numpy_analysis.ipynb` — exploration NumPy.
2. `02_pandas_analysis.ipynb` — nettoyage et analyse avec Pandas.
3. `03_visualization.ipynb` — visualisations.
4. `04_machine_learning.ipynb` — modélisation.

### Tests

```bash
pytest tests/ -v
```

**40 tests** couvrent le chargement, le prétraitement, l'entraînement, l'évaluation et la prédiction.

### Prédiction programmatique

```python
from salary_prediction.prediction import predict_salary

profile = {
    "work_year": 2025,
    "experience_level": "SE",
    "employment_type": "FT",
    "job_category": "Data Scientist",
    "remote_ratio": 0,
    "company_size": "M",
    "residence_continent": "North America",
    "company_continent": "North America",
}

salary = predict_salary(profile)
print(f"Salaire estimé : {salary:,.0f} USD")
# → Salaire estimé : 182,498 USD
```

---

## 🔬 Méthodologie

### 1. Compréhension et nettoyage des données (phases 1–2)
- Chargement du CSV, diagnostic (types, valeurs manquantes, doublons).
- **52,5 % de doublons complets** identifiés et expliqués (enquête multi-sources, salaires arrondis).
- Aucune valeur manquante, aucune valeur aberrante.
- Stratégie de nettoyage documentée dans [`docs/STRATEGIE_NETTOYAGE.md`](docs/STRATEGIE_NETTOYAGE.md).

### 2. Analyse exploratoire (phases 3–5)
- **NumPy** : statistiques descriptives (moyenne, médiane, quantiles, asymétrie).
- **Pandas** : `groupby`, `pivot_table`, fusion avec référentiel pays → continent.
- **Matplotlib/Seaborn** : histogrammes, boxplots, heatmaps, barplots.
- **6 figures** dans `images/`, documentées dans `images/README.md`.

### 3. Feature engineering (phase 6)
- **`job_category`** : regroupement des 422 intitulés de poste en **10 catégories métier**.
  - **Décision de conception documentée :** `"Research Scientist"` est classé en `"Data Scientist"` (et non `"Researcher"`), car les deux rôles ont des profils salariaux proches (médiane 150–180k USD) et `"scientist"` est un terme générique. Ce choix est **figé par un test** (`test_create_job_category[Research Scientist-Data Scientist]`) et cohérent avec l'idée que la catégorie `"Researcher"` est réservée aux titres sans `"scientist"` (ex. `"AI Researcher"`, `"Researcher"`).
- **Continents** : réduction de la cardinalité géographique (104 pays → 7 continents).
- **Variables exclues** : `salary` et `salary_currency` (fuite de données).

### 4. Modélisation (phase 6)
- **Split stratifié groupé** (`StratifiedGroupKFold`) pour éviter la fuite par duplication.
- **4 modèles comparés** : baseline, régression linéaire, Random Forest, Gradient Boosting.
- **Pipelines Scikit-Learn** pour garantir l'absence de fuite lors de la validation croisée.
- **GridSearchCV** testé mais non retenu (pas de gain significatif sur le test).

### 5. Mise en production (phases 7–8)
- **Package Python** `salary_prediction` installable (`pip install -e .`).
- **Pipeline sauvegardé** (`joblib`) avec métadonnées.
- **Application Streamlit** avec formulaire, prédiction en USD, gestion des cas limites.

### 6. Tests et documentation (phase 9)
- **40 tests pytest** couvrant tous les modules.
- Documentation complète : `docs/`, `reports/`, `images/README.md`.

---

## 📈 Limites du projet

**Transparence sur les limites** — toute prédiction doit être interprétée avec recul.

1. **R² de 0,20** : le modèle n'explique que 20 % de la variance des salaires. Il donne une tendance, pas une prédiction exacte.
2. **Biais géographique** : 93,7 % des données sont nord-américaines. Les prédictions sont plus fiables sur ce marché que sur d'autres.
3. **Biais sur les extrêmes** : les salaires très élevés (> 500 000 USD) sont sous-estimés. Les salaires bas (< 100 000 USD) sont sur-estimés.
4. **Sous-groupes rares** : l'Amérique du Sud, l'Afrique, le Moyen-Orient et le métier de « Researcher » sont mal prédits (effectifs faibles).
5. **Données d'enquête** : les salaires sont auto-déclarés, souvent arrondis. Le dataset contient 52,5 % de doublons exacts.
6. **Pas de causalité** : les associations observées ne prouvent pas de relations causales. Le métier, l'expérience et la localisation sont corrélés au salaire, mais ne le causent pas au sens strict.
7. **Classification des métiers** : le regroupement en 10 catégories est un choix de conception. `"Research Scientist"` est classé en `"Data Scientist"` (voir section Méthodologie). Ce choix est documenté par un test, mais il pourrait être affiné dans une version future.

**Usage prévu :** prédictions **indicatives** pour des profils comparables au dataset. Ne remplace pas une évaluation humaine pour une décision salariale réelle.

---

## 🛠️ Technologies utilisées

| Catégorie | Outils |
|-----------|--------|
| Langage | Python 3.12 |
| Calcul scientifique | NumPy 2.5, Pandas 3.1 |
| Visualisation | Matplotlib 3.11, Seaborn 0.13 |
| Machine Learning | Scikit-Learn 1.9 |
| Application web | Streamlit 1.66 |
| Tests | pytest 9.1 |
| Versioning | Git, GitHub |
| Sérialisation | joblib |

---

## 👤 Auteur

**Malak** — Projet portfolio Data Science / Machine Learning.

- 📧 Email : [malakmahir200@gmail.com]
- 💼 LinkedIn : [linkedin.com/in/malak-mahir-909880296]https://www.linkedin.com/in/malak-mahir-909880296)
- 🐙 GitHub : [github.com/Malaak50](https://github.com/Malaak50)
---

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Voir [`LICENSE`](LICENSE).

Les **données** sont sous licence **CC0 1.0** (domaine public) — voir [`data/raw/README.md`](data/raw/README.md).

---

## 🙏 Remerciements

- [ai-jobs.net](https://ai-jobs.net/salaries/) pour les données originales.
- [Kaggle](https://www.kaggle.com/) pour la curation du dataset.
- La communauté Scikit-Learn pour la documentation et les bonnes pratiques.

---

*Projet réalisé dans le cadre d'un portfolio Data Science. Dernière mise à jour : 2026-10-27.*