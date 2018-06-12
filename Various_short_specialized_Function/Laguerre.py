#!/home/oceanw/anaconda3/bin/python3
#Contains the functions that make the Laguerre polynomials and the associated Laguerre polynomial.
from numpy import array as ary
import numpy as np
from numpy import pi, e, real, imag
import matplotlib.pyplot as plt
from scipy.special import gamma
from scipy.special import factorial as fac



def HCF(x, y):
	x = abs(x)
	y = abs(y)
	if x > y:
		smaller = y
	else:
		smaller = x
	for i in range (1, int(smaller)+1):
		if((x%i == 0) and (y%i == 0)):
			hcf = i	#reassign hcf to be the current i.
	return hcf

#def fac(l):	#extend the definition of factorial by using the gamma function.
#	return gamma(l+1)

def Laguerre(x,q,k):	#k-th term of the Laguerre polynomial.
	#x has range from neg inf to pos inf;
	#q has range from 0 to pos inf;
	#k has range from 0 to q
	return ((fac(q)/fac(q-k))**2) * (e**(1j*pi*k)/fac(k))*x**(q-k)


def AddLaguerre(x,q):	#plot the Laguerre polynomial for a varying x, fixed q and k.
	y = np.zeros(np.shape(x))*(0+0j)
	for k in range (q+1):
		y += Laguerre(x,q,k)
	return y

x = np.linspace(0,4,1000)
#y = AddLaguerre(x,10)

def plotLagK(x,q):	#plot the kth term (smoothly varying), for a fixed x and q, a varying k.
	y = Laguerre(x,q,np.linspace(0,q,1000))
	z1= Laguerre(x,q,np.linspace(q,2*q,1000))	#less than the allowed range of k
	z2= Laguerre(x,q,np.linspace(-q,0,1000))	#more than the allowed range of k
	return y,z1,z2

def associatedLaguerreCoefList(n,k):
	poly = []
	for m in range (n+1):
		coefDenom= (-1)**m * fac(n+k)
		coefNumin= fac(n-m)*fac(k+m)*fac(m)
		if int(coefDenom/coefNumin)!=(coefDenom/coefNumin):	#append the fraction
			hcf = HCF(coefDenom, coefNumin)
			coef = (int(coefDenom/hcf),int(coefNumin/hcf))
			coef = str(coef[0]) +"/"+ str(coef[1])
		else:	#append the integer
			coef = int(coefDenom/coefNumin)
		poly.append(coef)
	poly.reverse()
	return poly
	
'''
y,z1,z2 = plotLagK(.21,5)

plt.plot(y.real, y.imag, color= 'b')
plt.plot(z1.real,z1.imag,color= 'black')
plt.plot(z2.real,z2.imag,color= 'g')
plt.show()
'''
while True:
	n = int(input("n="))
	l = int(input("l="))
	print("The polynomial is", associatedLaguerreCoefList(n,l))
