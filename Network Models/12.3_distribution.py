import numpy as np
from matplotlib import pyplot as plt


def preferentialgrowth_graph(n, n0, m):
    A = np.zeros((n, n))
    for i in range(n0):  # start with n0 sized network, preallocating the full n sized adjacency matrix
        for j in range(i + 1, n0):  # note that this avoids the diagonal i=j since j=i+1
            A[i, j] = 1
    A = A + np.transpose(A)  # symmetric
    for t in range(n - n0):  # creating n-n0 nodes and connect the node with m nodes (that may or may not exist yet)
        D = np.sum(A, axis=0) / np.sum(A)  # current degrees of the existing nodes???
        edges = np.random.choice(np.arange(n), m, replace=False, p=D)  # chooses m edges from integers {0,...,n-1}
        # once a node is chosen, it can not be chosen again
        # the choice is based on the probability determined by the degree D
        for i in range(m):  # wires the randomly chosen edges at the specified nodes
            A[t + n0, edges[i]] = 1
            A[edges[i], t + n0] = 1
    return A


n = 1000
n0 = 5
m = 3  # m is the minimum number of nodes
A = preferentialgrowth_graph(n,n0,m)
degrees = np.sum(A,1)
plt.loglog(np.sort(degrees)[::-1],np.arange(n)/n,'.')
plt.loglog(np.arange(m,np.max(degrees)),m**2*np.arange(m,np.max(degrees))**(-2),'--')

plt.rcParams.update({'font.size': 18})
plt.title('Preferential Growth')
plt.legend(['degree distribution', 'power law'])
plt.ylabel('$C(k)$')
plt.xlabel('$k$')
plt.show()
