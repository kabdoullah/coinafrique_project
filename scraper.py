import time
from typing import Callable

import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get

# URLs des catégories à scraper
CATEGORY_URLS = {
    "Chiens": "https://sn.coinafrique.com/categorie/chiens",
    "Moutons": "https://sn.coinafrique.com/categorie/moutons",
    "Poules, Lapins et Pigeons": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
    "Autres": "https://sn.coinafrique.com/categorie/autres-animaux",
}


def scrape_category(
    category: str, num_pages: int, progress_callback: Callable | None = None
) -> pd.DataFrame:
    """
    Scrape les annonces d'une catégorie sur plusieurs pages

    Args:
        category: Nom de la catégorie ('Chiens', 'Moutons', 'Poules', 'Autres')
        num_pages: Nombre de pages à scraper
        progress_callback: Fonction optionnelle pour afficher la progression

    Returns:
        DataFrame pandas avec les annonces scrapées
    """

    if category not in CATEGORY_URLS:
        raise ValueError(
            f"Catégorie invalide. Choisir parmi: {list(CATEGORY_URLS.keys())}")

    base_url = CATEGORY_URLS[category]
    df = pd.DataFrame()

    print(f"\nScraping de la catégorie: {category}")
    print(f"Nombre de pages: {num_pages}\n")

    for index_page in range(1, num_pages + 1):
        # Construire l'URL de la page
        url = f"{base_url}?page={index_page}"

        print(f"Page {index_page}/{num_pages}: {url}")

        try:
            # Faire la requête HTTP
            res = get(url)
            res.raise_for_status()

            # Parser le HTML
            soup = bs(res.content, "html.parser")

            # Trouver tous les containers d'annonces
            containers = soup.find_all("div", "col s6 m4 l3")

            # Collecter les données de cette page
            data = []
            for container in containers:
                try:
                    # Récupérer l'URL de l'annonce
                    href = container.find("a")["href"]

                    # Construire l'URL complète
                    if href.startswith("http"):
                        url_container = href
                    elif href.startswith("/"):
                        url_container = "https://sn.coinafrique.com" + href
                    else:
                        url_container = base_url + "/" + href

                    print("URL de l'annonce:", url_container)

                    # Faire une requête pour la page de l'annonce avec retry
                    max_retries = 3
                    retry_count = 0
                    soup_container = None

                    while retry_count < max_retries:
                        try:
                            res_container = get(url_container, timeout=10)
                            res_container.raise_for_status()
                            soup_container = bs(res_container.content, "html.parser")
                            break
                        except Exception as e:
                            retry_count += 1
                            if retry_count < max_retries:
                                print(
                                    f"  Erreur ({e}), tentative {retry_count + 1}/{max_retries}..."
                                )
                                time.sleep(1)
                            else:
                                print(
                                    f"  Échec après {max_retries} tentatives, annonce ignorée"
                                )
                                raise

                    if soup_container is None:
                        continue

                    # Extraire les informations
                    import re

                    # Titre - chercher n'importe quel h1
                    title_elem = soup_container.find("h1")
                    title = title_elem.text.strip() if title_elem else "N/A"


                    # Prix - chercher le p avec class="price"
                    price = "N/A"
                    price_elem = soup_container.find("p", class_="price")
                    if price_elem:
                        price = (
                            price_elem.get_text(strip=True).replace("CFA", "").strip()
                        )

                    # Adresse - chercher le span avec l'attribut data-address
                    address = "N/A"
                    address_span = soup_container.find("span", {"data-address": True})
                    if address_span:
                        address = address_span.get("data-address")

                    # Image - extraire depuis le slider swiper
                    image_url = "N/A"
                    swiper_slide = soup_container.find("div", class_="swiper-slide")
                    if swiper_slide and swiper_slide.get("style"):
                        style = swiper_slide.get("style")
                        # Extraire l'URL de l'image depuis le style background-image
                        match = re.search(r'url\(["\']?([^"\']+)["\']?\)', style)
                        if match:
                            image_url = match.group(1)

                    print(
                        f"Titre: {title}, Prix: {price}, Adresse: {address}, Image: {image_url[:50] if image_url != 'N/A' else 'N/A'}"
                    )

                    dic = {
                        "Nom": title,
                        "prix": price,
                        "adresse": address,
                        "image_lien": image_url,
                    }
                    data.append(dic)

                except Exception as e:
                    print(f"Erreur sur une annonce: {str(e)}")
                    pass

            # Créer un DataFrame pour cette page
            DF = pd.DataFrame(data)

            # Concaténer avec le DataFrame principal
            df = pd.concat([df, DF], axis=0).reset_index(drop=True)

            # Mettre à jour la progression
            if progress_callback:
                progress_callback(index_page, num_pages)

            # Pause entre les pages (être poli avec le serveur)
            if index_page < num_pages:
                time.sleep(0.7)

        except Exception as e:
            print(f"Erreur sur la page {index_page}: {str(e)}")
            continue

    print(f"\nScraping terminé! {len(df)} annonces récupérées au total\n")
    return df
