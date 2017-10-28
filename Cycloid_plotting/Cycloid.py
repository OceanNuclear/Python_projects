#!/home/oceanw/anaconda3/bin/python3
#Plots a generalized cycloid.

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

R = float(input("How big do you want R/r to be?(r is the radius of the disk, R is the radius of the arm tracing the cycloid.)"))
#Number of steps to integrate = 2000
dtheta = 1/2000
#Integrate to the limit Theta 
Steps = int(4*2*pi/dtheta)

x=[0]*Steps
y=[0]*Steps

for theta_n in range (0, Steps):
	theta = theta_n*dtheta
	x[theta_n] = theta-R*np.sin(theta)
	y[theta_n] = R-2*np.cos(theta)

plt.axes().set_aspect('equal', 'datalim')
plt.plot(x,y)
plt.show()

