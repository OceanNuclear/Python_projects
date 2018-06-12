#!/home/oceanw/anaconda3/bin/python3
#The spherical harmonics function (that produces, monopole, dipole, quadrapole, octapole, etc) is in the form of Y^l_m, as a function of theta.
#If Y is integrated with respect to theta, it is =0 for even l; but a recursive formula need to be used to find the value of the integral if y is odd.
#(Reduction formula for cos^n integral)
import numpy as np
from numpy import array as ary
from numpy import pi, sin, cos
#tau = pi*2
from scipy.misc import comb
from scipy.misc import factorial2 as fac2
from scipy.misc import factorial as fac
from scipy.special import perm



def ceil(num):
	return int(np.ceil(num))
#Integrand is Y^(l)_(m=0); where m=0.
def P0(l):	#Find the integral of P0l 
	if l%2==0: return 0
	Sum = 0
	for q in range (ceil(l/2), l+1):
		Sum += fac(2*q)*fac2(2*q-l-1) / fac( (l-q) * fac(q) * fac(2*q-l) * fac2(2*q-l) )
	return 1/(2**l) * Sum

while True:
	l = int(input("l="))
	print(P0(l))
