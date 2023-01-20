import dash
from dash import dcc, html, callback, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd

dash.register_page(__name__, name='Discussion on Bond Returns')

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "22rem",
    "padding": "6rem 1rem",
}

def return_error_jm(T,c,y0,y1):
    dt = 1
    
    # calculate initial price
    T0 = np.arange(1,T+1)
    cf0 = np.ones(T)*c*100
    cf0[-1] = cf0[-1] + 100
    dcf0 = (1/(1+y0)**T0)*cf0
    P0 = np.sum(dcf0)
    
    # calculate price after a year
    T1 = T0 - dt
    T1 = T1[T1>0]
    cf1 = cf0[T0 - dt > 0]
    dcf1 = (1/(1+y1)**T1)*cf1
    P1 = np.sum(dcf1)
    
    # calculate return
    r = (P1+100*c)/P0 -1
    
    # calculate return using JM
    mod_dur0 = np.sum(dcf0*T0)/(1+y0)/P0
    convex0 = np.sum((T0**2+T0)*dcf0)/(1+y0)**2/P0
    theta0 = np.log(1+y0)
    rc0 = theta0*dt - mod_dur0*(y1-y0) + 0.5*(convex0 - mod_dur0**2)*(y1-y0)**2 \
        + (y1-y0)*dt/(1+y0)
    r_jm = np.exp(rc0)-1
    
    return (r-r_jm)*100

def generate_graph_jm():
    c_range = np.linspace(0,200,5)/1000
    y_range = np.arange(-200,1001)/10000
    results = pd.DataFrame(index=y_range, columns=(c_range*100).astype(str))
    
    for c_i in c_range:
        for y_i in y_range:
            results.loc[y_i,str(c_i*100)] = return_error_jm(5,c_i, 0.04, y_i)
            
    results.index = results.index - 0.04

    fig = px.line(results, x=results.index, y=results.columns, 
                  title='Johansson\'s Method Approximation Error',
                  labels={
                     "index": "d(yield)",
                     "value": "Approx Error (%)",
                     "variable": "Coupon"
                  },
                  template='plotly_dark')
    
    fig = fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(22,26,29, 1)"})
    
    return fig
    
dtable = dash_table.DataTable(
    columns=[
        {"name": ["", "Method"], "id": "method"},
        {"name": ["5Y bond", "dt=30d, dy=1%"], "id": "5y1"},
        {"name": ["5Y bond", "dt=1Y, dy=1.02%"], "id": "5y2"},
        {"name": ["2Y bond", "dt=1Y, dy=0.1256%"], "id": "2y"},
    ],
    data=[
        {
            "method": 'Exact',
            "5y1": '-3.94%',
            "5y2": '0.3752%',
            "2y": '0.3752%',
        },
        {
            "method": 'Johansson\'s',
            "5y1": '-4.02%',
            "5y2": '0.3801%',
            "2y": '0.3752%',
        },
        {
            "method": 'Basic',
            "5y1": '-4.33%',
            "5y2": '-0.4225%',
            "2y": '0.2511%',
        },
    ],
    merge_duplicate_headers=True,
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white',
        'textAlign':'center',
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    },
)   

layout = html.Div(
    [
     html.Div("Fixed Income > Discussion on Bonds Returns", style={"font-style":"italic", "padding-bottom":'15px'}),
     html.H3("A brief discussion on bond returns estimation", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     html.Div("""In this section I present a discussion on different methodologies to estimate bond returns.
              Estimating the exact return of a bond is commonly handled by Bloomberg or other valuation platforms,
              where going from yield to price is correctly defined but implies several implementation details.
              This makes common (and very necessary) to estimate bond returns when studying investment strategies
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
     dcc.Markdown('''Although he forgot to mention what return that is, I\'ll give the spoiler: the return of all bonds is the implied return in that period (kind of makes sense).
                  It is not easy to see at first, and I\'ve had lengthy discussions on the topic. But for now we know that the return of all the bonds is 0.3752%.
                  '''),
     dcc.Markdown('''You don\'t have to believe me. So let's start with what we call the _exact_ price after one year.
                  Notice that we will have only 4 cashflows now (a year has passed), so the discounted cashflows will
                  add up to 96.3752. Now remember that we also need to add the value of the coupon payment of this bond, which is 4.
                  Considering this you will end up with a return of 0.3752% (told you).'''),
     dcc.Markdown('''Now we move on to the Basic Method. This method was not thought to handle coupon payments (think of it as a instantaneous approximation around
                  a yield level), but we can try to adapt it just to see how it performs. I tried the following:'''),
     dcc.Markdown('$$r_{BM}=\\frac{P_1+c-P_0}{P_0}=\\frac{P_1-P_0}{P_0}+\\frac{c}{P_0}=-ModDur\\times\\Delta y + \\frac{1}{2}Cvex(\\Delta y)^2 +\\frac{c}{P_0}$$', mathjax=True, style={'textAlign': 'center'}),
     dcc.Markdown('''Replacing the values as in the same example, we arrive at a return of -0.4225%. Far off, and even in the wrong direction, of the bond return.'''),
     dcc.Markdown('''Johansson's method accuracy was better than I expected: it arrives at 0.3801%, just about half a basis point over the result.'''),
     dcc.Markdown('''We can analyze the results also for the 2 year bond: the implied new yield after a year is 0.6256% (or a 0.1256% increase).
                  In this case Johansson's method is exact at 4 decimal places (0.3752%), but you start seeing differences in the fifth decimal place.
                  The basic method is still far off, forecasting a return of 0.2511%.'''),
     dcc.Markdown('''Finally, even though the shape of the curve can help us know what the actual return is, it doesn\'t 
                  have any *direct* impact on the accuracy of the approximations. What factors do have an impact?'''),
     dcc.Markdown('''
                  * Deviation from initial yield: as expected from a Taylor expansion, the approximation works better around the initial points.
                  * Coupon value: for increases in yield, the higher the coupon payments, the less effective the approximation is. The opposite is true for decreases in yield.'''
                  ),
     dcc.Markdown('''The effect of both variables in our 5 year bond example is shown in the following graph: 
                  '''),
     dcc.Graph(id='graph-error_jm', figure=generate_graph_jm(), style={'margin':'30px'}),
     
     html.H4("Summary and final remarks", style={'margin-top':'30px', 'margin-bottom':'10px', 'font-weight':'bold'}),
     dcc.Markdown('''A table collecting all the approximation results is shown below:'''),
     dtable,
     dcc.Markdown('''Some final remarks: ''', style={'margin-top':'20px'}),
     dcc.Markdown('''
                  * First and second order approximations around the yield do not account for the passage of time. Therefore, they are not useful when considering longer (than very brief) investment periods.
                  * Johansson's method seems to work very good when bonds move near their initial yield. But as the ending 
                  rate deviates from the initial yield you find rapidly increasing errors.
                  * There are other factors that impact the error. For example, the investment period and duration.
                  * Note that even though the yield change for the 5Y bond is similar, the error is higher for 30 days than for 1 year. The time component actually compensates the yield component up to some point.
                  * It\'s not so easy to see at the original scale, but notice in the graph the error is not symmetrical! '''
                  ),
     dcc.Markdown('''How good would this approximation work when using real prices? That's also an interesting discussion. If 
                  you have beared with me up to this point I'd love to have a chat and talk about this.'''),
    ],
    style=CONTENT_STYLE
)