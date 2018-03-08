#!/home/oceanw/anaconda3/bin/python
from numpy import sin, cos, tan, arccos, arctan, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
from quat import *
tau = 2*pi
from generalLibrary import *
debug = False
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
		ax.plot(X, Y, color='black')

		s3 = sqrt(1/3)
		theta_an, phi_an = cartesian_spherical(s3,s3,s3)

		print(theta_an,phi_an)
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

	xlimits = expandAxisLimit(0, tan(pi/8) )
	ylimits = expandAxisLimit(0,0.366) #0.366 is calculated above in the wasted bit of script (currently line 93)
	ax.set_xlim(xlimits)
	ax.set_ylim(ylimits)
	#ax.set_xlim([0, tan(pi/8)])
	#ax.set_ylim([0,0.366])

	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_aspect(0.366/tan(pi/8))

	BG()
	ax.set_title("Initial(red) and final(blue) orientation of grains (relative to the pulling axis)")
	
	[x_red, y_red, z_red] = normalize([1,1,1])
	x_dot, y_dot = point_xy(x_red, y_red, z_red)
	ax.plot([x_dot], [y_dot], 'rx')

	RotationMatrices = ReadR("Matrices/1FrameRotationMatrices.txt")
	RotationMatrices2= ReadR("Matrices/128FrameRotationMatrices.txt")
	
	for n in range(len(RotationMatrices)):
		v48 = R_v(RotationMatrices[n])
		v48_2=R_v(RotationMatrices2[n])

		r = chooseIPpoint(v48)
		r2= chooseIPpoint(v48_2)

		[Theta, Phi] = cartesian_spherical(r[0],r[1],r[2])
		[Theta2,Phi2]= cartesian_spherical(r2[0],r2[1],r2[2])

		R, Angle = stereographicProjector(Theta,Phi)
		X, Y = polar2D_xy(Angle, R)
	
		R2, Angle2 = stereographicProjector(Theta2,Phi2)
		X2, Y2 = polar2D_xy(Angle2, R2)

		ax.scatter(X, Y , color = 'r', marker = 'o')
		ax.plot(X2,Y2, markeredgecolor = 'b', markerfacecolor = 'none', marker='o')

		ax.annotate("",xy=(X2, Y2), xycoords='data',
			xytext=( X, Y ), textcoords='data',
			arrowprops=dict(arrowstyle="-",connectionstyle="arc3")
			)
	plt.show()
