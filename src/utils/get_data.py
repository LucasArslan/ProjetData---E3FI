import os
import requests

DATA_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/full.csv.gz"
OUTPUT_DIR = os.path.join("data", "raw")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "dvf_2023.csv.gz")

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"Fichier existant : {dest_path}")
        return
    
    print(f"Téléchargement depuis : {url}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Téléchargement terminé : {dest_path}")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    download_file(DATA_URL, OUTPUT_PATH)
