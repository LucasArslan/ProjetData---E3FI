import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import os

from src.components.layout import create_layout

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DETAIL_CSV = os.path.join(DATA_DIR, "cleaned", "data_detail.csv")
GEO_JSON = os.path.join(DATA_DIR, "raw", "etalab_communes.geojson")

print("Chargement des données")
df = pd.read_csv(DETAIL_CSV, dtype={'code_commune': str})
df['date_mutation'] = pd.to_datetime(df['date_mutation'])

with open(GEO_JSON, 'r', encoding='utf-8') as f:
    geojson = json.load(f)

departements = sorted(df['code_departement'].unique())
types_biens = sorted(df['type_local'].unique())
min_price = int(df['prix_m2'].min())
max_price = int(df['prix_m2'].max())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "ImmoViz France"
app.layout = create_layout(departements, types_biens, min_price, max_price)

@app.callback(
    [Output('map-graph', 'figure'),
     Output('line-evol', 'figure'),
     Output('pie-type', 'figure'),
     Output('kpi-price', 'children'),
     Output('kpi-volume', 'children')],
    [Input('btn-update', 'n_clicks')],
    [State('filter-dept', 'value'),
     State('filter-type', 'value'),
     State('filter-price', 'value')]
)
def update_dashboard(n_clicks, dept, types, price_range):
    mask = (df['type_local'].isin(types)) & \
           (df['prix_m2'] >= price_range[0]) & \
           (df['prix_m2'] <= price_range[1])
    
    if dept != 'all':
        mask = mask & (df['code_departement'] == dept)
    
    filtered = df[mask]
    
    # KPIs
    avg_price = f"{filtered['prix_m2'].mean():.0f}"
    volume = f"{len(filtered):,}".replace(",", " ")
    
    # Carte
    df_map = filtered.groupby(['code_commune', 'nom_commune'])['prix_m2'].mean().reset_index()
    df_map.columns = ['code_commune', 'nom_commune', 'prix_moyen']
    
    fig_map = px.choropleth_mapbox(
        df_map,
        geojson=geojson,
        locations='code_commune',
        featureidkey="properties.code",
        color='prix_moyen',
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 46.5, "lon": 2.5},
        opacity=0.6
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig_map, avg_price, volume

if __name__ == '__main__':
    app.run(debug=True)
