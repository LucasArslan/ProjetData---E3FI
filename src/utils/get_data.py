"""
get_data.py
--------------------
Script destiné à récupérer automatiquement les fichiers DVF (Demandes de
Valeurs Foncières) depuis data.gouv.fr et à les stocker dans le répertoire
data/raw du projet.
"""

import os
import requests
import zipfile

DOWNLOAD_LINKS = {
    2021: "https://www.data.gouv.fr/api/1/datasets/r/e117fe7d-f7fb-4c52-8089-231e755d19d3",
    2022: "https://www.data.gouv.fr/api/1/datasets/r/8c8abe23-2a82-4b95-8174-1c1e0734c921",
    2023: "https://www.data.gouv.fr/api/1/datasets/r/cc8a50e4-c8d1-4ac2-8de2-c1e4b3c44c86",
    2024: "https://www.data.gouv.fr/api/1/datasets/r/af812b0e-a898-4226-8cc8-5a570b257326",
    2025: "https://www.data.gouv.fr/api/1/datasets/r/4d741143-8331-4b59-95c2-3b24a7bdbe3c"
}

RAW_DIR = "D:/data/raw"

if not os.path.exists(RAW_DIR):
    os.makedirs(RAW_DIR)

def download_dvf_data():
    """
    Télécharge et décompresse les fichiers DVF définis dans DOWNLOAD_LINKS.
    Chaque fichier ZIP est extrait dans un sous-dossier data/raw/dvf_YYYY.
    """

    print("\n--- DEBUT DE L'ACQUISITION DES DONNÉES DVF ---")

    for year, url in DOWNLOAD_LINKS.items():

        zip_path = os.path.join(RAW_DIR, f"dvf_{year}.zip")
        extract_path = os.path.join(RAW_DIR, f"dvf_{year}")

        print(f"\n[Téléchargement] Année {year} depuis : {url}")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(zip_path, "wb") as f:
                for block in response.iter_content(chunk_size=8192):
                    f.write(block)

            print(f"[Succès] Archive téléchargée : {zip_path}")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)

            print(f"[Décompression] Données extraites dans : {extract_path}")

        except requests.exceptions.RequestException as e:
            print(f"[ERREUR] Impossible de télécharger les données {year} : {e}")

        except zipfile.BadZipFile:
            print(f"[ERREUR] Le fichier {zip_path} est corrompu ou non valide.")

    print("\n--- ACQUISITION TERMINÉE ---\n")


if __name__ == "__main__":
    download_dvf_data()
