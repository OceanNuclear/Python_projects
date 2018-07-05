#!/home/oceanw/anaconda3/bin/python
#This file contains mathematical functions to convert between quaternions and Rotation Matrices,
#as well as converting between coordinate systems.
import numpy as np
import random as rn
from numpy import sqrt, sin, cos, arccos, pi, arctan, arcsin
tau = 2*pi
from numpy import array as ary
from quat import *
from generalLibrary import *



plotHistogram=False
quaternion=True
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
	linearProjection(f(z))=g(z) = length of belt(z)	#because number of distinct states at z ∝ length of belt at z
	sin(f(rn.uniform(-1,1))) = 
	#where f(x) happens to be the inverse of d/dx (sin(x)); does it matter?
known:	freq(r=linearProjection(f(z)))/sqrt(1-r**2) = const
for quaternion case:
wanted:	probability density of that quaternion ∝ w^2 #because number of distinct states at w
'''

RadList = []
AngList = []
RadList2= []
AngList2= []

def linearProjector(theta, phi):
	radius = sin(theta)
	return ary([radius, phi])

for x in range (1000):
	if quaternion==True:
		q = np.zeros(4)
		'''
		#Density of state of theta_w must vary as sin(theta_w);
		theta_w = 2*arccos(rn.uniform(0,1))
		#theta_w = rn.uniform(0,pi)
		#where theta_w is the number of radian to rotate around the axis chosen in the next block of code.
		'''
		#shortcut version of commented out block above.
		w = rn.uniform(0,1)
		q[0] = w
		#Choose the axis of rotation at random
		THETA, PHI = randomPointOnSphere()
		q[1:]= sqrt(1-w**2)*spherical_cartesian(THETA,PHI)

		x,y,z = Q_v(q)	#Project the z axis.
		theta, phi = cartesian_spherical(x,y,z)
	else:
		theta, phi = randomPointOnSphere()
	Rad, Ang = linearProjector(theta,phi)
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

if plotHistogram==False:
	ax1 = fig.add_subplot(211, projection='polar')
	ax2 = fig.add_subplot(212, projection='polar')
	
	ax1.scatter(AngList, RadList,  color = 'b', marker='.', label = 'original top down view')
	ax2.scatter(AngList2,RadList2, color = 'r', marker='.', label = 'rotated view')

if plotHistogram==True:
	ax1 = fig.add_subplot(211)
	ax2 = fig.add_subplot(212)	

	#plot the bins
	numBin= 50
	freq1, range1, dummy = ax1.hist(RadList , bins=numBin)
	freq2, range2, dummy = ax2.hist(RadList2, bins=numBin)
	classmark1 = range1[:-1]+np.diff(range1)
	classmark2 = range2[:-1]+np.diff(range2)

	#create density of state to get a constant straight line.
	def density(classmark):
		return 1/sqrt(1-(classmark**2))

	ax1.plot(classmark1, freq1/density(classmark1))
	ax2.plot(classmark2, freq2/density(classmark2))

plt.savefig(picName)

'''
Conclusion:
The procedure for making points on a sphere are as follows:
1. Generate phi uniformly.
2. Generate theta independant from phi
3. Apply a transformation on theta (theta = f(theta)) such that it fits the probability distribution.

Therefore by reverse engineering we can produce random quaternions using the folllowing method:
1. Pick an axis using the existing random point on a sphere function.
2. Generate the amount of rotation to be applied (theta)
3. Scale theta to fit the probability distribution function. (we want probability distribution of w)
	By educated trial and error, theta_w = 2*arccos(rn.uniform(0,1))
	and is explained by the fact that cos((2*arccos(rand_var))/2)= linear distribution of random variable.
	In other words, we want a linear distribution of w in the range of 0 to 1.
4. Generate the relevant quaternion.
'''
