# Composant en-tête du dashboard
import dash_html_components as html

def header():
    """Retourne l'en-tête du dashboard"""
    return html.Div([
        html.H1("Data Dashboard", className="header-title"),
    ], className="header")
