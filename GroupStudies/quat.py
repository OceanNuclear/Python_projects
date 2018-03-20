#!/home/oceanw/anaconda3/bin/python
import numpy as np
import random as rn
from numpy import sqrt, sin, cos, arccos, pi, arctan
tau = 2*pi
from numpy import array as ary



def RotToQuat(R):
	I = np.identity(3)
	A = (I-R)/2
	Tr = np.clip(np.trace(A),0,2)	#Clip to prevent stupid floating point problems caused by Abaqus to lead to overflow.
	A0,A1,A2 = np.clip(np.diag(A),0,1)	#Get the diagonal
	x = (Tr-2*A0)/2
	y = (Tr-2*A1)/2
	z = (Tr-2*A2)/2
	w = 1-Tr/2
	return sqrt([w,x,y,z])

def spherical_cartesian(theta, phi):
	x = sin(theta)*cos(phi)
	y = sin(theta)*sin(phi)
	z = cos(theta)
	return [x,y,z]

def cartesian_spherical(x, y, z):
	x,y,z = ary(np.clip([x,y,z],-1,1), dtype=float) #change the data type to the desired format

	Theta = arccos((z))
	Phi = arctan(np.divide(y,x))
	Phi = np.nan_to_num(Phi)
	Phi+= ary( (np.sign(x)-1), dtype=bool)*pi #if x is positive, then phi is on the RHS of the circle; vice versa.
	return ary([Theta, Phi])

def RootSumSq(array):
	summation = [x**2 for x in np.ravel(array)]
	return sqrt(sum(summation))

def normalize(v):
	return v/RootSumSq(v)

def CheckUnity(array, varName="quarternion"):
	if abs(RootSumSq(array)-1)>2e-05:
		raise ValueError("This",varName,"component's root sum squares is not unity!")
	return

def CheckIfVector(v):
	if np.shape(v)!=(3,):
		raise TypeError("This is not a vector!")
	return

def CheckIfQuaternion(q):
	if np.shape(q)!=(4,):
		raise TypeError("This is not a quaternion!")
	return

def cross (u, v):
	CheckIfVector(u)
	CheckIfVector(v)
	x = u[1]*v[2] - u[2]*v[1]
	y = u[2]*v[0] - u[0]*v[2]
	z = u[0]*v[1] - u[1]*v[0]
	return [x,y,z]

def dot (u,v):
	summation = [u[n]*v[n] for n in range (len(u))]
	return sum(summation)

def inverse(q):
	qinv = ary([q[0], -q[1], -q[2], -q[3]])
	qinv = qinv/(RootSumSq(q)**2)
	return qinv

def multiply(p, q):
	a = p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3] #product of w minus dot product of axes.
	x = p[2]*q[3] - p[3]*q[2] + p[0]*q[1] + q[0]*p[1] #cross product of axes plus cross-multiply coefficient to the axes.
	y = p[3]*q[1] - p[1]*q[3] + p[0]*q[2] + q[0]*p[2]
	z = p[1]*q[2] - p[2]*q[1] + p[0]*q[3] + q[0]*p[3]
	return [a,x,y,z]

def dotQ(p,q):
	CheckIfQuaternion(p)
	CheckIfQuaternion(q)
	return ( p[0]*q[0] + p[1]*q[1] + p[2]*q[2] + p[3]*q[3] )

q0 = ary([1,0,0,0])

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

def Q_ThreeVar(q):
	theta = 2*arccos(np.clip(q[0],-1,1))
	s2 = sin(theta/2)
	x, y, z = ary(q)[1:]/s2
	THETA, PHI = cartesian_spherical(x,y,z)
	return [theta,THETA,PHI]

def QuatToR(q):
	theta = 2 * arccos(np.clip(q[0],0,pi))

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

def ThreeVar_Q(ThreeVar):
	[theta, THETA, PHI] = ThreeVar	#unpack the variables
	x,y,z = spherical_cartesian(THETA, PHI)	#convert to cartesian
	s2 = sin(theta/2)	#get multiplication factor
	q = [cos(theta/2), s2*x, s2*y, s2*z]	#create quaternion
	return q

def writeR(theta, THETA, PHI):
	#(THETA,PHI) gives the axis along which to rotate the sphere in; 
	#theta is the r
	#All of them are in in radians
	x,y,z = spherical_cartesian(THETA, PHI)
	s2 = sin(theta/2)
	q = [cos(theta/2), s2*x, s2*y, s2*z]
	R = QuatToR(q)
	line1 = str(R[0][0])+'\t'+str(R[0][1])+'\t'+str(R[0][2])
	line2 = str(R[1][0])+'\t'+str(R[1][1])+'\t'+str(R[1][2])
	line3 = str(R[2][0])+'\t'+str(R[2][1])+'\t'+str(R[2][2])
	return line1+"\n"+line2+"\n"+line3+"\n"

def matrixMulti(A,B):
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

def averageQuatLinAlg(qList):
	qList = ary(qList)
	if (np.shape(qList)[1]!=4): raise TypeError#Check that it contains quaternions in the shape of (Mx4).

	Matrix = np.linalg.multi_dot([qList.T,qList])
	EigenVal, EigenMat= np.linalg.eig(Matrix)
	average = EigenMat[np.argmax(EigenVal)]
	return average

def averageQuat(qList):
	qList = ary(qList)
	if (np.shape(qList)[1]!=4): raise TypeError#Check that it contains quaternions in the shape of (Mx4).

	Matrix = matrixMulti(qList.T,qList)
	EigenVal, EigenMat= np.linalg.eig(Matrix)
	average = EigenMat[np.argmax(EigenVal)]
	return normalize(average)

def medianQuat(qList):
	qList = ary(qList)
	if (np.shape(qList)[1]!=4): raise TypeError("It's not of the shape (Nx4)!")

	disorder = np.zeros(len(qList))
	for n in range(len(qList)):
		for p in qList:
			disorder[n] += misorientation2(p,qList[n])/(len(qList)-1)
	minInd = np.argmin(disorder)
	return qList[minInd], min(disorder), minInd, max(disorder)
	#return the quaternion with the minimum disorientation and the mean number of radian difference from the rest of the quaternions

def misorientationR(R1, R2):
	p = RotToQuat(R1)
	q = RotToQuat(R2)
	return misorientation(p,q)

def misorientation(p,q):
	product = multiply( p, inverse(q))
	return 1-abs(product[0]) #This will be 0<number<1
	#as it returns 1-cos(theta/2)), where theta is the angle required to turn from p to q.

def misorientation2(p,q):#Linear scale of misorientation
	differenceRotation = multiply( p,inverse(q) )	#returns a quaternion
	differenceRotation = np.clip(differenceRotation, -1,1)
	#^clips it back to the range of [-1,1] to correct for any floating point division and multiplication problems.
	theta = arccos(differenceRotation[0])*2
	return theta #return the misorientation in radian.
	#return 1-cos(theta) #scale it nonlinearly instead.

def generate111s():
	s3 = sqrt(1/3)
	x, y, z = [], [], []
	for n in range (8):
		x.append((-1)**(n>>2) *s3)
		y.append((-1)**(n>>1) *s3)
		z.append((-1)**(n>>0) *s3)
	return ary([x,y,z]).T	#shape is (8,3)

def misorientationSymm(p,q):	#Create the quaternaion representation of the 
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
	SymmList = np.concatenate((LGroup,NGroup,MGroup))

	for RotationalQuat in SymmList:	#indeed there are 24 symmetries.
		pRotated= multiply(p,RotationQuat) #post multiply the symmetry to p
		misor.append( misorientation2(pRotated,q) ) #Find the misorientation
	minInd = np.argmin(misor)
	return misor[minInd], minInd	#return the minimum no, of degrees required to turn it to the nearest location.

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

def uglyAverage(qList):
	qList = ary(qList).T #Gives a 4xM matrix instead this time.
	average = np.zeros(4)

	for n in range (4):
		average[n]=np.sum(qList[n])
	average = average/RootSumSq(average)
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
		print("\tThe mis-orientation between this q and the average is", multiply((q), correctAverage))
		print("\twhich should be the same as                          ", multiply(correctAverage, q))
		print("Currently there are", len(qlist), "quaternions.\n")
