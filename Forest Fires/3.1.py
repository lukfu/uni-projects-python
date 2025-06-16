import numpy as np
import matplotlib.pyplot as plt

N=256
data = np.loadtxt('fire1c.csv')
data = data[data<100]
counts, bins, bars = plt.hist(data,100)
n = np.array([x for x in bins])

alpha = 1.1
p = 100*n**(-alpha)
plt.plot(n,p, 'r')
plt.show()
