#!/home/oceanw/anaconda3/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
inFile = str(input("Please type in the input filename (without .txt):\n"))
numLines = sum(1 for line in open(inFile))

x = []
y = []
dy= []

def fittedFunc(x, a, b):
	print(a*x+b**2)	
	print(np.sqrt(a*x + b**2))
	yCalc = np.sqrt(a*x + b**2)/x
	return yCalc

loopTime=10
zoomAccuracy = 10
zoomTime = 2

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

print("Parsed ", numData, " data points.")

#Next step is to minimize Dev, seen below:
def Dev (x, y, dy, a, b):
	return sum((fittedFunc(x, a, b)-y/dy)**2)
Deviation = np.zeros(zoomAccuracy)

a1 = float (0.0001)
a2 = float (1)
b1 = float (0.0001)
b2 = float (1)
b = b1
#c = c1
for u in range (loopTime):
	for v in range (zoomTime):
		if (a1>a2):
			temp = a2
			a2 = a1
			a1 = temp
			a1 -= (a2-temp)
			a2 += (a2-temp)
		else:
			a1 -= (a2-a1)
			a2 += (a2-a1)
			
		aRange = np.linspace(a1, a2, zoomAccuracy)
		for n in range (zoomAccuracy):
			Deviation[n] = Dev(x, y, dy, aRange[n], b)
		#Shuffle (tranlate)
		while (np.nanargmin(Deviation)==0):
			for n in range (zoomAccuracy):
				Deviation[n] = Dev(x, y, dy, aRange[n], b)
			a1 -= (a2-a1)
			a2 -= (a2-a1)
			if (a1 == a2): break	
			print("shuffling value of a to the left to a1, a2 =", a1, a2)
			aRange = np.linspace(a1, a2, zoomAccuracy)#if the Deviation(0) is still min, then the loop will restart

		while (np.nanargmin(Deviation)==9):
			for n in range (zoomAccuracy):
				Deviation[n] = Dev(x, y, dy, aRange[n], b)
			a1 += (a2-a1)
			a2 += (a2-a1)
			if (a1 == a2): break
			print("shuffling value of a to the right to a1, a2 =", a1, a2)
			aRange = np.linspace(a1, a2, zoomAccuracy)

		#Zoom
		a1 = a1+ (a2-a1)*int(np.argwhere((np.argsort(Deviation)==0)))/10 -(a2-a1)/10
		a2 = a1+ (a2-a1)*int(np.argwhere((np.argsort(Deviation)==1)))/10
		a = (a1+a2)/2
		print("v= ",v , ", a = ", a)

	for v in range (zoomTime):
		if (b1>b2):
			temp = b2
			b2 = b1
			b1 = temp
			b1 -= (b2-temp)
			b2 += (b2-temp)
		else:
			b1 -= (b2-b1)
			b2 += (b2-b1)
		bRange = np.linspace(b1, b2, zoomAccuracy)	# range of 10 big chunks
		for n in range (zoomAccuracy):		
			Deviation[n] = Dev(x, y, dy, a, bRange[n])# list their deviations
		while (np.nanargmin(Deviation)==0):		#shift according to deviation if index of the smallest one is 0, i.e. left most
			for n in range (zoomAccuracy):
				Deviation[n] = Dev(x, y, dy, a, bRange[n])
			b1 -= (b2-b1)
			b2 -= (b2-b1)
			if (b1 == b2): break
			print("shuffling value of b to the left to b1, b2 =", b1, b2)
			bRange = np.linspace(b1, b2, zoomAccuracy)#re-create range
		while (np.nanargmin(Deviation)==(zoomAccuracy-1)):
			for n in range (zoomAccuracy):
				Deviation[n] = Dev(x, y, dy, a, bRange[n])
			b1 += (b2-b1)
			b2 += (b2-b1)
			if (b1 == b2): break
			bRange = np.linspace(b1, b2, zoomAccuracy)
			print("shuffling value of b to the right to b1, b2 =", b1, b2)
		b1 = b1+ (b2-b1)*int(np.argwhere((np.argsort(Deviation)==1)))/10
		b2 = b1+ (b2-b1)*int(np.argwhere((np.argsort(Deviation)==1)))/10
		b = (b1+b2)/2
		print("b = ", b)

print(a, b)
a, b
#a, b = fitVar(0.0001,1 ,0.0001,1) abandoning the original method #Empirically finds the minimum value
yCalc = fittedFunc(x,a,b)
residual = y - yCalc

#Plotting
z, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_title("Custom function fitting")
ax1.errorbar(x,y, yerr=dy, fmt='.')
ax1.plot(x,yCalc)
ax2.set_title("Residuals")
ax2.errorbar(x, residual, yerr=dy, fmt=',', linewidth=1)
ax2.plot(x,np.zeros(numData))
plt.plot(x,y)
plt.show()
