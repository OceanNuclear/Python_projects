#!/home/oceanw/anaconda3/bin/python
import numpy as np
import random as rn
from numpy import sqrt, sin, cos, arccos, pi, arctan
tau = 2*pi



#The function below is written by Will, not me.
def RotToQuat(R):  #R is the rotation matrix
	if( ((R[0][0] + R[1][1] + R[2][2]-1))<1E-10 ):
		s = sqrt(1 + R[0][0] + R[1][1] + R[2][2])*2	#s=4*w
		w = 0.25 * s
		x = ( R[2][1] - R[1][2] ) /s
		y = ( R[0][2] - R[2][0] ) /s
		z = ( R[1][0] - R[0][1] ) /s
 
	elif((R[0][0] > R[1][1])and(R[0][0] > R[2][2])): # rotational axis lies on 
		s = sqrt( 1.0 + R[0][0] - R[1][1] - R[2][2] )*2	#s=4*x
		w = (R[2][1] - R[1][2]) /s
		x = 0.25 * s
		y = (R[0][1] + R[1][0]) /s
		z = (R[0][2] + R[2][0]) /s
	  
	elif(R[1][1] > R[2][2]):
		s = sqrt( 1.0 + R[1][1] - R[0][0] - R[2][2] )*2	#s=4*y
		w = (R[0][2] - R[2][0]) /s
		x = (R[0][1] + R[1][0]) /s
		y = 0.25 * s
		z = (R[1][2] + R[2][1]) /s
 
	else:
		s = sqrt( 1.0 + R[2][2] - R[0][0] - R[1][1] )*2	#s=4*z
		w = (R[1][0] - R[0][1]) /s
		x = (R[0][2] + R[2][0]) /s
		y = (R[1][2] + R[2][1]) /s
		z = 0.25 * s
	Q = [w,x,y,z]	#identity matrix equates to [1,0,0,0]
	return Q
#End of function written by Will Mead.

def cartesian_spherical(x, y, z):
	x,y,z = np.array([x,y,z], dtype=float) #change the data type to the desired format

	Theta = arccos(z)
	Phi = arctan(np.divide(y,x))
	Phi = np.nan_to_num(Phi)
	Phi+= np.array( (np.sign(x)-1), dtype=bool)*pi #if x is positive, then phi is on the RHS of the circle; vice versa.
	return np.array([Theta, Phi])

def RootSumSq(array):
	summation = 0
	for x in np.ravel(array):
		summation += x**2
	return sqrt(summation)

def normalize(v):
	return v/RootSumSq(v)

def CheckUnity(array, varName="quarternion"):
	if abs(RootSumSq(array)-1)>1E-9:
		print("This",varName,"component's root sum squares is not unity!")
		raise ValueError
	return

def CheckIfVector(v):
	if np.shape(v)!=(3,):
		print("This is not a vector!")
		raise TypeError
	return

def CheckIfQuaternion(q):
	if np.shape(q)!=(4,):
		print("This is not a quaternion!")
		raise TypeError
	return

def cross (u, v):
	CheckIfVector(u)
	CheckIfVector(v)
	x = u[1]*v[2] - u[2]*v[1]
	y = u[2]*v[0] - u[0]*v[2]
	z = u[0]*v[1] - u[1]*v[0]
	return [x,y,z]

def dot (u,v):
	CheckIfVector(u)
	CheckIfVector(v)
	return (u[0]*v[0] + u[1]*v[1] + u[2]*v[2])

def inverse(q):
	CheckIfQuaternion(q)
	p = np.array([q[0], -q[1], -q[2], -q[3]])
	p = p/(RootSumSq(q)**2)
	return p

def multiply(p, q):
	CheckIfQuaternion(p)
	CheckIfQuaternion(q)
	a = p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3] #product of w minus dot product of axes.
	x = p[2]*q[3] - p[3]*q[2] + p[0]*q[1] + q[0]*p[1] #cross product of axes plus cross-multiply coefficient to the axes.
	y = p[3]*q[1] - p[1]*q[3] + p[0]*q[2] + q[0]*p[2]
	z = p[1]*q[2] - p[2]*q[1] + p[0]*q[3] + q[0]*p[3]
	return [a,x,y,z]

def dotQ(p,q):
	CheckIfQuaternion(p)
	CheckIfQuaternion(q)
	return ( p[0]*q[0] + p[1]*q[1] + p[2]*q[2] + p[3]*q[3] )

q0 = np.array([1,0,0,0])

def QuatToRotation(q):
	CheckIfQuaternion(q)
	CheckUnity(q, "Quaternion")
	theta = 2 * arccos(q[0])

	if theta>2E-5:
		axis = q[1:]/sin(theta/2)
		CheckUnity(axis, "unit axis")
	else:
		axis = "not applicable"

	print("\t", "Rotation by")
	print("\t", 'theta =', np.rad2deg(theta), "degrees")
	print("\t", "axis=", axis)
	return [theta, axis]

def QuatToR(q):
	CheckIfQuaternion(q)
	CheckUnity(q, "Quaternion")
	theta = 2 * arccos(q[0])

	R = np.identity(3)
	if theta>2E-5:
		axis = q[1:]/sin(theta/2)
		CheckUnity(axis, "unit axis")

		R[0][0] -= 2*( q[2]**2  +q[3]**2  )
		R[1][1] -= 2*( q[1]**2  +q[3]**2  )
		R[2][2] -= 2*( q[1]**2  +q[2]**2  )
		R[0][1] -= 2*( q[0]*q[3]-q[1]*q[2])
		R[0][2] -= 2*(-q[0]*q[2]-q[1]*q[3])
		R[1][0] -= 2*(-q[0]*q[3]-q[1]*q[2])
		R[1][2] -= 2*( q[0]*q[1]-q[2]*q[3])
		R[2][0] -= 2*( q[0]*q[2]-q[1]*q[3])
		R[2][1] -= 2*(-q[0]*q[1]-q[2]*q[3])

	return R

def matrixMulti(A,B):
	#optional: check that these two matrices are two dimentional and has the same dimension
	#if np.shape(A)[1]!=np.shape(B)[0]: raise TypeError
	#if (np.array(A).ndim!=2) or (np.array(B).ndim!=2): raise TypeError
	vertical=np.shape(A)[0]
	across = np.shape(B)[1]

	C = np.zeros([vertical, across])

	for down in range (vertical):
		for right in range (across):
			for n in range (len(B)):
				C[down][right] += A[down][n]*B[n][right]
	return C

def averageQuatLinAlg(qList):
	qList = np.array(qList)
	if (np.shape(qList)[1]!=4): raise TypeError#Check that it contains quaternions in the shape of (Mx4).

	Matrix = np.linalg.multi_dot([qList.T,qList])
	EigenVal, EigenMat= np.linalg.eig(Matrix)
	average = EigenMat[np.argmax(EigenVal)]

	#CheckUnity(average)
	#print("Check if ", RootSumSq(average),"is unity.")
	return average

def averageQuat(qList):
	qList = np.array(qList)
	if (np.shape(qList)[1]!=4): raise TypeError#Check that it contains quaternions in the shape of (Mx4).

	Matrix = matrixMulti(qList.T,qList)
	EigenVal, EigenMat= np.linalg.eig(Matrix)
	average = EigenMat[np.argmax(EigenVal)]

	#CheckUnity(average)
	#print("Check if ", RootSumSq(average),"is unity.")
	return average

def misorientationR(R1, R2):
	p = RotToQuat(R1)
	q = RotToQuat(R2)
	return misorientationQ(p,q)

def misorientation(p,q):
	product = multiply(inverse(p),q)
	return 1-abs(product[0]) #This will be a positive number >0 & <1.

def uglyAverage(qList):
	qList = np.array(qList).T #Gives a 4xM matrix instead this time.
	average = np.zeros(4)

	for n in range (4):
		average[n]=np.sum(qList[n])
	average = average/RootSumSq(average)

	#CheckUnity(average)
	#print("Check if ", RootSumSq(average),"is unity.")
	return average


def randomQGenerator():
	phi = rn.uniform(0,tau)
	elevation = arccos(rn.uniform(-1,1))
	THETA = pi/2-elevation
	theta = rn.uniform(0, tau)

	st2=sin(theta/2)
	x,y,z = spherical_cartesian(THETA,phi)
	return [cos(theta/2), st2*x, st2*y, st2*z]

if __name__=="__main__":
	qlist = []
	while True:#Forever loop
		input("Press enter to generate random rotational quaternion")
		q = randomQGenerator() #works on computer were I can import the sphereical_cartesian function only.
		print("q=",q)
		#print("\t",(q[1],q[2],q[3])/sin(arccos(q[0]))) # to print the 3D coord of the unit vector.
		R = QuatToR(q)
		print("R=",R)
		qlist.append(q)
		correctAverage = averageQuatLinAlg(qlist)
		#incorrectAverage = uglyAverage(qlist)
		print("Eigen Method average thus far yields      ", correctAverage,"length = ", RootSumSq(correctAverage))
		#print("Primitive averaging method thus far yields", incorrectAverage,RootSumSq(incorrectAverage))
		#print("Difference between their absolute values= ", np.abs(correctAverage)-np.abs(incorrectAverage))
		print("\tThe mis-orientation between this q and the average is", multiply(inverse(q), correctAverage))
		print("\twhich should be the same as                          ", multiply(correctAverage, q))
		print("Currently there are", len(qlist), "quaternions.\n")
