import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Discussion on Bond Returns')

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "22rem",
    "padding": "6rem 1rem",
}

layout = html.Div(
    [
     html.Div("Fixed Income > Discussion on Bonds Returns", style={"font-style":"italic", "padding-bottom":'15px'}),
     html.H3("A brief discussion on bond returns estimations", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     html.Div("""In this section I present a discussion on different methodologies to estimate bond returns.
              Estimating the exact return of a bond is commonly handled by Bloomberg or other valuation platforms,
              where going from yield to price is correctly defined but implies several implementation details.
              This makes common (and very necessary), to estimate bond returns when studying investment strategies
              related to fixed income. In the following sections I'll evaluate how good these estimations are."""),
     html.H4("What is the return of a 5 year duration bond when rates increase by 1%?", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     dcc.Markdown('''This is a common question which is usually tackled quickly by the first-order approximation,
                  but to be a little more precise we can also use the second-order approximation that includes
                  the bond\'s convexity.
                  I call this the _'basic method'_ (BM):'''),
     dcc.Markdown('$$r_{BM}=\\frac{\\Delta P}{P}=-ModDur\\times \\Delta y + \\frac{1}{2}Cvex(\\Delta y)^2$$', mathjax=True, style={'textAlign': 'center'}),
     dcc.Markdown('''This is a good enough approximation when considering a brief time period.
                  But what happens when we consider longer investment horizons? In this case, ignoring the effect
                  of time may cause us to arrive at wrong conclusions.'''),
                  
     html.H4("Including the time component", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     dcc.Markdown('''A great explanation on how the time component can be introduced in the return approximation can be 
                  found in [Johansson (2012)](https://mpra.ub.uni-muenchen.de/92607/1/MPRA_paper_92607.pdf).
                  This is basically a Taylor expansion considering variations in yield and time. I refer to 
                  this method as _'Johansson\'s Method'_ (JM):''', link_target="_blank"),
     dcc.Markdown('$$r_{J}=\\frac{\\Delta P}{P}=e^{R_c}-1$$', mathjax=True, style={'textAlign': 'center'}),
     dcc.Markdown('$\\text{Where   } \ \  R_c=\\theta t - ModDur \\times \\Delta y + \\frac{1}{2}(Cvex - ModDur^2)(\\Delta y)^2 + (1+y)^{-1} \Delta y \Delta t$', mathjax=True, style={'textAlign': 'center'}),
     dcc.Markdown('''We can compare the 2 methods we have so far in a simple (theoretical) framework:'''),
     html.Blockquote("""Consider a 5 year bond that pays coupon annually at a 4% rate, 
                  priced initially at par with a 30/360 convention. After 30 days, the bond yield has increased 
                  1% (to 5%). What is the bond return?""", className='blockNote'),
     dcc.Markdown('''With some easy calculations you can find the bond's modified duration to be 4.45 with a convexity of 25.01 (both at par). 
                  The _exact_ price after the 30 days and 1% increase is calculated as the sum of the present values of
                  the future cashflows (which, as mentioned before, in real life is never so simple). This gives us a 
                  price of 96.06 or a exact return of -3.94%. The Basic Method claims the return is -4.33%, 
                  and Johansson\'s method approximates -4.02%. As expected, Johansson\'s method is superior
                  by about 30bps (if you don't want them, I'll gladly take them!).'''),
                  
     html.H4("Does the shape of the curve matter?", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     dcc.Markdown('''So far we have made no assumptions on the curve term-structure, but it indeed has some important 
                  effects on what the returns of a bond are. Lets analyze this in (again) a very simple structure,
                  but adding more decimal precision:'''),
     html.Blockquote("""Consider a 5 year bond that pays coupon annually at a 4% rate, 
                  priced initially at par with a 30/360 convention. Additionally, we have a 2 year bond with 
                  a 0.5% annual coupon also priced at par. The short-term rate is 0.25%. After 1 year
                  the rate of the (now) 4 year bond is 5.0228% (1.0228% increase). What is the bond return?""", className='blockNote'),
     dcc.Markdown('''The first thing that is important to notice here is that the value in rate increase is not 
                  arbitrary. I chose it because it is the implied value in the term structure that I defined. 
                  There is an important property that holds when the implied values of the curve are realized,
                  as stated by Fabozzi : _\"The rules are simple. If forward rates are realized, all positions earn the same return\"_
                  (Fabozzi, The Handbook of Fixed Income Securities, Seventh Edition, p. 172).
                  '''),
     dcc.Markdown('''Although he forgot to mention what return that is, I\'ll give the spoiler: the implied return in that period (kind of makes sense).
                  It is not easy to see at first, and I\'ve had lengthy discussions on the topic. But for now we know that the return of all the bonds is 0.3752%.
                  '''),
     dcc.Markdown('''You don\'t have to believe me. So let's start with what we call the _exact_ price after one year.
                  Notice that we will have only 4 cashflows now (a year has passed), so the discounted cashflows will
                  add up to 96.3752. Now remember that we also need to add the value of the coupon payment of this bond, which is 4.
                  Considering this you will end up with a return of 0.3752% (told you).'''),
     dcc.Markdown('''Now we move on to the Basic Method. This method was not thought to handle coupon payments (think of it as a instantaneous approximation around
                  a yield level), but we can try to adapt it just to see how it goes. I tried the following:'''),
     dcc.Markdown('$$r_{BM}=\\frac{P_1+c-P_0}{P_0}=\\frac{P_1-P_0}{P_0}+\\frac{c}{P_0}=-ModDur\\times\\Delta y + \\frac{1}{2}Cvex(\\Delta y)^2 +\\frac{c}{P_0}$$', mathjax=True, style={'textAlign': 'center'}),
     dcc.Markdown('''Replacing the values as in the same example, we arrive at a return of -0.4225%. Far off, and even in the wrong direction, of the bond return.'''),
     dcc.Markdown('''Johansson's method accuracy was better than I expected: it arrives at 0.3569%, just about 2bps short of the result.''')
    ],
    style=CONTENT_STYLE
)