# Plan de travail — Data Science Salary Analysis & Salary Prediction

## 1. Problématique

Quels sont les facteurs associés aux salaires des professionnels de la Data Science
et peut-on prédire leur salaire annuel à partir de leurs caractéristiques professionnelles ?

## 2. Objectifs

1. Explorer un dataset réel de salaires (Data Science Salaries 2024/2025).
2. Utiliser NumPy pour les calculs scientifiques.
3. Utiliser Pandas pour nettoyer et analyser les données.
4. Réaliser des visualisations avec Matplotlib et Seaborn.
5. Construire plusieurs modèles de régression avec Scikit-Learn.
6. Comparer les performances des modèles.
7. Optimiser le modèle retenu avec GridSearchCV.
8. Interpréter les résultats du point de vue métier.
9. Créer une application Streamlit de prédiction.
10. Tester, documenter et publier le projet sur GitHub.

## 3. Variable cible et variables explicatives envisagées

- **Variable cible :** `salary_in_usd` (salaire annuel en USD).
- **Variables explicatives candidates :** `work_year`, `experience_level`,
  `employment_type`, `job_title`, `employee_residence`, `remote_ratio`,
  `company_location`, `company_size`.
- **Variables exclues :** `salary` et `salary_currency` (risque de fuite de données
  car `salary_in_usd` en dérive directement).

## 4. Phases du projet

| Phase | Thème | Étapes |
|-------|-------|--------|
| 1 | Compréhension et environnement | 1 à 6 |
| 2 | Acquisition et compréhension des données | 7 à 11 |
| 3 | Analyse NumPy | 12 à 17 |
| 4 | Analyse Pandas | 18 à 24 |
| 5 | Visualisation | 25 à 31 |
| 6 | Machine Learning | 32 à 44 |
| 7 | Architecture de production | 45 à 49 |
| 8 | Application Streamlit | 50 à 55 |
| 9 | Tests et documentation | 56 à 61 |
| 10 | GitHub | 62 à 68 |

## 5. Règles de travail

- Une seule étape à la fois, validation obligatoire avant de passer à la suivante.
- Expliquer avant de coder.
- Ne jamais inventer de résultats, de scores ou de sorties.
- Prévenir strictement les fuites de données : tout prétraitement est ajusté
  uniquement sur le jeu d’entraînement.
- Les hyperparamètres sont sélectionnés sans utiliser le jeu de test.
- Le code respecte les bonnes pratiques Python (nommage, fonctions réutilisables,
  gestion des erreurs, chemins portables, séparation des responsabilités).

## 6. Critères de validation globaux

- Chaque notebook s’exécute sans erreur, de haut en bas.
- Les résultats rapportés sont ceux réellement observés.
- Les métriques des modèles sont comparées sur le même jeu de test.
- Le modèle final est sauvegardé et rechargeable.
- L’application Streamlit fonctionne avec le modèle sauvegardé.
- Les tests pytest passent.
- Le README permet à un tiers de cloner et exécuter le projet.
- Le dépôt GitHub est public et vérifié.

## 7. Environnement

- **OS :** Windows
- **Python :** 3.12.10
- **pip :** 25.0.1
- **IDE :** VS Code
- **Dossier projet :** `C:\Users\malak\Desktop\data-science-salary-analysis`
- **Dataset :** Kaggle — `saurabhbadole/latest-data-science-job-salaries-2024`
  (dérivé de ai-jobs.net Salaries, licence à vérifier au téléchargement)

## 8. Notes de suivi

- **2026-10-23 — Changement de dataset.** Le dataset initialement utilisé
  (`saurabhbadole/latest-data-science-job-salaries-2024`) s'est révélé être un
  sous-ensemble du dataset ai-jobs.net, avec 50 % de doublons exacts. Il a été
  remplacé par le dataset ai-jobs.net complet (151 445 lignes, CC0). Les doublons
  sont légitimes (enquête réelle) et seront gérés à l'étape 11 par déduplication
  et split groupé.