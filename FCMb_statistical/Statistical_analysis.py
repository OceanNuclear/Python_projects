#!/home/oceanw/anaconda3/bin/python3
#This is written to statistically analyse the file "raw_data"in the same directory.
import numpy as np
import matplotlib.pyplot as plt

#Taking in data
f = open('raw_data', "r")
f.seek(0)			#because I'm paranoid that the pointer might be in some other place than the start of the file.
y = [0]*109			#There are 109 entries in the file.
for i in range (0,109):
	y(i) = int(f.read(4))

#Statistical part
sd = np.std(y)
mean = np.mean(y)
print("Standard Deviation =" + sd)	#FYI sd = 118.67416715388205
print("mean = " + mean)
cv = sd/mean
print("Coefficient of variation = " + cv)

#Plotting part
