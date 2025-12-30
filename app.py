import streamlit as st
from pages import scraping, download, dashboard, evaluation

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Coinafrique Scraper",
    page_icon="CA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Définir les pages avec st.Page
scraping_page = st.Page(
    scraping.show,
    title="Scrape data using BeautifulSoup",
    icon=":material/search:",
    url_path="scraping",
    default=True
)

download_page = st.Page(
    download.show,
    title="Download scraped data",
    icon=":material/download:",
    url_path="download"
)

dashboard_page = st.Page(
    dashboard.show,
    title="Dashboard of the data",
    icon=":material/bar_chart:",
    url_path="dashboard"
)

evaluation_page = st.Page(
    evaluation.show,
    title="Evaluate the App",
    icon=":material/edit_document:",
    url_path="evaluation"
)

# Navigation
pg = st.navigation([scraping_page, download_page, dashboard_page, evaluation_page])

# Exécuter la page sélectionnée
pg.run()


