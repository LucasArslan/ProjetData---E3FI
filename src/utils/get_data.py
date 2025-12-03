import requests
import zipfile
import os

# 1. Définir les liens corrects pour les années récentes (au format txt.zip)
# La DGFiP publie généralement les données annuellement. 
# Si vous avez besoin de données jusqu'à 2024, il faudra les fichiers les plus récents disponibles.

# Remplacer la boucle par une liste de paires (ANNEE, URL)
# Les URL ci-dessous sont les liens de téléchargement direct pour la plupart des années récentes.
# J'ai inclus 2024 et 2025 (pré-publiées) pour avoir 5 ans de données récentes.
DOWNLOAD_LINKS = {
    # Utilisez le lien "Copier le lien" directement sur data.gouv.fr
    2021: "https://www.data.gouv.fr/fr/datasets/r/d0ce598e-4a94-4b53-b0e6-69a474665a39", 
    2022: "https://www.data.gouv.fr/fr/datasets/r/f57c2936-e04c-47d3-9799-73e4882e9b0d", 
    2023: "https://www.data.gouv.fr/fr/datasets/r/d8544a4b-1498-4660-8488-84227c65c829", 
    2024: "https://www.data.gouv.fr/fr/datasets/r/cc303e3c-2f98-4228-98e9-d372f87a8913", 
    2025: "https://www.data.gouv.fr/fr/datasets/r/774052f5-b28e-4903-a442-70b86a87c10b", # Provisoire
}
# Ajoutez les années 2019 et 2020 si vous voulez une période complète de 5 ans glissants

BASE_DIR = 'data/raw' # Mettre à jour le chemin vers le dossier raw

# Créer le dossier 'data/raw' s'il n'existe pas
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

print("--- DEBUT DE L'ACQUISITION DES DONNÉES DVF ---")

for annee, url in DOWNLOAD_LINKS.items():
    local_zip_path = os.path.join(BASE_DIR, f"dvf_{annee}.zip")
    
    print(f"\n[Téléchargement] Année {annee} depuis {url}...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() 

        # ... (le reste du code de téléchargement est le même) ...
        with open(local_zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"[Succès] Fichier ZIP sauvegardé à {local_zip_path}")

        # Décompression
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            extract_dir = os.path.join(BASE_DIR, f"dvf_{annee}")
            zip_ref.extractall(extract_dir)
            print(f"[Décompression] Données extraites dans {extract_dir}")
            
    except requests.exceptions.RequestException as e:
        print(f"[ERREUR] Échec du téléchargement pour {annee}. Vérifiez l'URL : {e}")

print("\n--- ACQUISITION TERMINÉE ---")