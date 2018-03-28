#!/home/oceanw/anaconda3/bin/python3
# coding: utf-8
#Parametrically plots the e^(e^i*theta)) graph
from numpy import e, cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
import matplotlib.pyplot as plt

t_n = 10000
t = np.linspace(0, tau,t_n)

iterations = int(input("how many times should the complex variable e^ix be exponentiated?"))
'''
#here's an example of a recursive function:
def recurse(val):
	if val>0:#Runs the loop down to the 1th time.
		print(val)
		return recurse(val-1)
	else:	#termination condition
		return 0
'''
def recursivelyRaise(l):
	if l==-1:	#termination condition
		return t*1j
	elif l>-1:
		return e**(recursivelyRaise(l-1))
	else:
		return np.log(recursivelyRaise(l+1))
#Unbelievable! I'm extending the definition of my funcion! I'm inventing maths! Just as 3Blue1Brown said!

y = recursivelyRaise(iterations)
x = np.real(y)
y = np.imag(y)

plt.plot(x,y)
plt.show()
