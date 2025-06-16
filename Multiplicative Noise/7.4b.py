import numpy as np
import matplotlib.pyplot as plt

t=100000  # number of timesteps
N=10000  # number of particles
sigma=1
dSigma=1.8
dt=0.01
L=100
alpha=1
x = np.random.randint(2,size=(t+1,N))*2-1
x = x.astype(float)

for i in range(t):
    x[i+1,:] = x[i,:] + alpha * (sigma + dSigma/L * x[i,:]) * dSigma/L * dt + (sigma + dSigma/L * x[i,:]) * np.sqrt(dt) * x[i+1,:]
    x[i+1,x[i+1,:]>L] = L
    x[i+1,x[i+1,:]<-L] = -L
    # x[i + 1, :] = (x[i + 1, :] + L/2) % L - L/2  # Periodic boundary conditions
    # x[i + 1, :] = np.where(x[i + 1, :] < -L / 2, (-L - x[i + 1, :]), x[i + 1, :])
    # x[i + 1, :] = np.where(x[i + 1, :] > L / 2, (L - x[i + 1, :]), x[i + 1, :])

l=np.arange(51)*2-50
h10=np.histogram(x[10,:],l)
h100=np.histogram(x[100,:],l)
h1000=np.histogram(x[1000,:],l)
h10000=np.histogram(x[10000,:],l)
h100000=np.histogram(x[100000,:],l)

plt.figure(figsize=(13,16))
plt.plot(h10[1][:-1]+1/2,h10[0])
plt.plot(h100[1][:-1]+1/2,h100[0])
plt.plot(h1000[1][:-1]+1/2,h1000[0])
plt.plot(h10000[1][:-1]+1/2,h10000[0])
plt.plot(h100000[1][:-1]+1/2,h100000[0])

plt.legend(['t=10', 't=100', 't=1000', 't=10000', 't=100000'])
plt.ylabel('$p(x)$')
plt.xlabel('$x$')
plt.title('distribution')
plt.rcParams.update({'font.size': 18})
plt.show()
