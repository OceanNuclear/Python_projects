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

def dDevda(x,a,b):
	return ( 1/(x*np.sqrt(a*x+b**2)) )

def dDevdb(x,a,b):
	return ( b/(x*np.sqrt(a*x+b**2)) )
'''
def dDevdc(x,a,b,c):
	return ( )
'''

loopTime=5
def xIntercept(x1,y1,x2,y2):
	if (np.sign(y1) != np.sign(y2)):
		return (x1 + (x2-x1)*y1/(y1-y2))
	else:
		print("Not within estimation range! Extrapolating...")
		return (x1 + (x2-x1)*y1/(y1-y2))
	#Works for linear function only, which we expect the d(Dev)/da function to be, since Dev is quadratic wrt. a (and b.)

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
x = np.array(x)
y = np.array(y)
dy = np.array(dy)
numData = len(x)
print("Parsed ", numData, " data points.")

#Next step is to minimize S below:
def Dev (x, y, dy, a, b):
	return sum((fittedFunc(x, a, b)-y/dy)^2)

#By finding:
#loop twice to get the two points requierd?
def fitVar(a1, a2, b1, b2):
	a1 = float (a1)
	a2 = float (a2)
	b1 = float (b1)
	b2 = float (b2)
	print("first try at finding a...") #Variation in a fixed at b1
	print()
	S1 = sum( ((fittedFunc(x,a1,b1)-y)/dy)*(dDevda(x,a1,b1)) )
	S2 = sum( ((fittedFunc(x,a2,b1)-y)/dy)*(dDevda(x,a2,b1)) )
	a = xIntercept(a1,S1,a2,S2)
	print("a= ",a)	
	print("a= ",a)	
	print("first try at finding b...") #Variation in a fixed at a
	S1 = sum( ((fittedFunc(x,a,b1)-y)/dy)*(dDevdb(x,a,b1)) )
	S2 = sum( ((fittedFunc(x,a,b2)-y)/dy)*(dDevdb(x,a,b2)) )
	b = xIntercept(b1,S1,b2,S2)
	print("b= ",b)
	'''
	print("first try at finding c...") #Variation in a fixed at a,b
	S1 = sum( ((fittedFunc(x,a,b,c1)-y)/dy)*(dDevdb(x,a,b,c1)) )
	S2 = sum( ((fittedFunc(x,a,b,c2)-y)/dy)*(dDevdb(x,a,b,c2)) )
	b = xIntercept(c1,S1,c2,S2)
	print("c= ",c)
	'''

	for n in range (loopTime):
		print("	n=", (n+1) ," try;") 
		a1 = a- ((a2-a1)/10)
		a2 = a+ ((a2-a1)/10)
		print("a1=", a1, "a2=", a2)
		S1 = sum( ((fittedFunc(x,a1,b)-y)/dy)*(dDevda(x,a1,b)) )
		S2 = sum( ((fittedFunc(x,a2,b)-y)/dy)*(dDevda(x,a2,b)) )
		a = xIntercept (a1,S1,a2,S2)
		print("a= ",a)
		if(a<=0):
			print("a hits the lower bound!")
			a=0
		b1 = b- ((b2-b1)/10)
		b2 = b+ ((b2-b1)/10)
		print("b1=", b1, "b2=", b2)
		S1 = sum( ((fittedFunc(x,a,b1)-y)/dy)*(dDevdb(x,a,b1)) )
		S2 = sum( ((fittedFunc(x,a,b2)-y)/dy)*(dDevdb(x,a,b2)) )
		b = xIntercept (b1,S1,b2,S2)
		if(b<=0):
			print("a hits the lower bound!")
			b=0
		print("b= ",b)
		'''
		sum( ((fittedFunc(x,a,b)-y)/dy)*(dDevdc(x,a,b,c1)) )
		sum( ((fittedFunc(x,a,b)-y)/dy)*(dDevdc(x,a,b,c2)) )
		b = xIntercept (b1,S1,b2,S2)
		print("b= ",b)
		'''
	return a,b

		
#a, b = fitVar(0.0001,1 ,0.0001,1) abandoning the original method
a, b = fitVar2(0.0001,1,0.0001,1) #Empirically finds the minimum value
yCalc = fittedFunc(x,a,b)
residual = yCalc - y

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
