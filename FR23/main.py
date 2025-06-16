import learn as learn
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from scipy.optimize import curve_fit


# average definition
def average(V):
    avy=0.0
    aN=64.0
    for M in range(0,L):
        avy=avy+V[M]

    avy=avy/aN
    return avy


# curve fit function definition
def f(x,a,b,c):
    """Fit function y=f(x,p) with parameters p=(a,b,c) """
    return a*(1.0-np.exp(-b*x))+c


# fitting definition
# 1st adc@0.005 sec, 2nd adc@0.005+dx...
def fitting(V):
    L = 64
    x = np.arange(0.0,float(L),1.0)   # start,stop,step
    avy = 0.0
    for M in range(0,L):
        avy = avy+V[M]
        avy = avy/float(M)

# call curve fit function
    # bounds for parameters, maxfev for max amount of points, limit if too many points are hindering runtime
    popt, pcov = curve_fit(f, x, V,
                           bounds=((0.0,0.0,-1000.0),(300.0,2.0,1000.0)),maxfev=1000)
    a, b, c = popt

    S=0.0
    St=0.0
    for M in range (0,L):
        y=a*(1.0-np.exp(-b*x[M]))+c
        S=S+(V[M]-y)**2
        St=St+(V[M]-avy)**2

    r2=1.0-S/St
    print(a,b,c,r2)
    # print("Fitting parameters are a=%g, b=%g, r2=%g" % (a,b,r2))
    # file2.write(str(a)+' '+str(b)+' '+str(r2)+'\n')

    #plotting
    # import pylab
    # yfitted = f(x, *popt)   # equivalent to f(x, popt[0], popt[1], popt[2])
    # pylab.plot(x, V, 'o', label='data $y_i$')
    # pylab.plot(x, yfitted, '-', label='fit $f(x_i)$')
    # pylab.xlabel('x')
    # pylab.legend()
    # plt.show()

    return a,b,r2


def read_file(file_name):
    # Using open as to make sure the file is closed in the right way
    with open(os.path.join(sys.path[0], file_name), "r") as f:
        text = f.read()
    data_list = []
    # First split the rows in the file
    text = text.split('\n')
    # Then split the rows in the right way and adding the items in a temporary list, and finally adding that list to
    # the final list
    for row in text:
        item = row.split(';')
        if len(item) > 1:
            data_list.append(item)
    return data_list


# clean up
OMXdata = read_file('OMXdata.csv')
OMXdata.pop(0)
OMXdata.pop(0)

for x in range(4):
    for row in OMXdata:
        row.pop(len(row)-1)
for row in OMXdata:
    row.pop(1)
    row.pop(1)
OMXdata.reverse()


def calculate_return(kurs, datum, plot):
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

    x = np.asarray(retDatum, dtype='datetime64[s]')
    if plot == 1:
        plt.plot(x, ret)
        plt.tick_params(axis='x', labelrotation=90)
        plt.show()

    return retDatum, ret


#Splitting the data into parts
particular_value = '2012-01-02'
OMX0512 = []
for i in OMXdata:
    if i[0] == particular_value:
        break
    else:
        OMX0512.append(i)

OMXdata.reverse()
particular_value = '2017-01-02'
OMX1723 = []
for i in OMXdata:
    if i[0] == particular_value:
        OMX1723.append(i)
        break
    else:
        OMX1723.append(i)
OMX1723.reverse()
OMXdata.reverse()

#Making temporary data for plotting
datum0512 = [i[0] for i in OMX0512]
kurs0512 = [float(i[1].replace(",", ".")) for i in OMX0512]

#Making temporary data for plotting
datum1723 = [i[0] for i in OMX1723]
kurs1723 = [float(i[1].replace(",", ".")) for i in OMX1723]

ret1 = calculate_return(kurs0512,datum0512,0)
ret2 = calculate_return(kurs1723,datum1723,0)

ret1_size = np.size(ret1)
ret2_size = np.size(ret2)

ret1_data = []
ret1_date = []
for i in range(int(ret1_size/2)):
    iData = int(ret2_size/2 + i)
    print(i)
    ret1_data[i] = ret1[iData]
    ret1_date[i] = ret1[i]

print(ret1_data)
