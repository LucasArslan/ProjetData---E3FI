# Pied de page du dashboard
import dash_html_components as html

def footer():
    """Retourne le pied de page"""
    return html.Footer([
        html.P("© 2024 Data Dashboard. Tous droits réservés."),
    ], className="footer")
