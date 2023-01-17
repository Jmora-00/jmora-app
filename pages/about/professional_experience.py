import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "22rem",
    "padding": "6rem 1rem",
}

dash.register_page(__name__, name='Professional Experience')

def generate_graph_aum():
    data = pd.read_csv('assets/data/aum.csv', index_col=0)
    data.iloc[:,1] = data.iloc[:,1]/1000
    data.columns = ['Date', 'AUM (US$ Bn)']
    fig = px.line(data, x="Date", y="AUM (US$ Bn)", 
                  title='Chilean Central Bank and Treasury Bonds in AFP Capital\'s Portfolio',
                  template='plotly_dark')
    
    # add shaded areas
    x0 = ['2020-07-30', '2020-12-10', '2021-04-21']
    x1 = ['2021-07-30', '2021-12-10', '2022-04-21']
    
    for i in range(len(x0)):
        fig.add_vrect(x0=x0[i], x1=x1[i], 
              annotation_text=str(i+1)+" Withdrawal", annotation_position="top left",
              fillcolor="gray", opacity=0.25, line_width=0)
        
    fig = fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(22,26,29, 1)"})
    
    y_pos = [1, 0.90, 0.80]
    
    annot = fig.to_dict()["layout"]["annotations"]
    for (i, a) in enumerate(fig.to_dict()["layout"]["annotations"]):
        annot[i]["y"] = y_pos[i]
        #fig.update_layout(annotations=[{**a, **{"y": y_pos[i]}}])
    fig.update_layout(annotations=annot)
    
    return fig

def generate_graph_fundE():
    data = pd.read_csv('assets/data/vcfE2018-2022_mod.csv', index_col=0)
    norm = (data.iloc[:,0:6]).divide(data.iloc[0,0:6])*100
    norm.index = pd.to_datetime(norm.index, format='%m/%d/%Y')
    norm.index.names = ['Date']
    fig = px.line(norm, x=norm.index, y=norm.columns, 
                  labels={
                     "Date": "Date",
                     "value": "Return",
                     "variable": "Manager"
                  },
                  title='Fund E total return by manager (5Y)',
                  template='plotly_dark')

    return fig

def generate_graph_fundC():
    data = pd.read_csv('assets/data/vcfC2020-2021_mod.csv', index_col=0)
    norm = (data.iloc[:,0:7]).divide(data.iloc[0,0:7])*100
    norm.index = pd.to_datetime(norm.index, format='%m/%d/%Y')
    norm.index.names = ['Date']
    fig = px.line(norm, x=norm.index, y=norm.columns, 
                  labels={
                     "Date": "Date",
                     "value": "Return",
                     "variable": "Manager"
                  },
                  title='Fund C total return by manager (2Y)',
                  template='plotly_dark')

    return fig

layout = html.Div(
    [
     html.Div("About > Professional Experience", style={"font-style":"italic", "padding-bottom":'15px'}),
     html.H3("Updated Information", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     html.Div("To review my most updated credentials please:"),
     html.Li(
             [
                 html.Div("Visit my ", style={"display": "inline"}), 
                 dcc.Link("LinkedIn Profile", href="https://www.linkedin.com/in/juanamora/", target="_blank"),     
             ]),
     html.Li(
             [
                 html.Div("Download my ", style={"display": "inline"}), 
                 dcc.Link("Resume", href=dash.get_asset_url("MFE23-JAMora.pdf"), target="_blank"),    
             ]),
     html.Div("In the following sections I will provide more details about particular aspects of my professional experience.",
              style={ "padding-top":'10px'}),
     
     html.H3("AFP Capital", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     html.Div("""I worked for approximately 5 years in AFP Capital, a chilean pension fund manager.
              If you are not familiar with the chilean pension system, I provide some brief
              context in the following note."""),
     html.Blockquote(
         [
             html.Div("The chilean pension system:", style={'font-weight':'bold', "padding-bottom":'10px'}),
             html.Li("Chilean pension fund system is based on individual capitalization and fixed contribution.", style={'list-style-position':'outside'}),
             html.Li("Each individual chooses among several privately owned pension fund managers to invest their retirement savings.", style={'list-style-position':'outside'}),
             html.Li("Pension fund managers therefore compete to maximize investment returns under a defined risk framework.", style={'list-style-position':'outside'}),
             html.Li("Each pension fund manager has 5 different funds to choose from. They are named A to E (ordered in increasing level of risk).", style={'list-style-position':'outside'}),
         ]
         , className='blockNote'),
     html.Div("""I was in charge of local sovereign bonds and IRS strategies and trading in AFP Capital.
              I was also responsible for the cash management for all funds. Due to the funds' asset composition, 
              I was more involved in fund E's strategy (most conservative, higher percentage of local sovereign bonds),
              and fund C (balanced fund) of which I was co-portfolio manager during 2020-2021. 
              The AUM under my supervision varied between approximately US$ 10bn and US$ 6bn as shown in the following graph."""),     
     dcc.Graph(id='graph-aum', figure=generate_graph_aum(), style={'margin':'30px'}),
     html.Div("""In the previous graph you can see the amount of local bonds had a high variation. This is explained by several factors:"""),
     html.Li("During 2019 the macroeconomic outlook was positive, which triggered a decrease in these 'safe' assets.", style={'list-style-position':'outside'}),
     html.Li("To fight the effects of COVID, clients were allowed to partially redeem their funds. The liquidity of local bonds and the Central Bank's repurchase program made them good candidates to finance the redemptions.", style={'list-style-position':'outside'}),
     html.Div("""AFP Capital Fund E was the best performer during the overall 2018-2022 (5 year) period. 
              In the following graph you can see the fund's performance normalized to the first day of 2018. 
              The fund's nominal return was 45.98% during this period, or an annual return of 7.86% 
              (feel free to zoom in using the plotly tools).""", style={'margin-top':'15px'}),
     dcc.Graph(id='graph-fundE', figure=generate_graph_fundE(), style={'margin':'30px'}),
     html.Div("""During my period as co-portfolio manager of AFP Capital's fund C our total return was 12.54%, or 
              6.09% annual. This placed us second only to Habitat, that returned 6.16% annualy, and far above
              any other managers."""),
     dcc.Graph(id='graph-fundE', figure=generate_graph_fundE(), style={'margin':'30px'}),
    ],
    style=CONTENT_STYLE
)
              