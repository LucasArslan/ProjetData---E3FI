import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "ImmoViz France"

app.layout = html.Div([
    html.H1("ImmoViz France", style={'textAlign': 'center'}),
    html.Hr(),
    html.P("Dashboard en construction...")
])

if __name__ == '__main__':
    app.run(debug=True)
