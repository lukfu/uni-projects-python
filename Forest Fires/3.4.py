import numpy as np
import matplotlib.pyplot as plt

N=16
data_load = np.loadtxt('fire4a.csv')
fire_array = np.array(data_load)
fire_array=np.sort(fire_array)
k = len(fire_array)
C = [(k-x)/k for x in range(k)]
plt.subplot(1,2,1)
plt.loglog(fire_array/pow(N,2),C,'bo')

data_load = np.loadtxt('fire4b.csv')
fire_array = np.array(data_load)
fire_array=np.sort(fire_array)
k = len(fire_array)
C = [(k-x)/k for x in range(k)]
plt.subplot(1,2,2)
plt.loglog(fire_array/pow(N,2),C,'bo')
plt.show()
