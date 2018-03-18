#!/home/oceanw/anaconda3/bin/python
import numpy as np
from scipy.constants import pi
import math
import matplotlib.pyplot as plt
from numpy import sin, cos, tan, arccos, arctan
from matplotlib import animation
tau = 2*pi



def getInput():
	Theta=np.deg2rad(input("Theta in degrees (0<=Theta<=90)="))
	if (Theta<0) or (Theta>(pi/2)): raise ValueError

	Phi = np.deg2rad( input("no. of degrees=") )
	return Theta , Phi

def stereographicProjector(Theta, Phi):
	return tan(Theta/2), Phi

def spherical_cartesian(theta, phi):
	x = sin(theta)*cos(phi)
	y = sin(theta)*sin(phi)
	z = cos(theta)
	return [x,y,z]

def cartesian_spherical( x, y, z):
	Theta = arccos(z)
	Phi = arctan(y/x)

	if (type(x)==list) or (type(x)==np.ndarray):
		for n in range (len(x)):
			if   np.sign(x[n])==-1:	Phi[n] += pi
			elif (np.sign(x[n])==0) and (np.sign(y[n])==-1):	Phi[n]=3*pi/2
			elif (np.sign(x[n])==0) and (np.sign(y[n])== 1):	Phi[n] = pi/2
			elif (np.sign(z[n])==0):	(Theta[n], Phi[n])= (0,0)

	else:
		if   np.sign(x)==-1:	Phi += pi
		elif (np.sign(x)==0) and (np.sign(y)==-1):	Phi=3*pi/2
		elif (np.sign(x)==0) and (np.sign(y)== 1):	Phi = pi/2
		elif (np.sign(z)==0):	(Theta, Phi)= (0,0)
	return [Theta, Phi]

def DrawCircle( cTheta, cPhi, a = pi/2 ): # a is the angular radius
	t = np.linspace(pi/2,3*pi/2,500)
	
	#Find the x,y,z coordinate of the centre
	[x0, y0, z0] = spherical_cartesian(cTheta,cPhi)

	#Find the x,y,z coordinates of the point directly below it, from which the plotting will start.
	[xt, yt, zt] = spherical_cartesian( cTheta+pi/2,cPhi )

	x1 = x0*cos(a) + sin(a)*sin(t)*(y0*zt-z0*yt) + sin(a)*cos(t)*y0*(xt*y0-yt*x0) - sin(a)*cos(t)*z0*(zt*x0-xt*z0)
	y1 = y0*cos(a) + sin(a)*sin(t)*(z0*xt-x0*zt) + sin(a)*cos(t)*z0*(yt*z0-zt*y0) - sin(a)*cos(t)*x0*(xt*y0-yt*x0)
	z1 = z0*cos(a) + sin(a)*sin(t)*(x0*yt-y0*xt) + sin(a)*cos(t)*x0*(zt*x0-xt*z0) - sin(a)*cos(t)*y0*(yt*z0-zt*y0)

	[Theta,Phi] = cartesian_spherical(x1, y1, z1)

	return Theta, Phi
'''
def plotCircle(f):
	Theta, Phi = DrawCircle(pi/3 , f*2*pi/100 , a=pi/4) #cTheta has to be restricted to less than pi/2
	R, Angle = stereographicProjector(Theta, Phi)
	print("drawing frame",f)

	ax.clear()
	ax.set_rlim([0,1])
	line = ax.plot(Angle, R)
	
	return line

'''
def plotCircle(cTheta, cPhi):
	Theta, Phi = DrawCircle(cTheta , cPhi , a=pi/2) #Theta has to be restricted to less than pi/2
	R, Angle = stereographicProjector(Theta, Phi)

	gridline = ax.plot(Angle, R, color='black', linestyle=':')
	return gridline

def drawHalfCircle(cTheta, cPhi, a = pi/2): # copy of the DrawCircle function above
	t = np.linspace(0.8*pi , 1.2*pi,100)
	
	#Find the x,y,z coordinate of the centre
	[x0, y0, z0] = spherical_cartesian(cTheta,cPhi)

	#Find the x,y,z coordinates of the point directly below it, from which the plotting will start.
	[xt, yt, zt] = spherical_cartesian( cTheta+pi/2,cPhi )

	x1 = x0*cos(a) + sin(a)*sin(t)*(y0*zt-z0*yt) + sin(a)*cos(t)*y0*(xt*y0-yt*x0) - sin(a)*cos(t)*z0*(zt*x0-xt*z0)
	y1 = y0*cos(a) + sin(a)*sin(t)*(z0*xt-x0*zt) + sin(a)*cos(t)*z0*(yt*z0-zt*y0) - sin(a)*cos(t)*x0*(xt*y0-yt*x0)
	z1 = z0*cos(a) + sin(a)*sin(t)*(x0*yt-y0*xt) + sin(a)*cos(t)*x0*(zt*x0-xt*z0) - sin(a)*cos(t)*y0*(yt*z0-zt*y0)

	[Theta,Phi] = cartesian_spherical(x1, y1, z1)
	R, Angle = stereographicProjector(Theta, Phi)
	ax.plot(Angle, R, color = 'b')
	return R, Angle

def plotDiag(phi):
	gridline = ax.plot([phi,]*2, [0,1], color='black', linestyle=':')
	return gridline

def sphereCoveringCurve():
	n=5
	Theta = np.linspace(0,pi/2, 400)
	Phi = np.linspace(0, n*tau, 400)
	return np.array([Theta, Phi]).T

def duplicatePoints(x0,y0,z0): #Find the equivalent points relative to the z axis.
	if (z0<0): raise ValueError
	[x0,y0] = np.array([x0,y0])
	x = []
	y = []
	z = [z0,]*8
	
	for n in range (4):
		x.append((-1)**(n>>1) *x0); y.append((-1)**(n>>0) *y0)
		x.append((-1)**(n>>1) *y0); y.append((-1)**(n>>0) *x0)	

	return np.array([x,y,z]).T

def chooseIPpoint(arrayOf8pt):
	for r in arrayOf8pt:
		if np.sign(r[0])>=0:
			if np.sign(r[1])>=0:
				if (r[0]>=r[1]):
					return r


if __name__=="__main__":
	global fig
	fig = plt.figure()

	duration = 16
	fps = 25

	global ax
	ax = plt.subplot(111, projection = 'polar')
	ax.set_rlim([0,1])
	ax.set_rticks([])
	for n in range (4):
		plotCircle(pi/4, n*pi/2)
		#R, Phi = drawHalfCircle(pi/4, n*pi/2)

	global line
	line = []

	def plotBG():
		ax.clear()
		BG = []
		for n in range (4):
			BG.append(plotCircle(pi/4, n*pi/2))
			#R, Phi = drawHalfCircle(pi/4, n*pi/2)
		for n in range (8):
			for n in range (8):
				BG.append( plotDiag(n*pi/4) )
		print("init_func is being called.")
		return line

	def Plot8Point(f):
		[Theta, Phi] = sphereCoveringCurve()[f]
		print("animating frame no.", f+1)
		x0,y0,z0 = spherical_cartesian(Theta,Phi)

		Listof8 = (duplicatePoints(x0,y0,z0))
		[x,y,z] = chooseIPpoint(Listof8)
		[Theta, Phi] = cartesian_spherical(x,y,z)
	
		R, Angle = stereographicProjector(Theta,Phi)
		line2 = ax.scatter(Angle, R, color='r', marker='o', zorder=100)
		return line2,


	anim = animation.FuncAnimation(fig, Plot8Point, init_func=plotBG, frames = int(3), interval = 40, blit=True)
	anim.save( "movingCirlcle6.mp4", fps = 25, extra_args=['-vcodec', 'libx264'])
