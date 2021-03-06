#!/home/oceanw/anaconda3/bin/python
#Picks five frames out of the original, and then plot them on the pole figure/Inverse Pole Figure.
#This approach has been rendered obsolete as I can simply plot every frame's pole figure by using the script WanderOutside.py.
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
		ax.plot(X, Y, color='black')#, lw=0.8

		x_an, y_an = getIPtip()
		
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
	fig.set_tight_layout(True)	#remove the black outline.

	global ax
	ax = plt.subplot(111)
	#ax = plt.Axes(fig, [0., 0., 1., 1.] )
	ax.axis('off')

	xlimits = expandAxisLimit(0, tan(pi/8) )
	ylimits = expandAxisLimit(0,0.366) #0.366 is calculated above in the wasted bit of script (currently line 93)
	ax.set_xlim(xlimits)
	ax.set_ylim(ylimits)

	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_aspect(0.366/tan(pi/8))

	BG()
	ax.set_title("Initial(dot) and final(cross) orientation of grains (relative to the pulling axis)")
	
	RotationMatrices = ReadR( "NewModel/1FrameRotationMatrices.txt" )
	RotationMatrices2= ReadR( "NewModel/90FrameRotationMatrices.txt")
	RotationMatrices3= ReadR("NewModel/180FrameRotationMatrices.txt")
	RotationMatrices4= ReadR("NewModel/270FrameRotationMatrices.txt")
	RotationMatrices5= ReadR("NewModel/360FrameRotationMatrices.txt")
	
	for n in range(len(RotationMatrices)):
		v48 = R_v(RotationMatrices[n])
		v48_2=R_v(RotationMatrices2[n])
		v48_3=R_v(RotationMatrices3[n])
		v48_4=R_v(RotationMatrices4[n])
		v48_5=R_v(RotationMatrices5[n])

		r = chooseIPpoint(v48)
		r2= chooseIPpoint(v48_2)
		r3= chooseIPpoint(v48_3)
		r4= chooseIPpoint(v48_4)
		r5= chooseIPpoint(v48_5)

		[Theta, Phi] = cartesian_spherical( r[0], r[1], r[2])
		[Theta2,Phi2]= cartesian_spherical(r2[0],r2[1],r2[2])
		[Theta3,Phi3]= cartesian_spherical(r3[0],r3[1],r3[2])
		[Theta4,Phi4]= cartesian_spherical(r4[0],r4[1],r4[2])
		[Theta5,Phi5]= cartesian_spherical(r5[0],r5[1],r5[2])

		R, Angle = stereographicProjector(Theta,Phi)
		X, Y = polar2D_xy(Angle, R)	
		R2, Angle2 = stereographicProjector(Theta2,Phi2)
		X2, Y2 = polar2D_xy(Angle2, R2)
		R3, Angle3 = stereographicProjector(Theta3,Phi3)
		X3, Y3 = polar2D_xy(Angle3, R3)
		R4, Angle4 = stereographicProjector(Theta4,Phi4)
		X4, Y4 = polar2D_xy(Angle4, R4)
		R5, Angle5 = stereographicProjector(Theta5,Phi5)
		X5, Y5 = polar2D_xy(Angle5, R5)

		ax.scatter(X, Y , color = 'black', marker = '.')
		#ax.plot(X2,Y2, markeredgecolor = 'black', markerfacecolor = 'none', marker='x')

		ax.annotate("",xy=(X2, Y2), xycoords='data',
			xytext=( X, Y ), textcoords='data',
			arrowprops=dict(arrowstyle="-",connectionstyle="arc3")
			)
		ax.annotate("",xy=(X3, Y3), xycoords='data',
			xytext=( X2, Y2 ), textcoords='data',
			arrowprops=dict(arrowstyle="-",connectionstyle="arc3")
			)
		ax.annotate("",xy=(X4, Y4), xycoords='data',
			xytext=( X3, Y3 ), textcoords='data',
			arrowprops=dict(arrowstyle="-",connectionstyle="arc3")
			)
		ax.annotate("",xy=(X5, Y5), xycoords='data',
			xytext=( X4, Y4 ), textcoords='data',
			arrowprops=dict(arrowstyle="->",connectionstyle="arc3")
			)
	plt.savefig("NewModel.png")
