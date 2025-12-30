import streamlit as st
from scraper import CATEGORY_URLS, scrape_category


def show():
    """Affiche la page de scraping"""

    st.title("Scrape data using BeautifulSoup")
    st.markdown("""
    Cette page permet de scraper des données en direct depuis **Coinafrique.com** en utilisant BeautifulSoup.
    Sélectionnez une catégorie d'animaux et le nombre de pages à scraper.
    """)

    st.divider()

    # Créer trois colonnes pour les inputs
    col1, col2, col3 = st.columns([2, 1, 1], vertical_alignment="bottom")

    with col1:
        # Sélection de catégorie
        category = st.selectbox(
            "Choisir une catégorie",
            options=list(CATEGORY_URLS.keys()),
            help="Sélectionnez la catégorie d'animaux à scraper",
        )

    with col2:
        # Nombre de pages
        num_pages = st.selectbox(
            "Nombre de pages",
            options=list(range(1, 51)),
            index=1,
            help="Nombre de pages à scraper (1-50)",
        )
    with col3:
        # Bouton de scraping
        scrape_button = st.button(
            "Lancer le Scraping", type="primary", width="stretch"
        )

    st.divider()

    # Logique de scraping
    if scrape_button:
        # Créer des placeholders pour le feedback visuel
        progress_bar = st.progress(0, text="Initialisation...")
        status_container = st.empty()

        try:
            # Fonction callback pour mettre à jour la progression
            def update_progress(current_page, total_pages):
                progress = current_page / total_pages
                progress_bar.progress(
                    progress, text=f"Scraping page {current_page}/{total_pages}..."
                )

            # Message de démarrage
            status_container.info("Scraping en cours... Veuillez patienter.")

            # Appeler la fonction de scraping
            df = scrape_category(
                category=category,
                num_pages=num_pages,
                progress_callback=update_progress,
            )

            # Vider la barre de progression
            progress_bar.empty()
            status_container.empty()

            # Vérifier si des données ont été récupérées
            if df.empty:
                st.error(
                    "Aucune annonce trouvée. Vérifiez votre connexion internet ou réessayez plus tard."
                )
            else:
                # Message de succès
                st.success(
                    f"Scraping terminé avec succès! **{len(df)} annonces** récupérées"
                )

                # Prévisualisation des données
                st.subheader("Aperçu des données scrapées")
                st.dataframe(df.head(10), width="stretch", hide_index=True)

        except Exception as e:
            # Gestion des erreurs
            progress_bar.empty()
            status_container.empty()
            st.error(f"Erreur lors du scraping: {str(e)}")
            st.info(
                "**Suggestions:**\n- Vérifiez votre connexion internet\n- Réessayez avec moins de pages\n- Le site Coinafrique pourrait être temporairement indisponible"
            )
