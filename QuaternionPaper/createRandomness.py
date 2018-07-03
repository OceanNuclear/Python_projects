#!/home/oceanw/anaconda3/bin/python
#This file contains mathematical functions to convert between quaternions and Rotation Matrices,
#as well as converting between coordinate systems.
import numpy as np
import random as rn
from numpy import sqrt, sin, cos, arccos, pi, arctan
tau = 2*pi
from numpy import array as ary
from quat import *
from generalLibrary import *



picName = "randomnessTest/"
picName += str(input("Name of file (w/o .png)?"))
picName += ".png"

def randomPointOnSphere():
	THETA = arccos(rn.uniform(-1,1))#pick a random THETA, and make sure to scale it appropriately.
	PHI = rn.uniform(0,tau)		#pick a random PHI
	return [THETA, PHI]

RadList = []
AngList = []
RadList2= []
AngList2= []

def linearProjector(theta, phi):
	radius = sin(theta)
	return [radius, phi]

for x in range (100):
	##create random quaternion
	##Convert into R
	##Project the z axis.
	#Make the quaternion
	theta, phi = randomPointOnSphere()
	Rad, Ang = linearProjector(theta, phi)
	RadList = np.append(RadList, Rad)
	AngList = np.append(AngList, Ang)

	#create the rotation matrix R for rotating the angle of projection significantly enough for determining if the "random" pattern is random enough or not.
	R = np.zeros([3,3])
	R[0] = [-0.22955971415019039,	-0.016359124925339308,	0.9731570873558699]
	R[1] = [-0.9704505923981576,	0.08022683369058692,	-0.2275726320761089]
	R[2] = [-0.07435042268439407,	-0.9966423802887674,	-0.034292571484097145]

	#theta2 and phi2 are the rotated version of theta and phi respectively.
	x,y,z = np.linalg.multi_dot( [R, spherical_cartesian(theta,phi)])
	theta2, phi2 = cartesian_spherical(x,y,z)
	RadRotated, AngRotated = linearProjector(theta2,phi2)
	RadList2= np.append(RadList2, RadRotated)
	AngList2= np.append(AngList2, AngRotated)

fig = plt.figure()
ax1 = fig.add_subplot(211, projection='polar')
ax2 = fig.add_subplot(212, projection='polar')

ax1.scatter(AngList, RadList,  color = 'b', marker='.', label = 'original top down view')
ax1.title("original top down view")

ax2.scatter(AngList2,RadList2, color = 'r', marker='.', label = 'rotated view')
ax2.title("rotated view")

plt.show()
'''
#alternatively do
X, Y = polar2D_xy(AngList, RadList)
return [X,Y]
'''
