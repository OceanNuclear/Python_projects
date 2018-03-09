#!/home/oceanw/anaconda3/bin/python
from numpy import sin, cos, tan, arccos, arctan, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
from quat import *
tau = 2*pi
#This file does not contain reading functions, as it simply does the job of mathematical processing.



#General functions to switch coordinates.
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def polar2D_xy(Angle, R):
	return R*cos(Angle), R*sin(Angle)

def stereographicProjector(Theta, Phi):
	return tan(Theta/2), Phi

def spherical_cartesian(theta, phi):
	x = sin(theta)*cos(phi)
	y = sin(theta)*sin(phi)
	z = cos(theta)
	return [x,y,z]

def cartesian_spherical(x, y, z):
	x,y,z = np.array([x,y,z], dtype=float) #change the data type to the desired format

	Theta = arccos(z)
	Phi = arctan(np.divide(y,x))
	Phi = np.nan_to_num(Phi)
	Phi+= np.array( (np.sign(x)-1), dtype=bool)*pi #if x is positive, then phi is on the RHS of the circle; vice versa.
	return np.array([Theta, Phi])



#Plotters
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def expandAxisLimit(Min, Max, fraction=0.1):
	offSet = fraction*(Max-Min)
	return [Min-offSet, Max+offSet]

def Diag_xy(phi, r_lower=0, r_upper=1):
	return polar2D_xy([phi,]*2, [r_lower, r_upper])

def point_xy(x,y,z): #This function is created for convenience only.
	theta_an, phi_an = cartesian_spherical(x,y,z)
	R_an, Angle_an = stereographicProjector(theta_an, phi_an)
	x_an, y_an = polar2D_xy( Angle_an, R_an )
	return x_an, y_an

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

def drawHalfCircle(cTheta, cPhi, a = pi/2): # copy of the DrawCircle function above
	t = np.linspace( pi , 1.1959135*pi,100)#Need to prove that it's 1.1959.
	
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
	return R, Angle

def InversePoleFigureLine():
	R , Angle = drawHalfCircle( pi/4,pi )

	EdgeR = 0
	EdgeA = 0
	EdgeR = np.append(EdgeR, R)
	EdgeA = np.append(EdgeA, Angle)
	EdgeR = np.append(EdgeR, 0)
	EdgeA = np.append(EdgeA, pi/4)

	X,Y = polar2D_xy(EdgeA,EdgeR)
	return [X,Y]



#Main functions
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
'''
def PointPlotter(X, Y):
	ax.scatter(X, Y, color='r', marker='o', zorder=100)
	return
'''

def naturalNum(Index):
	if np.sign(Index)!=-1: return Index
	else: return 0

def normalize(r):
	return r/RootSumSq(r)

def deNormalize(v):
	return v/(2*abs(v[2]))

def R_v(R):
	Z = np.array([0,0,1]) #assume pulling axis is the z axis.
	[x,y,z] = np.linalg.multi_dot([R,Z]) #see where does the pulling axis lands.
	#Pick the vector that juts out of the top face:
	return duplicate48Points(x,y,z)

def duplicate48Points(x0,y0,z0): #Find the equivalent points by permuating the indices and adding negative signs.
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
		if ( sum(np.sign(r)>-np.ones(3))==3# all components are non-negative.
			) and ( abs(r[0])>=abs(r[1])
			) and ( abs(r[0])<=abs(r[2])
			) and ( abs(r[1])<=abs(r[2]) ):
			return r

def getIPpointID(arrayOf48pt):
	for n in range (len(arrayOf48pt)):
		if ( sum(np.sign(arrayOf48pt[n])>-np.ones(3))==3# all components are non-negative.
			) and ( abs(arrayOf48pt[n][0])>=abs(arrayOf48pt[n][1])
			) and ( abs(arrayOf48pt[n][0])<=abs(arrayOf48pt[n][2])
			) and ( abs(arrayOf48pt[n][1])<=abs(arrayOf48pt[n][2]) ):
			return n

def choosePFpoint(arrayOf48pt):
	pointList = []
	for r in arrayOf48pt:
		if ( np.sign(r[2])>-1): #z is non-zero
			pointList.append(r)
	return pointList



'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
#File reading functions
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

def Readrho(fileName):
	f = open( str(fileName))
	rho = f.readlines()
	rho = np.array(rho, dtype = float)
	return rho



#Generators
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
#sphereFillingCurve
def sphereFillingCurve( m,n , duration, fps=25):
	r = np.linspace(0,1,duration*fps)
	theta= sin(r) *pi
	phi = r*n*tau
	r = r*tau
	return np.array([r, theta, phi], dtype=float).T
