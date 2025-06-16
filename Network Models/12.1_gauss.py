import numpy as np
from matplotlib import pyplot as plt
import scipy.special


def random_graph(n,p):
    A = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            A[i,j] = np.random.rand()<p
            A[j,i] = A[i,j]
    return A


n = 2000
p = 0.05
xmax = 200
A = random_graph(n,p)
degrees = np.sum(A,1)
#prob=np.random.normal(n)

plt.hist(degrees)
#plt.plot(prob)
plt.xlim([0,xmax])
plt.title('Probability distribution')
plt.ylabel('$p(d)$')
plt.xlabel('$d$')
plt.rcParams.update({'font.size': 18})
plt.show()
