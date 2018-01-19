#!/home/oceanw/anaconda3/bin/python3

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

r = np.array([87 ,152, 217, 281, 346])
d = np.array([-40, -80, -115, -153, -255])
#all distances are in mm
points = np.zeros((25,2))
for xInd in range (5):
	for yInd in range (5):
		points[xInd*5+yInd] = (r[xInd], d[yInd])
counts = np.array([
	[91401,41859,17363,7052,2632],
	[193607,77909,30294,10794,3500],
	[243079,99569,36304,12632,4273],
	[367465,132203,45761,15225,5017],
	[612040,201294,60789,19417,6249]	])
y = counts.T.ravel()
numData = len(y)
dy= np.sqrt(y)

def fittedFunc(points, a, b, c):
	r2 = np.sqrt(points.T[0]**2 + (points.T[1]-b)**2)
	yCalc = a*np.exp(r2/c)/r2
	return yCalc
def fittedFunc2(x, a, c):
	yCalc = a*np.exp(-x/c)/x
	return yCalc

print("Parsed ", numData, " data points.")

guess_a = 300000000000000000000000000000000000000000000000000000000000000
guess_b = -400
guess_c = 5

[(a,b,c),((var_a,dummy, dummy),(dummy,var_b, dummy), (dummy, dummy, var_c))] = curve_fit(fittedFunc, points, y, sigma = dy,  absolute_sigma=True, check_finite=True) #p0=(guess_a, guess_b, guess_c))
#(var_a,dummy),(dummy,var_b) = pcov
da = np.sqrt(var_a)
db = np.sqrt(var_b)
dc = np.sqrt(var_c)

x = np.sqrt(points.T[0]**2 + (points.T[1]-b)**2)

print(points)
residual = y - fittedFunc2(x,a,c)
print(y)

print("a=",a,"+/-",da)
print("b=",b,"+/-",db)
print("c=",c,"+/-",dc)

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

