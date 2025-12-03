from dash import html, dcc
from src.components.map_component import create_choropleth_map # <-- Importation du composant

# Créez la carte (elle sera chargée au lancement de l'application)
choropleth_fig = create_choropleth_map()

# Définition du layout (de la structure visuelle) de la page d'accueil
layout = html.Div(
    children=[
        html.H1("Analyse des Prix Immobiliers au m²", className="header-title"),
        
        # Le composant dcc.Graph() de Dash affiche l'objet Figure de Plotly
        dcc.Graph(
            id='prix-m2-map',
            figure=choropleth_fig,
            className="card" # Ajout de classe CSS pour le style
        ),
        
        html.Div("Sources : DVF (data.gouv.fr) et Contours INSEE", className="footer-info"),
    ]
)