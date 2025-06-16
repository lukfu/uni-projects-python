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


#Calculate the return
def calculate_return(kurs, datum, shouldplot):
    kursCopy = kurs
    current = kursCopy.pop(0)

    datumCopy = datum
    datumCopy.pop(0)

    retDatum = []
    ret = []
    while len(kursCopy) > 0:
        retDatum.append(datumCopy[0]) 
        ret.append((kursCopy[0] - current) / current * 100)
        current = kursCopy.pop(0)
        datumCopy.pop(0)

    if shouldplot == 1:
        x = np.asarray(retDatum, dtype='datetime64[s]')
        plt.plot(x, ret)
        plt.tick_params(axis='x', labelrotation=90)
        plt.show()

    return retDatum, ret

def calc_exceedances(ret, u):
    list = []
    nExc = 0
    for i in ret:
        if i < u:
            list.append(-i)
            nExc = nExc + 1

    return list, nExc

def plot_gaussian(ret):
    mu, std = norm.fit(ret)
    plt.hist(ret, bins=25, density=True, alpha=0.6, color='g')

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()

def read_file(file_name):
    #Using open as to make sure the file is closed in the right way
    with open(os.path.join(sys.path[0], file_name), "r") as f:
        text = f.read()
    list = []
    #First split the rows in the file
    text = text.split('\n')
    #Then split the rows in the right way and adding the items in a temporary list, and finally adding that list to the final list
    for row in text:
        item = row.split(';')
        if(len(item) > 1):
            list.append(item)
    return list

def create_interval(list, start, stop):
    interval = []
    offset = 0
    for i in range (len(list)):
        if list[i][0] == start:
            offset = i
            break
    for i in range (len(list)):
        a = list[i+offset]
        if a[0] == stop:
            break
        else:
            interval.append(list[i+offset])
    return interval


def calc_quantiles(list, q):
    return np.percentile(list, q)


def plot_gpd(exc, threshold, shouldplot):
    exc = [x - threshold for x in exc]
    c = 0.1
    x = np.linspace(genpareto.ppf(0.01, c),
                    genpareto.ppf(0.99, c), 100)

    fig, ax = plt.subplots(1, 1)
    ax.plot(x, genpareto.pdf(x, c), 'r-', lw=5, alpha=0.6, label='genpareto pdf')

    vals = genpareto.ppf([0.001, 0.5, 0.999], c)
    np.allclose([0.001, 0.5, 0.999], genpareto.cdf(vals, c))

    ax.hist(exc, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
    ax.set_xlim([x[0], 10])
    ax.legend(loc='best', frameon=False)
    if shouldplot == 1:
        plt.show()

    sample = ot.Sample([[v] for v in exc])
    gpd_params = ot.GeneralizedParetoFactory().build(sample)
    return gpd_params


def plot_gev(ret, c, shouldplot):
    x = np.linspace(gev.ppf(0.01, c), gev.ppf(0.99, c), 100)
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, gev.pdf(x, c), 'r-', lw=5, alpha=0.6, label='genextreme pdf')
    vals = gev.ppf([0.001, 0.5, 0.999], c)
    np.allclose([0.001, 0.5, 0.999], gev.cdf(vals, c))

    ax.hist(ret, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
    ax.set_xlim([x[0], x[-1]])
    ax.legend(loc='best', frameon=False)
    if shouldplot == 1:
        plt.show()

    sample = ot.Sample([[v] for v in ret])
    gev_params = ot.GeneralizedExtremeValueFactory().buildAsGeneralizedExtremeValue(sample)
    return gev_params


def es_calc(var, sigma, gamma, mu):  # var is the gpd var
    ES = var + (sigma + gamma * (var - mu))/(1 - gamma)
    return ES


def monthly_var_calc(ret, nExc, nRet, quantiles, sigma, xi, mu):
    # max returns in each block as array
    T = 20
    l = nExc/nRet
    mu_new = (xi/sigma) * ((T * l) ** sigma - 1)
    sigma_new = xi * (l * T) ** sigma
    block_maxima = get_extremes(ts=ret, method="BM", extremes_type="low", block_size="20D", errors="raise",
                                min_last_block=None)
    BM = []
    for q in quantiles:
        BM_q = np.quantile(block_maxima, q)
        BM.append(BM_q)

    return BM

