# Layout pour la page complexe
import dash_html_components as html
from .page_specific_component import component

layout = html.Div([
    html.H1("Page Complexe"),
    component(),
])
