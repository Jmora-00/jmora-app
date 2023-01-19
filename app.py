import dash
from dash import html, dcc, Input, Output, State 
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.

menu_drop_style = {'background-color': 'rgb(0,0,0,0.0)', 
                     'textAlign': 'left',
                     'color': 'white',
                     'font-weight': 'bold',
                     'border': '0px',
                     'cursor':'pointer'
                     }

menu_link_style = {'background-color': 'rgb(0,0,0,0.0)', 
                     'textAlign': 'left',
                     'color': 'rgb(151,160,175,1)',
                     'border': '0px',
                     'cursor':'pointer',
                     'margin-left':'15px'}

sidebar = html.Div(
    [
        html.Img(src='/assets/juan_mora_logo_dark.png', height=82, width=246, className='center'),
        # html.Hr(
        #     style={'height':'1px', 'color':'var(--highlight)', 'backgroundColor':'var(--highlight)', 
        #            'borderWidth':'1px', 'borderColor':'var(--highlight)', 'opacity':'1',
        #            'margin-bottom':'1px'}),
        dbc.NavLink("Contact me", href="https://www.linkedin.com/in/juanamora/", target="_blank", 
                    style={'textAlign':'center','font-weight':'normal','color':'rgb(151,160,175,1)',
                           'borderRadius':'20px',
                           'border': '0px solid var(--grey)',
                           'padding-top':'5px',
                           'padding-bottom':'5px',
                           'margin-left': '20px',
                           'margin-right': '20px',
                           'margin-bottom':'20px',
                           'margin-top':'20px',
                           'background-color': 'rgb(36,42,68,1)'}),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/",  style=menu_link_style),
                dbc.NavLink("▾ About", active="exact", id="drop-menu-about", style=menu_drop_style),
                dbc.Collapse(
                    [
                        dbc.NavLink(
                            dash.page_registry['pages.about.professional_experience']["name"], 
                            href=dash.page_registry['pages.about.professional_experience']["path"], 
                            style=menu_link_style
                        ),
                        dbc.NavLink(
                            dash.page_registry['pages.about.why_a_webpage']["name"],
                            href=dash.page_registry['pages.about.why_a_webpage']["path"], 
                            style=menu_link_style
                        ),
                        dbc.NavLink(
                            dash.page_registry['pages.about.acknowledgments']["name"],
                            href=dash.page_registry['pages.about.acknowledgments']["path"], 
                            style=menu_link_style
                        )
                    ],
                    id="collapse-menu-about", is_open=True
                ),
                dbc.NavLink("▾ Fixed Income", active="exact", id="drop-menu-fixed_income", style=menu_drop_style),
                dbc.Collapse(
                    [
                        dbc.NavLink(
                            dash.page_registry['pages.fixed_income.discussion_br']["name"],
                            href=dash.page_registry['pages.fixed_income.discussion_br']["path"], 
                            style=menu_link_style
                        ),
                        # dbc.NavLink(
                        #     dash.page_registry['pages.fixed_income.sample_app']["name"], 
                        #     href=dash.page_registry['pages.fixed_income.sample_app']["path"],
                        #     style=menu_link_style
                        # )
                    ],
                    id="collapse-menu-fixed_income", is_open=True
                )
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, dash.page_container])

@app.callback(
    Output("collapse-menu-about", "is_open"),
    [Input("drop-menu-about", "n_clicks")],
    [State("collapse-menu-about", "is_open")],
)
def toggle_collapse_about(n, is_open):
    if n:       
        return not is_open
    return is_open

@app.callback(
    Output("collapse-menu-fixed_income", "is_open"),
    [Input("drop-menu-fixed_income", "n_clicks")],
    [State("collapse-menu-fixed_income", "is_open")],
)
def toggle_collapse_fixed_income(n, is_open):
    if n:       
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run(debug=True)
