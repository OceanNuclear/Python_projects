#!/home/oceanw/anaconda3/bin/python3
#source: https://hackernoon.com/washington-d-c-gives-no-fucks-be51aa152fe

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.misc import factorial
from scipy.special import jv

x = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
y = [53,206,263,227,130,72,50,43,15,13,9,6,2,3,1]
numData = len(x)
if (len(y)!=len(x)): raise ValueError
def fittedFunc(N, A, T, c):
	yCalc = A*np.exp(-T)*(T)**N /factorial(N) -c*jv(0,N)
	return yCalc

dummy, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_title("Poisson modelling of number of Fucks given on twitter"+str('\n')+"using the function " + r'$A \frac{T^N}{N!} e^{-T}$')
ax1.errorbar(x, y, yerr = 0.5, fmt ='o',)
ax2.set_title("Residuals")
ax2.plot(x,np.zeros(numData), linewidth=1)

print("Parsed ", numData, " data points.")

[(a,b,c),((var_a,dummy, dummy),(dummy, var_b, dummy), (dummy, dummy, var_c))] = curve_fit(fittedFunc, x, y, check_finite=True)
#(var_a,dummy),(dummy,var_b) = pcov
da = np.sqrt(var_a)
db = np.sqrt(var_b)
dc = np.sqrt(var_c)
yCalc = fittedFunc(x,a,b,c)
residual = y- yCalc

aString=('%.2e' % a)
bString=('%.2e' % b)
cString=('%.2e' % c)
aPlace= aString[-3:]
bPlace= bString[-3:]
cPlace= bString[-3:]
if(aPlace[:1]=="e"): aPlace=aPlace[-2:]
if(bPlace[:1]=="e"): bPlace=bPlace[-2:]
if(cPlace[:1]=="e"): cPlace=cPlace[-2:]
daString= str( '{:0=2.2f}'.format( (da/10**int(aPlace)), aPlace=int(aPlace) )+"e"+aPlace )
dbString= str( '{:0=2.2f}'.format( (db/10**int(bPlace)), bPlace=int(bPlace) )+"e"+bPlace )
dcString= str( '{:0=2.2f}'.format( (dc/10**int(cPlace)), cPlace=int(cPlace) )+"e"+cPlace )

print("a=",a,"+/-",da)
print("b=",b,"+/-",db)
print("c=",c,"+/-",dc)

equation = ("a ="+aString+r'$\pm$'+daString+str('\n')+"b ="+bString+r'$\pm$'+dbString + "c ="+cString+r'$\pm$'+dcString)

xSmooth = np.linspace(np.min(x), np.max(x), 1000)
yCalcSmooth = fittedFunc(xSmooth,a,b,c)

Fit = ax1.plot(xSmooth, yCalcSmooth)
ax1.legend(Fit, [equation])
#legend(loc="upper left", bbox_to_anchor=(1,1)) #uncomment this line to move the legend outside of the plot area.
ax2.errorbar(x, residual, yerr=0.5, fmt='o')
plt.ylabel("instances")
plt.xlabel("nubmer of u")
plt.show()
