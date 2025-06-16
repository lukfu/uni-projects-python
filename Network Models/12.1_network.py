import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def random_graph(n,p):
    A = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            A[i,j] = np.random.rand()<p
            A[j,i] = A[i,j]

    return A


n = 100
p = 0.1
A = random_graph(n,p)
G = nx.from_numpy_matrix(A)
nx.draw_circular(G)
plt.show()
