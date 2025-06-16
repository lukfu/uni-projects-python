import numpy as np
from matplotlib import pyplot as plt

t = 100000  # Number of iterations
N = 10000
x = np.zeros((t + 1, N))  # Pre allocation of the positions
dt = 0.01
L = 50
sigma_0 = 1
delta_sigma = 0.9

for i in range(t):
    x[i + 1, :] = x[i, :] + sigma_0 * np.random.randn(N) * np.sqrt(dt)
    x[i + 1, :] = (x[i + 1, :] + L) % (2 * L) - L  # Periodic boundary conditions

l = np.arange(100) - 50
h10 = np.histogram(x[10, :], l)
h100 = np.histogram(x[100, :], l)
h1000 = np.histogram(x[1000, :], l)
h10000 = np.histogram(x[10000, :], l)
h100000 = np.histogram(x[100000, :], l)

plt.figure(figsize=(15, 10))
plt.plot(h10[1][:-1] + 1 / 2, h10[0])
plt.plot(h100[1][:-1] + 1 / 2, h100[0])
plt.plot(h1000[1][:-1] + 1 / 2, h1000[0])
plt.plot(h10000[1][:-1] + 1 / 2, h10000[0])
plt.plot(h100000[1][:-1] + 1 / 2, h100000[0])
plt.legend(['t=10', 't=100', 't=1000', 't=10000', 't=100000'])
plt.ylabel('$p(x)$')
plt.xlabel('$x$')
plt.title('Distribution in a well, periodic boundary conditions')
plt.rcParams.update({'font.size': 18})
plt.show()
