# Figures — Data Science Salaries

Ce dossier contient les visualisations produites par
`notebooks/03_visualization.ipynb` (phase 5).

Chaque figure est sauvegardée en **PNG** à une résolution de 150 dpi,
avec `bbox_inches="tight"` pour éviter les marges inutiles.

## Index des figures

### 1. `01_histogramme_salaires.png`
**Ce qu'elle montre :** distribution des salaires annuels en USD sur les
151 445 observations, avec la moyenne (ligne orange) et la médiane (ligne
verte foncé) en annotations.

**Insight clé :** la moyenne (157 527 USD) est supérieure à la médiane
(146 100 USD) de 11 427 USD. La distribution est asymétrique à droite :
quelques très hauts salaires (jusqu'à 800 000 USD) tirent la moyenne vers
le haut.

**Décision qui en découle :** privilégier la médiane comme indicateur
central, tester `log1p` sur la cible à l'étape 32.

---

### 2. `02_histogramme_log.png`
**Ce qu'elle montre :** comparaison côte à côte entre la distribution brute
(à gauche) et la distribution après transformation `log1p` (à droite).

**Insight clé :** la distribution transformée est beaucoup plus symétrique
(skew passe de 1,35 à -0,50 ; kurtosis passe de 4,69 à 0,77). L'écart
moyenne-médiane passe de 11 427 USD à -0,035 en log-USD.

**Décision qui en découle :** `log1p` sera testé sur la cible à l'étape 32.
La décision finale dépendra des métriques (MAE, RMSE, R²) en USD.

---

### 3. `03_boxplots_principaux.png`
**Ce qu'elle montre :** quatre boxplots comparant la distribution des
salaires selon `experience_level`, `company_size`, `remote_ratio` et
`employment_type`.

**Insights clés :**
- `experience_level` est le facteur le plus discriminant : progression nette
  de EN (~86k) à EX (~189k), avec une dispersion croissante.
- `company_size` : les petites entreprises (`S`) paient beaucoup moins
  (~75k) que les moyennes et grandes (~146k-150k).
- `remote_ratio` : présentiel et full remote sont équivalents (~145k-147k).
  Le groupe hybride (50%) est un artefact (329 obs).
- `employment_type` : FT domine massivement (99,5%). Les autres groupes
  (PT, CT, FL) sont trop petits pour être interprétés.

**Décision qui en découle :** `experience_level` est une variable
prioritaire. Les variables quasi constantes seront conservées mais leur
importance sera vérifiée à l'étape 43.

---

### 4. `04_heatmap_continent_experience.png`
**Ce qu'elle montre :** salaire médian par combinaison
`experience_level × residence_continent`. Les cellules avec effectif < 30
sont masquées (grisées) pour éviter les conclusions sur de petits échantillons.

**Insights clés :**
- L'Amérique du Nord domine à tous les niveaux d'expérience (EN 93k, MI 135k,
  SE 165k, EX 191k).
- L'Océanie paie très bien les juniors (EN 106k), mieux que l'Europe ne paie
  ses intermédiaires (MI 63k).
- L'Asie et l'Amérique du Sud sont les zones les moins bien payées.
- L'effet de l'expérience est additif et régulier dans chaque continent.

**Décision qui en découle :** `residence_continent` (7 modalités) est
préférée à `employee_residence` (104 modalités) pour réduire la cardinalité.

---

### 5. `05_top10_metiers_pays.png`
**Ce qu'elle montre :** deux graphiques en barres horizontales :
- À gauche, le Top 10 des métiers par salaire médian.
- À droite, le Top 10 des pays par salaire médian (filtré `effectif >= 100`).

**Insights clés :**
- **Attention au piège des métiers de niche :** le Top 10 métiers inclut des
  intitulés avec `n=1` ou `n=2` (ex: "AWS Data Architect"). Le graphique
  illustre pourquoi il faut toujours filtrer par effectif.
- **Les pays sont fiables :** le filtre `effectif >= 100` garantit que les
  médianes sont robustes. Les USA (135 506 obs) dominent, suivis du Canada
  (6 207) et de l'Australie (590).

**Décision qui en découle :** pour l'analyse des métiers, utiliser le
regroupement `job_category` (étape 32) et non les intitulés bruts.

---

### 6. `06_experience_remote.png`
**Ce qu'elle montre :** salaire médian par combinaison
`experience_level × remote_ratio` (barres groupées).

**Insights clés :**
- Pour `EN` et `MI`, le présentiel (0%) paie légèrement mieux que le full
  remote (100%).
- Pour `SE`, présentiel et full remote sont au coude-à-coude.
- Pour `EX`, le full remote (195k) dépasse le présentiel (188k).
- Le groupe hybride (50%) est anormalement bas partout (effectifs faibles).

**Décision qui en découle :** `remote_ratio` est un effet d'interaction
avec `experience_level`. Les modèles arborescents (Random Forest, Gradient
Boosting) captureront cette interaction naturellement ; les modèles linéaires
pourraient avoir besoin d'un terme d'interaction explicite.

---

## Comment régénérer ces figures

Ouvrir `notebooks/03_visualization.ipynb` dans VS Code, sélectionner le
kernel `.venv`, et exécuter *Run All* (`Ctrl+Shift+P` → *Jupyter: Run All
Cells*). Les 6 figures seront régénérées dans ce dossier.

## Ce que ces figures ne montrent PAS

- **Pas de causalité** : les associations observées ne prouvent pas de
  relations causales. La modélisation (phase 6) isolera les effets propres
  de chaque variable.
- **Pas de généralisation mondiale** : 93,7 % des lignes sont
  nord-américaines. Les conclusions ne sont pas représentatives du marché
  mondial.
- **Pas d'analyse temporelle** : la distribution temporelle (94 % en
  2024-2025) n'est pas visualisée ici, mais documentée dans
  `docs/STRATEGIE_NETTOYAGE.md`.