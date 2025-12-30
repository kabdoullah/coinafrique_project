import os

import streamlit as st
import pandas as pd


def show():
    """Affiche la page de téléchargement des données Web Scraper"""

    st.title("Download Web Scraper Data")
    st.markdown("""
    Cette page permet de consulter et télécharger les données scrapées avec **Web Scraper**
    depuis Coinafrique.com.
    """)

    st.divider()

    # Dossier contenant les données
    data_folder = "webscraper_data"

    # Vérifier si le dossier existe
    if not os.path.exists(data_folder):
        st.error(f"Le dossier '{data_folder}' n'existe pas.")
        return

    # Lister tous les fichiers CSV dans le dossier
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

    if not csv_files:
        st.warning("Aucun fichier CSV trouvé dans le dossier webscraper_data.")
        st.info("Veuillez d'abord scraper des données avec Web Scraper.")
        return


    # Initialiser la session state pour stocker le fichier sélectionné
    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None

    # Fonction pour obtenir un nom lisible depuis le nom de fichier
    def get_display_name(filename):
        """Convertit le nom de fichier en nom d'affichage lisible"""
        filename_lower = filename.lower()
        if "chien" in filename_lower:
            return "Données des Chiens"
        elif "mouton" in filename_lower:
            return "Données des Moutons"
        elif "poule" in filename_lower or "volaille" in filename_lower:
            return "Données des Poules"
        elif "autre" in filename_lower:
            return "Autres Animaux"
        else:
            return f"{filename}"

    # Afficher les boutons pour chaque fichier
    st.subheader("Choisir une catégorie de données")

    # Créer une ligne de boutons (nombre de colonnes = nombre de fichiers)
    cols = st.columns(len(csv_files))

    for idx, filename in enumerate(csv_files):
        with cols[idx]:
            # Obtenir le nom d'affichage
            display_name = get_display_name(filename)

            # Déterminer le type de bouton (primary si sélectionné)
            button_type = (
                "primary"
                if st.session_state.selected_file == filename
                else "secondary"
            )

            # Créer le bouton
            if st.button(
                display_name,
                key=f"btn_{filename}",
                type=button_type,
                width="stretch",
            ):
                st.session_state.selected_file = filename
                st.rerun()

    st.divider()

    # Afficher les données du fichier sélectionné
    if st.session_state.selected_file:
        selected_file = st.session_state.selected_file
        file_path = os.path.join(data_folder, selected_file)

        # Charger et afficher les données
        try:
            df = pd.read_csv(file_path)

            # Afficher les statistiques
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Nombre de lignes", len(df))

            with col2:
                st.metric("Nombre de colonnes", len(df.columns))

            st.divider()

            # Prévisualisation des données
            st.subheader("Aperçu des données")

            # Options d'affichage
            col1, col2 = st.columns([1, 3])
            with col1:
                num_rows = st.number_input(
                    "Nombre de lignes à afficher",
                    min_value=5,
                    max_value=len(df),
                    value=min(10, len(df)),
                    step=5,
                )

            # Afficher les données
            st.dataframe(
                df.head(num_rows), width="stretch", hide_index=False
            )


        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier: {str(e)}")
            st.info("Assurez-vous que le fichier est un CSV valide.")

    else:
        st.info("Cliquez sur un bouton ci-dessus pour visualiser ces données")
