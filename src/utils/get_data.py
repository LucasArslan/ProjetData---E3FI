import os
import requests
import sys

DATA_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/full.csv.gz"
OUTPUT_DIR = os.path.join("data", "raw")
OUTPUT_FILENAME = "dvf_2023.csv.gz"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"Le fichier existe déjà : {dest_path}")
        return

    print(f"Démarrage du téléchargement depuis : {url}")
    print("Cela peut prendre quelques minutes")
    
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            total_length = response.headers.get('content-length')
            
            with open(dest_path, 'wb') as f:
                dl = 0
                for chunk in response.iter_content(chunk_size=8192): 
                    if chunk:
                        dl += len(chunk)
                        f.write(chunk)
                        mb_downloaded = dl / (1024 * 1024)
                        
                        if total_length:
                            total_mb = int(total_length) / (1024 * 1024)
                            percent = int(dl / int(total_length) * 100)
                            sys.stdout.write(f"\rTéléchargé : {mb_downloaded:.1f} Mo / {total_mb:.1f} Mo ({percent}%)")
                        else:
                            sys.stdout.write(f"\rTéléchargé : {mb_downloaded:.1f} Mo")
                        sys.stdout.flush()
                            
        print(f"\n[OK] Téléchargement terminé : {dest_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Erreur : {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    download_file(DATA_URL, OUTPUT_PATH)
