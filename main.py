import dash
from src.pages.home import layout as home_layout # <-- Importation du layout de la page d'accueil

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Définition du layout global de l'application (ici, on utilise simplement la mise en page 'home')
app.layout = html.Div(
    children=[
        # Ici, vous pourriez ajouter votre Header et Navbar (si créés)
        home_layout
        # Ici, vous pourriez ajouter votre Footer
    ]
)

# Lancer l'application si le script est exécuté directement
if __name__ == '__main__':
    print("Démarrage du dashboard sur http://127.0.0.1:8050/")
    # Assurez-vous d'avoir les données nettoyées et le GeoJSON en place avant de lancer
    app.run_server(debug=True)