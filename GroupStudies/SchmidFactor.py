#!/home/oceanw/anaconda3/bin/python
#Plots the schmid factor pole figure or inverse pole figure.
import numpy as np
from scipy.constants import pi
import math
import matplotlib.pyplot as plt
#from matplotlib import Animation
from matplotlib.colors import LinearSegmentedColormap
from numpy import sin, cos, tan, arccos, arctan, sqrt
from quat import *
tau = pi*2
from scipy.interpolate import griddata
from matplotlib import cm
from generalLibrary import *
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import time



#Background plotting functions
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def plotCircle(cTheta, cPhi):
	Theta, Phi = DrawCircle(cTheta , cPhi , a=pi/2) #Theta has to be restricted to less than pi/2
	R, Angle = stereographicProjector(Theta, Phi)

	X, Y = polar2D_xy(Angle, R)
	ax.plot(X,Y, color='black', linestyle='--', lw=0.8)
	return [R,Angle]

def plotDiag(phi):
	X,Y = Diag_xy(phi, 0,1)
	ax.plot( X,Y , color='black', linestyle='--', lw = 0.8)
	return

def plotDiag2(phi):
	X,Y = Diag_xy(phi, pi/6,1)
	ax.plot( X,Y , color='g')

def BG(CompletePoleFig=False):
	InversePoleFig= not CompletePoleFig
	if CompletePoleFig:
		for n in range (8):
			ax.plot(Diag_xy(n*tau/8)[0],Diag_xy(n*tau/8)[1], color = 'black', linestyle = '--', lw = 0.8)
			if not (n&0x1): #for even cases, plot the circles.
				plotCircle(pi/4, n*tau/8)
			'''
			if(n&0x1): #for odd cases, plot diagonals and vertices.
				plotDiag2(n*tau/8)
				PointPlotter(0.96 , n*tau/8)
			'''

	if InversePoleFig: #Plot the boundary of Inverse pole figure
		X,Y = InversePoleFigureLine()
		ax.plot(X, Y, color='black', lw=0.5)

		x_an, y_an = getIPtip()
		ax.annotate("[001]",	xy=[0,0], xycoords='data', ha='right',	color = 'black')
		ax.annotate("[101]",	xy=[tan(pi/8),0],xycoords='data',	color = 'black')
		ax.annotate("[111]",	xy=[x_an,y_an],	xycoords='data',	color = 'black')
	return



#Controller bit
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''

if __name__=="__main__":
	global fig
	fig = plt.figure()
	fig.set_tight_layout(True)

	global ax
	ax = plt.subplot(111)
	ax.axis('off')

	y_max = getIPtip()[1]

#	xlimits = expandAxisLimit(0, tan(pi/8) ,0.01)
#	ylimits = expandAxisLimit(0, y_max ,0.01) #y_max is calculated above in the wasted bit of script (currently line 93)

#	ax.set_xlim(xlimits)
#	ax.set_ylim(ylimits)

	ax.set_xlim([-1,1])	#
	ax.set_ylim([-1,1])	#

	ax.set_xticks([])
	ax.set_yticks([])

#	yxratio = y_max/tan(pi/8)
	yxratio = 1		#
	ax.set_aspect(yxratio)

	BG(CompletePoleFig=True)

	RFinal, AngleFinal = [], []

	vList = generateV(15000)	#of shape (N,3)			
	RotationMatrices = np.zeros(np.shape(vList))			
	rho = []
	print( "Random data generated, calcuating schmid factor for each point...")
	startTime = time.time()
	#RealData = True
	for n in range (len(RotationMatrices)):				
	#	if RealData:	v48 = R_v(RotationMatrices[n])
	#	else:		v48 = duplicate48Points(v[n][0], v[n][1], v[n][2])
	#	pointList = choosePFpoint(v48)
	#
	#	for upVector in pointList:
	#		[xl,yl,zl] = upVector
		[xl,yl,zl] = vList[n]
		[Theta, Phi] = cartesian_spherical(xl,yl,zl)
		RInt, AngleInt = stereographicProjector(Theta,Phi)
		RFinal.append(RInt)
		AngleFinal.append(AngleInt)

		schmidFactor = []
		for slipSystem in range (12):	#Loop through all 12 systems, and then plot the largest value among them.
			schmidFactor.append(schmidFinder(vList[n], slipSystem))
		rho.append(max(schmidFactor))
	Xco, Yco = polar2D_xy( AngleFinal, RFinal )

	points = np.array([Xco,Yco]).T
	print("Schmid factor calculation (excluding interpolation) took", time.time()-startTime)
	xRes = 500
	yRes = int(xRes*yxratio)

#	x, y = np.mgrid[0:tan(pi/8):(xRes*1j), 0:y_max:(yRes*1j)]
	x, y = np.mgrid[-1:1:(xRes*1j), -1:1:(yRes*1j)]		#
	z = griddata(points, rho, (x, y), method='cubic')

	#Plot the colormap itself.
	print("starting to plot the heat map...")
	startTime = time.time()
	graph = ax.pcolor(x,y,z, cmap=cm.jet)#, vmin = 7.5e10, vmax = 1.18e11)
	print("Time taken just to plot the main heat map =", time.time()-startTime)
	#Put white polygons outside of the inverse pole figure area to hide the irrelevant bits.
	xBound, yBound = InversePoleFigureLine()

	xBound = np.append( xBound[1:],-0.005)
	yBound = np.append( yBound[1:], 0 )
	yUpper = yBound-yBound+ getIPtip()[0] +0.01#the 0.01 bodges for the slight edge that appears on top 

#	ax.fill_between(xBound, yBound, yUpper, color = 'w')	

	#Plotting the non-pole Figure elements
	plt.title("Schmid Factor of one slip system in cubic crystals")
	plt.colorbar(graph)

	#plt.show()
	plt.savefig("SchmidFactorInversePoleFigure_OneSystemComplete.png")
