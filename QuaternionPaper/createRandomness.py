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

rn.seed(1998)
def randomPointOnSphere():
	THETA = arccos(rn.uniform(-1,1))#pick a random THETA, and make sure to scale it appropriately.
	#THETA = rn.uniform(0,pi)
	'''
		as observable from the result of linear_seed(1998).png,
		there are two concentrated spots at opposite angles as found in the rotated view,
		suggesting that it is the wrong method;
		while there are no discernable difference between the two views in arccos_seed(1998).png,
		so the arccos method must be more correct.
	'''
	PHI = rn.uniform(0,tau)		#pick a random PHI
	return [THETA, PHI]
'''
For dot on surface of sphere case:
wanted:	sin(arccos(x)) = sqrt(1- x^2)
	sin(f(rand_var))=sqrt(1-rand_var**2)
	sin(f(rand_var))=density of states
	linearProjection(f(z))=g(z) = lenght of belt(z)	#because number of distinct states at z ∝ length of belt at z
for quaternion case:
wanted:	probability density of that quaternion ∝ w^2 #because number of distinct states at w
'''

RadList = []
AngList = []
RadList2= []
AngList2= []

def linearProjector(theta, phi):
	radius = sin(theta)
	return [radius, phi]

for x in range (500):
	##create random quaternion
	##Convert into R
	##Project the z axis.
	#Make the quaternion
	theta, phi = randomPointOnSphere()
	Rad, Ang = linearProjector(theta, phi)
	RadList = np.append(RadList, Rad)
	AngList = np.append(AngList, Ang)

	#create the rotation matrix R for rotating the angle of projection such that I can view it from another angle.
	#If ther pattern is not truely random, the rotated view will show hot-spots at different locations than those in the original view.
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
ax2.scatter(AngList2,RadList2, color = 'r', marker='.', label = 'rotated view')

plt.savefig(picName)
'''
#alternatively do
X, Y = polar2D_xy(AngList, RadList)
return [X,Y]
'''
