from dash import dcc, html
import dash_bootstrap_components as dbc

DEPARTEMENTS = {
    '01': 'Ain', '02': 'Aisne', '75': 'Paris', '13': 'Bouches-du-Rhône',
}

def create_layout(dept_codes, types_biens, min_price, max_price):
    sidebar = html.Div([
        html.Div([
            html.H2("ImmoViz", className="display-6"),
            html.Hr(),
        ], className="sidebar-header"),
        
        html.Label("Département", className="filter-label"),
        dcc.Dropdown(
            id='filter-dept',
            options=[{'label': "France Entière", 'value': 'all'}] + 
                    [{'label': f"{d}", 'value': d} for d in dept_codes],
            value='all',
            clearable=False
        ),
        
        html.Label("Type de bien", className="filter-label"),
        dcc.Checklist(
            id='filter-type',
            options=[{'label': f" {t}", 'value': t} for t in types_biens],
            value=types_biens,
            inputStyle={"margin-right": "5px"}
        ),
        
        html.Label("Prix / m² (€)", className="filter-label"),
        dcc.RangeSlider(
            id='filter-price',
            min=min_price,
            max=max_price,
            value=[min_price, max_price],
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        
        html.Label("Date D�but (2023)", className="filter-label"),
        dbc.Row([
            dbc.Col(dcc.Dropdown(id='start-day', options=[{'label': i, 'value': i} for i in range(1, 32)], value=1), width=6),
            dbc.Col(dcc.Dropdown(id='start-month', options=[{'label': i, 'value': i} for i in range(1, 13)], value=1), width=6),
        ]),
        
        html.Label("Date Fin (2023)", className="filter-label"),
        dbc.Row([
            dbc.Col(dcc.Dropdown(id='end-day', options=[{'label': i, 'value': i} for i in range(1, 32)], value=31), width=6),
            dbc.Col(dcc.Dropdown(id='end-month', options=[{'label': i, 'value': i} for i in range(1, 13)], value=12), width=6),
        ]),
        
        html.Button("Actualiser", id='btn-update', className="btn-update"),
    ], className="sidebar")
    
    content = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Prix Moyen"),
                dbc.CardBody([
                    html.H2(id='kpi-price', className="kpi-value"),
                    html.Small("€ / m²", className="text-muted")
                ])
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Volume Ventes"),
                dbc.CardBody([
                    html.H2(id='kpi-volume', className="kpi-value"),
                ])
            ]), width=3),
        ]),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Cartographie"),
                dbc.CardBody([dcc.Graph(id='map-graph', style={'height': '60vh'})])
            ]))
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("�volution Prix"),
                dbc.CardBody(dcc.Graph(id='line-evol', style={'height': '300px'}))
            ]), width=8),
            dbc.Col(dbc.Card([
                dbc.CardHeader("R�partition"),
                dbc.CardBody(dcc.Graph(id='pie-type', style={'height': '300px'}))
            ]), width=4),
        ])
    ], className="content")
    
    return html.Div([sidebar, content])
