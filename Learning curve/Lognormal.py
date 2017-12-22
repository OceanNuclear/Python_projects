#!/home/oceanw/anaconda3/bin/python3
#Hypothesis: The sigmoidal shape of a learning curve can be explained by 
#Code for generating a lognormal distribution, for purely testing purpose.
#Unfinished.

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson

forgetting=0.1/15
maxTrial=1000

def Reset_x(lambda_j):
	progress = [0]*15
	progress[0] = poisson.rvs(lambda_j)/15

	for i in range(1 ,15 ):
		progress[i] = progress[i-1] + poisson.rvs(lambda_j)/15 -forgetting
		if progress[i] > 1:
			progress[i] = float(1)

	#This creates a ceiling of 1 for the rest of the function.
	return progress
x=np.zeros(shape=(maxTrial,15))
for j in range (0,maxTrial):
	randomNumber=np.random.uniform(3,17)
	print(randomNumber)
	x[j] = Reset_x(15/randomNumber)
	#x[jth trial][ith time's]


for j in range (0,10):
	plt.plot(x[j])
	#plot 10 of the random trials


x = np.transpose(x)
y = [0]* 15

for i in range (0,15):
	y[i]=np.mean(x[i])


plt.plot(y,'r', linewidth=3)
plt.show()

#Conclusion: the approach of summing up random trials (of variable mu value) only gives the same result as integrating the lognormal function.
#This model fails to reproduce the sigmoidal shape of the curve.
