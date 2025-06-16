import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from random import sample


def smallworld_graph(n,c,p):
    A = np.zeros((n,n))
    for i in range(n):
        for j in range(int(c/2)):
            A[i,(i+j+1)%n] = 1  # periodic boundary condition, if it goes past the boundary n, loop back
            if np.random.rand()<p:   # With probabilty p, do a rewire
                rewire_index = sample(list(np.where(np.logical_not(A[i,:])&np.logical_not(range(n)==i))[0]),1)
                # rewire the edge to another node with no connection     and     not to itself
                # only condition for np.where, so it returns an array that shows which nodes the rewiring can happen to
                # nodes that can not be rewired to are nodes that are currently wired and the node itself
                # list puts these nodes in a list, sample choose a node that becomes the rewire index
                A[i,(i+j+1)%n] = 0              # remove the existing edge
                A[i,rewire_index] = 1           # rewire the edge
    A = A + np.transpose(A)                     # make the adjacency matrix symmetric
    return A


n = 20
c = 4  # c is how many connections each node can have
p = 0.3
A = smallworld_graph(n,c,p)
G = nx.from_numpy_matrix(A)
nx.draw_circular(G)

plt.show()
