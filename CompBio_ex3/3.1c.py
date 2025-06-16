from statistics import mean

import numpy as np
import data as data
import matplotlib.pyplot as plt

bn = 0.1
dn = 0.2
dt = 0.1
data.tb=c()
data.td=c()
for i in 1:10^4
tb = 0
td = 0
t = 0
while tb==0 | td==0:
    t = t+dt # Recording of the time step
    nb = runif(1) # Random number between 0 and 1
    if tb==0 & nb < bn*dt:
        tb = t
        data.tb = c(data.tb, c(tb))

    if td==0 & nb < dn*dt:
        td = t
        data.td = c(data.td, c(td))


mean(data.tb)
mean(data.td)
# Histogram with regular axis
hist(data.td, xlim=c(0,30), breaks=seq(0,100,by=1), main = "td where dn = 0.2",
xlab = "td")
# Histogram with log axis
hist.data = hist(data.td, plot=F, xlim=c(0,30), breaks=seq(0,50,by=1))
plot(hist.data$count, log="y", type=’h’, lwd=2, lend=2, main = "td where dn = 0.2",
xlab = "td", ylab = "Frequency")
