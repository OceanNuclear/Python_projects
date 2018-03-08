#!/home/oceanw/anaconda3/bin/python
from numpy import sin, cos, tan, arccos, arctan, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
from quat import *
tau = 2*pi
from generalLibrary import *



#Background plotting functions
def DrawCircle( cTheta, cPhi, a = pi/2 ): # a is the angular radius
	t = np.linspace(0,tau,400)
	
	#Find the x,y,z coordinate of the centre
	[x0, y0, z0] = spherical_cartesian(cTheta,cPhi)

	#Find the x,y,z coordinates of the point directly below it, from which the plotting will start.
	[xt, yt, zt] = spherical_cartesian( cTheta+pi/2,cPhi )

	x1 = x0*cos(a) + sin(a)*sin(t)*(y0*zt-z0*yt) + sin(a)*cos(t)*y0*(xt*y0-yt*x0) - sin(a)*cos(t)*z0*(zt*x0-xt*z0)
	y1 = y0*cos(a) + sin(a)*sin(t)*(z0*xt-x0*zt) + sin(a)*cos(t)*z0*(yt*z0-zt*y0) - sin(a)*cos(t)*x0*(xt*y0-yt*x0)
	z1 = z0*cos(a) + sin(a)*sin(t)*(x0*yt-y0*xt) + sin(a)*cos(t)*x0*(zt*x0-xt*z0) - sin(a)*cos(t)*y0*(yt*z0-zt*y0)

	[Theta,Phi] = cartesian_spherical(x1, y1, z1)

	return Theta, Phi

def plotCircle(cTheta, cPhi):
	Theta, Phi = DrawCircle(cTheta , cPhi , a=pi/2) #Theta has to be restricted to less than pi/2
	R, Angle = stereographicProjector(Theta, Phi)

	X, Y = polar2D_xy(Angle, R)
	ax.plot(X,Y, color='black', linestyle=':')
	return [R,Angle]

def drawHalfCircle(cTheta, cPhi, a = pi/2): # copy of the DrawCircle function above
	t = np.linspace( pi , 1.19591*pi,100)
	
	#Find the x,y,z coordinate of the centre
	[x0, y0, z0] = spherical_cartesian(cTheta,cPhi)

	#Find the x,y,z coordinates of the point directly below it, from which the plotting will start.
	[xt, yt, zt] = spherical_cartesian( cTheta+pi/2,cPhi )

	x1 = x0*cos(a) + sin(a)*sin(t)*(y0*zt-z0*yt) + sin(a)*cos(t)*y0*(xt*y0-yt*x0) - sin(a)*cos(t)*z0*(zt*x0-xt*z0)
	y1 = y0*cos(a) + sin(a)*sin(t)*(z0*xt-x0*zt) + sin(a)*cos(t)*z0*(yt*z0-zt*y0) - sin(a)*cos(t)*x0*(xt*y0-yt*x0)
	z1 = z0*cos(a) + sin(a)*sin(t)*(x0*yt-y0*xt) + sin(a)*cos(t)*x0*(zt*x0-xt*z0) - sin(a)*cos(t)*y0*(yt*z0-zt*y0)

	[Theta,Phi] = cartesian_spherical(x1, y1, z1)
	R, Angle = stereographicProjector(Theta, Phi)

	X, Y = polar2D_xy(Angle, R)
	ax.plot(X,Y, color = 'b')
	return R, Angle

def plotDiag(phi):
	X,Y=polar2D_xy([phi,]*2, [0,1])
	ax.plot( X,Y , color='black', linestyle=':')
	return

def plotDiag2(phi):
	X,Y=polar2D_xy([phi,]*2, [pi/6,1])
	ax.plot( X,Y , color='g')

def BG(CompletePoleFig=False):
	for n in range (3):
		plotCircle(pi/4, n*tau/4)
	R, Phi = drawHalfCircle(pi/4, pi)

	EdgeR = 0
	EdgeA = 0
	EdgeR = np.append(EdgeR, R)
	EdgeA = np.append(EdgeA, Phi)
	EdgeR = np.append(EdgeR, 0)
	EdgeA = np.append(EdgeA, pi/4)

	X,Y = polar2D_xy(EdgeA,EdgeR)
	ax.plot(X, Y)

	for n in range (2):
		plotDiag(n*tau/8)
		'''
		if(n&0x1): #If n is odd:
			plotDiag2(n*tau/8)
			PointPlotter(0.96 , n*tau/8)
		'''
	if CompletePoleFig:
		for n in range (2,8):
			plotDiag(n*tau/8)
			'''
			if(n&0x1): #If n is odd:
				plotDiag2(n*tau/8)
				PointPlotter(0.96 , n*tau/8)
			'''
	ax.set_title("Initial(red) and final(blue) orientation of grains (relative to the pulling axis)")

	s3 = sqrt(1/3)
	theta_an, phi_an = cartesian_spherical(s3,s3,s3)
	R_an, Angle_an = stereographicProjector(theta_an, phi_an)
	x_an, y_an = polar2D_xy( R_an, Angle_an)

	ax.annotate("[001]",	xy=[0,0],	color = 'black')
	ax.annotate("[101]",	xy=[0,tan(pi/8)],color= 'black')
	ax.annotate("[111]",	xy=[x_an,y_an], color = 'black')
	'''
	ax.annotate("and the four corners",	xy=[pi/4 -np.deg2rad(30), 0.44 ],color = 'r'	)
	ax.annotate("of the top half of the cube",xy=[pi/4 -np.deg2rad(40),0.43],color = 'black')
	'''
	return

#Controller bit
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
if __name__=="__main__":
	xdim = 1280
	ydim = 720
	DPI = 80
	global fig
	fig = plt.figure()
	fig.set_tight_layout(True)
	fig.patch.set_visible(False)

	#fig.set_size_inches( int(xdim/DPI), int(ydim/DPI) )

	global ax
	#ax = plt.Axes(fig, [0., 0., 1., 1.] )
	ax = plt.subplot(111)
	ax.axis('off')
	ax.set_xlim([0,tan(pi/8)])
	ax.set_ylim([0,0.366])
	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_aspect(0.366/tan(pi/8))

	BG()

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

		ax.annotate("",
			xy=(X2, Y2), xycoords='data',
			xytext=(X, Y), textcoords='data',
			arrowprops=dict(arrowstyle="->",
				connectionstyle="arc3"),
				)
	plt.show()
