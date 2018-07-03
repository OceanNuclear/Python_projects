from odbAccess import *
import numpy as np
from sys import argv,exit
'''Usage: abq6131 python grainDislocationDensity.py'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rightTrim(input,suffix):
    if (input.find(suffix) == -1):
        input = input + suffix
    return input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def function():

	#specifying paths and jobs
	mypath = 'C:/SIMULIA/Abaqus/Commands/'
	mypathforoutput = 'F:/Group Studies/Work Package 5/RawData/'
	thisjob = 'cube125_1000C_SLOW_4_UVARMb\cube125_1000C_SLOW_4_UVARMb.odb'
	
	#useful definitions and important initialisations
	
	spaces = '   '
	odb = openOdb(path = thisjob)
	
	print('functioning')

	elemsets = odb.rootAssembly.instances['PART-1-1'].elementSets

	my_csys = odb.rootAssembly.DatumCsysByThreePoints(name='my_csys', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0), point1=(1, 0, 0), point2=(0, 1, 0))
	
	frameNoList = [1,2,3,4,8,12,20,30]
	for frameNo in frameNoList:
		
		print frameNo
		
		outputText = []
		
		for i in range(len(elemsets)):
			
			elemset = elemsets['GRAIN_'+ str(i+1)]
			#silly for loop but cba to unindent
			
			for a in range (0,1):
				step = odb.steps.values()[0]
				#print 'Processing Step:',step.name
				
				frames = step.frames
				
				frame = frames[frameNo]
				
				#print ('hasnt failed yet')
				
				#define dislocation field for each of the 12 slip systems... I could have made this a list for easier iteration in the future...
				
				SDVFieldList = []
				
				for fieldNo in range(12): 
				
					SDVFieldList.append(frame.fieldOutputs['SDV'+str(573+fieldNo)].getSubset(region = elemset))
				
				maxShearStress = 0
				
				for integrationPoints in range(len(SDVFieldList[0].values)):
					
					for SDVField in SDVFieldList:
						
						if (np.abs(SDVField.values[integrationPoints].data) > maxShearStress):
						
							maxShearStressFound = np.abs(SDVField.values[integrationPoints].data)
					
					maxShearStress = maxShearStress + maxShearStressFound / len(SDVFieldList[0].values)
						
				print ('max Shear Stress in grain ' + str(i+1) + ' = ' + str(maxShearStress) + '\n' )
				#outputText.append('GRAIN_' + str(i+1) +spaces+str(sum)+'\n')
				outputText.append(str(maxShearStress)+'\n')
				
		
		outFile_ev = open(mypathforoutput + "MaxShearStresses_" + str(frameNo+60) + "UnaxialNew.txt",'w')
		
		print 'reaches past outputting code' 
		
		for n in range(len(outputText)):
		
			outFile_ev.write(outputText[n])			
			
		outFile_ev.close()
	
	odb.close()
	
if __name__ == '__main__':
	
	function()	