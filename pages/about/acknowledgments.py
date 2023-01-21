import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "22rem",
    "padding": "6rem 1rem",
}

dash.register_page(__name__, name='Acknowledgments')

layout = html.Div(
    [
     html.Div("About > Acknowledgments", style={"font-style":"italic", "padding-bottom":'15px'}),
     html.H3("Acknowledgments", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     dcc.Markdown('''I ask a lot of questions. Thank you to all the people that still reply.  
                  For this project, in particular:
     '''),
     dcc.Markdown('''
                  * [Bo Johansson](https://www.linkedin.com/in/bo-johansson-88b63558/): the discussion on bond return\'s would not have been possible without his help and guidance.
                  * [Fernando Irarrazaval](https://www.linkedin.com/in/fernando-irarrazaval/): from databases and web hosting to graphic design. This guy knows everything.
                  * [Ruchir Sharma](https://www.linkedin.com/in/sharma-ruchir/): his macroeconomic insightfulness is only matched by his proofreading skills.
     '''),
    ],
    style=CONTENT_STYLE
)