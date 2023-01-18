# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:37:33 2023

@author: Tonijua
"""

import plotly.express as px
import numpy as np
import pandas as pd

# params
dt = 1
c = 0.04
y0 = 0.04
y1 = 0.05

# calculate initial price
T0 = np.arange(1,6)
cf0 = np.ones(5)*c*100
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
r = (P1+100*c)/P0

# calculate return using JM
mod_dur0 = np.sum(dcf0*T0)/(1+y0)/P0
convex0 = np.sum((T0**2+T0)*dcf0)/(1+y0)**2/P0
theta0 = np.log(1+y0)
rc0 = theta0*dt - mod_dur0*(y1-y0) + 0.5*(convex0 - mod_dur0**2)*(y1-y0)**2 \
    + (y1-y0)*dt/(1+y0)
r_jm = np.exp(rc0)-1


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

c_range = np.linspace(0,200,5)/1000
y_range = np.arange(-200,1001)/10000
results = pd.DataFrame(index=y_range, columns=(c_range*100).astype(str))

for c_i in c_range:
    for y_i in y_range:
        results.loc[y_i,str(c_i*100)] = return_error_jm(5,c_i, 0.04, y_i)
fig = px.line(results, x=results.index, y=results.columns)
fig.show()

    