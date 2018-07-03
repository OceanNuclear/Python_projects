from odbAccess import *
from quat import *
import numpy as np
from sys import argv,exit
'''Usage: abq6131 python extractRotations.py'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rightTrim(input,suffix):
    if (input.find(suffix) == -1):
        input = input + suffix
    return input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def RootSumSq(array):
	summation = 0
	for x in np.ravel(array):
		summation += x**2
	return np.sqrt(summation)

def CheckUnity(array, varName):
	if abs(RootSumSq(array)-1)>1000:
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

I = np.identity(3)
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

def QuatToR(q):
	
	#CheckIfQuaternion(q)
	#CheckUnity(q, "Quaternion")
	
	theta = 2 * np.arccos(q[0])

	R = np.identity(3)
	if theta!=0:
		axis = q[1:]/np.sin(theta/2)
		CheckUnity(axis, "unit axis")

		R[0][0] -= 2*( q[2]**2 + q[3]**2)
		R[1][1] -= 2*( q[1]**2 + q[3]**2)
		R[2][2] -= 2*( q[1]**2 + q[2]**2)
		R[0][1] -= 2*( q[0]*q[3]-q[1]*q[2])
		R[0][2] -= 2*(-q[0]*q[2]-q[1]*q[3])
		R[1][0] -= 2*(-q[0]*q[3]-q[1]*q[2])
		R[1][2] -= 2*( q[0]*q[1]-q[2]*q[3])
		R[2][0] -= 2*( q[0]*q[2]-q[1]*q[3])
		R[2][1] -= 2*(-q[0]*q[1]-q[2]*q[3])

	return R


def avgQ(QList):
	
	averageQuaternion = [0,0,0,0]
	
	for i in QList:
		averageQuaternion[0] = averageQuaternion[0] + i[0]
		averageQuaternion[1] = averageQuaternion[1] + i[1]
		averageQuaternion[2] = averageQuaternion[2] + i[2]
		averageQuaternion[3] = averageQuaternion[3] + i[3]
		
	modQ = averageQuaternion[0]*averageQuaternion[0] + averageQuaternion[1]*averageQuaternion[1] + averageQuaternion[2]*averageQuaternion[2] + averageQuaternion[3]*averageQuaternion[3]
	modQ = np.sqrt(modQ)
	
	averageQuaternion[0] = averageQuaternion[0]/modQ
	averageQuaternion[1] = averageQuaternion[1]/modQ
	averageQuaternion[2] = averageQuaternion[2]/modQ
	averageQuaternion[3] = averageQuaternion[3]/modQ
	
	return averageQuaternion
'''
def RotToQuat(R):  #R is local variable containg the rotation matrix
   
   w=0
   x=1
   y=0
   z=0
   s=0

   if( (1 + R[0,0] + R[1,1] + R[2,2])> 0.0001 ):
       s = np.sqrt(1 + R[0,0] + R[1,1] + R[2,2])*2   #s=4*w
       w = 0.25 * s
       x = ( R[2,1] - R[1,2] ) /s
       y = ( R[0,2] - R[2,0] ) /s
       z = ( R[1,0] - R[0,1] ) /s

   elif((R[0,0] > R[1,1])and(R[0,0] > R[2,2])):
       s = np.sqrt( 1.0 + R[0,0] - R[1,1] - R[2,2] )*2  #s=4*x
       w = (R[2,1] - R[1,2]) /s
       x = 0.25 * s
       y = (R[0,1] + R[1,0]) /s
       z = (R[0,2] + R[2,0]) /s
     
   elif(R[1,1] > R[2,2]):
       s = np.sqrt( 1.0 + R[1,1] - R[0,0] - R[2,2] )*2 #s=4*y
       w = (R[0,2] - R[2,0]) /s
       x = (R[0,1] + R[1,0]) /s
       y = 0.25 * s
       z = (R[1,2] + R[2,1]) /s

   else:
       s = np.sqrt( 1.0 + R[2,2] - R[0,0] - R[1,1] )*2  #s=4*z
       w = (R[1,0] - R[0,1]) /s
       x = (R[0,2] + R[2,0]) /s
       y = (R[1,2] + R[2,1]) /s
       z = 0.25 * s		   
	   
   return([w,x,y,z])
'''
def RotToQuat(R):	#By Ocean Wong
	I = np.identity(3)	#Initiate identity matrix
	A = (I-R)/2			#A = (I-R)/2 is simply a simplicifcation formula made by me, so I don't have to deal with an extra factor of 2 below.
	Tr = np.clip(np.trace(A),0,2)#Mathematically Tr is always in the range of 0-2, but Abaqus may exceed it due to rounding errors.
	A0,A1,A2 = np.clip(np.diag(A),0,1)	#Get the diagonal components
	
	x2 = Tr/2 -A0	#get x^2, y^2, z^2, w^2
	y2 = Tr/2 - A1
	z2 = Tr/2 - A2
	w2 = 1-Tr/2
	q = np.sqrt(np.clip([w2,x2,y2,z2],0,1)#At this stage everything is positive.
	#Everything below this line is for extracting the correct signs.
	aSymm = (A.T-A)/2
	wx = aSymm[2][1]
	wy = aSymm[0][2]
	sz = aSymm[1][0]
	
	sign = np.sign([1,wx,wy,wz])#assert that w is always positive.
	sign[1:] = [1 if x>=0 else -1 for x in sign[1:]]#turn zeros into +ve as well to account of the identity matrix (i.e. no rotation) case.
	return sign*q

def function():
	#specifying paths and jobs
	
	mypath = 'C:/SIMULIA/Abaqus/Commands/'
	mypathforoutput = '//ADF/Storage/B/M/BXM430/LiterallyEveryPoint/'
	thisjob = 'cube125_1000C_SLOW_4_UVARMb/cube125_1000C_SLOW_4_UVARMb.odb'
	#useful definitions and important initialisations
	spaces = '   '
	odb = openOdb(path = thisjob)
	
	print('functioning')
	#defining the model sets
	elemSets = odb.rootAssembly.instances['PART-1-1'].elementSets
	#only looking at the field outputs for the first frame of the model
	frameNo = 0
	for step in odb.steps.values():
		
		for frame in step.frames:
			outputText = []
			frameNo = frameNo+1
			print "processing frame",frameNo
			#create list of list of integers, number of elements in that list is the number of elements in the model
			
			DataListList = []
			
			#print len(DataListList)	#Commented away this line because you already know it prints out zero every time.
			
			fieldOUTPUTS = frame.fieldOutputs
			
			for i in range(len(elemSets)):
			
				elemSet = elemSets['GRAIN_' + str(i+2)]
				
				GrainList = []
				#number of integration points to Rmatrixes for: 
				
				for j in range(len(fieldOUTPUTS['UVARM1'].getSubset(region = elemSet).values)):
					
					newList = []
					RMatrix = np.zeros(shape = (3,3))
					#specifying the UVARMS to look at...
					
					for k in range(9):

						RVal = fieldOUTPUTS['UVARM'+ str(k+1)].getSubset(region = elemSet).values[j].data
						
						newList.append(RVal)
						#here i will now convert the grain list to a quaternion... step 1: convert list of 9 numbers to 3x3 numpy array
					
					RMatrix[1][1]= newList[1]
					RMatrix[1][2]= newList[8]
					RMatrix[1][0]= newList[3]
					
					RMatrix[2][0]= newList[5]
					RMatrix[2][1]= newList[7]
					RMatrix[2][2]= newList[2]
					
					RMatrix[0][0]= newList[0]
					RMatrix[0][1]= newList[4]
					RMatrix[0][2]= newList[6]
					
					quaternion = RotToQuat(RMatrix)
					
					GrainList.append(quaternion)
				'''	
				averageQuaternion = medianQuat(GrainList)[0]
				
				ResultMatrix = QuatToR(averageQuaternion)
				
				print ResultMatrix
				print "Chosen grain has Ind =",medianQuat(GrainList)[2],"and has avg. misor. =",medianQuat(GrainList)[1],"rad from the other 7 pts, max misor. =",medianQuat(GrainList)[3]

				DataListList.append(ResultMatrix)
				
				#print('GRAIN_' + str(i+1) + ': ' + str(str(DataListList[i]) + '\n'))
				
				outputText.append(str(ResultMatrix[0][0])+'   '+str(ResultMatrix[1][0]) +'   '+str(ResultMatrix[2][0]) + '\n')
				outputText.append(str(ResultMatrix[0][1])+'   '+str(ResultMatrix[1][1]) +'   '+str(ResultMatrix[2][1]) + '\n')
				outputText.append(str(ResultMatrix[0][2])+'   '+str(ResultMatrix[1][2]) +'   '+str(ResultMatrix[2][2]) + '\n')
				'''
				for quaternion in GrainList:	#made it print out every single quaternion instead.
					ResultMatrix = QuatToR(quaternion)
					DataListList.append(ResultMatrix)
					outputText.append(str(ResultMatrix[0][0])+ '\t' +str(ResultMatrix[1][0]) + '\t' +str(ResultMatrix[2][0]) + '\n')
					outputText.append(str(ResultMatrix[0][1])+ '\t' +str(ResultMatrix[1][1]) + '\t' +str(ResultMatrix[2][1]) + '\n')
					outputText.append(str(ResultMatrix[0][2])+ '\t' +str(ResultMatrix[1][2]) + '\t' +str(ResultMatrix[2][2]) + '\n')
			
			outFile_ev=open(mypathforoutput + str(frameNo) + "FrameRotationMatrices.txt",'w')
			
			for n in range(len(outputText)):
				
				outFile_ev.write(outputText[n])
			
			outFile_ev.close()

	
	odb.close()

if __name__ == '__main__':
	
	function()	
