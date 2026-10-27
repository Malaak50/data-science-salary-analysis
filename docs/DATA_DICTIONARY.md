# Dictionnaire de données — Data Science Salaries

Source : `data/raw/DataScience_salaries_2025.csv` (151 445 lignes de données, 11 colonnes).
Voir `data/raw/README.md` pour la provenance et la licence.

> **Note :** les types et les valeurs possibles ci-dessous sont les valeurs
> *attendues* d'après la documentation publique ai-jobs.net et la sémantique
> usuelle. Ils seront **vérifiés empiriquement à l'étape 10** (valeurs uniques,
> valeurs manquantes, types réels). Ce document décrit ce que l'on *s'attend* à
> trouver, pas ce qui a déjà été observé.

## Vue d'ensemble

| # | Colonne | Type attendu | Rôle dans le projet |
|---|---------|--------------|---------------------|
| 1 | `work_year` | entier | Explicative |
| 2 | `experience_level` | catégorielle | Explicative |
| 3 | `employment_type` | catégorielle | Explicative |
| 4 | `job_title` | catégorielle (texte libre) | Explicative |
| 5 | `salary` | numérique | **Exclue** (fuite de données) |
| 6 | `salary_currency` | catégorielle | **Exclue** (fuite de données) |
| 7 | `salary_in_usd` | numérique | **Variable cible** |
| 8 | `employee_residence` | catégorielle | Explicative |
| 9 | `remote_ratio` | catégorielle ordinale | Explicative |
| 10 | `company_location` | catégorielle | Explicative |
| 11 | `company_size` | catégorielle ordinale | Explicative |

## Détail par colonne

### 1. `work_year`

- **Type attendu :** entier (année).
- **Signification :** année au cours de laquelle le salaire a été versé.
- **Valeurs attendues :** entiers entre 2020 et 2025 (à vérifier à l'étape 10).
- **Rôle :** variable explicative (tendance temporelle des salaires).
- **Piège :** peut être traitée comme catégorielle ou numérique ; à trancher
  à l'étape 32 selon la distribution observée.

### 2. `experience_level`

- **Type attendu :** chaîne, code à 2 lettres.
- **Signification :** niveau d'expérience professionnelle.
- **Valeurs attendues :**
  - `EN` = Entry-level / Junior
  - `MI` = Mid-level / Intermédiaire
  - `SE` = Senior
  - `EX` = Executive / Direction
- **Rôle :** variable explicative **majeure** (l'expérience est l'un des
  facteurs les plus associés au salaire).

### 3. `employment_type`

- **Type attendu :** chaîne, code à 2 lettres.
- **Signification :** type de contrat de travail.
- **Valeurs attendues :**
  - `FT` = Full-time (temps plein)
  - `PT` = Part-time (temps partiel)
  - `CT` = Contract (contrat)
  - `FL` = Freelance
- **Rôle :** variable explicative.

### 4. `job_title`

- **Type attendu :** chaîne de texte libre.
- **Signification :** intitulé du poste.
- **Valeurs attendues :** de nombreuses valeurs distinctes (data scientist,
  data engineer, data analyst, ML engineer, etc.), avec des variantes
  orthographiques. Le nombre exact de valeurs uniques sera mesuré à l'étape 10.
- **Rôle :** variable explicative **majeure**, mais à forte cardinalité →
  nécessitera une stratégie de réduction/groupe à l'étape 32 (regroupement
  des intitulés proches, encodage ciblé).

### 5. `salary`

- **Type attendu :** numérique (entier ou réel).
- **Signification :** salaire annuel brut **dans la devise locale** indiquée par
  `salary_currency`.
- **Rôle :** **EXCLUE** des variables explicatives. `salary_in_usd` est calculé
  à partir de `salary` et `salary_currency` → l'utiliser reviendrait à donner la
  réponse au modèle (fuite de données triviale).

### 6. `salary_currency`

- **Type attendu :** chaîne, code ISO 4217 à 3 lettres (USD, EUR, GBP, etc.).
- **Signification :** devise dans laquelle `salary` est exprimé.
- **Rôle :** **EXCLUE** des variables explicatives (même raison que `salary`).

### 7. `salary_in_usd`

- **Type attendu :** numérique (entier).
- **Signification :** salaire annuel brut converti en dollars américains.
- **Rôle :** **VARIABLE CIBLE** du projet de régression.
- **Piège :** distribution très probablement asymétrique à droite (quelques
  salaires très élevés). Une transformation logarithmique pourra être envisagée
  à l'étape 32, en la documentant et en vérifiant l'impact sur les métriques.

### 8. `employee_residence`

- **Type attendu :** chaîne, code pays à 2 lettres (ISO 3166-1 alpha-2).
- **Signification :** pays de résidence de l'employé.
- **Valeurs attendues :** codes à 2 lettres (US, GB, DE, FR, etc.).
- **Rôle :** variable explicative ; sera fusionnée avec un référentiel
  pays → continent à l'étape 22 pour réduire la cardinalité et permettre des
  analyses par zone géographique.

### 9. `remote_ratio`

- **Type attendu :** entier.
- **Signification :** proportion de télétravail.
- **Valeurs attendues :**
  - `0` = aucun télétravail (100 % présentiel)
  - `50` = hybride
  - `100` = télétravail complet
- **Rôle :** variable explicative. **Attention :** bien que numérique, cette
  variable est **catégorielle ordinale** (3 modalités), pas continue. La traiter
  comme continue dans un modèle linéaire supposerait une progression linéaire
  entre présentiel et télétravail complet, ce qui est une hypothèse forte à
  discuter. Décision d'encodage à prendre à l'étape 32.

### 10. `company_location`

- **Type attendu :** chaîne, code pays à 2 lettres (ISO 3166-1 alpha-2).
- **Signification :** pays du siège de l'employeur.
- **Rôle :** variable explicative ; même traitement que `employee_residence`
  (fusion pays → continent à l'étape 22).

### 11. `company_size`

- **Type attendu :** chaîne, 1 lettre.
- **Signification :** taille de l'entreprise.
- **Valeurs attendues :**
  - `S` = Small (moins de 50 employés)
  - `M` = Medium (50 à 250 employés)
  - `L` = Large (plus de 250 employés)
- **Rôle :** variable explicative, **catégorielle ordinale** (S < M < L).
  Encodage ordinal possible, à décider à l'étape 32.

## Variables exclues et justification

| Variable | Raison de l'exclusion |
|----------|----------------------|
| `salary` | Fuite de données : `salary_in_usd` en dérive directement. |
| `salary_currency` | Fuite de données : `salary_in_usd` en dérive directement. |

Ces deux colonnes restent présentes dans le DataFrame pour l'audit et la
documentation, mais **ne seront jamais** incluses dans `X` (les variables
explicatives) à l'étape 32. Elles feront l'objet d'une vérification explicite
dans le code d'entraînement (assertion ou sélection par liste blanche).

## Points à vérifier à l'étape 10

- Le type Pandas réel de chaque colonne correspond-il au type attendu ?
- Les valeurs de `experience_level`, `employment_type`, `company_size` et
  `remote_ratio` sont-elles **strictement** celles listées ci-dessus, ou
  existe-t-il des variantes (casse, espaces, valeurs inconnues) ?
- `salary_in_usd` contient-il des zéros, des valeurs négatives, ou des valeurs
  aberrantes (par exemple > 1 000 000 USD) ?
- Y a-t-il des valeurs manquantes, et sur quelles colonnes ?
- La plage de `work_year` est-elle bien celle attendue ?
- Combien de valeurs uniques pour `job_title`, `employee_residence`,
  `company_location` ?