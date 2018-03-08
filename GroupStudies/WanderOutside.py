#!/home/oceanw/anaconda3/bin/python
from numpy import sin, cos, tan, arccos, arctan, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
from quat import *
tau = 2*pi
from generalLibrary import *
debug = True
normal= not debug



#Background plotting functions
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
		ax.plot(X, Y, color='black')#, lw=0.8

		s3 = sqrt(1/3)
		theta_an, phi_an = cartesian_spherical( s3,s3,s3 )
		R_an, Angle_an = stereographicProjector(theta_an, phi_an)
		x_an, y_an = polar2D_xy( Angle_an, R_an )
		
		ax.annotate("[001]",	xy=[0,0], xycoords='data', ha='right',	color = 'black')
		ax.annotate("[101]",	xy=[tan(pi/8),0],xycoords='data',	color = 'black')
		ax.annotate("[111]",	xy=[x_an,y_an],	xycoords='data',	color = 'black')
		'''
		ax.annotate("and the four corners",	xy=[pi/4 -np.deg2rad(30), 0.44 ],color = 'r'	)
		ax.annotate("of the top half of the cube",xy=[pi/4 -np.deg2rad(40),0.43],color = 'black')
		'''
	return

#Controller bit
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
if __name__=="__main__":
	global fig
	fig = plt.figure()
	fig.set_tight_layout(True)

	global ax
	ax = plt.subplot(111)
	#ax = plt.Axes(fig, [0., 0., 1., 1.] )
	ax.axis('off')

	xlimits = expandAxisLimit(0, tan(pi/8) , 3)
	ylimits = expandAxisLimit(0,0.366, 3) #0.366 is calculated above in the wasted bit of script (currently line 93)
	ax.set_xlim(xlimits)
	ax.set_ylim(ylimits)
	#ax.set_xlim([0, tan(pi/8)])
	#ax.set_ylim([0,0.366])

	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_aspect(0.366/tan(pi/8))

	BG()

	RotationMatrices = ReadR("NewModel/1FrameRotationMatrices.txt")
	numGrains = len(RotationMatrices)
	ID = np.ones(numGrains, dtype=int)*48#The max has range=(0,47), so in theory when ID has been introduced none of them should remain as 48.

	for grain in range(numGrains):
		v48 = R_v(RotationMatrices[grain])
		ID[grain] = getIPpointID(v48)

		r = v48[ID[grain]]
		[Theta, Phi] = cartesian_spherical( r[0], r[1], r[2])
		R, Angle = stereographicProjector(Theta,Phi)
		X, Y = polar2D_xy(Angle, R)

		ax.plot(X, Y , marker = 'o', markerfacecolor='none', markeredgecolor='black')
		'''
		ax.annotate("",xy=(X2, Y2), xycoords='data',
			xytext=( X, Y ), textcoords='data',
			arrowprops=dict(arrowstyle="-",connectionstyle="arc3")
			)
		'''
	numFrame = 397
	ax.set_title("Evolution of grains orientations up to frame"+str(numFrame)+"out of 397 frames")
	x_line = np.zeros([numGrains,numFrame])
	y_line = np.zeros([numGrains,numFrame])

	distance=np.zeros([numGrains,numFrame])

	thresholdDistance=0.2
	for frame in range (numFrame):
		fileName = "NewModel/"+str(frame+1)+"FrameRotationMatrices.txt"
		UpdatedMatrices = ReadR(fileName)
		print("Calculating for frame=", '{:0=3d}'.format(frame+1),"/", numFrame)
		for grain in range(numGrains):
			r = R_v(UpdatedMatrices[grain])[ID[grain]]
			[Theta, Phi] = cartesian_spherical( r[0], r[1], r[2])
			R, Angle = stereographicProjector(Theta,Phi)
			X, Y = polar2D_xy(Angle, R)
			if debug:
				x_line[grain][frame] = X
				y_line[grain][frame] = Y

				dx = X - x_line[grain][frame-1]
				dy = Y - y_line[grain][frame-1]
				distance[grain][frame] = RootSumSq([ dx , dy ])
				if distance[grain][frame]>thresholdDistance:
					print("Anomaly detected at grain",grain,"of frame",frame+1,
					"! This is because a distance of",'{:0=3.3f}'.format(distance[grain][frame]),
					"is measured between frames.")
					print("Previous frame is plotted at x=",x_line[grain][frame-1],
					"y=",y_line[grain][frame-1],
					"on the polar coordinate system, transformed to xy coordinates.")
					print(" Current frame is plotted at x=", x_line[grain][frame],
					"y=",y_line[grain][frame],
					"on the polar coordinate system, transformed to xy coordinates.")

	for grain in range(numGrains):
		ax.plot(x_line[grain], y_line[grain], color='black', lw=0.8)
	#plt.show()
	#plt.savefig("GrainOrientationEvolution_ToFrame"+str(numFrame)+".png")
