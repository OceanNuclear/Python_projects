#!/home/oceanw/anaconda3/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants as c
from scipy.special import erfinv, lambertw, erf
from numpy import sqrt, log, exp, pi
import re
#This program plots the (3D) Maxwell boltzmann distribution and integrate above and below a cutoff temperature.

#declaring constants
#I'll leave the boltzmann constant as c.k to prevent confusion with k = m/2kT
#and elementary charge as c.e
#just to make things easy


#Prompt user input
#Validation rule loops involved

m = float(input("Average mass of molecules in the system(u) is: "))
m = m*c.u

def E2v(E):
	v = sqrt(2*E/m)
	return v
def v2E(v):
	E = m*v*v/2
	return E

#program for parsing input
def splitted(string):
	item = [1.0,'placeholder']
	if (len(string.split()) != 2):
		print("invalid input!(please input in form of [123 K]); Exiting...")
		exit()
	item = string.split()
	return item

Tinput = str(input("Temperature T of the system (in eV or K) is: "))
item = splitted(Tinput)
print(item)
T = float(item[0])
T_u = str(item[1])
if (T_u!="eV") and (T_u!="K"):
	print("Invalid unit! Exiting...")
	exit()
elif (T_u == "eV"):
	k_T = c.e*T
elif (T_u == "K"):
	k_T = c.k*T

T0input = str(input("The cutoff E/T (in eV or K) is: "))
item = splitted(T0input)
print(item)
T0 = float(item[0])
T0_u = str(item[1])
if (T0_u!="eV") and (T0_u!="K"):
	print("Invalid unit! Exiting...")
	exit()
elif (T0_u == "eV"):
	k_T0 = c.e*T0
elif (T0_u == "K"):
	k_T0 = c.k*T0

'''
while True:
	T_u=str(input("Unit for T:[eV/K]"))
	if (T_u!="eV") and (T_u!="K"):
		print("Invalid input! Please type in again:")
		continue
	elif (T_u == "eV"):
		k_T = c.e*T
		break
	elif (T_u == "K"):
		k_T = c.k*T
		break

T0= float(input("Cutoff energy is:"))

while True:
	T0_u=str(input("The unit of cutoff temperature/energy T0 is: [eV/K]"))
	if (T0_u!="eV") and (T0_u!="K"):
		print("Invalid input. Please type in again:")
		continue
	elif(T0_u=="eV"):
		k_T0 = c.e*T0
		break
	elif(T0_u=="K"):
		k_T0 = c.k*T0
		break
'''
while True:
	T0_u_int=str(input("Integrate [above] or [below] T0? "))
	if (T0_u_int != "above") and (T0_u_int != "below"):
		print("Invalid input. Please type in again:")
	else: break



#Calculate the simplified constants
k=m/(2*k_T)
A=4*k**(3/2)/sqrt(pi) 

#Plotting 98% of the graph
#v98 is found "graphically" by the intersection of two graphs(without actually showing the graphs)
	#Needs to be changed in 1D plotting

x_ax_start= 0.5*E2v(k_T)
x_ax = 50*E2v(k_T) #50/sqrt(3) times the rms speed is arbitrarily chosen only.
div= 1000
dx = (x_ax - x_ax_start)/div

x = np.linspace(x_ax_start, x_ax, div)

g = erf(sqrt(k)*x)
h = 2*sqrt(k/pi)*x*exp(-k*x*x)+0.99
#0.99 means to show the 99% of molecules with lowest energy.

idx = np.argwhere(np.diff(np.sign(g - h)) != 0).reshape(-1) + 0
y_int = erf(sqrt(k)*(x[idx] + 0.5*dx)) #g(x[idx] + 0.5*dx)

vmax = (x[idx[0]] + 0.5*dx)
print("vmax = "+str(vmax))

v = np.linspace(0, vmax, div)
dv = vmax/div

f = A*v*v*exp(-k*v*v)

v0 = E2v(k_T0)
indv0 = int (v0/dv)

fraction = erf(sqrt(k)*v0)-2*sqrt(k/pi)*v0*exp(-k*v0*v0)
filling = f*1 # I dont' know why the eff won't it work without this line of *1. But it seems if I don't use an identity formula like this, I'll link filling up with f; changing filling[i] will also change the value of f[i]

for i in range (0 , indv0):
     try:
          filling[i] = 0.0
     except IndexError:
          break
	# if T0 is off the graph, then IndexError will occur.

if (T0_u_int == "above"):
	fraction = 1-fraction
	filling = f - filling

#Print the result
print("Fraction of molecules with energy "+T0_u_int+str(T0)+str(T0_u)+" = " + str(fraction) + " ")
#fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
fig, (ax1) = plt.subplots( 1, 1, sharex=True)

ax1.fill_between(v, f, filling, where = f > filling, facecolor='green', interpolate = True)
ax1.plot(v,f, 'b')

plt.show()
