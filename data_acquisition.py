import requests
import zipfile
import io
import os

# Liste des années à télécharger (ajustez selon les fichiers disponibles)
ANNEES_A_TELECHARGER = [2020, 2021, 2022, 2023, 2024]
BASE_URL = "https://www.data.gouv.fr/fr/datasets/r/d4e9c71a-2975-47e0-af96-a07727c975a5" # URL pour un exemple d'année (2024), à adapter pour les autres années

# Créer un dossier 'data' pour stocker les fichiers bruts
if not os.path.exists("data"):
    os.makedirs("data")

print("--- DEBUT DE L'ACQUISITION DES DONNÉES DVF ---")

for annee in ANNEES_A_TELECHARGER:
    # ATTENTION : L'URL ci-dessous est un EXEMPLE.
    # Vous DEVEZ trouver l'URL exacte pour chaque année sur data.gouv.fr
    # L'URL officielle est souvent : https://files.data.gouv.fr/dvf/DVF_annees/XXXX.zip
    # Une recherche sur le portail vous donnera les liens réels et mis à jour.

    url = f"https://files.data.gouv.fr/dvf/DVF_{annee}/full.zip"
    local_zip_path = f"data/dvf_{annee}.zip"

    print(f"\n[Téléchargement] Année {annee} depuis {url}...")

    try:
        # Télécharger le contenu du fichier ZIP
        response = requests.get(url, stream=True)
        response.raise_for_status() # Lève une exception si le code HTTP est une erreur (4xx ou 5xx)

        # Écrire le contenu binaire dans le fichier local
        with open(local_zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[Succès] Fichier ZIP sauvegardé à {local_zip_path}")

        # Décompresser le fichier ZIP
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            # Extraire dans un sous-dossier (ex: data/dvf_2024/)
            extract_dir = f"data/dvf_{annee}"
            zip_ref.extractall(extract_dir)
            print(f"[Décompression] Données extraites dans {extract_dir}")

    except requests.exceptions.RequestException as e:
        print(f"[ERREUR] Échec du téléchargement pour {annee}. Vérifiez l'URL : {e}")

print("\n--- ACQUISITION TERMINÉE ---")

# Enregistrez vos modifications Git
# git add data_acquisition.py
# git commit -m "Ajout du script d'acquisition des donnees DVF"
# git push origin main