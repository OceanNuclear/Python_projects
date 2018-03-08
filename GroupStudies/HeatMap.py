#!/home/oceanw/anaconda3/bin/python
import numpy as np
from scipy.constants import pi
import math
import matplotlib.pyplot as plt
#from matplotlib import Animation
from numpy import sin, cos, tan, arccos, arctan, sqrt
from quat import *
tau = pi*2
from scipy.interpolate import griddata
from matplotlib import cm
from generalLibrary import *



#Background plotting functions
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def plotCircle(cTheta, cPhi):
	Theta, Phi = DrawCircle(cTheta , cPhi , a=pi/2) #Theta has to be restricted to less than pi/2
	R, Angle = stereographicProjector(Theta, Phi)

	X, Y = polar2D_xy(Angle, R)
	ax.plot(X,Y, color='black', linestyle=':')
	return [R,Angle]

def plotDiag(phi):
	X,Y = Diag_xy(phi, 0,1)
	ax.plot( X,Y , color='black', linestyle=':')
	return

def plotDiag2(phi):
	X,Y = Diag_xy(phi, pi/6,1)
	ax.plot( X,Y , color='g')

def BG(CompletePoleFig=False):
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
		ax.plot(X, Y, color='black')

		s3 = sqrt(1/3)
		theta_an, phi_an = cartesian_spherical(s3,s3,s3)
		R_an, Angle_an = stereographicProjector(theta_an, phi_an)
		x_an, y_an = polar2D_xy( Angle_an, R_an )
		
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

	xlimits = expandAxisLimit(0, tan(pi/8) )
	ylimits = expandAxisLimit(0,0.366) #0.366 is calculated above in the wasted bit of script (currently line 93)
	ax.set_xlim(xlimits)
	ax.set_ylim(ylimits)

	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_aspect(0.366/tan(pi/8))

	BG(CompletePoleFig=False)

	RotationMatrices = ReadR("NewModel/120FrameRotationMatrices.txt")
	rho = Readrho("NewModel/DislocationDensityFrame120UnaxialNew.txt")

	RFinal, AngleFinal = [], []
	for n in range(len(RotationMatrices)):
		v48 = R_v(RotationMatrices[n])

		r = chooseIPpoint(v48)

		[Theta, Phi] = cartesian_spherical(r[0],r[1],r[2])

		RInt, AngleInt = stereographicProjector(Theta,Phi)
		RFinal.append(RInt); AngleFinal.append(AngleInt)
	X, Y = polar2D_xy(AngleFinal, RFinal)
	points = np.array([X,Y]).T

	x, y = np.mgrid[0:tan(pi/8):200j, 0:0.366:100j]

	z = griddata(points, rho, (x, y), method='cubic')
	#ax.scatter(X, Y , color = 'r', marker = 'o')

	graph = ax.pcolor(x,y,z, cmap=cm.jet)
	plt.title("Heat Map of Dislocation densities")

	plt.colorbar(graph, label = r"$m^{-2}$") #I think this is not part of ax, such that it is plotted outside of the figure.

	plt.show()

