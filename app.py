"""Application Streamlit — Data Science Salary Prediction.

Lancement :
    streamlit run app.py

L'application charge le pipeline entraîné (Gradient Boosting) et permet de
prédire un salaire annuel en USD à partir des caractéristiques d'un profil.

Gère les cas limites :
- modèle absent ou corrompu ;
- métadonnées absentes ;
- catégories inconnues (handle_unknown="ignore") ;
- prédiction hors plage d'entraînement (avertissement visuel) ;
- bouton de réinitialisation.
"""

import streamlit as st

# Configuration de la page (doit être le premier appel Streamlit)
st.set_page_config(
    page_title="Data Science Salary Prediction",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Imports du package (après set_page_config pour éviter les warnings Streamlit)
from salary_prediction.config import (
    FINAL_MODEL_PARAMS,
    REFERENCE_METRICS,
)
from salary_prediction.prediction import (
    PredictionError,
    load_metadata,
    load_pipeline,
    predict_salary,
)

# === Constantes locales ===
SALARY_MIN_TRAIN = 15_000
SALARY_MAX_TRAIN = 800_000


# --- Cache Streamlit ---

@st.cache_resource(show_spinner="Chargement du modèle...")
def get_pipeline():
    """Charge le pipeline une seule fois (mis en cache par Streamlit)."""
    return load_pipeline()


@st.cache_data(show_spinner="Chargement des métadonnées...")
def get_metadata():
    """Charge les métadonnées une seule fois (mises en cache)."""
    return load_metadata()


# --- En-tête ---

st.title("💰 Data Science Salary Prediction")
st.markdown(
    "Estimez le **salaire annuel en USD** d'un professionnel de la Data Science "
    "à partir de ses caractéristiques professionnelles."
)
st.markdown("---")


# --- Sidebar : à propos et performances ---

with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown(
        """
        **Modèle :** Gradient Boosting Regressor  
        **Données :** Data Science Salaries 2020-2025 (151 445 profils)  
        **Source :** [Kaggle — adilshamim8](https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs)
        """
    )

    st.markdown("---")
    st.subheader("📊 Performances du modèle")
    try:
        metadata = get_metadata()
        metrics = metadata["metriques"]
        st.metric("R² (test)", f"{metrics['R2_test']:.3f}")
        st.metric("MAE (test)", f"{metrics['MAE_test_usd']:,.0f} USD")
        st.metric("RMSE (test)", f"{metrics['RMSE_test_usd']:,.0f} USD")
    except Exception as e:
        st.warning(f"Métadonnées indisponibles : {e}")

    st.markdown("---")
    st.subheader("⚠️ Limites")
    st.caption(
        "Prédictions **indicatives**. Le modèle est entraîné sur des données "
        "majoritairement nord-américaines (93,7 %) et ne remplace pas une "
        "évaluation humaine. Les salaires extrêmes (> 500k USD) sont sous-estimés."
    )

    st.markdown("---")
    st.subheader("🧪 Tests de robustesse")
    with st.expander("Voir les cas limites gérés"):
        st.markdown(
            """
            **Catégorie inconnue** : le pipeline utilise
            `handle_unknown="ignore"` du `OneHotEncoder`. Une valeur inconnue
            est encodée à 0 pour toutes les modalités, sans planter.

            **Modèle absent** : si le fichier `salary_prediction_pipeline.joblib`
            est absent, l'application affiche une erreur claire et s'arrête.

            **Métadonnées absentes** : si `metadata.json` est absent, la sidebar
            affiche un avertissement, mais le formulaire reste fonctionnel.

            **Prédiction hors plage** : si le salaire prédit sort de
            [15 000, 800 000] USD, un avertissement visuel est affiché.
            """
        )

    st.markdown("---")
    st.subheader("🔗 Liens")
    st.markdown(
        "- [Code source (GitHub)](#)\n"
        "- [Documentation du projet](#)\n"
        "- [Dataset original](https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs)"
    )


# --- Chargement du pipeline ---

try:
    pipeline = get_pipeline()
    st.success("✅ Modèle chargé avec succès.")
except FileNotFoundError as e:
    st.error(
        f"❌ Modèle introuvable : {e}\n\n"
        f"Exécutez d'abord l'étape 44 (sauvegarde du pipeline)."
    )
    st.stop()
except PredictionError as e:
    st.error(f"❌ Erreur de chargement du modèle : {e}")
    st.stop()


# --- Formulaire de prédiction ---

st.subheader("🎯 Décrivez votre profil")
st.markdown("Renseignez les champs ci-dessous, puis cliquez sur **Prédire**.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        work_year = st.selectbox(
            "Année",
            options=[2020, 2021, 2022, 2023, 2024, 2025],
            index=5,  # 2025 par défaut
            help="Année de versement du salaire. 94 % des données sont en 2024-2025.",
        )
        experience_level = st.selectbox(
            "Niveau d'expérience",
            options=["EN", "MI", "SE", "EX"],
            index=2,  # SE par défaut (majoritaire dans le dataset)
            format_func=lambda x: {
                "EN": "EN — Junior (Entry-level)",
                "MI": "MI — Intermédiaire (Mid-level)",
                "SE": "SE — Senior",
                "EX": "EX — Executive (Direction)",
            }[x],
            help="Le niveau d'expérience est le facteur le plus discriminant du modèle.",
        )
        employment_type = st.selectbox(
            "Type d'emploi",
            options=["FT", "PT", "CT", "FL"],
            index=0,  # FT par défaut (99,5 % du dataset)
            format_func=lambda x: {
                "FT": "FT — Temps plein (Full-time)",
                "PT": "PT — Temps partiel (Part-time)",
                "CT": "CT — Contrat (Contract)",
                "FL": "FL — Freelance",
            }[x],
            help="99,5 % des profils du dataset sont en temps plein.",
        )
        job_category = st.selectbox(
            "Catégorie de métier",
            options=[
                "Data Scientist",
                "Data Analyst",
                "Data Engineer",
                "Software Engineer",
                "ML Engineer",
                "Manager",
                "Engineer",
                "Architect",
                "Researcher",
                "Other",
            ],
            index=0,
            help="Les intitulés bruts (422) sont regroupés en 10 catégories métier.",
        )

    with col2:
        remote_ratio = st.selectbox(
            "Télétravail (%)",
            options=[0, 50, 100],
            index=0,
            format_func=lambda x: {
                0: "0 % — Présentiel",
                50: "50 % — Hybride",
                100: "100 % — Full remote",
            }[x],
            help="Proportion de télétravail. 78 % des profils sont en présentiel.",
        )
        company_size = st.selectbox(
            "Taille de l'entreprise",
            options=["S", "M", "L"],
            index=1,  # M par défaut (96,8 % du dataset)
            format_func=lambda x: {
                "S": "S — Petite (< 50 employés)",
                "M": "M — Moyenne (50-250 employés)",
                "L": "L — Grande (> 250 employés)",
            }[x],
            help="96,8 % des profils sont dans des entreprises de taille moyenne.",
        )
        residence_continent = st.selectbox(
            "Continent de résidence",
            options=[
                "North America",
                "Europe",
                "Oceania",
                "Asia",
                "South America",
                "Africa",
                "Middle East",
            ],
            index=0,  # North America par défaut (93,7 % du dataset)
            help="93,7 % des profils sont en Amérique du Nord.",
        )
        company_continent = st.selectbox(
            "Continent de l'employeur",
            options=[
                "North America",
                "Europe",
                "Oceania",
                "Asia",
                "South America",
                "Africa",
                "Middle East",
            ],
            index=0,
            help="Généralement identique au continent de résidence (peu de remote transfrontalier).",
        )

    # Bouton de soumission (dans le formulaire)
    submitted = st.form_submit_button(
        "💡 Prédire le salaire",
        type="primary",
        use_container_width=True,
    )


# --- Logique de prédiction ---

if submitted:
    profile = {
        "work_year": work_year,
        "experience_level": experience_level,
        "employment_type": employment_type,
        "job_category": job_category,
        "remote_ratio": remote_ratio,
        "company_size": company_size,
        "residence_continent": residence_continent,
        "company_continent": company_continent,
    }

    try:
        salary = predict_salary(profile, pipeline=pipeline)

        st.markdown("---")
        st.subheader("📊 Résultat de la prédiction")

        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("Salaire annuel estimé", f"{salary:,.0f} USD")
        with col_res2:
            st.metric(
                "Fourchette indicative",
                f"± {REFERENCE_METRICS['MAE_test_usd']:,.0f} USD",
            )
        with col_res3:
            st.metric("R² du modèle", f"{REFERENCE_METRICS['R2_test']:.3f}")

        # Avertissement si prédiction hors plage d'entraînement
        if salary < SALARY_MIN_TRAIN or salary > SALARY_MAX_TRAIN:
            st.warning(
                f"⚠️ La prédiction ({salary:,.0f} USD) sort de la plage "
                f"d'entraînement ({SALARY_MIN_TRAIN:,} – {SALARY_MAX_TRAIN:,} USD). "
                f"Le modèle n'a pas appris sur des profils aussi extrêmes : "
                f"le résultat est peu fiable."
            )

        st.caption(
            f"Prédiction basée sur un modèle Gradient Boosting. "
            f"MAE test = {REFERENCE_METRICS['MAE_test_usd']:,.0f} USD — "
            f"en moyenne, le modèle se trompe de ce montant. "
            f"Les salaires extrêmes (> 500k USD) sont sous-estimés."
        )

        # Détail du profil soumis
        with st.expander("🔍 Détail du profil soumis"):
            st.json(profile)

    except PredictionError as e:
        st.error(f"❌ Erreur de prédiction : {e}")
        st.info(
            "💡 Vérifiez que tous les champs sont remplis avec des valeurs "
            "cohérentes. Si l'erreur persiste, contactez l'administrateur."
        )
    except Exception as e:
        st.error(f"❌ Erreur inattendue : {e}")
        st.info(
            "💡 Une erreur inattendue s'est produite. Réessayez ou rechargez "
            "la page. Si l'erreur persiste, signalez-la."
        )


# --- Bouton de réinitialisation (hors formulaire) ---

if st.button("🔄 Réinitialiser le formulaire", use_container_width=True):
    st.rerun()


# --- Pied de page ---

st.markdown("---")
st.caption(
    "Projet portfolio — Data Science Salary Analysis & Salary Prediction. "
    "Code source : [GitHub](#)."
)