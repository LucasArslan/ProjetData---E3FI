import pandas as pd
import os

RAW_PATH = os.path.join("data", "raw", "dvf_2023.csv.gz")
CSV_DETAIL_PATH = os.path.join("data", "cleaned", "data_detail.csv")
CHUNK_SIZE = 100000

def process():
    print("Démarrage du traitement France Entière")
    
    cols = ['date_mutation', 'nature_mutation', 'valeur_fonciere', 
            'code_departement', 'code_commune', 'nom_commune', 
            'type_local', 'surface_reelle_bati']
    
    chunks_kept = []
    reader = pd.read_csv(RAW_PATH, compression='gzip', usecols=cols, 
                         dtype={'code_commune': str, 'code_departement': str}, 
                         chunksize=CHUNK_SIZE)
    
    total_rows = 0
    for i, chunk in enumerate(reader):
        chunk = chunk[chunk['nature_mutation'] == "Vente"]
        chunk = chunk[chunk['type_local'].isin(['Maison', 'Appartement'])]
        chunk = chunk.dropna(subset=['valeur_fonciere', 'surface_reelle_bati', 'code_commune'])
        chunk = chunk[chunk['surface_reelle_bati'] > 9]
        chunk = chunk[chunk['valeur_fonciere'] > 1000]
        
        chunk['prix_m2'] = chunk['valeur_fonciere'] / chunk['surface_reelle_bati']
        chunk = chunk[(chunk['prix_m2'] > 500) & (chunk['prix_m2'] < 25000)]
        
        chunks_kept.append(chunk)
        total_rows += len(chunk)
        print(f"   Lot {i} ({total_rows} ventes)")
    
    df = pd.concat(chunks_kept)
    df['date_mutation'] = pd.to_datetime(df['date_mutation'])
    df['mois'] = df['date_mutation'].dt.to_period('M').astype(str)
    
    os.makedirs(os.path.dirname(CSV_DETAIL_PATH), exist_ok=True)
    df.to_csv(CSV_DETAIL_PATH, index=False)
    print(f"{CSV_DETAIL_PATH} généré.")

if __name__ == "__main__":
    process()
