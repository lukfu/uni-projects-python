import numpy as np
import matplotlib.pyplot as plt

N=128
data = np.loadtxt('fire5a1.csv')
fire = np.array(data)
fire=np.sort(fire)
k = len(fire)
C = [(k-x)/k for x in range(k)]
plt.loglog(fire/pow(N,2),C,'ro')

data = np.loadtxt('fire5a2.csv')
fire = np.array(data)
fire=np.sort(fire)
k = len(fire)
C = [(k-x)/k for x in range(k)]
leg = plt.loglog(fire/pow(N,2),C,'bo')
plt.show()