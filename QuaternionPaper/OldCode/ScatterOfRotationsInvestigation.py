from odbAccess import *
import numpy as np
#from pyquaternion import Quaternion
from sys import argv,exit
from qart import *

'''Usage: abq6131 python ScatterOfRotations.py'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rightTrim(input,suffix):
    if (input.find(suffix) == -1):
        input = input + suffix
    return input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def addUp(a):
	
	sum = 0

	for element in a:
	
		sum = sum + element

	return sum

def dot(a,b):
	
	product = 0
	
	for i in range(len(a)):
		
		product = product + a[i] * b[i]

	return product
	
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

def ScatterEvolution():

	for i in range(40):
	
		function(i)
   
def function():
	outputText = []
	#specifying paths and jobs
	mypath = 'C:/SIMULIA/Abaqus/Commands/'
	mypathforoutput = 'F:/Group Studies/Work Package 5/RawData/'
	thisjob = 'cube125_1000C_SLOW_4_UVARMb\cube125_1000C_SLOW_4_UVARMb.odb'
	#useful definitions and important initialisations
	spaces = '   '
	odb = openOdb(path = thisjob)
	
	print('functioning')
	#defining the model sets
	elemSets = odb.rootAssembly.instances['PART-1-1'].elementSets
	#only looking at the field outputs for the first frame of the model
	'''frameNo = 0'''
	frameOffSet = 153###TEST
	frameNo = len(odb.steps['Step-1'].frames) + frameOffSet###TEST
	temptime = 1000
	
	'''for stepNo in range(len(odb.steps)):'''
	for stepNo in range(len(odb.steps)-1):###TEST
	
	
		'''step = odb.steps['Step-'+str(stepNo + 1)]'''
		step = odb.steps['Step-'+str(stepNo + 2)]###TEST
		
		
		'''for frame in step.frames:'''
		for f in range(1):###TEST
			frame = step.frames[f + frameOffSet]###TEST
			
			time = temptime + frame.frameValue
			
			frameNo = frameNo + 1
			DataListList = []
			
			#print len(DataListList)
			
			fieldOUTPUTS = frame.fieldOutputs
			
			for i in range(len(elemSets)):
			
			#for i in range(3):
			
				elemSet = elemSets['GRAIN_' + str(i+1)]
				
				#elemSet = elemSets['GRAIN_' + str(i+32)]
				
				
				GrainList = []
				#number of integration points to Rmatrixes for: 
				
				for j in range(8):
					
					RMatrix = np.zeros(shape = (3,3))
					
					#specifying the UVARMS to look at...
					
					newList = []
					
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
					
					#apply function to convert to quaternion
					
					quaternion = RotToQuat(RMatrix)
					
					GrainList.append(quaternion)
					
					if (i==52):
						
						print RMatrix
					
				#now use this list of quaternions to calculate a scatter value
				averageQuaternion = avgQ(GrainList)
				
				#will calculate scatter of quaternions from this average...
				#expression for dist between is 1 - <q1.q2>
				scatter = 0
				
				for q in GrainList:
				
					scatter = scatter + (1 - np.abs(dot(q,averageQuaternion)))
					
					if (1-np.abs(dot(q,averageQuaternion)) > 0.5):
						
						print 'Grain_Number: ' + str(i+1)
						print np.abs(dot(q,averageQuaternion))
						
						QuatToRotation(averageQuaternion)
						QuatToRotation(q)
						'''
						print 'average q: \n'
						print averageQuaternion
						print '\n'
						print 'actual q: \n'
						print q
						print '\n'
						'''
				DataListList.append(scatter)
				#print ('scatter in grain' + str(i) +' ' + str(DataListList[i]))
				
			#sum all elements in the data list. and append to output text
			DataListSum = addUp(DataListList)/1000
			print( str(frameNo) + '  ' + str(DataListSum) + '\n')
			
			outputText.append(str(time)+'  '+str(DataListSum) + '\n')
		
		temptime = time
	'''
	outFile_ev=open(mypathforoutput + "ScatterOverTimeUniaxial.txt",'w')
	
	for n in range(len(outputText)):
			
		outFile_ev.write(outputText[n])			
		
	outFile_ev.close()
	'''
	odb.close()
	
if __name__ == '__main__':
	
	#ScatterEvolution()
	function()	