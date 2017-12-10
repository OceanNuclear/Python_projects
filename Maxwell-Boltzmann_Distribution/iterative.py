#!/home/oceanw/anaconda3/bin/python3

#And I have just realized that the iterative method is useless now that I can simply use interpolation to find the point of intersection anyways.

import numpy as np
from scipy.special import erf, erfinv, lambertw
from numpy import pi, sqrt, log, exp
from scipy import constants as c
import matplotlib.pyplot as plt

'''
For the following system of equation:
v98 = erfinv(y1)/sqrt(k)
y2 = 2*sqrt(k/pi)*v98*exp(-k*v98*v98)
y1 = y2 + 0.98
'''

#Pseudo-input
m= 1
m = m*c.u

T = 100
T_u = "K"
k_T = c.k*T
T0=100
T0_u= "K"
k_T0 = c.k*T0

#declaring the constants:
k=m/(2*k_T)
A=4*k**(3/2)/sqrt(pi) 
print(k)

#initial guess value

#Well apparently not all can be solved by the iterative method
#The fixed point iterative method requires the inverse function to be the line of slope m to have absolute value |m| smaller than the other line's |m|.

v = np.linspace(0, 6000, 10000)
y1 = erf(sqrt(k)*v)
y3 = 2*sqrt(k/pi)*v*exp(-k*v*v)+0.98
plt.plot(v,y1)
plt.plot(v,y3)

#f = np.linspace(0,1,1000)
#c = (f-0.98)*sqrt(pi/k)/2
#W = lambertw(-2*c*c*k)
#v98 = sqrt(W).imag/sqrt(2*k)
#This is NOT part of the function; it's only here to be tested; it's the inverse function for y3.
#plt.plot(f,v98)
#plt.show()



v98 = 2860
for i in range(5):
#	print("v98="+str(v98))
	y= erf(sqrt(k)*v98)
	plt.scatter(v98,y,c="b")

	c = (y-0.98)*sqrt(pi/k)/2
#	print("c = "+str(c))
	W= lambertw(-2*c*c*k)
	v98 = sqrt(W).imag/sqrt(2*k)
	#By the means of test plotting the LambertW function, I am able to confirm that this is NOT the function that I wanted in order to invert y into v98.
	#Aaaaand I give up. Because the Lambert W function is not smooth and I don't even know how.
	plt.scatter(v98,y,c="g")


#print(v98)
plt.show()
