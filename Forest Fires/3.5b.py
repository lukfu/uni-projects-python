import numpy as np
import matplotlib.pyplot as plt

N=128
print('Change p: 0.01, 0.03, 0.05, 0.07')


def plotFunc1(filename1,filename2,subplot):
    plt.subplot(1,4,subplot)
    data = np.loadtxt(filename1)
    fire = np.array(data)
    fire=np.sort(fire)
    k = len(fire)
    C = [(k-x)/k for x in range(k)]
    plt.loglog(fire/pow(N,2),C,'ro')
    data = np.loadtxt(filename2)
    fire = np.array(data)
    fire=np.sort(fire)
    k = len(fire)
    C = [(k-x)/k for x in range(k)]
    plt.loglog(fire/pow(N,2),C,'bo')

plotFunc1('fire5b11.csv','fire5b21.csv',1)
plotFunc1('fire5b12.csv','fire5b22.csv',2)
plotFunc1('fire5b13.csv','fire5b23.csv',3)
plotFunc1('fire5b1p1.csv','fire5b2p1.csv',4)
plt.show()
print('slope becomes closer, the higher p is')



print('Change f: 0.1, 0.2, 0.4, 0.8')
plotFunc1('fire5b14.csv','fire5b24.csv',1)
plotFunc1('fire5b15.csv','fire5b25.csv',2)
plotFunc1('fire5b16.csv','fire5b26.csv',3)
plotFunc1('fire5b121.csv','fire5b221.csv',4)
plt.show()
print('f bigger-> slope less clear')





print('T: 100, 500, 2000, 5000')
plotFunc1('fire5b311.csv','fire5b321.csv',1)
plotFunc1('fire5b312.csv','fire5b322.csv',2)
plotFunc1('fire5b313.csv','fire5b323.csv',3)
plotFunc1('fire5b314.csv','fire5b324.csv',4)
plt.show()
print('T bigger--> graph more clear, slope more clear, near x=1 graph become more similar')