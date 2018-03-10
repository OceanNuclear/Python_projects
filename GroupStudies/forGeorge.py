#!/home/oceanw/anaconda3/bin/python
from numpy import arccos, arctan, pi
from numpy import sin, cos, tan, sqrt
import numpy as np
#tau = 2*pi
from quat import *

#This file is written for George's reference, from which he can translate the file into Mtex.



def R_v(R):
	Z = np.array([0,0,1])
	[x,y,z] = np.linalg.multi_dot([R,Z]) #Do a matrix multiplication, i.e. applying the matrix on the Z (i.e. pulling) axis,
	#Thus see where does the pulling axis lands
	return [x,y,z]

def cartesian_spherical(x, y, z): #input a unit vector, pointing in any direction in 3D space.
	x,y,z = np.array([x,y,z], dtype=float) #change the data type to the desired format

	theta = arccos(z)	#since theta = r*cos(z), and r = 1 in a unit sphere.
	phi = arctan(np.divide(y,x))# and x = r*sin(theta)*cos(phi); y = r*sin(theta)*sin(phi)
	phi = np.nan_to_num(phi)#catches the case of (x=0)&(y=0).
	phi+= np.array( (np.sign(x)-1), dtype=bool)*pi	#if x is positive, then phi is on the RHS of the circle; vice versa.
	return [theta, phi]

#Here's the function that you want to be looking at:
#input your rotation matrices as RotationMatrices
def R_in_Spherical_out(RotationMatrices):
	vList = []
	for R in RotationMatrices:
		vList.append(R_v(R))
	return vList

def writeR(theta, THETA, PHI):
	#(THETA,PHI) gives the axis along which to rotate the sphere in; 
	#theta is the r
	#All of them are in in radians
	x,y,z = spherical_cartesian(THETA, PHI)
	s2 = sin(theta/2)
	q = [cos(theta/2), s2*x, s2*y, s2*z]
	QuatToR(q)
	return QuatToR(q)
