import streamlit as st


def show():
    """Affiche la page d'évaluation"""

    st.title("Give Your Feedback")
    st.markdown("""
    Votre avis est important pour nous! Merci de prendre quelques minutes pour évaluer
    cette application en remplissant l'un des formulaires ci-dessous.
    """)

    # Ajouter un espace vertical
    st.write("" * 4)

    # Créer deux colonnes pour les boutons
    col1, col2 = st.columns(2, gap='medium')

    with col1:
        # Bouton KoBoToolbox
        kobo_url = "https://ee.kobotoolbox.org/x/UE2lZveP"
        st.link_button(
            label="Ouvrir le formulaire KoBoToolbox",
            url=kobo_url,
            type="primary",
            width='stretch',
        )

    with col2:
        # Bouton Google Forms
        google_url = "https://docs.google.com/forms/d/e/1FAIpQLSdQzeUTCppKooo7bIBB6dTdZbhDZDRdMl-p0UAilDlIj3opvA/formResponse"
        st.link_button(
            label="Ouvrir le formulaire Google Forms",
            url=google_url,
            type="primary",
            width='stretch',
        )


   
  
