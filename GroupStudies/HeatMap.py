#!/home/oceanw/anaconda3/bin/python
#Plots the heat map of a pole figure or Inverse pole figure
#(depending on user requirement)
#And then save the figure.
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
def plotCircle(cTheta, cPhi):	#plot the curvy bit of the pole figure.
	Theta, Phi = DrawCircle(cTheta , cPhi , a=pi/2) #Theta has to be restricted to less than pi/2
	R, Angle = stereographicProjector(Theta, Phi)

	X, Y = polar2D_xy(Angle, R)
	ax.plot(X,Y, color='black', linestyle=':')
	return [R,Angle]

def plotDiag(phi):	#plot the 8 diagonal lines on the pole figure for a given phi.
	X,Y = Diag_xy(phi, 0,1)
	ax.plot( X,Y , color='black', linestyle=':')
	return

def plotDiag2(phi):
	X,Y = Diag_xy(phi, pi/6,1)
	ax.plot( X,Y , color='g')

def BG(CompletePoleFig=False):	#use =True instead to plot the complete pole figure.
	InversePoleFig= not CompletePoleFig
	if CompletePoleFig:
		for n in range (8):
			ax.plot(Diag_xy(n*pi/8), color = black, linestyle = ':')
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
	fig.set_tight_layout(True)	#needed to remove the black outline.

	global ax
	ax = plt.subplot(111)
	ax.axis('off')

	y_max = getIPtip()[1]

	xlimits = expandAxisLimit(0, tan(pi/8) ,0.01)
	ylimits = expandAxisLimit(0, y_max ,0.01) #y_max is calculated above in the wasted bit of script (currently line 93)

	ax.set_xlim(xlimits)
	ax.set_ylim(ylimits)

	ax.set_xticks([])
	ax.set_yticks([])

	yxratio = y_max/tan(pi/8)
	ax.set_aspect(yxratio)

	BG(CompletePoleFig=False)

	#frameNumstr=str(360)
	frameNumstr = "arbitraryData"
	print("Reading and plotting data for frame", frameNumstr)
	RFinal, AngleFinal = [], []
	'''
	v = [[0., 0., 1.],
	[0.,         0.31622777, 0.9486833, ],
	[0.,         0.4472136,  0.89442719,],
	[0.,         0.70710678, 0.70710678,],
	[-0.14002801,  0.14002801,  0.98019606,],
	[-0.19245009,  0.19245009,  0.96225045,],
	[-0.30151134,  0.30151134,  0.90453403,],
	[-0.40824829,  0.40824829,  0.81649658,],
	[-0.57735027,  0.57735027,  0.57735027,],
	[-0.33333333,  0.66666667,  0.66666667,],
	[-0.22941573,  0.6882472,   0.6882472, ]]
	rho = [0,0,2,4,1,1.5,2,3,4,5,5]
	RotationMatrices = np.zeros(np.shape(v))
	'''
	RealData = True
#	RotationMatrices = ReadR("NewModel/"+frameNumstr+"FrameRotationMatrices.txt")
#	rho = Readrho("NewModel/DislocationDensityFrame"+frameNumstr+"UnaxialNew.txt")

	RotationMatrices = ReadR("NewModel/dis5.txt")
	rho = Readrho("NewModel/dis5dis.txt")

	#Duplicate each point by 24 times:
	rho = (np.array([rho,]*24).T).ravel()

	for n in range (len(RotationMatrices)):
		if RealData:	v48 = R_v(RotationMatrices[n])
		else:		v48 = duplicate48Points(v[n][0], v[n][1], v[n][2])
		pointList = choosePFpoint(v48)

		for upVector in pointList:
			[xl,yl,zl] = upVector
			[Theta, Phi] = cartesian_spherical(xl,yl,zl)

			RInt, AngleInt = stereographicProjector(Theta,Phi)
			RFinal.append(RInt)
			AngleFinal.append(AngleInt)
	Xco, Yco = polar2D_xy( AngleFinal, RFinal )

	points = np.array([Xco,Yco]).T

	xRes = 500	#Define the horizonal resolution
	yRes = int(xRes*yxratio)
	x, y = np.mgrid[0:tan(pi/8):(xRes*1j), 0:y_max:(yRes*1j)]

	z = griddata(points, rho, (x, y), method='linear')	#Use cubic for smoother interpolation(warning: unexpected hotspots may result)

	##takes in the (x_data, y_data), z(x_data,y_data), and interpolated data points.
	#ax.scatter(points[:,0], points[:,1] , color = 'r', marker = 'o')

	#Plot the colormap itself.
	print("starting to plot the heat map...")
	startTime = time.time()
	graph = ax.pcolor(x,y,z, cmap=cm.jet)#, vmin = 7.5e10, vmax = 1.18e11)
	ax.scatter(Xco, Yco, color='black')
	print("Time taken just to plot the main heat map =", time.time()-startTime)
	#The five lines below put white polygons outside of the inverse pole figure area to hide the irrelevant bits.
	xBound, yBound = InversePoleFigureLine()

	xBound = np.append( xBound[1:],-0.01)
	yBound = np.append( yBound[1:], 0 )
	yUpper = yBound-yBound+ getIPtip()[0] +0.01#the 0.01 bodges for the slight edge that appears on top 

	ax.fill_between(xBound, yBound, yUpper, color = 'w')


	#Plotting the non-pole Figure elements
	plt.title("Heat map of dislocation densities at frame "+frameNumstr)
	plt.colorbar(graph, label = r"$m^{-2}$") #I think this is not part of ax, such that it is plotted outside of the figure.

	plt.show()
	#plt.savefig("point1.png")
	#plt.savefig("HeatMappable/Frame"+frameNumstr+"DislocationDensity.png")
	#plt.savefig("HeatMappable/Arbitrary Dislocation_OceansCode.png")
