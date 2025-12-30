import re

import pandas as pd
import streamlit as st

from data_cleaner import load_and_clean_all_data


def show():
    """Affiche la page du dashboard"""

    st.title("Dashboard of the data")
    st.markdown("""
    Visualisations et analyses des données scrapées depuis **Coinafrique.com**
    """)

    st.divider()

    # Charger et nettoyer les données
    with st.spinner("Chargement et nettoyage des données..."):
        df = load_and_clean_all_data()

    # Vérifier si des données sont disponibles
    if df.empty:
        st.warning("Aucune donnée disponible pour le dashboard.")
        st.info(
            "Veuillez d'abord ajouter des fichiers CSV dans le dossier **webscraper_data**."
        )
        return


    # Filtres
    st.markdown("### Filtres")

    # Ajouter une colonne catégorie basée sur les fichiers
    if "categorie" not in df.columns:
        df["categorie"] = "Toutes"

    # Sélecteur de catégorie
    categories_disponibles = ["Toutes"] + df["categorie"].unique().tolist()
    categorie_selectionnee = st.selectbox(
        "Sélectionner une catégorie",
        options=categories_disponibles,
        index=0
    )

    # Filtrer le DataFrame
    if categorie_selectionnee != "Toutes":
        df_filtered = df[df["categorie"] == categorie_selectionnee]
    else:
        df_filtered = df


    # Graphiques basés sur le DataFrame
    if not df_filtered.empty and "Nom" in df_filtered.columns and "prix" in df_filtered.columns and "adresse" in df_filtered.columns:

        # Première ligne - 2 colonnes
        col1, col2 = st.columns(2)

        with col1:
            # Graphique 1: Nombre d'annonces par catégorie - Bar Chart
            st.markdown("#### Nombre d'annonces par catégorie")
            if "categorie" in df_filtered.columns:
                cat_counts = df_filtered["categorie"].value_counts().reset_index()
                cat_counts.columns = ["Catégorie", "Nombre"]
                st.bar_chart(cat_counts, x="Catégorie", y="Nombre", color="#1f77b4")
            else:
                st.info("Aucune donnée de catégorie disponible")

        with col2:
            # Graphique 2: Nombre d'annonces par ville (top 10) - Line Chart
            st.markdown("#### Nombre d'annonces par ville (Line Chart)")
            ville_counts = df_filtered["adresse"].value_counts().head(10).reset_index()
            ville_counts.columns = ["Ville", "Nombre"]
            st.line_chart(ville_counts, x="Ville", y="Nombre", color="#ff7f0e")

        st.divider()

        # Deuxième ligne - 2 colonnes
        col3, col4 = st.columns(2)

        with col3:
            # Graphique 3: Évolution cumulative - Area Chart
            st.markdown("#### Distribution cumulative des annonces")
            cumul_data = df_filtered.reset_index()
            cumul_data["Index"] = range(1, len(cumul_data) + 1)
            cumul_data["Cumul"] = cumul_data["Index"]
            st.area_chart(cumul_data.head(100), x="Index", y="Cumul", color="#2ca02c")

        with col4:
            # Graphique 4: Distribution des prix - Scatter Chart
            st.markdown("#### Distribution des prix")
            if "prix" in df_filtered.columns:
                # Nettoyer les prix
                def clean_price_value(price_str):
                    if pd.isna(price_str):
                        return None
                    numbers = re.findall(r'\d+', str(price_str))
                    if numbers:
                        return float(''.join(numbers))
                    return None

                scatter_data = df_filtered.copy()
                scatter_data["prix_numeric"] = scatter_data["prix"].apply(clean_price_value)
                scatter_data = scatter_data[scatter_data["prix_numeric"].notna()].head(100)

                if not scatter_data.empty:
                    scatter_data["Index"] = range(1, len(scatter_data) + 1)
                    st.scatter_chart(scatter_data, x="Index", y="prix_numeric", color="#d62728")
                else:
                    st.info("Aucune donnée de prix disponible")
            else:
                st.info("Aucune donnée de prix disponible")
