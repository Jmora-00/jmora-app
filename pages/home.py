import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "16rem",
    "padding": "6rem 1rem",
}

button_style={'font-size': '14px', 
              'width': '280px', 
              'display': 'inline-block', 
              'margin-bottom': '10px', 
              'margin-left': '5px',
              'border-radius': '4px',
              'font-weight': 'bold',
              'height':'100px', 
              'background-color': 'rgb(0,0,0,0.0)',
              'color': 'gray',
              'border': '1px solid gray',
              'textAlign': 'center',
              'verticalAlign': 'center'}

dash.register_page(__name__, path='/', name='Home') # '/' is home page

# Homepage
df = px.data.gapminder()

layout = html.Div(
    [
        html.P(
               """I'm a finance professional interested in markets, fixed income and derivatives. Here you can find more information about myself.""", className="lead"
           ),
        html.H3("About", style={'margin-top':'20px','margin-bottom':'20px'}),
        dbc.Row([
            dbc.Col(html.Button('Professional Experience', id='prof-exp-button', n_clicks=0, className='homeButton')),
            dbc.Col(html.Button('Why a webpage?', id='why-awp-button', n_clicks=0, className='homeButton')),
            dbc.Col(html.Button('Acknowledgments', id='acknowledgments-button', n_clicks=0, className='homeButton')),
        ]),
        html.H3("Fixed Income", style={'margin-top':'20px','margin-bottom':'20px'}),
        dbc.Row([
            dbc.Col(html.Button('Discussion on bond returns estimation', id='br-button', n_clicks=0, className='homeButton')),
            dbc.Col(html.Button('Sample App', id='sample-app-button', n_clicks=0, className='homeButton')),
            dbc.Col(html.Button('Contact me', id='contact-button', n_clicks=0, className='homeButton')),
        ]),

    ],
    style=CONTENT_STYLE
)


