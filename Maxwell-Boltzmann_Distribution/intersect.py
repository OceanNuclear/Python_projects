#!/home/oceanw/anaconda3/bin/python3

#This file finds the point of intersection of two curves.

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf, erfinv, lambertw
from numpy import pi, sqrt, log, exp
from scipy import constants as c

#region for declaring constants
m= 1
m = m*c.u

T = 100
#T_u = "K"
k_T = c.k*T
k=m/(2*k_T)

x_ax_start=0
x_ax = 6000 #the x-axis limit
dx = 0.01

#plotting the x axis and the two curves
#f = x
#g = np.sin(np.arange(0, 10, int(x_ax/dx)) * 2) * 1000
#g = 2*x - 500
x = np.arange(x_ax_start, x_ax, dx)

f = erf(sqrt(k)*x)
g = 2*sqrt(k/pi)*x*exp(-k*x*x)+0.98

plt.plot(x,f)
plt.plot(x,g)

idx = np.argwhere(np.diff(np.sign(f - g)) != 0).reshape(-1) + 0

#idx is the x indices of the point of intersection -1;
#On average the mean displacement of the actual point of intersection from the marked point is +0.5
#To correct for this the point should be marked at x[idx]+0.5*dx
#And to correct for this the 

#This subprogram is used to handle cases where duplicates form due to f[i-1] == g[i-1] exactly.
def eliminate_duplicate(idx):
	idx2 = np.array([],dtype = int)
	for i in x:
		try:
			if(idx[i] == idx[i+1]-1):
				1==1
			else:
				idx2 = np.append(idx2,idx[i])
				print(type(idx2))
		except IndexError:
			idx2 = np.append(idx2,idx[i])
			break
	return(idx2)

idx = eliminate_duplicate(idx)
	#This eliminate_duplicate(idx) module is optional when porting to other programs.
y_int = erf(sqrt(k)*(x[idx] + 0.5*dx)) #f(x[idx] + 0.5*dx)
for i in idx:
	plt.plot( (x[idx] + 0.5*dx), y_int[i], 'ro')
print((x[idx] + 0.5*dx), y_int)
plt.show()
