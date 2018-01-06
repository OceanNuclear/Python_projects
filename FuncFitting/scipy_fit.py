#!/home/oceanw/anaconda3/bin/python3

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

inFile = str(input("Please type in the input filename (without .txt):\n"))
inFile += str(".txt")
numLines = sum(1 for line in open(inFile))

x = []
y = []
dy= []

def fittedFunc(x, a, b):
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

dummy, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_title("Custom function fitting using scipy")
ax1.errorbar(x, y, yerr = dy, fmt ='o',)
ax2.set_title("Residuals")
ax2.plot(x,np.zeros(numData), linewidth=1)

print("Parsed ", numData, " data points.")

[(a,b),((var_a,dummy),(dummy,var_b))] = curve_fit(fittedFunc, x, y, sigma = dy, absolute_sigma=True, check_finite=True)
#(var_a,dummy),(dummy,var_b) = pcov
da = np.sqrt(var_a)
db = np.sqrt(var_b)
yCalc = fittedFunc(x,a,b)

residual = y- yCalc

xSmooth = np.linspace(np.min(x), np.max(x), 1000)
yCalcSmooth = fittedFunc(xSmooth, a, b)

chiSq = sum( (residual/dy)**2 )
chiSqPerDoF = str( '{:0=3.2f}'.format( chiSq/numData ) )

aString=('%.2e' % a)
bString=('%.2e' % b)
aPlace= aString[-3:]
bPlace= bString[-3:]
if(aPlace[:1]=="e"): aPlace=aPlace[-2:]
if(bPlace[:1]=="e"): bPlace=bPlace[-2:]
daString= str( '{:0=2.2f}'.format( (da/10**int(aPlace)), aPlace=int(aPlace) )+"e"+aPlace )
dbString= str( '{:0=2.2f}'.format( (db/10**int(bPlace)), bPlace=int(bPlace) )+"e"+bPlace )

#printing the parameters
print("a=",a,"+\-",da)
print("b=",b,"+\-",db)

equation = ("a ="+aString+r'$\pm$'+daString+str('\n')+"b ="+bString+r'$\pm$'+dbString +str('\n') + r'$\chi^2$' +"=" +chiSqPerDoF )

Fit = ax1.plot(xSmooth,yCalcSmooth)
ax1.legend(Fit, [equation])
#legend(loc="upper left", bbox_to_anchor=(1,1)) #uncomment this line to move the legend outside of the plot area.
ax2.errorbar(x, residual, yerr=dy, fmt='o')
plt.show()
