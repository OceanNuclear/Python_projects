#!/home/oceanw/anaconda3/bin/python3

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#inFile = str(input("Please type in the input filename (without .txt):\n"))
#inFile += str(".txt")
#numLines = sum(1 for line in open(inFile))

x = [0.025, 0.04, 0.055, 0.07, 0.085, 0.11, 0.14]
y = [90, 75, 64, 56, 41, 32, 21]
dy= [7, 7, 6, 6, 5, 4, 6]

def fittedFunc(x, a, b, c ):
	yCalc = a*np.exp(-np.sqrt(x**2+c**2)/(b))/x
	return yCalc

'''
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
'''
numData = len(x)
x = np.array(x)
y = np.array(y)
dy = np.array(dy)

guessA = 124
guessB = 0.1
guessC = 2

dummy, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_title(str(r'$a \frac{e^{-\frac{\sqrt{r^2 + c^2}}{b}}}{r}$,'), fontsize = 28)
#ax1.set_suptitle("assume background =0")
ax1.errorbar(x, y, yerr = dy, fmt ='o',)
ax2.set_title("Residuals")
ax2.plot(x,np.zeros(numData), linewidth=1)
ax2.set_ylabel(r'count Rate ($s^{-1}$)')
ax1.set_ylabel(r'count Rate ($s^{-1}$)')
ax2.set_xlabel(r'Distance ($cm$)')

print("Parsed ", numData, " data points.")

[(a,b,c),((var_a,dummy, dummy),(dummy,var_b, dummy), (dummy, dummy, var_c))] = curve_fit(fittedFunc, x, y, sigma = dy, absolute_sigma=True, check_finite=True, p0=(guessA, guessB, guessC))
#(var_a,dummy),(dummy,var_b) = pcov
da = np.sqrt(var_a)
db = np.sqrt(var_b)
dc = np.sqrt(var_c)
yCalc = fittedFunc(x,a,b,c)

residual = y- yCalc

xSmooth = np.linspace(np.min(x), np.max(x), 1000)
yCalcSmooth = fittedFunc(xSmooth, a, b, c)

chiSq = sum( (residual/dy)**2 )
chiSqPerDoF = str( '{:0=3.2f}'.format( chiSq/numData ) )

aString=('%.2e' % a)
bString=('%.2e' % b)
cString=('%.2e' % c)
aPlace= aString[-3:]
bPlace= bString[-3:]
cPlace= cString[-3:]
if(aPlace[:1]=="e"): aPlace=aPlace[-2:]
if(bPlace[:1]=="e"): bPlace=bPlace[-2:]
if(cPlace[:1]=="e"): cPlace=cPlace[-2:]
daString= str( '{:0=2.2f}'.format( (da/10**int(aPlace)), aPlace=int(aPlace) )+"e"+aPlace )
dbString= str( '{:0=2.2f}'.format( (db/10**int(bPlace)), bPlace=int(bPlace) )+"e"+bPlace )
dcString= str( '{:0=2.2f}'.format( (dc/10**int(cPlace)), cPlace=int(cPlace) )+"e"+cPlace )

#printing the parameters
print("a=",a,"+\-",da)
print("b=",b,"+\-",db)
print("c=",c,"+\-",dc)

equation = ("a ="+aString+r'$\pm$'+daString+str('\n')+"b ="+bString+r'$\pm$'+dbString +str('\n') +str('\n')+"c ="+cString+r'$\pm$'+dcString +str('\n') + r'$\chi^2$' +"=" +chiSqPerDoF )

Fit = ax1.plot(xSmooth,yCalcSmooth)
ax1.legend(Fit, [equation])
#legend(loc="upper left", bbox_to_anchor=(1,1)) #uncomment this line to move the legend outside of the plot area.
ax2.errorbar(x, residual, yerr=dy, fmt='o')
plt.show()
