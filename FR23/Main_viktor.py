import VaR
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.stats import genpareto
from scipy.stats import genextreme as gev
import scipy.stats as stats
import openturns as ot
from pyextremes import get_extremes

#Cleaning the data
OMXS30data = VaR.read_file('OMXdata.csv')
OMXS30data.pop(0)
OMXS30data.pop(0)

for x in range(4):
    for row in OMXS30data:
        row.pop(len(row)-1)
for row in OMXS30data:
    row.pop(1)
    row.pop(1)
OMXS30data.reverse()

#Splitting the data into parts
OMX0512 = VaR.create_interval(OMXS30data, '2005-01-03','2012-01-02')

OMX1723 = VaR.create_interval(OMXS30data, '2017-01-02','2023-05-11')

#Making temporary data for plotting
datum0512 = [i[0] for i in OMX0512]
kurs0512 = [float(i[1].replace(",", ".")) for i in OMX0512]

#Making temporary data for plotting
datum1723 = [i[0] for i in OMX1723]
kurs1723 = [float(i[1].replace(",", ".")) for i in OMX1723]

returnsDate0512, returns0512 = VaR.calculate_return(kurs0512, datum0512,0)
returnsDate1723, returns1723 = VaR.calculate_return(kurs1723, datum1723,0)

exc0512 = VaR.calc_exceedances(returns0512, -3.38742)  ####
exc1723 = VaR.calc_exceedances(returns1723, -2.40204)

#VaR.plot_gaussian(returns0512)
#VaR.plot_gaussian(returns1723)

q = [5, 4, 3, 2, 1, 0.1, 0.01]
quantiles0512 = VaR.calc_quantiles(returns0512, q)
quantiles1723 = VaR.calc_quantiles(returns1723, q)

gpd_params1 = VaR.plot_gpd(exc0512[0], 3.38742, 0)
gpd_params2 = VaR.plot_gpd(exc1723[0], 2.40204, 0)

gpd_params0512 = [1.54199, -0.28021, 3.38742]  # sigma xi u
gpd_params1723 = [1.28666, 0.14442, 2.40204]

gev_params1 = VaR.plot_gev(returns0512, 0, 0)
gev_params2 = VaR.plot_gev(returns1723, 0.1, 0)

gev_params0512 = [-0.643121, 1.69659, -0.145823]  # mu sigma xi
gev_params1723 = [-0.446329, 1.40785, -0.183821]

nReturn0512 = np.size(returns0512)
nReturn1723 = np.size(returns1723)
nExc0512 = exc0512[1]
nExc1723 = exc1723[1]
