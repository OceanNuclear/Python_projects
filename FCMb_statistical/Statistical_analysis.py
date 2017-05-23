#!/home/oceanw/anaconda3/bin/python3
#This is written to statistically analyse the file "raw_data"in the same directory.
import numpy as np
import matplotlib.pyplot as plt

#USELESS
#Function to trim away the infinities in the data;
#def rm_inf(x, y):
#	x_out = []
#	y_out = []
#	for i in range (0,1000):	#runs up to 999 only
#		if abs(x[i])>100000000 or abs(y[i])>100000000:
#			x_out.append(0)
#			y_out.append(0)
#		else:
#			x_out.append(x[i])
#			y_out.append(y[i])
#	return(x_out, y_out)

#USELSS
#Overcomplicating part of the code that I decided to give up on.
#I mean I can use f.tell() to fix this problem of  'can't do nonzero cur-relative seeks' but I mean why should I do that?
#y = []
#for i in range (0,100000):
#	if f.read(4) != '': 
#		f.seek(
#		y.append(int(f.read(4)))
#	else:
#		break
#numData = len(y)

#Taking in data
f = open('raw_data', "r")
f.seek(0)			#because I'm paranoid that the pointer might be in some other place than the start of the file.
sigma_f = [0]*109		#There are 109 entries in the file.
for i in range (0,109):
	sigma_f[i] = int(f.read(4))


sigma_f.sort()	#Ordering the data set is needed for evalutating Ps.
#rank of y[i] = i+1

#Find the basic statistical values
sd = np.std(sigma_f)
mean = np.mean(sigma_f)
print("Standard Deviation ="+str(sd))	#FYI sd = 118.67416715388205
print("mean = "+str(mean))
cv = sd/mean
print("Coefficient of variation = "+str(cv))

#Plotting part
# 1. We need Ps, -ln(-ln(Ps)), rank, sigma_f, ln(sigma_f)
Rank = np.linspace(1, 109, 109)
Ps = 1- (Rank/(109+1))

from numpy import log
x = log(sigma_f)
y = -log(-log(Ps))

# 2. Weibull plot
plt.scatter(x,y)
plt.show()

#3. Linear regression
from scipy.stats import linregress
list_of_data = linregress(x,y)
print(list_of_data)
