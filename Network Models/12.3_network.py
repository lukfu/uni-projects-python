import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def preferentialgrowth(n, n0, m):
    A = np.zeros((n, n))
    for i in range(n0):  #
        for j in range(i + 1, n0):
            A[i, j] = 1
    A = A + np.transpose(A)
    for t in range(n - n0):
        D = np.sum(A, axis=0) / np.sum(A)
        edges = np.random.choice(np.arange(n), m, replace=False, p=D)
        for i in range(m):
            A[t + n0, edges[i]] = 1
            A[edges[i], t + n0] = 1
    return A


n = 100
n0 = 7
m = 2
A = preferentialgrowth(n,n0,m)
G = nx.from_numpy_matrix(A)
nx.draw_circular(G)
plt.show()
