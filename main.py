import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import os

from src.components.layout import create_layout

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DETAIL_CSV = os.path.join(DATA_DIR, "cleaned", "data_detail.csv")

print("Chargement des données")
df = pd.read_csv(DETAIL_CSV, dtype={'code_commune': str, 'code_departement': str})

departements = sorted(df['code_departement'].unique())
types_biens = sorted(df['type_local'].unique())
min_price = int(df['prix_m2'].min())
max_price = int(df['prix_m2'].max())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "ImmoViz France"

app.layout = create_layout(departements, types_biens, min_price, max_price)

if __name__ == '__main__':
    app.run(debug=True)
