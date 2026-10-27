---
title: "Data Science Salary Analysis & Salary Prediction"
author: "Malak — Portfolio Data Science"
date: "2026-10-27"
---

# 💰 Data Science Salary Analysis & Salary Prediction

**Projet portfolio Data Science / Machine Learning**

Malak — 2026

---

## 📌 Problématique

**Quels sont les facteurs associés aux salaires des professionnels de la Data Science, et peut-on prédire leur salaire annuel à partir de leurs caractéristiques professionnelles ?**

---

## 📊 Données

- **Source :** Kaggle — Data Science Salaries 2020-2025
- **Taille :** 151 445 profils, 11 colonnes
- **Période :** 2020–2025 (94 % en 2024–2025)
- **Licence :** CC0 1.0 (domaine public)
- **0 valeur manquante, 52,5 % de doublons exacts** (enquête multi-sources)

---

## 🔬 Méthodologie

1. **Analyse exploratoire** — NumPy, Pandas, Matplotlib, Seaborn
2. **Feature engineering** — `job_category` (422 → 10 métiers), continents (104 → 7)
3. **Modélisation** — 4 modèles comparés, split stratifié groupé
4. **Mise en production** — package Python + application Streamlit

---

## 🎯 Résultats

| Modèle | MAE test | RMSE test | R² test |
|--------|----------|-----------|---------|
| Baseline (médiane) | 54 207 USD | 73 873 USD | −0,037 |
| Régression Linéaire | 48 325 USD | 65 065 USD | 0,196 |
| Random Forest | 47 796 USD | 65 917 USD | 0,174 |
| **Gradient Boosting** ⭐ | **47 964 USD** | **64 788 USD** | **0,203** |

**Gradient Boosting retenu** — meilleur R² test, meilleure RMSE.

---

## 🔑 Facteurs les plus discriminants

1. **`job_category`** — 46 % de l'importance
2. **`experience_level`** — 27 %
3. **`residence_continent`** — 24 %

**Le métier, l'expérience et la localisation** expliquent l'essentiel des salaires.

---

## 📈 Limites

- **R² = 0,20** — le modèle n'explique que 20 % de la variance
- **Biais géographique** — 93,7 % des données nord-américaines
- **Extrêmes** — salaires > 500k USD sous-estimés
- **Sous-groupes rares** — Amérique du Sud, Afrique, Researcher
- **Pas de causalité** — associations, pas de relations causales

---

## 💻 Application Streamlit

**Formulaire interactif** — 8 champs, prédiction en USD.

**Cas limites gérés :**
- modèle absent → message clair
- catégorie inconnue → `handle_unknown="ignore"`
- prédiction hors plage → avertissement visuel

**Lancement :** `streamlit run app.py`

---

## 🛠️ Technologies

- **Python 3.12** — langage
- **NumPy / Pandas** — calcul et manipulation
- **Scikit-Learn** — modélisation
- **Matplotlib / Seaborn** — visualisation
- **Streamlit** — application web
- **pytest** — 40 tests automatisés
- **Git / GitHub** — versioning

---

## 🎓 Ce que ce projet démontre

- **Pipeline complet** — de l'exploration à la production
- **Rigueur méthodologique** — split groupé, anti-fuite, baseline
- **Feature engineering** — réduction de cardinalité, regroupement métier
- **Bonnes pratiques** — package Python, tests, documentation
- **Transparence** — limites documentées, pas de sur-promesse

---

## 🔗 Liens

- **GitHub :** https://github.com/Malaak50/data-science-salary-analysis
- **Application :** `streamlit run app.py`
- **Documentation :** `README.md`, `docs/`, `reports/`

**Merci !**