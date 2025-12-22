from dash import dcc, html
import dash_bootstrap_components as dbc

DEPARTEMENTS = {
    '01': 'Ain', '02': 'Aisne', '75': 'Paris', '13': 'Bouches-du-Rhône',
    '69': 'Rhône', '33': 'Gironde', '44': 'Loire-Atlantique'
}

def create_layout(dept_codes, types_biens, min_price, max_price):
    sidebar = html.Div([
        html.H2("ImmoViz", className="display-6"),
        html.Hr(),
        
        html.Label("Département"),
        dcc.Dropdown(
            id='filter-dept',
            options=[{'label': "France Entière", 'value': 'all'}] + 
                    [{'label': f"{d} - {DEPARTEMENTS.get(d, '')}", 'value': d} for d in dept_codes],
            value='all',
            clearable=False
        ),
        
        html.Label("Type de bien"),
        dcc.Checklist(
            id='filter-type',
            options=[{'label': f" {t}", 'value': t} for t in types_biens],
            value=types_biens,
            inputStyle={"margin-right": "5px"}
        ),
        
        html.Label("Prix / m² (€)"),
        dcc.RangeSlider(
            id='filter-price',
            min=min_price,
            max=max_price,
            value=[min_price, max_price],
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        
        html.Button("Actualiser", id='btn-update', className="btn-update"),
    ], className="sidebar")
    
    content = html.Div([
        html.H3("Carte"),
        dcc.Graph(id='map-graph')
    ], className="content")
    
    return html.Div([sidebar, content])
