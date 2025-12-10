import pandas as pd
import os

RAW_PATH = os.path.join("data", "raw", "dvf_2023.csv.gz")
CSV_DETAIL_PATH = os.path.join("data", "cleaned", "data_detail.csv")

def process():
    print("Démarrage du traitement")
    
    cols = ['date_mutation', 'nature_mutation', 'valeur_fonciere', 
            'code_departement', 'code_commune', 'nom_commune', 
            'type_local', 'surface_reelle_bati']
    
    df = pd.read_csv(RAW_PATH, compression='gzip', usecols=cols)
    
    # Filtres de base
    df = df[df['nature_mutation'] == "Vente"]
    df = df[df['type_local'].isin(['Maison', 'Appartement'])]
    df = df.dropna(subset=['valeur_fonciere', 'surface_reelle_bati'])
    
    print(f"Données filtrées : {len(df)} lignes")
    os.makedirs(os.path.dirname(CSV_DETAIL_PATH), exist_ok=True)
    df.to_csv(CSV_DETAIL_PATH, index=False)
    print("Terminé")

if __name__ == "__main__":
    process()
