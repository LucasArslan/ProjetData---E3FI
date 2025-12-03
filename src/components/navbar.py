# Barre de navigation du dashboard
import dash_html_components as html

def navbar():
    """Retourne la barre de navigation"""
    return html.Nav([
        html.Ul([
            html.Li(html.A("Accueil", href="/")),
            html.Li(html.A("À propos", href="/about")),
        ])
    ], className="navbar")
