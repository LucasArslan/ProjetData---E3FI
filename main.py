import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import os

from src.components.layout import create_layout

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DETAIL_CSV = os.path.join(DATA_DIR, "cleaned", "data_detail.csv")

print("Chargement des données")
df = pd.read_csv(DETAIL_CSV, dtype={'code_commune': str, 'code_departement': str})
df['date_mutation'] = pd.to_datetime(df['date_mutation'])

departements = sorted(df['code_departement'].unique())
types_biens = sorted(df['type_local'].unique())
min_price = int(df['prix_m2'].min())
max_price = int(df['prix_m2'].max())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "ImmoViz France"
app.layout = create_layout(departements, types_biens, min_price, max_price)

@app.callback(
    [Output('kpi-price', 'children'),
     Output('kpi-volume', 'children')],
    [Input('btn-update', 'n_clicks')],
    [State('filter-dept', 'value'),
     State('filter-type', 'value'),
     State('filter-price', 'value')]
)
def update_kpis(n_clicks, dept, types, price_range):
    mask = (df['type_local'].isin(types)) & \
           (df['prix_m2'] >= price_range[0]) & \
           (df['prix_m2'] <= price_range[1])
    
    if dept != 'all':
        mask = mask & (df['code_departement'] == dept)
    
    filtered = df[mask]
    
    avg_price = f"{filtered['prix_m2'].mean():.0f}"
    volume = f"{len(filtered):,}".replace(",", " ")
    
    return avg_price, volume

if __name__ == '__main__':
    app.run(debug=True)
