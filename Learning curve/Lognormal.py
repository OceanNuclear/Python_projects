#!/home/oceanw/anaconda3/bin/python3
#Hypothesis: The sigmoidal shape of a learning curve can be explained by 
#Code for generating a lognormal distribution, for purely testing purpose.
#Unfinished.

import matplotlib.pyplot as plt
import random as rn
import numpy as np

def Reset_x( mu , sigma ):
	x = [0]*15
	x[0] = rn.lognormvariate( mu , sigma )/15
	for i in range( 1 , 15 ):
		x[i] = x[i-1] + rn.lognormvariate( mu , sigma )/15 
		if x [i] > 1:
			x[i] = 1
	#This creates a ceiling of 1 for the rest of the function.
	return x
x=[0]*100
print(np.shape((x)))
for j in range (0,100):
	x[j] = Reset_x(0,1)
	#x[jth trial][ith time's]
x = np.transpose(x)
print(np.shape((x)))
y = [0]* 15
print(np.shape((x)))
for i in range (0,15):
	y[i]=np.mean(x[i])

plt.plot(y)
plt.show()

#Conclusion: the approach of summing up random trials (of the sigma and mu value!) only gives the same result as integrating the lognormal function.
#This model fails to reproduce the sigmoidal shape of the curve.

#Next step: randomize sigmal and mu values.
