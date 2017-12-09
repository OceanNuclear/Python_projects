#!/home/oceanw/anaconda3/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants as c
from scipy.special import erfinv, lambertw, erf
from numpy import sqrt, log, exp, pi
#This program plots the (3D) Maxwell boltzmann distribution and integrate above and below a cutoff temperature.

#declaring constants
#I'll leave the boltzmann constant as c.k to prevent confusion with k = m/2kT
#and elementary charge as c.e
#just to make things easy

#Prompt user to choose plotting parameters
#Validation rule loops involved
'''m = float(input("Average mass of molecules in the system(u) is:"))'''
m= 1
m = m*c.u
'''T = float(input("Temperature T of the system is:"))
while True:
	t_u=str(input("Unit for T:[eV/K]"))
	if (t_u!="eV") and (t_u!="K"):
		print("Invalid input. Please type in again:")
		continue
	elif (t_u == "eV"):
		k_T = T/c.e
		break
	elif (t_u == "K"):
		k_T = c.k*T
		break

T0= float(input("Cutoff energy is:"))

while True:
	T0_u=str(input("The unit of cutoff temperature/energy T0 is: [eV/K]"))
	if (T0_u!="eV") and (T0_u!="K"):
		print("Invalid input. Please type in again:")
		continue
	elif(T0_u=="eV"):
		k_T0 = T0/c.e
		break
	elif(T0_u=="K"):
		k_T0 = c.k*T0
		break

while True:
	T0_u_int=str(input("Integrate [above] or [below] T0?"))
	if (T0_u_int != "above") and (T0_u_int != "below"):
		print("Invalid input. Please type in again:")
		continue
	elif (T0_u_int == "above"):
		T0_u_int_bool = True
		break
	elif (T0_u_int == "below"):
		T0_u_int_bool = False
		break
'''
T = 100
T_u = "K"
k_T = c.k*T
T0=100
T0_u= "K"
k_T0 = c.k*T0
T0_u_int="above"

#Plotting 98% of the graph
#Needs to be changed in 1D plotting
#Make a switch inside the program to turn on/off redirection to iterative.py for plotting instead.
#First simplify the constants
k=m/(2*k_T)
A=4*k**(3/2)/sqrt(pi) 
c = log(2/sqrt(pi)) - log(1-0.98)
c=0.1

W= lambertw(-2*exp(-2*c)*k)
v98 = sqrt(W).imag/sqrt(2*k)
print(v98)
v = np.linspace(0, v98 ,1000)


f = A*v*v*exp(-k*v*v)

#Print the result
print("Fraction of molecules with energy "+T0_u_int+str(T0)+str(T0_u)+" = ")
plt.plot(v,f)
plt.show()
