# Stratégie de nettoyage — Data Science Salaries

Source : `data/raw/DataScience_salaries_2025.csv`
(151 445 lignes de données, 11 colonnes, 0 valeur manquante)
Provenance : Kaggle — curation multi-sources incluant AIJobs (CC0),
365DataScience, Payscale, KDnuggets, ZipRecruiter.
Voir `data/raw/README.md` pour le détail.

Ce document décrit les décisions de nettoyage et de préparation **avant**
toute implémentation. Il sera appliqué à l'étape 19 (Pandas). Toute décision
est justifiée par une observation chiffrée de l'étape 10.

---

## 1. Principe directeur

**Ne jamais modifier les données brutes.** `data/raw/` est immuable. Toutes les
transformations sont appliquées en mémoire ou écrites dans `data/processed/`
(étape 24). Cela garantit que l'on peut toujours revenir à la source et que
le pipeline est reproductible.

---

## 2. Valeurs manquantes

- **Observation :** 0 valeur manquante sur les 11 colonnes (151 445 × 11 cellules).
- **Décision :** aucune imputation, aucune suppression pour cause de `NaN`.
- **Risque résiduel :** l'absence totale de `NaN` sur un survey réel de 151 445
  lignes est inhabituelle. Elle s'explique probablement par un nettoyage en amont
  par le curateur du dataset. Ce point sera mentionné dans les limites du README
  final.

---

## 3. Doublons

### 3.1 Observation

- **79 532 doublons complets** (52,5 % des lignes).
- **5 639 combinaisons uniques** des 8 variables explicatives.
- La ligne la plus répétée apparaît **195 fois** (Data Scientist, 2025, SE, FT,
  160 000 USD, US, 100, M).

### 3.2 Interprétation

Les doublons sont **légitimes** : ils proviennent d'une enquête réelle
multi-sources où plusieurs répondants partageant le même profil déclarent un
salaire identique (salaires souvent arrondis : 90 000, 150 000, 160 000 USD).
Ce ne sont **pas** des artefacts de génération synthétique. L'explication
détaillée figure dans `data/raw/README.md`.

### 3.3 Décision

Deux protections **cumulées** contre la fuite de données par duplication :

1. **Déduplication avant split.** `df.drop_duplicates()` → 71 913 lignes
   uniques (151 445 − 79 532). Toutes les expérimentations de modélisation
   (phase 6) partiront de ce DataFrame dédupliqué.
2. **Split groupé.** Même après déduplication, des combinaisons de variables
   explicatives restent partagées par plusieurs lignes (seul le salaire diffère).
   Le split train/test utilisera `GroupShuffleSplit` avec
   `groups = df[8 variables explicatives].astype(str).agg("|".join, axis=1)`,
   afin qu'aucune combinaison explicative ne se retrouve à la fois dans le train
   et dans le test.

**Justification :** un `train_test_split` aléatoire naïf sur un dataset dupliqué
gonfle artificiellement les métriques. Le split groupé est la seule protection
rigoureuse. Cette décision sera rappelée à l'étape 33.

---

## 4. Variables exclues (fuite de données)

| Variable | Décision | Justification |
|----------|----------|---------------|
| `salary` | **Exclue** de `X` | `salary_in_usd` en dérive directement (via `salary_currency`). L'inclure donnerait un R² artificiellement proche de 1. |
| `salary_currency` | **Exclue** de `X` | Même raison. |

Ces deux colonnes restent dans le DataFrame pour l'audit, mais **ne seront
jamais** incluses dans les variables explicatives. Une assertion en code
(liste blanche) sera ajoutée à l'étape 32 pour empêcher toute réintroduction
accidentelle.

---

## 5. Variable cible `salary_in_usd`

- **Distribution :** moyenne 157 548, médiane 146 232, asymétrie 1,34,
  kurtosis 4,76, min 15 000, max 800 000.
- **Aucune valeur ≤ 0**, aucune valeur > 1 000 000 : pas d'aberration évidente.
- **Décision :** conserver toutes les valeurs. Aucune suppression d'outlier
  a priori.
- **Transformation :** une transformation `log1p` pourra être testée à l'étape 32
  pour réduire l'asymétrie. Elle sera **évaluée empiriquement** (comparaison des
  métriques avec et sans transformation) et documentée. Les métriques finales
  (MAE, RMSE) seront toujours rapportées dans l'espace d'origine (USD) pour
  rester interprétables.

---

## 6. Variable `job_title` — cardinalité élevée

- **Observation :** 317 valeurs uniques.
- **Problème :** un one-hot encoding naïf créerait 317 colonnes, dont beaucoup
  avec très peu d'occurrences (risque de sur-apprentissage et de colonnes
  quasi vides).
- **Décision :** regrouper les intitulés en **catégories métier** à l'étape 32,
  selon une table de correspondance documentée. Regroupement proposé (à affiner
  après inspection des 317 valeurs) :
  - `data_scientist` (data scientist, lead data scientist, etc.)
  - `data_engineer` (data engineer, big data engineer, etc.)
  - `data_analyst` (data analyst, business analyst, etc.)
  - `ml_engineer` (machine learning engineer, mlops, ai engineer, etc.)
  - `research` (research scientist, researcher, etc.)
  - `architect` (data architect, cloud architect, etc.)
  - `manager` (manager, director, head of data, etc.)
  - `other` (tout le reste)
- **Justification :** réduire la cardinalité tout en conservant le signal métier
  principal. La table exacte sera écrite et vérifiée à l'étape 32.

---

## 7. Variables quasi constantes

| Variable | Modalité dominante | % | Décision |
|----------|-------------------|----|----------|
| `company_size` | `M` | 96,8 % | Conserver pour l'analyse descriptive ; documenter le faible pouvoir discriminant. |
| `employment_type` | `FT` | 99,5 % | Idem. |
| `remote_ratio` | `0` | 78,0 % | Idem ; traiter comme catégorielle ordinale (0/50/100), pas comme continue. |

**Justification :** une variable à plus de 95 % sur une modalité apporte très peu
d'information au modèle. On ne la supprime pas (elle peut avoir un effet marginal
et sa suppression serait arbitraire), mais on **documente** sa faible importance
attendue. L'analyse d'importance des variables (étape 43) confirmera ou
infirmera cette attente.

---

## 8. Déséquilibre temporel

- **Observation :** 94 % des lignes en 2024–2025 (66,5 % en 2024, 22,3 % en 2025,
  9,1 % en 2023, 1,8 % sur 2020–2022).
- **Décision :** conserver `work_year` dans un premier temps, mais documenter
  cette limite. À l'étape 32, deux scénarios seront comparés :
  - **Scénario A :** `work_year` incluse comme variable numérique.
  - **Scénario B :** `work_year` exclue.
  La comparaison se fera sur le même split groupé, et le scénario retenu sera
  justifié dans le notebook.
- **Justification :** une variable temporelle très déséquilibrée peut dominer
  artificiellement le modèle et dégrader la généralisation aux années sous-
  représentées. Ne pas la conserver par défaut sans vérification serait une
  erreur méthodologique.

---

## 9. Types et conversions

- **Types actuels :** `int64` pour `work_year`, `salary`, `salary_in_usd`,
  `remote_ratio` ; `str` pour les 7 autres colonnes.
- **Décision :**
  - Convertir les colonnes catégorielles (`experience_level`, `employment_type`,
    `job_title`, `salary_currency`, `employee_residence`, `company_location`,
    `company_size`) en type `category` **après** le split train/test, pour
    économiser la mémoire et accélérer les groupbys. La conversion n'a pas
    d'impact sur les valeurs.
  - Ne **pas** convertir `remote_ratio` en `category` avant l'étape 32 : le
    choix d'encodage (ordinal vs one-hot) sera décidé à ce moment-là.
  - Ne **pas** convertir `work_year` en `category` : le scénario A/B de la
    section 8 tranchera.

---

## 10. Valeurs catégorielles inattendues

- **Observation :** les 4 variables catégorielles contrôlées
  (`experience_level`, `employment_type`, `company_size`, `remote_ratio`)
  contiennent exactement les valeurs attendues, sans variante de casse ni espace.
- **Décision :** aucune normalisation de casse ni `strip()` nécessaire. Une
  assertion de contrôle sera ajoutée à l'étape 19 pour vérifier que les valeurs
  restent dans les ensembles attendus après application de la stratégie.

---

## 11. Données traitées — sortie attendue (étape 24)

Le DataFrame nettoyé sera écrit dans `data/processed/salaries_clean.csv` avec :

- toutes les colonnes d'origine (pour audit) ;
- une colonne supplémentaire `job_category` (issue du regroupement de l'étape 32) ;
- les types `category` appliqués aux colonnes catégorielles ;
- **les doublons non supprimés dans le fichier** : la déduplication est une
  décision de **modélisation**, pas une décision de stockage. Le fichier
  `data/processed/` conserve toutes les lignes pour permettre d'autres analyses
  (descriptives, visualisations) qui n'ont pas besoin de déduplication. La
  déduplication est appliquée **au moment du split** (étape 33).

---

## 12. Ce que l'on ne fait PAS

- On ne supprime pas les valeurs extrêmes de `salary_in_usd` (elles sont
  plausibles métier).
- On n'impute pas de valeurs manquantes (il n'y en a pas).
- On ne normalise pas les salaires par l'inflation (hors périmètre du projet ;
  mentionné dans les limites).
- On ne supprime pas les doublons du fichier de stockage (voir section 11).
- On n'utilise pas `salary` ni `salary_currency` comme variables explicatives.

---

## 13. Traçabilité

Chaque décision ci-dessus est reliée à une observation chiffrée de l'étape 10.
Toute modification future de cette stratégie devra être justifiée et datée dans
ce document (section « Journal des modifications »).

### Journal des modifications

- **2026-10-24 :** version initiale, rédigée après le diagnostic de l'étape 10
  sur le dataset ai-jobs.net multi-sources (151 445 lignes, 79 532 doublons).