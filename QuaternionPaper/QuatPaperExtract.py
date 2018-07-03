from odbAccess import *
from quat import *
import numpy as np
from sys import argv,exit
from numpy import pi, sqrt, sin, cos, arccos, pi, arctan
import time

#declare program for writing a matrix to text file.
def writeMatrix(R):
	outputText = ""
	for line in R:
		for element in line:
			outputText += str(element)
			outputText += '\t'
		outputText += '\n'
	return outputText

	#Paths declaration
mypath = 'C:/SIMULIA/Abaqus/Commands/'
savepath=mypath+'HIPModel/'
thisjob = 'cube125_1000C_SLOW_4_UVARMb/cube125_1000C_SLOW_4_UVARMb.odb'
odb = openOdb(thisjob)

#shorthands:
rtAsm = odb.rootAssembly
my_csys=rtAsm.DatumCsysByThreePoints(name="my_csys", coordSysType=CARTESIAN, origin=(0.0,0.0,0.0), point1 = (1,0,0), point2=(0,1,0))
#my_csys is used for finding the strain in the correct frame.
str_dir = 2

#Find the number of grains
numGrain = len(rtAsm.instances['PART-1-1'].elementSets)	#=125 for the test file.
numGauss = len(odb.steps['Step-1'].frames[0].fieldOutputs['LE'].getTransformedField(datumCsys=my_csys).values)/numGrain	#1000/125=8 for the test file.
print "There are ", numGrain, " grains;"
print numGauss, " per grain."
if type(numGauss)!=int: raise ValueError("wrong nubmer of grains")

#Initiating variables to be printed:
frameNo = 0

startTime = time.time()
strainFile = open(savepath+"Strain.txt",'w')
for step in odb.steps.values():
	for frame in step.frames:
		#print(type(frame))
		frameNo += 1
		frameSpecificFieldOutput = frame.fieldOutputs #shorthand, used before all four of the variables.
		
		#Grain dependent files:
		volFile = open(savepath+"Volume_frame"+str(frameNo)+".txt", 'w')
		OriFile = open(savepath+"AverageOrientation_frame"+str(frameNo)+".txt",'w')
		GOSFile = open(savepath+"IntragrainOrientationScatter_frame"+str(frameNo)+".txt", 'w')
		aOrFile = open(savepath+"zzAllOrientation_frame"+str(frameNo)+".txt", 'w')
		
		#Initiating strain variable:
		strainInThisFrame = 0
		for grainID in range (numGrain):
			grain_region = rtAsm.instances['PART-1-1'].elementSets['GRAIN_'+str(grainID+1)]	#For the use of finding the grain regions in the following scenarios.
			print "Processing frameNo = ", frameNo, " grain ID = ", grainID
			#Initiating other variables:
			volume = 0
			Ori	=	np.zeros([numGauss,3,3])
			OriQuat=np.zeros([numGauss,4])
			for gauss in range (numGauss):
				strainInThisFrame += frameSpecificFieldOutput['LE'].getTransformedField(datumCsys=my_csys).values[(grainID*numGauss) + gauss].data[str_dir]
				#volume	+= frameSpecificFieldOutput['EVOL'].getSubset(region=grain_region).values[gauss].data
				
				#Download the matrix elements of each point to form the whole matrix Ori[gauss]
				Ori[gauss][0][0]= frameSpecificFieldOutput['UVARM1'].getSubset(region=grain_region).values[gauss].data
				Ori[gauss][0][1]= frameSpecificFieldOutput['UVARM5'].getSubset(region=grain_region).values[gauss].data
				Ori[gauss][0][2]= frameSpecificFieldOutput['UVARM7'].getSubset(region=grain_region).values[gauss].data
				Ori[gauss][1][0]= frameSpecificFieldOutput['UVARM4'].getSubset(region=grain_region).values[gauss].data
				Ori[gauss][1][1]= frameSpecificFieldOutput['UVARM2'].getSubset(region=grain_region).values[gauss].data
				Ori[gauss][1][2]= frameSpecificFieldOutput['UVARM9'].getSubset(region=grain_region).values[gauss].data
				Ori[gauss][2][0]= frameSpecificFieldOutput['UVARM6'].getSubset(region=grain_region).values[gauss].data
				Ori[gauss][2][1]= frameSpecificFieldOutput['UVARM8'].getSubset(region=grain_region).values[gauss].data
				Ori[gauss][2][2]= frameSpecificFieldOutput['UVARM3'].getSubset(region=grain_region).values[gauss].data
				aOrFile.write(writeMatrix(Ori[gauss]))
				'''
				(Note made on 15th June 2018 by Ocean Wong: I don't think any improvement to the code efficiency can be made by 
				looping through 
					frameSpecificFieldOutput #using a dictionary key
				first before nesting 
					getSubset(region=grain_region[grainID]).values[gauss]	#using a linked list
				in will make a difference in efficiency.)
				'''
				OriQuat[gauss] = RotToQuat(Ori[gauss])	#convert the Ori[gauss] matrix to a quaternion.
			avgOriQuat = averageQuat(OriQuat)
			GOS = 0
			#Caculating Grain orientation scatter:
			for gauss in range (numGauss):
				GOS += misorientation2( avgOriQuat,OriQuat[gauss] )/numGauss
			
			#writing to file
			volFile.write(str(volume)+'\n')
			OriFile.write(writeMatrix(QuatToR(avgOriQuat)))
			if GOS is not 0j:	#to prevent the '0j's found in frameNo==1, which will lead to errors when reading the file.
				GOSFile.write(str(GOS)+'\n')
			else: GOSFile.write(str(0)+'\n')
		volFile.close()
		OriFile.close()
		GOSFile.close()
		
		strainFile.write(str(strainInThisFrame/(numGrain*numGauss))+'\n')
strainFile.close()

#printing debugging/monitoring messages
print "Processed steps = ", frameNo, ";"
odb.close()
print "time taken to finish = ", time.time()-startTime,"s"
# #print "Written ", len(), " lines."