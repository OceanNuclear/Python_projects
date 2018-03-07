#!/home/oceanw/anaconda3/bin/python
from Will import RotToQuat
import numpy as np



def RootSumSq(array):
	summation = 0
	for x in np.ravel(array):
		summation += x**2
	return np.sqrt(summation)

def normalize(v):
	return v/RootSumSq(v)

def CheckUnity(array, varName):
	if abs(RootSumSq(array)-1)>1E-10:
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

def multiply(p, q):
	CheckIfQuaternion(p)
	CheckIfQuaternion(q)
	a = p[0]*q[0] - u[1]*v[1] + u[2]*v[2] + u[3]*v[3]
	x = p[2]*q[3] - p[3]*q[2] + p[0]*q[1] + q[0]*p[1]
	y = p[3]*q[1] - p[1]*q[3] + p[0]*q[2] + q[0]*p[2]
	z = p[1]*q[2] - p[2]*q[1] + p[0]*q[3] + q[0]*p[3]
	return 

def dotQ(p,q):
	CheckIfQuaternion(p)
	CheckIfQuaternion(q)
	return ( p[0]*q[0] + p[1]*q[1] + p[2]*q[2] + p[3]*q[3] )

q0 = np.array([1,0,0,0])
sqrHalf = np.sqrt(1/2)
q1 = np.array([sqrHalf,sqrHalf,0,0])

def QuatToRotation(q):
	CheckIfQuaternion(q)
	CheckUnity(q, "Quaternion")
	theta = 2 * np.arccos(q[0])

	if theta!=0:
		axis = q[1:]/np.sin(theta/2)
		CheckUnity(axis, "unit axis")
	else:
		axis = "not applicable"

	print("\n", "\t", "Rotation by")
	print("\t", 'theta =', np.rad2deg(theta), "degrees")
	print("\t", "axis", axis)
	return [theta, axis]
def QuatToR(q):
	CheckIfQuaternion(q)
	CheckUnity(q, "Quaternion")
	theta = 2 * np.arccos(q[0])

	R = np.identity(3)
	if theta!=0:
		axis = q[1:]/np.sin(theta/2)
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

if __name__=="__main__":
	QuatToRotation(q1)
