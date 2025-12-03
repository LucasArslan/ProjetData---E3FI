# Composant spécifique à la page complexe
import dash_html_components as html

def component():
    """Retourne un composant spécifique"""
    return html.Div([
        html.P("Contenu du composant spécifique"),
    ])
