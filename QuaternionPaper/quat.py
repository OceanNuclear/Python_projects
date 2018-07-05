#!/home/oceanw/anaconda3/bin/python
#This file contains mathematical functions to convert between quaternions and Rotation Matrices,
#as well as converting between coordinate systems.
import numpy as np
import random as rn
from numpy import sqrt, sin, cos, arccos, pi, arctan
tau = 2*pi
from numpy import array as ary



'''
#Function by Will Mead
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
'''
def RotToQuat(R):		#My version of the function to turn a rotation matrix into a quaternion
	I = np.identity(3)	# = identity matrix.
	A = (I-R)/2		
	#This A = (I-R)/2 formula is simply a simplification done by me; so that I don't have to deal with an extra factor of -2 when trying to find solutions.
	#From now on I only have to deal with the matrix A.
	Tr = np.clip(np.trace(A),0,2)	#Mathematically Tr is always in the range of 0 to 2; but Abaqus sometimes output matrices that violate this rule (slightly), leading to error further down the line.
	#Therefore np.clip is used to prevent it from exceeding these bounds.
	A0,A1,A2 = np.clip(np.diag(A),0,1)	#Get the diagonal components.

	x2 = (Tr-2*A0)/2	#x2,y2,z2 are all squares
	y2 = (Tr-2*A1)/2
	z2 = (Tr-2*A2)/2
	w2 = 1-Tr/2
	q = sqrt(np.clip([w2,x2,y2,z2], 0,1))	#Again clip it to prevent numbers larger than zero going under.
	#Note sqrt returns positive no. only, so the sign needs to be sorted out as below:

	aSymm = (A.T-A)/2	#aSymm means the asymmetric component of matrix A.
	wx = aSymm[2][1]	#Find w*x, w*y, w*z, for the sole purpose of finding the correct sign to return the quaternion in.
	wy = aSymm[0][2]	#w should always be +ve, so w*x, w*y, w*z should be of the sign x,y,z.
	wz = aSymm[1][0]

	sign = np.sign([1,wx,wy,wz])	#The sign of w is always +ve.
	sign[1:] = [1 if x>=0 else -1 for x in sign[1:]]	#list comprehension to catch cases where w=0 for the unit vector
	return sign*q	#q consist of positive no. only (see line 59)

def spherical_cartesian(theta, phi):	#simple conversion from spherical to cartesian, assuming r = 1
	x = sin(theta)*cos(phi)
	y = sin(theta)*sin(phi)
	z = cos(theta)
	return ary([x,y,z])

def RotX(theta):	#Rotation matrix to rotate about X axis
	R = np.identity(3)
	R[1][1] = cos(theta)
	R[2][2] = cos(theta)
	R[1][2] =-sin(theta)
	R[2][1] = sin(theta)
	return R

def RotY(theta):	#Rotation matrix to rotate about Y axis
	R = np.identity(3)
	R[0][0] = cos(theta)
	R[2][2] = cos(theta)
	R[2][0] =-sin(theta)
	R[0][2] = sin(theta)
	return R

def RotZ(theta):	#Rotation matrix to rotate about Z axis
	R = np.identity(3)
	R[0][0] = cos(theta)
	R[1][1] = cos(theta)
	R[0][1] =-sin(theta)
	R[1][0] = sin(theta)
	return R

def cartesian_spherical(x, y, z):	#cartesian unit vectors input spherical output.
	x,y,z = ary(np.clip([x,y,z],-1,1), dtype=float) #change the data type to the desired format

	Theta = arccos((z))
	Phi = arctan(np.divide(y,x))	#This division is going to give nan if (x,y,z) = (0,0,1)
	Phi = np.nan_to_num(Phi)	#Therefore assert phi = 0 if (x,y) = (0,0)
	Phi+= ary( (np.sign(x)-1), dtype=bool)*pi #if x is positive, then phi is on the RHS of the circle; vice versa.
	return ary([Theta, Phi])

def RootSumSq(array):			#Again, root sum square function commonly found in physical mathematics.
	summation = [x**2 for x in np.ravel(array)]
	return sqrt(sum(summation))
#Root sum square is such a commonly used function in physics, I don't know why there isn't an in-built module containing it.

def normalize(v):	#I don't think it's necessary to say what does it do?
	return v/RootSumSq(v)

def CheckUnity(array, varName="quarternion"):	#For debugging purpose, check that something's RootSumSq is 1.
	if abs(RootSumSq(array)-1)>2e-05:
		raise ValueError("This",varName,"component's root sum squares is not unity!")
	return

def CheckIfVector(v):	#For debugging purpose again.
	if np.shape(v)!=(3,):
		raise TypeError("This is not a vector!")
	return

def CheckIfQuaternion(q):	#Check that something has four component for debugging purpose.
	if np.shape(q)!=(4,):
		raise TypeError("This is not a quaternion!")
	return

def Check(condition, message="Generic error message"):	#General check function
	if not condition:
		raise TypeError(message)
	return

def cross (u, v):	#Cross product of two vectors.
	CheckIfVector(u)
	CheckIfVector(v)
	x = u[1]*v[2] - u[2]*v[1]
	y = u[2]*v[0] - u[0]*v[2]
	z = u[0]*v[1] - u[1]*v[0]
	return ary([x,y,z])

def dot (u,v):		#Dot product for same-length vector
	summation = [u[n]*v[n] for n in range (len(u))]
	return sum(summation)

def inverse(q):	#find the inverse of a quaternion
	qinv = ary([q[0], -q[1], -q[2], -q[3]])
	qinv = qinv/(RootSumSq(q)**2)
	return qinv

def multiply(p, q):	#mulitplication of quaternions.
	a = p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3] #product of w minus dot product of axes.
	x = p[2]*q[3] - p[3]*q[2] + p[0]*q[1] + q[0]*p[1] #cross product of axes plus cross-multiply coefficient to the axes.
	y = p[3]*q[1] - p[1]*q[3] + p[0]*q[2] + q[0]*p[2]
	z = p[1]*q[2] - p[2]*q[1] + p[0]*q[3] + q[0]*p[3]
	return ary([a,x,y,z])

def dotQ(p,q):	#dot product of two four component vectors.
	CheckIfQuaternion(p)
	CheckIfQuaternion(q)
	return ( p[0]*q[0] + p[1]*q[1] + p[2]*q[2] + p[3]*q[3] )

q0 = ary([1,0,0,0])	#Quaternion representing no rotation.

def QuatToRotation(q):	#Quaternions to verbal description that expresses
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
	return ary([theta, axis])

def Q_ThreeVar(q):
	theta = 2*arccos(np.clip(q[0],-1,1))
	s2 = sin(theta/2)
	x, y, z = ary(q)[1:]/s2
	THETA, PHI = cartesian_spherical(x,y,z)
	return ary([theta,THETA,PHI])

def QuatToR(q):
	theta = 2 * arccos(np.clip(q[0],-1,1))

	R = np.identity(3)
	if theta>2E-5 or abs(theta-pi)>2E-5: # theta_prime not approaching 0 or pi
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

def ThreeVar_Q(ThreeVar):	#Form a quaternion from THETA,PHI(axis orientation) and theta(angle of rotation) only
	[theta, THETA, PHI] = ThreeVar	#unpack the variables
	x,y,z = spherical_cartesian(THETA, PHI)	#convert to cartesian
	s2 = sin(theta/2)	#get multiplication factor
	q = [cos(theta/2), s2*x, s2*y, s2*z]	#create quaternion
	return q

def writeR(theta, THETA, PHI):	#input ThreeVar and ouput a string representing the Rotation Matrix
	#Used for random generation of variable

	#(THETA,PHI) gives the axis along which to rotate the sphere in; 
	#theta is the r
	#All of them are in in radians
	x,y,z = spherical_cartesian(THETA, PHI)
	s2 = sin(theta/2)
	q = [cos(theta/2), s2*x, s2*y, s2*z]
	R = QuatToR(q)
	return writeMatrix(R)

def writeMatrix(R):
	line1 = str(R[0][0])+'\t'+str(R[0][1])+'\t'+str(R[0][2])
	line2 = str(R[1][0])+'\t'+str(R[1][1])+'\t'+str(R[1][2])
	line3 = str(R[2][0])+'\t'+str(R[2][1])+'\t'+str(R[2][2])
	return line1+"\n"+line2+"\n"+line3+"\n"

def matrixMulti(A,B):	#Matrix mulitplication when np.linalg.multi_dot doesn't work (Netshape building computers do not have the np.linalg module)
	#optional: check that these two matrices are two dimentional and has the same dimension
	#if np.shape(A)[1]!=np.shape(B)[0]: raise TypeError
	#if (ary(A).ndim!=2) or (ary(B).ndim!=2): raise TypeError
	vertical=np.shape(A)[0]
	across = np.shape(B)[1]

	C = np.zeros([vertical, across])

	for down in range (vertical):
		for right in range (across):
			for n in range (len(B)):
				C[down][right] += A[down][n]*B[n][right]
	return C

def outerProduct(u,v):	#Find the outerproduct of two vectors, irrespective of their length
	matrix = np.zeros([len(u),len(v)])
	for down in range (len(u)):
		for across in range (len(v)):
			matrix[down][across] = u[down]*v[across]
	return matrix
		

def averageQuat(qList):	#Average quaternion finding method by the NASA paper
	#Recently corrected (after handing the project) and therefore has yet to be tested.
	qList = ary(qList)	#convert to numpy array in case it isn't already one.
	#CheckIfQuaternion(qList[1])	#Check that it contains quaternions in the shape of (Mx4).

	Matrix = np.zeros([4,4])
	for q in qList:
		Matrix += outerProduct(q,q)
	#print("the Eigen matrix", Matrix)
	EigenVal, EigenMat= np.linalg.eig(Matrix)
	average = EigenMat.T[np.argmax(EigenVal)]
	return average*np.sign(average[0])	#It may return complex number in the elements if qList is short.

'''
def averageQuatLinAlg(qList):		#well apparently it doesn't require me to use the method of multidot, therefore I have commented out this program
	#Recently corrected (after handing the project) and therefore has yet to be tested.
	qList = ary(qList)
	CheckIfQuaternion(qList[1])	#Check that it contains quaternions in the shape of (Mx4).

	Matrix = np.zeros([4,4])
	for q in qList:
		Matrix += outerProduct(q,q)	
	EigenVal, EigenMat= np.linalg.eig(Matrix)
	average = EigenMat[np.argmax(EigenVal)]
	return normalize(average)
'''

def medianQuat(qList):	#The method of finding the least misoriented quaternion
	qList = ary(qList)
	if (np.shape(qList)[1]!=4): raise TypeError("It's not of the shape (Nx4)!")

	disorder = np.zeros(len(qList))
	for n in range(len(qList)):
		for p in qList:
			disorder[n] += misorientation2(p,qList[n])/(len(qList)-1)
	minInd = np.argmin(disorder)
	return qList[minInd], min(disorder), minInd, max(disorder)
	#return the quaternion with the minimum disorientation and the mean number of radian difference from the rest of the quaternions

def misorientationR(R1, R2):	#Find the misorientation between two Rotation matrices.
	p = RotToQuat(R1)
	q = RotToQuat(R2)
	return misorientation(p,q)

def misorientation(p,q):	#Find the the 1-cos(theta/2) value of misorientation between two quaternions, where theta is the number of degrees around ANY arbitrary directions where we need to rotate the unit sphere around
	product = multiply( p, inverse(q))
	return 1-abs(product[0]) #This will be 0<number<1
	#as it returns 1-cos(theta/2)), where theta is the angle required to turn from p to q.

def misorientation2(p,q):	#Linear scale of misorientation
	differenceRotation = multiply( p,inverse(q) )	#returns a quaternion
	differenceRotation = np.clip(differenceRotation, -1,1)
	#^clips it back to the range of [-1,1] to correct for any floating point division and multiplication problems.
	theta = arccos((differenceRotation[0]**2-0.5)*2)	#This complicated formula is used to ensure that regardless of the sign of differenceRotation[0] we can still get a value of 0<=theta<=2pi.
	return theta	#return the misorientation angle in radian
	#return 1-cos(theta) #scale it nonlinearly instead

'''
def generate111s():	#generate a list of 8 vector pointing to the corners of the cube inscribed in the unit sphere.
	s3 = sqrt(1/3)
	x, y, z = [], [], []
	for n in range (8):
		x.append((-1)**(n>>2) *s3)
		y.append((-1)**(n>>1) *s3)
		z.append((-1)**(n>>0) *s3)
	return ary([x,y,z]).T	#shape is (8,3)
'''

def misorientationSymm(p,q):	#Misorientation program that accounts for crystal symmetry.
		#Shouldn't have to implement it if we're trying to find misorientation between Gauss points in the same grain.
	misor = []
	s2,s3 = sqrt(1/2), sqrt(1/3)
	I = np.identity(3)
	#Lgroup: rotate around the centre of faces.
	LGroup = np.identity(4)
	pos = np.pad(I*s2, ((0,0),(1,0)),'constant', constant_values=s2)
	neg = np.pad(-I*s2,((0,0),(1,0)),'constant', constant_values=s2)
	LGroup = np.concatenate((LGroup, pos, neg))
	order = [0,1,4,7,2,5,8,3,6,9]	#0 is identity, the other 3*3 comes from rotation around the centre of face.
	LGroup = LGroup[order]

	#MGroup: rotate around the edges.
	revIs2 = s2-s2*I
	asymm  = s2-s2*I
	asymm[:,1] = -asymm[:,1]
	asymm[1,0] = -s2
	MGroup = np.pad(np.concatenate((revIs2,asymm)), ((0,0),(1,0)), 'constant', constant_values=0)	#Gives 3*2 symmetries.

	#NGroup: rotate around opposite vertices.
	NGroup = ary([[1,1,1],[1,-1,1],[-1,1,1],[-1,-1,1]])/2
	#normalize by multiplying 1/sqrt(3), then *sin(theta/2)=sqrt(3/4) since theta=n*tau/3
	NGroup = np.concatenate((NGroup, -NGroup))	#Gives (2**2)*2 symmetries.
	NGroup = np.pad(NGroup, ((0,0),(1,0)), 'constant', constant_values=0.5)

	#Compile together the list of 24 symmetries, including the identity.
	SymmList = np.concatenate((LGroup,NGroup,MGroup))	#the three groups combined give all possible symmetries to the cube.

	for RotationalQuat in SymmList:	#indeed there are 24 symmetries.
		pRotated= multiply(p,RotationalQuat) #post multiply the symmetry to p
		misor.append( misorientation2(pRotated,q) ) #Find the misorientation
	minInd = np.argmin(misor)
	return misor[minInd], minInd	#return the minimum no, of degrees required to turn it to the nearest location.

'''
def misorientation4(p,q, method="radian"): #Misorientation between two quaternions, includes crystal symmetry, super computationally-intensive.
	v8 = generate111s() # gives 8 vectors, each pointing to a corner.
	vList1, vList2 = [], []
	for v in v8:
		vList1.append( np.linalg.multidot(QuatToR(q),v) ) #Rotate the pose according to p
		vList2.append( np.linalg.multidot(QuatToR(p),v) ) #and q respectively.
	misor = 0

	if method=="cosine":
	#For each vector in the first rotated pose,
		for u_rotated in vList1:
			#loop through the vectors of the second pose,
			misList =  []
			for v_rotated in vList2:
				#And find the vector in the second pose that gives a dot product with the first closest to 1
				misList.append( 1-dot(u_rotated,_rotated) )
			misor += min(misList)/len(misList)

	if method=="radian":
		for u_rotated in vList1:
			misList =  []

			for v_rotated in vList2:
				misList.append( arccos(np.clip(dot(u_rotated,v_rotated)),-1,1) )
			misor += min(misList)/len(misList)
	return misor
'''

def uglyAverage(qList):	#Simply take the renomalized average.
	qList = ary(qList) #Turn into array if not already one.

	average = np.zeros(4)
	for n in range (4):
		average[n] = np.average(qList[:,n])	#find the average in each column.
	return normalize(average)


def randomQGenerator():
	w = rn.uniform(1,0)		#pick a random angle of rotation
	THETA = arccos(rn.uniform(-1,1))#pick a random THETA, and make sure to scale it appropriately.
	PHI = rn.uniform(0, tau)	#pick a random PHI

	st2 = sqrt(1-w**2)
	x,y,z = spherical_cartesian(THETA,PHI)
	return ary([w, st2*x, st2*y, st2*z])

if __name__=="__main__":	#If this program is run directly then it'll generate random quaternions to be averaged.
	qlist = []
	while True:	#Forever loop
		input("Press enter to generate random rotational quaternion no. "+str(len(qlist)+1))
		q = randomQGenerator() #works on computer were I can import the sphereical_cartesian function only.
		print("q generated=",q)
		#print("\t",(q[1],q[2],q[3])/sin(arccos(q[0]))) # to print the 3D coord of the unit vector.
		R = QuatToR(q)
		#print("R generated=",R)
		qlist.append(q)

		correctAverage = averageQuat(qlist)
		incorrectAvg   = uglyAverage(qlist)
		#incorrectAverage = uglyAverage(qlist)
		print("Eigen Method average thus far yields      ", correctAverage,", length = ", RootSumSq(correctAverage))
		print("Renormalized average thus far yields      ", incorrectAvg , ", legnth = ", RootSumSq(incorrectAvg))
		#print("Primitive averaging method thus far yields", incorrectAverage,RootSumSq(incorrectAverage))
		#print("Difference between their absolute values= ", np.abs(correctAverage)-np.abs(incorrectAverage))
		print("\tThe mis-orientation between q_data and EigenAverage is", multiply(q, correctAverage))
		print("\tThe mis-orientation between EigenAverage and q_data is", multiply(correctAverage, q))
		print("\tCompared with the Renomalized average                 ", multiply(incorrectAvg, q),"\n")	#Compare with ugly average.
