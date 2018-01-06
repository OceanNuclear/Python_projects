#!/home/oceanw/anaconda3/bin/python3
#This program plots a function with error bars.
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.interpolate import spline

inFile = str(input("Please type in the input filename (without .txt):\n"))
while (inFile!= str("")):
	inFile += str(".txt")
	numLines = sum(1 for line in open(inFile))

	x = []
	y = []
	dy= []

	f = open(inFile, "r")
	line=["" for x in range (numLines)]
	for n in range (numLines):
		line[n]=(str(f.readline()))
		if (len(line[n].split()) != 3):
			pass
		else:
			x.append( float(line[n].split()[0]) )
			y.append( float(line[n].split()[1]) )
			dy.append(float(line[n].split()[2]) )
	numData = len(x)
	x = np.array(x)
	y = np.array(y)
	dy = np.array(dy)
	xSmooth = np.zeros(0)
	for dataPoint in range (1, len(x)):
		xSmooth = np.append( xSmooth, np.linspace( x[dataPoint-1], x[dataPoint], 10))
	ySmooth = spline(x, y, xSmooth)

	plt.plot(xSmooth, ySmooth)
	plt.errorbar(x, y, yerr=dy, fmt='.', linewidth=2) #Among all styles of dots, ',' is the smallest, '.' is the second smallest.
	inFile = str(input("Please type in the input filename (without .txt):\n"))
xName = str(input("Name of the xaxis?"))
yName = str(input("Name of the yaxis?"))
title = str(input("Title?"))

plt.title(title)
plt.xlabel(xName)
plt.ylabel(yName)
plt.show()
