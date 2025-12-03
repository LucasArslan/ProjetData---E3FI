import pandas as pd
import os
import zipfile
import json
from pathlib import Path

# Chemins de base : Le script est dans src/utils, la racine est deux niveaux au-dessus.
PROJECT_ROOT = Path(__file__).parent.parent.parent
RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
CLEANED_DATA_DIR = PROJECT_ROOT / 'data' / 'cleaned'

# 1. LOGIQUE DE DÉCOMPRESSION DES ZIP MANUELS
def extract_dvf_zips():
    """Décompresse les fichiers ZIP DVF manuellement placés dans data/raw."""
    
    # Assurez-vous que les dossiers de sortie existent
    if not RAW_DATA_DIR.exists():
        RAW_DATA_DIR.mkdir(parents=True)
    if not CLEANED_DATA_DIR.exists():
        CLEANED_DATA_DIR.mkdir(parents=True)

    print("--- Démarrage de la décompression des fichiers ZIP DVF (Module PANDAS) ---")
    
    # Parcourir les fichiers dans data/raw
    for item in os.listdir(RAW_DATA_DIR):
        if item.endswith('.zip'):
            zip_path = RAW_DATA_DIR / item
            
            # Créer le dossier d'extraction (par exemple, 'valeursfoncieres-2024')
            extract_folder_name = zip_path.stem 
            extract_dir = RAW_DATA_DIR / extract_folder_name
            
            # Si le dossier n'existe pas, on décompresse
            if not extract_dir.exists():
                print(f"[Décompression] Extraction de {item} vers {extract_dir.name}...")
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        # Extrait les CSV/TXT dans le dossier créé
                        zip_ref.extractall(extract_dir)
                    print(f"[Succès] {item} décompressé.")
                except Exception as e:
                    print(f"[ERREUR] Échec de la décompression de {item}: {e}")
            else:
                print(f"[Décompression] Dossier {extract_folder_name} déjà présent, skipping.")

# 2. LOGIQUE DE CHARGEMENT ET DE FUSION
def load_and_merge_data():
    """Charge et fusionne tous les fichiers CSV/TXT DVF décompressés."""
    all_data = []
    
    # Parcourir les sous-dossiers (les années décompressées) dans data/raw
    for folder_name in os.listdir(RAW_DATA_DIR):
        folder_path = RAW_DATA_DIR / folder_name
        
        # On ne traite que les dossiers créés par la décompression et non le dossier cleaned
        if folder_path.is_dir() and folder_name != 'cleaned':
            
            # Trouver le fichier CSV DVF (le seul qui nous intéresse dans le dossier)
            for file_name in os.listdir(folder_path):
                # Utiliser lower() pour être plus tolérant au format (csv ou txt)
                if file_name.lower().endswith('.csv') or file_name.lower().endswith('.txt'): 
                    file_path = folder_path / file_name
                    print(f"Chargement du fichier : {file_path.name}")
                    
                    # On essaie de lire le fichier
                    try:
                        # TENTATIVE 1 : Séparateur point-virgule (le plus courant pour DVF)
                        df = pd.read_csv(
                            file_path, 
                            sep=';', 
                            dtype={'Code service instructeur': str, 'Code postal': str, 'Code commune': str},
                            low_memory=False
                        )
                        # Vérification simple: si le nombre de colonnes est > 5, c'est probablement bon
                        if df.shape[1] > 5:
                             all_data.append(df)
                        else:
                             raise ValueError("Tentative avec ';' a donné un nombre insuffisant de colonnes.")

                    except Exception as e:
                        # TENTATIVE 2 : Séparateur virgule (si la première a échoué)
                        try:
                            df = pd.read_csv(
                                file_path, 
                                sep=',', 
                                dtype={'Code service instructeur': str, 'Code postal': str, 'Code commune': str},
                                low_memory=False
                            )
                            if df.shape[1] > 5:
                                 all_data.append(df)
                            else:
                                 raise ValueError("Tentative avec ',' a donné un nombre insuffisant de colonnes.")

                        except Exception as e2:
                             print(f"Erreur fatale lors du chargement de {file_path.name}. Problème de format ou de séparateur. Erreur: {e2}")

                        
    if not all_data:
        print("Aucun fichier de données CSV ou TXT n'a pu être chargé correctement dans les sous-dossiers de data/raw.")
        return None
        
    df_final = pd.concat(all_data, ignore_index=True)
    return df_final


# 3. LOGIQUE DE NETTOYAGE, CALCUL et AGRÉGATION
def clean_and_aggregate_data(df_raw, geojson_filename="communes-2024.geojson"):
    """Nettoie, calcule le prix au m² et agrège les données."""
    
    print("\n--- DEBUT DU NETTOYAGE ET CALCUL PANDAS ---")

    # 1. Sélection et Renommage des colonnes essentielles
    try:
        df_clean = df_raw[[
            'Date mutation', 
            'Valeur fonciere', 
            'Surface reelle bati', 
            'Code commune',
            'Type de local'
        ]].copy()
    except KeyError as e:
        print(f"[ERREUR COLONNE] Vérifiez les noms des colonnes dans votre CSV: {e}")
        # Une erreur ici indique que le fichier n'a pas été chargé correctement (mauvais séparateur)
        return None, None # Arrêt si colonnes introuvables

    df_clean.columns = ['date_mutation', 'prix_vente', 'surface_bati', 'code_commune', 'type_local']

    # 2. Nettoyage des valeurs manquantes et incohérentes
    df_clean = df_clean.dropna(subset=['prix_vente', 'surface_bati'])
    
    df_clean = df_clean[
        (df_clean['prix_vente'] > 1000) & 
        (df_clean['surface_bati'] > 5) &
        (df_clean['type_local'].isin(['Maison', 'Appartement']))
    ].copy() 

    # 3. Calcul de l'Indicateur Clé : Prix au m²
    df_clean['prix_m2'] = df_clean['prix_vente'] / df_clean['surface_bati']

    # 4. Préparation pour l'analyse temporelle et géospatiale
    df_clean['date_mutation'] = pd.to_datetime(df_clean['date_mutation'])
    df_clean['annee'] = df_clean['date_mutation'].dt.year
    df_clean['code_commune'] = df_clean['code_commune'].astype(str).str.zfill(5) # 5 chiffres pour la jointure

    print(f"DataFrame nettoyé et prêt à l'analyse. Nombre de lignes restantes : {len(df_clean)}")
    
    # 5. Agrégation pour la carte (prix moyen global par commune)
    df_aggregated_map = df_clean.groupby('code_commune').agg(
        prix_m2_moyen_global=('prix_m2', 'median'),
        nombre_ventes_global=('prix_vente', 'count')
    ).reset_index()

    print("Agrégation par Commune globale effectuée.")
    
    # 6. Chargement du GeoJSON (Module GÉOLOCALISATION)
    geojson_path = RAW_DATA_DIR / geojson_filename
    if not geojson_path.exists():
        print(f"[ERREUR GÉO] Fichier GeoJSON manquant : {geojson_filename} doit être dans data/raw.")
        return None, None

    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
        
    return df_aggregated_map, geojson_data


# 4. POINT D'ENTRÉE DU SCRIPT
if __name__ == '__main__':
    
    # Étape 1 : Décompression
    extract_dvf_zips() 
    
    # Étape 2 : Chargement
    df_raw = load_and_merge_data()
    
    if df_raw is not None and not df_raw.empty:
        
        # Étape 3 : Nettoyage et Agrégation
        df_aggregated, geojson_data = clean_and_aggregate_data(df_raw)
        
        if df_aggregated is not None:
            # Étape 4 : Sauvegarde du CSV nettoyé final
            df_aggregated.to_csv(CLEANED_DATA_DIR / 'cleaneddata.csv', index=False)
            print(f"\n[SUCCÈS] Données agrégées sauvegardées dans {CLEANED_DATA_DIR / 'cleaneddata.csv'}")

            # Étape 5 : Sauvegarde du GeoJSON (pour être chargé par le dashboard plus tard)
            # Normalement le GeoJSON reste dans RAW, mais on peut vérifier sa présence
            
    else:
        print("\n[ERREUR FATALE] Le chargement de données a échoué. Vérifiez les fichiers ZIP/CSV dans data/raw.")