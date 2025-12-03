# Fonctions utilitaires communes
import pandas as pd
from pathlib import Path

def load_data(filepath):
    """Charge les données depuis un fichier CSV"""
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Fichier non trouvé: {filepath}")
        return None

def save_data(df, filepath):
    """Sauvegarde les données dans un fichier CSV"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Données sauvegardées dans: {filepath}")
