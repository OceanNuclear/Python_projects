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
	Phi = arctan(y/x) + ((np.sign(x)-1)/2)*pi #if x is positive, then phi is on the RHS of the circle; vice versa.

	return [Theta, Phi]

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
		if ( sum(np.sign(r)>-np.ones(3))==3# all components are non-negative.
			) and ( abs(r[0])>=abs(r[1])
			) and ( abs(r[0])<=abs(r[2])
			) and ( abs(r[1])<=abs(r[2]) ):
			return r

def getIPpointID(arrayOf48pt):
	for n in range (len(arrayOf48pt)):
		if ( sum(np.sign(arrayOf48pt[n])>-np.ones(arrayOf48pt[n]))==3# all components are non-negative.
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



'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
#Generators
#sphereFillingCurve
def sphereFillingCurve( m,n , duration, fps=25):
	r = np.linspace(0,1,duration*fps)
	theta= sin(r) *pi
	phi = r*n*tau
	r = r*tau
	return np.array([r, theta, phi], dtype=float).T
