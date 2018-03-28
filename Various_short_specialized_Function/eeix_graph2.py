#!/home/oceanw/anaconda3/bin/python3
# coding: utf-8
#Parametrically plots the e^(e^i*theta)) graph
from numpy import e, cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
import matplotlib.pyplot as plt



t_n = 10000
'''
#Using a logspace causes problems due to inherent flaw of floating points.
def moreTimeLargeEnd(small, large, num):
	if small==0: start=-100
	else: start=np.log(small)

	end = np.log(large)

	inv = np.logspace(end, start, num, base = e)
	return inv[0]-inv
#t = np.logspace(-100, np.log(tau),t_n, base = e)
#t = moreTimeLargeEnd(0,pi,t_n)
#t = np.append(tau-t, t )
'''
t = np.linspace( 0,tau, t_n)
#t = np.logspace(-100, np.log(pi), t_n, base = e)
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
