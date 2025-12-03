import pandas as pd
import plotly.express as px
import json
import os
from src.utils.clean_data import clean_and_merge_geodata # Assumons que cette fonction renvoie les données

def create_choropleth_map():
    """Crée la carte choroplèthe interactive du prix au m² par commune."""
    
    # 1. Charger les données propres et le GeoJSON
    # NOTE: Si vous exécutez le nettoyage avant, vous pouvez charger directement les fichiers CSV/JSON.
    df_prix = pd.read_csv('data/cleaned/cleaneddata.csv')
    
    # Remplacer 'votre_fichier_contours.geojson' par le nom réel de votre fichier GeoJSON
    geojson_path = os.path.join('data', 'raw', 'votre_fichier_contours.geojson')
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
        
    # 2. S'assurer que les codes sont des chaînes de caractères (clés de jointure)
    df_prix['code_commune'] = df_prix['code_commune'].astype(str).str.zfill(5)


    # 3. Créer la carte avec Plotly Express
    # C'est ici que Plotly effectue la jointure entre le GeoJSON et le DataFrame (Module Plotly)
    fig = px.choropleth_mapbox(df_prix, 
                               geojson=geojson_data, 
                               locations='code_commune',  # Colonne contenant les codes communes (INSEE)
                               featureidkey="properties.code", # Clé du GeoJSON à joindre (vérifiez si c'est 'code' ou 'insee' dans votre fichier GeoJSON)
                               color='prix_m2_moyen_global', # Colonne des prix à visualiser
                               color_continuous_scale="Viridis", # Échelle de couleurs
                               mapbox_style="carto-positron", # Style de fond de carte
                               zoom=4, 
                               center = {"lat": 46.603354, "lon": 1.888334}, # Centre de la France
                               opacity=0.8,
                               labels={'prix_m2_moyen_global':'Prix Moyen au m² (€)'},
                               hover_data={'code_commune': True, 'nombre_ventes_global': True}
                              )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

# Exemple d'utilisation (pour tester le composant seul)
# fig = create_choropleth_map()
# fig.show()