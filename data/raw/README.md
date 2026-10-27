# Dataset — Data Science Salaries

## Origine

- **Nom du fichier :** DataScience_salaries_2025.csv
- **Source :** Kaggle — miroir officiel du dataset ai-jobs.net Salaries
- **URL :** https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs
- **Source originale :** ai-jobs.net Salaries (https://ai-jobs.net/salaries/)
- **Licence :** CC0 1.0 (domaine public, aucune attribution requise)
- **Date de téléchargement :** À COMPLÉTER (date du jour)

## Licence

- **Licence déclarée :** CC0 1.0 (source originale ai-jobs.net)
- **Redistribution autorisée :** oui
- **Décision de versionnement du CSV sur GitHub :** le CSV reste exclu par `.gitignore` (taille + bonne pratique). L'URL et la licence sont documentées pour permettre la reproductibilité.

## Contenu vérifié localement

- **Encodage :** UTF-8
- **Nombre de lignes (en-tête inclus) :** 151 446
- **Nombre de lignes de données :** 151 445
- **Nombre de colonnes :** 11
- **Colonnes :** work_year, experience_level, employment_type, job_title, salary, salary_currency, salary_in_usd, employee_residence, remote_ratio, company_location, company_size
- **Valeurs manquantes :** 0 sur toutes les colonnes
- **Doublons complets :** 79 532 (52,5 %)
- **Combinaisons uniques de variables explicatives :** 5 639
- **Ligne la plus répétée :** 195 occurrences

## Nature des doublons — explicitation

Le dataset présente 52,5 % de doublons complets. Ce n'est PAS un artefact de génération synthétique :

1. **Source primaire réelle :** ai-jobs.net est une enquête salariale annuelle menée auprès de professionnels réels.
2. **Doublons légitimes d'enquête :** plusieurs répondants ayant le même profil (même poste, niveau, pays, taille d'entreprise, année) peuvent déclarer un salaire identique, notamment parce que les salaires sont souvent arrondis (90 000, 150 000, 160 000 USD).
3. **Documentation officielle :** ai-jobs.net documente cette caractéristique.

**Conséquences pour la modélisation (voir étape 11) :**
- Un split train/test aléatoire naïf provoquerait une fuite de données (même ligne dans train et test).
- Stratégie retenue : déduplication avant entraînement + split groupé sur les combinaisons de variables explicatives.

## Notes

- Le dataset précédemment utilisé (`saurabhbadole/latest-data-science-job-salaries-2024`) était un sous-ensemble de ce dataset ai-jobs.net (mêmes exemples de doublons, structure identique). Il a été abandonné pour travailler directement sur la source primaire.