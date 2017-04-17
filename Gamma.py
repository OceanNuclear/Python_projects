#!/home/oceanw/anaconda3/bin/python
#This is my first time using def!
import numpy as np
import scipy.constants as c
def gamma(v):
	g= np.sqrt(1-(v/c.c)**2)
	return 1/g
v= float(input("what's the absolute velocity, in m/s?"))
print(gamma(v))

