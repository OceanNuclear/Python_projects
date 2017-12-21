#!/home/oceanw/anaconda3/bin/python3
#By Ocean Wong on 9/12/2016
#Birmingham, UK
#Intended to plot the velocity and position of a rocket on the surface of the earth (constant g), with a nozzle that's not parallel to the axis of it's centre of mass.
#(this assumes that the spaceship is not subjected to any other forces than gravitational and the push of the nozzle (i.e. no air resistance), and does not lose any significant amount of mass)

import matplotlib.pyplot as plt
import numpy as np
import scipy.special as spc
import scipy.integrate as int
import scipy.constants as k
t_n = 1001
t = np.linspace(0,10,t_n)
g = 1
c = (np.sqrt(k.pi/2)) #correction factor for the fresnel functions
#We only need to know these two ratios for the full calculation.
FM = float(input("What is the ratio of (Mass of rocket):(force exerted by the ejected gas onto the nozzle)(in m/s2)?"))
R_K = float(input("(Minimum distance between the axis of propulsion and the CM)(R):(radius of gyration)(K)?"))
R2K = R_K/2
u = np.sqrt(FM*R2K)
cu= c/u
l = cu*FM

#velocity and position calculations
vi = spc.fresnel(t/cu)
vx = l*vi[0]
vy = l*vi[1]-g*t
velox = lambda x : spc.fresnel(x)[0]
veloy = lambda x : spc.fresnel(x)[1]
x = [0] * (t_n-1)
y = [0] * (t_n-1)
for i in range (0, t_n-1):
	xi = int.quad(velox, 0, t[i]/cu)
	x[i] = l*cu*xi[0]
	yi = int.quad(veloy, 0, t[i]/cu)
	y[i] = l*cu*yi[0]-g/2*t[i]**2
#just for the record, angular speed and position at time t is as below:
#theta = (u*t)**2
#omega = 2*u*u*t
#theta_2pi = theta%(2*k.pi)

#plotting
import pandas as pd
velocity, = plt.plot(vx, vy, label='velocity')
position, = plt.plot(x, y, label='position')
plt.title('Freebody rotation with gravity')
#caption = "Plotting the first 10 seconds of its motion, using force: mass ratio = "
#caption += str(FM)
#caption += " m/s2 and R:K ratio = "
#caption += str(R_K)
#fig = plt.figure()

plt.legend(handles=[velocity, position])#label the graphs
plt.show()

#%save Fresnel_velocity_modelling_2 1-58
#OR: get_ipython().magic('save Fresnel_velocity_modelling_2 1-59')

#The results shows that the velocity will spiral inwards towards the point of
