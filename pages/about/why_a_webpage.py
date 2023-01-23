import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "22rem",
    "padding": "6rem 1rem",
}


dash.register_page(__name__, name='Why a webpage?')

layout = html.Div(
    [
     html.Div("About > Why a webpage?", style={"font-style":"italic", "padding-bottom":'15px'}),
     html.H3("Why a webpage?", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     html.Div("In short: Because it is fun!"),
     dcc.Markdown('''Of course, there are other reasons. My objective is to also show some of my skills and interests
                  to potential employers.  
                  I believe there are several relevant skills that are required for a project like this:
                  some related to the technical implementation (basically coding), others related to my professional expertise
                  (finance and fixed income), and finally, communication skills (content!).  
                  You can find about the last two throughout the site and the [relevant section](/about/professional-experience).
                  Here I will elaborate on the technical side of the project.
     '''),
     html.H4("Technical Skills", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     dcc.Markdown('''This page was done using Dash and the theme is highly inspired in their [documentation site](https://dash.plotly.com)
                  (unfortunately, I lack graphic design skills or _good taste_ to create one of my own). My goal though,
                  was to make as much as possible (or while it is interesting) manually, trying to imitate their theme but not just importing a template.
                  I'm happy with the result, which has helped me:
         '''),
     dcc.Markdown('''
                  * Practice my Python coding skills.
                  * Refresh my knowdledge of Dash, which has been through several updates since the first time I used it.
                  * Learn a little about HTML, some Markdown, and a lot of CSS and its magic.
                  * Apply data scraping techniques and data processing.
                  * Learn about the deployment process and optimizing resources.
                  * Practice version control: the source code of this project is [hosted on GitHub](https://github.com/Jmora-00/jmora-app.git), please don\'t look too much into it.
     '''),
    ],
    style=CONTENT_STYLE
)