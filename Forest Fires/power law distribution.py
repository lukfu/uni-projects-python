import numpy as np
import matplotlib.pyplot as plt

i = 100    # fire count
r = np.random.uniform(0, 1, i)
alpha = 0.8
fire_size = 500


def p(x):     # probability function p(n), x is fire size
    return x ** -alpha


def c_inverse(m):
    return m ** (1 / (1 - alpha))


n = p(fire_size)
n_i = c_inverse(r)
plt.hist(n_i, bins=20)
plt.show()
