import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Acknowledgments')

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 2 and much more!')
    ]
)