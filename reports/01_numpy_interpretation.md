# Rapport — Interprétation des statistiques NumPy

**Projet :** Data Science Salary Analysis & Salary Prediction
**Notebook source :** `notebooks/01_numpy_analysis.ipynb`
**Date :** 2026-10-26
**Dataset :** `data/raw/DataScience_salaries_2025.csv` (151 445 lignes)

---

## 1. Statistiques calculées

| Indicateur | Valeur |
|------------|--------|
| Effectif | 151 445 |
| Moyenne | 157 527,46 USD |
| Médiane | 146 100,00 USD |
| Écart-type (ddof=1) | 74 150,77 USD |
| Coefficient de variation | 47,07 % |
| Minimum | 15 000 USD |
| Maximum | 800 000 USD |
| p1 | 36 842 USD |
| p5 | 60 000 USD |
| Q1 (p25) | 105 800 USD |
| Médiane (p50) | 146 100 USD |
| Q3 (p75) | 198 000 USD |
| p95 | 290 180 USD |
| p99 | 385 000 USD |
| Asymétrie (skewness) | 1,35 |
| Kurtosis | 4,69 |

## 2. Contrôle de cohérence

Les statistiques calculées via NumPy (`np.mean`, `np.median`, `np.std(ddof=1)`)
et via Pandas (`Series.mean`, `Series.median`, `Series.std`) sont **identiques
à 0,0 près** sur les cinq indicateurs testés (moyenne, médiane, min, max,
écart-type). Ce double contrôle confirme la fiabilité de la lecture des données.

## 3. Interprétation métier

### 3.1 La moyenne est trompeuse

La moyenne (157 527 USD) dépasse la médiane (146 100 USD) de **11 427 USD**.
Quelques salaires exceptionnels tirent la moyenne vers le haut. La médiane est
donc l'indicateur central à privilégier pour décrire le marché.

### 3.2 Distribution asymétrique à droite

L'asymétrie de **1,35** confirme la queue droite longue. Une transformation
`log1p` de la cible sera testée à l'étape 32.

### 3.3 Forte dispersion

Le coefficient de variation de **47,07 %** montre que les salaires sont très
hétérogènes. Les variables explicatives (expérience, métier, pays, télétravail)
devront être exploitées pour tenter d'expliquer cette dispersion.

### 3.4 Valeurs extrêmes légitimes

Le min (15 000 USD) et le max (800 000 USD) correspondent à des réalités du
marché. La kurtosis de **4,69** (queues épaisses) confirme que les valeurs
extrêmes sont plus fréquentes qu'une loi normale ne le prédirait. **Aucune
valeur extrême ne sera supprimée.**

### 3.5 Écart interdécile important

Le rapport p99 / p1 est d'environ **10,4×**. Les 1 % les mieux payés gagnent
en moyenne plus de 10 fois ce que gagnent les 1 % les moins payés. Cela
justifie une analyse par sous-groupes à la phase 4.

### 3.6 Cœur du marché resserré

50 % des salaires se situent entre **105 800 USD** (Q1) et **198 000 USD** (Q3),
soit une fourchette de 92 200 USD. C'est une information utile pour
positionner les prédictions du futur modèle.

## 4. Décisions pour la suite du projet

| Décision | Justification |
|----------|---------------|
| Conserver toutes les lignes (aucune suppression d'outlier) | Valeurs extrêmes légitimes |
| Tester `log1p(salary_in_usd)` à l'étape 32 | Asymétrie 1,35 |
| Privilégier la médiane dans les analyses descriptives | Moyenne > médiane |
| Analyses par sous-groupes à la phase 4 | CV 47 %, écart interdécile 10,4× |
| Rapporter les métriques finales en USD | Interprétabilité métier |

## 5. Limites

- Les salaires ne sont pas ajustés à l'inflation entre 2020 et 2025.
- Le dataset est issu d'une curation multi-sources, avec 52,5 % de doublons
  exacts (légitimes, voir `data/raw/README.md`). Les statistiques décrivent
  cette population particulière, pas nécessairement le marché mondial réel.
- La sur-représentation des États-Unis et des années 2024-2025 (94 % des lignes)
  biaise les statistiques vers ce segment.