#!/home/oceanw/anaconda3/bin/python3
#This is written to statistically analyse the file "raw_data"in the same directory.
import numpy as np
import matplotlib.pyplot as plt


#For finding (experimental survival probability)
def mt(x,y):
	z = []
	for i in range (0, 496):
		No_of_larger = int(0)
		for j in range (0, 109):
			if y[j]>i:
				No_of_larger +=1
		percentage = float(No_of_larger/109)
		z.append(percentage)
	return(z)
#Well apparently finding Ps is a bit more complicated than just using the experimental probability


#function to trim away the infinities in the data; yet to be implemented, but when used can make the code more beautiful.
def rm_inf(x, y):
	x_out = []
	y_out = []
	for i in range (0,1000):	#runs up to 999 only
		if abs(x[i])>100000000 or abs(y[i])>100000000:
			pass
		else:
			x_out.append(x[i])
			y_out.append(y[i])
	return(x_out, y_out)


#Taking in data
f = open('raw_data', "r")
f.seek(0)			#because I'm paranoid that the pointer might be in some other place than the start of the file.
y = [0]*109				#There are 109 entries in the file.
for i in range (0,109):
	y[i] = int(f.read(4))


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


y.sort()	#Odering the data set is needed for evalutating Ps.

#Find the basic statistical values
sd = np.std(y)
mean = np.mean(y)
print("Standard Deviation ="+str(sd))	#FYI sd = 118.67416715388205
print("mean = "+str(mean))
cv = sd/mean
print("Coefficient of variation = "+str(cv))

#Plotting part
#1. Ps(survival probability)
x = np.linspace(0, 495, 496)
Ps = mt(x,y)
plt.plot(x,Ps)
#plt.show()
#remove the # above to show the plot

#2. Weibull's plot
from numpy import log
y_axis = -log(-log(Ps))
x_axis = log(x)
#truncate away the infinities
x_2 = [0]*394
y_2 = [0]*394
for i in range (101, 495):
	x_2[i-101] = x_axis[i]
	y_2[i-101] = y_axis[i]
plt.plot(x_2, y_2)
#plt.show()
#remove the # above to show the plot

#3. Linear regression
from scipy.stats import linregress
list_of_data = linregress(x_2,y_2)
print(list_of_data)
