#!/home/oceanw/anaconda3/bin/python
import numpy as np
from scipy.constants import pi
import math
import matplotlib.pyplot as plt
from numpy import sin, cos, tan, arccos, arctan, sqrt
from quat import *
tau = pi*2
from quat import *
from matplotlib import animation



#General functions to switch coordinates.
def polar2D_xy(Angle, R):
	return R*cos(Angle), R*sin(Angle)

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

	if (type(x)==list) or (type(x)==np.ndarray):#If data type inputted is a list:
		for n in range (len(x)):
			if   np.sign(x[n])==-1:	Phi[n] += pi
			elif (np.sign(x[n])==0) and (np.sign(y[n])==-1):	Phi[n]=3*pi/2
			elif (np.sign(x[n])==0) and (np.sign(y[n])== 1):	Phi[n] = pi/2
			elif (z[n]==1):	(Theta[n], Phi[n])= (0,0)

	else: # i.e. all of them has len == 1:
		if   np.sign(x)==-1:	Phi += pi
		elif (np.sign(x)==0) and (np.sign(y)==-1):	Phi=3*pi/2
		elif (np.sign(x)==0) and (np.sign(y)== 1):	Phi = pi/2
		elif (z==1):	(Theta, Phi)= (0,0)

	return [Theta, Phi]



#Background plotting functions
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
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

def BG():
	for n in range (3):
		plotCircle(pi/4, n*tau/4)

	R, Phi = drawHalfCircle(pi/4, pi)

	EdgeR, EdgeA = 0, 0

	EdgeR = np.append(EdgeR, R)
	EdgeA = np.append(EdgeA, Phi)

	EdgeR = np.append(EdgeR, 0)
	EdgeA = np.append(EdgeA, pi/4)

	X,Y = polar2D_xy(EdgeA,EdgeR)
	ax.plot(X, Y)

	for n in range (8):
		plotDiag(n*tau/8)
		'''
		if(n&0x1): #If n is odd:
			plotDiag2(n*tau/8)
			PointPlotter(0.96 , n*tau/8)
		'''
	ax.set_title(r"Rotation around the $\frac{\pi}{4}$ axis")#
	"""
	ax.annotate("These edges corresponds",	xy =[pi/4 , 0.52]		,color = 'black')
	ax.annotate("to the 4 full edges,",	xy=[pi/4 -np.deg2rad(10), 0.48 ],color = 'b'	)
	ax.annotate("the 4 half edges,",	xy=[pi/4 -np.deg2rad(20), 0.455],color = 'g'	)
	ax.annotate("and the four corners",	xy=[pi/4 -np.deg2rad(30), 0.44 ],color = 'r'	)
	ax.annotate("of the top half of the cube",xy=[pi/4 -np.deg2rad(40),0.43],color = 'black')
	"""
	return []



#Main functions
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
'''
def PointPlotter(X, Y):
	ax.scatter(X, Y, color='r', marker='o', zorder=100)
	return
'''
def deNormalize(v):
	return v/(abs(v[2]))

def R_v(R):
	R_inv = np.linalg.pinv(R)
	I = np.identity(3)
	Z = I[2] #assume pulling axis is the z axis.

	[x,y,z] = np.linalg.multi_dot([R_inv,Z]) #see where does the pulling axis lands.
	#Pick the vector that juts out of the top face:
	return duplicate48Points(x,y,z)

def duplicate48Points(x0,y0,z0): #Find the equivalent points relative to the z axis.
	[x0,y0] = np.array([x0,y0])
	x,y,z = [], [], []
	
	for n in range (8):
		x.append((-1)**(n>>2) *x0); y.append((-1)**(n>>1) *y0); z.append((-1)**(n>>0) *z0)
		x.append((-1)**(n>>2) *y0); y.append((-1)**(n>>1) *x0); z.append((-1)**(n>>0) *z0)
		x.append((-1)**(n>>2) *x0); y.append((-1)**(n>>1) *z0); z.append((-1)**(n>>0) *y0)
		x.append((-1)**(n>>2) *y0); y.append((-1)**(n>>1) *z0); z.append((-1)**(n>>0) *x0)
		x.append((-1)**(n>>2) *z0); y.append((-1)**(n>>1) *x0); z.append((-1)**(n>>0) *y0)
		x.append((-1)**(n>>2) *z0); y.append((-1)**(n>>1) *y0); z.append((-1)**(n>>0) *x0)

	return np.array([x,y,z]).T

def chooseIPpoint(arrayOf48pt):
	for r in arrayOf48pt:
		if ( sum(np.sign(r)>-np.ones(3))==3) and ( abs(r[0])>=abs(r[1]) ) and ( abs(r[0])<=abs(r[2]) ) and ( abs(r[1])<=abs(r[2]) ):
			return r

#Rotation matrix reader
def ReadR(fileName):
	f = open( str(fileName) )
	Matrices = f.readlines()
	f.close()
	Matrices = np.reshape(Matrices, [-1,3])
	Matrix = []
	for n in range (len(Matrices)):
		Matrix.append(	[np.array(Matrices[n][0].split() , dtype=float),
				np.array( Matrices[n][1].split() , dtype=float),
				np.array( Matrices[n][2].split() , dtype=float) ] )
	#np.shape(Matrix) ==(n,3,3)
	return Matrix

def sphereFillingCurve( m,n , duration, fps):
	r = np.linspace(0,1,duration*fps)
	theta= sin(r) *pi
	phi = r*n*tau
	r = r*tau
	return np.array([r, theta, phi], dtype=float).T


#Controller bit
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''

if __name__=="__main__":
	global fig
	fig = plt.figure()
	#fig.add_axes(ax)
	duration = 5
	fps = 25

	global ax
	ax = plt.subplot(111)
	ax.set_xlim([0,tan(pi/8)])
	ax.set_ylim([0,0.366])
	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_aspect(0.366/tan(pi/8))
	#line, = ax.plot([0,0+0.01], [0,0+0.01] , color = 'r', marker = 'o')
	(line,) = ax.plot([0],[0], color = 'r', marker = 'o')

	BG()

	#RotationMatrices = ReadR("Matrices/1FrameRotationMatrices.txt")
	#RotationMatrices2= ReadR("Matrices/128FrameRotationMatrices.txt")
	
	curve = sphereFillingCurve(1, 6, duration, fps)

	def draw(f):
		[theta, theta_axis, phi_axis] = curve[f]
		x_axis, y_axis, z_axis = spherical_cartesian(pi/2, pi/4)
		s = sin(theta/2)
		q = [cos(theta/2), s*x_axis, s*y_axis, s*z_axis]
		print("converting quaternion of frame",f+1)
		R = QuatToR(q)
		v48 = R_v(R)

		r = chooseIPpoint(v48)

		[Theta, Phi] = cartesian_spherical(r[0],r[1],r[2])

		R, Angle = stereographicProjector(Theta,Phi)
		X, Y = polar2D_xy(Angle, R)
		line.set_data([X],[Y])

		return (line,)

	anim = animation.FuncAnimation(fig, draw, init_func = BG, frames = int(fps*duration), interval = 40, blit=True)
	anim.save( 'XYAXIS.mp4', fps = 25, extra_args=['-vcodec', 'libx264'])
