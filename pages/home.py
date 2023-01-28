import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/', name='Home') # '/' is home page

# Homepage
def get_path(page):
    print(dash.page_registry)
    return 'test'

layout = html.Div(
    [
        html.P(
               """I'm a finance professional interested in markets, fixed income and derivatives. Here you can find more information about myself.""", className="lead"
           ),
        html.H3("About", style={'margin-top':'20px','margin-bottom':'20px'}),
        dbc.Row([
            dbc.Col(dbc.Button('Professional Experience', id='prof-exp-button',
                                href="/about/professional-experience",
                                n_clicks=0, className='homeButton')),
            dbc.Col(dbc.Button('Why a webpage?', id='why-awp-button',
                               href='about/why-a-webpage',
                               n_clicks=0, className='homeButton')),
            dbc.Col(dbc.Button('Acknowledgments', id='acknowledgments-button', 
                               href='about/acknowledgments',
                               n_clicks=0, className='homeButton')),
        ]),
        html.H3("Fixed Income", style={'margin-top':'20px','margin-bottom':'20px'}),
        dbc.Row([
            dbc.Col(dbc.Button('Discussion on bond returns estimation', id='br-button', 
                               href='/fixed-income/discussion-br',
                               n_clicks=0, className='homeButton')),
            dbc.Col(
                # dbc.Button('Sample App', id='sample-app-button', 
                #                href='/fixed-income/sample-app',
                #                n_clicks=0, className='homeButton')
                ),
            dbc.Col(),
        ]),

    ],
    className='content',
)