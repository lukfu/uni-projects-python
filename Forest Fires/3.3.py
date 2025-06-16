import numpy as np
import matplotlib.pyplot as plt

#Trees
nMin = 1
nMax = 5000
nNumber = 7000  # to simulate
alpha = 1.1

nList = np.linspace(nMin,nMax,nMax-nMin+1)
pList = nList**(-alpha)  # Probability for n
pList = 1/sum(pList)*pList  # probability after making sure 0<P<1
cList = [sum(pList[i:]) for i in range(len(nList))]
#random number
randomNumberList = np.random.rand(nNumber)

cArray = np.array(cList)
for i in range(len(randomNumberList)):  # finds index of cArray closest to the random number
    idx = (np.abs(cArray - randomNumberList[i])).argmin()  # x = abs(CDF-r)--> lowest value in x corresponds
    randomNumberList[i] = nList[idx]  # to closest index. found with argmin()
# alters randomNumberList to match nList by reordering randomNumberList

graphMin=1
graphMax=100
plt.hist(randomNumberList,graphMax,range=[graphMin, graphMax],color='C1',alpha=0.8)  # plot random generated distr.

ntrees = np.round(nMin*np.random.rand(nNumber)**(1/(1-alpha)))  # rounding c^-1
plt.hist(ntrees,graphMax,range=[graphMin, graphMax],alpha=0.4)  # plot c^-1 distribution
plt.show()
counts1,bin1,staple1 = plt.hist(ntrees,graphMax,alpha=0.4)
counts2,bin2,staple2 = plt.hist(ntrees,graphMax,range=[graphMin, graphMax],alpha=0.4)
# random distr. is orange, ntrees is brown
