#!/home/oceanw/anaconda3/bin/python3

#auth B Mitchell
#Gives ProbdensityFunctions Evolution with time for some average momentum

import numpy as np
import matplotlib.pyplot as plt

def propegatingWave(x, t):
    
    a = 0.5 #determines origanal uncertainty in momentum
    b = 2   #constant
    k0 = 1   #average wave number
    
    coeff = 1/(np.sqrt(1/(2*a*a) + b*b*t*t/2))
    exp = np.exp(( -1*np.power((a*x- b*a*k0*t),2) )/(1+b*b*t*t/4))

    return coeff*exp;    

plt.ion()
ax = plt.gca()
#One of these two above lines give the changing colour :)
t = np.arange(0,20,0.1)
delt = 0.05
time = 0;

while time < 7:
    
    ax.relim
    plt.plot(t, propegatingWave(t,time))
    time = time + delt
    plt.pause(0.05)
    plt.draw()
