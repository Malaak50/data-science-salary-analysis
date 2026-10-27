# Données traitées — Data Science Salaries

## Fichier

- **Nom :** `salaries_clean.csv`
- **Produit par :** `notebooks/02_pandas_analysis.ipynb` (section 8)
- **Format :** CSV UTF-8, séparateur virgule, en-tête inclus, index Pandas non écrit (`index=False`)
- **Taille :** voir la sortie de la cellule 8.2 du notebook (typiquement ~15 Mo)
- **Lignes :** 151 445 (aucune suppression)
- **Colonnes :** 13

## Schéma

| # | Colonne | Type | Rôle |
|---|---------|------|------|
| 1 | `work_year` | int64 | Explicative |
| 2 | `experience_level` | str | Explicative |
| 3 | `employment_type` | str | Explicative |
| 4 | `job_title` | str | Explicative (à regrouper à l'étape 32) |
| 5 | `salary` | int64 | **Exclue** (fuite de données) |
| 6 | `salary_currency` | str | **Exclue** (fuite de données) |
| 7 | `salary_in_usd` | int64 | **Variable cible** |
| 8 | `employee_residence` | str | Explicative |
| 9 | `remote_ratio` | int64 | Explicative (ordinale) |
| 10 | `company_location` | str | Explicative |
| 11 | `company_size` | str | Explicative (ordinale) |
| 12 | `residence_continent` | str | Explicative (ajoutée à l'étape 22) |
| 13 | `company_continent` | str | Explicative (ajoutée à l'étape 22) |

## Ce qui est conservé

- **Toutes les lignes** : 151 445, y compris les **79 532 doublons complets**
  (déduplication au moment du split, étape 33).
- **Toutes les valeurs extrêmes** de `salary_in_usd` (min 15 000, max 800 000).
  Aucune n'est aberrante au regard du métier.
- **Aucune valeur manquante** (0 depuis le chargement).

## Ce qui n'est PAS dans le fichier

- `job_category` : créé à l'étape 32, après le split train/test.
- `salary_in_usd_log` : transformation de la cible, testée à l'étape 32.
- `is_train` / `is_test` : indicateurs de split, créés à l'étape 33.
- Les prédictions du modèle : sauvegardées dans `models/` à l'étape 44.

## Pourquoi ce fichier n'est pas versionné sur Git

`.gitignore` contient `data/processed/*.csv`. Ce fichier est **régénérable**
en réexécutant le notebook `02_pandas_analysis.ipynb` (section 8). On
versionne **le code qui produit les données**, pas les données dérivées —
convention standard en Data Science.

## Comment régénérer ce fichier

Depuis la racine du projet, avec le venv activé :

```cmd
jupyter nbconvert --to notebook --execute notebooks/02_pandas_analysis.ipynb --output 02_pandas_analysis_executed.ipynb