#!/home/oceanw/anaconda3/bin/python3

import numpy as np
n_max = 60
A = [0]*(n_max+1)
#To be replaced with fourier analysis
for i in range (0, 30):
	A[2*i+1] = 2*pow(-1, i)/(pow((2*i+1),2)*np.pi)
for n in range (1, n_max): print (A[n])
