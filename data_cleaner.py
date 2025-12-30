import os
import re

import pandas as pd
import streamlit as st


def clean_price(price_str):
    """
    Nettoie et convertit les prix en valeur numérique.

    Args:
        price_str: String contenant le prix (ex: "250 000 CFA", "Prix sur demande")

    Returns:
        float: Prix numérique ou None si prix non disponible
    """
    if pd.isna(price_str):
        return None

    price_str = str(price_str).strip()

    # Vérifier si c'est "Prix sur demande"
    if "demande" in price_str.lower() or "négociable" in price_str.lower():
        return None

    # Extraire les chiffres
    numbers = re.findall(r'\d+', price_str)
    if numbers:
        # Joindre les nombres (ex: "250 000" -> "250000")
        price_num = int(''.join(numbers))
        return float(price_num)

    return None



def extract_image_url(image_style_str):
    """
    Extrait l'URL de l'image depuis le style CSS.

    Args:
        image_style_str: String contenant le style CSS (ex: 'background-image: url("https://...")')

    Returns:
        str: URL de l'image
    """
    if pd.isna(image_style_str):
        return None

    # Extraire l'URL entre les guillemets
    match = re.search(r'url\("(.+?)"\)', str(image_style_str))
    if match:
        return match.group(1)

    return None


def determine_category(filename):
    """
    Détermine la catégorie depuis le nom du fichier.

    Args:
        filename: Nom du fichier (ex: "coinafrique_chiens_webscraper.csv")

    Returns:
        str: Nom de la catégorie
    """
    filename_lower = filename.lower()

    if "chien" in filename_lower:
        return "Chiens"
    elif "mouton" in filename_lower:
        return "Moutons"
    elif "poule" in filename_lower:
        return "Poules, Lapins et Pigeons"
    elif "autre" in filename_lower:
        return "Autres"
    else:
        return "Non catégorisé"


def clean_dataframe(df):
    """
    Nettoie un DataFrame complet.

    Args:
        df: DataFrame à nettoyer

    Returns:
        DataFrame: DataFrame nettoyé
    """
    df_clean = df.copy()

    # Supprimer les colonnes techniques et inutiles
    columns_to_drop = [
        'web_scraper_order',
        'web_scraper_start_url',
        'container_urls',
        'image_lien',
    ]
    df_clean = df_clean.drop(columns=[col for col in columns_to_drop if col in df_clean.columns])

    return df_clean

@st.cache_data
def load_and_clean_all_data(data_folder="webscraper_data"):
    """
    Charge et nettoie tous les fichiers CSV du dossier.

    Args:
        data_folder: Chemin du dossier contenant les CSV

    Returns:
        DataFrame: DataFrame combiné et nettoyé
    """
    if not os.path.exists(data_folder):
        return pd.DataFrame()

    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

    if not csv_files:
        return pd.DataFrame()

    all_dfs = []

    for filename in csv_files:
        file_path = os.path.join(data_folder, filename)
        try:
            df = pd.read_csv(file_path)
            df_clean = clean_dataframe(df)

            # Ajouter la colonne catégorie basée sur le nom du fichier
            df_clean["categorie"] = determine_category(filename)

            all_dfs.append(df_clean)
        except Exception as e:
            print(f"Erreur lors du chargement de {filename}: {e}")
            continue

    if all_dfs:
        # Combiner tous les DataFrames
        combined_df = pd.concat(all_dfs, ignore_index=True)

        # Supprimer les doublons potentiels
        if 'Nom' in combined_df.columns and 'adresse' in combined_df.columns:
            combined_df = combined_df.drop_duplicates(
                subset=['Nom', 'prix', 'adresse'],
                keep='first'
            )

        return combined_df

    return pd.DataFrame()


