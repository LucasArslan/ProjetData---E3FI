from dash import dcc, html
import dash_bootstrap_components as dbc

DEPARTEMENTS = {
    '01': 'Ain', '75': 'Paris', '13': 'Bouches-du-Rhône'
}

def create_layout(dept_codes, types_biens, min_price, max_price):
    sidebar = html.Div([
        html.H2("ImmoViz"),
        html.Hr(),
        html.Label("Département"),
        dcc.Dropdown(id='filter-dept', options=[{'label': "France", 'value': 'all'}], value='all'),
    ], className="sidebar")
    
    content = html.Div([
        html.H3("Carte"),
        dcc.Graph(id='map-graph')
    ], className="content")
    
    return html.Div([sidebar, content])
