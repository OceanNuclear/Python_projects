#!/home/oceanw/anaconda3/bin/python3
from numpy import array as ary
import numpy as np
from numpy import pi, e, real, imag
import matplotlib.pyplot as plt
from scipy.special import gamma
#from scipy.special import factorial as fac



def fac(l):
	return gamma(l+1)
def Laguerre(x,q,k):
	#x has range from neg inf to pos inf;
	#q has range from 0 to pos inf;
	#k has range from 0 to q
	return ((fac(q)/fac(q-k))**2) * (e**(1j*pi*k)/fac(k))*x**(q-k)


def AddLaguerre(x,q):
	y = np.zeros(np.shape(x))*(0+0j)
	for k in range (q+1):
		y += Laguerre(x,q,k)
	return y

x = np.linspace(0,4,1000)
#y = AddLaguerre(x,10)

def plotLagK(x,q):
	y = Laguerre(x,q,np.linspace(0,q,1000))
	z1= Laguerre(x,q,np.linspace(q,2*q,1000))	#after
	z2= Laguerre(x,q,np.linspace(-q,0,1000))	#before
	return y,z1,z2

y,z1,z2 = plotLagK(.21,5)

plt.plot(y.real, y.imag, color= 'b')
plt.plot(z1.real,z1.imag,color= 'black')
plt.plot(z2.real,z2.imag,color= 'g')
plt.show()
